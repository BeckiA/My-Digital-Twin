"""Digital Twin Gradio Application.

This application runs an interactive digital twin representing your career,
background, and skills using the Agents SDK (Agent + Runner) with function tools
for recording user interest and unknown questions via Pushover.
"""

import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    function_tool,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    ItemHelpers,
)
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
from styles import CSS, JS, EXAMPLES, HERO_HTML, FOOTER_HTML


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
# Guardrails & Agent Definition
# -----------------------------------------------------------------------------
GUARDRAIL_REFUSAL_MESSAGE = (
    "I am designed to answer only about my career life, background, and skills, "
    "not anything else. I am not designed for such cases."
)

model = get_model()

# Classifier agent to strictly evaluate if a user query belongs to career scope
scope_guardrail_evaluator = Agent(
    name="career_scope_evaluator",
    model=model,
    instructions=(
        "You are a strict guardrail classifier for a professional career Digital Twin.\n"
        "Your role is to verify whether the user's message is strictly relevant to professional career topics.\n\n"
        "ALLOWED:\n"
        "- The person's professional career, work history, jobs, projects, technical skills, tech stack, education, portfolio.\n"
        "- Inquiries about hiring, collaboration, getting in touch, and professional contact details.\n"
        "- Standard professional greetings and introductions (e.g., hello, hi, who are you, what can you do).\n\n"
        "BLOCKED:\n"
        "- Personal life inquiries: dating, romance, marital status, family, children, private life, personal wealth/finances, personal hobbies, religious beliefs, lifestyle, medical information.\n"
        "- Unrelated general topics: general trivia, homework, recipes, entertainment, sports, politics, creative writing unrelated to career.\n\n"
        "Output ONLY one word: either 'ALLOWED' or 'BLOCKED'."
    ),
)


def extract_latest_user_text(input_data) -> str:
    """Extracts the latest user query text from the input payload."""
    if isinstance(input_data, str):
        return input_data
    if isinstance(input_data, list):
        for item in reversed(input_data):
            if isinstance(item, dict) and item.get("role") == "user":
                content = item.get("content", "")
                if isinstance(content, str):
                    return content
                elif isinstance(content, list):
                    return " ".join(
                        part.get("text", "")
                        for part in content
                        if isinstance(part, dict) and "text" in part
                    )
            elif isinstance(item, str):
                return item
    return str(input_data)


@input_guardrail(name="career_scope_guardrail", run_in_parallel=False)
async def career_scope_guardrail(ctx, target_agent, input_data) -> GuardrailFunctionOutput:
    """Enforces that the digital twin only discusses career and professional topics."""
    user_text = extract_latest_user_text(input_data).strip()
    if not user_text:
        return GuardrailFunctionOutput(output_info="Empty message", tripwire_triggered=False)

    # 1. Fast heuristic check for obvious personal life keywords
    personal_keywords = [
        "girlfriend", "boyfriend", "wife", "husband", "spouse", "married",
        "dating", "relationship", "dating life", "love life", "personal life",
        "kids", "children", "personal salary", "religion", "political view"
    ]
    lower_text = user_text.lower()
    if any(kw in lower_text for kw in personal_keywords):
        return GuardrailFunctionOutput(
            output_info="Personal life question detected via keyword rule",
            tripwire_triggered=True,
        )

    # 2. Contextual LLM evaluation for scope boundaries
    try:
        eval_result = await Runner.run(scope_guardrail_evaluator, user_text)
        decision = eval_result.final_output.strip().upper()
        is_blocked = "BLOCKED" in decision
        return GuardrailFunctionOutput(
            output_info=f"Classifier decision: {decision}",
            tripwire_triggered=is_blocked,
        )
    except Exception as e:
        print(f"[Guardrail] Scope evaluation note: {e}")
        # Allow main agent (with prompt guardrails) to handle on evaluation error
        return GuardrailFunctionOutput(output_info="Fallback on error", tripwire_triggered=False)


agent = Agent(
    name="digi-twin",
    model=model,
    instructions=TWIN_SYSTEM_PROMPT,
    tools=[record_user_details, record_unknown_question],
    input_guardrails=[career_scope_guardrail],
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


async def chat(message: str, history: list):
    """Handles chat message interaction via Runner.run_streamed() with streaming text response."""
    # 1. Immediate visual feedback
    yield "Avatar is typing ..."

    messages = []

    # 2. Parse and sanitize conversation history from Gradio
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

    # 3. Add current user message
    user_message_text = extract_text(message)
    if user_message_text:
        messages.append({"role": "user", "content": user_message_text})

    response_text = ""
    # 4. Execute agent loop with streaming and guardrail tripwire enforcement
    try:
        result = Runner.run_streamed(agent, messages)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event, "data"):
                delta = getattr(event.data, "delta", None)
                if isinstance(delta, str) and delta:
                    response_text += delta
                    yield response_text
            elif event.type == "run_item_stream_event" and hasattr(event, "item"):
                raw_item = getattr(event.item, "raw_item", None)
                if raw_item is not None:
                    extracted = ItemHelpers.extract_text(raw_item)
                    if extracted and extracted != response_text:
                        response_text = extracted
                        yield response_text

        # Fallback if no deltas were streamed
        if not response_text and hasattr(result, "final_output_as"):
            final_out = result.final_output_as(str)
            if final_out:
                yield final_out

    except InputGuardrailTripwireTriggered:
        yield GUARDRAIL_REFUSAL_MESSAGE
    except Exception as e:
        print(f"[Digital Twin] Streaming error: {e}")
        yield f"An error occurred: {e}"


# -----------------------------------------------------------------------------
# Gradio Application
# -----------------------------------------------------------------------------
with gr.Blocks(
    title="Bereket Abera · Digital Twin",
    fill_height=False,
) as demo:
    gr.HTML(HERO_HTML)
    gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        chatbot=gr.Chatbot(
            show_label=False,
            elem_classes=["twin-chat"],
            height=160,
        ),
        textbox=gr.Textbox(
            placeholder="Message Bereket's twin…",
            show_label=False,
            container=False,
            lines=1,
            max_lines=6,
            elem_classes=["twin-input"],
            elem_id="twin-message",
            submit_btn="Send",
        ),
        fill_height=False,
    )
    gr.HTML(FOOTER_HTML)

if __name__ == "__main__":
    server_name = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    share = os.getenv("GRADIO_SHARE", "False").lower() in ("true", "1")

    demo.launch(
        server_name=server_name,
        server_port=server_port,
        share=share,
        theme=gr.themes.Base(),
        css=CSS,
        js=JS,
    )
