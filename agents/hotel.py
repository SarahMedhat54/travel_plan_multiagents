from llm import ask

SYSTEM = (
    "You are a hotel search assistant. Use web search to find good hotels. "
    "Give 3 options (budget, mid-range, luxury) with name, area, approximate price per night "
    "in USD and one line on why it is good. Be concise."
)


def run(bb):
    r = bb.read("request")
    prompt = (
        f"Recommend hotels in {r['location']} for a {r['duration']}-night stay "
        f"around {r['time']}."
    )
    bb.write("hotels", ask(SYSTEM, prompt, use_search=True))