    # --- 4. CALCOLO REATTIVO BACKGROUND ---
    stack_ref_lead = max_leadership / moltiplicatore_truppe if moltiplicatore_truppe > 0 else 0

    # --- 5. GENERAZIONE OUTPUT ---
    if max_leadership > 0 or max_supremacy > 0:
        st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")
        
        totale_leadership_usata = 0
        totale_supremacy_usata = 0
        mappa_risultati = {}
        mappa_mostri_risultati = {}

        # 1. Calcolo delle Truppe Regolari (Invariato)
        for truppa in database_truppe:
            if stati_checkbox.get(truppa["id"], False) and stack_ref_lead > 0:
                valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_ref_lead / 10) + 0.45
                count_truppe = int(valore_interno) * 10
                totale_leadership_usata += count_truppe * truppa["lead_cost"]
                count_formattato = f"{count_truppe:,}".replace(",", ".")
            else:
                count_formattato = "0"
            mappa_risultati[truppa["id"]] = {"name": ctx.get(truppa["name"], truppa["name"]), "count": count_formattato, "col_idx": truppa["col_idx"], "row": truppa["row"]}

        # 2. ⚔️ ALGORITMO DI CALCOLO STRUTTURATO SULLA PROPORZIONE DI SALUTE (HP RATIO)
        # Costo autorità fisso dei singoli mostri ricavato dalla tua tabella Excel (53, 53, 43)
        costo_m9 = 53
        costo_m8 = 53
        costo_m7 = 43

        # Impostiamo le proporzioni rigide della salute (M9 = 1X, M8 = 2X, M7 = 4X)
        peso_m9 = 1.0 if attiva_m9 else 0.0
        peso_m8 = 2.0 if attiva_m8 else 0.0
        peso_m7 = 4.0 if attiva_m7 else 0.0

        # Calcolo del costo proporzionale reale per slot
        costo_combinato_hp = (peso_m9 * costo_m9) + (peso_m8 * costo_m8) + (peso_m7 * costo_m7)

        if costo_combinato_hp > 0 and max_supremacy > 0:
            # Calcoliamo il coefficiente moltiplicatore partendo dalla tua Supremazia Massima
            unita_base_x = max_supremacy / costo_combinato_hp
            
            # Calcoliamo la quantità esatta da inserire all'interno di ogni casella (slot) del gioco
            m9_slot = int((unita_base_x * peso_m9) / 10) * 10
            m8_slot = int((unita_base_x * peso_m8) / 10) * 10
            m7_slot = int((unita_base_x * peso_m7) / 10) * 10

            # CORREZIONE RIGIDA: La Supremazia usata in gioco corrisponde a (mostri per slot) * (costo autorità)
            totale_supremacy_usata = (m9_slot * costo_m9) + (m8_slot * costo_m8) + (m7_slot * costo_m7)

            # Se a causa degli arrotondamenti per decine si supera la capienza, effettuiamo una correzione di sicurezza
            while totale_supremacy_usata > max_supremacy:
                if m7_slot >= 10: m7_slot -= 10
                elif m8_slot >= 10: m8_slot -= 10
                elif m9_slot >= 10: m9_slot -= 10
                else: break
                totale_supremacy_usata = (m9_slot * costo_m9) + (m8_slot * costo_m8) + (m7_slot * costo_m7)
        else:
            m9_slot, m8_slot, m7_slot = 0, 0, 0

        # Mappatura dei risultati per la griglia dell'interfaccia
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
    # --- 4. CALCOLO REATTIVO BACKGROUND ---
    stack_ref_lead = max_leadership / moltiplicatore_truppe if moltiplicatore_truppe > 0 else 0

    # --- 5. GENERAZIONE OUTPUT ---
    if max_leadership > 0 or max_supremacy > 0:
        st.markdown(f"### 📋 {ctx.get('calc_results_h3', 'Calculated March Distribution')}")
        
        totale_leadership_usata = 0
        totale_supremacy_usata = 0
        mappa_risultati = {}
        mappa_mostri_risultati = {}

        # 1. Calcolo delle Truppe Regolari (Invariato)
        for truppa in database_truppe:
            if stati_checkbox.get(truppa["id"], False) and stack_ref_lead > 0:
                valore_interno = (truppa["ratio"] / truppa["lead_cost"] * stack_ref_lead / 10) + 0.45
                count_truppe = int(valore_interno) * 10
                totale_leadership_usata += count_truppe * truppa["lead_cost"]
                count_formattato = f"{count_truppe:,}".replace(",", ".")
            else:
                count_formattato = "0"
            mappa_risultati[truppa["id"]] = {"name": ctx.get(truppa["name"], truppa["name"]), "count": count_formattato, "col_idx": truppa["col_idx"], "row": truppa["row"]}

        # 2. ⚔️ ALGORITMO DI CALCOLO STRUTTURATO SULLA PROPORZIONE DI SALUTE (HP RATIO)
        # Costo autorità fisso dei singoli mostri ricavato dalla tua tabella Excel (53, 53, 43)
        costo_m9 = 53
        costo_m8 = 53
        costo_m7 = 43

        # Impostiamo le proporzioni rigide della salute (M9 = 1X, M8 = 2X, M7 = 4X)
        peso_m9 = 1.0 if attiva_m9 else 0.0
        peso_m8 = 2.0 if attiva_m8 else 0.0
        peso_m7 = 4.0 if attiva_m7 else 0.0

        # Calcolo del costo proporzionale reale per slot
        costo_combinato_hp = (peso_m9 * costo_m9) + (peso_m8 * costo_m8) + (peso_m7 * costo_m7)

        if costo_combinato_hp > 0 and max_supremacy > 0:
            # Calcoliamo il coefficiente moltiplicatore partendo dalla tua Supremazia Massima
            unita_base_x = max_supremacy / costo_combinato_hp
            
            # Calcoliamo la quantità esatta da inserire all'interno di ogni casella (slot) del gioco
            m9_slot = int((unita_base_x * peso_m9) / 10) * 10
            m8_slot = int((unita_base_x * peso_m8) / 10) * 10
            m7_slot = int((unita_base_x * peso_m7) / 10) * 10

            # CORREZIONE RIGIDA: La Supremazia usata in gioco corrisponde a (mostri per slot) * (costo autorità)
            totale_supremacy_usata = (m9_slot * costo_m9) + (m8_slot * costo_m8) + (m7_slot * costo_m7)

            # Se a causa degli arrotondamenti per decine si supera la capienza, effettuiamo una correzione di sicurezza
            while totale_supremacy_usata > max_supremacy:
                if m7_slot >= 10: m7_slot -= 10
                elif m8_slot >= 10: m8_slot -= 10
                elif m9_slot >= 10: m9_slot -= 10
                else: break
                totale_supremacy_usata = (m9_slot * costo_m9) + (m8_slot * costo_m8) + (m7_slot * costo_m7)
        else:
            m9_slot, m8_slot, m7_slot = 0, 0, 0

        # Mappatura dei risultati per la griglia dell'interfaccia
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
