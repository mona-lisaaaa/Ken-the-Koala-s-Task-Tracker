import streamlit as st
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
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 0
if 'remaining' not in st.session_state:
    st.session_state.remaining = 0
if 'paused' not in st.session_state:
    st.session_state.paused = False

# --- Format seconds as MM:SS ---
def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}"

# --- Handle start ---
if start:
    try:
        # Interpret all digits as minutes (e.g., 0130 = 130 minutes)
        minutes = int(time_input)
        total_seconds = minutes * 60
        if total_seconds > 0:
            st.session_state.total_seconds = total_seconds
            st.session_state.remaining = total_seconds
            st.session_state.running = True
            st.session_state.paused = False
    except ValueError:
        st.error("Please enter a valid number like '0130' for 130 minutes.")

# --- Handle pause ---
if pause:
    st.session_state.running = False
    st.session_state.paused = True

# --- Handle reset ---
if reset:
    st.session_state.running = False
    st.session_state.paused = False
    st.session_state.remaining = st.session_state.total_seconds

# --- Timer logic ---
if st.session_state.running and st.session_state.remaining > 0:
    while st.session_state.remaining > 0 and st.session_state.running:
        # Display timer
        timer_display.markdown(f"<div class='timer-text'>⏳ {format_time(st.session_state.remaining)}</div>", unsafe_allow_html=True)

        time.sleep(1)
        st.session_state.remaining -= 1
        st.experimental_rerun()

# --- When time's up ---
if st.session_state.remaining == 0 and st.session_state.total_seconds != 0:
    heart_slot.markdown("<div class='heart'>💙</div>", unsafe_allow_html=True)
    koala_slot.markdown("<div class='km'>K + M</div>", unsafe_allow_html=True)
    timer_display.markdown(f"<div class='timer-text'>⏳ 00:00</div>", unsafe_allow_html=True)
    st.success("Great work bb I'm so proud of you —love, Mona 💖")
    st.session_state.total_seconds = 0
    st.session_state.running = False
