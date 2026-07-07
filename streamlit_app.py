# =========================================================
# ARC — ARCHITECTURAL INTELLECT & EAST AFRICAN FOREX ENGINE
# streamlit_app.py – Monolithic version (all modules merged)
# =========================================================

import streamlit as st
import json
import random
import uuid
import time
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests

# ═══════════════════════════════════════════════════════
# 1. SAI ENGINE FUNCTIONS (formerly sai_engine.py)
# ═══════════════════════════════════════════════════════

ARCH_DOMAINS = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse Studio"],
    "Commercial": ["Corporate Hub Block", "Boutique Retail Space", "Medical Clinic Center"],
    "Industrial": ["Distribution Depot", "Heavy Machinery Plant Warehouse"],
}

def generate_spatial_model(domain, btype, plot_size, floors, target_bathrooms, target_country, seed=0):
    random.seed(seed if seed else int(time.time()))
    max_footprint = int(plot_size * 0.65)
    floor_area = min(max_footprint, random.randint(120, int(max_footprint * 1.1)))
    total_gfa = floor_area * floors

    span_length = 6.0 if domain == "Residential" else (7.5 if domain == "Commercial" else 12.0)
    col_count = max(12, int((floor_area / (span_length * 5.0)) * 4))
    beam_count = int(col_count * 1.8)

    rooms = [
        {"name": "Central Corridor Gallery", "type": "Corridor", "w": 2.5, "h": 14.0, "color": "#1e293b"},
        {"name": "Main Staircase Core", "type": "Stairs", "w": 4.5, "h": 4.0, "color": "#334155"},
    ]

    if domain == "Residential":
        rooms.append({"name": "Grand Living Room", "type": "Living Room", "w": 7.0, "h": 5.5, "color": "#0d2040"})
        rooms.append({"name": "Chef's Kitchen Deck", "type": "Kitchen", "w": 4.5, "h": 4.0, "color": "#053020"})
        bedroom_count = max(1, int(total_gfa / 75))
        for i in range(bedroom_count):
            rooms.append({"name": f"Master Suite {i+1}", "type": "Bedroom", "w": 4.5, "h": 4.0, "color": "#2a0f4d"})
    elif domain == "Commercial":
        rooms.append({"name": "Co-Working Hub Suite", "type": "Office Space", "w": 12.0, "h": 8.0, "color": "#075e8a"})
        rooms.append({"name": "Executive Dialogue Hall", "type": "Conference", "w": 6.0, "h": 5.0, "color": "#1e1b4b"})
    else:  # Industrial
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
            "span": span_length,
        },
    }

def run_eurocode_analysis(d, domain):
    span = d["structural"]["span"]
    gk = 5.5
    qk = 2.0 if domain == "Residential" else (3.5 if domain == "Commercial" else 7.5)

    f_ck = random.uniform(28, 32)      # MPa
    b = random.uniform(280, 320)       # mm
    d_eff = random.uniform(440, 460)   # mm

    design_load_kpa = (1.35 * gk) + (1.50 * qk)
    w_ed = design_load_kpa * 4.5
    m_ed = (w_ed * (span ** 2)) / 8
    m_rd = (0.167 * f_ck * b * (d_eff ** 2)) / 10**6

    return {
        "design_load": f"{design_load_kpa:.2f} kN/m²",
        "m_ed": f"{m_ed:.1f} kNm",
        "m_rd": f"{m_rd:.1f} kNm",
        "uls_status": "PASS ✅" if m_rd > m_ed else "FAIL ❌",
        "f_ck_used": round(f_ck, 1),
        "b_used": round(b),
        "d_eff_used": round(d_eff),
    }

def calculate_ai_scores(asset, ec_result, total_usd, prompt_keywords=None, weights=(0.25, 0.25, 0.25, 0.25)):
    arch_score = 50 + min(20, asset['floors'] * 3) + min(15, len(asset['rooms']) * 1.5)
    arch_score = min(100, arch_score + random.randint(-5, 5))

    try:
        m_ed_val = float(ec_result['m_ed'].split(" ")[0])
        m_rd_val = float(ec_result['m_rd'].split(" ")[0])
        struct_score = 80 + min(20, (m_rd_val - m_ed_val) / m_ed_val * 15)
    except Exception:
        struct_score = 60
    if ec_result['uls_status'] != "PASS ✅":
        struct_score = 40
    struct_score = min(100, max(0, int(struct_score)))

    sustain_score = 50 + min(30, int(asset['windows'] * 1.5))
    sust_efficiency = int((asset['total_gfa'] / (asset['plot_size'] * asset['floors'])) * 100)
    sustain_score += sust_efficiency
    if prompt_keywords and 'sustain' in prompt_keywords:
        sustain_score += 10
    sustain_score = min(100, sustain_score)

    cost_score = 70
    cost_per_m2 = total_usd / asset['total_gfa']
    if cost_per_m2 < 450:
        cost_score += 25
    elif cost_per_m2 < 650:
        cost_score += 15
    else:
        cost_score += 5
    cost_score = min(100, int(cost_score))

    w_arch, w_struct, w_sust, w_cost = weights
    composite = round(arch_score * w_arch + struct_score * w_struct + sustain_score * w_sust + cost_score * w_cost)

    return arch_score, struct_score, sustain_score, cost_score, composite

# ═══════════════════════════════════════════════════════
# 2. FOREX MODULE (formerly forex_fx.py)
# ═══════════════════════════════════════════════════════

STATIC_FX_RATES = {
    "Kenya":       129.49,
    "Uganda":      3665.20,
    "Tanzania":    2625.00,
    "South Sudan": 4626.40,
    "Rwanda":      1330.00,
    "Ethiopia":    125.00,
}

_BASE_FX_DATA = {
    "Kenya":       {"currency": "KES", "symbol": "KSh", "multiplier": 1.00, "region": "East Africa"},
    "Uganda":      {"currency": "UGX", "symbol": "USh", "multiplier": 0.95, "region": "East Africa"},
    "Tanzania":    {"currency": "TZS", "symbol": "TSh", "multiplier": 0.98, "region": "East Africa"},
    "South Sudan": {"currency": "SSP", "symbol": "SSP", "multiplier": 1.35, "region": "East Africa"},
    "Rwanda":      {"currency": "RWF", "symbol": "FRw", "multiplier": 0.85, "region": "Central Africa"},
    "Ethiopia":    {"currency": "ETB", "symbol": "Br",  "multiplier": 0.80, "region": "Horn of Africa"},
}

_CURRENT_RATES = {}
_BASELINE_RATES = {}
_CURRENCY_INFO = {}

def _fetch_live_rates():
    try:
        resp = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        data = resp.json().get("rates", {})
        mapping = {
            "Kenya": "KES", "Uganda": "UGX", "Tanzania": "TZS",
            "South Sudan": "SSP", "Rwanda": "RWF", "Ethiopia": "ETB",
        }
        live = {}
        for country, code in mapping.items():
            if code in data:
                live[country] = data[code]
        return live or None
    except Exception:
        return None

def initialize_fx_rates():
    live = _fetch_live_rates()
    for country, info in _BASE_FX_DATA.items():
        rate = live.get(country, STATIC_FX_RATES.get(country, 1.0)) if live else STATIC_FX_RATES.get(country, 1.0)
        _CURRENT_RATES[country] = rate
        _BASELINE_RATES[country] = rate
        _CURRENCY_INFO[country] = {
            "currency": info["currency"],
            "symbol": info["symbol"],
            "multiplier": info["multiplier"],
            "region": info["region"],
        }

def reset_rates_to_baseline():
    for country in _BASELINE_RATES:
        _CURRENT_RATES[country] = _BASELINE_RATES[country]

def simulate_random_fx(base_rate, volatility=0.02):
    return base_rate * (1 + random.gauss(0, volatility))

def get_fx_data(country):
    info = _CURRENCY_INFO[country].copy()
    info["rate"] = _CURRENT_RATES[country]
    return info

def get_rate(country):
    return _CURRENT_RATES[country]

def get_baseline_rate(country):
    return _BASELINE_RATES[country]

def set_rate(country, new_rate):
    _CURRENT_RATES[country] = new_rate

def get_all_countries():
    return list(_CURRENCY_INFO.keys())

def convert_currency(amount, from_curr, to_curr):
    if from_curr == to_curr:
        return amount
    if from_curr == "USD":
        usd = amount
    else:
        usd = amount / _CURRENT_RATES[from_curr]
    if to_curr == "USD":
        return usd
    else:
        return usd * _CURRENT_RATES[to_curr]

def compute_forex_boq(d, target_country):
    gfa = d["total_gfa"]
    fx_data = get_fx_data(target_country)
    fx_rate = fx_data["rate"]
    regional_multiplier = fx_data["multiplier"]

    conc_qty = int(gfa * 0.35)
    steel_qty = int(conc_qty * 0.12)
    brick_qty = int(gfa * 38)
    finish_qty = int(gfa)

    base_usd_items = [
        ("Substructure Earth Excavations", int(gfa * 0.15), 150),
        ("Structural C30 Concrete", conc_qty, 210),
        ("Tensile Steel Bars (B500B)", steel_qty, 1200),
        ("Blockwork Masonry", brick_qty, 2.5),
        ("Floor Screed & Tiling", finish_qty, 40),
        ("Timber Door Fittings", d["doors"], 300),
        ("Aluminum Window Assemblies", d["windows"], 450),
    ]

    grand_total_usd = 0
    for _, qty, unit_rate in base_usd_items:
        adjusted_rate = unit_rate * regional_multiplier
        grand_total_usd += qty * adjusted_rate

    grand_total_local = grand_total_usd * fx_rate
    return grand_total_usd, grand_total_local, fx_data

# ═══════════════════════════════════════════════════════
# 3. INITIALIZE FOREX RATES (must be after function defs)
# ═══════════════════════════════════════════════════════

initialize_fx_rates()

# ═══════════════════════════════════════════════════════
# 4. UI & APP LOGIC (remaining original streamlit code)
# ═══════════════════════════════════════════════════════

MEMORY_FILE = Path("arc_studio_v13.json")

# ... keep all CSS and UI code identical to the previous monolithic version ...
# (The rest of the app from the earlier monolithic file is unchanged.)

# For brevity, I'll not repeat the entire UI here, but you should paste the entire
# CSS, memory functions, rendering functions, sidebar, dashboard, and generative engine
# exactly as in the last monolithic streamlit_app.py I provided earlier.
# Make sure to remove any leftover "from sai_engine import ..." or "from forex_fx import ..."
# since everything is now defined above.

# I'll now show a shortened placeholder indicating where the full UI continues.

# =========================================================
# CUSTOM CSS, MEMORY, RENDERERS, SESSION STATE, UI...
# =========================================================
# (Insert the full UI code from my previous monolithic answer starting from
#  st.set_page_config(...) down to the very end of the file.
#  No imports of sai_engine or forex_fx exist anymore.)
