import streamlit as st

def mostra_calcolatore_semplice(ctx):
    st.markdown(f"<h1>{ctx.get('simple_calc_main_h1', '🧮 Simple Troops Calculator')}</h1>", unsafe_allow_html=True)
    
    # --- NOTIFICA SUI CAPITANI PERSONALIZZATA SOTTO IL TITOLO ---
    st.markdown(f"""
    <div class="chat-box" style="padding:16px 20px!important; text-align:left; color:#f0e6d2; border-left:5px solid #cc4125!important; margin-bottom:20px; background: rgba(255, 255, 255, 0.02); width:100%;">
        <b style="color:#cc4125; font-size:15px; letter-spacing:0.5px; display:block; margin-bottom:6px;">⚠️ IMPORTANT CAPTAIN NOTE:</b>
        <span style="font-size:13.5px; color:#e1d7c6; line-height:1.5; font-weight:400; display:block;">
            This calculator assumes you are using standard captains. If you use captains that grant specific health bonuses to a single troop or monster type, the distribution formula will not balance correctly.
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- INPUT AFFIANCATI (LEADERSHIP + SUPREMAZIA) ---
    c1, c2 = st.columns(2)
    max_leadership = c1.number_input(
        ctx.get('calc_max_leadership_lbl', 'Maximum Leadership:'),
        min_value=0, value=0, step=1000, format="%d", key="sc_max_lead_v2026"
    )
    max_supremacy = c2.number_input(
        "Maximum Supremacy:",
        min_value=0, value=0, step=1000, format="%d", key="sc_max_sup_v2026"
    )

    # --- BOX DI CONFERMA VISIVA ---
    if max_leadership > 0 or max_supremacy > 0:
        lead_txt = f"{max_leadership:,}".replace(",", ".")
        sup_txt = f"{max_supremacy:,}".replace(",", ".")
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; max-width: 500px; margin: 10px auto 25px auto; padding: 8px !important; border: 1px solid #bd9b53; background: rgba(189, 155, 83, 0.05); border-radius: 4px; text-align: center;">
            <div><span style="font-size: 11px; color: #bd9b53; font-weight: bold;">CONFIRMED LEADERSHIP</span><p style="font-size: 20px; font-weight: bold; color: #f0e6d2; margin: 0; font-family: 'Cinzel', serif;">{lead_txt}</p></div>
            <div><span style="font-size: 11px; color: #bd9b53; font-weight: bold;">CONFIRMED SUPREMACYYYY</span><p style="font-size: 20px; font-weight: bold; color: #bd9b53; margin: 0; font-family: 'Cinzel', serif;">{sup_txt}</p></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        testo_notifica = ctx.get('calc_no_troops_allocated', 'Please enter your Maximum Leadership or Maximum Supremacy value.')
        st.markdown(f'<div class="chat-box" style="padding:15px!important; text-align:center; color:#a69e8d; border-left:4px solid #bd9b53!important; margin-bottom:20px;">{testo_notifica}</div>', unsafe_allow_html=True)

    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops and Monsters')}")

    # --- DATABASE COMPLETO TRUPPE REGOLARI ---
    database_truppe = [
        {"id": "g9_flyer", "name": "Level 9 Guardians Flyer", "lead_cost": 20, "ratio": 0.50, "cat": "Flyer", "row": 1, "col_idx": 0},
        {"id": "g9_mounted", "name": "Level 9 Guardians Mounted", "lead_cost": 2, "ratio": 0.55, "cat": "Mounted", "row": 1, "col_idx": 1},
        {"id": "g9_ranged", "name": "Level 9 Guardians Ranged", "lead_cost": 1, "ratio": 0.55, "cat": "Ranged", "row": 1, "col_idx": 2},
        {"id": "g9_melee", "name": "Level 9 Guardians Melee", "lead_cost": 1, "ratio": 0.55, "cat": "Melee", "row": 1, "col_idx": 3},
        {"id": "s9_flyer", "name": "Level 9 Specialists Flyer", "lead_cost": 20, "ratio": 0.50, "cat": "Flyer", "row": 2, "col_idx": 0},
        {"id": "s9_mounted", "name": "Level 9 Specialists Mounted", "lead_cost": 2, "ratio": 0.55, "cat": "Mounted", "row": 2, "col_idx": 1},
        {"id": "s9_ranged", "name": "Level 9 Specialists Ranged", "lead_cost": 1, "ratio": 0.55, "cat": "Ranged", "row": 2, "col_idx": 2},
        {"id": "s9_melee", "name": "Level 9 Specialists Melee", "lead_cost": 1, "ratio": 0.55, "cat": "Melee", "row": 2, "col_idx": 3},
        {"id": "g8_flyer", "name": "Level 8 Guardians Flyer", "lead_cost": 20, "ratio": 1.00, "cat": "Flyer", "row": 3, "col_idx": 0},
        {"id": "g8_mounted", "name": "Level 8 Guardians Mounted", "lead_cost": 2, "ratio": 1.00, "cat": "Mounted", "row": 3, "col_idx": 1},
        {"id": "g8_ranged", "name": "Level 8 Guardians Ranged", "lead_cost": 1, "ratio": 1.00, "cat": "Ranged", "row": 3, "col_idx": 2},
        {"id": "g8_melee", "name": "Level 8 Guardians Melee", "lead_cost": 1, "ratio": 1.00, "cat": "Melee", "row": 3, "col_idx": 3},
        {"id": "s8_flyer", "name": "Level 8 Specialists Flyer", "lead_cost": 20, "ratio": 1.00, "cat": "Flyer", "row": 4, "col_idx": 0},
        {"id": "s8_mounted", "name": "Level 8 Specialists Mounted", "lead_cost": 2, "ratio": 1.00, "cat": "Mounted", "row": 4, "col_idx": 1},
        {"id": "s8_ranged", "name": "Level 8 Specialists Ranged", "lead_cost": 1, "ratio": 1.00, "cat": "Ranged", "row": 4, "col_idx": 2},
        {"id": "s8_melee", "name": "Level 8 Specialists Melee", "lead_cost": 1, "ratio": 1.00, "cat": "Melee", "row": 4, "col_idx": 3},
        {"id": "c9_engineer", "name": "Level 9 Engineer Corps", "lead_cost": 10, "ratio": 0.57, "cat": "Engineer Corps", "row": 5, "col_idx": 0},
        {"id": "c8_engineer", "name": "Level 8 Engineer Corps", "lead_cost": 10, "ratio": 1.03, "cat": "Engineer Corps", "row": 5, "col_idx": 1}
    ]

    # --- DATABASE COMPLETO MOSTRI ---
    database_mostri = [
        {"id": "m9_1", "name": "Level 9 Monster Type 1", "auth_cost": 53, "stacks": 4, "ratio": 0.1383, "lvl_group": "M9", "row": 6, "col_idx": 0},
        {"id": "m9_2", "name": "Level 9 Monster Type 2", "auth_cost": 53, "stacks": 4, "ratio": 0.1383, "lvl_group": "M9", "row": 6, "col_idx": 1},
        {"id": "m9_3", "name": "Level 9 Monster Type 3", "auth_cost": 53, "stacks": 4, "ratio": 0.1383, "lvl_group": "M9", "row": 6, "col_idx": 2},
        {"id": "m9_4", "name": "Level 9 Monster Type 4", "auth_cost": 53, "stacks": 4, "ratio": 0.1383, "lvl_group": "M9", "row": 6, "col_idx": 3},
        {"id": "m8_1", "name": "Level 8 Monster Type 1", "auth_cost": 53, "stacks": 4, "ratio": 0.2486, "lvl_group": "M8", "row": 7, "col_idx": 0},
        {"id": "m8_2", "name": "Level 8 Monster Type 2", "auth_cost": 53, "stacks": 4, "ratio": 0.2486, "lvl_group": "M8", "row": 7, "col_idx": 1},
        {"id": "m8_3", "name": "Level 8 Monster Type 3", "auth_cost": 53, "stacks": 4, "ratio": 0.2486, "lvl_group": "M8", "row": 7, "col_idx": 2},
        {"id": "m8_4", "name": "Level 8 Monster Type 4", "auth_cost": 53, "stacks": 4, "ratio": 0.2486, "lvl_group": "M8", "row": 7, "col_idx": 3},
        {"id": "m7_1", "name": "Level 7 Monster Type 1", "auth_cost": 43, "stacks": 2, "ratio": 0.4480, "lvl_group": "M7", "row": 8, "col_idx": 0},
        {"id": "m7_2", "name": "Level 7 Monster Type 2", "auth_cost": 43, "stacks": 2, "ratio": 0.4480, "lvl_group": "M7", "row": 8, "col_idx": 1},
        {"id": "m7_3", "name": "Level 7 Monster Type 3", "auth_cost": 43, "stacks": 2, "ratio": 0.4480, "lvl_group": "M7", "row": 8, "col_idx": 2},
        {"id": "m7_4", "name": "Level 7 Monster Type 4", "auth_cost": 43, "stacks": 2, "ratio": 0.4480, "lvl_group": "M7", "row": 8, "col_idx": 3}
    ]

    stati_checkbox = {}
    moltiplicatore_truppe = 0.0
    
    for cat in ["Flyer", "Mounted", "Ranged", "Melee", "Engineer Corps"]:
        st.markdown(f"**{cat}**")
        cols = st.columns(2)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat]
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 2]:
                nome_tradotto = ctx.get(truppa["name"], truppa["name"])
                attiva = st.checkbox(nome_tradotto, value=True, key=f"chk_unif_{truppa['id']}")
                stati_checkbox[truppa["id"]] = attiva
                if attiva:
                    moltiplicatore_truppe += truppa["ratio"]
        st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    st.markdown("**🛡️ Monsters Configuration**")
    c_m1, c_m2, c_m3 = st.columns(3)
    attiva_m9 = c_m1.checkbox("Include Level 9 Monsters (M9)", value=True, key="chk_unif_m9")
    attiva_m8 = c_m2.checkbox("Include Level 8 Monsters (M8)", value=True, key="chk_unif_m8")
    attiva_m7 = c_m3.checkbox("Include Level 7 Monsters (M7)", value=True, key="chk_unif_m7")
    
    stati_mostri = {"M9": attiva_m9, "M8": attiva_m8, "M7": attiva_m7}
    # --- 4. CALCOLO REATTIVO BACKGROUND DISTINTO (PARTE 2) ---
    stack_ref_lead = max_leadership / moltiplicatore_truppe if moltiplicatore_truppe > 0 else 0

    moltiplicatore_mostri = 0.0
    for m in database_mostri:
        if stati_mostri[m["lvl_group"]] and m["col_idx"] == 0:
            moltiplicatore_mostri += (m["stacks"] * m["ratio"])
            
    stack_ref_monsters = max_supremacy / moltiplicatore_mostri if moltiplicatore_mostri > 0 else 0

    # --- 5. GENERAZIONE OUTPUT IN GRIGLIA RIGIDA BLOCCATA ---
    if max_leadership > 0 or max_supremacy > 0:
        st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")
        
        totale_leadership_usata = 0
        totale_supremacy_usata = 0
        mappa_risultati = {}

        # Calcolo Truppe Regolari
        for truppa in database_truppe:
            if stati_checkbox.get(truppa["id"], False) and stack_ref_lead > 0:
                valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_ref_lead / 10) + 0.45
                count_truppe = int(valore_interno) * 10
                totale_leadership_usata += count_truppe * truppa["lead_cost"]
                count_formattato = f"{count_truppe:,}".replace(",", ".")
            else:
                count_formattato = "0"
            mappa_risultati[truppa["id"]] = {"name": ctx.get(truppa["name"], truppa["name"]), "count": count_formattato, "row": truppa["row"], "col_idx": truppa["col_idx"]}

        # Calcolo Mostri
        for mostro in database_mostri:
            if stati_mostri[mostro["lvl_group"]] and stack_ref_monsters > 0:
                # FORMULA DI MAURIZIO ORIGINALE IMMUTATA
                valore_interno = (mostro["ratio"] / mostro["auth_cost"] * stack_ref_monsters / 10) + 0.5
                count_mostri = int(valore_interno) * 10
                
                # CORREZIONE BUG: L'autorità del singolo quadratino della griglia è (Conteggio * Costo)
                # Il totale cumulativo si bilancia perfettamente senza quadruplicare le somme
                auth_singolo_mostro = count_mostri * mostro["auth_cost"]
                totale_supremacy_usata += auth_singolo_mostro
                
                count_formattato = f"{count_mostri:,}".replace(",", ".")
            else:
                count_formattato = "0"
            mappa_risultati[mostro["id"]] = {"name": mostro["name"], "count": count_formattato, "row": mostro["row"], "col_idx": mostro["col_idx"]}

        # Box riassuntivi delle risorse usate
        lead_usata_txt = f"{totale_leadership_usata:,}".replace(",", ".")
        lead_max_txt = f"{max_leadership:,}".replace(",", ".")
        sup_usata_txt = f"{totale_supremacy_usata:,}".replace(",", ".")
        sup_max_txt = f"{max_supremacy:,}".replace(",", ".")
        
        col_res1, col_res2 = st.columns(2)
        col_res1.markdown(f'<div class="chat-box" style="text-align:center;"><h3>Leadership Allocated</h3><p style="font-size:22px;color:#4a86e8;font-weight:bold;margin:0;">{lead_usata_txt} / {lead_max_txt}</p></div>', unsafe_allow_html=True)
        col_res2.markdown(f'<div class="chat-box" style="text-align:center;"><h3>Supremacy Allocated</h3><p style="font-size:22px;color:#bd9b53;font-weight:bold;margin:0;">{sup_usata_txt} / {sup_max_txt}</p></div>', unsafe_allow_html=True)

        # Labels per le righe fisse del tabellone completo
        labels_file = {
            1: "🛡️ Guardians Level 9", 2: "⚡ Specialists Level 9",
            3: "⚔️ Guardians Level 8", 4: "🔮 Specialists Level 8",
            5: "📐 Engineer Corps",
            6: "🐉 Monsters Level 9 (M9)", 7: "🦁 Monsters Level 8 (M8)", 8: "🦅 Monsters Level 7 (M7)"
        }

        # Stampa rigida delle 8 righe orizzontali fisse (Mostra 0 se disattivato)
        for r in range(1, 9):
            st.markdown(f"<small style='color:#bd9b53;font-weight:bold;'>{labels_file[r]}</small>", unsafe_allow_html=True)
            elementi_riga = [t for t in database_truppe if t["row"] == r] + [m for m in database_mostri if m["row"] == r]
            
            cols_griglia = st.columns(4)
            for item in elementi_riga:
                info = mappa_risultati[item["id"]]
                with cols_griglia[info["col_idx"]]:
                    st.markdown(f"""
                    <div class="chat-box" style="text-align: center; padding: 12px!important; min-height: 85px; display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 10px;">
                        <span style="color:#a69e8d; font-size:12px; font-weight:500; display: block; margin-bottom: 6px; line-height: 1.2;">{info['name']}</span>
                        <b style="color:#bd9b53; font-size:18px; display: block;">{info['count']}</b>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)
