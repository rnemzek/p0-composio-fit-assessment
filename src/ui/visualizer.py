import os
import streamlit as st
import time

st.title("Big Sexy's Agent Monitor")
log_file = "logs/agent_activity.log"

if os.path.exists(log_file):
    with open(log_file, "r") as f:
        st.code(f.read())

else:
    st.warning(f"Searching for: {os.path.abspath(log_file)}")
    st.info("Run 'python3 main.py' in another terminal to start the agent!")

# Displaying the log in a scrolling code block
log_spot = st.empty()

while True:
    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
            log_spot.code("".join(lines[-15:])) # Show last 15 actions
    except FileNotFoundError:
        log_spot.error("Log file not found. Start main.py first!")
    time.sleep(1)

