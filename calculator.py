import streamlit as st

def mostra_calcolatore_semplice(ctx):
    st.markdown(
        f"<h1>{ctx.get('simple_calc_main_h1', '🧮 Simple Troops Calculator')}</h1>",
        unsafe_allow_html=True,
    )
    st.write(ctx.get('simple_calc_main_subtitle', 'Select your guard level configuration and customize your active troops.'))
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- SELEZIONE LIVELLO DELLE GUARDIE ---
    livello_scelto = st.selectbox(
        ctx.get('calc_select_guard_level', 'Seleziona il livello delle guardie:'),
        ["G9", "G8"],
        key="sc_guard_level_selector_final_v30"
    )

    # --- INPUT LEADERSHIP MASSIMA ---
    max_leadership = st.number_input(
        ctx.get('calc_max_leadership_lbl', 'Maximum Leadership:'),
        min_value=0, value=332000, step=1000, key="sc_max_lead"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops to Include in March')}")

    # --- FILTRI IN BASE ALLA SELEZIONE ---
    filtri_fogli = {
        "Guardie 9": livello_scelto == "G9",
        "Specialisti 9": livello_scelto == "G9",
        "Catapulte 9": livello_scelto == "G9",
        "Guardie 8": livello_scelto in ["G9", "G8"],
        "Specialisti 8": livello_scelto in ["G9", "G8"],
        "Catapulte 8": livello_scelto in ["G9", "G8"]
    }

    # --- DATABASE CON I SOLI COEFFICIENTI FISSI DI MAURIZIO ---
    database_truppe = [
        # --- TIER 9 ---
        {"id": "g9_flyer", "name": "L9 Guard Flyer (Corax)", "lead_cost": 20, "stacks": 2, "ratio": 0.50, "filter_key": "Guardie 9", "cat": "Flyer"},
        {"id": "s9_flyer", "name": "L9 Spec Flyer (Griffin/Lion)", "lead_cost": 20, "stacks": 2, "ratio": 0.50, "filter_key": "Specialisti 9", "cat": "Flyer"},
        
        {"id": "g9_mounted", "name": "L9 Guard Mounted (Cavalli)", "lead_cost": 2, "stacks": 2, "ratio": 0.55, "filter_key": "Guardie 9", "cat": "Mounted"},
        {"id": "s9_mounted", "name": "L9 Spec Mounted", "lead_cost": 2, "stacks": 2, "ratio": 0.55, "filter_key": "Specialisti 9", "cat": "Mounted"},
        
        {"id": "g9_ranged", "name": "L9 Guard Ranged (Arco)", "lead_cost": 1, "stacks": 4, "ratio": 0.55, "filter_key": "Guardie 9", "cat": "Ranged"},
        {"id": "s9_ranged", "name": "L9 Spec Ranged", "lead_cost": 1, "stacks": 4, "ratio": 0.55, "filter_key": "Specialisti 9", "cat": "Ranged"},
        
        {"id": "g9_melee", "name": "L9 Guard Melee (Mischia)", "lead_cost": 1, "stacks": 4, "ratio": 0.55, "filter_key": "Guardie 9", "cat": "Melee"},
        {"id": "s9_melee", "name": "L9 Spec Melee", "lead_cost": 1, "stacks": 4, "ratio": 0.55, "filter_key": "Specialisti 9", "cat": "Melee"},
        
        {"id": "c9_engineer", "name": "C9 Engineer Corps", "lead_cost": 10, "stacks": 1, "ratio": 0.57, "filter_key": "Catapulte 9", "cat": "Engineer Corps"},

        # --- TIER 8 ---
        {"id": "g8_flyer", "name": "L8 Guard Flyer (Corax)", "lead_cost": 20, "stacks": 2, "ratio": 1.00, "filter_key": "Guardie 8", "cat": "Flyer"},
        {"id": "s8_flyer", "name": "L8 Spec Flyer", "lead_cost": 20, "stacks": 2, "ratio": 1.00, "filter_key": "Specialisti 8", "cat": "Flyer"},
        
        {"id": "g8_mounted", "name": "L8 Guard Mounted (Cavalli)", "lead_cost": 2, "stacks": 2, "ratio": 1.00, "filter_key": "Guardie 8", "cat": "Mounted"},
        {"id": "s8_mounted", "name": "L8 Spec Mounted", "lead_cost": 2, "stacks": 2, "ratio": 1.00, "filter_key": "Specialisti 8", "cat": "Mounted"},
        
        {"id": "g8_ranged", "name": "L8 Guard Ranged (Arco)", "lead_cost": 1, "stacks": 4, "ratio": 1.00, "filter_key": "Guardie 8", "cat": "Ranged"},
        {"id": "s8_ranged", "name": "L8 Spec Ranged", "lead_cost": 1, "stacks": 4, "ratio": 1.00, "filter_key": "Specialisti 8", "cat": "Ranged"},
        
        {"id": "g8_melee", "name": "L8 Guard Melee (Mischia)", "lead_cost": 1, "stacks": 4, "ratio": 1.00, "filter_key": "Guardie 8", "cat": "Melee"},
        {"id": "s8_melee", "name": "L8 Spec Melee", "lead_cost": 1, "stacks": 4, "ratio": 1.00, "filter_key": "Specialisti 8", "cat": "Melee"},
        
        {"id": "c8_engineer", "name": "C8 Engineer Corps", "lead_cost": 10, "stacks": 1, "ratio": 1.03, "filter_key": "Catapulte 8", "cat": "Engineer Corps"}
    ]

    truppe_selezionate = []
    categorie = ["Flyer", "Mounted", "Ranged", "Melee", "Engineer Corps"]
    
    # Generazione dei Checkbox visivi
    for cat in categorie:
        st.markdown(f"**{cat}**")
        cols = st.columns(2)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat and filtri_fogli[t["filter_key"]]]
        
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 2]:
                nome_tradotto = ctx.get(truppa["name"], truppa["name"])
                
                attiva = st.checkbox(nome_tradotto, value=True, key=f"chk_final_v30_{truppa['id']}")
                if attiva:
                    truppe_selezionate.append(truppa)
                    
        st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")

    risultati_finali_html = ""
    totale_leadership_usata = 0

    # IL VALORE CARDINE DI MAURIZIO LEGATO ALLA LEADERSHIP: 
    # Rapporto proporzionale lineare puro basato sul setup standard a quota 13.9
    stack_reference = max_leadership / 13.90

    if truppe_selezionate:
        for truppa in truppe_selezionate:
            # APPLICAZIONE DIRETTA DELLA FORMULA SULLA LEADERSHIP DELLA TRUPPA (lead_cost)
            valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_reference / 10) + 0.45
            count_truppe_totale_riga = int(valore_interno) * 10
            
            # La leadership reale consumata dalla truppa
            leadership_riga = count_truppe_totale_riga * truppa["lead_cost"]
            totale_leadership_usata += leadership_riga

            count_formattato = f"{count_truppe_totale_riga:,}".replace(",", ".")
            lead_riga_formattata = f"{leadership_riga:,}".replace(",", ".")
            nome_tradotto_riga = ctx.get(truppa["name"], truppa["name"])

            if count_truppe_totale_riga > 0:
                risultati_finali_html += f"""
                <div class="chat-box" style="display:flex; justify-content:space-between; align-items:center; padding:10px 16px!important; margin-bottom:8px!important;">
                    <span style="color:#f0e6d2; font-weight:500;">{nome_tradotto_riga}</span>
                    <div style="text-align:right;">
                        <span style="color:#bd9b53; font-weight:bold; font-size:18px; margin-right:15px;">{count_formattato} u.</span>
                        <span style="color:#a69e8d; font-size:13px;">(Lead riga: {lead_riga_formattata})</span>
                    </div>
                </div>
                """
        
        # Box riassuntivi finali trasparenti e reali
        lead_usata_formattata = f"{totale_leadership_usata:,}".replace(",", ".")
        lead_max_formattata = f"{max_leadership:,}".replace(",", ".")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown(f'<div class="chat-box" style="text-align:center;"><h3>{ctx.get("calc_total_used_lead_lbl", "Total Leadership Allocated")}</h3><p style="font-size:24px;color:#4a86e8;font-weight:bold;margin:0;">{lead_usata_formattata} / {lead_max_formattata}</p></div>', unsafe_allow_html=True)
        with col_res2:
            rimanente = max_leadership - totale_leadership_usata
            rimanente_formattata = f"{rimanente:,}".replace(",", ".")
            colore_rimanente = "#38761d" if rimanente >= 0 else "#990000"
            st.markdown(f'<div class="chat-box" style="text-align:center;"><h3>{ctx.get("calc_remaining_lead_lbl", "Remaining Leadership")}</h3><p style="font-size:24px;color:{colore_rimanente};font-weight:bold;margin:0;">{rimanente_formattata}</p></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(risultati_finali_html, unsafe_allow_html=True)
