# ❌ Tic-Tac-Toe Game (Streamlit UI & CLI) ⭕

A modern, interactive Tic-Tac-Toe game built with Python and Streamlit, playable directly in the browser via **WebAssembly / GitHub Pages** or locally via **Streamlit / Terminal**.

---

## 🌐 Live Web Demo

Play directly in your browser without installing anything:
👉 **[Play on GitHub Pages](https://asthakhade13-svg.github.io/TIC-TAC-TOE-Game/)**

---

## 🌟 Features

- 🎮 **Streamlit Web UI (Runs in Browser via Stlite / WebAssembly)**:
  - Clean and responsive 3x3 interactive board grid.
  - **Pass & Play (2 Players)** mode.
  - **Single Player vs Computer AI** with difficulty levels:
    - *Easy* (Random moves)
    - *Medium* (Balanced)
    - *Hard / Unbeatable* (Minimax algorithm)
  - Live Scoreboard tracking Player X, Player O, and Draws.
  - Win celebrations with confetti/balloons.
- 💻 **Terminal CLI Game**:
  - Fast, keyboard-driven classic console version.

---

## 🛠️ Local Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/asthakhade13-svg/TIC-TAC-TOE-Game.git
   cd TIC-TAC-TOE-Game
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Run Locally

### 1. Web UI (Streamlit)
To launch the interactive browser interface locally:
```bash
streamlit run app.py
```

### 2. Terminal Mode
To play the classic command-line game:
```bash
python game.py
```

---

## 📂 Project Structure

```text
├── index.html         # Stlite WebAssembly entrypoint for GitHub Pages
├── .nojekyll          # Bypasses Jekyll build on GitHub Pages
├── app.py             # Streamlit Web UI application
├── game.py            # Terminal console game
├── requirements.txt   # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
