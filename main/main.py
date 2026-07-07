# In main.py
from llm_engine import parse_architectural_prompt

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_concepts(request: GenerateRequest):
    # 1. AI BRAIN: Parse the prompt first
    ai_config = await parse_architectural_prompt(
        request.prompt, 
        fallback_domain=request.domain, 
        fallback_type=request.type
    )
    
    # 2. Use AI config values, falling back to User sidebar inputs if needed
    final_domain = ai_config["domain"]
    final_type = ai_config["type"]
    final_plot = ai_config["plot_size"]
    final_floors = ai_config["floors"]
    final_baths = ai_config["bathrooms"]
    
    if request.country not in REGIONAL_FX:
        raise HTTPException(status_code=400, detail="Country not supported in FX Engine")

    concept_names = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
    generated_concepts = []

    for i in range(5):
        # Mutate inputs for every concept
        mut_plot = final_plot + random.randint(-150, 150)
        mut_floors = max(1, final_floors + random.randint(-1, 1))
        mut_rooms = max(1, final_baths + random.randint(-1, 1))
        
        raw_asset = generate_spatial_model(
            final_domain, final_type, 
            mut_plot, mut_floors, mut_rooms, 
            request.country, seed=i
        )
        
        ec_result = run_eurocode_analysis(raw_asset, raw_asset['domain'])
        total_usd, total_local, fx_meta = compute_forex_boq(raw_asset, raw_asset['country'])
        
        arch, struct, sust, cost = calculate_ai_scores(raw_asset, ec_result, total_usd, request.prompt)
        
        response_obj = ConceptOutput(
            id=raw_asset["id"],
            name=concept_names[i],
            domain=raw_asset["domain"],
            type=raw_asset["type"],
            total_gfa=raw_asset["total_gfa"],
            floors=raw_asset["floors"],
            country=raw_asset["country"],
            scores=ConceptScore(
                architectural=arch, 
                structural=struct, 
                sustainability=sust, 
                cost=cost
            ),
            boq_usd_total=int(total_usd),
            boq_local_total=int(total_local),
            currency_symbol=fx_meta['symbol']
        )
        generated_concepts.append(response_obj)

    return {"status": "success", "concepts": generated_concepts}

# =========================================================
# ARC API — ARCHITECTURAL INTELLECT & EAST AFRICAN FOREX ENGINE
# Full FastAPI Implementation for React Frontend Integration
# =========================================================

import uuid
import random
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# =========================================================
# 1. SETUP & CONFIGURATION
# =========================================================
app = FastAPI(title="RANDOM V3 API", description="Sai Engine & FX Architecture Studio")

# Allow ANY frontend (React/Next.js) to connect to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your React app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# 2. REGIONAL FOREX DATA ENGINE (EAST AFRICA 2026)
# =========================================================
REGIONAL_FX = {
    "Kenya":       {"currency": "KES", "rate": 129.49, "symbol": "KSh", "multiplier": 1.00, "region": "East Africa"},
    "Uganda":      {"currency": "UGX", "rate": 3665.20, "symbol": "USh", "multiplier": 0.95, "region": "East Africa"},
    "Tanzania":    {"currency": "TZS", "rate": 2625.00, "symbol": "TSh", "multiplier": 0.98, "region": "East Africa"},
    "South Sudan": {"currency": "SSP", "rate": 4626.40, "symbol": "SSP", "multiplier": 1.35, "region": "East Africa"},
    "Rwanda":      {"currency": "RWF", "rate": 1330.00, "symbol": "FRw", "multiplier": 0.85, "region": "Central Africa"},
    "Ethiopia":    {"currency": "ETB", "rate": 125.00, "symbol": "Br",  "multiplier": 0.80, "region": "Horn of Africa"}
}

ARCH_DOMAINS = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse Studio"],
    "Commercial": ["Corporate Hub Block", "Boutique Retail Space", "Medical Clinic Center"],
    "Industrial": ["Distribution Depot", "Heavy Machinery Plant Warehouse"]
}

# =========================================================
# 3. PYDANTIC DATA MODELS (API INPUT / OUTPUT)
# =========================================================

class GenerateRequest(BaseModel):
    country: str
    domain: str
    type: str
    plot_size: int
    floors: int
    bathrooms: int
    prompt: Optional[str] = ""

class BQOItem(BaseModel):
    description: str
    quantity: str
    rate_local: str
    total_local: str

class ConceptScore(BaseModel):
    architectural: int
    structural: int
    sustainability: int
    cost: int

class ConceptOutput(BaseModel):
    id: str
    name: str
    domain: str
    type: str
    total_gfa: int
    floors: int
    country: str
    scores: ConceptScore
    boq_usd_total: int
    boq_local_total: int
    currency_symbol: str
    # We don't return the full rooms array to the React frontend to keep JSON small. 
    # Frontend will request 2D/3D separately or use IDs for real-time 3D rendering.

class GenerateResponse(BaseModel):
    status: str
    concepts: List[ConceptOutput]

# =========================================================
# 4. CORE ARCHITECTURAL ENGINE LOGIC
# =========================================================

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
        {"name": "Main Staircase Core", "type": "Stairs", "w": 4.5, "h": 4.0, "color": "#334155"}
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
    else: # Industrial
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
            "span": span_length
        }
    }

def run_eurocode_analysis(d, domain):
    span = d["structural"]["span"]
    gk = 5.5  
    qk = 2.0 if domain == "Residential" else (3.5 if domain == "Commercial" else 7.5)
    design_load_kpa = (1.35 * gk) + (1.50 * qk)
    w_ed = design_load_kpa * 4.5  
    m_ed = (w_ed * (span ** 2)) / 8
    b = 300; d_eff = 450; f_ck = 30  
    m_rd = (0.167 * f_ck * b * (d_eff ** 2)) / 10**6

    return {
        "m_ed_val": m_ed,
        "m_rd_val": m_rd,
        "uls_status": "PASS" if m_rd > m_ed else "FAIL"
    }

def compute_forex_boq(d, target_country):
    gfa = d["total_gfa"]
    fx_meta = REGIONAL_FX[target_country]
    fx_rate = fx_meta["rate"]
    regional_multiplier = fx_meta["multiplier"]

    conc_qty = int(gfa * 0.35); steel_qty = int(conc_qty * 0.12)
    brick_qty = int(gfa * 38); finish_qty = int(gfa)

    base_usd_items = [
        {"Item": "Substructure Excavations", "Qty": int(gfa*0.15), "Unit": "m³", "Rate": 150},
        {"Item": "Structural C30 Concrete", "Qty": conc_qty, "Unit": "m³", "Rate": 210},
        {"Item": "Tensile Steel Bars (B500B)", "Qty": steel_qty, "Unit": "Tons", "Rate": 1200},
        {"Item": "Blockwork Masonry", "Qty": brick_qty, "Unit": "Pcs", "Rate": 2.5},
        {"Item": "Floor Screed & Tiling", "Qty": finish_qty, "Unit": "m²", "Rate": 40},
        {"Item": "Timber Door Fittings", "Qty": d["doors"], "Unit": "Sets", "Rate": 300},
        {"Item": "Aluminum Window Assemblies", "Qty": d["windows"], "Unit": "Sets", "Rate": 450}
    ]
    grand_total_usd = 0
    for item in base_usd_items:
        adjusted_rate = item["Rate"] * regional_multiplier
        grand_total_usd += item["Qty"] * adjusted_rate
    grand_total_local = grand_total_usd * fx_rate
    return grand_total_usd, grand_total_local, fx_meta

def calculate_ai_scores(asset, ec_result, total_usd, prompt):
    # Architect AI
    arch_score = 50 + min(20, asset['floors'] * 3) + min(15, len(asset['rooms']) * 1.5)
    arch_score = min(100, arch_score + random.randint(-5, 5))

    # Structural AI
    if ec_result['uls_status'] == "PASS":
        struct_score = 80 + min(20, int((ec_result['m_rd_val'] - ec_result['m_ed_val']) / ec_result['m_ed_val'] * 15))
    else: 
        struct_score = 40
    struct_score = min(100, max(0, int(struct_score)))

    # Sustainability AI
    sustain_score = 50 + min(30, int(asset['windows'] * 1.5))
    sust_efficiency = int((asset['total_gfa'] / (asset['plot_size'] * asset['floors'])) * 100)
    sustain_score += sust_efficiency
    if prompt and 'sustain' in prompt.lower(): 
        sustain_score += 10
    sustain_score = min(100, sustain_score)

    # Cost AI
    cost_score = 70
    cost_per_m2 = total_usd / asset['total_gfa']
    if cost_per_m2 < 450: cost_score += 25
    elif cost_per_m2 < 650: cost_score += 15
    else: cost_score += 5
    cost_score = min(100, int(cost_score))

    return arch_score, struct_score, sustain_score, cost_score

# =========================================================
# 5. FASTAPI ENDPOINT
# =========================================================

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_concepts(request: GenerateRequest):
    if request.country not in REGIONAL_FX:
        raise HTTPException(status_code=400, detail="Country not supported in FX Engine")
    if request.domain not in ARCH_DOMAINS:
        raise HTTPException(status_code=400, detail="Invalid architectural domain")

    concept_names = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
    generated_concepts = []

    for i in range(5):
        # Mutate inputs slightly for every concept to create 5 unique variations
        mut_plot = request.plot_size + random.randint(-150, 150)
        mut_floors = max(1, request.floors + random.randint(-1, 1))
        mut_rooms = max(1, request.bathrooms + random.randint(-1, 1))

        # Generate the raw spatial model
        raw_asset = generate_spatial_model(
            request.domain, request.type, 
            mut_plot, mut_floors, mut_rooms, 
            request.country, seed=i
        )

        # Analyze & Calculate BoQs
        ec_result = run_eurocode_analysis(raw_asset, raw_asset['domain'])
        total_usd, total_local, fx_meta = compute_forex_boq(raw_asset, raw_asset['country'])

        # Sai Engine Scores
        arch, struct, sust, cost = calculate_ai_scores(raw_asset, ec_result, total_usd, request.prompt)

        # Construct API Response Object
        response_obj = ConceptOutput(
            id=raw_asset["id"],
            name=concept_names[i],
            domain=raw_asset["domain"],
            type=raw_asset["type"],
            total_gfa=raw_asset["total_gfa"],
            floors=raw_asset["floors"],
            country=raw_asset["country"],
            scores=ConceptScore(
                architectural=arch, 
                structural=struct, 
                sustainability=sust, 
                cost=cost
            ),
            boq_usd_total=int(total_usd),
            boq_local_total=int(total_local),
            currency_symbol=fx_meta['symbol']
        )
        generated_concepts.append(response_obj)

    return {"status": "success", "concepts": generated_concepts}

# Add this Pydantic model at the top of main.py
class PromptInterpretRequest(BaseModel):
    prompt: str

@app.post("/api/interpret")
async def interpret_prompt(request: PromptInterpretRequest):
    # Call your AI parsing function (the one we wrote earlier)
    ai_config = await parse_architectural_prompt(
        request.prompt,
        fallback_domain="Residential", 
        fallback_type="Modern Villa"
    )
    return ai_config