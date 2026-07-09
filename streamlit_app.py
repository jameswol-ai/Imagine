# =========================================================
# ARC STUDIO PRO – ARCHITECTURAL INTELLECT & FOREX ENGINE
# v21.0 – Forecasting, Drift Animation, Sensitivity, Compare, IFC Export
# Single-file Streamlit App
# =========================================================

import streamlit as st
import json, uuid, math, hashlib, sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from io import BytesIO
import collections
from mpl_toolkits.mplot3d import Axes3D  # ensure 3D works

# ------------------------------------------------------------
# CUSTOM THEME
# ------------------------------------------------------------
st.set_page_config(page_title="Arc Studio Pro", page_icon="📐", layout="wide")
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
    .stSidebar { background: #1e293b; border-right: 1px solid #38bdf8; }
    h1,h2,h3,h4,h5,h6 { color: #38bdf8 !important; }
    .stMetric { background: rgba(56,189,248,0.1); border-radius:12px; padding:10px; border:1px solid #38bdf8; }
    .stButton button { background:#38bdf8; color:#0f172a; font-weight:bold; border-radius:8px; }
    .stButton button:hover { background:#0284c7; color:white; }
    .stTabs [data-baseweb="tab"] { background:#1e293b; border-radius:8px 8px 0 0; color:#94a3b8; }
    .stTabs [aria-selected="true"] { background:#38bdf8 !important; color:#0f172a !important; }
</style>""", unsafe_allow_html=True)

# ------------------------------------------------------------
# DATABASE & AUTH
# ------------------------------------------------------------
USER_DB = Path("arc_users.db")
def init_user_db():
    conn = sqlite3.connect(USER_DB); c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password_hash TEXT NOT NULL, role TEXT DEFAULT 'user', email TEXT DEFAULT '')''')
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO users VALUES (?,?,'admin','admin@arc.studio')", ("admin", admin_hash))
    conn.commit(); conn.close()

def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()
def authenticate_user(u, p):
    conn = sqlite3.connect(USER_DB); c = conn.cursor()
    c.execute("SELECT password_hash,role FROM users WHERE username=?", (u,))
    row = c.fetchone(); conn.close()
    if row: db_hash, role = row; return (True, role) if hash_password(p) == db_hash else (False, None)
    return (False, None)
def register_user(u, p, email="", role="user"):
    conn = sqlite3.connect(USER_DB); c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?,?,?,?)", (u, hash_password(p), role, email))
        conn.commit(); return True, f"User '{u}' created."
    except sqlite3.IntegrityError: return False, "Username exists."
    finally: conn.close()
def get_all_users():
    conn = sqlite3.connect(USER_DB); c = conn.cursor(); c.execute("SELECT username,role,email FROM users"); users = c.fetchall(); conn.close(); return users
def delete_user(u):
    conn = sqlite3.connect(USER_DB); c = conn.cursor(); c.execute("DELETE FROM users WHERE username=?", (u,)); conn.commit(); conn.close()
init_user_db()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.show_registration = False

def login_page():
    st.markdown("<h1 style='text-align:center'>🔐 Arc Studio Pro Login</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        with st.form("login"):
            u = st.text_input("Username"); p = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                ok, role = authenticate_user(u, p)
                if ok: st.session_state.authenticated = True; st.session_state.username = u; st.session_state.role = role; st.rerun()
                else: st.error("Invalid credentials")
        if st.button("Register new account"): st.session_state.show_registration = True; st.rerun()
def registration_page():
    st.markdown("<h2 style='text-align:center'>📝 Create Account</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        with st.form("register"):
            u = st.text_input("Username"); p = st.text_input("Password", type="password"); e = st.text_input("Email (optional)")
            if st.form_submit_button("Register"):
                if not u or not p: st.error("Username and password required.")
                else:
                    ok, msg = register_user(u, p, e)
                    if ok: st.success(msg + " You can login now."); st.session_state.show_registration = False
                    else: st.error(msg)
        if st.button("Back to Login"): st.session_state.show_registration = False; st.rerun()

if not st.session_state.authenticated:
    if st.session_state.show_registration: registration_page()
    else: login_page()
    st.stop()

def logout():
    for k in ["authenticated","username","role","show_registration"]:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

# ------------------------------------------------------------
# DATA CONFIGURATIONS
# ------------------------------------------------------------
REGIONAL_FX = {
    "Kenya": {"currency":"KES","rate_to_usd":129.49,"symbol":"KSh","cost_multiplier":1.0,"risk_premium":0.02},
    "Uganda": {"currency":"UGX","rate_to_usd":3665.20,"symbol":"USh","cost_multiplier":0.95,"risk_premium":0.03},
    "Tanzania": {"currency":"TZS","rate_to_usd":2625.00,"symbol":"TSh","cost_multiplier":0.98,"risk_premium":0.025},
    "South Sudan": {"currency":"SSP","rate_to_usd":4626.40,"symbol":"SSP","cost_multiplier":1.35,"risk_premium":0.08}
}
ARCH_DOMAINS = {
    "Residential": {"types":["Luxury Villa","Modern Apartment","Townhouse Studio"],"max_coverage":0.5,"max_far":2.5},
    "Commercial": {"types":["Corporate Hub Block","Boutique Retail Space","Medical Clinic Center"],"max_coverage":0.7,"max_far":4.5},
    "Industrial": {"types":["Distribution Depot","Heavy Machinery Plant Warehouse"],"max_coverage":0.6,"max_far":1.8}
}
SOIL_PROFILES = {
    "Kampala Red Lateritic Clay": {"cohesion":35,"friction_angle":12,"unit_weight":18.0},
    "Nairobi Black Cotton Soil": {"cohesion":15,"friction_angle":8,"unit_weight":16.5},
    "Coastal Quartz Sand (Dar)": {"cohesion":0,"friction_angle":32,"unit_weight":19.0},
    "Juba Alluvial Silt Deposit": {"cohesion":20,"friction_angle":15,"unit_weight":17.5}
}
SEISMIC_ZONES = {"Low (PGA=0.05g)":{"PGA":0.05,"S":1.0,"importance":1.0},"Moderate (PGA=0.15g)":{"PGA":0.15,"S":1.2,"importance":1.0},"High (PGA=0.25g)":{"PGA":0.25,"S":1.4,"importance":1.25}}
WIND_ZONES = {"Low (22 m/s)":22,"Moderate (28 m/s)":28,"High (35 m/s)":35}
ROOM_COLORS = {"Bedroom":"#a78bfa","Living Room":"#34d399","Kitchen":"#fbbf24","Bathroom":"#60a5fa","Office":"#f87171","Dining":"#f472b6","Corridor":"#94a3b8","Garage":"#64748b"}

# ------------------------------------------------------------
# STATE MANAGEMENT
# ------------------------------------------------------------
MEMORY_FILE = Path("arc_studio_v21.json")
def load_memory():
    if MEMORY_FILE.exists():
        try: return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except: pass
    return {"designs":[],"logs":[]}
def save_memory(mem): MEMORY_FILE.write_text(json.dumps(mem, indent=2), encoding="utf-8")
def log_event(msg):
    mem = st.session_state.memory
    mem["logs"].append({"time":datetime.now().isoformat(),"user":st.session_state.username,"msg":msg})
    save_memory(mem)

if "memory" not in st.session_state: st.session_state.memory = load_memory()
if "active_design" not in st.session_state: st.session_state.active_design = None

# ------------------------------------------------------------
# CORE FUNCTIONS
# ------------------------------------------------------------
def generate_intelligent_layout(rooms, nx, ny, span):
    grid = np.full((ny, nx), "Corridor", dtype=object)
    indices = [(i,j) for i in range(ny) for j in range(nx)]; np.random.shuffle(indices)
    for idx, room in enumerate(rooms):
        if idx >= len(indices): break
        i, j = indices[idx]; grid[i, j] = room
    return grid.tolist()

def generate_building_model(domain, btype, floors, baths, country, material_frame, plot_size, soil_type, g_k, q_k, steel_section, seismic_zone, wind_zone, username):
    room_map = {
        "Luxury Villa": ["Bedroom","Bedroom","Bedroom","Living Room","Kitchen","Bathroom","Dining","Office"],
        "Modern Apartment": ["Living Room","Bedroom","Kitchen","Bathroom"],
        "Townhouse Studio": ["Living Room","Bedroom","Kitchen","Bathroom","Corridor"],
        "Corporate Hub Block": ["Office","Office","Office","Corridor","Bathroom"],
        "Boutique Retail Space": ["Living Room","Corridor","Bathroom"],
        "Medical Clinic Center": ["Office","Office","Corridor","Bathroom"],
        "Distribution Depot": ["Garage","Garage","Office","Corridor"],
        "Heavy Machinery Plant Warehouse": ["Garage","Garage","Corridor"]
    }
    rooms = room_map.get(btype, ["Living Room","Bedroom","Kitchen","Bathroom"])
    rooms.extend(["Bathroom"] * max(0, baths - rooms.count("Bathroom")))
    span = 5.0; ground_footprint = plot_size * 0.4
    bay_area = span * span; total_bays = max(2, math.ceil(ground_footprint / bay_area))
    nx = max(2, math.ceil(math.sqrt(total_bays))); ny = max(2, math.ceil(total_bays / nx))
    layout_grid = generate_intelligent_layout(rooms, nx, ny, span)
    total_gfa = ground_footprint * floors
    doors = max(1, len(rooms) * 2); windows = max(2, len(rooms) * 3)
    design = {"id":str(uuid.uuid4())[:6].upper(),"username":username,"domain":domain,"type":btype,"floors":floors,"bathrooms":baths,
              "country":country,"material_frame":material_frame,"plot_size":plot_size,"soil_type":soil_type,
              "ground_footprint":ground_footprint,"rooms":rooms,"layout":{"grid":layout_grid,"nx":nx,"ny":ny,"span":span},
              "total_gfa":total_gfa,"doors":doors,"windows":windows,
              "loads":{"g_k":g_k,"q_k":q_k,"steel_section":steel_section,"seismic_zone":seismic_zone,"wind_zone":wind_zone},
              "created":datetime.now().isoformat()}
    design["analysis"] = run_eurocode_analysis(design)
    design["zoning"] = verify_zoning_laws(design)
    design["boq"] = compute_detailed_forex_boq(design)
    return design

def ensure_design_compatibility(design):
    if "layout" not in design:
        span = 5.0; ground_footprint = design.get("ground_footprint", design["plot_size"]*0.4)
        bay_area = span * span; total_bays = max(2, math.ceil(ground_footprint / bay_area))
        nx = max(2, math.ceil(math.sqrt(total_bays))); ny = max(2, math.ceil(total_bays / nx))
        layout_grid = generate_intelligent_layout(design.get("rooms", ["Living Room","Bedroom","Kitchen","Bathroom"]), nx, ny, span)
        design["layout"] = {"grid":layout_grid,"nx":nx,"ny":ny,"span":span}
    if "loads" not in design:
        design["loads"] = {"g_k":5.5,"q_k":2.5 if design.get("domain")=="Residential" else (4.0 if design.get("domain")=="Commercial" else 7.5),"steel_section":None,"seismic_zone":"Moderate (PGA=0.15g)","wind_zone":"Moderate (28 m/s)"}
    else:
        d = design["loads"]
        if "seismic_zone" not in d: d["seismic_zone"] = "Moderate (PGA=0.15g)"
        if "wind_zone" not in d: d["wind_zone"] = "Moderate (28 m/s)"
        if "g_k" not in d: d["g_k"] = 5.5
        if "q_k" not in d: d["q_k"] = 2.5 if design.get("domain")=="Residential" else (4.0 if design.get("domain")=="Commercial" else 7.5)
        if "steel_section" not in d: d["steel_section"] = None
    if "analysis" not in design: design["analysis"] = run_eurocode_analysis(design)
    if "zoning" not in design: design["zoning"] = verify_zoning_laws(design)
    if "boq" not in design: design["boq"] = compute_detailed_forex_boq(design)
    return design

def run_eurocode_analysis(design):
    span = design.get("layout", {}).get("span", 5.0)
    gk = design["loads"]["g_k"]; qk = design["loads"]["q_k"]
    seismic = SEISMIC_ZONES.get(design["loads"]["seismic_zone"], {"PGA":0.15})
    wind_speed = WIND_ZONES.get(design["loads"]["wind_zone"], 28)
    soil = SOIL_PROFILES.get(design["soil_type"], {})
    floors = design["floors"]
    M = (gk + 1.5*qk) * span**2 / 8
    base_pressure = (gk + qk) * floors * 1.5
    footing_width = math.sqrt(base_pressure / max(soil.get("cohesion", 20), 1))
    wind_force = 0.613 * wind_speed**2 * span * floors / 1000
    drift = wind_force * floors**3 / 2000
    return {"max_moment_kNm":round(M,2),"footing_width_m":round(footing_width,2),"wind_base_shear_kN":round(wind_force,2),"drift_mm":round(drift,2),"seismic_base_shear_kN":round(seismic["PGA"]*floors*100*span*5,2),"status":"PASS" if M<100 else "REVIEW"}

def verify_zoning_laws(design):
    max_cov = ARCH_DOMAINS[design["domain"]]["max_coverage"]; max_far = ARCH_DOMAINS[design["domain"]]["max_far"]
    cov = design["ground_footprint"] / design["plot_size"]; far = design["total_gfa"] / design["plot_size"]
    return {"coverage":round(cov,2),"coverage_ok":cov<=max_cov,"far":round(far,2),"far_ok":far<=max_far,"status":"APPROVED" if (cov<=max_cov and far<=max_far) else "VIOLATION"}

def compute_detailed_forex_boq(design, rate_overrides=None):
    country = design["country"]; fx = REGIONAL_FX[country]; mult = fx["cost_multiplier"]; risk = fx["risk_premium"]
    base_rates = {"Reinforced Concrete (Eurocode 2)":350,"Structural Steel Profile (Eurocode 3)":400,"Timber Profile (Eurocode 5)":280}
    if rate_overrides is None: rate_overrides = {}
    rate_per_m2 = rate_overrides.get(design["material_frame"], base_rates.get(design["material_frame"], 350))
    gfa = design["total_gfa"]
    substructure = 0.15 * rate_per_m2 * gfa; superstructure = 0.70 * rate_per_m2 * gfa
    finishes = 0.10 * rate_per_m2 * gfa; preliminaries = 0.05 * rate_per_m2 * gfa
    total_usd = (substructure + superstructure + finishes + preliminaries) * mult * (1 + risk)
    return {"substructure":round(substructure,2),"superstructure":round(superstructure,2),
            "finishes":round(finishes,2),"preliminaries":round(preliminaries,2),
            "total_usd":round(total_usd,2),"total_local":round(total_usd * fx["rate_to_usd"],2),
            "local_currency":fx["currency"],"symbol":fx["symbol"],"rate_used":fx["rate_to_usd"]}

# ------------------------------------------------------------
# FOREX FORECASTING
# ------------------------------------------------------------
def run_forecast(currency_code, horizon, steps, history_df=None):
    if history_df is None or currency_code not in history_df.columns:
        base_rate = REGIONAL_FX[currency_code]["rate_to_usd"]
        np.random.seed(42); noise = np.random.normal(0, 0.5, 90).cumsum()
        history = base_rate + noise; dates = [datetime.now() - timedelta(days=i) for i in range(90,0,-1)]
    else:
        history = history_df[currency_code].values; dates = history_df.index
    alpha = 0.3; smoothed = [history[0]]
    for i in range(1, len(history)): smoothed.append(alpha * history[i] + (1-alpha) * smoothed[-1])
    forecast = [smoothed[-1]] * steps
    trend = "rising" if smoothed[-1] > smoothed[-min(30,len(smoothed))] else "falling"
    last_date = dates[-1] if dates else datetime.now()
    forecast_dates = [last_date + timedelta(days=i+1) for i in range(steps)]
    chart = {"historical_dates":dates,"historical_values":history,"forecast_dates":forecast_dates,"forecast_values":forecast,"smoothed":smoothed}
    return forecast, trend, chart

# ------------------------------------------------------------
# 2D & 3D VISUALS
# ------------------------------------------------------------
def draw_2d_blueprint(design, overlay_design=None):
    layout = design["layout"]["grid"]; nx = design["layout"]["nx"]; ny = design["layout"]["ny"]
    fig, ax = plt.subplots(figsize=(8, 8*ny/nx if nx>0 else 8))
    ax.set_xlim(0, nx); ax.set_ylim(0, ny); ax.set_aspect('equal'); ax.axis('off')
    for i in range(ny):
        for j in range(nx):
            room = layout[i][j]; color = ROOM_COLORS.get(room, "#94a3b8")
            rect = mpatches.Rectangle((j, ny-1-i), 1, 1, linewidth=2, edgecolor='white', facecolor=color, alpha=0.8)
            ax.add_patch(rect); ax.text(j+0.5, ny-1-i+0.5, room[:8], ha='center', va='center', fontsize=7, color='black', weight='bold')
    if overlay_design:
        overlay = overlay_design["layout"]["grid"]; ony = min(ny, overlay_design["layout"]["ny"]); onx = min(nx, overlay_design["layout"]["nx"])
        for i in range(ony):
            for j in range(onx):
                room = overlay[i][j]; color = ROOM_COLORS.get(room, "#94a3b8")
                rect = mpatches.Rectangle((j, ny-1-i), 1, 1, linewidth=1, edgecolor='red', facecolor=color, alpha=0.3, hatch='//')
                ax.add_patch(rect)
    ax.annotate('N', xy=(0.5, ny+0.2), fontsize=14, color='white', ha='center', arrowprops=dict(facecolor='white', shrink=0.05))
    buf = BytesIO(); fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor()); plt.close(fig); buf.seek(0)
    return buf

def draw_interactive_blueprint(design):
    st.image(draw_2d_blueprint(design), use_column_width=True)
    layout = design["layout"]["grid"]; ny = len(layout); nx = len(layout[0]) if layout else 0
    cols = st.columns(3)
    with cols[0]:
        i1 = st.number_input("Row (first room)", 0, ny-1, 0, key="r1"); j1 = st.number_input("Col (first room)", 0, nx-1, 0, key="c1")
    with cols[1]:
        i2 = st.number_input("Row (second room)", 0, ny-1, 0, key="r2"); j2 = st.number_input("Col (second room)", 0, nx-1, 0, key="c2")
    with cols[2]:
        if st.button("Swap Rooms"): layout[i1][j1], layout[i2][j2] = layout[i2][j2], layout[i1][j1]; st.rerun()
    return design

def draw_3d_isometric_view(design, drift_factor=0):
    layout = design["layout"]["grid"]; ny = len(layout); nx = len(layout[0]) if layout else 0
    floors = design["floors"]
    fig = plt.figure(figsize=(8,6)); ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('none'); fig.patch.set_facecolor('#0f172a'); ax.xaxis.pane.fill = False; ax.yaxis.pane.fill = False; ax.zaxis.pane.fill = False
    for f in range(floors):
        z = f * 3.0; offset_x = drift_factor * math.sin(z/2)
        for i in range(ny):
            for j in range(nx):
                room = layout[i][j]; color = ROOM_COLORS.get(room, "#94a3b8")
                x = [j+offset_x, j+1+offset_x, j+1+offset_x, j+offset_x]; y = [i, i, i+1, i+1]; zz = [z]*4
                ax.add_collection3d(mpatches.Polygon(list(zip(x,y)), facecolor=color, alpha=0.5, edgecolor='white'))
                for (x1,y1),(x2,y2) in [((j+offset_x,i),(j+1+offset_x,i)),((j+1+offset_x,i),(j+1+offset_x,i+1)),((j+offset_x,i+1),(j+1+offset_x,i+1)),((j+offset_x,i),(j+offset_x,i+1))]:
                    ax.plot([x1,x2], [y1,y2], [z,z], color='white', linewidth=0.5)
    ax.set_xlim(0, nx); ax.set_ylim(0, ny); ax.set_zlim(0, floors*3); ax.axis('off'); st.pyplot(fig)

# ------------------------------------------------------------
# IFC / REVIT JSON EXPORT
# ------------------------------------------------------------
def generate_ifc_json(design):
    grid = design["layout"]["grid"]; nx = design["layout"]["nx"]; ny = design["layout"]["ny"]; span = design["layout"]["span"]
    floors = design["floors"]
    elements = []
    for f in range(floors):
        for i in range(ny):
            for j in range(nx):
                room = grid[i][j]
                for (x1,y1),(x2,y2) in [((j,i),(j+1,i)),((j+1,i),(j+1,i+1)),((j,i+1),(j+1,i+1)),((j,i),(j,i+1))]:
                    wall = {"type":"IfcWall","name":f"Wall_F{f}_R{i}{j}","coordinates":{"start":{"x":x1*span,"y":y1*span,"z":f*3},"end":{"x":x2*span,"y":y2*span,"z":f*3}},"height":3}
                    elements.append(wall)
                slab = {"type":"IfcSlab","name":f"Slab_F{f}_R{i}{j}","coordinates":{"x":j*span,"y":i*span,"z":f*3},"width":span,"depth":span}
                elements.append(slab)
    return {"project_name":f"ARC_{design['id']}","elements":elements}

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("<h1 style='color:#38bdf8;'>ARC STUDIO PRO</h1>", unsafe_allow_html=True)
    st.markdown(f"👤 {st.session_state.username} ({st.session_state.role})")
    nav = st.pills("🌐 Workspace", ["Control Hub", "Synthesis Lab"], default="Control Hub")
    st.markdown("---")
    if st.session_state.role == "admin":
        with st.expander("👥 User Management"):
            with st.form("add_user_form"):
                new_u = st.text_input("New Username"); new_p = st.text_input("New Password", type="password"); new_e = st.text_input("Email"); new_r = st.selectbox("Role", ["user","admin"])
                if st.form_submit_button("Add"): ok, msg = register_user(new_u, new_p, new_e, new_r); st.success(msg) if ok else st.error(msg)
            st.write("Users:")
            for u in get_all_users():
                c1, c2, c3 = st.columns([3,1,1]); c1.write(f"{u[0]} ({u[1]})")
                if u[0] != st.session_state.username and c2.button("🗑️", key=f"del_{u[0]}"): delete_user(u[0]); st.rerun()
    with st.expander("⚙️ Configuration Matrix", expanded=True):
        country = st.selectbox("Region", list(REGIONAL_FX.keys()))
        domain = st.selectbox("Category", list(ARCH_DOMAINS.keys()))
        btype = st.selectbox("Typology", ARCH_DOMAINS[domain]["types"])
        plot = st.slider("Plot (m²)", 200, 5000, 800, 50)
        floors = st.slider("Storeys", 1, 12, 3); baths = st.slider("Bathrooms", 1, 10, 2)
        soil = st.selectbox("Soil", list(SOIL_PROFILES.keys()))
        material = st.pills("Framing", ["Reinforced Concrete (Eurocode 2)","Structural Steel Profile (Eurocode 3)","Timber Profile (Eurocode 5)"], default="Reinforced Concrete (Eurocode 2)")
        g_k = st.slider("Permanent Load (kN/m²)", 3.0, 8.0, 5.5, 0.5)
        default_q = 2.5 if domain=="Residential" else (4.0 if domain=="Commercial" else 7.5)
        q_k = st.slider("Imposed Load (kN/m²)", 1.5, 10.0, default_q, 0.5)
        steel = st.selectbox("Steel Section", ["UB 254x146x31","UB 305x165x40","UC 254x254x73","UC 305x305x97"]) if "Steel" in material else None
        seismic = st.selectbox("Seismic Zone", list(SEISMIC_ZONES.keys()), index=1)
        wind = st.selectbox("Wind Zone", list(WIND_ZONES.keys()), index=1)
    trigger = st.sidebar.button("⚡ Execute Generation", type="primary", use_container_width=True)
    if st.button("🚪 Logout"): logout()

# ------------------------------------------------------------
# MAIN INTERFACE
# ------------------------------------------------------------
if nav == "Control Hub":
    st.title("🌍 Regional Telemetry Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("KES", REGIONAL_FX["Kenya"]["rate_to_usd"]); col2.metric("UGX", REGIONAL_FX["Uganda"]["rate_to_usd"]); col3.metric("TZS", REGIONAL_FX["Tanzania"]["rate_to_usd"]); col4.metric("SSP", REGIONAL_FX["South Sudan"]["rate_to_usd"])
    st.markdown("---")
    my_designs = [d for d in st.session_state.memory["designs"] if d.get("username") == st.session_state.username]
    st.metric("My Archetypes", len(my_designs))
    if st.session_state.memory["logs"]:
        st.subheader("Recent Events")
        for e in reversed(st.session_state.memory["logs"][-5:]): st.caption(f"⏱️ {e['time'][-11:-3]} — {e['msg']} ({e.get('user','')})")

elif nav == "Synthesis Lab":
    st.title("📐 Generative Synthesis & Analysis")
    if trigger:
        with st.spinner("Synthesizing..."):
            design = generate_building_model(domain, btype, floors, baths, country, material, plot, soil, g_k, q_k, steel, seismic, wind, st.session_state.username)
            design = ensure_design_compatibility(design)
            st.session_state.active_design = design
            st.session_state.memory["designs"].append(design)
            log_event(f"Generated #{design['id']}"); save_memory(st.session_state.memory)

    if st.session_state.active_design:
        d = ensure_design_compatibility(st.session_state.active_design)
        if d.get("username") != st.session_state.username:
            st.warning("Design not owned by current user.")
        else:
            st.subheader(f"Active Design: {d['id']} — {d['type']}")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Region", d["country"]); col2.metric("GFA", f"{d['total_gfa']:,} m²"); col3.metric("Floors", d["floors"]); col4.metric("Doors/Windows", f"🚪{d['doors']} 🪟{d['windows']}")

            tabs = st.tabs(["2D Interactive","3D Isometric","Structural Passport","Zoning","BoQ & Forex","Forex Forecast","Drift Animation","Cost Sensitivity","Design Compare","Export IFC"])

            with tabs[0]:
                st.markdown("### Interactive 2D Blueprint")
                d = draw_interactive_blueprint(d); st.session_state.active_design = d; save_memory(st.session_state.memory)
            with tabs[1]: draw_3d_isometric_view(d)
            with tabs[2]: st.json(d["analysis"])
            with tabs[3]:
                zon = d["zoning"]
                st.write(f"Coverage: {zon['coverage']} (max {ARCH_DOMAINS[d['domain']]['max_coverage']}) — {'✅' if zon['coverage_ok'] else '❌'}")
                st.write(f"FAR: {zon['far']} (max {ARCH_DOMAINS[d['domain']]['max_far']}) — {'✅' if zon['far_ok'] else '❌'}")
                st.write(f"Overall: {zon['status']}")
            with tabs[4]:
                boq = d["boq"]; colA, colB = st.columns(2)
                with colA: st.metric("Substructure", f"${boq['substructure']:,.2f}"); st.metric("Superstructure", f"${boq['superstructure']:,.2f}"); st.metric("Finishes", f"${boq['finishes']:,.2f}")
                with colB: st.metric("Total USD", f"${boq['total_usd']:,.2f}"); st.metric(f"Total {boq['local_currency']}", f"{boq['symbol']} {boq['total_local']:,.2f}")
            with tabs[5]:
                st.subheader("📈 Forex Rate Forecast")
                cur = st.selectbox("Currency", list(REGIONAL_FX.keys()), key="forex_cur")
                horizon = st.radio("Horizon", ["short","medium","long"], horizontal=True, key="fx_hor")
                steps_map = {"short":7,"medium":30,"long":90}
                steps = st.slider("Days", 1, 90, steps_map[horizon])
                forecast, trend, chart = run_forecast(cur, horizon, steps)
                st.metric("Current", f"{REGIONAL_FX[cur]['symbol']} {REGIONAL_FX[cur]['rate_to_usd']}")
                st.metric(f"{steps}-day avg", f"{REGIONAL_FX[cur]['symbol']} {np.mean(forecast):.2f}")
                st.write(f"Trend: {trend.capitalize()}")
                fig, ax = plt.subplots(figsize=(8,4))
                ax.plot(chart["historical_dates"], chart["historical_values"], label="Historical", color="#38bdf8")
                ax.plot(chart["historical_dates"], chart["smoothed"], "--", color="orange", label="Smoothed")
                ax.plot(chart["forecast_dates"], chart["forecast_values"], "o-", color="red", label="Forecast")
                ax.legend(); ax.set_facecolor('#1e293b'); fig.patch.set_facecolor('#0f172a'); ax.tick_params(colors='white'); st.pyplot(fig)
            with tabs[6]:
                st.subheader("🌬️ Wind Drift Animation")
                drift_range = st.slider("Drift amplitude factor", 0.0, 1.0, 0.3, 0.05)
                draw_3d_isometric_view(d, drift_factor=drift_range)
                st.caption("Slide to simulate sway under wind load.")
            with tabs[7]:
                st.subheader("💰 Cost Sensitivity Analysis")
                st.write("Adjust base unit rates (USD/m²):")
                base_rates = {"Reinforced Concrete (Eurocode 2)":350,"Structural Steel Profile (Eurocode 3)":400,"Timber Profile (Eurocode 5)":280}
                new_rates = {}
                for mat, rate in base_rates.items():
                    new_rates[mat] = st.slider(mat, 200, 600, rate, 10)
                updated_boq = compute_detailed_forex_boq(d, rate_overrides=new_rates)
                colA, colB = st.columns(2)
                with colA: st.metric("Updated Total USD", f"${updated_boq['total_usd']:,.2f}")
                with colB: st.metric(f"Updated {updated_boq['local_currency']}", f"{updated_boq['symbol']} {updated_boq['total_local']:,.2f}")
            with tabs[8]:
                st.subheader("🆚 Design Comparison")
                my_designs_list = [d for d in st.session_state.memory["designs"] if d.get("username")==st.session_state.username]
                if len(my_designs_list) < 2: st.warning("Save at least two designs to compare.")
                else:
                    ids = [f"{d['id']} - {d['type']}" for d in my_designs_list]
                    d1_idx = st.selectbox("Design A", range(len(ids)), format_func=lambda x:ids[x])
                    d2_idx = st.selectbox("Design B", range(len(ids)), index=min(1,len(ids)-1), format_func=lambda x:ids[x])
                    if st.button("Compare"):
                        d1 = my_designs_list[d1_idx]; d2 = my_designs_list[d2_idx]
                        st.write("### Overlay Blueprint")
                        st.image(draw_2d_blueprint(d1, overlay_design=d2), use_column_width=True)
                        col1, col2 = st.columns(2)
                        with col1: st.metric("A GFA", d1["total_gfa"]); st.metric("A Cost USD", d1["boq"]["total_usd"]); st.metric("A Floors", d1["floors"])
                        with col2: st.metric("B GFA", d2["total_gfa"]); st.metric("B Cost USD", d2["boq"]["total_usd"]); st.metric("B Floors", d2["floors"])
            with tabs[9]:
                st.subheader("📦 Export to IFC/Revit JSON")
                ifc_json = generate_ifc_json(d)
                st.download_button("Download IFC-like JSON", data=json.dumps(ifc_json, indent=2), file_name=f"ARC_{d['id']}_ifc.json", mime="application/json")
                st.json(ifc_json, expanded=False)
    else:
        st.info("Configure parameters and press Execute Generation.")
