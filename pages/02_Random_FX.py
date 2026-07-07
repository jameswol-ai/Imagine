"""
Forex Module – Live & static exchange rates, volatility simulator, currency converter,
and Bill of Quantities (BOQ) costing in local currency.
"""

import random
import requests

# ── Static fallback rates ───────────────────────────
STATIC_FX_RATES = {
    "Kenya":       129.49,
    "Uganda":      3665.20,
    "Tanzania":    2625.00,
    "South Sudan": 4626.40,
    "Rwanda":      1330.00,
    "Ethiopia":    125.00,
}

# ── Base country metadata ───────────────────────────
_BASE_FX_DATA = {
    "Kenya":       {"currency": "KES", "symbol": "KSh", "multiplier": 1.00, "region": "East Africa"},
    "Uganda":      {"currency": "UGX", "symbol": "USh", "multiplier": 0.95, "region": "East Africa"},
    "Tanzania":    {"currency": "TZS", "symbol": "TSh", "multiplier": 0.98, "region": "East Africa"},
    "South Sudan": {"currency": "SSP", "symbol": "SSP", "multiplier": 1.35, "region": "East Africa"},
    "Rwanda":      {"currency": "RWF", "symbol": "FRw", "multiplier": 0.85, "region": "Central Africa"},
    "Ethiopia":    {"currency": "ETB", "symbol": "Br",  "multiplier": 0.80, "region": "Horn of Africa"},
}

# Module‑level storage (initialized by initialize_fx_rates())
_CURRENT_RATES = {}       # {country: rate}
_BASELINE_RATES = {}
_CURRENCY_INFO = {}


def _fetch_live_rates():
    """Try to fetch live rates from ExchangeRate-API (free tier)."""
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        data = response.json()
        rates = data.get("rates", {})
        currency_map = {
            "Kenya": "KES",
            "Uganda": "UGX",
            "Tanzania": "TZS",
            "South Sudan": "SSP",
            "Rwanda": "RWF",
            "Ethiopia": "ETB",
        }
        live = {}
        for country, code in currency_map.items():
            if code in rates:
                live[country] = rates[code]
        return live if live else None
    except Exception:
        return None


def initialize_fx_rates():
    """
    Build the global rate table, preferring live API data with static fallback.
    Call once at startup.
    """
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
    """Restore the original (live or static) rates, e.g. after a volatility simulation."""
    for country in _BASELINE_RATES:
        _CURRENT_RATES[country] = _BASELINE_RATES[country]


def simulate_random_fx(base_rate, volatility=0.02):
    """Apply Gaussian noise to a rate (used for stress testing)."""
    return base_rate * (1 + random.gauss(0, volatility))


def get_fx_data(country):
    """
    Return a dict with current rate, currency, symbol, multiplier, region.
    """
    info = _CURRENCY_INFO[country].copy()
    info["rate"] = _CURRENT_RATES[country]
    return info


def get_rate(country):
    return _CURRENT_RATES[country]


def set_rate(country, new_rate):
    _CURRENT_RATES[country] = new_rate


def get_all_countries():
    return list(_CURRENCY_INFO.keys())


def convert_currency(amount, from_curr, to_curr):
    """Convert amount between any two currencies (including USD)."""
    if from_curr == to_curr:
        return amount

    # Pivot through USD
    if from_curr == "USD":
        usd_value = amount
    else:
        usd_value = amount / _CURRENT_RATES[from_curr]

    if to_curr == "USD":
        return usd_value
    else:
        return usd_value * _CURRENT_RATES[to_curr]


def compute_forex_boq(d, target_country):
    """
    Generate a Bill of Quantities in USD and local currency.
    Uses the country’s cost multiplier and current FX rate.
    """
    gfa = d["total_gfa"]
    fx_data = get_fx_data(target_country)
    fx_rate = fx_data["rate"]
    regional_multiplier = fx_data["multiplier"]

    conc_qty = int(gfa * 0.35)
    steel_qty = int(conc_qty * 0.12)
    brick_qty = int(gfa * 38)
    finish_qty = int(gfa)

    base_usd_items = [
        {"Item": "Substructure Earth Excavations", "Qty": int(gfa * 0.15), "Unit": "m³", "Rate": 150},
        {"Item": "Structural C30 Concrete", "Qty": conc_qty, "Unit": "m³", "Rate": 210},
        {"Item": "Tensile Steel Bars (B500B)", "Qty": steel_qty, "Unit": "Tons", "Rate": 1200},
        {"Item": "Blockwork Masonry", "Qty": brick_qty, "Unit": "Pcs", "Rate": 2.5},
        {"Item": "Floor Screed & Tiling", "Qty": finish_qty, "Unit": "m²", "Rate": 40},
        {"Item": "Timber Door Fittings", "Qty": d["doors"], "Unit": "Sets", "Rate": 300},
        {"Item": "Aluminum Window Assemblies", "Qty": d["windows"], "Unit": "Sets", "Rate": 450},
    ]

    grand_total_usd = 0
    for item in base_usd_items:
        adjusted_rate = item["Rate"] * regional_multiplier
        grand_total_usd += item["Qty"] * adjusted_rate

    grand_total_local = grand_total_usd * fx_rate
    return grand_total_usd, grand_total_local, fx_data
