import streamlit as st
from blackboard import Blackboard
from agents import flight, hotel, activities, budget, output

st.set_page_config(page_title="Travel Planner", page_icon="✈️")
st.title("✈️ AI Travel Planner")

with st.form("trip"):
    col1, col2 = st.columns(2)
    origin = col1.text_input("Departing from", "Cairo")
    location = col2.text_input("Destination", "Dubai")
    time_ = col1.text_input("When (month/season)", "December")
    duration = col2.number_input("Duration (days)", 1, 30, 5)
    go = st.form_submit_button("Plan my trip")

if go:
    bb = Blackboard()
    bb.write("request", {
        "origin": origin,
        "location": location,
        "time": time_,
        "duration": str(duration),
    })

    steps = [
        ("Searching flights...", flight),
        ("Searching hotels...", hotel),
        ("Finding activities...", activities),
    ]
    try:
        for label, agent in steps:
            with st.spinner(label):
                agent.run(bb)

        tab1, tab2, tab3 = st.tabs(["Flights", "Hotels", "Activities"])
        tab1.markdown(bb.read("flights"))
        tab2.markdown(bb.read("hotels"))
        tab3.markdown(bb.read("activities"))

        with st.spinner("Calculating budget..."):
            budget.run(bb)
        st.metric("Estimated total (USD)", f"${bb.read('budget')['total_usd']:,.0f}")

        with open("trip_budget.xlsx", "rb") as f:
            st.download_button("Download budget (Excel)", f, "trip_budget.xlsx")

        with st.spinner("Writing your final plan..."):
            plan = output.run(bb)
        st.divider()
        st.subheader("Your trip plan")
        st.markdown(plan)

    except Exception as e:
        st.error(f"Something went wrong: {e}")