import streamlit as st

def mostra_calcolatore_semplice(ctx):
    st.markdown(f"<h1>{ctx.get('simple_calc_main_h1', '🧮 Simple Troops Calculator')}</h1>", unsafe_allow_html=True)
    st.write(ctx.get('simple_calc_main_subtitle', 'Enter your maximum leadership and customize your active troops.'))
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- 1. INPUT LEADERSHIP MASSIMA A 0 DI DEFAULT ---
    max_leadership = st.number_input(
        ctx.get('calc_max_leadership_lbl', 'Maximum Leadership:'),
        min_value=0, value=0, step=1000, key="sc_max_lead_v700"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops to Include in March')}")

    # --- 2. DATABASE COMPLETO SENZA I LIVELLI 7 ---
    database_truppe = [
        # --- LIVELLO 9 ---
        {"id": "g9_flyer", "name": "L9 Guard Flyer (Corax)", "lead_cost": 20, "stacks": 1, "ratio": 0.50, "cat": "Flyer"},
        {"id": "s9_flyer", "name": "L9 Spec Flyer (Griffin/Lion)", "lead_cost": 20, "stacks": 1, "ratio": 0.50, "cat": "Flyer"},
        {"id": "g9_mounted", "name": "L9 Guard Mounted (Cavalli)", "lead_cost": 2, "stacks": 1, "ratio": 0.55, "cat": "Mounted"},
        {"id": "s9_mounted", "name": "L9 Spec Mounted", "lead_cost": 2, "stacks": 1, "ratio": 0.55, "cat": "Mounted"},
        {"id": "g9_ranged", "name": "L9 Guard Ranged (Arco)", "lead_cost": 1, "stacks": 1, "ratio": 0.55, "cat": "Ranged"},
        {"id": "s9_ranged", "name": "L9 Spec Ranged", "lead_cost": 1, "stacks": 1, "ratio": 0.55, "cat": "Ranged"},
        {"id": "g9_melee", "name": "L9 Guard Melee (Mischia)", "lead_cost": 1, "stacks": 1, "ratio": 0.55, "cat": "Melee"},
        {"id": "s9_melee", "name": "L9 Spec Melee", "lead_cost": 1, "stacks": 1, "ratio": 0.55, "cat": "Melee"},
        {"id": "c9_engineer", "name": "C9 Engineer Corps", "lead_cost": 10, "stacks": 1, "ratio": 0.57, "cat": "Engineer Corps"},

        # --- LIVELLO 8 ---
        {"id": "g8_flyer", "name": "L8 Guard Flyer (Corax)", "lead_cost": 20, "stacks": 1, "ratio": 1.00, "cat": "Flyer"},
        {"id": "s8_flyer", "name": "L8 Spec Flyer", "lead_cost": 20, "stacks": 1, "ratio": 1.00, "cat": "Flyer"},
        {"id": "g8_mounted", "name": "L8 Guard Mounted (Cavalli)", "lead_cost": 2, "stacks": 1, "ratio": 1.00, "cat": "Mounted"},
        {"id": "s8_mounted", "name": "L8 Spec Mounted", "lead_cost": 2, "stacks": 1, "ratio": 1.00, "cat": "Mounted"},
        {"id": "g8_ranged", "name": "L8 Guard Ranged (Arco)", "lead_cost": 1, "stacks": 1, "ratio": 1.00, "cat": "Ranged"},
        {"id": "s8_ranged", "name": "L8 Spec Ranged", "lead_cost": 1, "stacks": 1, "ratio": 1.00, "cat": "Ranged"},
        {"id": "g8_melee", "name": "L8 Guard Melee (Mischia)", "lead_cost": 1, "stacks": 1, "ratio": 1.00, "cat": "Melee"},
        {"id": "s8_melee", "name": "L8 Spec Melee", "lead_cost": 1, "stacks": 1, "ratio": 1.00, "cat": "Melee"},
        {"id": "c8_engineer", "name": "C8 Engineer Corps", "lead_cost": 10, "stacks": 1, "ratio": 1.03, "cat": "Engineer Corps"}
    ]

    truppe_selezionate = []
    stati_checkbox = {}
    moltiplicatore_dinamico = 0.0
    categorie = ["Flyer", "Mounted", "Ranged", "Melee", "Engineer Corps"]
    
    # Generazione Checkbox
    for cat in categorie:
        st.markdown(f"**{cat}**")
        cols = st.columns(2)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat]
        
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 2]:
                nome_tradotto = ctx.get(truppa["name"], truppa["name"])
                attiva = st.checkbox(nome_tradotto, value=True, key=f"chk_v700_{truppa['id']}")
                stati_checkbox[truppa["id"]] = attiva
                if attiva:
                    truppe_selezionate.append(truppa)
                    moltiplicatore_dinamico += truppa["ratio"]
                    
        st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    # --- 3. CALCOLO REATTIVO DEL RIFERIMENTO STACK ---
    if moltiplicatore_dinamico > 0:
        stack_reference = max_leadership / moltiplicatore_dinamico
    else:
        stack_reference = 0

    st.markdown(f"""
        <div class="chat-box" style="text-align: center; max-width: 500px; margin: 20px auto; border-left: 6px solid #bd9b53 !important; background: linear-gradient(145deg, #241f16, #14120e) !important; padding: 10px !important;">
            <h2 style="margin: 0 0 2px 0; font-size: 13px; color: #bd9b53; letter-spacing: 0.5px; font-family: 'Cinzel', serif;">
                {ctx.get('calc_auto_multiplier_lbl', 'CURRENT ACTIVE MULTIPLIER (B19)')}
            </h2>
            <p style="font-size: 26px; font-weight: bold; color: #f0e6d2; margin: 0; font-family: 'Cinzel', serif;">
                {moltiplicatore_dinamico:.2f}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")

    risultati_finali_html = ""
    totale_leadership_usata = 0

    if max_leadership > 0 and stack_reference > 0:
        for truppa in truppe_selezionate:
            # FORMULA ORIGINALE DI MAURIZIO
            valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_reference / 10) + 0.45
            count_truppe = int(valore_interno) * 10
            
            leadership_riga = count_truppe * truppa["lead_cost"]
            totale_leadership_usata += leadership_riga

            count_formattato = f"{count_truppe:,}".replace(",", ".")
            lead_riga_formattata = f"{leadership_riga:,}".replace(",", ".")
            nome_tradotto_riga = ctx.get(truppa["name"], truppa["name"])

            if count_truppe > 0:
                risultati_finali_html += f"""
                <div class="chat-box" style="display:flex; justify-content:space-between; align-items:center; padding:10px 16px!important; margin-bottom:8px!important;">
                    <span style="color:#f0e6d2; font-weight:500;">{nome_tradotto_riga}</span>
                    <div style="text-align:right;">
                        <span style="color:#bd9b53; font-weight:bold; font-size:18px; margin-right:15px;">{count_formattato} u.</span>
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
        st.info(ctx.get('calc_no_troops_allocated', 'Inserisci un valore di Leadership Massima per calcolare la distribuzione dei plotoni.'))
