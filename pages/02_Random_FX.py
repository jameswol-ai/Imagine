import streamlit as st
import json
from pathlib import Path

# --- CONFIG & HELPERS ---
# Assuming you place the shared memory logic in a root folder for access
MEMORY_FILE = Path("arc_studio_v15.json")

def load_memory():
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"designs": []}

# --- PAGE UI ---
st.set_page_config(page_title="Random Engine", page_icon="📊", layout="wide")

st.title("📊 Random: Forex & Financial Intel")
st.markdown("Automated market data ingestion and regional BoQ cost estimation.")

# --- SECTION 1: MARKET INDICES ---
st.subheader("Regional Spot Indices")
fx_data = {
    "Kenya": {"currency": "KES", "rate": 129.49, "symbol": "KSh"},
    "Uganda": {"currency": "UGX", "rate": 3665.20, "symbol": "USh"},
    "Tanzania": {"currency": "TZS", "rate": 2625.00, "symbol": "TSh"},
    "South Sudan": {"currency": "SSP", "rate": 4626.40, "symbol": "SSP"}
}

cols = st.columns(4)
for i, (country, meta) in enumerate(fx_data.items()):
    cols[i].metric(f"USD / {meta['currency']}", f"{meta['symbol']} {meta['rate']:.2f}")

st.markdown("---")

# --- SECTION 2: BOQ ESTIMATION ---
st.subheader("Bill of Quantities (BoQ) Ledger")

memory = load_memory()
designs = memory.get("designs", [])

if not designs:
    st.info("No architectural designs found in the pipeline. Please generate a design in the Sai Lab first.")
else:
    selected_design_id = st.selectbox("Select Project to Cost", [d['id'] for d in designs])
    active_design = next((d for d in designs if d['id'] == selected_design_id), None)

    if active_design:
        # Import your calculation logic here or keep it in a shared utils file
        # items, total_usd, total_local, fx_meta = compute_detailed_forex_boq(active_design, active_design['country'])
        
        st.write(f"### Financial Summary for Instance {active_design['id']}")
        
        # Display cost data in a clean dataframe
        # st.table(items)
        
        st.metric("Total Project Cost (USD)", f"$ {10000:,.2f}") # Placeholder
        st.metric("Total Local Cost", f"{active_design['country']} Calculation")
        
        st.markdown("### Forward Rate Hedging")
        st.slider("Capital Lockup Duration", 3, 12, 3, help="Months")
        st.success("Hedging calculations active.")

# --- SIDEBAR NAV ---
st.sidebar.markdown("---")
if st.sidebar.button("Return to Hub"):
    st.switch_page("app.py")



# (Include your compute_detailed_forex_boq function here)

st.title("📊 Random: Forex & Financial Intel")

# Logic for market display and BoQ estimation
st.subheader("Regional Spot Indices")
# ... display FX metrics ...

st.markdown("---")
st.subheader("Bill of Quantities (BoQ) Estimator")
# ... inputs for BoQ and call compute_detailed_forex_boq ...
