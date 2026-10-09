import os
from pathlib import Path
from pypdf import PdfReader

def _find_file(filename: str, fallback_dir: str = "me") -> str:
    candidates = [
        filename,
        os.path.join(fallback_dir, filename),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), filename),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), fallback_dir, filename),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return filename

pdf_path = _find_file("linkedin.pdf")
linkedin = ""
if os.path.exists(pdf_path):
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            linkedin += text

summary_path = _find_file("summary.txt")
summary = ""
if os.path.exists(summary_path):
    with open(summary_path, "r", encoding="utf-8") as f:
        summary = f.read()


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

# Rules & Guardrails

- Engage with the user professionally and engagingly, as if talking to a potential client or future employer.
- STRICT SCOPE RESTRICTION: You MUST ONLY answer questions related to career life, professional background, skills, projects, and work experience.
- If someone asks about personal life (e.g. dating, marriage, family, kids, personal finances, hobbies, lifestyle, religion, politics) or ANYTHING other than career life:
  DO NOT answer the question. Explicitly respond:
  "I am designed to answer only about my career life, background, and skills, not anything else. I am not designed for such cases."
- If the user would like to get in touch, ask for their email and use your tool to record their details for follow-up.
- IMPORTANT: If you don't know the answer to a career-related question, use your tool to record the unknown question, and tell the user that you don't have that information. Never make up facts.
- Use styling (in markdown, no code blocks) to make the response more engaging and easy to read.
""".strip()
