import streamlit as st

def mostra_calcolatore_semplice(ctx):
    st.markdown(f"<h1>{ctx.get('simple_calc_main_h1', '🧮 Tactical Army Stack Calculator')}</h1>", unsafe_allow_html=True)
    st.write(ctx.get('simple_calc_main_subtitle', 'Configure march settings and customize active troops.'))
    
    c1, c2 = st.columns(2)
    livello_scelto = c1.selectbox(ctx.get('calc_select_guard_level', 'Seleziona livello:'), ["G9", "G8"], key="sc_lvl_v7")
    max_leadership = c2.number_input(ctx.get('calc_max_leadership_lbl', 'Max Leadership:'), min_value=0, value=332000, step=1000, key="sc_lead_v7")

    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops')}")
    filtri = {"G9": livello_scelto == "G9", "S9": livello_scelto == "G9", "C9": livello_scelto == "G9", "G8": True, "S8": True, "C8": True}

    # Struttura dati nativa immutata dal foglio di Maurizio
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
            database_truppe.append({"id": f"g9_{c['t'].lower()}", "name": f"L9 Guard {c['t']}", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r9"], "f_key": "G9", "cat": c["t"], "grp": "G9"})
            database_truppe.append({"id": f"g8_{c['t'].lower()}", "name": f"L8 Guard {c['t']}", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r8"], "f_key": "G8", "cat": c["t"], "grp": "G8"})
            if c["sp"]:
                database_truppe.append({"id": f"s9_{c['t'].lower()}", "name": f"L9 Spec {c['t']}", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r9"], "f_key": "S9", "cat": c["t"], "grp": "S9"})
                database_truppe.append({"id": f"s8_{c['t'].lower()}", "name": f"L8 Spec {c['t']}", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r8"], "f_key": "S8", "cat": c["t"], "grp": "S8"})
        else:
            database_truppe.append({"id": "c9_eng", "name": "C9 Engineer Corps", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r9"], "f_key": "C9", "cat": c["t"], "grp": "ENG"})
            database_truppe.append({"id": "c8_eng", "name": "C8 Engineer Corps", "lead_cost": c["lead"], "stacks": c["st"], "ratio": c["r8"], "f_key": "C8", "cat": c["t"], "grp": "ENG"}
    ]

    stati_checkbox = {}
    for cat in ["Flyer", "Mounted", "Ranged", "Melee", "Engineer Corps"]:
        st.markdown(f"**{cat}**")
        cols = st.columns(2)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat and filtri[t["f_key"]]]
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 2]:
                attiva = st.checkbox(ctx.get(truppa["name"], truppa["name"]), value=True, key=f"chk_f7_{truppa['id']}")
                stati_checkbox[truppa["id"]] = attiva
        st.markdown("<hr style='margin: 4px 0; opacity: 0.05;'>", unsafe_allow_html=True)

    # --- ALGORITMO DI PROTEZIONE DEL BILANCIAMENTO A SQUADRE ---
    # Calcoliamo il moltiplicatore bloccando la sovrapposizione simultanea di Guardie e Specialisti
    moltiplicatore_dinamico = 0.0
    for t in database_truppe:
        if filtri[t["f_key"]] and stati_checkbox[t["id"]]:
            # Sottraiamo il doppione simmetrico se sia Guard che Spec dello stesso Tier sono accesi insieme
            is_spec_duplicate = t["grp"] in ["S9", "S8"] and stati_checkbox.get(t["id"].replace("s9_", "g9_").replace("s8_", "g8_"), False)
            if not is_spec_duplicate:
                moltiplicatore_dinamico += (t["stacks"] * t["ratio"])

    stack_reference = max_leadership / moltiplicatore_dinamico if moltiplicatore_dinamico > 0 else 0

    st.markdown(f"""<div class="chat-box" style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; padding: 12px !important; border-left: 6px solid #bd9b53 !important; background: linear-gradient(145deg, #1c1810, #0f0d0a) !important; margin-bottom: 20px !important;">
        <div><span style="font-size: 11px; color: #bd9b53; font-weight: bold;">MULTIPLIER (B19)</span><p style="font-size: 22px; font-weight: bold; color: #f0e6d2; margin: 0;">{moltiplicatore_dinamico:.2f}</p></div>
        <div><span style="font-size: 11px; color: #bd9b53; font-weight: bold;">STACK REF # (J19)</span><p style="font-size: 22px; font-weight: bold; color: #bd9b53; margin: 0;">{stack_reference:,.2f}</p></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")
    
    totale_leadership_usata = 0
    gruppi_html = {"G9": "", "S9": "", "G8": "", "S8": "", "ENG": ""}
    
    meta_gruppi = {
        "G9": {"title": "🛡️ GUARDIE LIVELLO 9", "color": "#bd9b53"},
        "S9": {"title": "⚡ SPECIALISTI LIVELLO 9", "color": "#cc4125"},
        "G8": {"title": "⚔️ GUARDIE LIVELLO 8", "color": "#4a86e8"},
        "S8": {"title": "🔮 SPECIALISTI LIVELLO 8", "color": "#8e7cc3"},
        "ENG": {"title": "📐 ENGINEER CORPS (CATAPULTE)", "color": "#b45f06"}
    }

    if stack_reference > 0:
        for t in database_truppe:
            if filtri[t["f_key"]] and stati_checkbox[t["id"]] and t["stacks"] > 0:
                valore_interno = (t["ratio"] / t["lead_cost"] * stack_reference / 10) + 0.45
                count_truppe = int(valore_interno) * 10
                leadership_riga = count_truppe * t["stacks"] * t["lead_cost"]
                totale_leadership_usata += leadership_riga

                if count_truppe > 0:
                    short_name = t["name"].replace("L9 ", "").replace("L8 ", "").replace("C9 ", "").replace("C8 ", "")
                    gruppi_html[t["grp"]] += f"""
                    <div style="flex: 1; min-width: 140px; text-align: center; padding: 8px; background: rgba(0,0,0,0.3); border-radius: 4px; border: 1px solid rgba(255,255,255,0.03); margin: 4px;">
                        <span style="font-size: 11px; color: #a69e8d; display: block; font-weight: 500;">{ctx.get(short_name, short_name)}</span>
                        <b style="font-size: 16px; color: #f0e6d2; display: block; margin: 2px 0;">{count_truppe:,} <span style="font-size:10px; color:#bd9b53; font-weight:normal;">u.</span></b>
                        <span style="font-size: 10px; color: #666;">Lead riga: {leadership_riga:,}</span>
                    </div>
                    """

        output_corpo_html = ""
        for g_key, g_meta in meta_gruppi.items():
            if gruppi_html[g_key].strip() != "":
                output_corpo_html += f"""
                <div style="padding: 12px; margin-bottom: 12px; border-left: 4px solid {g_meta['color']}; background: rgba(255,255,255,0.015); border-radius: 0 6px 6px 0;">
                    <div style="font-size: 12px; color: {g_meta['color']}; font-weight: bold; letter-spacing: 0.8px; margin-bottom: 8px;">{g_meta['title']}</div>
                    <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                        {gruppi_html[g_key]}
                    </div>
                </div>
                """

        rimanente = max_leadership - totale_leadership_usata
        c_rim = "#38761d" if rimanente >= 0 else "#990000"
        
        col_res1, col_res2 = st.columns(2)
        col_res1.markdown(f'<div class="chat-box" style="text-align:center; padding:8px!important;"><h3>Allocated</h3><p style="font-size:20px;color:#4a86e8;font-weight:bold;margin:0;">{totale_leadership_usata:,} / {max_leadership:,}</p></div>', unsafe_allow_html=True)
        col_res2.markdown(f'<div class="chat-box" style="text-align:center; padding:8px!important;"><h3>Remaining</h3><p style="font-size:20px;color:{c_rim};font-weight:bold;margin:0;">{rimanente:,}</p></div>', unsafe_allow_html=True)
        st.markdown("<br>" + output_corpo_html, unsafe_allow_html=True)
    else:
        st.info("Nessuna formazione selezionata.")
