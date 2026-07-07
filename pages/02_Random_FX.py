import streamlit as st
import json
import random
import requests
from pathlib import Path
from datetime import datetime
import plotly.express as px
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Random Engine", page_icon="📊", layout="wide")

# ---- CUSTOM GLASSMORPHISM & ANIMATIONS (identical to Sai Lab) ----
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
    .fx-badge {
        background: rgba(0,0,0,0.3);
        border-radius: 12px;
        padding: 10px 8px;
        text-align: center;
        border: 1px solid rgba(56,189,248,0.2);
        transition: 0.2s;
    }
    .fx-badge:hover {
        border-color: rgba(56,189,248,0.5);
        background: rgba(30,41,59,0.5);
    }
    .hedge-card {
        background: rgba(139,92,246,0.1);
        border-left: 4px solid #8b5cf6;
    }
</style>
""", unsafe_allow_html=True)

# ---- MEMORY ----
MEMORY_FILE = Path("arc_studio_v15.json")

def load_memory():
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"designs": []}

# ---- LIVE FX RATES (same as before) ----
STATIC_FX = {
    "Kenya": 129.49, "Uganda": 3665.20, "Tanzania": 2625.00,
    "South Sudan": 4626.40, "Rwanda": 1330.00, "Ethiopia": 125.00
}

def get_live_fx():
    try:
        resp = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        data = resp.json()["rates"]
        mapping = {
            "Kenya": "KES", "Uganda": "UGX", "Tanzania": "TZS",
            "South Sudan": "SSP", "Rwanda": "RWF", "Ethiopia": "ETB"
        }
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

# ---- BOQ COMPUTATION (same as Sai Engine) ----
def compute_detailed_forex_boq(design):
    gfa = design.get("gfa", design.get("total_gfa", 0))
    if not gfa:  # fallback if gfa missing
        gfa = design.get("floor_area", 100) * design.get("floors", 1)
    fx_meta = REGIONAL_FX[design["country"]]
    fx_rate = fx_meta["rate"]
    multiplier = fx_meta["multiplier"]

    conc_qty = int(gfa * 0.35)
    steel_qty = int(conc_qty * 0.12)
    brick_qty = int(gfa * 38)
    finish_qty = int(gfa)

    items = [
        {"Item": "Substructure Earth Excavations", "Qty": int(gfa*0.15), "Unit": "m³", "Rate (USD)": 150},
        {"Item": "Structural C30 Concrete", "Qty": conc_qty, "Unit": "m³", "Rate (USD)": 210},
        {"Item": "Tensile Steel Bars (B500B)", "Qty": steel_qty, "Unit": "Tons", "Rate (USD)": 1200},
        {"Item": "Blockwork Masonry", "Qty": brick_qty, "Unit": "Pcs", "Rate (USD)": 2.5},
        {"Item": "Floor Screed & Tiling", "Qty": finish_qty, "Unit": "m²", "Rate (USD)": 40},
        {"Item": "Timber Door Fittings", "Qty": len(design.get("rooms", []))+design.get("floors",1)*2, "Unit": "Sets", "Rate (USD)": 300},
        {"Item": "Aluminum Window Assemblies", "Qty": max(4, int(gfa/16)), "Unit": "Sets", "Rate (USD)": 450}
    ]

    total_usd = sum(item["Qty"] * item["Rate (USD)"] * multiplier for item in items)
    total_local = total_usd * fx_rate
    return items, total_usd, total_local, fx_meta

# ---- SESSION ----
memory = load_memory()
designs = memory.get("designs", [])

# ---- UI ----
st.markdown("""
<div class="glass-panel" style="text-align:center; margin-bottom:24px;">
    <h1 style="font-size:2.5rem; margin-bottom:4px;">📊 Random Engine</h1>
    <div style="color:#94a3b8;">Forex & Financial Intel – Live Market Data & BoQ Estimation</div>
</div>
""", unsafe_allow_html=True)

tab_market, tab_boq, tab_portfolio = st.tabs(["📈 Market Indices", "💰 BoQ Estimator", "📋 Project Portfolio"])

# ==================== MARKET INDICES ====================
with tab_market:
    st.subheader("Regional Spot Indices")
    cols = st.columns(6)
    for i, (country, meta) in enumerate(REGIONAL_FX.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="fx-badge">
                <div style="font-size:0.85rem; color:#94a3b8;">{meta['currency']}</div>
                <div style="font-size:1.4rem; font-weight:700;">{meta['symbol']} {meta['rate']:,.2f}</div>
                <div style="font-size:0.7rem; color:#22c55e;">{country}</div>
                <div style="font-size:0.65rem; color:#64748b;">Multiplier: {meta['multiplier']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    # Forex trend chart (simulated)
    st.subheader("📉 30-Day USD/KES Simulated Trend")
    # Generate mock historical data
    dates = pd.date_range(end=datetime.today(), periods=30).to_list()
    base_rate = REGIONAL_FX["Kenya"]["rate"]
    simulated = [base_rate + random.uniform(-2, 2) for _ in range(30)]
    df = pd.DataFrame({"Date": dates, "Rate": simulated})
    fig = px.line(df, x="Date", y="Rate", template="plotly_dark")
    fig.update_traces(line_color="#38bdf8")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

# ==================== BOQ ESTIMATOR ====================
with tab_boq:
    st.subheader("Bill of Quantities (BoQ) Ledger")
    if not designs:
        st.info("No architectural designs found in the pipeline. Generate a design in the Sai Lab first.")
    else:
        design_ids = [d["id"] for d in designs]
        selected_id = st.selectbox("Select Project", design_ids,
                                    format_func=lambda x: f"{x} – {next(d['type'] for d in designs if d['id']==x)}")
        active = next(d for d in designs if d["id"] == selected_id)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Project ID", active["id"])
            st.metric("Type", active["type"])
        with col2:
            st.metric("Country", active["country"])
            st.metric("GFA (m²)", active.get("gfa", active.get("total_gfa", 0)))
        with col3:
            fx_info = REGIONAL_FX[active["country"]]
            st.metric("Local Currency", f"{fx_info['symbol']} ({fx_info['currency']})")
            st.metric("FX Rate", f"{fx_info['rate']:,.2f}")

        items, total_usd, total_local, fx_meta = compute_detailed_forex_boq(active)

        # Detailed BOQ table
        st.markdown("#### Quantity Breakdown")
        df_items = pd.DataFrame(items)
        df_items["Total (USD)"] = df_items["Qty"] * df_items["Rate (USD)"] * fx_meta["multiplier"]
        df_items = df_items.round(2)
        st.dataframe(df_items, use_container_width=True, hide_index=True)

        # Totals
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="glass-panel" style="border-left:4px solid #38bdf8;">
                <div style="color:#38bdf8; font-weight:600;">🇺🇸 USD Total</div>
                <div style="font-size:2rem; font-weight:700;">${total_usd:,.2f}</div>
                <div style="color:#94a3b8;">Regional multiplier: {fx_meta['multiplier']}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="glass-panel" style="border-left:4px solid #facc15;">
                <div style="color:#facc15; font-weight:600;">{fx_meta['currency']} Local</div>
                <div style="font-size:2rem; font-weight:700;">{fx_meta['symbol']} {total_local:,.2f}</div>
                <div style="color:#94a3b8;">Rate: {fx_meta['rate']:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        # Forward Rate Hedging
        st.markdown("---")
        st.markdown("### 📈 Forward Rate Hedging")
        col_h1, col_h2 = st.columns([1, 2])
        with col_h1:
            months = st.slider("Capital Lockup Duration (months)", 3, 12, 6)
        with col_h2:
            # Simple hedge calculation
            hedge_rate = fx_meta["rate"] * (1 + random.uniform(-0.02, 0.04))  # simulated forward premium
            hedged_cost = total_usd * hedge_rate
            st.markdown(f"""
            <div class="glass-panel hedge-card">
                <div style="color:#8b5cf6; font-weight:600;">🔒 Forward Hedge Estimate</div>
                <div style="font-size:1.2rem;">Locked-in rate for {months} months: <b>{hedge_rate:,.2f}</b></div>
                <div style="margin-top:10px;">Estimated local cost if hedged: <b>{fx_meta['symbol']} {hedged_cost:,.2f}</b></div>
                <div style="color:#94a3b8; font-size:0.8rem; margin-top:5px;">Hedge savings vs. spot: {fx_meta['symbol']} {abs(total_local - hedged_cost):,.2f}</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== PROJECT PORTFOLIO ====================
with tab_portfolio:
    st.subheader("📋 Project Portfolio Overview")
    if not designs:
        st.info("No projects yet.")
    else:
        # Aggregate cost data for all designs
        rows = []
        for d in designs:
            _, usd, local, fx = compute_detailed_forex_boq(d)
            rows.append({
                "ID": d["id"],
                "Type": d["type"],
                "Country": d["country"],
                "GFA (m²)": d.get("gfa", d.get("total_gfa", 0)),
                "USD Total": round(usd, 2),
                "Local Total": round(local, 2),
                "FX Rate": fx["rate"]
            })
        df_all = pd.DataFrame(rows)

        # Summary metrics
        total_usd_all = df_all["USD Total"].sum()
        st.markdown(f"**Total Portfolio Value:** ${total_usd_all:,.2f} USD")
        st.dataframe(df_all, use_container_width=True, hide_index=True)

        # Bar chart by country
        st.markdown("### 💹 Cost Comparison by Country")
        fig_bar = px.bar(df_all, x="Country", y="USD Total", color="Type", 
                         barmode="group", template="plotly_dark", 
                         title="Project Costs (USD)")
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("""
    <div style="font-size:1.8rem; font-weight:700; font-family:'Space Grotesk';">
        <span style="color:#8b5cf6;">RANDOM</span> FX
    </div>
    <div style="color:#94a3b8; margin-bottom:20px;">Market Intelligence</div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.caption("All rates update on page load (free API, 24h cache).")
    st.caption("Forward hedge is simulated – not financial advice.")
    st.markdown("---")
    if st.button("🏠 Return to Hub"):
        st.switch_page("app.py")