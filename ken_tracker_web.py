import streamlit as st
from datetime import datetime, timedelta
import time

# --- Page setup ---
st.set_page_config(page_title="Ken the Koala's Task Tracker", layout="centered")
st.markdown(
    """
    <style>
        .title-text {
            font-size: 28px;
            color: white;
            text-align: center;
            font-family: Courier;
        }
        .timer-text {
            font-size: 48px;
            color: white;
            text-align: center;
            font-family: Courier;
        }
        .heart {
            font-size: 70px;
            text-align: center;
        }
        .km {
            font-size: 24px;
            color: white;
            margin-top: -60px;
            text-align: center;
            font-family: Courier;
        }
        .stApp {
            background-color: #aed6f1;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title ---
st.markdown("<div class='title-text'>🐨 Ken the Koala's Task Tracker</div>", unsafe_allow_html=True)

# --- Timer state ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'end_time' not in st.session_state:
    st.session_state.end_time = None
if 'paused_remaining' not in st.session_state:
    st.session_state.paused_remaining = 0
if 'timer_completed' not in st.session_state:
    st.session_state.timer_completed = False

# --- Input fields ---
task = st.text_input("Task", "Enter your task here 📝")
time_input = st.text_input("Enter time in minutes", "Enter time here ⏰")

# --- Control buttons ---
col1, col2, col3 = st.columns(3)
start = col1.button("🐰 start")
pause = col2.button("🦊 pause")
reset = col3.button("🦕 reset")

# --- Timer display slots ---
heart_slot = st.empty()
koala_slot = st.empty()
timer_display = st.empty()

# --- Format time ---
def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02}"

# --- Start button ---
if start:
    try:
        minutes = int(time_input)
        duration = minutes * 60

        if st.session_state.paused_remaining > 0:
            duration = st.session_state.paused_remaining

        st.session_state.end_time = datetime.now() + timedelta(seconds=duration)
        st.session_state.running = True
        st.session_state.timer_completed = False
        st.session_state.paused_remaining = 0

    except ValueError:
        st.error("Please enter a valid number like '25' for 25 minutes.")

# --- Pause button ---
if pause and st.session_state.running:
    remaining = int((st.session_state.end_time - datetime.now()).total_seconds())
    st.session_state.paused_remaining = max(0, remaining)
    st.session_state.running = False

# --- Reset button ---
if reset:
    st.session_state.running = False
    st.session_state.end_time = None
    st.session_state.paused_remaining = 0
    st.session_state.timer_completed = False

# --- Timer logic ---
remaining_seconds = 0
if st.session_state.running and st.session_state.end_time:
    remaining_seconds = int((st.session_state.end_time - datetime.now()).total_seconds())

    if remaining_seconds <= 0:
        st.session_state.running = False
        st.session_state.end_time = None
        st.session_state.paused_remaining = 0
        st.session_state.timer_completed = True
        remaining_seconds = 0

elif st.session_state.paused_remaining > 0:
    remaining_seconds = st.session_state.paused_remaining

# --- Display timer ---
if st.session_state.running or remaining_seconds > 0:
    timer_display.markdown(f"<div class='timer-text'>⏳ {format_time(remaining_seconds)}</div>", unsafe_allow_html=True)

# --- Completion message ---
if st.session_state.timer_completed:
    heart_slot.markdown("<div class='heart'>🐨</div>", unsafe_allow_html=True)
    koala_slot.markdown("<div class='km'>K + M</div>", unsafe_allow_html=True)
    timer_display.markdown("<div class='timer-text'>⏳ 00:00:00</div>", unsafe_allow_html=True)
    st.success("Great work bb I'm so proud of you —love, Mona 💖")
    st.session_state.timer_completed = False  # reset for next run

# --- Refresh every second if running ---
if st.session_state.running:
    time.sleep(1)
    st.experimental_rerun()

