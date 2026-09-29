from llm import ask

SYSTEM = (
    "You are a flight search assistant. Use web search to find current flight options. "
    "Give 2-3 options with airline, approximate price in USD, duration and stops. "
    "If exact prices are unavailable, give an estimated range and say it is an estimate. "
    "Be concise."
)


def run(bb):
    r = bb.read("request")
    prompt = (
        f"Find round-trip flights from {r['origin']} to {r['location']} "
        f"around {r['time']} for a {r['duration']}-day trip."
    )
    bb.write("flights", ask(SYSTEM, prompt, use_search=True))