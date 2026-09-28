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
        
        /* Titoli stile Epic War */
        h1, h2, h3 {{ color: #d4b373 !important; font-family: 'Cinzel', serif !important; text-shadow: 3px 3px 6px #000000; letter-spacing: 1px; font-weight: 700; }}
        h1 {{ border-bottom: 2px solid #bd9b53; padding-bottom: 10px; margin-bottom: 25px !important; font-size: 28px !important; }}
        
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
        if st.button("ACCESS PORTAL", use_container_width=True):
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




       # SELETTORE DELLA LINGUA CON BANDIERE
    lang_choice = st.sidebar.selectbox(
        "🌐 SELECT LANGUAGE:",
        [
            "🇬🇧 English",
            "🇮🇹 Italiano",
            "🇫🇷 Français",
            "🇪🇸 Español",
            "🇩🇪 Deutsch",
            "🇷🇺 Русский",
            "🇹🇷 Türkçe",
        ],
    )

    # Mappatura dei file esterni caricati sul tuo GitHub (Aggiornata con le bandiere)
    lang_files = {
        "🇬🇧 English": "en.json",
        "🇮🇹 Italiano": "it.json",
        "🇫🇷 Français": "fr.json",
        "🇪🇸 Español": "es.json",
        "🇩🇪 Deutsch": "de.json",
        "🇷🇺 Русский": "ru.json",
        "🇹🇷 Türkçe": "tr.json",
    }



    # Caricamento dinamico dei testi per la barra laterale
    ctx = {}
    if lang_choice in lang_files and os.path.exists(lang_files[lang_choice]):
        try:
            with open(lang_files[lang_choice], "r", encoding="utf-8") as f:
                ctx = json.load(f)
        except Exception:
            ctx = {}

    # Menu laterale che cambia lingua prendendo i dati dai tuoi JSON
           # Menu laterale che cambia lingua prendendo i dati dai tuoi JSON
    options = [
        ctx.get("menu_home", "🏠 Home Dashboard"),
        ctx.get("menu_info", "📋 Clan Info & Chats"),
        ctx.get("menu_min", "📊 Event Minimums"),
        ctx.get("menu_disc", "🌐 Discord Server"),
        ctx.get("menu_calc", "⚔️ Troops Calculator"),
        ctx.get("menu_res", "🏆 Clan Results")
    ]

    page = st.sidebar.radio("NAVIGATION:", options)
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
            df = pd.read_csv(url)
            return df
        except Exception:
            return None

    results_data = load_clan_results(CSV_URL)

        # --- PAGINA 0: HOME DASHBOARD ---
    if page in ["🏠 Home Dashboard", ctx.get("menu_home")]:
        apply_custom_style("bg_home.jpg")

        st.markdown(
            f"<h1>{ctx.get('home_h1', '🏠 UFC Command Center - Alliance Status')}</h1>",
            unsafe_allow_html=True,
        )
        st.write(
            ctx.get(
                "home_write",
                "Check the official chest leaderboard updated in real-time.",
            )
        )
        
        # NUOVO BOX AZZURRO AD ALTA LEGGIBILITÀ
        text_home_info = ctx.get("home_info", "💡 **Notice for UFC Members:** By clicking the button below, the official leaderboard will open safely in a new browser tab in View-Only mode.")
        st.markdown(
            f"""
            <div style="background-color: rgba(28, 142, 230, 0.1); border-left: 5px solid rgb(28, 142, 230); padding: 16px 20px; border-radius: 4px; margin-bottom: 15px;">
                <p style="color: #f0e6d2; margin: 0; font-size: 16px; font-weight: 500; line-height: 1.6; letter-spacing: 0.3px;">
                    {text_home_info}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button(
            ctx.get(
                "home_btn", "⚔️ CLICK HERE TO OPEN UFC CHESTS LEADERBOARD ⚔️"
            ),
            GOOGLE_SHEET_LINK,
            use_container_width=True,
        )


    # --- PAGINA 1: CLAN INFO & CHATS ---
    elif page in ["📋 Clan Info & Chats", ctx.get("menu_info")]:
        apply_custom_style("bg_info.jpg")

        st.markdown(
            f"<h1>{ctx.get('info_h1', '📋 Alliance Info and Official Channels')}</h1>",
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
                "Access the most efficient stack and army simulator used by elite Total Battle players.",
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
            "https://kaikaiju.com",
            use_container_width=True,
        )
         # --- PAGINA 5: CLAN RESULTS (MOTORE DI SEARCH DIRETTO ED ENERGETICO) ---
    elif page in ["🏆 Clan Results", ctx.get("menu_res")]:
        apply_custom_style("bg_info.jpg")

        st.markdown(f"<h1>{ctx.get('res_h1', '🏆 UFC Alliance Real-Time Results')}</h1>", unsafe_allow_html=True)
        st.write(ctx.get("res_write", "Live statistics and chest counters directly from the alliance war log."))
        st.markdown("<br>", unsafe_allow_html=True)

        # 1. Inizializzazione pulita a stringhe
        val_cripte = "0"
        val_mostri = "0"
        val_totale = "0"

        dettagli_forzieri = [
            {"Chest Name": "Rare Crypt 30", "Total Chests": "0"},
            {"Chest Name": "Epic Crypt 30", "Total Chests": "0"},
            {"Chest Name": "Epic Crypt 35", "Total Chests": "0"},
            {"Chest Name": "Arachne's Swarm", "Total Chests": "0"},
            {"Chest Name": "Epic Undead Squad", "Total Chests": "0"},
            {"Chest Name": "Shadow City", "Total Chests": "0"},
            {"Chest Name": "Armageddon", "Total Chests": "0"},
            {"Chest Name": "Hellforge", "Total Chests": "0"},
            {"Chest Name": "Epic Fenrir Squad", "Total Chests": "0"},
            {"Chest Name": "Jormungandr Squad", "Total Chests": "0"},
            {"Chest Name": "Epic Chimera Squad", "Total Chests": "0"},
            {"Chest Name": "Epic Basilisk Squad", "Total Chests": "0"},
            {"Chest Name": "Epic Briareus Squad", "Total Chests": "0"},
            {"Chest Name": "Sands of Eternity", "Total Chests": "0"},
            {"Chest Name": "Arcanomancer squad", "Total Chests": "0"},
            {"Chest Name": "Yokai", "Total Chests": "0"}
        ]

        # 2. MOTORE DI SCANSIONE TOTALE (Cerca il testo in qualsiasi cella e prende la cella di destra)
        if results_data is not None:
            try:
                # Convertiamo l'intero foglio in stringhe pulite senza indici rigidi
                df_clean = results_data.fillna("0").astype(str)
                
                for r_idx in range(len(df_clean)):
                    for c_idx in range(len(df_clean.columns)):
                        cella_testo = df_clean.iloc[r_idx, c_idx].strip()
                        cella_testo_lower = cella_testo.lower()
                        
                        # Se la cella contiene un nome cercato, prendiamo il valore della cella subito a destra
                        if c_idx + 1 < len(df_clean.columns):
                            valore_destra = df_clean.iloc[r_idx, c_idx + 1].strip()
                            if valore_destra == "" or valore_destra.lower() == "nan":
                                valore_destra = "0"
                                
                            if "crypts (rare & epic)" in cella_testo_lower or "crypts total" in cella_testo_lower:
                                val_cripte = valore_destra
                            elif "epic monsters" in cella_testo_lower:
                                val_mostri = valore_destra
                            elif "total clan chests" in cella_testo_lower:
                                val_totale = valore_destra
                            
                            for item in dettagli_forzieri:
                                if item["Chest Name"].lower() in cella_testo_lower:
                                    item["Total Chests"] = valore_destra
            except Exception:
                pass

        # 3. COMPILAZIONE GRAFICA DEI TRE BOX IN CIMA
        col_cripte, col_mostri, col_totale = st.columns(3)
        with col_cripte:
            st.markdown(f'<div class="chat-box" style="text-align: center;"><h3 style="margin:0; font-size:16px;">🏰 CRYPTS TOTAL</h3><p style="font-size: 28px; font-weight: bold; color: #4a86e8; margin: 10px 0 0 0;">{val_cripte}</p></div>', unsafe_allow_html=True)
        with col_mostri:
            st.markdown(f'<div class="chat-box" style="text-align: center; border-left: 5px solid #990000 !important;"><h3 style="margin:0; font-size:16px;">👹 EPIC MONSTERS</h3><p style="font-size: 28px; font-weight: bold; color: #990000; margin: 10px 0 0 0;">{val_mostri}</p></div>', unsafe_allow_html=True)
        with col_totale:
            st.markdown(f'<div class="chat-box" style="text-align: center; background: linear-gradient(145, #241f16, #14120e) !important;"><h3 style="margin:0; font-size:16px;">🏆 TOTAL CLAN CHESTS</h3><p style="font-size: 32px; font-weight: bold; color: #d4b373; margin: 10px 0 0 0; text-shadow: 0 0 10px #bd9b53;">{val_totale}</p></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)

        # 4. GENERAZIONE DEL GRAFICO CON I TUOI COLORI STRATEGICI
        import plotly.express as px
        
        torta_nomi = []
        torta_valori = []
        
        mappa_colori_clan = {
            "Rare Crypt 30": "#4a86e8", "Epic Crypt 30": "#9900ff", "Epic Crypt 35": "#674ea7",
            "Arachne's Swarm": "#990000", "Epic Undead Squad": "#e6b8af", "Shadow City": "#f4cccc",
            "Armageddon": "#fce5cd", "Hellforge": "#eaeaea", "Epic Fenrir Squad": "#00bfff",
            "Jormungandr Squad": "#4682b4", "Epic Chimera Squad": "#ffd700", "Epic Basilisk Squad": "#ffaa00",
            "Epic Briareus Squad": "#fff2cc", "Sands of Eternity": "#ff4500", "Arcanomancer squad": "#e60000",
            "Yokai": "#38761d"
        }
        
        for item in dettagli_forzieri:
            try:
                # Pulizia totale delle stringhe per estrarre numeri puri puliti da virgole e punti
                val_stringa = item["Total Chests"].replace(",", "").replace(".", "").strip()
                num_pulito = int(val_stringa)
                if num_pulito > 0:
                    torta_nomi.append(item["Chest Name"])
                    torta_valori.append(num_pulito)
            except Exception:
                pass

        if len(torta_valori) > 0:
            fig = px.pie(
                names=torta_nomi, 
                values=torta_valori, 
                color=torta_nomi,
                color_discrete_map=mappa_colori_clan, 
                hole=0.35
            )
            fig.update_traces(
                textposition='auto', textinfo='percent',
                textfont=dict(color='#f0e6d2', size=13, family='Inter', weight='bold'),
                marker=dict(line=dict(color='#14120e', width=2))
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=True,
                legend=dict(
                    orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5,
                    font=dict(color='#f0e6d2', size=11, family='Inter')
                ),
                margin=dict(t=10, b=40, l=10, r=10), height=480
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.warning("⚠️ No active data available for the chart summary.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📊 Detailed Chest Summary")

        # 5. LISTA DEI 16 FORZIERI COMPLETA
        for item in dettagli_forzieri:
            st.markdown(
                f"""
                <div class="chat-box" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 16px !important; margin-bottom: 8px !important;">
                    <span style="color: #f0e6d2; font-weight: 500;">{item['Chest Name']}</span>
                    <span style="color: #bd9b53; font-weight: bold; font-family: 'Cinzel', serif; font-size: 18px;">{item['Total Chests']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
                
        text_res_info = ctx.get("res_info", "📊 *Notice:* These statistics are synchronized directly with the main war log sheets to monitor general alliance efficiency.")
        st.markdown(
            f"""
            <div style="background-color: rgba(28, 142, 230, 0.1); border-left: 5px solid rgb(28, 142, 230); padding: 16px 20px; border-radius: 4px; margin-bottom: 15px;">
                <p style="color: #f0e6d2; margin: 0; font-size: 16px; font-weight: 500; font-style: italic; line-height: 1.6; letter-spacing: 0.3px;">
                    {text_res_info}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
