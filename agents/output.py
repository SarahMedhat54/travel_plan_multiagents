from llm import ask

SYSTEM = (
    "You are a travel concierge. Using the provided research, write a clear final trip plan: "
    "a short overview, recommended flight, recommended hotel, a day-by-day itinerary, "
    "and the budget summary. Use headings and be practical."
)


def run(bb) -> str:
    data = bb.read_all()
    prompt = (
        f"REQUEST: {data['request']}\n\n"
        f"FLIGHTS:\n{data['flights']}\n\n"
        f"HOTELS:\n{data['hotels']}\n\n"
        f"ACTIVITIES:\n{data['activities']}\n\n"
        f"BUDGET: {data['budget']}"
    )
    plan = ask(SYSTEM, prompt)
    with open("trip_plan.md", "w", encoding="utf-8") as f:
        f.write(plan)
    return plan