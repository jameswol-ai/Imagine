def run_eurocode_analysis(d, domain):
    span = d["structural"]["span"]
    gk = 5.5  
    qk = 2.0 if domain == "Residential" else (3.5 if domain == "Commercial" else 7.5)
    
    # --- Sai randomness: vary material strength and dimensions slightly ---
    # Concrete characteristic strength: nominal 30 MPa, ± 2 MPa
    f_ck = random.uniform(28, 32)  
    # Beam width: nominal 300 mm, ± 20 mm
    b = random.uniform(280, 320)  
    # Effective depth: nominal 450 mm, ± 10 mm
    d_eff = random.uniform(440, 460)
    
    design_load_kpa = (1.35 * gk) + (1.50 * qk)
    w_ed = design_load_kpa * 4.5  
    m_ed = (w_ed * (span ** 2)) / 8
    m_rd = (0.167 * f_ck * b * (d_eff ** 2)) / 10**6
    
    return {
        "design_load": f"{design_load_kpa:.2f} kN/m²",
        "m_ed": f"{m_ed:.1f} kNm",
        "m_rd": f"{m_rd:.1f} kNm",
        "uls_status": "PASS ✅" if m_rd > m_ed else "FAIL ❌",
        # Optionally expose the random parameters for transparency
        "f_ck_used": round(f_ck, 1),
        "b_used": round(b),
        "d_eff_used": round(d_eff)
    }