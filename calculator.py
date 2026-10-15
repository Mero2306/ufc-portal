import streamlit as st

def mostra_calcolatore_semplice(ctx):
    st.markdown(f"<h1>{ctx.get('simple_calc_main_h1', '🧮 Simple Troops Calculator')}</h1>", unsafe_allow_html=True)
    st.write(ctx.get('simple_calc_main_subtitle', 'Select configuration and customize your active troops.'))
    
    livello_scelto = st.selectbox(ctx.get('calc_select_guard_level', 'Seleziona livello:'), ["G9", "G8"], key="sc_lvl_v300")
    max_leadership = st.number_input(ctx.get('calc_max_leadership_lbl', 'Max Leadership:'), min_value=0, value=332000, step=1000, key="sc_lead_v300")

    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops')}")
    
    filtri = {
        "G9": livello_scelto == "G9", "S9": livello_scelto == "G9", "C9": livello_scelto == "G9",
        "G8": livello_scelto in ["G9", "G8"], "S8": livello_scelto in ["G9", "G8"], "C8": livello_scelto in ["G9", "G8"]
    }

    # Configurazione rigida con gli stack esatti e i ratio del tuo foglio
    config_base = [
        {"t": "Flyer", "lead": 20, "st": 2, "r9": 0.50, "r8": 1.00, "has_spec": True, "has_eng": False},
        {"t": "Mounted", "lead": 2, "st": 2, "r9": 0.55, "r8": 1.00, "has_spec": True, "has_eng": False},
        {"t": "Ranged", "lead": 1, "st": 4, "r9": 0.55, "r8": 1.00, "has_spec": True, "has_eng": False},
        {"t": "Melee", "lead": 1, "st": 4, "r9": 0.55, "r8": 1.00, "has_spec": True, "has_eng": False},
        {"t": "Engineer Corps", "lead": 10, "st": 1, "r9": 0.57, "r8": 1.03, "has_spec": False, "has_eng": True}
    ]

    database_truppe = []
    for c in config_base:
        if not c["has_eng"]:
            database_truppe.append({"id": f"g9_{c['t'].lower()}", "name": f"L9 Guard {c['t']}", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r9"], "f_key": "G9", "cat": c["t"]})
            database_truppe.append({"id": f"g8_{c['t'].lower()}", "name": f"L8 Guard {c['t']}", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r8"], "f_key": "G8", "cat": c["t"]})
            if c["has_spec"]:
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
                nome_tradotto = ctx.get(truppa["name"], truppa["name"])
                attiva = st.checkbox(nome_tradotto, value=True, key=f"chk_f300_{truppa['id']}")
                stati_checkbox[truppa["id"]] = attiva
                if attiva and truppa["stacks"] > 0:
                    truppe_selezionate.append(truppa)
                    moltiplicatore_dinamico += (truppa["stacks"] * truppa["ratio"])
        st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    # Correzione del divisore per evitare che raddoppiando le righe i numeri crollino a un terzo
    # Il foglio originale di Maurizio ragiona sulla base di un set standard da 13.90
    moltiplicatore_calcolato = moltiplicatore_dinamico / 2.0 if moltiplicatore_dinamico > 0 else 0
    stack_reference = max_leadership / moltiplicatore_calcolato if moltiplicatore_calcolato > 0 else 0

    st.markdown(f"""<div class="chat-box" style="text-align: center; border-left: 6px solid #bd9b53 !important; background: #14120e !important; padding: 10px !important;">
        <h2 style="margin: 0; font-size: 13px; color: #bd9b53; font-family: 'Cinzel', serif;">{ctx.get('calc_auto_multiplier_lbl', 'CURRENT ACTIVE MULTIPLIER (B19)')}</h2>
        <p style="font-size: 26px; font-weight: bold; color: #f0e6d2; margin: 0; font-family: 'Cinzel', serif;">{moltiplicatore_calcolato:.2f}</p>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")
    risultati_finali_html = ""
    totale_leadership_usata = 0

    if stack_reference > 0:
        for t in database_truppe:
            if filtri[t["f_key"]] and stati_checkbox[t["id"]] and t["stacks"] > 0:
                # Applica la formula esatta di Maurizio per trovare il valore COMPLESSIVO per stack
                valore_interno = (t["ratio"] / t["lead_cost"] * stack_reference / 10) + 0.45
                count_truppe_per_stack = int(valore_interno) * 10
                
                # La leadership reale consumata dalla riga tiene conto del numero degli stack
                leadership_riga = count_truppe_per_stack * t["stacks"] * t["lead_cost"]
                totale_leadership_usata += leadership_riga

                count_formattato = f"{count_truppe_per_stack:,}".replace(",", ".")
                lead_riga_formattata = f"{leadership_riga:,}".replace(",", ".")

                if count_truppe_per_stack > 0:
                    risultati_finali_html += f"""<div class="chat-box" style="display:flex; justify-content:space-between; align-items:center; padding:10px 16px!important; margin-bottom:8px!important;">
                        <span style="color:#f0e6d2; font-weight:500;">{ctx.get(t["name"], t["name"])} <small style="color:#bd9b53;">({t['stacks']} Stacks)</small></span>
                        <div style="text-align:right;">
                            <span style="color:#bd9b53; font-weight:bold; font-size:18px; margin-right:15px;">{count_formattato} u. <small style="font-size:11px;color:#a69e8d;">/stack</small></span>
                            <span style="color:#a69e8d; font-size:13px;">(Lead riga: {lead_riga_formattata})</span>
                        </div>
                    </div>"""
        
        lead_usata_txt = f"{totale_leadership_usata:,}".replace(",", ".")
        lead_max_txt = f"{max_leadership:,}".replace(",", ".")
        rimanente = max_leadership - totale_leadership_usata
        rimanente_txt = f"{rimanente:,}".replace(",", ".")
        
        col_res1, col_res2 = st.columns(2)
        col_res1.markdown(f'<div class="chat-box" style="text-align:center;"><h3>Allocated</h3><p style="font-size:24px;color:#4a86e8;font-weight:bold;margin:0;">{lead_usata_txt} / {lead_max_txt}</p></div>', unsafe_allow_html=True)
        col_res2.markdown(f'<div class="chat-box" style="text-align:center;"><h3>Remaining</h3><p style="font-size:24px;color:{"#38761d" if rimanente >= 0 else "#990000"};font-weight:bold;margin:0;">{rimanente_txt}</p></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(risultati_finali_html, unsafe_allow_html=True)
    else:
        st.info("Nessuna truppa selezionata.")
