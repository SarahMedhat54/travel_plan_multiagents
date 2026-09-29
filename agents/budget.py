import json
from openpyxl import Workbook
from llm import ask

SYSTEM = (
    "You are a travel budget analyst. Read the trip info and estimate costs in USD. "
    "Return ONLY valid JSON in this exact shape: "
    '{"items": [{"category": "Flights|Hotels|Activities|Other", "item": "text", "cost_usd": number}]}'
)


def run(bb):
    r = bb.read("request")
    prompt = (
        f"Trip: {r['origin']} -> {r['location']}, {r['duration']} days, {r['time']}.\n\n"
        f"FLIGHTS:\n{bb.read('flights')}\n\n"
        f"HOTELS:\n{bb.read('hotels')}\n\n"
        f"ACTIVITIES:\n{bb.read('activities')}\n\n"
        "Pick one realistic option per category, count hotel nights, and list every cost."
    )
    raw = ask(SYSTEM, prompt, json_mode=True).strip()
    raw = raw[raw.find("{"): raw.rfind("}") + 1]
    items = json.loads(raw)["items"]
    total = sum(i["cost_usd"] for i in items)

    wb = Workbook()
    ws = wb.active
    ws.title = "Budget"
    ws.append(["Category", "Item", "Cost (USD)"])
    for i in items:
        ws.append([i["category"], i["item"], i["cost_usd"]])
    ws.append(["", "TOTAL", f"=SUM(C2:C{len(items) + 1})"])
    wb.save("trip_budget.xlsx")

    bb.write("budget", {"items": items, "total_usd": total})