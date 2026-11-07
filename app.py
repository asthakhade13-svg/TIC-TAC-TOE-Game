import streamlit as st
import numpy as np
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="Tic-Tac-Toe",
    page_icon="🎮",
    layout="centered"
)

# --- Custom Styling ---
st.markdown("""
<style>
    /* App container spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 520px;
    }

    /* Scoreboard cards */
    .score-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        font-weight: bold;
    }
    @media (prefers-color-scheme: dark) {
        .score-card {
            background-color: #262730;
        }
    }

    /* Board buttons */
    div[data-testid="column"] button {
        height: 90px !important;
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        margin-bottom: 8px !important;
        transition: all 0.2s ease-in-out;
    }

    /* Primary action buttons */
    button[kind="primary"] {
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Game Logic Helper Functions ---
def init_game():
    st.session_state.board = np.zeros((3, 3), dtype=int)  # 1 for X, -1 for O, 0 for empty
    st.session_state.current_turn = 1                      # 1 is X, -1 is O
    st.session_state.winner = None                         # 'X', 'O', 'Draw', or None
    st.session_state.winning_combo = []                    # [(r, c), ...]

def check_game_state(b):
    """
    Checks if there's a winner or a draw on board `b`.
    Returns (winner, winning_coordinates) where winner is 'X', 'O', 'Draw', or None.
    """
    # Check rows
    for r in range(3):
        row_sum = np.sum(b[r, :])
        if row_sum == 3:
            return 'X', [(r, 0), (r, 1), (r, 2)]
        if row_sum == -3:
            return 'O', [(r, 0), (r, 1), (r, 2)]

    # Check columns
    for c in range(3):
        col_sum = np.sum(b[:, c])
        if col_sum == 3:
            return 'X', [(0, c), (1, c), (2, c)]
        if col_sum == -3:
            return 'O', [(0, c), (1, c), (2, c)]

    # Check main diagonal
    diag1 = [b[i, i] for i in range(3)]
    if sum(diag1) == 3:
        return 'X', [(0, 0), (1, 1), (2, 2)]
    if sum(diag1) == -3:
        return 'O', [(0, 0), (1, 1), (2, 2)]

    # Check anti-diagonal
    diag2 = [b[i, 2 - i] for i in range(3)]
    if sum(diag2) == 3:
        return 'X', [(0, 2), (1, 1), (2, 0)]
    if sum(diag2) == -3:
        return 'O', [(0, 2), (1, 1), (2, 0)]

    # Check for draw or ongoing
    if 0 not in b:
        return 'Draw', []

    return None, []


# --- AI Move Calculation ---
def get_available_moves(b):
    return [(r, c) for r in range(3) for c in range(3) if b[r, c] == 0]

def minimax(b, depth, is_maximizing):
    winner, _ = check_game_state(b)
    if winner == 'O':  # AI is O (-1)
        return 10 - depth
    elif winner == 'X':  # Human is X (1)
        return depth - 10
    elif winner == 'Draw':
        return 0

    available = get_available_moves(b)
    if is_maximizing:
        best_score = -float('inf')
        for r, c in available:
            b[r, c] = -1
            score = minimax(b, depth + 1, False)
            b[r, c] = 0
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for r, c in available:
            b[r, c] = 1
            score = minimax(b, depth + 1, True)
            b[r, c] = 0
            best_score = min(best_score, score)
        return best_score

def get_best_ai_move(b, difficulty="Hard (Unbeatable)"):
    available = get_available_moves(b)
    if not available:
        return None

    if difficulty == "Easy":
        return random.choice(available)

    if difficulty == "Medium":
        # 50% optimal, 50% random
        if random.random() < 0.5:
            return random.choice(available)

    # Minimax for Hard/Unbeatable
    best_score = -float('inf')
    best_move = available[0]
    for r, c in available:
        b[r, c] = -1
        score = minimax(b, 0, False)
        b[r, c] = 0
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move


# --- Session State Initialization ---
if "board" not in st.session_state:
    init_game()

if "scores" not in st.session_state:
    st.session_state.scores = {"X": 0, "O": 0, "Draws": 0}


# --- Move Handling Callback ---
def make_move(row, col):
    if st.session_state.winner is not None or st.session_state.board[row, col] != 0:
        return

    # Player Move
    st.session_state.board[row, col] = st.session_state.current_turn
    winner, combo = check_game_state(st.session_state.board)

    if winner:
        st.session_state.winner = winner
        st.session_state.winning_combo = combo
        if winner in ['X', 'O']:
            st.session_state.scores[winner] += 1
        elif winner == 'Draw':
            st.session_state.scores["Draws"] += 1
        return

    # Switch turn
    st.session_state.current_turn *= -1

    # Trigger AI turn if applicable
    if st.session_state.game_mode == "vs Computer" and st.session_state.current_turn == -1:
        ai_move = get_best_ai_move(st.session_state.board, st.session_state.ai_difficulty)
        if ai_move:
            r, c = ai_move
            st.session_state.board[r, c] = -1
            winner, combo = check_game_state(st.session_state.board)
            if winner:
                st.session_state.winner = winner
                st.session_state.winning_combo = combo
                if winner in ['X', 'O']:
                    st.session_state.scores[winner] += 1
                elif winner == 'Draw':
                    st.session_state.scores["Draws"] += 1
            else:
                st.session_state.current_turn = 1


# --- Sidebar: Configuration & Controls ---
with st.sidebar:
    st.header("⚙️ Game Settings")
    game_mode = st.radio(
        "Opponent",
        options=["vs Player (Pass & Play)", "vs Computer"],
        key="game_mode",
        on_change=init_game
    )

    if game_mode == "vs Computer":
        st.selectbox(
            "AI Difficulty",
            options=["Hard (Unbeatable)", "Medium", "Easy"],
            key="ai_difficulty"
        )

    st.markdown("---")
    st.header("📊 Game Controls")
    if st.button("🔄 New Game", use_container_width=True, type="primary"):
        init_game()
        st.rerun()

    if st.button("🗑️ Reset Scoreboard", use_container_width=True):
        st.session_state.scores = {"X": 0, "O": 0, "Draws": 0}
        init_game()
        st.rerun()

    st.markdown("---")
    st.caption("Built with Streamlit & NumPy")


# --- Main UI ---
st.title("❌ Tic-Tac-Toe ⭕")

# Scoreboard
col_score1, col_score2, col_score3 = st.columns(3)
with col_score1:
    st.markdown(f"<div class='score-card'>Player X<br><span style='font-size:1.4rem; color:#ff4b4b;'>{st.session_state.scores['X']}</span></div>", unsafe_allow_html=True)
with col_score2:
    st.markdown(f"<div class='score-card'>Draws<br><span style='font-size:1.4rem; color:#808495;'>{st.session_state.scores['Draws']}</span></div>", unsafe_allow_html=True)
with col_score3:
    st.markdown(f"<div class='score-card'>Player O<br><span style='font-size:1.4rem; color:#1c83e1;'>{st.session_state.scores['O']}</span></div>", unsafe_allow_html=True)

st.write("")

# Game Status Notification
if st.session_state.winner == 'X':
    st.success("🎉 **Player X wins!** Congratulations!")
    st.balloons()
elif st.session_state.winner == 'O':
    if st.session_state.game_mode == "vs Computer":
        st.error("🤖 **Computer (O) wins!** Better luck next time!")
    else:
        st.success("🎉 **Player O wins!** Congratulations!")
        st.balloons()
elif st.session_state.winner == 'Draw':
    st.info("🤝 **It's a draw!** Well played!")
else:
    turn_player = "X" if st.session_state.current_turn == 1 else "O"
    turn_color = "#ff4b4b" if turn_player == "X" else "#1c83e1"
    st.markdown(f"<h4 style='text-align: center;'>Current Turn: <span style='color:{turn_color};'>{turn_player}</span></h4>", unsafe_allow_html=True)

st.write("")

# Board Grid Render
symbol_map = {0: " ", 1: "X", -1: "O"}

for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        val = st.session_state.board[r, c]
        label = symbol_map[val]
        is_disabled = (val != 0) or (st.session_state.winner is not None)

        cols[c].button(
            label=label if label != " " else "ㅤ",  # non-breaking space for button height consistency
            key=f"cell_{r}_{c}",
            disabled=is_disabled,
            use_container_width=True,
            on_click=make_move,
            args=(r, c)
        )

# Quick Play Again Button below the board when game ends
if st.session_state.winner is not None:
    st.write("")
    if st.button("▶️ Play Again", use_container_width=True, type="primary"):
        init_game()
        st.rerun()
