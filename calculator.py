import streamlit as st

def mostra_calcolatore_semplice(ctx):
    st.markdown(
        f"<h1>{ctx.get('simple_calc_main_h1', '🧮 Simple Troops Calculator')}</h1>",
        unsafe_allow_html=True,
    )
    st.write(ctx.get('simple_calc_main_subtitle', 'Select your guard level configuration and customize your active troops.'))
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- 1. SELEZIONE LIVELLO MASSIMO (Cella B2 del tuo foglio) ---
    livello_scelto = st.selectbox(
        ctx.get('calc_select_guard_level', 'Seleziona il livello delle guardie:'),
        ["G9", "G8"],
        key="sc_guard_level_selector_final_official_v100"
    )

    # --- 2. INPUT LEADERSHIP MASSIMA (Cella C16 del tuo foglio) ---
    max_leadership = st.number_input(
        ctx.get('calc_max_leadership_lbl', 'Maximum Leadership:'),
        min_value=0, value=332000, step=1000, key="sc_max_lead"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops to Include in March')}")

    # --- 3. CONFIGURAZIONE FILTRI DEI LIVELLI ATTIVI ---
    filtri_fogli = {
        "Guardie 9": livello_scelto == "G9",
        "Guardie 8": livello_scelto in ["G9", "G8"],
        "Catapulte 9": livello_scelto == "G9",
        "Catapulte 8": livello_scelto in ["G9", "G8"]
    }

    # --- 4. DATABASE INTEGRALE ORIGINALE CON LE 9 RIGHE REGOLARI DI MAURIZIO ---
    database_truppe = [
        {"id": "l9_corax", "name": "L9 Corax", "lead_cost": 20, "stacks": 2, "ratio": 0.50, "filter_key": "Guardie 9", "cat": "Flyer"},
        {"id": "l8_corax", "name": "L8 Corax", "lead_cost": 20, "stacks": 2, "ratio": 1.00, "filter_key": "Guardie 8", "cat": "Flyer"},
        
        {"id": "l9_cavalli", "name": "L9 Cavalli (Mounted)", "lead_cost": 2, "stacks": 2, "ratio": 0.55, "filter_key": "Guardie 9", "cat": "Mounted"},
        {"id": "l8_cavalli", "name": "L8 Cavalli (Mounted)", "lead_cost": 2, "stacks": 2, "ratio": 1.00, "filter_key": "Guardie 8", "cat": "Mounted"},
        
        {"id": "l9_guardie", "name": "L9 Guardie (Melee/Ranged)", "lead_cost": 1, "stacks": 4, "ratio": 0.55, "filter_key": "Guardie 9", "cat": "Melee/Ranged"},
        {"id": "l8_guardie", "name": "L8 Guardie (Melee/Ranged)", "lead_cost": 1, "stacks": 4, "ratio": 1.00, "filter_key": "Guardie 8", "cat": "Melee/Ranged"},
        
        {"id": "c9_catapulte", "name": "C9 Catapulte (Siege)", "lead_cost": 10, "stacks": 1, "ratio": 0.57, "filter_key": "Catapulte 9", "cat": "Engineer Corps"},
        {"id": "c8_catapulte", "name": "C8 Catapulte (Siege)", "lead_cost": 10, "stacks": 1, "ratio": 1.03, "filter_key": "Catapulte 8", "cat": "Engineer Corps"}
    ]

    stati_checkbox = {}
    moltiplicatore_dinamico = 0.0
    categorie = ["Flyer", "Mounted", "Melee/Ranged", "Engineer Corps"]
    
    # Generazione dei checkbox interattivi (Mostra solo le truppe coerenti con G9 o G8 scelto)
    for cat in categorie:
        st.markdown(f"**{cat}**")
        cols = st.columns(2)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat and filtri_fogli[t["filter_key"]]]
        
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 2]:
                nome_tradotto = ctx.get(truppa["name"], truppa["name"])
                
                # Ciascuna casella attiva o esclude dinamicamente il peso dal calcolo di J19
                attiva = st.checkbox(nome_tradotto, value=True, key=f"chk_official_v100_{truppa['id']}")
                stati_checkbox[truppa["id"]] = attiva
                
                if attiva and truppa["stacks"] > 0:
                    contr_riga = truppa["stacks"] * truppa["ratio"]
                    moltiplicatore_dinamico += contr_riga
                    
        st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    # --- 5. CALCOLO REATTIVO AUTOMATICO DEL RIFERIMENTO STACK ---
    if moltiplicatore_dinamico > 0:
        stack_reference = max_leadership / moltiplicatore_dinamico
    else:
        stack_reference = 0

    # Display del Moltiplicatore dinamico (Cella B19 del foglio)
    st.markdown(
        f"""
        <div class="chat-box" style="text-align: center; max-width: 500px; margin: 20px auto; border-left: 6px solid #bd9b53 !important; background: linear-gradient(145deg, #241f16, #14120e) !important; padding: 10px !important;">
            <h2 style="margin: 0 0 2px 0; font-size: 13px; color: #bd9b53; letter-spacing: 0.5px; font-family: 'Cinzel', serif;">
                {ctx.get('calc_auto_multiplier_lbl', 'CURRENT ACTIVE MULTIPLIER (B19)')}
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

    if stack_reference > 0:
        for truppa in database_truppe:
            # Se la truppa appartiene al livello attivo ed è selezionata dal giocatore
            if filtri_fogli[truppa["filter_key"]] and stati_checkbox[truppa["id"]] and truppa["stacks"] > 0:
                
                # TRADUZIONE LETTERALE DELLA FORMULA DI MAURIZIO:
                # =INT(Ratio / Costo_Lead * Riferimento_Stack / 10 + 0.45) * 10
                valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_reference / 10) + 0.45
                count_truppe_per_stack = int(valore_interno) * 10
                
                # La leadership di riga tiene conto del numero complessivo degli stack attivi nel gioco
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
        
        # Stampa dei box riassuntivi della leadership allocata
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
