# =========================================================
# ARC — ARCHITECTURAL INTELLECT & EAST AFRICAN FOREX ENGINE
# streamlit_app.py  –  UI Layer (v15.1 modular)
# =========================================================

import streamlit as st
import json
import random
import time
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os, sys, traceback

# =========================================================
# INITIALISE CORE SERVICES
# =========================================================

MEMORY_FILE = Path("arc_studio_v13.json")

# =========================================================
# CUSTOM CSS (ANIMATED GLASSMORPHISM)
# =========================================================
st.set_page_config(
    page_title="RANDOM V3 | Sai Engine & FX",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 15px rgba(56, 189, 248, 0.2); }
        50% { box-shadow: 0 0 35px rgba(56, 189, 248, 0.6); }
        100% { box-shadow: 0 0 15px rgba(56, 189, 248, 0.2); }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: #0b0f1a;
        background-image: 
            radial-gradient(ellipse at 20% 20%, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(56, 189, 248, 0.05) 0%, transparent 70%);
        background-size: 200% 200%;
        animation: gradientShift 15s ease infinite;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-top: 0;
    }
    
    .glass-panel {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1.2);
        position: relative;
        overflow: hidden;
    }
    .glass-panel::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.03), transparent);
        transition: left 0.5s ease;
    }
    .glass-panel:hover::before {
        left: 100%;
    }
    .glass-panel:hover {
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.7);
        transform: translateY(-4px);
    }

    .glow-edge {
        position: relative;
        border: 1px solid rgba(56, 189, 248, 0.25);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.08);
    }
    
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid #1e293b;
        color: #e2e8f0;
        border-radius: 14px;
        padding: 14px;
        font-family: 'Space Grotesk';
        transition: all 0.2s ease;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border: 1px solid #38bdf8;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.25);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #3b82f6);
        color: white;
        border: none;
        border-radius: 14px;
        font-weight: 700;
        font-size: 1.1rem;
        font-family: 'Space Grotesk';
        transition: all 0.4s ease;
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.3);
        width: 100%;
        padding: 16px;
        letter-spacing: 0.5px;
        animation: pulse 3s infinite;
    }
    .stButton > button:hover {
        transform: scale(1.04) translateY(-2px);
        box-shadow: 0 0 50px rgba(59, 130, 246, 0.6);
        background: linear-gradient(135deg, #9f7aea, #5a7df1);
    }
    
    .metric-bar-bg { 
        width: 100%; 
        height: 6px; 
        background: #1e293b; 
        border-radius: 6px; 
        margin-top: 8px; 
        overflow: hidden; 
    }
    .metric-bar-fg { 
        height: 100%; 
        border-radius: 6px; 
        transition: width 1.5s ease-in-out;
        background-size: 200% 100%;
        animation: shimmer 2s infinite linear;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(9, 14, 25, 0.95);
        backdrop-filter: blur(14px);
        border-right: 1px solid #1e293b;
    }
    
    .project-memory-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 8px;
        font-size: 0.85rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.2s ease;
    }
    .project-memory-card:hover { 
        background: #1e293b; 
        border-color: #38bdf8;
        box-shadow: 0 0 12px rgba(56,189,248,0.1);
    }
    
    .mini-plan {
        background-color: #1e293b;
        background-image: 
            linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
        background-size: 20px 20px;
        border-radius: 12px;
        height: 80px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }
    .mini-plan::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 30%, rgba(59,130,246,0.15), transparent 60%);
    }
    
    .float-element {
        animation: float 6s ease-in-out infinite;
    }
    
    .canvas-container {
        background: #040711; 
        padding: 8px; 
        border-radius: 16px; 
        border: 1px solid #1e293b;
        box-shadow: 0 0 30px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
    }
    .canvas-container:hover {
        border-color: #38bdf8;
        box-shadow: 0 0 40px rgba(56,189,248,0.15);
    }
    
    .score-card {
        border-left: 4px solid;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# MEMORY & STATE MANAGEMENT
# =========================================================
DEFAULT_STATE = {"designs": [], "concepts": [], "logs": []}

def load_memory():
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_STATE.copy()
    return DEFAULT_STATE.copy()

def save_memory():
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.memory, f, indent=2)
    except Exception:
        pass

def log_event(msg):
    st.session_state.memory["logs"].append({
        "time": datetime.now().isoformat(),
        "msg": msg
    })
    save_memory()

# =========================================================
# GRAPHICS RENDERING (2D & ISOMETRIC)
# =========================================================
def render_native_blueprint(plan):
    canvas_html = '<div class="arc-blueprint-canvas" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(220px,1fr)); gap:14px; background:#0a0f1c; padding:24px; border-radius:18px; border:1px dashed #334155; margin:10px 0; box-shadow: inset 0 0 30px rgba(0,0,0,0.5);">'
    for room in plan:
        canvas_html += (
            f'<div style="padding:16px; border-radius:12px; color:#fff; border:1px solid rgba(255,255,255,0.08); background-color:{room["color"]}; box-shadow:0 8px 24px rgba(0,0,0,0.4); transition: all 0.2s ease; cursor:pointer;" '
            f'onmouseover="this.style.transform=\'scale(1.03)\'; this.style.boxShadow=\'0 12px 32px rgba(0,0,0,0.6)\';" '
            f'onmouseout="this.style.transform=\'scale(1)\'; this.style.boxShadow=\'0 8px 24px rgba(0,0,0,0.4)\';">'
            f'<div style="font-size:1rem; font-weight:600; font-family:\'Space Grotesk\';">{room["name"]}</div>'
            f'<div style="font-size:0.8rem; opacity:0.8; margin-top:4px;">📐 {room["w"]}m × {room["h"]}m ({room["type"]})</div>'
            f'</div>'
        )
    canvas_html += '</div>'
    return canvas_html

def render_isometric_html(plan):
    canvas_w, canvas_h = 800, 380
    shapes_js = ""
    for idx, r in enumerate(plan):
        offset_x = (idx % 3) * 170 + 100
        offset_y = (idx // 3) * 110 + 130
        rw = min(115, int(r["w"] * 14))
        rh = min(95, int(r["h"] * 14))
        color = r["color"]
        shapes_js += f"""
        ctx.fillStyle = "{color}";
        ctx.beginPath();
        ctx.moveTo({offset_x}, {offset_y});
        ctx.lineTo({offset_x} + {rw}, {offset_y} - {rh}/2);
        ctx.lineTo({offset_x} + {rw} + {rw}, {offset_y});
        ctx.lineTo({offset_x} + {rw}, {offset_y} + {rh}/2);
        ctx.closePath();
        ctx.fill(); ctx.strokeStyle = "rgba(255,255,255,0.3)"; ctx.stroke();
        ctx.fillStyle = "rgba(255,255,255,0.06)";
        ctx.beginPath();
        ctx.moveTo({offset_x}, {offset_y});
        ctx.lineTo({offset_x}, {offset_y} - 40);
        ctx.lineTo({offset_x} + {rw}, {offset_y} + {rh}/2 - 40);
        ctx.lineTo({offset_x} + {rw}, {offset_y} + {rh}/2);
        ctx.closePath(); ctx.fill(); ctx.stroke();
        ctx.fillStyle = "#ffffff"; ctx.font = "bold 11px Space Grotesk";
        ctx.fillText("{r['name']}", {offset_x} + 15, {offset_y} - 2);
        """
    return f"""
    <div class="canvas-container">
        <canvas id="arc3dCanvas" width="{canvas_w}" height="{canvas_h}" style="max-width:100%; background:#050814;"></canvas>
        <script>
            const canvas = document.getElementById('arc3dCanvas'); const ctx = canvas.getContext('2d');
            ctx.strokeStyle = 'rgba(56, 189, 248, 0.04)';
            for(let i=0; i<canvas.width; i+=40) {{ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke(); }}
            for(let j=0; j<canvas.height; j+=40) {{ ctx.beginPath(); ctx.moveTo(0,j); ctx.lineTo(canvas.width, j); ctx.stroke(); }}
            {shapes_js}
        </script>
    </div>
    """

def render_plotly_3d_rooms(plan):
    x, y, z = [], [], []
    for i, room in enumerate(plan):
        col = i % 3
        row = i // 3
        xc = col * 12
        yc = row * 10
        w = room["w"]
        d = room["h"]
        x.extend([xc - w/2, xc + w/2, xc + w/2, xc - w/2, None])
        y.extend([yc - d/2, yc - d/2, yc + d/2, yc + d/2, None])
        z.extend([0,0,0,0,None])

    fig = go.Figure(data=[
        go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color='white', width=2),
            hoverinfo='none'
        )
    ])
    for i, room in enumerate(plan):
        col = i % 3
        row = i // 3
        xc = col * 12
        yc = row * 10
        w = room["w"]
        d = room["h"]
        fig.add_trace(go.Mesh3d(
            x=[xc-w/2, xc+w/2, xc+w/2, xc-w/2],
            y=[yc-d/2, yc-d/2, yc+d/2, yc+d/2],
            z=[0,0,0,0],
            color=room["color"],
            opacity=0.7,
            flatshading=True,
            hoverinfo='text',
            text=room["name"]
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False, showgrid=False),
            yaxis=dict(visible=False, showgrid=False),
            zaxis=dict(visible=False, showgrid=False),
            bgcolor='#040711'
        ),
        paper_bgcolor='#040711',
        margin=dict(l=0, r=0, b=0, t=20),
        showlegend=False,
        title="3D Room Layout (Interactive)",
        title_font=dict(color='#94a3b8', size=14)
    )
    return fig

# =========================================================
# SESSION STATE INIT
# =========================================================
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()
if "generated_concepts" not in st.session_state:
    st.session_state.generated_concepts = []
if "active_design" not in st.session_state:
    st.session_state.active_design = None
if "ai_boost" not in st.session_state:
    st.session_state.ai_boost = 0

mem = st.session_state.memory

# =========================================================
# SIDEBAR UI
# =========================================================
st.sidebar.markdown("""
<div style="font-size: 2rem; font-weight: 700; font-family: 'Space Grotesk';">
    <span style="color: #8b5cf6;">R</span>ANDOM V3
</div>
<div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 24px;">Sai Engine & FX Studio</div>
""", unsafe_allow_html=True)

nav_page = st.sidebar.radio("Studio Workspace", ["Control Hub Dashboard", "Generative Design Engine"], index=1)
st.sidebar.markdown("---")

with st.sidebar.expander("📐 Arc Configuration Options", expanded=True):
    select_country = st.selectbox("East African Target Region", get_all_countries())
    select_domain = st.selectbox("Structural Logic Domain", list(ARCH_DOMAINS.keys()))
    select_type = st.selectbox("Specific Typology", ARCH_DOMAINS[select_domain])
    input_plot = st.slider("Total Boundary Plot Area (m²)", 200, 5000, 800, step=50)
    input_floors = st.slider("Building Height Limit (Floors)", 1, 12, 3)
    input_baths = st.slider("Total Bathroom Batteries", 1, 10, 2)

with st.sidebar.expander("⚖️ AI Agent Weights", expanded=False):
    w_arch = st.slider("Architect Weight", 0.0, 1.0, 0.25, 0.05)
    w_struct = st.slider("Structural Weight", 0.0, 1.0, 0.25, 0.05)
    w_sust = st.slider("Sustainability Weight", 0.0, 1.0, 0.25, 0.05)
    w_cost = st.slider("Cost Weight", 0.0, 1.0, 0.25, 0.05)
    total_w = w_arch + w_struct + w_sust + w_cost
    if total_w > 0:
        w_arch /= total_w
        w_struct /= total_w
        w_sust /= total_w
        w_cost /= total_w
    weights = (w_arch, w_struct, w_sust, w_cost)
    st.caption(f"Normalised: arch {w_arch:.2f}, struct {w_struct:.2f}, sust {w_sust:.2f}, cost {w_cost:.2f}")

# ── Forex Converter Widget ──────────────────────────
with st.sidebar.expander("💱 Forex Converter", expanded=False):
    currencies = ["USD"] + get_all_countries()
    convert_from = st.selectbox("From", currencies, key="conv_from")
    convert_to = st.selectbox("To", currencies, key="conv_to")
    amount = st.number_input("Amount", min_value=0.0, value=1000.0, step=100.0)

    result = convert_currency(amount, convert_from, convert_to)

    sym_from = "$" if convert_from == "USD" else get_fx_data(convert_from)["symbol"]
    sym_to = "$" if convert_to == "USD" else get_fx_data(convert_to)["symbol"]
    st.metric(f"{sym_from} {amount:,.2f} → {sym_to} {result:,.2f}")

    if convert_from != convert_to:
        rate = get_fx_data(convert_to)["rate"] / (get_fx_data(convert_from)["rate"] if convert_from != "USD" else 1.0)
        st.caption(f"1 {convert_from} = {rate:.4f} {convert_to}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📂 PROJECT MEMORY")
if len(mem["designs"]) > 0:
    for d in mem["designs"][-5:]:
        st.sidebar.markdown(f"""
        <div class="project-memory-card">
            <span>🏗️ #{d['id']} - {d['type']}</span>
            <span style="color: #22c55e; font-size:10px;">● Live</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.sidebar.caption("No designs archived yet...")

# =========================================================
# DASHBOARD VIEW
# =========================================================
if nav_page == "Control Hub Dashboard":
    st.markdown("""
    <div class="glass-panel float-element" style="margin-bottom: 32px; text-align: center;">
        <h1 style="font-size: 2.5rem; margin-bottom: 4px;">Welcome back, Architect 👋</h1>
        <div style="color: #94a3b8; font-size: 1.1rem;">Create. Evolve. Perfect.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💹 LIVE RANDOM FX INDICES")
    fx_cols = st.columns(6)
    for i, country in enumerate(get_all_countries()):
        data = get_fx_data(country)
        with fx_cols[i]:
            st.markdown(f"""
            <div class="glass-panel" style="padding: 16px 8px; text-align: center;">
                <div style="font-size: 0.8rem; color: #94a3b8;">{country}</div>
                <div style="font-size: 1.5rem; font-weight: 700; font-family: 'Space Grotesk';">{data['symbol']} {data['rate']}</div>
                <div style="font-size: 0.7rem; color: #22c55e;">▴ {data['region']}</div>
            </div>
            """, unsafe_allow_html=True)

    with st.expander("📈 Simulated KES/USD History (60 days)", expanded=False):
        start_rate = get_fx_data("Kenya")["rate"]
        np.random.seed(42)
        random_steps = np.random.normal(0, 0.008, 60)
        rates = [start_rate]
        for step in random_steps:
            rates.append(rates[-1] * (1 + step))
        fx_df = pd.DataFrame({"Day": range(len(rates)), "KES/USD": rates})
        fig = px.line(fx_df, x="Day", y="KES/USD", title="Simulated KES/USD (random walk)")
        fig.update_traces(line_color="#38bdf8")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="glass-panel" style="text-align:center;">', unsafe_allow_html=True)
        st.metric("Total Blueprints Saved", len(mem["designs"]), delta="+1")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass-panel" style="text-align:center;">', unsafe_allow_html=True)
        st.metric("Architectural Concepts", len(mem["designs"]) * 5, delta="Evolving")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="glass-panel" style="text-align:center;">', unsafe_allow_html=True)
        st.metric("Pipeline Logs", len(mem["logs"]))
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# GENERATIVE ENGINE VIEW
# =========================================================
elif nav_page == "Generative Design Engine":
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
        <div class="glass-panel" style="padding: 20px 32px;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0; background: linear-gradient(135deg, #8b5cf6, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Synthesis Lab</h1>
            <div style="color: #94a3b8; font-size: 0.95rem;">Sai Engine & Evolution Matrix Active</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col_input, col_gen = st.columns([2.5, 1])
        with col_input:
            st.markdown("### 🤖 RANDOM COPILOT")
            st.markdown("<div style='color: #94a3b8; font-size: 0.9rem;'>Your AI design partner</div>", unsafe_allow_html=True)
            prompt = st.text_area("Describe your dream project...", placeholder="e.g. Sustainable beach house with open spaces, modern aesthetic...", height=100)

            tag_c1, tag_c2, tag_c3 = st.columns(3)
            if tag_c1.button("🌱 Sustainable", use_container_width=True):
                st.session_state.ai_boost = 10
            if tag_c2.button("🏛️ Modern", use_container_width=True):
                st.session_state.ai_boost = 5
            if tag_c3.button("🌴 Tropical", use_container_width=True):
                st.session_state.ai_boost = 8

        with col_gen:
            st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
            trigger_synthesis = st.button("✨ Generate Concepts", type="primary", use_container_width=True)

    if trigger_synthesis:
        with st.spinner("🧠 Sai Engine synthesizing 5 architectural variations..."):
            concepts = []
            for i in range(5):
                mut_plot = input_plot + random.randint(-150, 150)
                mut_floors = max(1, input_floors + random.randint(-1, 1))
                mut_rooms = max(1, input_baths + random.randint(-1, 1))
                d = generate_spatial_model(
                    select_domain, select_type, mut_plot, mut_floors, mut_rooms, select_country, seed=i
                )
                d["plan"] = d["rooms"]
                ec = run_eurocode_analysis(d, d["domain"])
                total_usd, total_local, fx = compute_forex_boq(d, d["country"])
                arch, struct, sust, cost, comp = calculate_ai_scores(d, ec, total_usd, prompt, weights)
                d["scores"] = {"arch": arch, "struct": struct, "sust": sust, "cost": cost, "composite": comp}
                d["total_usd"] = total_usd
                d["total_local"] = total_local
                d["fx"] = fx
                concepts.append(d)
            concepts.sort(key=lambda x: x["scores"]["composite"], reverse=True)
            st.session_state.generated_concepts = concepts
            st.session_state.active_design = concepts[0]
            log_event(f"Sai Engine spawned 5 new architectural concepts. Alpha: {concepts[0]['id']}")

    st.markdown("---")

    if st.session_state.generated_concepts:
        st.markdown("### 🔬 EVOLUTION ENGINE RESULTS")
        st.markdown("<div style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 24px;'>5 unique design concepts evaluated by Sai AI Agents</div>", unsafe_allow_html=True)

        concept_names = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
        concept_colors = ["#4ade80", "#eab308", "#3b82f6", "#8b5cf6", "#ec4899"]

        cols = st.columns(5)
        for i, c in enumerate(st.session_state.generated_concepts[:5]):
            with cols[i]:
                sc = c["scores"]
                st.markdown(f"""
                <div class="glass-panel glow-edge" style="padding: 16px; border-left: 4px solid {concept_colors[i]}; text-align: center;">
                    <div class="mini-plan">
                        <div style="color: #64748b; font-size: 0.8rem;">🏗️ Concept {concept_names[i]}</div>
                    </div>
                    <div style="font-weight: 600; color: {concept_colors[i]}; font-size: 1.1rem;">{concept_names[i]}</div>
                    <div style="font-size: 12px; color: #94a3b8; margin-bottom: 12px;">{c['type']}</div>
                    
                    <div style="font-size: 0.75rem; text-align: left; margin-top: 5px; color: #94a3b8;">🏛️ Arch {sc['arch']}%</div>
                    <div class="metric-bar-bg"><div class="metric-bar-fg" style="width: {sc['arch']}%; background: {concept_colors[i]};"></div></div>
                    
                    <div style="font-size: 0.75rem; text-align: left; margin-top: 5px; color: #94a3b8;">⚙️ Struct {sc['struct']}%</div>
                    <div class="metric-bar-bg"><div class="metric-bar-fg" style="width: {sc['struct']}%; background: #00d2ff;"></div></div>
                    
                    <div style="font-size: 0.75rem; text-align: left; margin-top: 5px; color: #94a3b8;">🌱 Sustain {sc['sust']}%</div>
                    <div class="metric-bar-bg"><div class="metric-bar-fg" style="width: {sc['sust']}%; background: #38bdf8;"></div></div>
                    
                    <div style="font-size: 0.75rem; text-align: left; margin-top: 5px; color: #94a3b8;">💰 Cost {sc['cost']}%</div>
                    <div class="metric-bar-bg"><div class="metric-bar-fg" style="width: {sc['cost']}%; background: #facc15;"></div></div>
                </div>
                """, unsafe_allow_html=True)

        with st.expander("📊 AI Score Radar Comparison", expanded=True):
            radar_data = []
            for i, c in enumerate(st.session_state.generated_concepts[:5]):
                sc = c["scores"]
                radar_data.append({
                    "Concept": f"{concept_names[i]} ({c['type']})",
                    "Architecture": sc["arch"],
                    "Structural": sc["struct"],
                    "Sustainability": sc["sust"],
                    "Cost Efficiency": sc["cost"]
                })
            df_radar = pd.DataFrame(radar_data)
            categories = ["Architecture", "Structural", "Sustainability", "Cost Efficiency"]
            fig_radar = go.Figure()
            for i, row in df_radar.iterrows():
                fig_radar.add_trace(go.Scatterpolar(
                    r=row[categories].values,
                    theta=categories,
                    fill='toself',
                    name=row["Concept"],
                    line_color=concept_colors[i],
                    opacity=0.7
                ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(range=[0, 100], showticklabels=False, gridcolor='#1e293b'),
                    angularaxis=dict(gridcolor='#1e293b')
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8'),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # Top recommendation
        st.markdown("---")
        st.markdown("### 🏆 TOP RECOMMENDATION: CONCEPT ALPHA (Composite Score Leader)")
        asset = st.session_state.generated_concepts[0]

        col_detail, col_save = st.columns([3,1])
        with col_save:
            if st.button("💾 Save to Library", use_container_width=True):
                design_entry = {
                    "id": asset["id"],
                    "type": asset["type"],
                    "country": asset["country"],
                    "total_gfa": asset["total_gfa"],
                    "scores": asset["scores"],
                    "plan": asset["plan"],
                    "timestamp": datetime.now().isoformat()
                }
                st.session_state.memory["designs"].append(design_entry)
                save_memory()
                log_event(f"Saved design {asset['id']} to library")
                st.success("Design saved to project memory!")

        sc_a = asset["scores"]
        ec_a = run_eurocode_analysis(asset, asset['domain'])
        a1, a2, a3, a4 = st.columns(4)
        with a1:
            st.markdown(f"""
            <div class="glass-panel score-card" style="border-left-color: #4ade80;">
                <div style="color: #4ade80; font-weight:600;">🏛️ Architect AI</div>
                <div style="color:#94a3b8; font-size:12px;">Function & Aesthetics</div>
                <div style="font-size:20px; font-weight:700;">{asset['type']}</div>
                <div class="metric-bar-bg"><div class="metric-bar-fg" style="width:{sc_a['arch']}%; background:#4ade80;"></div></div>
                <div style="font-size: 12px; margin-top: 6px;">{sc_a['arch']}% Match</div>
            </div>
            """, unsafe_allow_html=True)
        with a2:
            st.markdown(f"""
            <div class="glass-panel score-card" style="border-left-color: #00d2ff;">
                <div style="color: #00d2ff; font-weight:600;">⚙️ Structural AI</div>
                <div style="color:#94a3b8; font-size:12px;">Safety & Stability</div>
                <div style="font-size:20px; font-weight:700;">{ec_a['uls_status']}</div>
                <div class="metric-bar-bg"><div class="metric-bar-fg" style="width:{sc_a['struct']}%; background:#00d2ff;"></div></div>
                <div style="font-size: 12px; margin-top: 6px;">{sc_a['struct']}% Safety</div>
            </div>
            """, unsafe_allow_html=True)
        with a3:
            st.markdown(f"""
            <div class="glass-panel score-card" style="border-left-color: #38bdf8;">
                <div style="color: #38bdf8; font-weight:600;">🌱 Sustainability AI</div>
                <div style="color:#94a3b8; font-size:12px;">Green & Efficiency</div>
                <div style="font-size:20px; font-weight:700;">{asset['windows']} Windows</div>
                <div class="metric-bar-bg"><div class="metric-bar-fg" style="width:{sc_a['sust']}%; background:#38bdf8;"></div></div>
                <div style="font-size: 12px; margin-top: 6px;">{sc_a['sust']}% Eco</div>
            </div>
            """, unsafe_allow_html=True)
        with a4:
            st.markdown(f"""
            <div class="glass-panel score-card" style="border-left-color: #facc15;">
                <div style="color: #facc15; font-weight:600;">💰 Cost AI</div>
                <div style="color:#94a3b8; font-size:12px;">Budget & Value</div>
                <div style="font-size:20px; font-weight:700;">{asset['fx']['symbol']} {int(asset['total_local']):,}</div>
                <div class="metric-bar-bg"><div class="metric-bar-fg" style="width:{sc_a['cost']}%; background:#facc15;"></div></div>
                <div style="font-size: 12px; margin-top: 6px;">{sc_a['cost']}% Value</div>
            </div>
            """, unsafe_allow_html=True)

        # 2D & 3D Layout
        st.markdown("---")
        col_2d, col_3d = st.columns(2)
        with col_2d:
            st.markdown("### 🗺️ 2D FLOOR PLAN")
            st.markdown(render_native_blueprint(asset["plan"]), unsafe_allow_html=True)
            st.caption(f"Total GFA: {asset['total_gfa']:,} m² | {asset['floors']} Floors | {asset['country']}")

            with st.expander("📊 Live Currency Bill of Quantities"):
                use_volatility = st.checkbox("📈 Simulate FX Volatility", value=False)
                if use_volatility:
                    volatility_pct = st.slider("Volatility %", 0.5, 10.0, 2.0) / 100
                    # Apply random volatility to each country's rate
                    for country in get_all_countries():
                        baseline = get_baseline_rate(country)
                        set_rate(country, simulate_random_fx(baseline, volatility_pct))
                usd, local, fx = compute_forex_boq(asset, asset['country'])
                st.metric("USD Total", f"${int(usd):,}")
                st.metric(f"Local {fx['currency']}", f"{fx['symbol']} {int(local):,}")
                st.caption(f"1 USD = {fx['rate']:.2f} {fx['currency']}")

                # Reset rates after display
                if use_volatility:
                    reset_rates_to_baseline()

        with col_3d:
            st.markdown("### 📦 3D MASSING CONCEPT")
            view_mode = st.radio("3D View Mode", ["Isometric Wireframe", "Interactive 3D Rooms"], horizontal=True)
            if view_mode == "Isometric Wireframe":
                st.components.v1.html(render_isometric_html(asset["plan"]), height=450)
            else:
                fig3d = render_plotly_3d_rooms(asset["plan"])
                st.plotly_chart(fig3d, use_container_width=True)

        # Export report
        st.markdown("---")
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            report_str = f"# ARC Design Report\n\n"
            report_str += f"**Concept Alpha** | {asset['type']} | {asset['country']}\n\n"
            report_str += f"- GFA: {asset['total_gfa']} m²\n"
            report_str += f"- Floors: {asset['floors']}\n"
            report_str += f"- Rooms: {len(asset['plan'])}\n"
            report_str += f"- BOQ USD: ${int(asset['total_usd']):,}\n"
            report_str += f"- Local ({asset['fx']['currency']}): {asset['fx']['symbol']} {int(asset['total_local']):,}\n\n"
            report_str += f"## AI Scores\n"
            for key, val in asset['scores'].items():
                report_str += f"- {key.capitalize()}: {val}%\n"
            report_bytes = report_str.encode()
            st.download_button(
                label="📄 Download Design Report",
                data=report_bytes,
                file_name=f"arc_report_{asset['id']}.md",
                mime="text/markdown"
            )

    else:
        st.info("🌀 Awaiting input. Configure your structural parameters in the sidebar and click **'Generate Concepts'** to visualize your AI architectural portfolio.")
