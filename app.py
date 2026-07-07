import streamlit as st

st.set_page_config(page_title="Arc Studio", page_icon="📐", layout="wide")

st.title("🌍 Arc Operating System")
st.markdown("### Integrated Intelligence & Structural Synthesis")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Sai Engine")
    st.info("Architectural synthesis, Eurocode compliance, and zoning.")
    if st.button("Access Sai Lab"):
        st.switch_page("pages/01_Sai_Engine.py")

with col2:
    st.subheader("Random Engine")
    st.info("East African Forex intelligence and BoQ estimation.")
    if st.button("Access Random Lab"):
        st.switch_page("pages/02_Random_FX.py")
