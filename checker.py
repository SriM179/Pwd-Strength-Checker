import re
import math
import uuid
import streamlit as st

# ---------------- Page & Theme ----------------
st.set_page_config(page_title="Password Strength Checker", page_icon="🔐", layout="centered")

st.markdown("""
<style>
:root{
  --bg:#0f1117; --panel:#1a1f2e; --muted:#262c3f; --text:#e8ecf1; --sub:#aeb6c2;
  --ok:#22c55e; --warn:#f59e0b; --bad:#ef4444; --ring:#7c3aed;
}
[data-testid="stAppViewContainer"]{background:var(--bg);}
h1,h2,h3,h4,h5,p,span,li,code{color:var(--text) !important;}
.small{color:var(--sub); font-size:0.92rem}

.chip{
  display:inline-flex; align-items:center; gap:.5rem;
  padding:.42rem .9rem; border-radius:999px;
  font-weight:700; font-size:.95rem; letter-spacing:.2px;
  color:#fff; background:linear-gradient(90deg,#6d28d9,#9333ea);
  border:1px solid rgba(255,255,255,.12);
  box-shadow:0 6px 18px rgba(147,51,234,.25);
  margin: 2px 0 8px 0;
}

.badge{
  display:inline-flex; align-items:center; gap:.5rem; padding:.35rem .7rem; border-radius:999px;
  font-weight:700; font-size:.9rem; letter-spacing:.2px; border:1px solid rgba(255,255,255,.08);
  margin-bottom:6px;
}
.badge.ok{ background:rgba(34,197,94,.15); color:#7ef5b0; border-color:rgba(34,197,94,.35)}
.badge.warn{ background:rgba(245,158,11,.15); color:#ffd68a; border-color:rgba(245,158,11,.35)}
.badge.bad{ background:rgba(239,68,68,.15); color:#ff9e9e; border-color:rgba(239,68,68,.35)}

.list li{margin:.35rem 0}
.tip{
  background:linear-gradient(180deg, rgba(124,58,237,.15), rgba(124,58,237,.08));
  border:1px solid rgba(124,58,237,.35); border-radius:18px; padding:16px 18px;
}

/* Cute progress bar */
.cute-bar{ width:100%; background:#d6d9e6; border-radius:999px; height:16px; position:relative; overflow:hidden;
  box-shadow:0 0 0 2px rgba(255,255,255,.05) inset; margin:.4rem 0 .7rem 0;}
.cute-bar__fill{ height:100%; border-radius:999px; transition:width .35s ease; }
.cute-bar__label{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
  font-size:12px; font-weight:800; color:#0f1117; text-shadow:0 1px 0 rgba(255,255,255,.5); }
</style>
""", unsafe_allow_html=True)

st.title("🔐 Password Strength Checker")

# ---------- Load banned words ----------
@st.cache_data(show_spinner=False)
def load_wordlist(path: str):
    with open(path, "r") as f:
        return {line.strip().lower() for line in f if line.strip()}
used_words = load_wordlist("list.txt")

# ---------- Regex ----------
RE_LOWER = re.compile(r"[a-z]")
RE_UPPER = re.compile(r"[A-Z]")
RE_DIGIT = re.compile(r"\d")
RE_SYMBOL = re.compile(r"[!\"#$%&'()*+,\-./:;<=>?@\[\]^_`{|}~]")

# ---------- Charset & entropy ----------
def charset_size(password: str) -> int:
    size = 0
    if RE_LOWER.search(password): size += 26
    if RE_UPPER.search(password): size += 26
    if RE_DIGIT.search(password): size += 10
    if RE_SYMBOL.search(password): size += 32
    return size

def entropy_bits(password: str) -> float:
    size = charset_size(password)
    if size <= 0: return 0.0
    return len(password) * math.log2(size)

# ---------- Time formatter ----------
def human_time(seconds: float) -> str:
    if seconds < 1: return "less than 1 second"
    minute, hour, day, year = 60, 3600, 86400, 31536000
    if seconds < minute: return f"{int(seconds)} second(s)"
    if seconds < hour: return f"{int(seconds/60)} minute(s)"
    if seconds < day: return f"{int(seconds/3600)} hour(s)"
    if seconds < year: return f"{int(seconds/day)} day(s)"
    yrs = seconds / year
    return f"{yrs:.1f} year(s)" if yrs < 1000 else f"{yrs:.0f} year(s)"

# ---------- Strength checker ----------
def check(password: str):
    if password.lower() in used_words:
        return "Common", 0, ["avoid dictionary/common words"], 0.0

    score, feedback = 0, []
    if len(password) >= 8: score += 1
    else: feedback.append("at least 8 characters")
    if RE_UPPER.search(password): score += 1
    else: feedback.append("uppercase letter")
    if RE_LOWER.search(password): score += 1
    else: feedback.append("lowercase letter")
    if RE_DIGIT.search(password): score += 1
    else: feedback.append("number")
    if RE_SYMBOL.search(password): score += 1
    else: feedback.append("special character")

    strength = "Weak" if score <= 2 else ("Medium" if score <= 4 else "Strong")
    ebits = entropy_bits(password)
    return strength, score, feedback, ebits

# ---------- Helpers: color & bar ----------
def _rgb_red_yellow_green(f: float) -> str:
    f = max(0.0, min(1.0, f))
    if f <= 0.5:
        r, g, b = 255, int(510*f), 0
    else:
        t = (f-0.5)*2
        r = int(255*(1-t)); g = int(255 - 85*t) + 85; b = 0
    return f"#{r:02x}{g:02x}{b:02x}"

def render_strength_bar(fraction: float, show_text: bool=True):
    fraction = max(0.0, min(1.0, fraction))
    pct = int(fraction*100)
    color = _rgb_red_yellow_green(fraction)
    bar_id = "bar_" + uuid.uuid4().hex[:8]
    html = f"""
      <div id="{bar_id}" class="cute-bar">
        <div class="cute-bar__fill" style="width:{pct}%;
             background-image: linear-gradient(90deg, {color}, {color}EE);
             box-shadow: 0 0 14px {color}88, 0 0 30px {color}44;"></div>
        {'<div class="cute-bar__label">'+str(pct)+'%</div>' if show_text else ''}
      </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ---------- UI ----------
password = st.text_input("Enter password", type="password", placeholder="••••••••")

ATTACKER_SCENARIOS = {
    "Online (throttled, e.g. login attempts)": 100,
    "Offline GPU (single modern GPU)": 1e9,
    "Large offline cluster / botnet": 1e14
}

if password:
    strength, score, feedback, ebits = check(password)

    # Bar
    fraction = score / 5
    render_strength_bar(fraction, show_text=True)

    badge_class = "ok" if strength=="Strong" else ("warn" if strength=="Medium" else "bad")
    emoji = "🟢" if strength=="Strong" else ("🟡" if strength=="Medium" else "🔴")
    st.markdown(f'<span class="badge {badge_class}">{emoji} {strength} password</span>', unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown('<div class="chip">📊 Estimated entropy</div>', unsafe_allow_html=True)
        st.markdown(f"<p style='margin:.15rem 0 1rem 2px;'><code>{ebits:.1f} bits</code></p>", unsafe_allow_html=True)

        st.markdown('<div class="chip">🧩 Missing requirements</div>', unsafe_allow_html=True)
        if feedback:
            st.markdown('<ul class="list" style="margin-top:.25rem;">' + "".join([f"<li>❌ {f}</li>" for f in feedback]) + "</ul>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='margin-top:.25rem;'>All basic requirements met ✅</p>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chip">⏳ Estimated time to crack</div>', unsafe_allow_html=True)
        lines = []
        for scenario, gps in ATTACKER_SCENARIOS.items():
            combos_log2 = max(0.0, ebits)
            avg_attempts_log2 = combos_log2 - 1
            seconds = (2 ** avg_attempts_log2) / gps if avg_attempts_log2 < 1000 else float("inf")
            lines.append(f"- **{scenario}** (~{int(gps):,} guesses/s): {human_time(seconds)}")
        st.markdown("\n\n".join(lines))

    st.markdown('<div class="chip">💡 Tip</div>', unsafe_allow_html=True)
    st.markdown('<div class="tip">Entropy (bits) beats length alone. Use a random passphrase (e.g., four+ uncommon words) and avoid dictionary or personal info.</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="chip">Start here</div>', unsafe_allow_html=True)
    st.markdown('<p class="small">Type a password to see live results.</p>', unsafe_allow_html=True)
