import streamlit as st

def mostra_calcolatore_semplice(ctx):
    # Titolo e descrizioni UFC
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
        min_value=0, value=332000, step=1000, format="%d", key="sc_max_lead_v2026_final"
    )
    max_supremacy = c2.number_input(
        ctx.get('calc_max_supremacy_lbl', 'Maximum Supremacy:'),
        min_value=0, value=223000, step=1000, format="%d", key="sc_max_sup_v2026_final"
    )

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

    stati_checkbox = {}
    moltiplicatore_truppe = 0.0
    
    mappa_titoli_categorie = {
        "Flyer": f"🛡️ {ctx.get('Level 9 Guardians Flyer', 'Flyer').replace('Liv.9 Guardiani ', '')}",
        "Mounted": f"⚡ {ctx.get('Level 9 Guardians Mounted', 'Mounted').replace('Liv.9 Guardiani ', '')}",
        "Ranged": f"⚔️ {ctx.get('Level 9 Guardians Ranged', 'Ranged').replace('Liv.9 Guardiani ', '')}",
        "Melee": f"🔮 {ctx.get('Level 9 Guardians Melee', 'Melee').replace('Liv.9 Guardiani ', '')}",
        "Engineer Corps": f"📐 {ctx.get('menu_calc', 'Engineer Corps').replace('⚔️ ', '').replace('Calcolatore Truppe', 'Corpo Genieri')}"
    }
    
    for cat in ["Flyer", "Mounted", "Ranged", "Melee", "Engineer Corps"]:
        st.markdown(f"**{mappa_titoli_categorie[cat]}**")
        cols = st.columns(2)
        truppe_in_cat = [t for t in database_truppe if t["cat"] == cat]
        for idx, truppa in enumerate(truppe_in_cat):
            with cols[idx % 2]:
                nome_tradotto = ctx.get(truppa["name"], truppa["name"])
                attiva = st.checkbox(nome_tradotto, value=True, key=f"chk_unif_{truppa['id']}_v5")
                stati_checkbox[truppa["id"]] = attiva
                if attiva:
                    moltiplicatore_truppe += truppa["ratio"]
        st.markdown("<hr style='margin: 5px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    st.markdown(f"**{ctx.get('calc_monsters_config_title', '🛡️ Monsters Configuration')}**")
    c_m1, c_m2, c_m3 = st.columns(3)
    attiva_m9 = c_m1.checkbox(ctx.get("Include Level 9 Monsters (M9)", "Include Level 9 Monsters (M9)"), value=True, key="chk_unif_m9_v5")
    attiva_m8 = c_m2.checkbox(ctx.get("Include Level 8 Monsters (M8)", "Include Level 8 Monsters (M8)"), value=True, key="chk_unif_m8_v5")
    attiva_m7 = c_m3.checkbox(ctx.get("Include Level 7 Monsters (M7)", "Include Level 7 Monsters (M7)"), value=True, key="chk_unif_m7_v5")
    # --- CALCOLO REATTIVO BACKGROUND DISTINTO STRUTTURATO SULLA SUPREMAZIA ---
    stack_ref_lead = max_leadership / moltiplicatore_truppe if moltiplicatore_truppe > 0 else 0

    if max_leadership > 0 or max_supremacy > 0:
        st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")
        
        totale_leadership_usata = 0
        totale_supremacy_usata = 0
        mappa_risultati = {}
        mappa_mostri_risultati = {}

        # 1. Calcolo delle Truppe Regolari
        for truppa in database_truppe:
            if stati_checkbox.get(truppa["id"], False) and stack_ref_lead > 0:
                valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_ref_lead / 10) + 0.45
                count_truppe = int(valore_interno) * 10
                totale_leadership_usata += count_truppe * truppa["lead_cost"]
                count_formattato = f"{count_truppe:,}".replace(",", ".")
            else:
                count_formattato = "0"
            mappa_risultati[truppa["id"]] = {"name": ctx.get(truppa["name"], truppa["name"]), "count": count_formattato, "col_idx": truppa["col_idx"], "row": truppa["row"]}

        # 2. Algoritmo di saturazione basato sulla Supremazia e sulla proporzione della Salute
        costo_m9 = 53
        costo_m8 = 53
        costo_m7 = 43

        peso_m9 = 1.0 if attiva_m9 else 0.0
        peso_m8 = 2.0 if attiva_m8 else 0.0
        peso_m7 = 4.0 if attiva_m7 else 0.0

        costo_combinato_hp = (peso_m9 * costo_m9) + (peso_m8 * costo_m8) + (peso_m7 * costo_m7)

        if costo_combinato_hp > 0 and max_supremacy > 0:
            unita_base_x = max_supremacy / costo_combinato_hp
            
            m9_slot = int((unita_base_x * peso_m9) / 10) * 10
            m8_slot = int((unita_base_x * peso_m8) / 10) * 10
            m7_slot = int((unita_base_x * peso_m7) / 10) * 10

            totale_supremacy_usata = (m9_slot * costo_m9) + (m8_slot * costo_m8) + (m7_slot * costo_m7)

            while totale_supremacy_usata > max_supremacy:
                if m7_slot >= 10: m7_slot -= 10
                elif m8_slot >= 10: m8_slot -= 10
                elif m9_slot >= 10: m9_slot -= 10
                else: break
                totale_supremacy_usata = (m9_slot * costo_m9) + (m8_slot * costo_m8) + (m7_slot * costo_m7)
        else:
            m9_slot, m8_slot, m7_slot = 0, 0, 0

        mappa_mostri_risultati["m9_group"] = {"name": ctx.get("Level 9 Monsters", "Level 9 Monsters"), "count": f"{m9_slot}", "col_idx": 0}
        mappa_mostri_risultati["m8_group"] = {"name": ctx.get("Level 8 Monsters", "Level 8 Monsters"), "count": f"{m8_slot}", "col_idx": 1}
        mappa_mostri_risultati["m7_group"] = {"name": ctx.get("Level 7 Monsters", "Level 7 Monsters"), "count": f"{m7_slot}", "col_idx": 2}

        # Configurazione box riassuntivi finali
        lead_usata_txt = f"{totale_leadership_usata:,}".replace(",", ".")
        lead_max_txt = f"{max_leadership:,}".replace(",", ".")
        sup_usata_txt = f"{totale_supremacy_usata:,}".replace(",", ".")
        sup_max_txt = f"{max_supremacy:,}".replace(",", ".")
        
        col_res1, col_res2 = st.columns(2)
        col_res1.markdown(f'<div class="chat-box" style="text-align:center;"><h3>{ctx.get("calc_total_used_lead_lbl", "Leadership Allocated")}</h3><p style="font-size:22px;color:#4a86e8;font-weight:bold;margin:0;">{lead_usata_txt} / {lead_max_txt}</p></div>', unsafe_allow_html=True)
        col_res2.markdown(f'<div class="chat-box" style="text-align:center;"><h3>{ctx.get("calc_total_used_sup_lbl", "Supremacy Allocated")}</h3><p style="font-size:22px;color:#bd9b53;font-weight:bold;margin:0;">{sup_usata_txt} / {sup_max_txt}</p></div>', unsafe_allow_html=True)

        # Griglia Stampa Truppe
        labels_file = {
            1: ctx.get("Level 9 Guardians", "🛡️ Guardians Level 9"), 
            2: ctx.get("Level 9 Specialists", "⚡ Specialists Level 9"),
            3: ctx.get("Level 8 Guardians", "⚔️ Guardians Level 8"), 
            4: ctx.get("Level 8 Specialists", "🔮 Specialists Level 8"),
            5: ctx.get("Level 9 Engineer Corps", "📐 Engineer Corps")
        }

        for r in range(1, 6):
            st.markdown(f"<small style='color:#bd9b53;font-weight:bold;'>{labels_file[r]}</small>", unsafe_allow_html=True)
            truppe_riga = [mappa_risultati[t["id"]] for t in database_truppe if t["row"] == r]
            cols_griglia = st.columns(4)
            for item in truppe_riga:
                with cols_griglia[item["col_idx"]]:
                    st.markdown(f"""
                    <div class="chat-box" style="text-align: center; padding: 12px!important; min-height: 85px; display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 10px;">
                        <span style="color:#a69e8d; font-size:12px; font-weight:500; display: block; margin-bottom: 6px; line-height: 1.2;">{item['name']}</span>
                        <b style="color:#bd9b53; font-size:18px; display: block;">{item['count']}</b>
                    </div>
                    """, unsafe_allow_html=True)

        # Griglia Mostri
        st.markdown("<hr style='margin: 15px 0; opacity: 0.15;'>", unsafe_allow_html=True)
        st.markdown(f"<small style='color:#bd9b53;font-weight:bold;'>{ctx.get('Level 9 Monsters Row', '🐉 Tactical Monsters')}</small>", unsafe_allow_html=True)
        
        cols_mostri = st.columns(4)
        mostri_render = [
            mappa_mostri_risultati["m9_group"],
            mappa_mostri_risultati["m8_group"],
            mappa_mostri_risultati["m7_group"]
        ]
        for m_r in mostri_render:
            with cols_mostri[m_r["col_idx"]]:
                st.markdown(f"""
                <div class="chat-box" style="text-align: center; padding: 12px!important; min-height: 85px; display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 10px;">
                    <span style="color:#a69e8d; font-size:12px; font-weight:500; display: block; margin-bottom: 6px; line-height: 1.2;">{m_r['name']}</span>
                    <b style="color:#bd9b53; font-size:18px; display: block;">{m_r['count']}</b>
                </div>
                """, unsafe_allow_html=True)
