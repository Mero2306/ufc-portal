import streamlit as st

def mostra_calcolatore_semplice(ctx):
    st.markdown(f"<h1>{ctx.get('simple_calc_main_h1', '🧮 Tactical Army Stack Calculator')}</h1>", unsafe_allow_html=True)
    st.write(ctx.get('simple_calc_main_subtitle', 'Configure march settings and customize active troops.'))
    
    c1, c2 = st.columns(2)
    livello_scelto = c1.selectbox(ctx.get('calc_select_guard_level', 'Seleziona livello:'), ["G9", "G8"], key="sc_lvl_v5")
    max_leadership = c2.number_input(ctx.get('calc_max_leadership_lbl', 'Max Leadership:'), min_value=0, value=332000, step=1000, key="sc_lead_v5")

    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops')}")
    filtri = {"G9": livello_scelto == "G9", "S9": livello_scelto == "G9", "C9": livello_scelto == "G9", "G8": True, "S8": True, "C8": True}

    # Database iper-compresso (Genera dinamicamente le 18 righe Guardie + Specialisti + Genieri)
    config_base = [
        {"t": "Flyer", "lead": 20, "st": 2, "r9": 0.50, "r8": 1.00, "sp": True, "eng": False},
        {"t": "Mounted", "lead": 2, "st": 2, "r9": 0.55, "r8": 1.00, "sp": True, "eng": False},
        {"t": "Ranged", "lead": 1, "st": 4, "r9": 0.55, "r8": 1.00, "sp": True, "eng": False},
        {"t": "Melee", "lead": 1, "st": 4, "r9": 0.55, "r8": 1.00, "sp": True, "eng": False},
        {"t": "Engineer Corps", "lead": 10, "st": 1, "r9": 0.57, "r8": 1.03, "sp": False, "eng": True}
    ]

    database_truppe = []
    for c in config_base:
        if not c["eng"]:
            database_truppe.append({"id": f"g9_{c['t'].lower()}", "name": f"L9 Guard {c['t']}", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r9"], "f_key": "G9", "cat": c["t"]})
            database_truppe.append({"id": f"g8_{c['t'].lower()}", "name": f"L8 Guard {c['t']}", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r8"], "f_key": "G8", "cat": c["t"]})
            if c["sp"]:
                database_truppe.append({"id": f"s9_{c['t'].lower()}", "name": f"L9 Spec {c['t']}", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r9"], "f_key": "S9", "cat": c["t"]})
                database_truppe.append({"id": f"s8_{c['t'].lower()}", "name": f"L8 Spec {c['t']}", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r8"], "f_key": "S8", "cat": c["t"]})
        else:
            database_truppe.append({"id": "c9_eng", "name": "C9 Engineer Corps", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r9"], "f_key": "C9", "cat": c["t"]})
            database_truppe.append({"id": "c8_eng", "name": "C8 Engineer Corps", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r8"], "f_key": "C8", "cat": c["t"]})

    truppe_selezionate = []
    stati_checkbox = {}
    moltiplicatore_dinamico = 0.0

    for cat in ["Flyer", "Mounted", "Ranged", "Melee", "Engineer Corps"]:
        st.markdown(f"**{cat}**")
        cols = st.columns(2)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat and filtri[t["f_key"]]]
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 2]:
                attiva = st.checkbox(ctx.get(truppa["name"], truppa["name"]), value=True, key=f"chk_f_{truppa['id']}")
                stati_checkbox[truppa["id"]] = attiva
                if attiva and truppa["stacks"] > 0:
                    truppe_selezionate.append(truppa)
                    moltiplicatore_dinamico += (truppa["stacks"] * truppa["ratio"])
        st.markdown("<hr style='margin: 4px 0; opacity: 0.05;'>", unsafe_allow_html=True)

    stack_reference = max_leadership / moltiplicatore_dinamico if moltiplicatore_dinamico > 0 else 0

    st.markdown(f"""<div class="chat-box" style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; padding: 12px !important; border-left: 6px solid #bd9b53 !important; background: linear-gradient(145deg, #1c1810, #0f0d0a) !important; margin-bottom: 20px !important;">
        <div><span style="font-size: 11px; color: #bd9b53; font-weight: bold;">MULTIPLIER (B19)</span><p style="font-size: 22px; font-weight: bold; color: #f0e6d2; margin: 0;">{moltiplicatore_dinamico:.2f}</p></div>
        <div><span style="font-size: 11px; color: #bd9b53; font-weight: bold;">STACK REF # (J19)</span><p style="font-size: 22px; font-weight: bold; color: #bd9b53; margin: 0;">{stack_reference:,.2f}</p></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")
    risultati_finali_html = ""
    totale_leadership_usata = 0

    if stack_reference > 0:
        for t in database_truppe:
            if filtri[t["f_key"]] and stati_checkbox[t["id"]] and t["stacks"] > 0:
                valore_interno = (t["ratio"] / t["lead_cost"] * stack_reference / 10) + 0.45
                count_truppe_per_stack = int(valore_interno) * 10
                leadership_riga = count_truppe_per_stack * t["stacks"] * t["lead_cost"]
                totale_leadership_usata += leadership_riga

                b_color = "#bd9b53" if "L9" in t["name"] or "C9" in t["name"] else "#4a86e8"
                b_lbl = "Tier 9" if "L9" in t["name"] or "C9" in t["name"] else "Tier 8"

                if count_truppe_per_stack > 0:
                    risultati_finali_html += f"""<div class="chat-box" style="display:flex; justify-content:space-between; align-items:center; padding:10px 15px!important; margin-bottom:8px!important; border-right: 4px solid {b_color} !important; background: rgba(255,255,255,0.02);">
                        <div><span style="color:#f0e6d2; font-weight:600; font-size:14px;">{ctx.get(t["name"], t["name"])}</span><br><small style="color:{b_color}; font-size:10px; font-weight:bold;">{b_lbl} • {t['stacks']} Stacks</small></div>
                        <div style="text-align:right;"><span style="color:#f0e6d2; font-weight:bold; font-size:18px; margin-right:5px;">{count_truppe_per_stack:,}</span><span style="color:#bd9b53; font-size:12px;">u.</span><br><small style="color:#a69e8d; font-size:11px;">Lead riga: {leadership_riga:,}</small></div>
                    </div>"""
        
        rimanente = max_leadership - totale_leadership_usata
        c_rim = "#38761d" if rimanente >= 0 else "#990000"
        
        col_res1, col_res2 = st.columns(2)
        col_res1.markdown(f'<div class="chat-box" style="text-align:center; padding:8px!important;"><h3>Allocated</h3><p style="font-size:20px;color:#4a86e8;font-weight:bold;margin:0;">{totale_leadership_usata:,} / {max_leadership:,}</p></div>', unsafe_allow_html=True)
        col_res2.markdown(f'<div class="chat-box" style="text-align:center; padding:8px!important;"><h3>Remaining</h3><p style="font-size:20px;color:{c_rim};font-weight:bold;margin:0;">{rimanente:,}</p></div>', unsafe_allow_html=True)
        st.markdown("<br>" + risultati_finali_html, unsafe_allow_html=True)
    else:
        st.info("Nessuna formazione selezionata.")
