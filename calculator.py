import streamlit as st

def mostra_calcolatore_semplice(ctx):
    st.markdown(
        f"<h1>{ctx.get('simple_calc_main_h1', '🧮 Simple Troops Calculator')}</h1>",
        unsafe_allow_html=True,
    )
    st.write(ctx.get('simple_calc_main_subtitle', 'Select your troop configuration to calculate the exact march count.'))
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- INPUT DELLA LEADERSHIP MASSIMA ---
    max_leadership = st.number_input(
        ctx.get('calc_max_leadership_lbl', 'Maximum Leadership:'),
        min_value=0, value=332000, step=1000, key="sc_max_lead"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops to Include in March')}")

    # --- DATABASE AGGIORNATO CON ENGINEER CORPS ---
    database_truppe = [
        {"id": "l9_flyer", "name": "L9 Flyer (Corax)", "lead_cost": 20, "contr": 1.00, "cat": "Flyer"},
        {"id": "l8_flyer", "name": "L8 Flyer (Corax)", "lead_cost": 20, "contr": 2.00, "cat": "Flyer"},
        {"id": "l7_flyer", "name": "L7 Flyer (Corax)", "lead_cost": 20, "contr": 0.00, "cat": "Flyer"},
        
        {"id": "l9_mounted", "name": "L9 Mounted", "lead_cost": 2, "contr": 1.10, "cat": "Mounted"},
        {"id": "l8_mounted", "name": "L8 Mounted", "lead_cost": 2, "contr": 2.00, "cat": "Mounted"},
        
        {"id": "l9_ranged", "name": "L9 Ranged", "lead_cost": 1, "contr": 2.20, "cat": "Ranged"},
        {"id": "l8_ranged", "name": "L8 Ranged", "lead_cost": 1, "contr": 4.00, "cat": "Ranged"},
        
        {"id": "l9_melee", "name": "L9 Melee", "lead_cost": 1, "contr": 2.20, "cat": "Melee"},
        {"id": "l8_melee", "name": "L8 Melee", "lead_cost": 1, "contr": 4.00, "cat": "Melee"},
        
        {"id": "c9_engineer", "name": "C9 Engineer Corps", "lead_cost": 10, "contr": 0.57, "cat": "Engineer Corps"},
        {"id": "c8_engineer", "name": "C8 Engineer Corps", "lead_cost": 10, "contr": 1.03, "cat": "Engineer Corps"}
    ]

    truppe_selezionate = []
    moltiplicatore_totale = 0.0

    # Categorie aggiornate con i 5 nomi ufficiali di gioco
    categorie = ["Flyer", "Mounted", "Ranged", "Melee", "Engineer Corps"]
    
    for cat in categorie:
        st.markdown(f"**{cat}**")
        cols = st.columns(3)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat]
        
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 3]:
                nome_tradotto = ctx.get(truppa["name"], truppa["name"])
                def_val = truppa["contr"] > 0
                
                attiva = st.checkbox(nome_tradotto, value=def_val, key=f"chk_{truppa['id']}")
                if attiva:
                    truppe_selezionate.append(truppa)
                    moltiplicatore_totale += truppa["contr"]
        st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    # --- CALCOLO MATEMATICO ---
    if moltiplicatore_totale > 0:
        stack_reference = max_leadership / moltiplicatore_totale
    else:
        stack_reference = 0

    # --- DISPLAY DEL MOLTIPLICATORE DINAMICO ---
    st.markdown(
        f"""
        <div class="chat-box" style="text-align: center; max-width: 500px; margin: 20px auto; border-left: 6px solid #bd9b53 !important; background: linear-gradient(145deg, #241f16, #14120e) !important; padding: 10px !important;">
            <h2 style="margin: 0 0 2px 0; font-size: 13px; color: #bd9b53; letter-spacing: 0.5px; font-family: 'Cinzel', serif;">
                {ctx.get('calc_auto_multiplier_lbl', 'AUTOMATIC MULTIPLIER')}
            </h2>
            <p style="font-size: 26px; font-weight: bold; color: #f0e6d2; margin: 0; font-family: 'Cinzel', serif;">
                {moltiplicatore_totale:.2f}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- COMPOSIZIONE FINALE DELLA MARCIA ---
    st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")

    risultati_finali_html = ""
    totale_leadership_effettiva = 0

    if stack_reference > 0 and truppe_selezionate:
        for truppa in truppe_selezionate:
            if truppa["contr"] > 0:
                leadership_riga = stack_reference * truppa["contr"]
                count_truppe = round(leadership_riga / truppa["lead_cost"])
                
                leadership_effettiva_riga = count_truppe * truppa["lead_cost"]
                totale_leadership_effettiva += leadership_effettiva_riga

                count_formattato = f"{count_truppe:,}".replace(",", ".")
                lead_riga_formattata = f"{leadership_effettiva_riga:,}".replace(",", ".")
                nome_tradotto_riga = ctx.get(truppa["name"], truppa["name"])

                risultati_finali_html += f"""
                <div class="chat-box" style="display:flex; justify-content:space-between; align-items:center; padding:10px 16px!important; margin-bottom:8px!important;">
                    <span style="color:#f0e6d2; font-weight:500;">{nome_tradotto_riga}</span>
                    <div style="text-align:right;">
                        <span style="color:#bd9b53; font-weight:bold; font-size:18px; margin-right:15px;">{count_formattato} u.</span>
                        <span style="color:#a69e8d; font-size:13px;">(Lead: {lead_riga_formattata})</span>
                    </div>
                </div>
                """
        
        # Box riassuntivi della Leadership Totale Allocata
        lead_usata_formattata = f"{totale_leadership_effettiva:,}".replace(",", ".")
        lead_max_formattata = f"{max_leadership:,}".replace(",", ".")
        st.markdown(f'<div class="chat-box" style="text-align:center;"><h3>{ctx.get("calc_total_used_lead_lbl", "Total Leadership Allocated")}</h3><p style="font-size:24px;color:#4a86e8;font-weight:bold;margin:0;">{lead_usata_formattata} / {lead_max_formattata}</p></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(risultati_finali_html, unsafe_allow_html=True)
    else:
        st.info(ctx.get('calc_no_troops_allocated', 'Please select at least one troop type with a valid multiplier contribution.'))
