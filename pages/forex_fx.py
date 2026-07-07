# forex_fx.py (minimal version)

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
    "Kenya": {"currency": "KES", "symbol": "KSh", "multiplier": 1.00, "region": "East Africa"},
    "Uganda": {"currency": "UGX", "symbol": "USh", "multiplier": 0.95, "region": "East Africa"},
    "Tanzania": {"currency": "TZS", "symbol": "TSh", "multiplier": 0.98, "region": "East Africa"},
    "South Sudan": {"currency": "SSP", "symbol": "SSP", "multiplier": 1.35, "region": "East Africa"},
    "Rwanda": {"currency": "RWF", "symbol": "FRw", "multiplier": 0.85, "region": "Central Africa"},
    "Ethiopia": {"currency": "ETB", "symbol": "Br", "multiplier": 0.80, "region": "Horn of Africa"},
}

_CURRENT_RATES = {}
_BASELINE_RATES = {}
_CURRENCY_INFO = {}

def _fetch_live_rates():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        data = response.json()
        rates = data.get("rates", {})
        currency_map = {
            "Kenya": "KES", "Uganda": "UGX", "Tanzania": "TZS",
            "South Sudan": "SSP", "Rwanda": "RWF", "Ethiopia": "ETB",
        }
        live = {}
        for country, code in currency_map.items():
            if code in rates:
                live[country] = rates[code]
        return live if live else None
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

def get_fx_data(country):
    info = _CURRENCY_INFO[country].copy()
    info["rate"] = _CURRENT_RATES[country]
    return info

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
    rate = fx_data["rate"]
    mult = fx_data["multiplier"]
    conc = int(gfa * 0.35)
    steel = int(conc * 0.12)
    brick = int(gfa * 38)
    finish = int(gfa)
    items = [
        ("Earth Excavations", int(gfa * 0.15), 150),
        ("C30 Concrete", conc, 210),
        ("Steel B500B", steel, 1200),
        ("Blockwork", brick, 2.5),
        ("Floor Screed", finish, 40),
        ("Timber Doors", d["doors"], 300),
        ("Alu Windows", d["windows"], 450),
    ]
    usd = 0
    for _, qty, unit_rate in items:
        usd += qty * unit_rate * mult
    local = usd * rate
    return usd, local, fx_data

def simulate_random_fx(base_rate, volatility=0.02):
    return base_rate * (1 + random.gauss(0, volatility))

def get_baseline_rate(country):
    return _BASELINE_RATES[country]

def set_rate(country, new_rate):
    _CURRENT_RATES[country] = new_rate

def reset_rates_to_baseline():
    for country in _BASELINE_RATES:
        _CURRENT_RATES[country] = _BASELINE_RATES[country]
