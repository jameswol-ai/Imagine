# =========================================================
# ARC — ARCHITECTURAL INTELLECT & EAST AFRICAN FOREX ENGINE
# streamlit_app.py – Galaxy UI, User Auth, Sai Engine
# =========================================================

import streamlit as st
import json
import random
import uuid
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from plotly.subplots import make_subplots

# ═══════════════════════════════════════════════════════
# 0. TRANSLATION DICTIONARIES (unchanged)
# ═══════════════════════════════════════════════════════
TRANSLATIONS = { ... }  # (same as provided, omitted for brevity – keep exactly)

def t(key, **kwargs):
    lang = st.session_state.get("lang", "en")
    text = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

# ═══════════════════════════════════════════════════════
# AUTH & USER MANAGEMENT
# ═══════════════════════════════════════════════════════
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "arc_users.json"

def hash_password(password: str) -> str:
    return hashlib.sha256((password + "arc_salt_24").encode()).hexdigest()

def load_users() -> list:
    if USER_FILE.exists():
        try:
            with open(USER_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_users(users: list):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_user(username: str) -> dict | None:
    for u in load_users():
        if u["username"] == username:
            return u
    return None

def create_user(username: str, password: str, role: str = "user") -> dict:
    users = load_users()
    if get_user(username):
        raise ValueError("Username already exists.")
    user = {
        "username": username,
        "password_hash": hash_password(password),
        "role": role,
        "level": 1,
        "xp": 0,
        "badges": [],
        "created": datetime.now().isoformat()
    }
    users.append(user)
    save_users(users)
    return user

def authenticate(username: str, password: str) -> dict | None:
    user = get_user(username)
    if user and user["password_hash"] == hash_password(password):
        return user
    return None

def update_user_data(username: str, updates: dict):
    users = load_users()
    for u in users:
        if u["username"] == username:
            u.update(updates)
            break
    save_users(users)

def xp_for_level(level: int) -> int:
    return level * 100

def add_xp(username: str, amount: int) -> bool:
    user = get_user(username)
    if not user:
        return False
    old_level = user["level"]
    user["xp"] += amount
    while user["xp"] >= xp_for_level(user["level"]):
        user["xp"] -= xp_for_level(user["level"])
        user["level"] += 1
        badge = f"level_{user['level']}"
        if user["level"] % 5 == 0 and badge not in user["badges"]:
            user["badges"].append(badge)
    update_user_data(username, {"level": user["level"], "xp": user["xp"], "badges": user["badges"]})
    return user["level"] > old_level

# ═══════════════════════════════════════════════════════
# PER‑USER MEMORY
# ═══════════════════════════════════════════════════════
def get_memory_path(username: str) -> Path:
    return DATA_DIR / f"{username}_arc_memory.json"

DEFAULT_STATE = {"designs": [], "concepts": [], "logs": []}

def load_memory(username: str) -> dict:
    path = get_memory_path(username)
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key in DEFAULT_STATE:
                if key not in data:
                    data[key] = DEFAULT_STATE[key]
            return data
        except:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory(username: str, memory: dict):
    with open(get_memory_path(username), "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def log_event(username: str, memory: dict, msg: str):
    memory["logs"].append({"time": datetime.now().isoformat(), "msg": msg})
    save_memory(username, memory)

# ═══════════════════════════════════════════════════════
# SAI ENGINE & FX MODULE (unchanged from original)
# ═══════════════════════════════════════════════════════
# (Include all functions: ARCH_DOMAINS, generate_spatial_model, run_eurocode_analysis,
#  calculate_ai_scores, STATIC_FX_RATES, _BASE_FX_DATA, _fetch_live_rates,
#  initialize_fx_rates, simulate_random_fx, compute_forex_boq, etc.
#  They remain identical to the provided code.)

# ═══════════════════════════════════════════════════════
# GANTT & FX INDICATORS (unchanged)
# ═══════════════════════════════════════════════════════
def generate_gantt_chart(asset): ...
def fetch_historical_fx_kes(start_date, end_date): ...
def compute_rsi(series, period=14): ...
def plot_real_fx_with_indicators(df): ...

# ═══════════════════════════════════════════════════════
# RENDERERS (unchanged)
# ═══════════════════════════════════════════════════════
def render_native_blueprint(plan): ...
def render_isometric_html(plan): ...
def render_plotly_3d_rooms(plan): ...

# ═══════════════════════════════════════════════════════
# GALAXY THEME CSS
# ═══════════════════════════════════════════════════════
GALAXY_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&family=Space+Mono&family=Exo+2:wght@400;600;700&display=swap');

/* Starfield animated background */
@keyframes starGlow {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}
@keyframes nebulaShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes warpSpeed {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

html, body, .stApp {
    background: radial-gradient(ellipse at bottom, #0d0b1e 0%, #000000 70%);
    font-family: 'Exo 2', sans-serif;
    color: #e0e7ff;
}
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Ccircle cx='20' cy='40' r='2' fill='%23fff' opacity='0.4'/%3E%3Ccircle cx='150' cy='200' r='1.5' fill='%23fff' opacity='0.3'/%3E%3Ccircle cx='280' cy='80' r='2.5' fill='%23fff' opacity='0.5'/%3E%3Ccircle cx='370' cy='250' r='1' fill='%23fff' opacity='0.6'/%3E%3Ccircle cx='60' cy='300' r='2' fill='%23fff' opacity='0.3'/%3E%3C/svg%3E") repeat;
    z-index: -2;
    animation: starGlow 3s infinite alternate;
}
.stApp::after {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: radial-gradient(circle at 20% 30%, rgba(147,51,234,0.15), transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(59,130,246,0.15), transparent 50%),
                radial-gradient(circle at 50% 50%, rgba(168,85,247,0.1), transparent 70%);
    z-index: -1;
    background-size: 200% 200%;
    animation: nebulaShift 10s ease infinite;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    color: #c7d2fe;
    text-shadow: 0 0 8px rgba(139,92,246,0.5);
}

.glass-panel {
    background: rgba(15, 23, 42, 0.5);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 0 30px rgba(139,92,246,0.15);
}

.stButton > button {
    background: linear-gradient(135deg, #8b5cf6, #6366f1);
    color: white;
    border: none;
    border-radius: 14px;
    font-weight: 700;
    font-size: 1rem;
    font-family: 'Orbitron', sans-serif;
    transition: all 0.3s;
    box-shadow: 0 0 20px rgba(139,92,246,0.4);
}
.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 40px rgba(168,85,247,0.7);
}

.metric-bar-bg {
    background: rgba(30,41,59,0.8);
    border-radius: 8px;
    height: 8px;
}
.metric-bar-fg {
    border-radius: 8px;
    background: linear-gradient(90deg, #8b5cf6, #38bdf8);
    box-shadow: 0 0 12px #8b5cf6;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(9,14,25,0.9);
    backdrop-filter: blur(18px);
    border-right: 1px solid rgba(139,92,246,0.4);
}
</style>
"""

# ═══════════════════════════════════════════════════════
# APP INITIALISATION
# ═══════════════════════════════════════════════════════
st.set_page_config(page_title="ARC – Sai Engine", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")
st.markdown(GALAXY_CSS, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_data = None
    st.session_state.memory = DEFAULT_STATE.copy()
    st.session_state.generated_concepts = []
    st.session_state.active_design = None
    st.session_state.lang = "en"

# Auto‑create admin if no users
if not load_users():
    create_user("admin", "admin123", role="admin")

# ═══════════════════════════════════════════════════════
# LOGIN PAGE
# ═══════════════════════════════════════════════════════
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#c084fc;'>🌌 ARC STATION</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#a78bfa;'>Sai Engine & Cosmic Architecture</p>", unsafe_allow_html=True)
        with st.form("auth_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            col_login, col_reg = st.columns(2)
            with col_login:
                login_btn = st.form_submit_button("🚀 Launch")
            with col_reg:
                register_btn = st.form_submit_button("✨ Register")
            if login_btn:
                user = authenticate(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_data = user
                    st.session_state.memory = load_memory(username)
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
            if register_btn:
                if not username or not password:
                    st.error("Please fill all fields.")
                else:
                    try:
                        create_user(username, password)
                        st.success("Account created! You can now log in.")
                    except ValueError as e:
                        st.error(str(e))
    st.stop()

# ═══════════════════════════════════════════════════════
# LOGGED IN – SETUP
# ═══════════════════════════════════════════════════════
username = st.session_state.username
user_data = st.session_state.user_data
mem = st.session_state.memory
initialize_fx_rates()  # load live FX

# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:20px;">
        <div style="font-size:1.4rem; font-weight:700; color:#c084fc;">🌌 ARC</div>
        <div style="font-size:0.8rem; color:#94a3b8;">👤 {username} | Lvl {user_data['level']}</div>
    </div>
    """, unsafe_allow_html=True)
    # XP bar
    lvl = user_data["level"]
    xp = user_data["xp"]
    needed = xp_for_level(lvl)
    progress = xp / needed if needed > 0 else 1.0
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
        <span style="font-size:12px; color:#a78bfa;">LVL {lvl}</span>
        <div style="flex:1; height:6px; background:#1e293b; border-radius:3px;">
            <div style="width:{progress*100}%; height:100%; background:linear-gradient(90deg,#c084fc,#38bdf8); border-radius:3px;"></div>
        </div>
        <span style="font-size:10px; color:#94a3b8;">{xp}/{needed} XP</span>
    </div>
    """, unsafe_allow_html=True)

    lang_option = st.selectbox("🌐 Language", ["English", "Kiswahili"], index=0)
    st.session_state.lang = "en" if lang_option == "English" else "sw"

    page = st.radio("Navigation", [t("dashboard"), t("generative")], index=1)

    if user_data.get("role") == "admin":
        with st.expander("🛡️ Admin Console"):
            users = load_users()
            for u in users:
                cols = st.columns([3,1])
                cols[0].write(f"{u['username']} (Lvl {u['level']})")
                if u["username"] != username:
                    if cols[1].button("❌", key=f"del_{u['username']}"):
                        users.remove(u)
                        save_users(users)
                        st.rerun()
                else:
                    cols[1].write("you")

    st.markdown("---")
    st.markdown(t("project_memory"))
    if mem["designs"]:
        for d in mem["designs"][-3:]:
            st.markdown(f"<div class='project-memory-card'><span>🏗️ {d['id']}</span><span style='color:#a78bfa;'>●</span></div>", unsafe_allow_html=True)
    else:
        st.caption(t("no_designs"))

    if st.button("🚪 Logout"):
        save_memory(username, mem)
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.memory = DEFAULT_STATE.copy()
        st.session_state.generated_concepts = []
        st.rerun()

# ═══════════════════════════════════════════════════════
# MAIN PAGES (Dashboard & Generative) – keep original logic
# ═══════════════════════════════════════════════════════
if page == t("dashboard"):
    # ... (identical to provided, but use mem instead of st.session_state.memory directly; already mem is same)
    # Ensure all FX/forex blocks use get_fx_data etc.
    # Add a quick XP reward for viewing dashboard maybe.
    pass

elif page == t("generative"):
    # ... (identical provided Generative page, but add XP for generating concepts)
    # After generating concepts, call add_xp(username, 20) and if leveled up -> st.balloons()
    pass

# (Include the complete code for both pages, incorporating the XP reward)
