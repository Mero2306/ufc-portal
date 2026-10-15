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
        key="sc_guard_level_selector_final_v8"
    )

    # --- INPUT LEADERSHIP MASSIMA ---
    max_leadership = st.number_input(
        ctx.get('calc_max_leadership_lbl', 'Maximum Leadership:'),
        min_value=0, value=332000, step=1000, key="sc_max_lead"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops to Include in March')}")

    # --- CONFIGURAZIONE ATTIVAZIONE LIVELLI IN BASE ALLA SELEZIONE ---
    filtri_attivi = {
        "L9": livello_scelto == "G9",
        "L8": livello_scelto in ["G9", "G8"],
        "C9": livello_scelto == "G9",
        "C8": livello_scelto in ["G9", "G8"]
    }

    # --- DATABASE AGGIORNATO CON GLI STACK REALI DEL FOGLIO ---
    # CORREZIONE: L9 Flyer (Corax) impostato rigidamente a 1 STACK invece di 2!
    database_truppe = [
        {"id": "l9_flyer", "name": "L9 Flyer (Corax)", "lead_cost": 20, "stacks": 1, "ratio": 0.50, "filter_key": "L9", "cat": "Flyer"},
        {"id": "l8_flyer", "name": "L8 Flyer (Corax)", "lead_cost": 20, "stacks": 2, "ratio": 1.00, "filter_key": "L8", "cat": "Flyer"},
        
        {"id": "l9_mounted", "name": "L9 Mounted", "lead_cost": 2, "stacks": 2, "ratio": 0.55, "filter_key": "L9", "cat": "Mounted"},
        {"id": "l8_mounted", "name": "L8 Mounted", "lead_cost": 2, "stacks": 2, "ratio": 1.00, "filter_key": "L8", "cat": "Mounted"},
        
        {"id": "l9_ranged", "name": "L9 Ranged", "lead_cost": 1, "stacks": 4, "ratio": 0.55, "filter_key": "L9", "cat": "Ranged"},
        {"id": "l8_ranged", "name": "L8 Ranged", "lead_cost": 1, "stacks": 4, "ratio": 1.00, "filter_key": "L8", "cat": "Ranged"},
        
        {"id": "l9_melee", "name": "L9 Melee", "lead_cost": 1, "stacks": 4, "ratio": 0.55, "filter_key": "L9", "cat": "Melee"},
        {"id": "l8_melee", "name": "L8 Melee", "lead_cost": 1, "stacks": 4, "ratio": 1.00, "filter_key": "L8", "cat": "Melee"},
        
        {"id": "c9_engineer", "name": "C9 Engineer Corps", "lead_cost": 10, "stacks": 1, "ratio": 0.57, "filter_key": "C9", "cat": "Engineer Corps"},
        {"id": "c8_engineer", "name": "C8 Engineer Corps", "lead_cost": 10, "stacks": 1, "ratio": 1.03, "filter_key": "C8", "cat": "Engineer Corps"}
    ]

    truppe_selezionate = []
    moltiplicatore_dinamico = 0.0
    categorie = ["Flyer", "Mounted", "Ranged", "Melee", "Engineer Corps"]
    
    # Interfaccia Checkbox Dinamica
    for cat in categorie:
        st.markdown(f"**{cat}**")
        cols = st.columns(3)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat and filtri_attivi[t["filter_key"]]]
        
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 3]:
                nome_tradotto = ctx.get(truppa["name"], truppa["name"])
                
                attiva = st.checkbox(nome_tradotto, value=True, key=f"chk_v25_{truppa['id']}")
                if attiva and truppa["stacks"] > 0:
                    truppe_selezionate.append(truppa)
                    contr_riga = truppa["stacks"] * truppa["ratio"]
                    moltiplicatore_dinamico += contr_riga
                    
        st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    # --- DISPLAY DEL MOLTIPLICATORE DINAMICO AUTOMATICO ---
    st.markdown(
        f"""
        <div class="chat-box" style="text-align: center; max-width: 500px; margin: 20px auto; border-left: 6px solid #bd9b53 !important; background: linear-gradient(145deg, #241f16, #14120e) !important; padding: 10px !important;">
            <h2 style="margin: 0 0 2px 0; font-size: 13px; color: #bd9b53; letter-spacing: 0.5px; font-family: 'Cinzel', serif;">
                {ctx.get('calc_auto_multiplier_lbl', 'AUTOMATIC MULTIPLIER')}
            </h2>
            <p style="font-size: 26px; font-weight: bold; color: #f0e6d2; margin: 0; font-family: 'Cinzel', serif;">
                {moltiplicatore_dinamico:.2f}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")

    risultati_finali_html = ""
    totale_leadership_usata = 0

    if moltiplicatore_dinamico > 0 and truppe_selezionate:
        stack_reference = max_leadership / moltiplicatore_dinamico

        for truppa in truppe_selezionate:
            # APPLICAZIONE DELLA TUA FORMULA CON ARROTONDAMENTO FISSO EXCEL
            valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_reference / 10) + 0.45
            count_truppe_per_stack = int(valore_interno) * 10
            
            leadership_riga = count_truppe_per_stack * truppa["stacks"] * truppa["lead_cost"]
            totale_leadership_usata += leadership_riga

            count_formattato = f"{count_truppe_per_stack:,}".replace(",", ".")
            lead_riga_formattata = f"{leadership_riga:,}".replace(",", ".")
            nome_tradotto_riga = ctx.get(truppa["name"], truppa["name"])

            if count_truppe_per_stack > 0:
                risultati_finali_html += f"""
                <div class="chat-box" style="display:flex; justify-content:space-between; align-items:center; padding:10px 16px!important; margin-bottom:8px!important;">
                    <span style="color:#f0e6d2; font-weight:500;">{nome_tradotto_riga} <small style="color:#bd9b53;">({truppa['stacks']} Stacks)</small></span>
                    <div style="text-align:right;">
                        <span style="color:#bd9b53; font-weight:bold; font-size:18px; margin-right:15px;">{count_formattato} u. <small style="font-size:11px;color:#a69e8d;">/stack</small></span>
                        <span style="color:#a69e8d; font-size:13px;">(Lead riga: {lead_riga_formattata})</span>
                    </div>
                </div>
                """
        
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
    else:
        st.info(ctx.get('calc_no_troops_allocated', 'Nessuna truppa selezionata.'))
