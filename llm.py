import os
import time
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIStatusError, APIConnectionError

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)
MODELS = [
    m.strip()
    for m in os.getenv("GROQ_MODELS", "openai/gpt-oss-120b").split(",")
    if m.strip()
]


def ask(system: str, prompt: str, use_search: bool = False, json_mode: bool = False) -> str:
    # Groq has no web search here, so tell the model not to call any tool
    system = (
        system.replace("Use web search to find", "Based on your knowledge, suggest")
        + " You have no tools and no internet access. Never call a tool. "
        "Answer directly from your own knowledge and label all prices as estimates."
    )
    if json_mode:
        system += " Respond with raw JSON only, no markdown, no explanation."

    for model in MODELS:
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model=model,
                    max_tokens=2000,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                )
                text = response.choices[0].message.content
                if text:
                    return text
                break
            except RateLimitError:
                print(f"[{model}] Rate limited, retry {attempt + 1}/3...")
                time.sleep(5 * (attempt + 1))
            except APIConnectionError:
                print(f"[{model}] Connection problem, retry {attempt + 1}/3...")
                time.sleep(2 * (attempt + 1))
            except APIStatusError as e:
                print(f"[{model}] Error {e.status_code}: {str(e)[:150]}")
                if e.status_code == 400 and "tool" in str(e):
                    continue  # model tried to call a tool, retry the same model
                break

    raise RuntimeError(
        "All models failed. Check your GROQ_API_KEY and the model name in .env."
    )