import streamlit as st

def mostra_calcolatore_semplice(ctx):
    st.markdown(f"<h1>{ctx.get('simple_calc_main_h1', '🧮 Simple Troops Calculator')}</h1>", unsafe_allow_html=True)
    
    # --- NOTIFICA SUI CAPITANI ALLARGATA E AD ALTA LEGGIBILITÀ ---
    st.markdown(f"""
    <div class="chat-box" style="padding:16px 20px!important; text-align:left; color:#f0e6d2; border-left:5px solid #cc4125!important; margin-bottom:20px; background: rgba(255, 255, 255, 0.02); width:100%;">
        <b style="color:#cc4125; font-size:15px; letter-spacing:0.5px; display:block; margin-bottom:6px;">⚠️ IMPORTANT CAPTAIN NOTE:</b>
        <span style="font-size:13.5px; color:#e1d7c6; line-height:1.5; font-weight:400; display:block;">
            This calculator assumes you are using standard captains. If you use captains that grant specific health bonuses to a single troop type, the distribution formula will not balance correctly.
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- 1. INPUT LEADERSHIP MASSIMA (FORMATTATO SENZA DECIMALI INUTILI) ---
    max_leadership = st.number_input(
        ctx.get('calc_max_leadership_lbl', 'Maximum Leadership:'),
        min_value=0.0, value=0.0, step=1000.0, format="%.0f", key="sc_max_lead_v9000"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- NOTIFICA SE LA LEADERSHIP È 0 ---
    if max_leadership == 0.0:
        testo_notifica = ctx.get('calc_no_troops_allocated', 'Please enter a Maximum Leadership value to calculate the troop stack distribution.')
        st.markdown(f"""
        <div class="chat-box" style="padding:15px!important; text-align:center; color:#a69e8d; border-left:4px solid #bd9b53!important; margin-bottom:20px;">
            {testo_notifica}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops to Include in March')}")

    # --- 2. DATABASE INTEGRALE ORDINATO PER FILI VISIVE RIGIDE ---
    database_truppe = [
        # --- FILA 1: GUARDIE LIVELLO 9 ---
        {"id": "g9_flyer", "name": "Liv.9 Guard Flyer", "lead_cost": 20, "ratio": 0.50, "cat": "Flyer", "row": 1, "col_idx": 0},
        {"id": "g9_mounted", "name": "Liv.9 Guard Mounted", "lead_cost": 2, "ratio": 0.55, "cat": "Mounted", "row": 1, "col_idx": 1},
        {"id": "g9_ranged", "name": "Liv.9 Guard Ranged", "lead_cost": 1, "ratio": 0.55, "cat": "Ranged", "row": 1, "col_idx": 2},
        {"id": "g9_melee", "name": "Liv.9 Guard Melee", "lead_cost": 1, "ratio": 0.55, "cat": "Melee", "row": 1, "col_idx": 3},

        # --- FILA 2: SPECIALISTI LIVELLO 9 ---
        {"id": "s9_flyer", "name": "Liv.9 Spec Flyer", "lead_cost": 20, "ratio": 0.50, "cat": "Flyer", "row": 2, "col_idx": 0},
        {"id": "s9_mounted", "name": "Liv.9 Spec Mounted", "lead_cost": 2, "ratio": 0.55, "cat": "Mounted", "row": 2, "col_idx": 1},
        {"id": "s9_ranged", "name": "Liv.9 Spec Ranged", "lead_cost": 1, "ratio": 0.55, "cat": "Ranged", "row": 2, "col_idx": 2},
        {"id": "s9_melee", "name": "Liv.9 Spec Melee", "lead_cost": 1, "ratio": 0.55, "cat": "Melee", "row": 2, "col_idx": 3},

        # --- FILA 3: GUARDIE LIVELLO 8 ---
        {"id": "g8_flyer", "name": "Liv.8 Guard Flyer", "lead_cost": 20, "ratio": 1.00, "cat": "Flyer", "row": 3, "col_idx": 0},
        {"id": "g8_mounted", "name": "Liv.8 Guard Mounted", "lead_cost": 2, "ratio": 1.00, "cat": "Mounted", "row": 3, "col_idx": 1},
        {"id": "g8_ranged", "name": "Liv.8 Guard Ranged", "lead_cost": 1, "ratio": 1.00, "cat": "Ranged", "row": 3, "col_idx": 2},
        {"id": "g8_melee", "name": "Liv.8 Guard Melee", "lead_cost": 1, "ratio": 1.00, "cat": "Melee", "row": 3, "col_idx": 3},

        # --- FILA 4: SPECIALISTI LIVELLO 8 ---
        {"id": "s8_flyer", "name": "Liv.8 Spec Flyer", "lead_cost": 20, "ratio": 1.00, "cat": "Flyer", "row": 4, "col_idx": 0},
        {"id": "s8_mounted", "name": "Liv.8 Spec Mounted", "lead_cost": 2, "ratio": 1.00, "cat": "Mounted", "row": 4, "col_idx": 1},
        {"id": "s8_ranged", "name": "Liv.8 Spec Ranged", "lead_cost": 1, "ratio": 1.00, "cat": "Ranged", "row": 4, "col_idx": 2},
        {"id": "s8_melee", "name": "Liv.8 Spec Melee", "lead_cost": 1, "ratio": 1.00, "cat": "Melee", "row": 4, "col_idx": 3},

        # --- FILA 5: GENIERI ---
        {"id": "c9_engineer", "name": "Liv.9 Engineer Corps", "lead_cost": 10, "ratio": 0.57, "cat": "Engineer Corps", "row": 5, "col_idx": 0},
        {"id": "c8_engineer", "name": "Liv.8 Engineer Corps", "lead_cost": 10, "ratio": 1.03, "cat": "Engineer Corps", "row": 5, "col_idx": 1}
    ]

    truppe_selezionate = []
    stati_checkbox = {}
    moltiplicatore_dinamico = 0.0
    categorie_mostrate = ["Flyer", "Mounted", "Ranged", "Melee", "Engineer Corps"]
    
    # Generazione dei Checkbox delle singole truppe
    for cat in categorie_mostrate:
        st.markdown(f"**{cat}**")
        cols = st.columns(2)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat]
        
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 2]:
                nome_tradotto = ctx.get(truppa["name"], truppa["name"])
                attiva = st.checkbox(nome_tradotto, value=True, key=f"chk_v9000_{truppa['id']}")
                stati_checkbox[truppa["id"]] = attiva
                if attiva:
                    truppe_selezionate.append(truppa)
                    moltiplicatore_dinamico += truppa["ratio"]
                    
        st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    # --- 3. CALCOLO REATTIVO IN BACKGROUND ---
    if moltiplicatore_dinamico > 0:
        stack_reference = max_leadership / moltiplicatore_dinamico
    else:
        stack_reference = 0

    # Generazione dei blocchi rigidi a schermo
    if max_leadership > 0.0 and stack_reference > 0:
        st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")
        
        totale_leadership_usata = 0
        mappa_risultati = {}

        for truppa in database_truppe:
            is_attiva = stati_checkbox.get(truppa["id"], False)
            
            if is_attiva:
                valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_reference / 10) + 0.45
                count_truppe = int(valore_interno) * 10
                leadership_riga = count_truppe * truppa["lead_cost"]
                totale_leadership_usata += leadership_riga
                count_formattato = f"{count_truppe:,}".replace(",", ".")
            else:
                count_formattato = "0"

            mappa_risultati[truppa["id"]] = {
                "name": ctx.get(truppa["name"], truppa["name"]),
                "count": count_formattato,
                "row": truppa["row"],
                "col_idx": truppa["col_idx"]
            }

        # Monitor centrale della leadership allocata
        lead_usata_formattata = f"{totale_leadership_usata:,}".replace(",", ".")
        lead_max_formattata = f"{int(max_leadership):,}".replace(",", ".")
        st.markdown(f'<div class="chat-box" style="text-align:center; max-width: 400px; margin: 0 auto 20px auto;"><h3>{ctx.get("calc_total_used_lead_lbl", "Total Leadership Allocated")}</h3><p style="font-size:24px;color:#4a86e8;font-weight:bold;margin:0;">{lead_usata_formattata} / {lead_max_formattata}</p></div>', unsafe_allow_html=True)

        # --- DISEGNO RIGIDO DELLE 5 FILE DI UNITÀ ---
        labels_file = {
            1: "🛡️ Guard Level 9",
            2: "⚡ Specialists Level 9",
            3: "⚔️ Guard Level 8",
            4: "🔮 Specialists Level 8",
            5: "📐 Engineer Corps"
        }

        for r in range(1, 6):
            st.markdown(f"<small style='color:#bd9b53;font-weight:bold;'>{labels_file[r]}</small>", unsafe_allow_html=True)
            truppe_riga = [t for t in database_truppe if t["row"] == r]
            
            cols_griglia = st.columns(4)
            
            for truppa in truppe_riga:
                info = mappa_risultati[truppa["id"]]
                with cols_griglia[info["col_idx"]]:
                    st.markdown(f"""
                    <div class="chat-box" style="text-align: center; padding: 12px!important; min-height: 85px; display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 10px;">
                        <span style="color:#a69e8d; font-size:12px; font-weight:500; display: block; margin-bottom: 6px; line-height: 1.2;">{info['name']}</span>
                        <b style="color:#bd9b53; font-size:18px; display: block;">{info['count']}</b>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)
