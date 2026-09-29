from blackboard import Blackboard
from agents import planner, budget, output


def main():
    request = {
        "location": input("Destination: ").strip() or "Dubai",
        "origin": input("Departing from: ").strip() or "Cairo",
        "time": input("When (month/season): ").strip() or "December",
        "duration": input("Duration (days): ").strip() or "5",
    }
    bb = Blackboard()
    planner.run(bb, request)   # flights + hotels + activities
    budget.run(bb)             # budget + Excel file
    print("\n" + output.run(bb))


if __name__ == "__main__":
    main()