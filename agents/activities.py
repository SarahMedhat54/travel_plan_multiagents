from llm import ask

SYSTEM = (
    "You are a local activities expert. Use web search to find current attractions and "
    "experiences. Suggest 5-8 activities with name, approximate cost in USD, and recommended "
    "time needed. Consider the season of the trip. Be concise."
)


def run(bb):
    r = bb.read("request")
    prompt = (
        f"Suggest activities in {r['location']} for a {r['duration']}-day trip "
        f"around {r['time']}."
    )
    bb.write("activities", ask(SYSTEM, prompt, use_search=True))