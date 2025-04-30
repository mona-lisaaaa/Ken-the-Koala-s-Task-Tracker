import streamlit as st
import time
from datetime import datetime, timedelta

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

# --- Session state initialization ---
if 'running' not in st.session_state:
    st.session_state.running = False
if 'end_time' not in st.session_state:
    st.session_state.end_time = None
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 0
if 'paused_remaining' not in st.session_state:
    st.session_state.paused_remaining = 0

# --- Format seconds as HH:MM ---
def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours:02}:{minutes:02}"

# --- Handle start ---
if start:
    try:
        minutes = int(time_input)
        total_seconds = minutes * 60
        if total_seconds > 0:
            st.session_state.total_seconds = total_seconds
            st.session_state.end_time = datetime.now() + timedelta(seconds=total_seconds)
            st.session_state.running = True
    except ValueError:
        st.error("Please enter a valid number like '90' for 90 minutes.")

# --- Handle pause ---
if pause and st.session_state.running:
    st.session_state.paused_remaining = (st.session_state.end_time - datetime.now()).total_seconds()
    st.session_state.running = False

# --- Handle reset ---
if reset:
    st.session_state.running = False
    st.session_state.end_time = None
    st.session_state.paused_remaining = 0

# --- Timer logic ---
remaining_time = 0
if st.session_state.running and st.session_state.end_time:
    remaining_time = int((st.session_state.end_time - datetime.now()).total_seconds())
    if remaining_time <= 0:
        remaining_time = 0
        st.session_state.running = False

elif not st.session_state.running and st.session_state.paused_remaining:
    remaining_time = int(st.session_state.paused_remaining)

# --- Display Timer ---
if st.session_state.total_seconds > 0:
    timer_display.markdown(f"<div class='timer-text'>⏳ {format_time(remaining_time)}</div>", unsafe_allow_html=True)

# --- When time's up ---
if remaining_time == 0 and st.session_state.total_seconds > 0:
    heart_slot.markdown("<div class='heart'>💙</div>", unsafe_allow_html=True)
    koala_slot.markdown("<div class='km'>K + M</div>", unsafe_allow_html=True)
    timer_display.markdown(f"<div class='timer-text'>⏳ 00:00</div>", unsafe_allow_html=True)
    st.success("Great work bb I'm so proud of you —love, Mona 💖")
    st.session_state.total_seconds = 0
    st.session_state.end_time = None
    st.session_state.paused_remaining = 0

# --- Auto-refresh every second if running ---
if st.session_state.running:
    time.sleep(1)
    st.experimental_rerun()
