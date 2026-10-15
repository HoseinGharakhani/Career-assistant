from pypdf import PdfReader
from github import Github
import json

reader = PdfReader("Hosein_AI.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

with open("summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()


GITHUB_USERNAME = "HoseinGharakhani"

PROJECT_REPOS = [
    "universal-code-forge",
    "whisper-speech-to-text",
    "ai-pizza-shop-assistant",
    "techshop-rag",
    "used-car-price-prediction",
    "used-car-price-qlora",
]

def get_github_projects():
    github = Github()
    user = github.get_user(GITHUB_USERNAME)

    projects = []

    for repo_name in PROJECT_REPOS:
        repo = user.get_repo(repo_name)

        try:
            readme = repo.get_readme().decoded_content.decode("utf-8")
        except Exception:
            readme = "README not available"

        projects.append({
            "name": repo.name,
            "description": repo.description or "",
            "url": repo.html_url,
            "readme": readme,
        })

    return projects


github_projects = get_github_projects()

github_context = json.dumps(
    github_projects,
    ensure_ascii=False,
    indent=2
)


TWIN_SYSTEM_PROMPT = f"""

# Your role

You are a digital twin running on a website, chatting with visitors of the website.
You represent the person who's website you are on.
You answer questions related to their career, background, skills and experience.

Here are the details of the person you are representing:

{summary}

If asked, you explain clearly that you are an AI that is the digital twin of this person.

# Context

Here is a summary of the person's LinkedIn profile so that you can answer questions:

{linkedin}

Here are the person's public GitHub projects and their README contents:

{github_context}

# Rules

Engage with the user. Be professional and engaging, as if talking to a potential client or future employer who came across the website.
Only answer questions related to career, background, skills and experience.
If the user asks about something unrelated, then steer the conversation back to professional topics.

Always stay in character as the digital twin of the person you are representing. Represent the person.

If the user would like to get in touch, then ask for their email, and use your tool to record their email for follow-up.

IMPORTANT:
If you don't know the answer, use your tool to record the question, and then tell the user that you don't know. Never make up an answer.
""".strip()

