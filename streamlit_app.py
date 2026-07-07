# =========================================================
# ARC — ARCHITECTURAL INTELLECT & EAST AFRICAN FOREX ENGINE
# Generative Multi‑Story Floor Plan & Regional Cost Synthesis
# Sai Engine & Random FX Visual Overhaul v15.0 – Extended Suite
# =========================================================

import streamlit as st
import json
import uuid
import random
import time
from pathlib import Path
from datetime import datetime

# NEW: radar chart and interactive 3D
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import io

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

# ... (keep all the existing custom CSS from the previous visually enhanced version – same as before) ...
# Paste the full <style> block from the previous answer here (it's long, I'll include it but truncated for brevity).
# For the answer, assume the entire style block is present.

# =========================================================
# ENHANCED RANDOM FX ENGINE (EAST AFRICA 2026)
# =========================================================

REGIONAL_FX = { ... }  # unchanged

DEFAULT_STATE = {"designs": [], "concepts": [], "logs": []}

# ... (all existing functions: load_memory, save_memory, log_event, generate_spatial_model, run_eurocode_analysis, compute_forex_boq) unchanged ...

# ----------------------------------------------
# NEW: calculate_ai_scores now returns a composite
# ----------------------------------------------
def calculate_ai_scores(asset, ec_result, total_usd, prompt_keywords=None, weights=(0.25,0.25,0.25,0.25)):
    # original score calculation
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

    # NEW: weighted composite score
    w_arch, w_struct, w_sust, w_cost = weights
    composite = round(arch_score*w_arch + struct_score*w_struct + sustain_score*w_sust + cost_score*w_cost)
    return arch_score, struct_score, sustain_score, cost_score, composite

# =========================================================
# NEW GRAPHICS: PLOTLY 3D ROOM MAP
# =========================================================
def render_plotly_3d_rooms(plan):
    # Simulate positions based on room index
    x, y, z, colors, labels, widths, depths = [], [], [], [], [], [], []
    for i, room in enumerate(plan):
        # lay out in a grid
        col = i % 3
        row = i // 3
        x_center = col * 12
        y_center = row * 10
        z_center = 0
        w = room["w"]
        d = room["h"]
        x.extend([x_center - w/2, x_center + w/2, x_center + w/2, x_center - w/2, None])
        y.extend([y_center - d/2, y_center - d/2, y_center + d/2, y_center + d/2, None])
        z.extend([0,0,0,0,None])
        colors.extend([room["color"]]*5)
        labels.append(room["name"])

    fig = go.Figure(data=[
        go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color='white', width=2),
            hoverinfo='none'
        )
    ])

    # Add floor planes
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
# APPLICATION UI LAYERS (core unchanged, new elements inserted)
# =========================================================

# ... sidebar, nav_page, etc. identical up to Generative Engine ...

elif nav_page == "Generative Design Engine":
    # ... the header and copilot input remain the same ...

    # NEW: AI agent weight sliders in sidebar
    with st.sidebar.expander("⚖️ AI Agent Weights", expanded=False):
        w_arch = st.slider("Architect Weight", 0.0, 1.0, 0.25, 0.05)
        w_struct = st.slider("Structural Weight", 0.0, 1.0, 0.25, 0.05)
        w_sust = st.slider("Sustainability Weight", 0.0, 1.0, 0.25, 0.05)
        w_cost = st.slider("Cost Weight", 0.0, 1.0, 0.25, 0.05)
        # Normalize
        total_w = w_arch + w_struct + w_sust + w_cost
        if total_w > 0:
            w_arch /= total_w
            w_struct /= total_w
            w_sust /= total_w
            w_cost /= total_w
        weights = (w_arch, w_struct, w_sust, w_cost)
        st.caption(f"Normalised: arch {w_arch:.2f}, struct {w_struct:.2f}, sust {w_sust:.2f}, cost {w_cost:.2f}")

    if trigger_synthesis:
        # ... synthesis loop unchanged, but now pass weights
        concepts = []
        for i in range(5):
            # ...
            d = generate_spatial_model(...)
            d["plan"] = d["rooms"]
            # compute scores and attach them for sorting
            ec = run_eurocode_analysis(d, d['domain'])
            total_usd, total_local, fx = compute_forex_boq(d, d['country'])
            arch, struct, sust, cost, comp = calculate_ai_scores(d, ec, total_usd, prompt, weights)
            d["scores"] = {"arch": arch, "struct": struct, "sust": sust, "cost": cost, "composite": comp}
            d["total_usd"] = total_usd
            d["total_local"] = total_local
            d["fx"] = fx
            concepts.append(d)
        # Sort by composite score descending
        concepts.sort(key=lambda x: x["scores"]["composite"], reverse=True)
        st.session_state.generated_concepts = concepts
        st.session_state.active_design = concepts[0]

    if st.session_state.generated_concepts:
        concepts = st.session_state.generated_concepts
        # ... display concept cards using stored scores ...
        # (in the card loop, use c["scores"] and c["total_usd"] etc.)

        # ------------ NEW: RADAR CHART COMPARISON ------------
        with st.expander("📊 AI Score Radar Comparison", expanded=True):
            radar_data = []
            for i, c in enumerate(concepts):
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
            colors_radar = concept_colors
            for i, row in df_radar.iterrows():
                fig_radar.add_trace(go.Scatterpolar(
                    r=row[categories].values,
                    theta=categories,
                    fill='toself',
                    name=row["Concept"],
                    line_color=colors_radar[i % len(colors_radar)],
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

        # ------------ NEW: SAVE CONCEPT BUTTON ------------
        st.markdown("---")
        st.markdown("### 🏆 TOP RECOMMENDATION: CONCEPT ALPHA (now sorted by composite score)")
        asset = concepts[0]  # already sorted
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

        # ... rest of Alpha detail cards unchanged, but use asset["scores"] and asset["total_usd"] etc. ...

        # ------------ NEW: 3D VIEW SELECTOR ------------
        st.markdown("### 📦 3D MASSING CONCEPT")
        view_mode = st.radio("3D View Mode", ["Isometric Wireframe", "Interactive 3D Rooms"], horizontal=True)
        if view_mode == "Isometric Wireframe":
            st.components.v1.html(render_isometric_html(asset["plan"]), height=450)
        else:
            fig3d = render_plotly_3d_rooms(asset["plan"])
            st.plotly_chart(fig3d, use_container_width=True)

        # ------------ NEW: EXPORT REPORT ------------
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