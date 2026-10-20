"""Digital Twin Core Agent Module.

Encapsulates LLM provider configuration, function tools (Pushover alerts),
career scope guardrails, and conversation runner logic for both streaming
and non-streaming interfaces.
"""

import os
from typing import AsyncGenerator, Dict, List, Optional
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

    print(f"[Digital Twin Agent] Initializing LLM provider: {provider}")

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
    clean_name = name.strip() if name and name != "Name not provided" else ""
    if clean_name:
        return f"Recorded successfully. Reply to the user: Thank you, {clean_name}! I've successfully recorded your details. Bereket will be in touch with you soon!"
    return "Recorded successfully. Reply to the user: Thank you! I've successfully recorded your details. Bereket will be in touch with you soon!"


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
# Runner Wrappers (Streaming & Non-Streaming)
# -----------------------------------------------------------------------------
async def run_twin(messages: List[Dict[str, str]]) -> str:
    """Runs a complete conversation turn and returns final text."""
    try:
        result = await Runner.run(agent, messages)
        if hasattr(result, "final_output_as"):
            return result.final_output_as(str)
        return str(getattr(result, "final_output", ""))
    except InputGuardrailTripwireTriggered:
        return GUARDRAIL_REFUSAL_MESSAGE
    except Exception as e:
        print(f"[Digital Twin] Runner error: {e}")
        return f"An error occurred: {e}"


async def stream_twin(messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
    """Streams delta chunks from the twin agent for real-time SSE output."""
    yielded_any = False
    try:
        result = Runner.run_streamed(agent, messages)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event, "data"):
                # ONLY stream actual assistant text output deltas!
                # Explicitly ignore function_call_arguments deltas so raw JSON is never leaked.
                event_type = getattr(event.data, "type", "")
                if event_type == "response.output_text.delta" or type(event.data).__name__ == "ResponseTextDeltaEvent":
                    delta = getattr(event.data, "delta", None)
                    if isinstance(delta, str) and delta:
                        yielded_any = True
                        yield delta
            elif event.type == "run_item_stream_event" and hasattr(event, "item"):
                item = getattr(event, "item", None)
                if item is not None and getattr(item, "type", "") == "message_output_item":
                    raw_item = getattr(item, "raw_item", None)
                    if raw_item is not None:
                        extracted = ItemHelpers.extract_text(raw_item)
                        if extracted and not yielded_any:
                            yielded_any = True
                            yield extracted

        # Fallback if no deltas were captured during streaming
        if not yielded_any and hasattr(result, "final_output_as"):
            final_out = result.final_output_as(str)
            if final_out:
                yield final_out
    except InputGuardrailTripwireTriggered:
        yield GUARDRAIL_REFUSAL_MESSAGE
    except Exception as e:
        print(f"[Digital Twin] Streaming error: {e}")
        yield f"An error occurred: {e}"
