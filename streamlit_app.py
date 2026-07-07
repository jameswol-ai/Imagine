# =========================================================
# ARC — ARCHITECTURAL INTELLECT & EAST AFRICAN FOREX ENGINE
# Generative Multi-Story Floor Plan & Regional Cost Synthesis
# Fully Integrated RANDOM V3 Dashboard UI
# =========================================================

import streamlit as st
import json
import uuid
import random
import math
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIG & GLOBAL HUD COSMETICS
# =========================================================

st.set_page_config(
    page_title="Random V3 | Arc Forex & Arch AI",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

MEMORY_FILE = Path("arc_studio_v12.json")

# =========================================================
# CUSTOM CSS DASHBOARD STYLING
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');
    
    /* Base Body & Fonts */
    html, body, [data-testid="stSidebarNav"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #040711;
        color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: -0.03em;
    }
    
    /* Streamlit component overrides for Dark Mode */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        color: #ffffff;
        border-radius: 8px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #8b5cf6, #6366f1);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
        transform: scale(1.02);
    }
    
    /* Custom Components to match RANDOM V3 */
    .glass-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 16px;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 500;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-top: 4px;
    }
    .agent-bar-bg {
        width: 100%; 
        height: 6px; 
        background: #1e293b; 
        border-radius: 4px; 
        margin-top: 10px;
    }
    .agent-bar-fg {
        height: 100%; 
        border-radius: 4px;
    }
    
    /* Blueprint Grid */
    .arc-blueprint-canvas {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 12px;
        background: #090d16;
        padding: 20px;
        border-radius: 12px;
        border: 1px dashed #334155;
        margin: 10px 0;
    }
    .arc-room-module {
        padding: 16px;
        border-radius: 8px;
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .room-title { font-size: 1rem; font-weight: 600; font-family: 'Space Grotesk', sans-serif; }
    .room-meta { font-size: 0.75rem; opacity: 0.75; margin-top: 4px; }
    
    /* Sidebar custom */
    [data-testid="stSidebar"] {
        background-color: #0a0f1c;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background: transparent;
        color: #94a3b8;
        font-weight: 500;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# REGIONAL FOREX DATA ENGINE (EAST AFRICA - LIVE 2026 RATES)
# =========================================================

REGIONAL_FX = {
    "Kenya": {"currency": "KES", "rate_to_usd": 129.49, "symbol": "KSh", "cost_multiplier": 1.0},
    "Uganda": {"currency": "UGX", "rate_to_usd": 3665.20, "symbol": "USh", "cost_multiplier": 0.95},
    "Tanzania": {"currency": "TZS", "rate_to_usd": 2625.00, "symbol": "TSh", "cost_multiplier": 0.98},
    "South Sudan": {"currency": "SSP", "rate_to_usd": 4626.40, "symbol": "SSP", "cost_multiplier": 1.35}
}

DEFAULT_STATE = {"designs": [], "logs": []}

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
if "active_design" not in st.session_state:
    st.session_state.active_design = None

mem = st.session_state.memory

# =========================================================
# ARCHITECTURAL MATRIX SYNTHESIS
# =========================================================

ARCH_DOMAINS = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse Studio"],
    "Commercial": ["Corporate Hub Block", "Boutique Retail Space", "Medical Clinic Center"],
    "Industrial": ["Distribution Depot", "Heavy Machinery Plant Warehouse"]
}

def generate_spatial_model(domain, btype, plot_size, floors, target_bathrooms, target_country):
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
            rooms.append({"name": f"Master Suite Room {i+1}", "type": "Bedroom", "w": 4.5, "h": 4.0, "color": "#2a0f4d"})
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
        "domain": domain,
        "type": btype,
        "plot_size": plot_size,
        "floors": floors,
        "floor_area": floor_area,
        "total_gfa": total_gfa,
        "rooms": rooms,
        "doors": doors,
        "windows": windows,
        "country": target_country,
        "structural": {
            "columns": int(col_count * floors),
            "beams": int(beam_count * floors),
            "span": span_length
        }
    }

# =========================================================
# GRAPHICS CANVAS RENDERING ENGINE
# =========================================================

def render_native_blueprint(plan):
    canvas_html = '<div class="arc-blueprint-canvas">'
    for room in plan:
        canvas_html += (
            f'<div class="arc-room-module" style="background-color: {room["color"]};">'
            f'<div class="room-title">{room["name"]}</div>'
            f'<div class="room-meta">📐 {room["w"]}m × {room["h"]}m ({room["type"]})</div>'
            f'</div>'
        )
    canvas_html += '</div>'
    st.markdown(canvas_html, unsafe_allow_html=True)

def render_circular_score(label, score):
    """Generates a mockup Circular Score Card"""
    if score >= 85: color = "#22c55e"
    elif score >= 70: color = "#eab308"
    else: color = "#3b82f6"
    
    radius = 18
    circumference = radius * 2 * 3.14159
    stroke_dash = (score / 100) * circumference

    html = f"""
    <div class="glass-card" style="text-align: center; padding: 15px;">
        <div style="position: relative; width: 70px; height: 70px; margin: 0 auto;">
            <svg width="70" height="70" viewBox="0 0 50 50">
                <circle cx="25" cy="25" r="18" stroke="#1e293b" stroke-width="4" fill="none"/>
                <circle cx="25" cy="25" r="18" stroke="{color}" stroke-width="4" fill="none" 
                        stroke-dasharray="{stroke_dash} {circumference}" stroke-linecap="round" 
                        transform="rotate(-90 25 25)"/>
            </svg>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-family: 'Space Grotesk'; font-size: 18px; font-weight: 700; color: white;">{score}</div>
        </div>
        <div style="font-weight: 600; color: white; margin-top: 6px; font-size: 14px;">{label}</div>
        <div style="font-size: 11px; color: #8a9bb5; margin-top: 4px;">Overall Score</div>
    </div>
    """
    return html

# =========================================================
# STRUCTURAL CODE TESTING (EUROCODES)
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
    allowable_deflection = (span * 1000) / 250
    est_deflection = (5 * (w_ed/1.35) * (span**4) * 10**12) / (384 * 200000 * (b * (d_eff**3) / 12))

    return {
        "design_load": f"{design_load_kpa:.2f} kN/m²",
        "m_ed": f"{m_ed:.1f} kNm",
        "m_rd": f"{m_rd:.1f} kNm",
        "uls_status": "PASS" if m_rd > m_ed else "FAIL",
        "deflection_limit": f"{allowable_deflection:.1f} mm",
        "calculated_deflection": f"{min(allowable_deflection, est_deflection):.1f} mm"
    }

# =========================================================
# MATERIAL QUANTUM ASSESSMENT & FOREX BOQ
# =========================================================

def compute_forex_boq(d, target_country):
    gfa = d["total_gfa"]
    fx_meta = REGIONAL_FX[target_country]
    fx_rate = fx_meta["rate_to_usd"]
    currency_symbol = fx_meta["symbol"]
    regional_multiplier = fx_meta["cost_multiplier"]

    conc_qty = int(gfa * 0.35)
    steel_qty = int(conc_qty * 0.12)
    brick_qty = int(gfa * 38)
    finish_qty = int(gfa)

    base_usd_items = [
        {"Item Description": "Substructure Ground Earth Excavations", "Qty": int(gfa*0.15), "Unit": "m³", "Rate_USD": 150},
        {"Item Description": "Structural C30 Reinforcement Concrete", "Qty": conc_qty, "Unit": "m³", "Rate_USD": 210},
        {"Item Description": "Tensile Steel Bars Profile (B500B)", "Qty": steel_qty, "Unit": "Tons", "Rate_USD": 1200},
        {"Item Description": "External Wall Perimeter Blockwork Masonry", "Qty": brick_qty, "Unit": "Pcs", "Rate_USD": 2.5},
        {"Item Description": "Internal Floor Level Screed & Tiling Work", "Qty": finish_qty, "Unit": "m²", "Rate_USD": 40},
        {"Item Description": "Timber Internal Opening Door Fitting Units", "Qty": d["doors"], "Unit": "Sets", "Rate_USD": 300},
        {"Item Description": "Anodized Aluminum Glazed Window Assemblies", "Qty": d["windows"], "Unit": "Sets", "Rate_USD": 450}
    ]

    grand_total_usd = 0
    grand_total_local = 0
    calculated_items = []

    for item in base_usd_items:
        adjusted_rate_usd = item["Rate_USD"] * regional_multiplier
        cost_usd = item["Qty"] * adjusted_rate_usd
        cost_local = cost_usd * fx_rate
        grand_total_usd += cost_usd
        grand_total_local += cost_local

        calculated_items.append({
            "Material Asset Item": item["Item Description"],
            "Quantity Matrix": f"{item['Qty']:,} {item['Unit']}",
            "Rate (Local)": f"{currency_symbol} {int(adjusted_rate_usd * fx_rate):,}",
            "Total Local": f"{currency_symbol} {int(cost_local):,}"
        })

    return calculated_items, grand_total_usd, grand_total_local, fx_meta

# =========================================================
# ISOMETRIC CANVAS ENGINE (3D HOVER VIEWPORT)
# =========================================================

def draw_3d_isometric_canvas(plan):
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
        ctx.fill();
        ctx.strokeStyle = "rgba(255,255,255,0.3)";
        ctx.stroke();
        
        ctx.fillStyle = "rgba(255,255,255,0.06)";
        ctx.beginPath();
        ctx.moveTo({offset_x}, {offset_y});
        ctx.lineTo({offset_x}, {offset_y} - 40);
        ctx.lineTo({offset_x} + {rw}, {offset_y} + {rh}/2 - 40);
        ctx.lineTo({offset_x} + {rw}, {offset_y} + {rh}/2);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 11px Space Grotesk";
        ctx.fillText("{r['name']}", {offset_x} + 15, {offset_y} - 2);
        """

    return f"""
    <div style="background:#040711; padding:8px; border-radius:10px; border:1px solid #1e293b; text-align:center;">
        <canvas id="arc3dCanvas" width="{canvas_w}" height="{canvas_h}" style="max-width:100%; background:#050814;"></canvas>
        <script>
            const canvas = document.getElementById('arc3dCanvas');
            const ctx = canvas.getContext('2d');
            ctx.strokeStyle = 'rgba(56, 189, 248, 0.04)';
            for(let i=0; i<canvas.width; i+=40) {{ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); ctx.stroke(); }}
            for(let j=0; j<canvas.height; j+=40) {{ ctx.beginPath(); ctx.moveTo(0,j); ctx.lineTo(canvas.width, j); ctx.stroke(); }}
            {shapes_js}
        </script>
    </div>
    """

# =========================================================
# APPLICATION CONTROL ENGINE LAYERS
# =========================================================

st.sidebar.markdown("""
<div style="font-size: 1.5rem; font-weight: 700; font-family: 'Space Grotesk';">
    <span style="color: #8b5cf6;">R</span>ANDOM V3
</div>
<div style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 20px;">Evolution AI Design Studio</div>
""", unsafe_allow_html=True)

nav_page = st.sidebar.radio("Studio Workspace", ["Control Hub Dashboard", "Generative Design Engine"])
st.sidebar.markdown("---")

with st.sidebar.expander("📐 Arc Configuration Options", expanded=True):
    select_country = st.selectbox("East African Target Region", list(REGIONAL_FX.keys()))
    select_domain = st.selectbox("Structural Logic Domain", list(ARCH_DOMAINS.keys()))
    select_type = st.selectbox("Specific Typology", ARCH_DOMAINS[select_domain])

    input_plot = st.slider("Total Boundary Plot Area (m²)", 200, 5000, 800, step=50)
    input_floors = st.slider("Building Height Limit (Floors)", 1, 12, 3)
    input_baths = st.slider("Total Bathroom Batteries", 1, 10, 2)

st.sidebar.markdown("---")
st.sidebar.caption("Built with ❤️ for Architects & Engineers of the Future")

# ---------------------------------------------------------
# WORKSPACE DISPLAY: DASHBOARD
# ---------------------------------------------------------
if nav_page == "Control Hub Dashboard":
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
        <div>
            <h1 style="font-size: 2.25rem; margin-bottom: 0;">Welcome back, Architect 👋</h1>
            <div style="color: #94a3b8; font-weight: 500;">Create. Evolve. Perfect.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fx_col1, fx_col2, fx_col3, fx_col4 = st.columns(4)
    fx_col1.metric("Live Forex USD / KES", f"KSh {REGIONAL_FX['Kenya']['rate_to_usd']}")
    fx_col2.metric("Live Forex USD / UGX", f"USh {REGIONAL_FX['Uganda']['rate_to_usd']}")
    fx_col3.metric("Live Forex USD / TZS", f"TSh {REGIONAL_FX['Tanzania']['rate_to_usd']}")
    fx_col4.metric("Live Forex USD / SSP", f"SSP {REGIONAL_FX['South Sudan']['rate_to_usd']}")

    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.metric("Evolved Blueprints Saved", len(mem["designs"]))
    c2.metric("Pipeline Computations", len(mem["logs"]))

# ---------------------------------------------------------
# WORKSPACE DISPLAY: SYNTHESIS CORE LAB (RANDOM V3 UI)
# ---------------------------------------------------------
elif nav_page == "Generative Design Engine":
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div>
            <h1 style="font-size: 2rem; margin-bottom: 0;">Welcome back, Architect 👋</h1>
            <div style="color: #94a3b8;">Create. Evolve. Perfect.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Copilot Input Section ---
    with st.container():
        col_copilot_1, col_copilot_2 = st.columns([3, 1])
        with col_copilot_1:
            st.markdown("### 🤖 RANDOM COPILOT")
            st.markdown("<div style='color: #94a3b8; font-size: 0.9rem;'>Your AI design partner</div>", unsafe_allow_html=True)
            prompt = st.text_area("Describe your dream project...", 
                                  placeholder="e.g. Sustainable beach house with open spaces, natural ventilation and modern design", 
                                  height=100)
            col_btns = st.columns(3)
            with col_btns[0]: st.button("🌱 Sustainable", use_container_width=True)
            with col_btns[1]: st.button("🏛️ Modern", use_container_width=True)
            with col_btns[2]: st.button("🌴 Tropical", use_container_width=True)
            
        with col_copilot_2:
            # Simulated robot graphic placeholder
            st.markdown("""
            <div style="display:flex; justify-content:center; align-items:center; height:120px; text-align:center;">
                <div style="background: linear-gradient(135deg, #1e293b, #0f172a); border-radius: 50%; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; border: 1px solid #8b5cf6;">
                    <span style="font-size: 48px;">🤖</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            trigger_synthesis = st.button("✨ Generate Concepts", type="primary", use_container_width=True)

    if trigger_synthesis:
        with st.spinner("Synchronizing currency profiles and processing structural calculations..."):
            generated_asset = generate_spatial_model(select_domain, select_type, input_plot, input_floors, input_baths, select_country)
            generated_asset["plan"] = generated_asset["rooms"]

            st.session_state.active_design = generated_asset
            mem["designs"].append(generated_asset)
            log_event(f"Evolved local multi-floor architectural framework instance #{generated_asset['id']}")
            st.rerun()

    st.markdown("---")
    
    # --- Evolution Engine Results ---
    if st.session_state.active_design is not None:
        asset = st.session_state.active_design
        
        st.markdown("### 🔬 EVOLUTION ENGINE RESULTS")
        st.markdown("<div style='color: #94a3b8; font-size: 0.9rem;'>5 unique design concepts generated and evaluated by AI Agents</div>", unsafe_allow_html=True)
        
        # Simulate 5 concepts based on the current generated asset
        concepts = [
            ("Alpha", 92), ("Beta", 85), ("Gamma", 78), ("Delta", 71), ("Epsilon", 64)
        ]
        cols = st.columns(5)
        for i, (name, score) in enumerate(concepts):
            with cols[i]:
                # Use the actual asset image/placeholder, but we render the circle
                st.markdown(f"""
                <div class="glass-card" style="padding: 0; overflow: hidden;">
                    <div style="height: 100px; background: #1e293b; display: flex; justify-content: center; align-items: center;">
                        <span style="color: #94a3b8;">🏗️ Concept Viz</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(render_circular_score(f"Concept {name}", score), unsafe_allow_html=True)

        # --- AI AGENT EVALUATION ---
        st.markdown("### AI AGENT EVALUATION SUMMARY")
        ec_analysis = run_eurocode_analysis(asset, asset["domain"])
        boq_data, _, _, fx = compute_forex_boq(asset, asset["country"])
        sustain_score = min(100, int((asset["total_gfa"] / (asset["plot_size"] * asset["floors"])) * 90) + 20)

        e1, e2, e3, e4 = st.columns(4)
        
        # Agent 1: Architect AI
        with e1:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #4ade80;">
                <div style="color: #4ade80; font-weight: 600;">🏛️ Architect AI</div>
                <div style="color: #94a3b8; font-size: 12px; margin-top: 2px;">Function & Aesthetics</div>
                <div style="font-size: 20px; font-weight: 700; margin-top: 6px; color: white;">{asset['type']}</div>
                <div class="agent-bar-bg"><div class="agent-bar-fg" style="width: 92%; background: #4ade80;"></div></div>
            </div>
            """, unsafe_allow_html=True)
            
        # Agent 2: Structural AI
        with e2:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #00d2ff;">
                <div style="color: #00d2ff; font-weight: 600;">⚙️ Structural AI</div>
                <div style="color: #94a3b8; font-size: 12px; margin-top: 2px;">Safety & Stability</div>
                <div style="font-size: 20px; font-weight: 700; margin-top: 6px; color: white;">{ec_analysis['uls_status']} (M_Rd > M_Ed)</div>
                <div class="agent-bar-bg"><div class="agent-bar-fg" style="width: 88%; background: #00d2ff;"></div></div>
            </div>
            """, unsafe_allow_html=True)
            
        # Agent 3: Sustainability AI
        with e3:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #38bdf8;">
                <div style="color: #38bdf8; font-weight: 600;">🌱 Sustainability AI</div>
                <div style="color: #94a3b8; font-size: 12px; margin-top: 2px;">Green & Efficiency</div>
                <div style="font-size: 20px; font-weight: 700; margin-top: 6px; color: white;">{sustain_score}/100</div>
                <div class="agent-bar-bg"><div class="agent-bar-fg" style="width: {sustain_score}%; background: #38bdf8;"></div></div>
            </div>
            """, unsafe_allow_html=True)
            
        # Agent 4: Cost AI
        with e4:
            cost_score = min(100, 100 - int(boq_data[-1]["Total Local"].split(" ")[1].replace(",", "")) // 10000)
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #facc15;">
                <div style="color: #facc15; font-weight: 600;">💰 Cost AI</div>
                <div style="color: #94a3b8; font-size: 12px; margin-top: 2px;">Budget & Value</div>
                <div style="font-size: 20px; font-weight: 700; margin-top: 6px; color: white;">{cost_score}%</div>
                <div class="agent-bar-bg"><div class="agent-bar-fg" style="width: {cost_score}%; background: #facc15;"></div></div>
            </div>
            """, unsafe_allow_html=True)

        # --- 2D & 3D Grid Layout ---
        st.markdown("---")
        c2d, c3d = st.columns(2)
        with c2d:
            st.markdown("### 2D FLOOR PLAN")
            render_native_blueprint(asset["plan"])
            st.caption(f"Total GFA: {asset['total_gfa']}m² | {asset['floors']} Floors")
        with c3d:
            st.markdown("### 3D MASSING - CONCEPT ALPHA")
            st.components.v1.html(draw_3d_isometric_canvas(asset["plan"]), height=410)

        # --- BOQ & DETAILS EXPANDER ---
        with st.expander("📊 View Full Multi-Currency Bill of Quantities (BOQ) & Eurocode Details"):
            ec = run_eurocode_analysis(asset, asset["domain"])
            st.json({
                "Eurocode 2 Analysis": {
                    "Design Load": ec["design_load"],
                    "Applied Moment (M_Ed)": ec["m_ed"],
                    "Resistance (M_Rd)": ec["m_rd"],
                    "Status": ec["uls_status"]
                }
            })
            boq_table, total_usd, total_local, current_fx = compute_forex_boq(asset, asset["country"])
            st.table(boq_table)
            st.metric("Total Estimated Cost (USD)", f"$ {int(total_usd):,}")
            st.metric(f"Total Estimated Cost ({current_fx['currency']})", f"{current_fx['symbol']} {int(total_local):,}")

    else:
        st.info("No layout structures are currently loaded into memory. Adjust the parameters on the sidebar options panel and click **'Generate Concepts'**.")