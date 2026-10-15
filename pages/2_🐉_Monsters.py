import streamlit as st

def mostra_monsters(ctx=None):
    if ctx is None:
        ctx = {}
        
    st.markdown(f"<h1>{ctx.get('simple_calc_monsters_h1', '🐉 Tactical Monsters Calculator')}</h1>", unsafe_allow_html=True)
    
    # --- NOTIFICA SUI CAPITANI PERSONALIZZATA ---
    st.markdown(f"""
    <div class="chat-box" style="padding:16px 20px!important; text-align:left; color:#f0e6d2; border-left:5px solid #cc4125!important; margin-bottom:20px; background: rgba(255, 255, 255, 0.02); width:100%;">
        <b style="color:#cc4125; font-size:15px; letter-spacing:0.5px; display:block; margin-bottom:6px;">⚠️ IMPORTANT CAPTAIN NOTE:</b>
        <span style="font-size:13.5px; color:#e1d7c6; line-height:1.5; font-weight:400; display:block;">
            This calculator assumes you are using standard captains. If you use captains that grant specific health bonuses to a single monster type, the distribution formula will not balance correctly.
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- 1. CONFIGURAZIONE INPUT AGGIORNATO CON LA SUPREMAZIA ---
    max_supremacy = st.number_input(
        "Maximum Supremacy:",
        min_value=0, value=0, step=1000, key="monster_max_sup_v1"
    )

    # --- BOX DI CONFERMA VISIVA DELLA SUPREMAZIA ---
    if max_supremacy > 0:
        sup_txt = f"{max_supremacy:,}".replace(",", ".")
        st.markdown(f"""
        <div style="text-align: center; max-width: 400px; margin: 10px auto 25px auto; padding: 8px !important; border: 1px solid #bd9b53; background: rgba(189, 155, 83, 0.05); border-radius: 4px;">
            <span style="font-size: 11px; color: #bd9b53; font-weight: bold; letter-spacing: 0.5px; display: block; margin-bottom: 2px;">CONFIRMED MAXIMUM SUPREMACY</span>
            <p style="font-size: 24px; font-weight: bold; color: #f0e6d2; margin: 0; font-family: 'Cinzel', serif;">{sup_txt}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-box" style="padding:15px!important; text-align:center; color:#a69e8d; border-left:4px solid #bd9b53!important; margin-bottom:20px;">
            Please enter your Maximum Supremacy value to calculate the monster distribution.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🐉 Monsters Configuration")
    
    # --- SELEZIONE MOSTRI A GRUPPI DI LIVELLO ---
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        attiva_m9 = st.checkbox("Include Level 9 Monsters (M9)", value=True, key="chk_page_m9_v3")
    with c_m2:
        attiva_m8 = st.checkbox("Include Level 8 Monsters (M8)", value=True, key="chk_page_m8_v3")
    with c_m3:
        attiva_m7 = st.checkbox("Include Level 7 Monsters (M7)", value=True, key="chk_page_m7_v3")

    stati_mostri_livello = {"M9": attiva_m9, "M8": attiva_m8, "M7": attiva_m7}

    # --- 2. DATABASE ORIGINALE DEI MOSTRI CON I PARAMETRI ESATTI DI MAURIZIO ---
    database_mostri = [
        # --- FILA 1: MOSTRI LIVELLO 9 ---
        {"id": "m9_1", "name": "Level 9 Monster Type 1", "auth_cost": 53, "stacks": 4, "ratio": 0.1383, "lvl_group": "M9", "col_idx": 0},
        {"id": "m9_2", "name": "Level 9 Monster Type 2", "auth_cost": 53, "stacks": 4, "ratio": 0.1383, "lvl_group": "M9", "col_idx": 1},
        {"id": "m9_3", "name": "Level 9 Monster Type 3", "auth_cost": 53, "stacks": 4, "ratio": 0.1383, "lvl_group": "M9", "col_idx": 2},
        {"id": "m9_4", "name": "Level 9 Monster Type 4", "auth_cost": 53, "stacks": 4, "ratio": 0.1383, "lvl_group": "M9", "col_idx": 3},

        # --- FILA 2: MOSTRI LIVELLO 8 ---
        {"id": "m8_1", "name": "Level 8 Monster Type 1", "auth_cost": 53, "stacks": 4, "ratio": 0.2486, "lvl_group": "M8", "col_idx": 0},
        {"id": "m8_2", "name": "Level 8 Monster Type 2", "auth_cost": 53, "stacks": 4, "ratio": 0.2486, "lvl_group": "M8", "col_idx": 1},
        {"id": "m8_3", "name": "Level 8 Monster Type 3", "auth_cost": 53, "stacks": 4, "ratio": 0.2486, "lvl_group": "M8", "col_idx": 2},
        {"id": "m8_4", "name": "Level 8 Monster Type 4", "auth_cost": 53, "stacks": 4, "ratio": 0.2486, "lvl_group": "M8", "col_idx": 3},

        # --- FILA 3: MOSTRI LIVELLO 7 ---
        {"id": "m7_1", "name": "Level 7 Monster Type 1", "auth_cost": 43, "stacks": 2, "ratio": 0.4480, "lvl_group": "M7", "col_idx": 0},
        {"id": "m7_2", "name": "Level 7 Monster Type 2", "auth_cost": 43, "stacks": 2, "ratio": 0.4480, "lvl_group": "M7", "col_idx": 1},
        {"id": "m7_3", "name": "Level 7 Monster Type 3", "auth_cost": 43, "stacks": 2, "ratio": 0.4480, "lvl_group": "M7", "col_idx": 2},
        {"id": "m7_4", "name": "Level 7 Monster Type 4", "auth_cost": 43, "stacks": 2, "ratio": 0.4480, "lvl_group": "M7", "col_idx": 3}
    ]

    # --- CALCOLO DEL MOLTIPLIPLICATORE DINAMICO BASATO SULLA SUPREMAZIA ---
    moltiplicatore_mostri = 0.0
    for mostro in database_mostri:
        if stati_mostri_livello[mostro["lvl_group"]] and mostro["col_idx"] == 0:
            moltiplicatore_mostri += (mostro["stacks"] * mostro["ratio"])

    # Il Riferimento Stack (J19) si calcola dinamicamente partendo dalla Supremazia inserita
    stack_reference = max_supremacy / moltiplicatore_mostri if moltiplicatore_mostri > 0 else 0

    # --- GENERAZIONE OUTPUT DEI MOSTRI ---
    if max_supremacy > 0 and stack_reference > 0:
        st.markdown(f"### 📋 Calculated Monster Distribution")
        
        totale_supremacy_usata = 0
        mappa_risultati = {}

        for mostro in database_mostri:
            is_attivo = stati_mostri_livello[mostro["lvl_group"]]
            
            if is_attivo:
                # FORMULA DI MAURIZIO CORRETTA SULLA SUPREMAZIA:
                valore_interno = (mostro["ratio"] / mostro["auth_cost"] * stack_reference / 10) + 0.5
                count_mostri = int(valore_interno) * 10
                
                # Supremazia totale spesa dalla riga = Soldati * Numero Stack * Costo Spazio
                sup_riga = count_mostri * mostro["stacks"] * mostro["auth_cost"]
                totale_supremacy_usata += sup_riga
                count_formattato = f"{count_mostri:,}".replace(",", ".")
            else:
                count_formattato = "0"

            mappa_risultati[mostro["id"]] = {
                "name": mostro["name"],
                "count": count_formattato
            }

        # Monitor della Supremazia totale spesa
        sup_usata_txt = f"{totale_supremacy_usata:,}".replace(",", ".")
        sup_max_txt = f"{max_supremacy:,}".replace(",", ".")
        st.markdown(f'<div class="chat-box" style="text-align:center; max-width: 400px; margin: 0 auto 20px auto;"><h3>Total Supremacy Allocated</h3><p style="font-size:24px;color:#4a86e8;font-weight:bold;margin:0;">{sup_usata_txt} / {sup_max_txt}</p></div>', unsafe_allow_html=True)

        # --- DISEGNO RIGIDO DELLE 3 FILE DI MOSTRI A 4 COLONNE NATIVE ---
        mostri_ordinati = [
            ["m9_1", "m9_2", "m9_3", "m9_4"],  # Fila 1: Mostri 9
            ["m8_1", "m8_2", "m8_3", "m8_4"],  # Fila 2: Mostri 8
            ["m7_1", "m7_2", "m7_3", "m7_4"]   # Fila 3: Mostri 7
        ]

        labels_file = {
            0: "🐉 Monsters Level 9 (M9)",
            1: "🦁 Monsters Level 8 (M8)",
            2: "🦅 Monsters Level 7 (M7)"
        }

        for idx_riga, m_ids in enumerate(mostri_ordinati):
            st.markdown(f"<small style='color:#bd9b53;font-weight:bold;'>{labels_file[idx_riga]}</small>", unsafe_allow_html=True)
            cols_griglia = st.columns(4)
            
            for idx_col, m_id in enumerate(m_ids):
                info = mappa_risultati[m_id]
                with cols_griglia[idx_col]:
                    st.markdown(f"""
                    <div class="chat-box" style="text-align: center; padding: 12px!important; min-height: 85px; display: flex; flex-direction: column; justify-content: center; align-items: center; margin-bottom: 10px;">
                        <span style="color:#a69e8d; font-size:12px; font-weight:500; display: block; margin-bottom: 6px; line-height: 1.2;">{info['name']}</span>
                        <b style="color:#bd9b53; font-size:18px; display: block;">{info['count']}</b>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom: 5px;'></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    mostra_monsters()

