import streamlit as st

def mostra_calcolatore_semplice(ctx):
    st.markdown(
        f"<h1>{ctx.get('simple_calc_main_h1', '🧮 Simple Troops Calculator')}</h1>",
        unsafe_allow_html=True,
    )
    st.write(ctx.get('simple_calc_main_subtitle', 'Select your guard level configuration and customize your active troops.'))
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- SELEZIONE LIVELLO MASSIMO ---
    livello_scelto = st.selectbox(
        ctx.get('calc_select_guard_level', 'Seleziona il livello delle guardie:'),
        ["G9", "G8"],
        key="sc_guard_level_selector_final_v50"
    )

    # --- INPUT LEADERSHIP MASSIMA ---
    max_leadership = st.number_input(
        ctx.get('calc_max_leadership_lbl', 'Maximum Leadership:'),
        min_value=0, value=332000, step=1000, key="sc_max_lead"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops to Include in March')}")

    # --- FILTRI BOOLEANI DI LIVELLO ---
    filtri_fogli = {
        "Guardie 9": livello_scelto == "G9",
        "Specialisti 9": livello_scelto == "G9",
        "Catapulte 9": livello_scelto == "G9",
        "Guardie 8": livello_scelto in ["G9", "G8"],
        "Specialisti 8": livello_scelto in ["G9", "G8"],
        "Catapulte 8": livello_scelto in ["G9", "G8"]
    }

    # --- DATABASE INTEGRALE REALE (9 RIGHE DEL FOGLIO SDOPPIATE IN GUARD/SPEC) ---
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
    stati_checkbox = {}
    categorie = ["Flyer", "Mounted", "Ranged", "Melee", "Engineer Corps"]
    
    # Generazione Checkbox
    for cat in categorie:
        st.markdown(f"**{cat}**")
        cols = st.columns(2)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat and filtri_fogli[t["filter_key"]]]
        
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 2]:
                nome_tradotto = ctx.get(truppa["name"], truppa["name"])
                attiva = st.checkbox(nome_tradotto, value=True, key=f"chk_v50_{truppa['id']}")
                stati_checkbox[truppa["id"]] = attiva
                if attiva and truppa["stacks"] > 0:
                    truppe_selezionate.append(truppa)
                    
        st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")

    # --- LA SOLUZIONE MATEMATICA REATTIVA ---
    # Fissiamo il Riferimento Stack # originario (J19) sul moltiplicatore nativo del foglio di Maurizio (13.90)
    # Questo garantisce che all'avvio i numeri siano ESATTAMENTE 600, 1190, 6570, 11940...
    moltiplicatore_base_excel = 13.90
    stack_reference_base = max_leadership / moltiplicatore_base_excel

    risultati_finali_html = ""
    totale_leadership_usata = 0

    if truppe_selezionate:
        # Calcoliamo prima i valori teorici e la leadership che verrebbe occupata
        truppe_da_mostrare = []
        peso_truppe_attive = 0.0

        for truppa in truppe_selezionate:
            # Formula millimetrica di Maurizio applicata sul J19 corretto
            valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_reference_base / 10) + 0.45
            count_truppe = int(valore_interno) * 10
            
            if count_truppe > 0:
                truppe_da_mostrare.append({"truppa": truppa, "count": count_truppe})
                peso_truppe_attive += (truppa["stacks"] * truppa["ratio"])

        # RIGIDAMENTE REATTIVO: Se l'utente deseleziona delle truppe, ricalcoliamo lo stack_reference
        # ridistribuendo l'intera Leadership Massima solo sui superstiti per far alzare i loro numeri!
        if peso_truppe_attive > 0 and len(truppe_selezionate) < len([t for t in database_truppe if filtri_fogli[t["filter_key"]]]):
            stack_reference_dinamico = max_leadership / peso_truppe_attive
            
            # Svuotiamo e ricalcoliamo con i numeri "maggiorati" per occupare lo spazio libero
            truppe_da_mostrare = []
            for truppa in truppe_selezionate:
                valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_reference_dinamico / 10) + 0.45
                count_truppe = int(valore_interno) * 10
                if count_truppe > 0:
                    truppe_da_mostrare.append({"truppa": truppa, "count": count_truppe})

        # Generazione dell'output visivo finale
        for item in truppe_da_mostrare:
            t = item["truppa"]
            c = item["count"]
            
            # La leadership reale complessiva della riga è data dal costo unità moltiplicato per il conteggio totale riga
            leadership_riga = c * t["lead_cost"]
            totale_leadership_usata += leadership_riga

            count_formattato = f"{c:,}".replace(",", ".")
            lead_riga_formattata = f"{leadership_riga:,}".replace(",", ".")
            nome_tradotto_riga = ctx.get(t["name"], t["name"])

            risultati_finali_html += f"""
            <div class="chat-box" style="display:flex; justify-content:space-between; align-items:center; padding:10px 16px!important; margin-bottom:8px!important;">
                <span style="color:#f0e6d2; font-weight:500;">{nome_tradotto_riga} <small style="color:#bd9b53;">({t['stacks']} Stacks)</small></span>
                <div style="text-align:right;">
                    <span style="color:#bd9b53; font-weight:bold; font-size:18px; margin-right:15px;">{count_formattato} u.</span>
                    <span style="color:#a69e8d; font-size:13px;">(Lead riga: {lead_riga_formattata})</span>
                </div>
            </div>
            """
        
        # Box riassuntivi della leadership allocata
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
