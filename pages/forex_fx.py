# forex_fx.py – minimal test

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
    # (same as before)
    pass

def initialize_fx_rates():
    # Very simple version
    for country, info in _BASE_FX_DATA.items():
        rate = STATIC_FX_RATES.get(country, 1.0)
        _CURRENT_RATES[country] = rate
        _BASELINE_RATES[country] = rate
        _CURRENCY_INFO[country] = info.copy()

# Add the other functions (get_fx_data, etc.) unchanged
