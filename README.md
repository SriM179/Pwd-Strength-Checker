# 🔑 Password Strength Checker

## Introduction: 
A simple, interactive app built with Streamlit that checks how strong your password really is.
It measures entropy, checks against common passwords, and estimates how long different attackers would take to crack it — all with a colorful, playful UI.

URL:  
       
    https://pass-safety-check.streamlit.app/ 

### Features
- Real-time password feedback
- Cute gradient progress bar (red → yellow → green)
- Detects common/weak passwords from list.txt
- Estimates crack times for:
     - Online attacks (~100 guesses/sec)
     - GPU brute force (~1B guesses/sec)
     - Botnets/clusters (~100T guesses/sec)
- Shows what’s missing (uppercase, number, symbol, etc.)
- Gives quick safety tips

#### How to Run
    streamlit run checker.py
