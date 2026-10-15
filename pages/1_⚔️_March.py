import streamlit as st

# Funzione per emulare il funzionamento del vecchio ctx (se non passa dal file principale)
def mostra_march(ctx=None):
    if ctx is None:
        ctx = {}
        
    st.markdown(f"<h1>{ctx.get('simple_calc_main_h1', '🧮 Tactical Army March Calculator')}</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- 1. INPUT LEADERSHIP MASSIMA ---
    max_leadership = st.number_input(
        ctx.get('calc_max_leadership_lbl', 'Maximum Leadership:'),
        min_value=0, value=0, step=1000, key="march_max_lead"
    )

    # --- BOX DI CONFERMA VISIVA GIGANTE CON I PUNTI DELLE MIGLIAIA ---
    if max_leadership > 0:
        lead_conferma_formattata = f"{max_leadership:,}".replace(",", ".")
        st.markdown(f"""
        <div style="text-align: center; max-width: 400px; margin: 10px auto 25px auto; padding: 8px !important; border: 1px solid #bd9b53; background: rgba(189, 155, 83, 0.05); border-radius: 4px;">
            <span style="font-size: 11px; color: #bd9b53; font-weight: bold; letter-spacing: 0.5px; display: block; margin-bottom: 2px;">CONFIRMED LEADERSHIP</span>
            <p style="font-size: 24px; font-weight: bold; color: #f0e6d2; margin: 0; font-family: 'Cinzel', serif;">{lead_conferma_formattata}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        testo_notifica = ctx.get('calc_no_troops_allocated', 'Please enter a Maximum Leadership value to calculate the troop stack distribution.')
        st.markdown(f"""
        <div class="chat-box" style="padding:15px!important; text-align:center; color:#a69e8d; border-left:4px solid #bd9b53!important; margin-bottom:20px;">
            {testo_notifica}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"### {ctx.get('calc_select_troops_title', '⚔️ Select Troops to Include in March')}")

    # --- 2. DATABASE INTEGRALE DELLE TRUPPE REGOLARI E SPECIALISTI T9/T8 ---
    database_truppe = [
        {"id": "g9_flyer", "name": "Level 9 Guardians Flyer", "lead_cost": 20, "stacks": 1, "ratio": 0.50, "cat": "Flyer"},
        {"id": "s9_flyer", "name": "Level 9 Specialists Flyer", "lead_cost": 20, "stacks": 1, "ratio": 0.50, "cat": "Flyer"},
        {"id": "g9_mounted", "name": "Level 9 Guardians Mounted", "lead_cost": 2, "stacks": 1, "ratio": 0.55, "cat": "Mounted"},
        {"id": "s9_mounted", "name": "Level 9 Specialists Mounted", "lead_cost": 2, "stacks": 1, "ratio": 0.55, "cat": "Mounted"},
        {"id": "g9_ranged", "name": "Level 9 Guardians Ranged", "lead_cost": 1, "stacks": 1, "ratio": 0.55, "cat": "Ranged"},
        {"id": "s9_ranged", "name": "Level 9 Specialists Ranged", "lead_cost": 1, "stacks": 1, "ratio": 0.55, "cat": "Ranged"},
        {"id": "g9_melee", "name": "Level 9 Guardians Melee", "lead_cost": 1, "stacks": 1, "ratio": 0.55, "cat": "Melee"},
        {"id": "s9_melee", "name": "Level 9 Specialists Melee", "lead_cost": 1, "stacks": 1, "ratio": 0.55, "cat": "Melee"},
        {"id": "c9_engineer", "name": "Level 9 Engineer Corps", "lead_cost": 10, "stacks": 1, "ratio": 0.57, "cat": "Engineer Corps"},

        {"id": "g8_flyer", "name": "Level 8 Guardians Flyer", "lead_cost": 20, "stacks": 1, "ratio": 1.00, "cat": "Flyer"},
        {"id": "s8_flyer", "name": "Level 8 Specialists Flyer", "lead_cost": 20, "stacks": 1, "ratio": 1.00, "cat": "Flyer"},
        {"id": "g8_mounted", "name": "Level 8 Guardians Mounted", "lead_cost": 2, "stacks": 1, "ratio": 1.00, "cat": "Mounted"},
        {"id": "s8_mounted", "name": "Level 8 Specialists Mounted", "lead_cost": 2, "stacks": 1, "ratio": 1.00, "cat": "Mounted"},
        {"id": "g8_ranged", "name": "Level 8 Guardians Ranged", "lead_cost": 1, "stacks": 1, "ratio": 1.00, "cat": "Ranged"},
        {"id": "s8_ranged", "name": "Level 8 Specialists Ranged", "lead_cost": 1, "stacks": 1, "ratio": 1.00, "cat": "Ranged"},
        {"id": "g8_melee", "name": "Level 8 Guardians Melee", "lead_cost": 1, "stacks": 1, "ratio": 1.00, "cat": "Melee"},
        {"id": "s8_melee", "name": "Level 8 Specialists Melee", "lead_cost": 1, "stacks": 1, "ratio": 1.00, "cat": "Melee"},
        {"id": "c8_engineer", "name": "Level 8 Engineer Corps", "lead_cost": 10, "stacks": 1, "ratio": 1.03, "cat": "Engineer Corps"}
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
                attiva = st.checkbox(nome_tradotto, value=True, key=f"march_chk_{truppa['id']}")
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
    if max_leadership > 0 and stack_reference > 0:
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
                "count": count_formattato
            }

        # Monitor centrale della leadership allocata
        lead_usata_formattata = f"{totale_leadership_usata:,}".replace(",", ".")
        lead_max_formattata = f"{max_leadership:,}".replace(",", ".")
        st.markdown(f'<div class="chat-box" style="text-align:center; max-width: 400px; margin: 0 auto 20px auto;"><h3>{ctx.get("calc_total_used_lead_lbl", "Total Leadership Allocated")}</h3><p style="font-size:24px;color:#4a86e8;font-weight:bold;margin:0;">{lead_usata_formattata} / {lead_max_formattata}</p></div>', unsafe_allow_html=True)

        # --- DISEGNO RIGIDO DEL TABELLONE A 4 COLONNE NATIVE ---
        truppe_ordinate = [
            ["g9_flyer", "g9_mounted", "g9_ranged", "g9_melee"],      # RIGA 1: Guardie 9
            ["s9_flyer", "s9_mounted", "s9_ranged", "s9_melee"],      # RIGA 2: Specialisti 9
            ["g8_flyer", "g8_mounted", "g8_ranged", "g8_melee"],      # RIGA 3: Guardie 8
            ["s8_flyer", "s8_mounted", "s8_ranged", "s8_melee"],      # RIGA 4: Specialisti 8
            ["c9_engineer", "c8_engineer"]                            # RIGA 5: Genieri
        ]

        labels_file = {
            0: "🛡️ Guardians Level 9",
            1: "⚡ Specialists Level 9",
            2: "⚔️ Guardians Level 8",
            3: "🔮 Specialists Level 8",
            4: "📐 Engineer Corps"
        }

        for idx_riga, riga_ids in enumerate(truppe_ordinate):
            st.markdown(f"<small style='color:#bd9b53;font-weight:bold;'>{labels_file[idx_riga]}</small>", unsafe_allow_html=True)
            cols_griglia = st.columns(4)
            
            for idx_col, t_id in enumerate(riga_ids):
                info = mappa_risultati[t_id]
                with cols_griglia[idx_col]:
                    st.markdown(f"""
                    <div class="chat-box" style="text-align: center; padding: 12px!important; min-height: 85px; display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 10px;">
                        <span style="color:#a69e8d; font-size:12px; font-weight:500; display: block; margin-bottom: 6px; line-height: 1.2;">{info['name']}</span>
                        <b style="color:#bd9b53; font-size:18px; display: block;">{info['count']}</b>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)

# Avvia la funzione se eseguito direttamente da Streamlit come pagina autonoma
if __name__ == "__main__":
    mostra_march()

