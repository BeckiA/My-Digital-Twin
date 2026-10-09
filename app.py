"""Digital Twin Gradio Application.

This application runs an interactive digital twin representing your career,
background, and skills using the Agents SDK (Agent + Runner) with function tools
for recording user interest and unknown questions via Pushover.
"""

import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
import gradio as gr

# Enable system certificate validation for Windows/corporate proxies
try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

# Load environment variables early
load_dotenv(override=True)

from context import TWIN_SYSTEM_PROMPT
from helpers.pushover import push
from styles import CSS, JS, EXAMPLES


# -----------------------------------------------------------------------------
# LLM Provider Configuration
# -----------------------------------------------------------------------------
def get_model() -> OpenAIChatCompletionsModel:
    """Configures and returns the OpenAIChatCompletionsModel based on environment.

    Defaults to Google Gemini as the primary provider, with dynamic support
    for Ollama, Groq, OpenAI, and OpenRouter via the LLM_PROVIDER environment variable.
    """
    provider = os.getenv("LLM_PROVIDER", "").lower().strip()

    # Auto-detect default provider if not explicitly specified
    if not provider:
        if os.getenv("GEMINI_API_KEY"):
            provider = "gemini"
        elif os.getenv("OPENAI_API_KEY"):
            provider = "openai"
        elif os.getenv("GROQ_API_KEY"):
            provider = "groq"
        elif os.getenv("OPENROUTER_API_KEY"):
            provider = "openrouter"
        else:
            provider = "ollama"

    print(f"[Digital Twin] Initializing LLM provider: {provider}")

    if provider == "gemini":
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set in your .env file.")

        gemini_client = AsyncOpenAI(
            base_url=os.getenv(
                "GEMINI_BASE_URL",
                "https://generativelanguage.googleapis.com/v1beta/openai/",
            ),
            api_key=gemini_api_key,
        )
        model_name = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")
        return OpenAIChatCompletionsModel(
            model=model_name,
            openai_client=gemini_client,
        )

    elif provider == "ollama":
        ollama_client = AsyncOpenAI(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
        )
        model_name = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        return OpenAIChatCompletionsModel(
            model=model_name,
            openai_client=ollama_client,
        )

    elif provider == "groq":
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY is not set in your .env file.")

        groq_client = AsyncOpenAI(
            base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
            api_key=groq_api_key,
        )
        model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        return OpenAIChatCompletionsModel(
            model=model_name,
            openai_client=groq_client,
        )

    elif provider == "openrouter":
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY is not set in your .env file.")

        openrouter_client = AsyncOpenAI(
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            api_key=openrouter_api_key,
        )
        model_name = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat")
        return OpenAIChatCompletionsModel(
            model=model_name,
            openai_client=openrouter_client,
        )

    elif provider == "openai":
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set in your .env file.")

        openai_client = AsyncOpenAI(
            base_url=os.getenv("OPENAI_BASE_URL"),
            api_key=openai_api_key,
        )
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return OpenAIChatCompletionsModel(
            model=model_name,
            openai_client=openai_client,
        )

    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER '{provider}'. "
            "Supported options: 'gemini', 'ollama', 'groq', 'openrouter', 'openai'."
        )


# -----------------------------------------------------------------------------
# Function Tools
# -----------------------------------------------------------------------------
@function_tool
def record_user_details(
    email: str,
    name: str = "Name not provided",
    notes: str = "not provided",
) -> str:
    """Use this tool to record that a user is interested in being in touch and provided an email address."""
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return "OK"


@function_tool
def record_unknown_question(question: str) -> str:
    """Always use this tool to record any question that couldn't be answered as you didn't know the answer."""
    push(f"Recording {question} asked that I couldn't answer")
    return "OK"


# -----------------------------------------------------------------------------
# Agent Definition
# -----------------------------------------------------------------------------
model = get_model()

agent = Agent(
    name="digi-twin",
    model=model,
    instructions=TWIN_SYSTEM_PROMPT,
    tools=[record_user_details, record_unknown_question],
)


# -----------------------------------------------------------------------------
# Chat Interface Logic
# -----------------------------------------------------------------------------
def extract_text(content) -> str:
    """Extract plain text string from string, dictionary, or Gradio content block lists."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        return " ".join(
            part.get("text", "")
            for part in content
            if isinstance(part, dict) and "text" in part
        )
    elif isinstance(content, dict):
        return content.get("text", str(content))
    return str(content) if content is not None else ""


async def chat(message: str, history: list) -> str:
    """Handles chat message interaction by delegating to the agent Runner."""
    messages = []

    # 1. Parse and sanitize conversation history from Gradio
    for turn in history:
        if isinstance(turn, dict):
            role = turn.get("role", "user")
            content = extract_text(turn.get("content", ""))
            if content:
                messages.append({"role": role, "content": content})
        elif isinstance(turn, (list, tuple)) and len(turn) == 2:
            user_text = extract_text(turn[0])
            assistant_text = extract_text(turn[1])
            if user_text:
                messages.append({"role": "user", "content": user_text})
            if assistant_text:
                messages.append({"role": "assistant", "content": assistant_text})

    # 2. Add current user message
    user_message_text = extract_text(message)
    if user_message_text:
        messages.append({"role": "user", "content": user_message_text})

    # 3. Execute agent loop asynchronously
    result = await Runner.run(agent, messages)
    return result.final_output


# -----------------------------------------------------------------------------
# Gradio Application
# -----------------------------------------------------------------------------
demo = gr.ChatInterface(
    chat,
    examples=EXAMPLES,
    title="Digital Twin",
    description="Talk to my AI twin about my career",
    chatbot=gr.Chatbot(show_label=False),
)

if __name__ == "__main__":
    server_name = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    share = os.getenv("GRADIO_SHARE", "False").lower() in ("true", "1")

    demo.launch(
        server_name=server_name,
        server_port=server_port,
        share=share,
        css=CSS,
        js=JS,
        theme=gr.themes.Base(),
    )
