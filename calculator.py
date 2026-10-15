import streamlit as st

def mostra_calcolatore_semplice(ctx):
    st.markdown(f"<h1>{ctx.get('simple_calc_main_h1', '🧮 Simple Troops Calculator')}</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- 1. INPUT LEADERSHIP MASSIMA ---
    max_leadership = st.number_input(
        ctx.get('calc_max_leadership_lbl', 'Maximum Leadership:'),
        min_value=0, value=0, step=1000, key="sc_max_lead_v2000"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- NOTIFICA IN ALTO SE LA LEADERSHIP È 0 ---
    if max_leadership == 0:
        testo_notifica = ctx.get('calc_no_troops_allocated', 'Please enter a Maximum Leadership value to calculate the troop stack distribution.')
        st.markdown(f"""
        <div class="chat-box" style="padding:15px!important; text-align:center; color:#a69e8d; border-left:4px solid #bd9b53!important; margin-bottom:20px;">
            {testo_notifica}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops to Include in March')}")

    # --- 2. DATABASE COMPLETO DELLE TRUPPE REGOLARI E SPECIALISTI T9/T8 ---
    database_truppe = [
        # --- LIVELLO 9 ---
        {"id": "g9_flyer", "name": "Liv.9 Guard Flyer", "lead_cost": 20, "stacks": 2, "ratio": 0.50, "cat": "Flyer"},
        {"id": "s9_flyer", "name": "Liv.9 Spec Flyer", "lead_cost": 20, "stacks": 2, "ratio": 0.50, "cat": "Flyer"},
        {"id": "g9_mounted", "name": "Liv.9 Guard Mounted", "lead_cost": 2, "stacks": 2, "ratio": 0.55, "cat": "Mounted"},
        {"id": "s9_mounted", "name": "Liv.9 Spec Mounted", "lead_cost": 2, "stacks": 2, "ratio": 0.55, "cat": "Mounted"},
        {"id": "g9_ranged", "name": "Liv.9 Guard Ranged", "lead_cost": 1, "stacks": 4, "ratio": 0.55, "cat": "Ranged"},
        {"id": "s9_ranged", "name": "Liv.9 Spec Ranged", "lead_cost": 1, "stacks": 4, "ratio": 0.55, "cat": "Ranged"},
        {"id": "g9_melee", "name": "Liv.9 Guard Melee", "lead_cost": 1, "stacks": 4, "ratio": 0.55, "cat": "Melee"},
        {"id": "s9_melee", "name": "Liv.9 Spec Melee", "lead_cost": 1, "stacks": 4, "ratio": 0.55, "cat": "Melee"},
        {"id": "c9_engineer", "name": "Liv.9 Engineer Corps", "lead_cost": 10, "stacks": 1, "ratio": 0.57, "cat": "Engineer Corps"},

        # --- LIVELLO 8 ---
        {"id": "g8_flyer", "name": "Liv.8 Guard Flyer", "lead_cost": 20, "stacks": 2, "ratio": 1.00, "cat": "Flyer"},
        {"id": "s8_flyer", "name": "Liv.8 Spec Flyer", "lead_cost": 20, "stacks": 2, "ratio": 1.00, "filter_key": "Specialisti 8", "cat": "Flyer"},
        {"id": "g8_mounted", "name": "Liv.8 Guard Mounted", "lead_cost": 2, "stacks": 2, "ratio": 1.00, "cat": "Mounted"},
        {"id": "s8_mounted", "name": "Liv.8 Spec Mounted", "lead_cost": 2, "stacks": 2, "ratio": 1.00, "cat": "Mounted"},
        {"id": "g8_ranged", "name": "Liv.8 Guard Ranged", "lead_cost": 1, "stacks": 4, "ratio": 1.00, "cat": "Ranged"},
        {"id": "s8_ranged", "name": "Liv.8 Spec Ranged", "lead_cost": 1, "stacks": 4, "ratio": 1.00, "cat": "Ranged"},
        {"id": "g8_melee", "name": "Liv.8 Guard Melee", "lead_cost": 1, "stacks": 4, "ratio": 1.00, "cat": "Melee"},
        {"id": "s8_melee", "name": "Liv.8 Spec Melee", "lead_cost": 1, "stacks": 4, "ratio": 1.00, "cat": "Melee"},
        {"id": "c8_engineer", "name": "Liv.8 Engineer Corps", "lead_cost": 10, "stacks": 1, "ratio": 1.03, "cat": "Engineer Corps"}
    ]

    truppe_selezionate = []
    stati_checkbox = {}
    moltiplicatore_dinamico = 0.0
    categorie = ["Flyer", "Mounted", "Ranged", "Melee", "Engineer Corps"]
    
    # Generazione dei Checkbox delle singole truppe
    for cat in categorie:
        st.markdown(f"**{cat}**")
        cols = st.columns(2)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat]
        
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 2]:
                nome_tradotto = ctx.get(truppa["name"], truppa["name"])
                attiva = st.checkbox(nome_tradotto, value=True, key=f"chk_v2000_{truppa['id']}")
                stati_checkbox[truppa["id"]] = attiva
                if attiva:
                    truppe_selezionate.append(truppa)
                    moltiplicatore_dinamico += (truppa["stacks"] * truppa["ratio"])
                    
        st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    # --- 3. CALCOLO REATTIVO IN BACKGROUND ---
    if moltiplicatore_dinamico > 0:
        stack_reference = max_leadership / moltiplicatore_dinamico
    else:
        stack_reference = 0

    # Calcolo visivo finale dei plotoni se la leadership inserita è maggiore di 0
    if max_leadership > 0 and stack_reference > 0:
        st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")
        
        totale_leadership_usata = 0
        elementi_griglia = []
        
        for truppa in truppe_selezionate:
            # APPLICAZIONE FORMULA ORIGINALE DI MAURIZIO
            valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_reference / 10) + 0.45
            count_truppe = int(valore_interno) * 10
            
            leadership_riga = count_truppe * truppa["stacks"] * truppa["lead_cost"]
            totale_leadership_usata += leadership_riga

            count_formattato = f"{count_truppe:,}".replace(",", ".")
            nome_tradotto_riga = ctx.get(truppa["name"], truppa["name"])

            if count_truppe > 0:
                # Creiamo la singola cella solida in HTML
                cella_html = f"""
                <div class="chat-box" style="text-align: center; padding: 12px!important; min-height: 80px; display: flex; flex-direction: column; justify-content: center; align-items: center; margin: 4px;">
                    <span style="color:#a69e8d; font-size:12px; font-weight:500; display: block; margin-bottom: 6px; line-height: 1.2;">{nome_tradotto_riga}</span>
                    <b style="color:#bd9b53; font-size:18px; display: block;">{count_formattato}</b>
                </div>
                """
                elementi_griglia.append(cella_html)
        
        # --- COSTRUZIONE DELLA TABELLA RIGIDA A 4 COLONNE ---
        griglia_finale_html = '<table style="width:100%; border-collapse: collapse; border: none; background: transparent;">'
        for i in range(0, len(elementi_griglia), 4):
            griglia_finale_html += '<tr style="border: none; background: transparent;">'
            for j in range(4):
                if i + j < len(elementi_griglia):
                    griglia_finale_html += f'<td style="width: 25%; padding: 0; border: none; background: transparent;">{elementi_griglia[i+j]}</td>'
                else:
                    griglia_finale_html += '<td style="width: 25%; padding: 0; border: none; background: transparent;"></td>'
            griglia_finale_html += '</tr>'
        griglia_finale_html += '</table>'

        lead_usata_formattata = f"{totale_leadership_usata:,}".replace(",", ".")
        lead_max_formattata = f"{max_leadership:,}".replace(",", ".")
        
        # Monitor centrale della leadership allocata
        st.markdown(f'<div class="chat-box" style="text-align:center; max-width: 400px; margin: 0 auto 20px auto;"><h3>{ctx.get("calc_total_used_lead_lbl", "Total Leadership Allocated")}</h3><p style="font-size:24px;color:#4a86e8;font-weight:bold;margin:0;">{lead_usata_formattata} / {lead_max_formattata}</p></div>', unsafe_allow_html=True)
        st.markdown(griglia_finale_html, unsafe_allow_html=True)
