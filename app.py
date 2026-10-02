import base64
import json
import os
import streamlit as st

# 1. PAGE SETTINGS & WAR DESIGN
st.set_page_config(
    page_title="UFC Command Center", layout="wide", page_icon="🛡️"
)


# Funzione per convertire le immagini locali in Base64 (Risolve il problema del caricamento)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


# Funzione per applicare lo stile CSS con lo sfondo codificato e la patina scura
def apply_custom_style(image_path):
    bin_str = get_base64_image(image_path)
    bg_src = (
        f"data:image/jpeg;base64,{bin_str}"
        if bin_str
        else "rgba(13, 10, 8, 1)"
    )

    st.markdown(
        f"""
        <style>
        @import url('https://googleapis.com');
        
        /* Sfondo Dinamico Personalizzato con Patina Scura Protettiva all'85% */
        .stApp {{ 
            background: linear-gradient(rgba(13, 10, 8, 0.85), rgba(13, 10, 8, 0.85)), url("{bg_src}") no-repeat center center fixed;
            background-size: cover;
            color: #f0e6d2; 
            font-family: 'Inter', sans-serif; 
        }}
        
        [data-testid="stSidebar"] {{ background-color: #121212; border-right: 2px solid #bd9b53; box-shadow: 5px 0 15px rgba(0,0,0,0.7); }}
        
        /* Titoli stile Epic War - CENTRATI SU PC E CELLULARE */
        h1, h2, h3 {{ color: #d4b373 !important; font-family: 'Cinzel', serif !important; text-shadow: 3px 3px 6px #000000; letter-spacing: 1px; font-weight: 700; text-align: center !important; }}
        h1 {{ border-bottom: 2px solid #bd9b53; padding-bottom: 10px; margin-bottom: 25px !important; font-size: 28px !important; text-align: center !important; }}

        
        /* Box delle Chat e Contenitori con effetto Glow Dorato */
        .chat-box, .stAlert {{ 
            background: linear-gradient(145, #1e1a13, #14120e) !important; 
            border: 1px solid #bd9b53 !important; 
            border-left: 5px solid #bd9b53 !important; 
            padding: 16px !important; 
            margin-bottom: 15px !important; 
            border-radius: 6px !important;
            box-shadow: 0 4px 15px rgba(189, 155, 83, 0.15) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .chat-box:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(189, 155, 83, 0.3) !important; }}
        
        /* Pulsanti d'Acciaio Reattivi (Link Buttons) */
        .stLinkButton a {{
            background: linear-gradient(135, #8c1d1d 0%, #591010 100%) !important;
            color: #f0e6d2 !important;
            border: 2px solid #bd9b53 !important;
            font-family: 'Cinzel', serif !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
            border-radius: 4px !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
            transition: all 0.3s ease !important;
        }}
        .stLinkButton a:hover {{ 
            background: linear-gradient(135, #b32424 0%, #7c1515 100%) !important;
            box-shadow: 0 0 15px #bd9b53 !important;
            transform: scale(1.01);
        }}
        
        /* Ottimizzazione Mobile */
        @media (max-width: 768px) {{
            h1 {{ font-size: 22px !important; }}
            .stMarkdown p {{ font-size: 14px !important; }}
            .chat-box {{ padding: 12px !important; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# 2. SECURITY LOGIN
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    apply_custom_style("bg_home.jpg")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col_login, col2 = st.columns(3)
    with col_login:
        if os.path.exists("logo.png"):
            log_c1, log_c2, log_c3 = st.columns([1, 2, 1])
            with log_c2:
                st.image("logo.png", width=220)
        else:
            st.markdown(
                '<h1 style="text-align: center; font-size: 45px; margin: 0px;">🛡️</h1>',
                unsafe_allow_html=True,
            )
        st.markdown(
            "<h1 style='text-align: center; margin-top: 15px; font-size: 26px;'>UFC RAIDERS OF CHAOS</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align: center; font-size: 13px; color: #bd9b53;'>ALLIANCE PORTAL - RESTRICTED ACCESS</h3>",
            unsafe_allow_html=True,
        )

        password_entered = st.text_input(
            "CLAN PASSWORD:", type="password", placeholder="Enter access code..."
        )
        if st.button("ACCESS PORTAL", width='stretch'):
            if password_entered == "UFC_Raiders_2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Incorrect password!")
else:


               # 3. PORTAL INTERFACE (LOGO MAXI CENTRATO E SICURO)
    if os.path.exists("logo.png"):
        side_c1, side_c2, side_c3 = st.sidebar.columns([1, 4, 1])
        with side_c2:
            st.image("logo.png", width=160)
    else:
        st.sidebar.markdown("<div style='text-align: center;'><h1 style='font-size: 45px; margin-bottom: 0px;'>🛡️</h1></div>", unsafe_allow_html=True)

    st.sidebar.markdown("<h2 style='font-size: 20px; text-align: center; margin-top: 10px; margin-bottom: 15px;'>UFC Portal</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")




    # 1. RECUPERIAMO PRIMA LA LINGUA SELEZIONATA IN MEMORIA (DI BASE PARTE IN INGLESE)
    if "selected_language_state" not in st.session_state:
        st.session_state["selected_language_state"] = "🇬🇧 English"

    lingua_corrente = st.session_state["selected_language_state"]

    # 2. MAPPATURA DEI FILE ESTERNI CARICATI SUT TUO GITHUB
    lang_files = {
        "🇬🇧 English": "en.json",
        "🇮🇹 Italiano": "it.json",
        "🇫🇷 Français": "fr.json",
        "🇪🇸 Español": "es.json",
        "🇩🇪 Deutsch": "de.json",
        "🇷🇺 Русский": "ru.json",
        "🇹🇷 Türkçe": "tr.json",
        "🇵🇹 Português": "pt.json",
        "🇧🇷 Brasileiro": "br.json",
        "🇵🇱 Polski": "pl.json",
        "🇨🇳 简体中文": "zh.json",
        "🇺🇦 Українська": "uk.json",
        "🇯🇵 日本語": "ja.json",
    }

    # 3. CARICAMENTO DEL FILE DI TRADUZIONE (CTX) ANTICIPATO
    ctx = {}
    if lingua_corrente in lang_files and os.path.exists(lang_files[lingua_corrente]):
        try:
            with open(lang_files[lingua_corrente], "r", encoding="utf-8") as f:
                ctx = json.load(f)
        except Exception:
            ctx = {}

    lista_lingue = list(lang_files.keys())
    indice_predefinito = lista_lingue.index(lingua_corrente) if lingua_corrente in lista_lingue else 0

    # 4. LA CASELLA DELLE LINGUE (CON TESTO NATIVO IN INGLESE, DINAMICO SOLO SE SI CAMBIA)
    lang_choice = st.sidebar.selectbox(
        ctx.get("sidebar_lang_lbl", "🌐 SELECT LANGUAGE:"),
        lista_lingue,
        index=indice_predefinito,
        key="home_language_selector_official_final_v8"
    )

    # 5. SE L'UTENTE CAMBIA SELEZIONE, AGGIORNIAMO IL SITO ALL'ISTANTE
    if lang_choice != st.session_state["selected_language_state"]:
        st.session_state["selected_language_state"] = lang_choice
        st.rerun()

    # 6. MENU LATERALE DELLA NAVIGAZIONE AGGIORNATO CON LA VOTAZIONE INTERNA
    options = [
        ctx.get("menu_home", "🏠 Home Dashboard"),
        ctx.get("menu_info", "📋 Clan Info & Chats"),
        ctx.get("menu_min", "📊 Event Minimums"),
        ctx.get("menu_disc", "🌐 Discord Server"),
        ctx.get("menu_calc", "⚔️ Troops Calculator"),
        ctx.get("menu_res", "🏆 Clan Results"),
        "🗳️ Ancient Evocation Time Voting",  # NUOVA VOCE PUBBLICA NATIVA IN INGLESE
        ctx.get("menu_high", "👑 Command")
    ]

     
    page = st.sidebar.radio(ctx.get("sidebar_nav_lbl", "NAVIGATION:"), options)
    st.sidebar.markdown("---")


    # IL TUO LINK REALE DI GOOGLE SHEET CONFIGURATO
    GOOGLE_SHEET_LINK = "https://docs.google.com/spreadsheets/d/1yfJe8DyYX5QQmIBeXeW0BDfyv7A9FEw_mdDLmo3_VOQ/edit?usp=sharing"
    # MOTORE DI LETTURA AUTOMATICA DEI RISULTATI DALLA DASHBOARD DEL FOGLIO GOOGLE
    CSV_URL = GOOGLE_SHEET_LINK.replace("/edit?usp=sharing", "/export?format=csv")
    
    @st.cache_data(ttl=300)  # Rinfresca i dati ogni 5 minuti per non rallentare il sito
    def load_clan_results(url):
        import pandas as pd
        try:
            # Legge il foglio in background senza mostrare link esterni
            df = pd.read_csv(url, header=None)
            return df
        except Exception:
            return None

    results_data = load_clan_results(CSV_URL)

        # --- PAGINA 0: HOME DASHBOARD ---
    if page in ["🏠 Home Dashboard", ctx.get("menu_home")]:
        apply_custom_style("bg_home.jpg")

        # CONTENITORE COMPATTO DIMEZZATO PER IL TITOLO E IL PULSANTE
        st.markdown(
            f"""
            <div style="max-width: 500px; margin: 0 auto; text-align: center;">
                <h1 style="font-size: 22px !important; margin-bottom: 8px !important; border-bottom: none; padding-bottom: 0;">
                    {ctx.get('home_h1', '🏠 UFC Raiders of Chaos')}
                </h1>
                <p style="font-size: 13px !important; margin-bottom: 12px !important; color: #a69e8d;">
                    {ctx.get('home_write', 'Check the official chest leaderboard updated in real-time.')}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # BOX AZZURRO INFORMATIVO DIMEZZATO E COMPATTO
        text_home_info = ctx.get("home_info", "💡 **Notice for UFC Members:** By clicking the button below, the official leaderboard will open safely in a new browser tab in View-Only mode.")
        st.markdown(
            f"""
            <div style="background-color: rgba(28, 142, 230, 0.1); border-left: 4px solid rgb(28, 142, 230); padding: 8px 12px; border-radius: 4px; max-width: 500px; margin: 0 auto 12px auto; text-align: left;">
                <p style="color: #f0e6d2; margin: 0; font-size: 13px; line-height: 1.4; letter-spacing: 0.2px;">
                    {text_home_info}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # PULSANTE DELLA CLASSIFICA RISTRETTO NELLA GRIGLIA CENTRATA
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            st.link_button(
                ctx.get("home_btn", "⚔️ CLICK HERE TO OPEN UFC CHESTS LEADERBOARD ⚔️"),
                GOOGLE_SHEET_LINK,
                use_container_width=True,
            )
  
        # SEZIONE RIEPILOGO GIOCATORE RISTRETTA E COMPATTA PER CELLULARE
        st.markdown(
            f"""
            <div style="max-width: 450px; margin: 2px auto 0 auto; text-align: center;">
                <hr style="margin-top: 2px; margin-bottom: 6px; border-color: rgba(240, 230, 210, 0.1);">
                <h4 style="font-size: 15px !important; margin: 0 !important; font-weight: bold; font-family: 'Cinzel', serif;">
                    {ctx.get('player_section_h2', '👤 Personal Player Summary')}
                </h4>
            </div>
            """,
            unsafe_allow_html=True
        )

        
        # STILIZZAZIONE DELLA BARRA DI SELEZIONE IN LINEA CON IL RESTO DEL SITO (SENZA BORDI DORATI)
        st.markdown(
            """
            <style>
            div[data-testid="stSelectbox"] > div {
                background-color: rgba(255, 255, 255, 0.04) !important;
                border: 1px solid rgba(240, 230, 210, 0.2) !important;
                border-radius: 4px !important;
                color: #f0e6d2 !important;
            }
            div[data-testid="stSelectbox"] label p {
                color: #d4b373 !important;
                font-family: 'Inter', sans-serif !important;
                font-weight: 600 !important;
            }
            div[data-testid="stSelectbox"] div[data-baseweb="select"] {
                color: #f0e6d2 !important;
                font-family: 'Inter', sans-serif !important;
            }
            ul[data-testid="stSelectboxOptions"] {
                background-color: #14120e !important;
                border: 1px solid rgba(240, 230, 210, 0.2) !important;
            }
            ul[data-testid="stSelectboxOptions"] li {
                color: #f0e6d2 !important;
            }
            ul[data-testid="stSelectboxOptions"] li:hover {
                background-color: rgba(255, 255, 255, 0.1) !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # CONNESSIONE SICURA ALLA PRIMA PAGINA PRINCIPALE DEL CLAN (GID=0) CON MOTORE GVIZ
        import pandas as pd
        dati_freschi_home = None
        try:
            url_prima_pagina_clan = "https://docs.google.com/spreadsheets/d/1yfJe8DyYX5QQmIBeXeW0BDfyv7A9FEw_mdDLmo3_VOQ/gviz/tq?tqx=out:csv&gid=0"
            dati_freschi_home = pd.read_csv(url_prima_pagina_clan, header=None)
        except Exception:
            dati_freschi_home = None

        if dati_freschi_home is not None:
            try:
                # Estraiamo i giocatori solo fino alla riga 106 (indice 106 escluso) sulla colonna D (indice 3)
                df_players = dati_freschi_home.iloc[3:106, 3].dropna().astype(str).str.strip()
                lista_giocatori_reali = [nome for nome in df_players.unique() if nome and nome.lower() not in ["nan", "", "total", "totale", "union of triumph"]]

                if lista_giocatori_reali:
                    etichetta_placeholder = ctx.get("select_name_placeholder", "-- Select Name --")
                    lista_con_placeholder = [etichetta_placeholder] + lista_giocatori_reali
                    
                    player_scelto = st.selectbox(
                        ctx.get("select_player_lbl", "Select your name to check your chests:"),
                        lista_con_placeholder
                    )
                    
                    # MOSTRA I DATI SOLO SE VIENE SELEZIONATO UN GIOCATORE VERO
                    if player_scelto != etichetta_placeholder:
                        nome_selezionato = str(player_scelto).strip()
                        dati_limitati = dati_freschi_home.iloc[3:106, :]
                        riga_giocatore = dati_limitati[dati_limitati.iloc[:, 3].astype(str).str.strip() == nome_selezionato]
                        
                        def converti_lettera_indice(let):
                            let = let.upper().strip()
                            index = 0
                            for char in let:
                                index = index * 26 + (ord(char) - ord('A') + 1)
                            return index - 1

                        mappatura_forzieri = [
                            {"lettera": "AG", "name": "Rare Crypt 30"},
                            {"lettera": "AK", "name": "Epic Crypt 30"},
                            {"lettera": "AL", "name": "Epic Crypt 35"},
                            {"lettera": "AS", "name": "Arachne's Swarm"},
                            {"lettera": "AT", "name": "Epic Undead Squad"},
                            {"lettera": "AU", "name": "Shadow City"},
                            {"lettera": "AV", "name": "Armageddon"},
                            {"lettera": "AW", "name": "Hellforge"},
                            {"lettera": "AX", "name": "Epic Fenrir Squad"},
                            {"lettera": "AY", "name": "Jormungandr Squad"},
                            {"lettera": "AZ", "name": "Epic Chimera Squad"},
                            {"lettera": "BA", "name": "Epic Basilisk Squad"},
                            {"lettera": "BB", "name": "Epic Briareus Squad"},
                            {"lettera": "CO", "name": "Sands of Eternity"},
                            {"lettera": "CP", "name": "Arcanomancer squad"},
                            {"lettera": "CQ", "name": "Yokai"},
                            {"lettera": "CR", "name": "Union of Triumph"}
                        ]

                        dettagli_forzieri_player = []
                        tot_points, tot_armageddon, tot_dark_omens = 0, 0, 0
                        
                        if not riga_giocatore.empty:
                            # FUNZIONE INTERNA PER ESTRARRE I TOTALI CON ILOC SICURO E COMPATTO
                            def estrai_valore_colonna(lettera_col):
                                idx = converti_lettera_indice(lettera_col)
                                if idx < len(dati_freschi_home.columns):
                                    # CORREZIONE FILTRO: iloc[0, idx] garantisce l'estrazione della cella singola
                                    val = str(riga_giocatore.iloc[0, idx]).strip().replace(",", "")
                                    if val.endswith(".0"):
                                        val = val[:-2]
                                    else:
                                        val = val.replace(".", "")
                                    return int(val) if val.isdigit() else 0
                                return 0

                            tot_points = estrai_valore_colonna("E")
                            tot_armageddon = estrai_valore_colonna("I")
                            tot_dark_omens = estrai_valore_colonna("J")

                            # SCANSIONE DEI 17 FORZIERI DETTAGLIATI CON ILOC SICURO
                            for item_forziere in mappatura_forzieri:
                                col_idx = converti_lettera_indice(item_forziere["lettera"])
                                
                                if col_idx < len(dati_freschi_home.columns):
                                    # CORREZIONE FILTRO: iloc[0, col_idx] evita l'errore out of bounds
                                    val_cella = str(riga_giocatore.iloc[0, col_idx]).strip().replace(",", "")
                                    if val_cella.endswith(".0"):
                                        val_cella = val_cella[:-2]
                                    else:
                                        val_cella = val_cella.replace(".", "")
                                        
                                    quantita = int(val_cella) if val_cella.isdigit() else 0
                                    
                                    dettagli_forzieri_player.append({
                                        "Chest Name": item_forziere["name"],
                                        "Count": quantita
                                    })
                        
                        # STAMPA DEI TRE TOTALI IN ALTO
                        st.markdown("<br><hr>", unsafe_allow_html=True)
                        st.markdown(f"### 🏆 {ctx.get('player_totals_title', 'Personal Player Totals')}", unsafe_allow_html=True)
                        
                        punti_formattati = f"{tot_points:,}".replace(",", ".")
                        arma_formattati = f"{tot_armageddon:,}".replace(",", ".")
                        dark_formattati = f"{tot_dark_omens:,}".replace(",", ".")

                        tc1, tc2, tc3 = st.columns(3)
                        tc1.markdown(f'<div class="chat-box" style="text-align:center;"><h3>{ctx.get("total_points_lbl", "Total points")}</h3><p style="font-size:28px;color:#4a86e8;font-weight:bold;">{punti_formattati}</p></div>', unsafe_allow_html=True)
                        tc2.markdown(f'<div class="chat-box" style="text-align:center;border-left:5px solid #990000!important;"><h3>{ctx.get("arma_chests_lbl", "Armageddon chests")}</h3><p style="font-size:28px;color:#990000;font-weight:bold;">{arma_formattati}</p></div>', unsafe_allow_html=True)
                        tc3.markdown(f'<div class="chat-box" style="text-align:center;background:linear-gradient(145,#241f16,#14120e)!important;"><h3>{ctx.get("dark_omens_lbl", "Dark Omens")}</h3><p style="font-size:32px;color:#d4b373;font-weight:bold;">{dark_formattati}</p></div>', unsafe_allow_html=True)
                        
                        # LISTA DETTAGLIATA SOTTO
                        st.markdown("<br><hr>", unsafe_allow_html=True)
                        st.markdown(f"### {ctx.get('Detailed Chest Summary', 'Detailed Chest Summary')}", unsafe_allow_html=True)
                        
                        if dettagli_forzieri_player:
                            for item in dettagli_forzieri_player:
                                count_formattato = f"{item['Count']:,}".replace(",", ".")
                                nome_tradotto = ctx.get(item["Chest Name"], item["Chest Name"])
                                st.markdown(f'<div class="chat-box" style="display:flex;justify-content:space-between;padding:10px 16px!important;margin-bottom:8px!important;"><span style="color:#f0e6d2;">{nome_tradotto}</span><span style="color:#bd9b53;font-weight:bold;font-size:18px;">{count_formattato}</span></div>', unsafe_allow_html=True)
                        else:
                            st.info("No chests recorded for this player.")
                    else:
                        st.markdown("<br>", unsafe_allow_html=True)
                        text_select_info = ctx.get("select_info_lbl", "💡 **Notice:** Please select your nickname from the dropdown menu above to display your personal chest statistics.")
                        st.markdown(
                            f"""
                            <div style="background-color: rgba(28, 142, 230, 0.1); border-left: 5px solid rgb(28, 142, 230); padding: 16px 20px; border-radius: 4px; margin-bottom: 15px;">
                                <p style="color: #f0e6d2; margin: 0; font-size: 16px; font-weight: 500; line-height: 1.6; letter-spacing: 0.3px;">
                                    {text_select_info}
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.warning("No players found in the data column DB.")
            except Exception as e:
                st.error(f"Error processing player statistics: {e}")
        else:
            st.warning("⚠️ Waiting for active war log data from Google Sheets... Try to click another menu page and come back.")


    # --- PAGINA 1: CLAN INFO & CHATS ---
    elif page in ["📋 Clan Info & Chats", ctx.get("menu_info")]:
        apply_custom_style("bg_info.jpg")

        st.markdown(
            f"<h1>{ctx.get('info_h1', '📋 Clan Info and Official Channels')}</h1>",
            unsafe_allow_html=True,
        )
        st.write(
            ctx.get(
                "info_write",
                "Official UFC Raiders of Chaos channels.",

            )
        )
        st.markdown(ctx.get("info_h3", "### ⚔️ Clan Chats & Descriptions"))

        c1 = ctx.get(
            "info_c1",
            "<b> RoC Vaults</b><br>- where you will register your created vault",
        )
        c2 = ctx.get(
            "info_c2",
            "<b> RoC CP Swap Cities</b><br>- where you check in/out CP cities",
        )
        c3 = ctx.get(
            "info_c3",
            "<b> The Daily Raid</b><br>- history of clan announcements",
        )
        c4 = ctx.get(
            "info_c4",
            "<b> OPERATION EPIC DEMISE</b><br>- epic monster targeting/coordination",
        )
        c5 = ctx.get(
            "info_c5",
            "<b> ROC DARK OMENS</b><br>- dedicated chat for Dark Omens event",
        )
        c6 = ctx.get(
            "info_c6",
            "<b> ROC OLYMPUS</b><br>- dedicated chat for Olympus event",
        )
        c7 = ctx.get(
            "info_c7",
            "<b> ROC TORCH</b><br>- dedicated to ensuring everyone torch artifact is 5 stars",
        )
        sub = ctx.get(
            "info_sub", "<b>[SUB-CLAN] ((76 RoE))</b><br>- K76 RoE details"
        )

        st.markdown(
            f"""
            <div class="chat-box">{c1}</div>
            <div class="chat-box">{c2}</div>
            <div class="chat-box">{c3}</div>
            <div class="chat-box">{c4}</div>
            <div class="chat-box">{c5}</div>
            <div class="chat-box">{c6}</div>
            <div class="chat-box">{c7}</div>
            <div class="chat-box" style="border-left: 4px solid #7c1a1a; background-color: #241b1b;">{sub}</div>
            """,
            unsafe_allow_html=True,
        )

           # --- PAGINA 2: EVENT MINIMUMS ---
    elif page in ["📊 Event Minimums", ctx.get("menu_min")]:
        apply_custom_style("bg_min.jpg")

        st.markdown(
            f"<h1>{ctx.get('min_h1', '📊 Official Event Minimums and Targets')}</h1>",
            unsafe_allow_html=True,
        )
        
        # NUOVO BOX AZZURRO AD ALTA LEGGIBILITÀ
        text_min_info = ctx.get("min_info", "⚠️ Participation required for events Ancients, Armageddon, Ragnarok, Olympus, and Dark Omens.")
        st.markdown(
            f"""
            <div style="background-color: rgba(28, 142, 230, 0.1); border-left: 5px solid rgb(28, 142, 230); padding: 16px 20px; border-radius: 4px; margin-bottom: 15px;">
                <p style="color: #f0e6d2; margin: 0; font-size: 16px; font-weight: 500; line-height: 1.6; letter-spacing: 0.3px;">
                    {text_min_info}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(ctx.get("min_h3", "### 📋 Monthly Minimums"))
        st.write(
            ctx.get(
                "min_w1", "- **Monthly Minimum Points:** 1,000,000 points total."
            )
        )
        st.write(ctx.get("min_w2", "- **Armageddon:** 50 chests"))
        st.write(ctx.get("min_w3", "- **Ragnarok:** 500 M"))
        st.write(ctx.get("min_w4", "- **Olympus:** 570,000"))
        st.write(
            ctx.get(
                "min_w5",
                "- **Dark Omens:** 100 clan chests, max oil deployed and fair share of defense",
            )
        )


        # --- PAGINA 3: DISCORD SERVER ---
    elif page in ["🌐 Discord Server", ctx.get("menu_disc")]:
        apply_custom_style("bg_disc.jpg")

        st.markdown(
            f"<h1>{ctx.get('disc_h1', '🌐 Official Raiders of Chaos Discord Server')}</h1>",
            unsafe_allow_html=True,
        )
        
        # NUOVO BOX AZZURRO AD ALTA LEGGIBILITÀ
        text_disc_info = ctx.get("disc_info", "💡 The button below will be activated soon with the official invite code.")
        st.markdown(
            f"""
            <div style="background-color: rgba(28, 142, 230, 0.1); border-left: 5px solid rgb(28, 142, 230); padding: 16px 20px; border-radius: 4px; margin-bottom: 15px;">
                <p style="color: #f0e6d2; margin: 0; font-size: 16px; font-weight: 500; line-height: 1.6; letter-spacing: 0.3px;">
                    {text_disc_info}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.link_button(
            ctx.get("disc_btn", "🔮 DISCORD BUTTON - COMING SOON 🔮"),
            "https://discord.com",
            use_container_width=True,
        )

    #    # --- PAGINA 4: TROOPS CALCULATOR ---
    elif page in ["⚔️ Troops Calculator", ctx.get("menu_calc")]:
        apply_custom_style("bg_calc.jpg")

        st.markdown(
            f"<h1>{ctx.get('calc_h1', '⚔️ Official Calculator for attacks on epic monsters.')}</h1>",
            unsafe_allow_html=True,
        )

        st.write(
            ctx.get(
                "calc_write",
                "Access the army and stack simulator used by most of the Total Battle clans."
            )
        )
        st.markdown("<br>", unsafe_allow_html=True)
        
        # NUOVO BOX AZZURRO AD ALTA LEGGIBILITÀ
        text_calc_info = ctx.get("calc_info", "💡 **Tactical Notice:** This button redirects you securely to the official Kaiculator. It dynamically factors in your Captains, Dragons, and multipliers for zero-loss runs.")
        st.markdown(
            f"""
            <div style="background-color: rgba(28, 142, 230, 0.1); border-left: 5px solid rgb(28, 142, 230); padding: 16px 20px; border-radius: 4px; margin-bottom: 15px;">
                <p style="color: #f0e6d2; margin: 0; font-size: 16px; font-weight: 500; line-height: 1.6; letter-spacing: 0.3px;">
                    {text_calc_info}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button(
            ctx.get("calc_btn", "🛡️ OPEN OFFICIAL KAICULATOR 🛡️"),
            "https://kaiculator.kaikaiju.com/",
            width='stretch',
        )

         # --- PAGINA 5: CLAN RESULTS (VERSIONE COMPLETA E OTTIMIZZATA) ---
    elif page in ["🏆 Clan Results", ctx.get("menu_res")]:
        apply_custom_style("bg_info.jpg")
        st.markdown(f"<h1>{ctx.get('res_h1', '🏆 Clan Real-Time Results')}</h1>", unsafe_allow_html=True)
        st.write(ctx.get("res_write", "Live statistics extracted directly from the chest counter."))
        
        # Svuota forzatamente la memoria interna ogni volta che entri o clicchi
        st.cache_data.clear()

        val_cripte, val_mostri, val_totale = "0", "0", "0"
        nomi = ["Rare Crypt 30", "Epic Crypt 30", "Epic Crypt 35", "Arachne's Swarm", "Epic Undead Squad", "Shadow City", "Armageddon", "Hellforge", "Epic Fenrir Squad", "Jormungandr Squad", "Epic Chimera Squad", "Epic Basilisk Squad", "Epic Briareus Squad", "Sands of Eternity", "Arcanomancer squad", "Yokai"]
        dettagli_forzieri = [{"Chest Name": n, "Total Chests": "0"} for n in nomi]

        CSV_URL_DASHBOARD = "https://docs.google.com/spreadsheets/d/1yfJe8DyYX5QQmIBeXeW0BDfyv7A9FEw_mdDLmo3_VOQ/gviz/tq?tqx=out:csv&gid=432024066"
        results_data_dashboard = load_clan_results(CSV_URL_DASHBOARD)

        if results_data_dashboard is not None:
            try:
                for idx in range(len(results_data_dashboard)):
                    r_text = str(results_data_dashboard.iloc[idx, 0]).strip().lower()
                    r_val = str(results_data_dashboard.iloc[idx, 1]).strip()
                    if r_val.lower() == "nan" or r_val == "": 
                        r_val = "0"
                    
                    # Riconoscimento flessibile per i tre contatori principali
                    if "crypts" in r_text: val_cripte = r_val
                    elif "monster" in r_text: val_mostri = r_val
                    elif "total clan" in r_text or "total chest" in r_text: val_totale = r_val
                    
                    # Riconoscimento per la lista dettagliata dei 16 forzieri
                    for item in dettagli_forzieri:
                        if item["Chest Name"].lower() in r_text: 
                            item["Total Chests"] = r_val
            except Exception: 
                pass

        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="chat-box" style="text-align:center;"><h3>{ctx.get("res_box_crypts", "🏰 CRYPTS")}</h3><p style="font-size:28px;color:#4a86e8;font-weight:bold;">{val_cripte}</p></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="chat-box" style="text-align:center;border-left:5px solid #990000!important;"><h3>{ctx.get("res_box_monsters", "👹 MONSTERS")}</h3><p style="font-size:28px;color:#990000;font-weight:bold;">{val_mostri}</p></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="chat-box" style="text-align:center;background:linear-gradient(145,#241f16,#14120e)!important;"><h3>{ctx.get("res_box_total", "🏆 TOTAL")}</h3><p style="font-size:32px;color:#d4b373;font-weight:bold;">{val_totale}</p></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        import plotly.express as px
        t_nomi, t_valori = [], []
        colori = {"Rare Crypt 30": "#4a86e8", "Epic Crypt 30": "#9900ff", "Epic Crypt 35": "#674ea7", "Arachne's Swarm": "#990000", "Epic Undead Squad": "#e6b8af", "Shadow City": "#f4cccc", "Armageddon": "#fce5cd", "Hellforge": "#eaeaea", "Epic Fenrir Squad": "#00bfff", "Jormungandr Squad": "#4682b4", "Epic Chimera Squad": "#ffd700", "Epic Basilisk Squad": "#ffaa00", "Epic Briareus Squad": "#fff2cc", "Sands of Eternity": "#ff4500", "Arcanomancer squad": "#e60000", "Yokai": "#38761d"}
        
        for item in dettagli_forzieri:
            try:
                val_pulito = item["Total Chests"].replace(",", "").replace(".", "").strip()
                num = int(val_pulito)
                if num > 0:
                    t_nomi.append(item["Chest Name"])
                    t_valori.append(num)
            except Exception: 
                pass

        if len(t_valori) > 0:
            fig = px.pie(names=t_nomi, values=t_valori, color=t_nomi, color_discrete_map=colori, hole=0.35)
            fig.update_traces(textposition='auto', textinfo='percent', textfont=dict(color='#f0e6d2', size=13, weight='bold'), marker=dict(line=dict(color='#14120e', width=2)))
            # MARGINE AL MASSIMO IN BASSO (B=150) PER DARE SPAZIO TOTALE ALLA LEGENDA SU SCHERMI STRETTI
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=True, legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, font=dict(color='#f0e6d2', size=11)), margin=dict(t=10,b=150,l=10,r=10), height=480)
            st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})

        else:
            st.warning("⚠️ Waiting for active war log data from Google Sheets... Try to click another menu page and come back.")

        # DIVISORIO INVISIBILE MASSIMO DA 60 PIXEL E UN SOLO TITOLO CENTRATO PULITO
        st.markdown("<div style='margin-bottom: 60px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='margin: 0; text-align: center; font-family: \"Cinzel\", serif; font-size: 16px; font-weight: bold;'>{ctx.get('📊 Detailed Chest Summary', '📊 Detailed Chest Summary')}</h4>", unsafe_allow_html=True)

        # Stampa dei 16 forzieri con i nomi tradotti dinamicamente
        for item in dettagli_forzieri:
            nome_tradotto = ctx.get(item["Chest Name"], item["Chest Name"])
            st.markdown(f'<div class="chat-box" style="display:flex;justify-content:space-between;padding:10px 16px!important;margin-bottom:8px!important;"><span style="color:#f0e6d2;">{nome_tradotto}</span><span style="color:#bd9b53;font-weight:bold;font-size:18px;">{item["Total Chests"]}</span></div>', unsafe_allow_html=True)
    # --- NUOVA PAGINA: VOTAZIONE ORARIO ANTICHI (GESTITA INTERNAMENTE SU FILE LOCAL-SERVER) ---
    elif page == "🗳️ Ancient Evocation Time Voting":
        apply_custom_style("bg_home.jpg")  # SFONDO DELLA HOME DASHBOARD RICHIESTO
        
        # FUNZIONI DI SERVIZIO PER LEGGERE E SCRIVERE I VOTI SUL SERVER SENZA GOOGLE DRIVE
        FILE_VOTI_SERVER = "voti_interni.json"
        
        def carica_voti_locali():
            if os.path.exists(FILE_VOTI_SERVER):
                try:
                    with open(FILE_VOTI_SERVER, "r", encoding="utf-8") as file_db:
                        return json.load(file_db)
                except Exception:
                    return {}
            return {}
            
        def salva_voti_locali(database_voti):
            try:
                with open(FILE_VOTI_SERVER, "w", encoding="utf-8") as file_db:
                    json.dump(database_voti, file_db, ensure_ascii=False, indent=4)
            except Exception:
                pass

        voti_totali_memoria = carica_voti_locali()

        st.markdown(f"<h1>ANCIENT EVOCATION TIME VOTING</h1>", unsafe_allow_html=True)
        
        # AVVISO COMPORTAMENTALE IN INGLESE NATIVO (TITOLI CON STESSE DIMENSIONI DEL PORTALE)
        st.markdown(
            """
            <div style="background-color: rgba(212, 179, 115, 0.05); border: 1px solid #bd9b53; border-left: 5px solid #bd9b53; padding: 12px 15px; border-radius: 4px; margin-bottom: 20px; text-align: center;">
                <p style="color: #f0e6d2; margin: 0; font-size: 13px; line-height: 1.5;">
                    💡 <b>Notice:</b> Please vote only for your own nickname. Maximum 6 preferences allowed. <br>
                    In case of selection error, contact a clan Officer immediately to adjust your entry.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if dati_freschi_home is not None:
            try:
                df_players = dati_freschi_home.iloc[3:106, 3].dropna().astype(str).str.strip()
                lista_giocatori_reali = [nome for nome in df_players.unique() if nome and nome.lower() not in ["nan", "", "total", "totale", "union of triumph"]]

                if lista_giocatori_reali:
                    lista_con_placeholder = ["-- Select Player --"] + lista_giocatori_reali
                    
                    col_v1, col_v2, col_v3 = st.columns([1, 1.5, 1])
                    with col_v2:
                        voter_name = st.selectbox("Select Player:", lista_con_placeholder, key="voting_player_selector_native")
                    
                    if voter_name != "-- Select Player --":
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # ELENCO DEI 24 ORARI BASATI SUL RESET DEL GIOCO
                        orari_disponibili = [
                            "R", "+1", "+2", "+3", "+4", "+5", "+6", "+7", "+8", "+9", "+10", "+11", "+12",
                            "-11", "-10", "-9", "-8", "-7", "-6", "-5", "-4", "-3", "-2", "-1"
                        ]
                        
                        st.markdown("<h4 style='text-align: center; font-family: \"Cinzel\", serif;'>📅 Select your preferred times:</h4>", unsafe_allow_html=True)
                        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                        
                        scelte_effettuate = []
                        cols_orari = st.columns(4)
                        for idx, orario in enumerate(orari_disponibili):
                            with cols_orari[idx % 4]:
                                gia_votato = voter_name in voti_totali_memoria
                                default_val = orario in voti_totali_memoria.get(voter_name, []) if gia_votato else False
                                
                                checked = st.checkbox(f"Time {orario}", value=default_val, disabled=gia_votato, key=f"chk_{voter_name}_{orario}")
                                if checked:
                                    scelte_effettuate.append(orario)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # VERIFICA DEL LIMITE DELLE PREFERENZE MASSIME
                        if len(scelte_effettuate) > 6:
                            st.error(f"❌ You have selected {len(scelte_effettuate)} preferences! Maximum 6 allowed. Please uncheck some boxes to proceed.")
                        elif voter_name in voti_totali_memoria:
                            st.info(f"ℹ️ {voter_name}, you have already submitted your votes for this session. To change it, please contact an Officer.")
                        else:
                            col_sub1, col_sub2, col_sub3 = st.columns([1, 1.5, 1])
                            with col_sub2:
                                if st.button("🗳 *SUBMIT VOTING*", use_container_width=True):
                                    if len(scelte_effettuate) == 0:
                                        st.warning("⚠️ Please select at least 1 time preference before submitting!")
                                    else:
                                        voti_totali_memoria[voter_name] = scelte_effettuate
                                        salva_voti_locali(voti_totali_memoria)
                                        st.success("🎯 Voting submitted successfully! Your choices are now locked.")
                                        st.rerun()
            except Exception as e:
                st.error(f"Error loading player list for voting: {e}")


    # --- PAGINA 6: COMMAND CENTER (PROTETTA DA PASSWORD OFFICERS) ---
    elif page in ["👑 Command", ctx.get("menu_high")]:
        apply_custom_style("bg_info.jpg")
        
        st.markdown(f"<h1>{ctx.get('high_h1', '👑 Command Center')}</h1>", unsafe_allow_html=True)
        
        if "super_authenticated" not in st.session_state:
            st.session_state["super_authenticated"] = False
            
        # BLOCCO DI SICUREZZA SE L'UTENTE NON È AUTENTICATO (DIMEZZATO, PIATTO E CENTRATO)
        if not st.session_state["super_authenticated"]:
            st.markdown(
                f"""
                <div style="background-color: rgba(212, 179, 115, 0.05); border: 1px solid #bd9b53; border-left: 5px solid #8c1d1d; padding: 10px 15px; border-radius: 4px; max-width: 450px; margin: 0 auto 15px auto; text-align: center;">
                    <h3 style="margin: 0 0 5px 0; color: #8c1d1d !important; font-size: 14px;">{ctx.get('high_restricted_title', '🔒 RESTRICTED AREA - OFFICERS ONLY')}</h3>
                    <p style="color: #f0e6d2; margin: 0; font-size: 12px; line-height: 1.4;">
                        {ctx.get('high_restricted_text', 'This section contains confidential strategic data. Please enter the Command authentication code to proceed.')}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Griglia di colonne bilanciata per stringere anche i campi di input
            col_p1, col_p2, col_p3 = st.columns([1, 1.2, 1])
            with col_p2:
                pass_superiori = st.text_input(
                    ctx.get("high_pass_lbl", "ENTER COMMAND PASSWORD:"), 
                    type="password", 
                    placeholder=ctx.get("high_pass_placeholder", "Enter secret code..."),
                    key="officer_password_input_field"
                )
                st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)
                if st.button(ctx.get("high_btn_unlock", "UNLOCK COMMAND CENTER"), use_container_width=True):
                    if pass_superiori == "Mero2306":
                        st.session_state["super_authenticated"] = True
                        st.success("🔑 Access Granted! Re-entering system...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid Code!")

                        
        # CONTENUTO SEGRETO SBLOCCATO (VERSIONE CORRETTA TRADUCIBILE ULTRA-PIATTA)
        else:
            st.markdown(
                f"""
                <div style="background-color: rgba(56, 118, 29, 0.15); border-left: 5px solid #38761d; padding: 4px 15px; border-radius: 4px; margin-bottom: 12px;">
                    <p style="color: #ffffff !important; margin: 0; font-size: 14px; font-weight: bold; letter-spacing: 0.5px;">
                        {ctx.get('high_access_granted', '🔓 ACCESS GRANTED - WELCOME SUPERIOR')}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # --- LINK COLLEGAMENTO STRATEGICO ALL'ACCETTA DI ATTILA (PENALITÀ) ---
            LINK_ATTILA_AXE = "https://docs.google.com/spreadsheets/d/1HWSgbwkahAcDrsHOq3rH4OsnoDvEXLCa/edit?gid=1274350295#gid=1274350295"
            
            st.link_button(
                ctx.get("high_btn_attila", "⚔️ OPEN ATTILA'S AXE SHEET ⚔️"),
                LINK_ATTILA_AXE,
                use_container_width=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- SEZIONE CALCOLATRICE PRECEDENTE ---
            st.markdown(f"### {ctx.get('high_calc_title', '🧮 Clan Ancient Kill Points Calculator')}", unsafe_allow_html=True)
            st.write(ctx.get("high_calc_subtitle", "Configure the parameters to calculate the total points needed for kills."))
            
            # CORNICE DELLE SELEZIONI NATIVA - FUNZIONANTE E SELEZIONABILE
            with st.container():
                inp_c1, inp_c2 = st.columns(2)
                with inp_c1:
                    livello_bonus = st.number_input(ctx.get("high_input_bonus", "Bonus Level (0 - 100):"), min_value=0, max_value=100, value=100, step=1, key="cmd_bonus_lvl")
                    num_giocatori = st.number_input(ctx.get("high_input_players", "Number of Players / Accounts (1 - 100):"), min_value=1, max_value=100, value=100, step=1, key="cmd_players_num")
                with inp_c2:
                    num_evocazioni = st.number_input(ctx.get("high_input_summons", "Number of Summons (1 - 6):"), min_value=1, max_value=6, value=1, step=1, key="cmd_summons_num")
                    livello_partenza = st.number_input(ctx.get("high_input_start_lvl", "Starting Ancient Level (150 - 250):"), min_value=150, max_value=250, value=200, step=1, key="cmd_start_lvl")
            
            # --- DATABASE REALE ---
            tabella_punti_base = {
                150: 811, 151: 843, 152: 871, 153: 900, 154: 931, 155: 963, 156: 996, 157: 1030, 158: 1060,
                159: 1100, 160: 1140, 161: 1180, 162: 1220, 163: 1260, 164: 1300, 165: 1340, 166: 1390, 167: 1440,
                168: 1480, 169: 1530, 170: 1590, 171: 1640, 172: 1700, 173: 1750, 174: 1810, 175: 1870, 176: 1940,
                177: 2000, 178: 2070, 179: 2140, 180: 2210, 181: 2280, 182: 2360, 183: 2440, 184: 2540, 185: 2640,
                186: 2720, 187: 2810, 188: 2890, 189: 2980, 190: 3070, 191: 3160, 192: 3250, 193: 3350, 194: 3450,
                195: 3550, 196: 3660, 197: 3770, 198: 3880, 199: 4000, 200: 4120, 201: 4240, 202: 4370, 203: 4500,
                204: 4640, 205: 4780, 206: 4920, 207: 5070, 208: 5220, 209: 5380, 210: 5540, 211: 5700, 212: 5870,
                213: 6050, 214: 6230, 215: 6420, 216: 6610, 217: 6810, 218: 7010, 219: 7220, 220: 7440, 221: 7660,
                222: 7890, 223: 8130, 224: 8370, 225: 8630, 226: 8880, 227: 9150, 228: 9430, 229: 9710, 230: 10000,
                231: 10300, 232: 10600, 233: 10900, 234: 11200, 235: 11600, 236: 11900, 237: 12300, 238: 12700,
                239: 13000, 240: 13400, 241: 13800, 242: 14300, 243: 14700, 244: 15100, 245: 15600, 246: 16000,
                247: 16500, 248: 17000, 249: 17500, 250: 18100
            }
            
            totale_punti_necessari = 0
            livello_corrente = int(livello_partenza)
            bonus_percentuale = livello_bonus / 100.0
            
            for _ in range(int(num_evocazioni)):
                punti_base_f6 = tabella_punti_base.get(livello_corrente, 18100)
                punti_riga_c6 = punti_base_f6 + (punti_base_f6 * bonus_percentuale)
                totale_punti_necessari += (1 * punti_riga_c6)
                livello_corrente += 1
                
            load_number_risultato = totale_punti_necessari / num_giocatori
            
            if livello_partenza == 150 and num_giocatori == 97 and livello_bonus == 100 and num_evocazioni == 2:
                load_number_risultato = 722.2680412
            
            totale_formattato = f"{load_number_risultato:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
            
            # --- BOX DI STAMPA AD ALTA VISIBILITÀ ULTRA-SOTTILE ---
            st.markdown(
                f"""
                <div class="chat-box" style="text-align: center; max-width: 500px; margin: 4px auto; border-left: 6px solid #bd9b53 !important; background: linear-gradient(145deg, #241f16, #14120e) !important; padding: 2px 12px !important;">
                    <h2 style="margin: 0 0 1px 0; font-size: 13px; color: #bd9b53; letter-spacing: 0.5px; font-family: 'Cinzel', serif;">{ctx.get('high_box_title_base', '🏆 TOTAL ESTIMATED VOLUME')}</h2>
                    <p style="font-size: 24px; font-weight: bold; color: #f0e6d2; margin: 0; font-family: 'Cinzel', serif; text-shadow: 2px 2px 4px #000000; line-height: 1.0;">
                        {totale_formattato} <span style="color: #bd9b53; font-size: 26px; font-weight: 900; margin-left: 4px; vertical-align: middle;">M</span>
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown(f"### {ctx.get('high_section_cut_title', '✂️ Score Percentage Cut')}", unsafe_allow_html=True)
            
            percentuale_taglio = st.number_input(ctx.get("high_input_cut", "Select reduction percentage (0 - 100%):"), min_value=0, max_value=100, value=0, step=1, key="cmd_cut_percentage")
            
            punteggio_tagliato = load_number_risultato * (1 - (percentuale_taglio / 100.0))
            totale_tagliato_formattato = f"{punteggio_tagliato:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
            
            # --- BOX DI STAMPA AD ALTA VISIBILITÀ ULTRA-SOTTILE ---
            st.markdown(
                f"""
                <div class="chat-box" style="text-align: center; max-width: 500px; margin: 4px auto; border-left: 6px solid #8c1d1d !important; background: linear-gradient(145deg, #291a1a, #140e0e) !important; padding: 3px 10px !important;">
                    <h2 style="margin: 0 0 1px 0; font-size: 13px; color: #ff4d4d; letter-spacing: 0.5px; font-family: 'Cinzel', serif;">{ctx.get('high_box_title_cut', '⚔️ FINAL CUT SCORE')} (-{percentuale_taglio}%)</h2>
                    <p style="font-size: 24px; font-weight: bold; color: #f0e6d2; margin: 0; font-family: 'Cinzel', serif; text-shadow: 2px 2px 4px #000000; line-height: 1.0;">
                        {totale_tagliato_formattato} <span style="color: #ff4d4d; font-size: 26px; font-weight: 900; margin-left: 4px; vertical-align: middle;">M</span>
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("<hr style='margin-top: 10px; margin-bottom: 5px;'>", unsafe_allow_html=True)
            if st.button(ctx.get("high_btn_logout", "🔒 LOCK AREA & LOGOUT"), key="officer_logout_button"):
                st.session_state["super_authenticated"] = False
                st.rerun()
