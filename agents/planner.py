import time
from agents import flight, hotel, activities


def run(bb, request: dict):
    """Writes the request, then runs the three agents one after another."""
    bb.write("request", request)
    for agent in (flight, hotel, activities):
        agent.run(bb)
        time.sleep(1)  # be gentle with the API