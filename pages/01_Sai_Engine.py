"""
Sai Engine — Architectural generation, structural analysis, and multi‑agent scoring.
No Streamlit or UI code here; pure logic and randomisation.
"""

import random
import uuid
import time

# ── Architectural typologies ────────────────────────
ARCH_DOMAINS = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse Studio"],
    "Commercial": ["Corporate Hub Block", "Boutique Retail Space", "Medical Clinic Center"],
    "Industrial": ["Distribution Depot", "Heavy Machinery Plant Warehouse"],
}


def generate_spatial_model(domain, btype, plot_size, floors, target_bathrooms, target_country, seed=0):
    """
    Create a random spatial plan (rooms, structural skeleton) for one concept.
    Returns a dictionary with all plan metadata.
    """
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
    """
    Simulate Eurocode 2 bending check with random material properties (Sai randomness).
    Returns a dict with design load, moments, and pass/fail status.
    """
    span = d["structural"]["span"]
    gk = 5.5
    qk = 2.0 if domain == "Residential" else (3.5 if domain == "Commercial" else 7.5)

    # Randomised concrete strength and beam dimensions
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
    """
    Multi‑agent scoring: Architecture, Structure, Sustainability, Cost.
    Returns individual scores and a weighted composite.
    """
    # Architecture
    arch_score = 50 + min(20, asset['floors'] * 3) + min(15, len(asset['rooms']) * 1.5)
    arch_score = min(100, arch_score + random.randint(-5, 5))

    # Structural
    try:
        m_ed_val = float(ec_result['m_ed'].split(" ")[0])
        m_rd_val = float(ec_result['m_rd'].split(" ")[0])
        struct_score = 80 + min(20, (m_rd_val - m_ed_val) / m_ed_val * 15)
    except Exception:
        struct_score = 60
    if ec_result['uls_status'] != "PASS ✅":
        struct_score = 40
    struct_score = min(100, max(0, int(struct_score)))

    # Sustainability
    sustain_score = 50 + min(30, int(asset['windows'] * 1.5))
    sust_efficiency = int((asset['total_gfa'] / (asset['plot_size'] * asset['floors'])) * 100)
    sustain_score += sust_efficiency
    if prompt_keywords and 'sustain' in prompt_keywords:
        sustain_score += 10
    sustain_score = min(100, sustain_score)

    # Cost
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
