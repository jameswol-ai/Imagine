# =========================================================
# ARC — ARCHITECTURAL INTELLECT & EAST AFRICAN FOREX ENGINE
# Generative Multi-Story Floor Plan & Regional Cost Synthesis
# Sai Engine & Random FX Visual Overhaul v14.0 – Enhanced UI
# =========================================================

import streamlit as st
import json
import uuid
import random
import time
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG & GLOBAL HUD COSMETICS
# =========================================================

st.set_page_config(
    page_title="RANDOM V3 | Sai Engine & FX",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

MEMORY_FILE = Path("arc_studio_v13.json")

# =========================================================
# ADVANCED CUSTOM CSS & ANIMATED GLASSMORPHISM ENGINE
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');
    
    /* Animated background gradients */
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
    
    /* Glassmorphism Card Effect - enhanced */
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

    /* Glowing accent cards */
    .glow-edge {
        position: relative;
        border: 1px solid rgba(56, 189, 248, 0.25);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.08);
    }
    
    /* Input & Text Overrides */
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
    
    /* Supercharged Generate Button */
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
    
    /* Metric progress bars with shimmer */
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
    
    /* Sidebar Upgrade */
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
    
    /* Concept card mini floor-plan pattern */
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
    
    /* Floating decorations */
    .float-element {
        animation: float 6s ease-in-out infinite;
    }
    
    /* 3D canvas container */
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
    
    /* Score card accent borders */
    .score-card {
        border-left: 4px solid;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# ENHANCED RANDOM FX ENGINE (EAST AFRICA 2026)
# =========================================================

REGIONAL_FX = {
    "Kenya":       {"currency": "KES", "rate": 129.49, "symbol": "KSh", "multiplier": 1.00, "region": "East Africa"},
    "Uganda":      {"currency": "UGX", "rate": 3665.20, "symbol": "USh", "multiplier": 0.95, "region": "East Africa"},
    "Tanzania":    {"currency": "TZS", "rate": 2625.00, "symbol": "TSh", "multiplier": 0.98, "region": "East Africa"},
    "South Sudan": {"currency": "SSP", "rate": 4626.40, "symbol": "SSP", "multiplier": 1.35, "region": "East Africa"},
    "Rwanda":      {"currency": "RWF", "rate": 1330.00, "symbol": "FRw", "multiplier": 0.85, "region": "Central Africa"},
    "Ethiopia":    {"currency": "ETB", "rate": 125.00, "symbol": "Br",  "multiplier": 0.80, "region": "Horn of Africa"}
}

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
# ARCHITECTURAL MATRIX SYNTHESIS (unchanged core logic)
# =========================================================

ARCH_DOMAINS = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse Studio"],
    "Commercial": ["Corporate Hub Block", "Boutique Retail Space", "Medical Clinic Center"],
    "Industrial": ["Distribution Depot", "Heavy Machinery Plant Warehouse"]
}

def generate_spatial_model(domain, btype, plot_size, floors, target_bathrooms, target_country, seed=0):
    random.seed(seed if seed else int(time.time()))
    max_footprint = int(plot_size * 0.65)
    floor_area = min(max_footprint, random.randint(120, int(max_footprint * 1.1)))
    total_gfa = floor_area * floors

    span_length = 6.0 if domain == "Residential" else (7.5 if domain == "Commercial" else 12.0)
    col_count = max(12, int((floor_area / (span_length * 5.0)) * 4))
    beam_count = int(col_count * 1.8)

    rooms = []
    rooms.append({"name": "Central Corridor Gallery", "type": "Corridor", "w": 2.5, "h": 14.0, "color": "#1e293b"})
    rooms.append({"name": "Main Staircase Core", "type": "Stairs", "w": 4.5, "h": 4.0, "color": "#334155"})

    if domain == "Residential":
        rooms.append({"name": "Grand Living Room", "type": "Living Room", "w": 7.0, "h": 5.5, "color": "#0d2040"})
        rooms.append({"name": "Chef's Kitchen Deck", "type": "Kitchen", "w": 4.5, "h": 4.0, "color": "#053020"})
        bedroom_count = max(1, int(total_gfa / 75))
        for i in range(bedroom_count):
            rooms.append({"name": f"Master Suite {i+1}", "type": "Bedroom", "w": 4.5, "h": 4.0, "color": "#2a0f4d"})
    elif domain == "Commercial":
        rooms.append({"name": "Co-Working Hub Suite", "type": "Office Space", "w": 12.0, "h": 8.0, "color": "#075e8a"})
        rooms.append({"name": "Executive Dialogue Hall", "type": "Conference", "w": 6.0, "h": 5.0, "color": "#1e1b4b"})
    else:
        rooms.append({"name": "Main Production Bay Floor", "type": "Manufacturing Floor", "w": 18.0, "h": 12.0, "color": "#3b0764"})
        rooms.append({"name": "Logistics Dispatch Terminal", "type": "Loading Bay", "w": 8.0, "h": 8.0, "color": "#451a03"})

    for b in range(target_bathrooms):
        rooms.append({"name": f"Sanitary Bathroom {b+1}", "type": "Bathroom", "w": 3.0, "h": 2.5, "color": "#4a2306"})

    doors = len(rooms) + floors * 2
    windows = max(4, int(total_gfa / 16))

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "domain": domain, "type": btype, "plot_size": plot_size,
        "floors": floors, "floor_area": floor_area, "total_gfa": total_gfa,
        "rooms": rooms, "doors": doors, "windows": windows,
        "country": target_country,
        "structural": {"columns": int(col_count * floors), "beams": int(beam_count * floors), "span": span_length}
    }

# =========================================================
# GRAPHICS RENDERING (2D & 3D)
# =========================================================

def render_native_blueprint(plan):
    canvas_html = '<div class="arc-blueprint-canvas" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(220px,1fr)); gap:14px; background:#0a0f1c; padding:24px; border-radius:18px; border:1px dashed #334155; margin:10px 0; box-shadow: inset 0 0 30px rgba(0,0,0,0.5);">'
    for room in plan:
        canvas_html += (
            f'<div style="padding:16px; border-radius:12px; color:#fff; border:1px solid rgba(255,255,255,0.08); background-color:{room["color"]}; box-shadow:0 8px 24px rgba(0,0,0,0.4); transition: all 0.2s ease; cursor:pointer;" onmouseover="this.style.transform=\'scale(1.03)\'; this.style.boxShadow=\'0 12px 32px rgba(0,0,0,0.6)\';" onmouseout="this.style.transform=\'scale(1)\'; this.style.boxShadow=\'0 8px 24px rgba(0,0,0,0.4)\';">'
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

# =========================================================
# SAI ENGINE - AI AGENT METRICS SYNTHESIS (unchanged)
# =========================================================

def run_eurocode_analysis(d, domain):
    span = d["structural"]["span"]
    gk = 5.5  
    qk = 2.0 if domain == "Residential" else (3.5 if domain == "Commercial" else 7.5)
    design_load_kpa = (1.35 * gk) + (1.50 * qk)
    w_ed = design_load_kpa * 4.5  
    m_ed = (w_ed * (span ** 2)) / 8
    b = 300; d_eff = 450; f_ck = 30  
    m_rd = (0.167 * f_ck * b * (d_eff ** 2)) / 10**6
    return {
        "design_load": f"{design_load_kpa:.2f} kN/m²",
        "m_ed": f"{m_ed:.1f} kNm",
        "m_rd": f"{m_rd:.1f} kNm",
        "uls_status": "PASS" if m_rd > m_ed else "FAIL"
    }

def compute_forex_boq(d, target_country):
    gfa = d["total_gfa"]
    fx_meta = REGIONAL_FX[target_country]
    fx_rate = fx_meta["rate"]
    regional_multiplier = fx_meta["multiplier"]

    conc_qty = int(gfa * 0.35); steel_qty = int(conc_qty * 0.12); brick_qty = int(gfa * 38); finish_qty = int(gfa)
    base_usd_items = [
        {"Item": "Substructure Earth Excavations", "Qty": int(gfa*0.15), "Unit": "m³", "Rate": 150},
        {"Item": "Structural C30 Concrete", "Qty": conc_qty, "Unit": "m³", "Rate": 210},
        {"Item": "Tensile Steel Bars (B500B)", "Qty": steel_qty, "Unit": "Tons", "Rate": 1200},
        {"Item": "Blockwork Masonry", "Qty": brick_qty, "Unit": "Pcs", "Rate": 2.5},
        {"Item": "Floor Screed & Tiling", "Qty": finish_qty, "Unit": "m²", "Rate": 40},
        {"Item": "Timber Door Fittings", "Qty": d["doors"], "Unit": "Sets", "Rate": 300},
        {"Item": "Aluminum Window Assemblies", "Qty": d["windows"], "Unit": "Sets", "Rate": 450}
    ]
    grand_total_usd = 0
    for item in base_usd_items:
        adjusted_rate = item["Rate"] * regional_multiplier
        grand_total_usd += item["Qty"] * adjusted_rate
    grand_total_local = grand_total_usd * fx_rate
    return grand_total_usd, grand_total_local, fx_meta

def calculate_ai_scores(asset, ec_result, total_usd, prompt_keywords=None):
    arch_score = 50 + min(20, asset['floors'] * 3) + min(15, len(asset['rooms']) * 1.5)
    arch_score = min(100, arch_score + random.randint(-5, 5))

    try:
        m_ed_val = float(ec_result['m_ed'].split(" ")[0])
        m_rd_val = float(ec_result['m_rd'].split(" ")[0])
        struct_score = 80 + (min(20, (m_rd_val - m_ed_val) / m_ed_val * 15))
    except: struct_score = 60
    if ec_result['uls_status'] == "FAIL": struct_score = 40
    struct_score = min(100, max(0, int(struct_score)))

    sustain_score = 50 + min(30, int(asset['windows'] * 1.5))
    sust_efficiency = int((asset['total_gfa'] / (asset['plot_size'] * asset['floors'])) * 100)
    sustain_score += sust_efficiency
    if prompt_keywords and 'sustain' in prompt_keywords: sustain_score += 10
    sustain_score = min(100, sustain_score)

    cost_score = 70
    cost_per_m2 = total_usd / asset['total_gfa']
    if cost_per_m2 < 450: cost_score += 25
    elif cost_per_m2 < 650: cost_score += 15
    else: cost_score += 5
    cost_score = min(100, int(cost_score))

    return arch_score, struct_score, sustain_score, cost_score

# =========================================================
# APPLICATION UI LAYERS
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
    select_country = st.selectbox("East African Target Region", list(REGIONAL_FX.keys()))
    select_domain = st.selectbox("Structural Logic Domain", list(ARCH_DOMAINS.keys()))
    select_type = st.selectbox("Specific Typology", ARCH_DOMAINS[select_domain])
    input_plot = st.slider("Total Boundary Plot Area (m²)", 200, 5000, 800, step=50)
    input_floors = st.slider("Building Height Limit (Floors)", 1, 12, 3)
    input_baths = st.slider("Total Bathroom Batteries", 1, 10, 2)

# --- PROJECT MEMORY (Sidebar Bottom) ---
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

# ---------------------------------------------------------
# DASHBOARD VIEW
# ---------------------------------------------------------
if nav_page == "Control Hub Dashboard":
    st.markdown("""
    <div class="glass-panel float-element" style="margin-bottom: 32px; text-align: center;">
        <h1 style="font-size: 2.5rem; margin-bottom: 4px;">Welcome back, Architect 👋</h1>
        <div style="color: #94a3b8; font-size: 1.1rem;">Create. Evolve. Perfect.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💹 LIVE RANDOM FX INDICES")
    fx_cols = st.columns(6)
    for i, (country, data) in enumerate(REGIONAL_FX.items()):
        with fx_cols[i]:
            st.markdown(f"""
            <div class="glass-panel" style="padding: 16px 8px; text-align: center;">
                <div style="font-size: 0.8rem; color: #94a3b8;">{country}</div>
                <div style="font-size: 1.5rem; font-weight: 700; font-family: 'Space Grotesk';">{data['symbol']} {data['rate']}</div>
                <div style="font-size: 0.7rem; color: #22c55e;">▴ {data['region']}</div>
            </div>
            """, unsafe_allow_html=True)

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

# ---------------------------------------------------------
# GENERATIVE ENGINE VIEW (RANDOM V3 UI) – Enhanced
# ---------------------------------------------------------
elif nav_page == "Generative Design Engine":
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
        <div class="glass-panel" style="padding: 20px 32px;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0; background: linear-gradient(135deg, #8b5cf6, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Synthesis Lab</h1>
            <div style="color: #94a3b8; font-size: 0.95rem;">Sai Engine & Evolution Matrix Active</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Copilot Input
    with st.container():
        col_input, col_gen = st.columns([2.5, 1])
        with col_input:
            st.markdown("### 🤖 RANDOM COPILOT")
            st.markdown("<div style='color: #94a3b8; font-size: 0.9rem;'>Your AI design partner</div>", unsafe_allow_html=True)
            prompt = st.text_area("Describe your dream project...", placeholder="e.g. Sustainable beach house with open spaces, modern aesthetic...", height=100)

            tag_c1, tag_c2, tag_c3 = st.columns(3)
            if tag_c1.button("🌱 Sustainable", use_container_width=True): st.session_state.ai_boost = 10
            if tag_c2.button("🏛️ Modern", use_container_width=True): st.session_state.ai_boost = 5
            if tag_c3.button("🌴 Tropical", use_container_width=True): st.session_state.ai_boost = 8

        with col_gen:
            st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
            trigger_synthesis = st.button("✨ Generate Concepts", type="primary", use_container_width=True)

    # --- Evolution Engine & Sai Processing ---
    if trigger_synthesis:
        with st.spinner("🧠 Sai Engine synthesizing 5 architectural variations..."):
            concepts = []
            for i in range(5):
                mut_plot = input_plot + random.randint(-150, 150)
                mut_floors = max(1, input_floors + random.randint(-1, 1))
                mut_rooms = max(1, input_baths + random.randint(-1, 1))
                d = generate_spatial_model(select_domain, select_type, mut_plot, mut_floors, mut_rooms, select_country, seed=i)
                d["plan"] = d["rooms"]
                concepts.append(d)

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
                ec = run_eurocode_analysis(c, c['domain'])
                total_usd, total_local, fx = compute_forex_boq(c, c['country'])
                arch, struct, sust, cost = calculate_ai_scores(c, ec, total_usd, prompt)

                st.markdown(f"""
                <div class="glass-panel glow-edge" style="padding: 16px; border-left: 4px solid {concept_colors[i]}; text-align: center;">
                    <div class="mini-plan">
                        <div style="color: #64748b; font-size: 0.8rem;">🏗️ Concept {concept_names[i]}</div>
                    </div>
                    <div style="font-weight: 600; color: {concept_colors[i]}; font-size: 1.1rem;">{concept_names[i]}</div>
                    <div style="font-size: 12px; color: #94a3b8; margin-bottom: 12px;">{c['type']}</div>
                    
                    <div style="font-size: 0.75rem; text-align: left; margin-top: 5px; color: #94a3b8;">🏛️ Arch {arch}%</div>
                    <div class="metric-bar-bg"><div class="metric-bar-fg" style="width: {arch}%; background: {concept_colors[i]};"></div></div>
                    
                    <div style="font-size: 0.75rem; text-align: left; margin-top: 5px; color: #94a3b8;">⚙️ Struct {struct}%</div>
                    <div class="metric-bar-bg"><div class="metric-bar-fg" style="width: {struct}%; background: #00d2ff;"></div></div>
                    
                    <div style="font-size: 0.75rem; text-align: left; margin-top: 5px; color: #94a3b8;">🌱 Sustain {sust}%</div>
                    <div class="metric-bar-bg"><div class="metric-bar-fg" style="width: {sust}%; background: #38bdf8;"></div></div>
                    
                    <div style="font-size: 0.75rem; text-align: left; margin-top: 5px; color: #94a3b8;">💰 Cost {cost}%</div>
                    <div class="metric-bar-bg"><div class="metric-bar-fg" style="width: {cost}%; background: #facc15;"></div></div>
                </div>
                """, unsafe_allow_html=True)

        # Alpha details with enhanced cards
        st.markdown("---")
        asset = st.session_state.generated_concepts[0]
        st.markdown("### 🏆 TOP RECOMMENDATION: CONCEPT ALPHA")

        ec_alpha = run_eurocode_analysis(asset, asset['domain'])
        total_usd_a, total_local_a, fx_a = compute_forex_boq(asset, asset['country'])
        arch_a, struct_a, sust_a, cost_a = calculate_ai_scores(asset, ec_alpha, total_usd_a, prompt)

        a1, a2, a3, a4 = st.columns(4)
        with a1:
            st.markdown(f"""
            <div class="glass-panel score-card" style="border-left-color: #4ade80;">
                <div style="color: #4ade80; font-weight:600;">🏛️ Architect AI</div>
                <div style="color:#94a3b8; font-size:12px;">Function & Aesthetics</div>
                <div style="font-size:20px; font-weight:700;">{asset['type']}</div>
                <div class="metric-bar-bg"><div class="metric-bar-fg" style="width:{arch_a}%; background:#4ade80;"></div></div>
                <div style="font-size: 12px; margin-top: 6px;">{arch_a}% Match</div>
            </div>
            """, unsafe_allow_html=True)
        with a2:
            st.markdown(f"""
            <div class="glass-panel score-card" style="border-left-color: #00d2ff;">
                <div style="color: #00d2ff; font-weight:600;">⚙️ Structural AI</div>
                <div style="color:#94a3b8; font-size:12px;">Safety & Stability</div>
                <div style="font-size:20px; font-weight:700;">{ec_alpha['uls_status']}</div>
                <div class="metric-bar-bg"><div class="metric-bar-fg" style="width:{struct_a}%; background:#00d2ff;"></div></div>
                <div style="font-size: 12px; margin-top: 6px;">{struct_a}% Safety</div>
            </div>
            """, unsafe_allow_html=True)
        with a3:
            st.markdown(f"""
            <div class="glass-panel score-card" style="border-left-color: #38bdf8;">
                <div style="color: #38bdf8; font-weight:600;">🌱 Sustainability AI</div>
                <div style="color:#94a3b8; font-size:12px;">Green & Efficiency</div>
                <div style="font-size:20px; font-weight:700;">{asset['windows']} Windows</div>
                <div class="metric-bar-bg"><div class="metric-bar-fg" style="width:{sust_a}%; background:#38bdf8;"></div></div>
                <div style="font-size: 12px; margin-top: 6px;">{sust_a}% Eco</div>
            </div>
            """, unsafe_allow_html=True)
        with a4:
            st.markdown(f"""
            <div class="glass-panel score-card" style="border-left-color: #facc15;">
                <div style="color: #facc15; font-weight:600;">💰 Cost AI</div>
                <div style="color:#94a3b8; font-size:12px;">Budget & Value</div>
                <div style="font-size:20px; font-weight:700;">{fx_a['symbol']} {int(total_local_a):,}</div>
                <div class="metric-bar-bg"><div class="metric-bar-fg" style="width:{cost_a}%; background:#facc15;"></div></div>
                <div style="font-size: 12px; margin-top: 6px;">{cost_a}% Value</div>
            </div>
            """, unsafe_allow_html=True)

        # 2D & 3D Layout with FX BOQ
        st.markdown("---")
        col_2d, col_3d = st.columns(2)
        with col_2d:
            st.markdown("### 🗺️ 2D FLOOR PLAN")
            st.markdown(render_native_blueprint(asset["plan"]), unsafe_allow_html=True)
            st.caption(f"Total GFA: {asset['total_gfa']:,} m² | {asset['floors']} Floors | {asset['country']}")

            with st.expander("📊 Live Currency Bill of Quantities"):
                boq_table, usd, local, fx = compute_forex_boq(asset, asset['country'])
                st.metric("USD Total", f"${int(usd):,}")
                st.metric(f"Local {fx['currency']}", f"{fx['symbol']} {int(local):,}")
                st.caption(f"Rates based on 1 USD = {fx['rate']} {fx['currency']}")

        with col_3d:
            st.markdown("### 📦 3D MASSING CONCEPT")
            st.components.v1.html(render_isometric_html(asset["plan"]), height=450)
            # Decorative but non-functional buttons – visually refined
            st.markdown("""
            <div style="display: flex; gap: 10px; margin-top: 12px;">
                <div class="glass-panel" style="flex:1; text-align:center; padding:10px; cursor:default; opacity:0.7;">🖱️ Rotate</div>
                <div class="glass-panel" style="flex:1; text-align:center; padding:10px; cursor:default; opacity:0.7;">🔍 Zoom</div>
                <div class="glass-panel" style="flex:1; text-align:center; padding:10px; background: rgba(139,92,246,0.15); border-color:#8b5cf6; cursor:pointer;">📄 Export</div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("🌀 Awaiting input. Configure your structural parameters in the sidebar and click **'Generate Concepts'** to visualize your AI architectural portfolio.")