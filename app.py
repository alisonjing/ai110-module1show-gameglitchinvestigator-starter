import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮", layout="centered")

# ── Custom UI Styling ──────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Animated gradient background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    background-size: 400% 400%;
    animation: gradientShift 10s ease infinite;
}

@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Main content card */
[data-testid="stVerticalBlock"] {
    background: rgba(255, 255, 255, 0.04);
    border-radius: 16px;
    padding: 8px;
}

/* Title styling */
h1 {
    color: #ffffff !important;
    text-align: center;
    font-size: 2.8rem !important;
    text-shadow: 0 0 20px #a855f7, 0 0 40px #6366f1;
    letter-spacing: 2px;
}

/* Subheader */
h3 {
    color: #c4b5fd !important;
    text-align: center;
}

/* Score display */
.score-box {
    background: linear-gradient(135deg, #6366f1, #a855f7);
    border-radius: 12px;
    padding: 12px 24px;
    text-align: center;
    color: white;
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #a855f7) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: bold !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6) !important;
}

/* Text input */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(168, 85, 247, 0.5) !important;
    border-radius: 10px !important;
    color: white !important;
    font-size: 1.1rem !important;
    text-align: center !important;
}

/* Caption text */
.stCaption, p {
    color: #a5b4fc !important;
}

/* General text */
label, .stMarkdown p {
    color: #e0e7ff !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🎮 Game Glitch Investigator")
st.markdown(
    "<p style='text-align:center; color:#a5b4fc; font-size:1rem;'>"
    "An AI-generated guessing game — fixed and ready to play.</p>",
    unsafe_allow_html=True
)

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 10,  #FIX, increased # of tries based on level of difficulty
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown(
    f"<div class='score-box'>⭐ Score: {st.session_state.score}</div>",
    unsafe_allow_html=True
)

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. " # dynamic range reflects selected difficulty
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 1          # reset attempt counter to 1 for new game using using Claude Agent mode
    st.session_state.secret = random.randint(low, high)  # use difficulty range, not hardcoded 1–100 using Claude Agent mode
    st.session_state.score = 0             # reset score so new game starts fresh using Claude Agent mode
    st.session_state.status = "playing"    # clear won/lost so st.stop() doesn't fire immediately using Claude Agent mode
    st.session_state.history = []          # clear guess history for new game using Claude Agent mode
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
