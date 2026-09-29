class Blackboard:
    """Shared memory: every agent reads from it and writes only to its own key."""

    def __init__(self):
        self.data = {
            "request": {},       # origin, location, time, duration
            "flights": None,     # written by the flight agent
            "hotels": None,      # written by the hotel agent
            "activities": None,  # written by the activities agent
            "budget": None,      # written by the budget agent
        }

    def write(self, key: str, value):
        self.data[key] = value
        print(f"[Blackboard] Written: {key}")

    def read(self, key: str):
        return self.data.get(key)

    def read_all(self) -> dict:
        return self.data