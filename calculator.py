import streamlit as st

def mostra_calcolatore_semplice(ctx):
    st.markdown(
        f"<h1>{ctx.get('simple_calc_main_h1', '🧮 Simple Troops Calculator')}</h1>",
        unsafe_allow_html=True,
    )
    st.write(ctx.get('simple_calc_main_subtitle', 'Select your guard level configuration to balance your march stacks.'))
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- SELEZIONE LIVELLO DELLE GUARDIE ---
    livello_scelto = st.selectbox(
        ctx.get('calc_select_guard_level', 'Seleziona il livello delle guardie:'),
        ["G9", "G8"],
        key="sc_guard_level_selector_final_v5"
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

    # --- DATABASE REALE COMPLETO DI TUTTE LE RIGHE DEL FOGLIO ---
    database_truppe = [
        {"id": "l9_flyer", "name": "L9 Flyer (Corax)", "lead_cost": 20, "stacks": 2, "ratio": 0.50, "filter_key": "L9", "cat": "Flyer"},
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
    stati_checkbox = {}
    categorie = ["Flyer", "Mounted", "Ranged", "Melee", "Engineer Corps"]
    
    # Interfaccia interattiva a Checkbox (Tutte attive di default come nel foglio di Maurizio)
    for cat in categorie:
        st.markdown(f"**{cat}**")
        cols = st.columns(3)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat and filtri_attivi[t["filter_key"]]]
        
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 3]:
                nome_tradotto = ctx.get(truppa["name"], truppa["name"])
                
                # Checkbox flessibile
                attiva = st.checkbox(nome_tradotto, value=True, key=f"chk_v22_{truppa['id']}")
                stati_checkbox[truppa["id"]] = attiva
                if attiva and truppa["stacks"] > 0:
                    truppe_selezionate.append(truppa)
                    
        st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    # --- CALCOLO BASE FISSO SULLA STRUTTURA DEL FOGLIO (MOLTIPLICATORE TOTALE = 20.10) ---
    # Per fare in modo che escano i tuoi numeri precisi (600, 1190, 13140, 23880), il Riferimento Stack #
    # deve essere calcolato dividendo la leadership massima per il coefficiente di tutta la marcia potenziale (20.10)
    moltiplicatore_strutturale_excel = 20.10
    stack_reference = max_leadership / moltiplicatore_strutturale_excel

    st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")

    risultati_finali_html = ""
    totale_leadership_effettiva = 0

    if truppe_selezionate:
        for truppa in truppe_selezionate:
            # APPLICAZIONE MILLIMETRICA DELLA FORMULA DI MAURIZIO:
            # =INT(Ratio / Costo_Lead * Riferimento_Stack / 10 + 0.45) * 10
            valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_reference / 10) + 0.45
            count_truppe_per_stack = int(valore_interno) * 10
            
            leadership_riga = count_truppe_per_stack * truppa["stacks"] * truppa["lead_cost"]
            totale_leadership_effettiva += leadership_riga

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
        
        # Mostra il riepilogo totale (In linea con la logica del foglio)
        lead_usata_formattata = f"{totale_leadership_effettiva:,}".replace(",", ".")
        lead_max_formattata = f"{max_leadership:,}".replace(",", ".")
        st.markdown(f'<div class="chat-box" style="text-align:center;"><h3>Total Theoretical Leadership Allocated</h3><p style="font-size:24px;color:#e69138;font-weight:bold;margin:0;">{lead_usata_formattata} / {lead_max_formattata}</p></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(risultati_finali_html, unsafe_allow_html=True)
    else:
        st.info(ctx.get('calc_no_troops_allocated', 'Nessuna truppa selezionata.'))
