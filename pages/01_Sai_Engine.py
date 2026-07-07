import streamlit as st
import json
import uuid
import random
import requests
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sai Architectural Lab", page_icon="📐", layout="wide")

# ---- CUSTOM GLASSMORPHISM & ANIMATIONS ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 15px rgba(56, 189, 248, 0.2); }
        50% { box-shadow: 0 0 35px rgba(56, 189, 248, 0.6); }
        100% { box-shadow: 0 0 15px rgba(56, 189, 248, 0.2); }
    }
    html, body, [data-testid="stAppViewContainer"] {
        background: #0b0f1a;
        background-image: radial-gradient(ellipse at 20% 20%, rgba(59,130,246,0.08) 0%, transparent 50%),
                          radial-gradient(ellipse at 80% 80%, rgba(139,92,246,0.08) 0%, transparent 50%);
        animation: gradientShift 15s ease infinite;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
    }
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: -0.03em;
    }
    .glass-panel {
        background: rgba(15,23,42,0.65);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
    }
    .glass-panel:hover {
        border-color: rgba(255,255,255,0.15);
        box-shadow: 0 12px 48px rgba(0,0,0,0.7);
        transform: translateY(-2px);
    }
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #3b82f6);
        color: white;
        border: none;
        border-radius: 14px;
        font-weight: 700;
        width: 100%;
        padding: 14px;
        font-family: 'Space Grotesk';
        animation: pulse 3s infinite;
    }
    .metric-card {
        background: rgba(15,23,42,0.8);
        border-radius: 12px;
        padding: 16px;
        border-left: 4px solid #38bdf8;
        margin: 10px 0;
        transition: 0.2s;
    }
    .metric-card:hover {
        background: rgba(30,41,59,0.8);
    }
    .room-card {
        background: rgba(0,0,0,0.3);
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: 0.2s;
    }
    .room-card:hover {
        transform: scale(1.05);
        border-color: rgba(139,92,246,0.5);
    }
</style>
""", unsafe_allow_html=True)

# ---- MEMORY & DATA ----
MEMORY_FILE = Path("arc_studio_v15.json")

# ---- FALLBACK & LIVE FX ----
STATIC_FX = {
    "Kenya": 129.49, "Uganda": 3665.20, "Tanzania": 2625.00,
    "South Sudan": 4626.40, "Rwanda": 1330.00, "Ethiopia": 125.00
}
def get_live_fx():
    try:
        resp = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        data = resp.json()["rates"]
        mapping = {"Kenya":"KES","Uganda":"UGX","Tanzania":"TZS","South Sudan":"SSP","Rwanda":"RWF","Ethiopia":"ETB"}
        return {c: data[mapping[c]] for c in mapping if mapping[c] in data}
    except:
        return None

def build_regional_fx():
    live = get_live_fx()
    base = {
        "Kenya":       {"currency":"KES","symbol":"KSh","multiplier":1.0, "region":"East Africa"},
        "Uganda":      {"currency":"UGX","symbol":"USh","multiplier":0.95,"region":"East Africa"},
        "Tanzania":    {"currency":"TZS","symbol":"TSh","multiplier":0.98,"region":"East Africa"},
        "South Sudan": {"currency":"SSP","symbol":"SSP","multiplier":1.35,"region":"East Africa"},
        "Rwanda":      {"currency":"RWF","symbol":"FRw","multiplier":0.85,"region":"Central Africa"},
        "Ethiopia":    {"currency":"ETB","symbol":"Br", "multiplier":0.80,"region":"Horn of Africa"}
    }
    for c in base:
        base[c]["rate"] = live.get(c, STATIC_FX.get(c, 1.0))
    return base

REGIONAL_FX = build_regional_fx()

# ---- SESSION STATE ----
if "design" not in st.session_state:
    st.session_state.design = None

# ---- SYNTHESIS FUNCTIONS ----
def generate_design(domain, floors, plot_size, bathrooms, country):
    max_footprint = int(plot_size * 0.65)
    floor_area = min(max_footprint, random.randint(120, int(max_footprint * 1.1)))
    gfa = floor_area * floors

    rooms = []
    rooms.append({"name":"Lobby / Corridor", "type":"Circulation", "w":2.5, "h":12, "color":"#1e293b"})
    rooms.append({"name":"Stairwell Core", "type":"Vertical", "w":4.5, "h":4, "color":"#334155"})
    if domain == "Residential":
        rooms.append({"name":"Living + Dining", "type":"Living", "w":7, "h":5.5, "color":"#0d2040"})
        rooms.append({"name":"Kitchen", "type":"Kitchen", "w":4.5, "h":4, "color":"#053020"})
        bedrooms = max(1, int(gfa/75))
        for i in range(bedrooms):
            rooms.append({"name":f"Bedroom {i+1}", "type":"Bedroom", "w":4.5, "h":4, "color":"#2a0f4d"})
    elif domain == "Commercial":
        rooms.append({"name":"Open Office", "type":"Office", "w":12, "h":8, "color":"#075e8a"})
        rooms.append({"name":"Meeting Room", "type":"Conference", "w":6, "h":5, "color":"#1e1b4b"})
    else:
        rooms.append({"name":"Production Floor", "type":"Industrial", "w":18, "h":12, "color":"#3b0764"})
        rooms.append({"name":"Loading Bay", "type":"Logistics", "w":8, "h":8, "color":"#451a03"})
    for b in range(bathrooms):
        rooms.append({"name":f"Bathroom {b+1}", "type":"Bathroom", "w":3, "h":2.5, "color":"#4a2306"})

    span = 6 if domain=="Residential" else (7.5 if domain=="Commercial" else 12)
    cols = max(12, int((floor_area/(span*5))*4))
    beams = int(cols*1.8)

    return {
        "id": str(uuid.uuid4())[:8],
        "domain": domain,
        "floors": floors,
        "plot_size": plot_size,
        "floor_area": floor_area,
        "gfa": gfa,
        "rooms": rooms,
        "country": country,
        "bathrooms": bathrooms,
        "structural": {
            "columns": int(cols*floors),
            "beams": int(beams*floors),
            "span": span
        }
    }

def eurocode_analysis(design):
    span = design["structural"]["span"]
    gk = 5.5
    qk = 2 if design["domain"]=="Residential" else (3.5 if design["domain"]=="Commercial" else 7.5)
    f_ck = random.uniform(28, 32)
    b = random.uniform(280,320)
    d_eff = random.uniform(440,460)
    w_ed = (1.35*gk + 1.5*qk) * 4.5
    m_ed = (w_ed * span**2)/8
    m_rd = (0.167 * f_ck * b * d_eff**2)/1e6
    status = "PASS ✅" if m_rd > m_ed else "FAIL ❌"
    return {
        "design_load": f"{(1.35*gk + 1.5*qk):.1f} kN/m²",
        "m_ed": f"{m_ed:.1f} kNm",
        "m_rd": f"{m_rd:.1f} kNm",
        "uls_status": status,
        "f_ck": round(f_ck,1),
        "b": round(b),
        "d_eff": round(d_eff)
    }

def compute_cost(design):
    fx = REGIONAL_FX[design["country"]]
    gfa = design["gfa"]
    usd = (gfa*0.15*150 + gfa*0.35*210 + gfa*0.35*0.12*1200 + gfa*38*2.5 +
           gfa*40 + len(design["rooms"])*300 + (gfa//16)*450) * fx["multiplier"]
    local = usd * fx["rate"]
    return usd, local, fx

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("""
    <div style="font-size:1.8rem; font-weight:700; font-family:'Space Grotesk';">
        <span style="color:#8b5cf6;">SAI</span> LAB
    </div>
    <div style="color:#94a3b8; margin-bottom:20px;">Structural Synthesis</div>
    """, unsafe_allow_html=True)
    st.header("Design Parameters")
    country = st.selectbox("Region", list(REGIONAL_FX.keys()))
    domain = st.selectbox("Building Type", ["Residential","Commercial","Industrial"])
    plot_size = st.slider("Plot Area (m²)", 200, 5000, 800, step=50)
    floors = st.slider("Floors", 1, 12, 3)
    bathrooms = st.slider("Bathrooms", 1, 10, 2)

    if st.button("✨ Generate Synthesis", use_container_width=True):
        with st.spinner("Computing spatial model..."):
            st.session_state.design = generate_design(domain, floors, plot_size, bathrooms, country)
            st.rerun()

    st.markdown("---")
    if st.button("Return to Hub"):
        st.switch_page("app.py")

# ---- MAIN AREA ----
st.title("📐 Sai: Architectural & Structural Synthesis")
st.markdown("Advanced building modeling and Eurocode compliance laboratory.")

if st.session_state.design:
    d = st.session_state.design
    ec = eurocode_analysis(d)
    usd, local, fx = compute_cost(d)

    tab1, tab2, tab3 = st.tabs(["🗺️ Spatial Layout", "📦 Structural Spec", "📐 Eurocode Analysis"])

    # TAB 1: Rooms
    with tab1:
        st.markdown("### Room Configuration")
        cols = st.columns(3)
        for i, room in enumerate(d["rooms"]):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="room-card" style="background-color:{room['color']}33; border-color:{room['color']};">
                    <div style="font-size:1rem;">{room['name']}</div>
                    <div style="font-size:0.75rem; opacity:0.7;">📐 {room['w']}m × {room['h']}m</div>
                    <div style="font-size:0.7rem;">{room['type']}</div>
                </div>
                """, unsafe_allow_html=True)

    # TAB 2: Structural Spec
    with tab2:
        st.markdown("### Structural Framework")
        col1, col2 = st.columns([1,2])
        with col1:
            st.metric("Storeys", d["floors"])
            st.metric("Total GFA", f"{d['gfa']:,} m²")
            st.metric("Columns", d["structural"]["columns"])
            st.metric("Beams", d["structural"]["beams"])
        with col2:
            st.info("The structural skeleton is optimized for the selected regional material profile.")
            st.markdown(f"""
            <div class="glass-panel">
                <h4 style="color:#38bdf8;">Structural Load Path</h4>
                <p>Span: {d['structural']['span']} m | Load bearing walls assumed 150mm thick</p>
                <p>Material: C30/37 concrete, B500B reinforcement</p>
            </div>
            """, unsafe_allow_html=True)

    # TAB 3: Eurocode Analysis
    with tab3:
        st.markdown("### Compliance Verification")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Design Load", ec["design_load"])
        c2.metric("M_Ed", ec["m_ed"])
        c3.metric("M_Rd", ec["m_rd"])
        c4.metric("ULS", ec["uls_status"])

        if "PASS" in ec["uls_status"]:
            st.success("ULS Status: PASS – The section is adequate.")
        else:
            st.error("ULS Status: FAIL – Increase section size or reinforcement.")

        st.markdown("---")
        st.markdown(f"**Cost Estimate (USD):** ${int(usd):,}")
        st.markdown(f"**Local Cost ({fx['currency']}):** {fx['symbol']} {int(local):,}")

        # Eurocode parameters
        with st.expander("🧪 Random Variability (Sai Engine)"):
            st.write(f"Concrete strength f_ck: {ec['f_ck']} MPa")
            st.write(f"Beam width b: {ec['b']} mm")
            st.write(f"Effective depth d_eff: {ec['d_eff']} mm")

else:
    st.info("Use the sidebar parameters to initialize a new structural synthesis sequence.")