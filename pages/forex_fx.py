# forex_fx.py – Full version with all functions

import random
import requests

STATIC_FX_RATES = {
    "Kenya": 129.49,
    "Uganda": 3665.20,
    "Tanzania": 2625.00,
    "South Sudan": 4626.40,
    "Rwanda": 1330.00,
    "Ethiopia": 125.00,
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
