import streamlit as st

def mostra_calcolatore_semplice(ctx):
    # Titolo e descrizioni UFC agganciati ai file delle lingue
    st.markdown(f"<h1>{ctx.get('calc_h1', '⚔️ Official Calculator for attacks on epic monsters.')}</h1>", unsafe_allow_html=True)
    st.write(ctx.get('simple_calc_main_subtitle', 'Enter your maximum leadership and customize your active troops.'))
    
    # --- NOTIFICA SUI CAPITANI SOTTO IL TITOLO ---
    st.markdown(f"""
    <div class="chat-box" style="padding:16px 20px!important; text-align:left; color:#f0e6d2; border-left:5px solid #cc4125!important; margin-bottom:20px; background: rgba(255, 255, 255, 0.02); width:100%;">
        <b style="color:#cc4125; font-size:15px; letter-spacing:0.5px; display:block; margin-bottom:6px;">{ctx.get('calc_note_title', '⚠️ IMPORTANT CAPTAIN NOTE:')}</b>
        <span style="font-size:13.5px; color:#e1d7c6; line-height:1.5; font-weight:400; display:block;">
            {ctx.get('calc_note_text', 'This calculator assumes you are using standard captains. If you use captains that grant specific health bonuses to a single troop or monster type, the distribution formula will not balance correctly.')}
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- INPUT AFFIANCATI ---
    c1, c2 = st.columns(2)
    max_leadership = c1.number_input(
        ctx.get('calc_max_leadership_lbl', 'Maximum Leadership:'),
        min_value=0, value=0, step=1000, format="%d", key="sc_max_lead_v2026_final"
    )
    max_supremacy = c2.number_input(
        ctx.get('calc_max_supremacy_lbl', 'Maximum Supremacy:'),
        min_value=0, value=0, step=1000, format="%d", key="sc_max_sup_v2026_final"
    )

    # --- BOX DI CONFERMA VISIVA AUTOBILANCIATO ---
    if max_leadership > 0 or max_supremacy > 0:
        lead_txt = f"{max_leadership:,}".replace(",", ".")
        sup_txt = f"{max_supremacy:,}".replace(",", ".")
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; max-width: 500px; margin: 10px auto 25px auto; padding: 8px !important; border: 1px solid #bd9b53; background: rgba(189, 155, 83, 0.05); border-radius: 4px; text-align: center;">
            <div><span style="font-size: 11px; color: #bd9b53; font-weight: bold;">{ctx.get('calc_confirmed_lead', 'CONFIRMED LEADERSHIP')}</span><p style="font-size: 20px; font-weight: bold; color: #f0e6d2; margin: 0; font-family: 'Cinzel', serif;">{lead_txt}</p></div>
            <div><span style="font-size: 11px; color: #bd9b53; font-weight: bold;">{ctx.get('calc_confirmed_sup', 'CONFIRMED SUPREMACY')}</span><p style="font-size: 20px; font-weight: bold; color: #bd9b53; margin: 0; font-family: 'Cinzel', serif;">{sup_txt}</p></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        testo_notifica = ctx.get('calc_no_troops_allocated', 'Please enter your Maximum Leadership or Maximum Supremacy value to calculate the troop stack distribution.')
        st.markdown(f'<div class="chat-box" style="padding:15px!important; text-align:center; color:#a69e8d; border-left:4px solid #bd9b53!important; margin-bottom:20px;">{testo_notifica}</div>', unsafe_allow_html=True)

    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops and Monsters to Include in March')}")

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

    # Database Mostri
    database_mostri = [
        {"id": "m9_group", "name": "Level 9 Monsters", "auth_cost": 55, "stacks": 4, "ratio": 0.1383, "lvl_group": "M9", "col_idx": 0},
        {"id": "m8_group", "name": "Level 8 Monsters", "auth_cost": 55, "stacks": 4, "ratio": 0.2486, "lvl_group": "M8", "col_idx": 1},
        {"id": "m7_group", "name": "Level 7 Monsters", "auth_cost": 43, "stacks": 2, "ratio": 0.4480, "lvl_group": "M7", "col_idx": 2}
    ]

    stati_checkbox = {}
    moltiplicatore_truppe = 0.0
    
    # RIPRISTINO RIGIDO DEI TITOLI ORIGINALI SENZA ALCUNA CHIAVE DEI GRAFICI SBALIATA
    mappa_titoli_categories = {
        "Flyer": "Flyer",
        "Mounted": "Mounted",
        "Ranged": "Ranged",
        "Melee": "Melee",
        "Engineer Corps": "Engineer Corps"
    }
    
    for cat in ["Flyer", "Mounted", "Ranged", "Melee", "Engineer Corps"]:
        st.markdown(f"**{mappa_titoli_categories[cat]}**")
        cols = st.columns(2)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat]
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 2]:
                nome_tradotto = ctx.get(truppa["name"], truppa["name"])
                attiva = st.checkbox(nome_tradotto, value=True, key=f"chk_unif_{truppa['id']}_v7")
                stati_checkbox[truppa["id"]] = attiva
                if attiva:
                    moltiplicatore_truppe += truppa["ratio"]
        st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    st.markdown(f"**{ctx.get('calc_monsters_config_title', '🛡️ Monsters Configuration')}**")
    c_m1, c_m2, c_m3 = st.columns(3)
    attiva_m9 = c_m1.checkbox(ctx.get("Include Level 9 Monsters (M9)", "Include Level 9 Monsters (M9)"), value=True, key="chk_unif_m9_v7")
    attiva_m8 = c_m2.checkbox(ctx.get("Include Level 8 Monsters (M8)", "Include Level 8 Monsters (M8)"), value=True, key="chk_unif_m8_v7")
    attiva_m7 = c_m3.checkbox(ctx.get("Include Level 7 Monsters (M7)", "Include Level 7 Monsters (M7)"), value=True, key="chk_unif_m7_v7")
    
    stati_mostri = {"M9": attiva_m9, "M8": attiva_m8, "M7": attiva_m7}
    # --- 4. CALCOLO REATTIVO BACKGROUND DISTINTO (PARTE 2) ---
    stack_ref_lead = max_leadership / moltiplicatore_truppe if moltiplicatore_truppe > 0 else 0

    moltiplicatore_mostri = 0.0
    for m in database_mostri:
        if stati_mostri[m["lvl_group"]]:
            moltiplicatore_mostri += (m["stacks"] * m["ratio"])
            
    stack_ref_monsters = max_supremacy / moltiplicatore_mostri if moltiplicatore_mostri > 0 else 0

    # --- 5. GENERAZIONE OUTPUT IN GRIGLIA RIGIDA BLOCCATA ---
    if max_leadership > 0 or max_supremacy > 0:
        st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")
        
        totale_leadership_usata = 0
        totale_supremacy_usata = 0
        mappa_risultati = {}
        mappa_mostri_risultati = {}

        # Calcolo Truppe Regolari (Griglia Rigida 4 Colonne)
        for truppa in database_truppe:
            if stati_checkbox.get(truppa["id"], False) and stack_ref_lead > 0:
                valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_ref_lead / 10) + 0.45
                count_truppe = int(valore_interno) * 10
                totale_leadership_usata += count_truppe * truppa["lead_cost"]
                count_formattato = f"{count_truppe:,}".replace(",", ".")
            else:
                count_formattato = "0"
            mappa_risultati[truppa["id"]] = {"name": ctx.get(truppa["name"], truppa["name"]), "count": count_formattato, "col_idx": truppa["col_idx"]}

        # ALGORITMO DI RICALIBRAZIONE MILLESIMALE ANTI-SFORO PER I MOSTRI
        safety_loop_counter = 0
        while safety_loop_counter < 100:
            test_supremacy_totale = 0
            for mostro in database_mostri:
                if stati_mostri[mostro["lvl_group"]] and stack_ref_monsters > 0:
                    valore_interno = (mostro["ratio"] / mostro["auth_cost"] * stack_ref_monsters / 10) + 0.5
                    count_test = int(valore_interno) * 10
                    test_supremacy_totale += (count_test * mostro["stacks"] * mostro["auth_cost"])
            
            if test_supremacy_totale <= max_supremacy or stack_ref_monsters <= 0:
                break
            
            stack_ref_monsters *= 0.999
            safety_loop_counter += 1

        # Applicazione definitiva dei conteggi mostri calibrati
        for mostro in database_mostri:
            if stati_mostri[mostro["lvl_group"]] and stack_ref_monsters > 0:
                valore_interno = (mostro["ratio"] / mostro["auth_cost"] * stack_ref_monsters / 10) + 0.5
                count_mostri = int(valore_interno) * 10
                totale_supremacy_usata += (count_mostri * mostro["stacks"] * mostro["auth_cost"])
                count_formattato = f"{count_mostri:,}".replace(",", ".")
            else:
                count_formattato = "0"
            mappa_mostri_risultati[mostro["id"]] = {"name": ctx.get(mostro["name"], mostro["name"]), "count": count_formattato, "col_idx": mostro["col_idx"]}

        # Box riassuntivi delle risorse usate tradotti
        lead_usata_txt = f"{totale_leadership_usata:,}".replace(",", ".")
        lead_max_txt = f"{max_leadership:,}".replace(",", ".")
        sup_usata_txt = f"{totale_supremacy_usata:,}".replace(",", ".")
        sup_max_txt = f"{max_supremacy:,}".replace(",", ".")
        
        col_res1, col_res2 = st.columns(2)
        col_res1.markdown(f'<div class="chat-box" style="text-align:center;"><h3>{ctx.get("calc_total_used_lead_lbl", "Leadership Allocated")}</h3><p style="font-size:22px;color:#4a86e8;font-weight:bold;margin:0;">{lead_usata_txt} / {lead_max_txt}</p></div>', unsafe_allow_html=True)
        col_res2.markdown(f'<div class="chat-box" style="text-align:center;"><h3>{ctx.get("calc_total_used_sup_lbl", "Supremacy Allocated")}</h3><p style="font-size:22px;color:#bd9b53;font-weight:bold;margin:0;">{sup_usata_txt} / {sup_max_txt}</p></div>', unsafe_allow_html=True)

        labels_file = {
            1: ctx.get("Level 9 Guardians", "🛡️ Guardians Level 9"), 
            2: ctx.get("Level 9 Specialists", "⚡ Specialists Level 9"),
            3: ctx.get("Level 8 Guardians", "⚔️ Guardians Level 8"), 
            4: ctx.get("Level 8 Specialists", "🔮 Specialists Level 8"),
            5: ctx.get("Level 9 Engineer Corps", "📐 Engineer Corps")
        }

        # Stampa delle prime 5 file rigide (Truppe Regolari a 4 colonne)
        for r in range(1, 6):
            st.markdown(f"<small style='color:#bd9b53;font-weight:bold;'>{labels_file[r]}</small>", unsafe_allow_html=True)
            truppe_riga = [t for t in database_truppe if t["row"] == r]
            
            cols_griglia = st.columns(4)
            for item in truppe_riga:
                info = mappa_risultati[item["id"]]
                with cols_griglia[info["col_idx"]]:
                    st.markdown(f"""
                    <div class="chat-box" style="text-align: center; padding: 12px!important; min-height: 85px; display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 10px;">
                        <span style="color:#a69e8d; font-size:12px; font-weight:500; display: block; margin-bottom: 6px; line-height: 1.2;">{info['name']}</span>
                        <b style="color:#bd9b53; font-size:18px; display: block;">{info['count']}</b>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)

        # --- STAMPA DI TUTTI I MOSTRI ACCORPATI IN UN'UNICA RIGA ORIZZONTALE A 4 COLONNE ---
        st.markdown("<hr style='margin: 15px 0; opacity: 0.15;'>", unsafe_allow_html=True)
        st.markdown(f"<small style='color:#bd9b53;font-weight:bold;'>{ctx.get('Level 9 Monsters Row', '🐉 Tactical Monsters')}</small>", unsafe_allow_html=True)
        
        cols_mostri = st.columns(4)
        for mostro in database_mostri:
            info_m = mappa_mostri_risultati[mostro["id"]]
            with cols_mostri[mostro["col_idx"]]:
                st.markdown(f"""
                <div class="chat-box" style="text-align: center; padding: 12px!important; min-height: 85px; display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 10px;">
                    <span style="color:#a69e8d; font-size:12px; font-weight:500; display: block; margin-bottom: 6px; line-height: 1.2;">{info_m['name']}</span>
                    <b style="color:#bd9b53; font-size:18px; display: block;">{info_m['count']}</b>
                </div>
                """, unsafe_allow_html=True)
