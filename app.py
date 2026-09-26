import streamlit as st
import os

# 1. PAGE SETTINGS & WAR DESIGN
st.set_page_config(page_title="UFC Command Center", layout="wide", page_icon="🛡️")

st.markdown(
    """
    <style>
    .stApp { background-color: #1a1a1a; color: #e6c687; }
    [data-testid="stSidebar"] { background-color: #262626; border-right: 2px solid #bd9b53; }
    h1, h2, h3 { color: #bd9b53 !important; font-family: 'Georgia', serif; text-shadow: 2px 2px 4px #000000; font-weight: bold; }
    .stMarkdown p { color: #dfdfdf; font-size: 16px; }
    .stAlert { background-color: #2b2311 !important; border: 1px solid #bd9b53 !important; color: #e6c687 !important; }
    .stSlider > div [data-baseweb="slider"] > div { background-color: #bd9b53; }
    .chat-box { background-color: #262626; border: 1px solid #444; border-left: 4px solid #bd9b53; padding: 14px; margin-bottom: 12px; border-radius: 4px; }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. LOGIN AUTHENTICATION
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col_login, col2 = st.columns(3)
    with col_login:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=145)
        else:
            st.markdown('<h1 style="text-align: center; font-size: 45px; margin: 0px;">🛡️</h1>', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; margin-top: 15px; font-size: 26px;'>UFC RAIDERS OF CHAOS</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; font-size: 13px; color: #bd9b53;'>ALLIANCE PORTAL - RESTRICTED ACCESS</h3>", unsafe_allow_html=True)
        
        password_entered = st.text_input("CLAN PASSWORD:", type="password", placeholder="Enter access code...")
        if st.button("ACCESS PORTAL", width='stretch'):
            if password_entered == "UFC_Raiders_2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Incorrect password!")
else:
    # 3. PORTAL ACCESSED - INTERFACE
    if os.path.exists("logo.png"):
        st.sidebar.image("logo.png", width=85)
    else:
        st.sidebar.markdown("<h1 style='font-size: 38px; text-align: center; margin-bottom: 0px;'>🛡️</h1>", unsafe_allow_html=True)
        
    st.sidebar.markdown("<h2 style='font-size: 18px; text-align: center; margin-top: 0px;'>UFC Portal</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    # 6 LANGUAGES SELECTOR
    lang = st.sidebar.selectbox("🌐 INTERFACE LANGUAGE:", ["English", "Italiano", "Français", "Español", "Deutsch", "Русский"])
    st.sidebar.markdown("---")

    # --- ENGLISH ---
    if lang == "English":
        page = st.sidebar.radio("NAVIGATION:", ["🏠 Home Dashboard", "📋 Clan Info & Chats", "📊 Event Minimums", "🌐 Discord Server", "⚔️ Troops Calculator"])
        if page == "🏠 Home Dashboard":
            st.markdown("<h1>🏠 UFC Command Center - Alliance Status</h1>", unsafe_allow_html=True)
            st.write("Check the official chest leaderboard updated in real-time by alliance OCR.")
            st.info("💡 **Notice for UFC Members:** By clicking the button below, the official leaderboard will open safely in view mode.")
            st.link_button("⚔️ CLICK HERE TO OPEN UFC CHESTS LEADERBOARD ⚔️", "https://google.com", use_container_width=True)
        elif page == "📋 Clan Info & Chats":
            st.markdown("<h1>📋 Alliance Info & Official Channels</h1>", unsafe_allow_html=True)
            st.markdown(
                """
                <div class="chat-box"><b>[CHAT 1] RoC Vaults</b><br>- where you will register your created vault</div>
                <div class="chat-box"><b>[CHAT 2] RoC CP Swap Cities</b><br>- where you check in/out CP cities</div>
                <div class="chat-box"><b>[CHAT 3] The Daily Raid</b><br>- history of clan announcements</div>
                <div class="chat-box"><b>[CHAT 4] OPERATION EPIC DEMISE</b><br>- epic monster targeting/coordination</div>
                <div class="chat-box"><b>[CHAT 5] ROC DARK OMENS</b><br>- dedicated chat for Dark Omens event</div>
                <div class="chat-box"><b>[CHAT 6] ROC OLYMPUS</b><br>- dedicated chat for Olympus event</div>
                <div class="chat-box"><b>[CHAT 7] ROC TORCH</b><br>- dedicated to ensuring everyone torch artifact is 5 stars</div>
                <div class="chat-box" style="border-left: 4px solid #7c1a1a; background-color: #241b1b;"><b>[SUB-CLAN] ((76 RoE))</b><br>- K76 RoE details</div>
                """, unsafe_allow_html=True
            )
        elif page == "📊 Event Minimums":
            st.markdown("<h1>📊 Official Event Minimums & Targets</h1>", unsafe_allow_html=True)
            st.info("⚠️ Participation required for events Ancients, Ragnarok, Olympus, and Dark Omens.")
            st.write("- **Monthly Minimum Points:** 1,000,000 points *(crypts level 30 rare, level 30/35 epic, and epic monster chests)*")
            st.write("- **Armageddon:** 50 chests")
            st.write("- **Ragnaroc:** 500m")
            st.write("- **Olympus:** 570.000")
            st.write("- **Dark Omens:** 100 clan chests, max oil deployed and fair share of defense")
        elif page == "🌐 Discord Server":
            st.markdown("<h1>🌐 Official Raiders of Chaos Discord Server</h1>", unsafe_allow_html=True)
            st.info("💡 The button below will be activated soon with the official invite code.")
            st.link_button("🔮 DISCORD BUTTON - COMING SOON 🔮", "https://discord.com", use_container_width=True)
        elif page == "⚔️ Troops Calculator":
            st.markdown("<h1>⚔️ UFC Tactical Manual & March Simulator</h1>", unsafe_allow_html=True)
            capacity = st.slider("Select maximum march capacity:", 10000, 600000, 200000, step=5000)
            target = st.selectbox("Select attack target:", ["Level 35 Crypts", "Alliance Citadels"])
            if target == "Level 35 Crypts":
                st.success(f"💥 **Crypt Configuration:** Send **{int(capacity * 0.6):,} Infantry** and **{int(capacity * 0.4):,} Archers**.")
            else: st.warning("⚠️ Send the entire balanced army according to directives.")

    # --- ITALIANO ---
    elif lang == "Italiano":
        page = st.sidebar.radio("NAVIGAZIONE:", ["🏠 Dashboard Principale", "📋 Info Clan & Chat", "📊 Minimi Richiesti", "🌐 Server Discord", "⚔️ Calcolatore Truppe"])
        if page == "🏠 Dashboard Principale":
            st.markdown("<h1>🏠 UFC Command Center - Stato dell Alleanza</h1>", unsafe_allow_html=True)
            st.write("Consulta la classifica ufficiale dei forzieri aggiornata in tempo reale.")
            st.info("💡 **Nota per i membri UFC:** Cliccando sul pulsante sotto, la classifica si aprira in Sola Lettura.")
            st.link_button("⚔️ CLICCA QUI PER APRIRE LA CLASSIFICA FORZIERI UFC ⚔️", "https://google.com", use_container_width=True)
        elif page == "📋 Info Clan & Chat":
            st.markdown("<h1>📋 Informazioni Clan & Canali Ufficiali</h1>", unsafe_allow_html=True)
            st.markdown(
                """
                <div class="chat-box"><b>[CHAT 1] RoC Vaults</b><br>- dove registrare i vault creati</div>
                <div class="chat-box"><b>[CHAT 2] RoC CP Swap Cities</b><br>- dove fare il check in/out delle citta CP</div>
                <div class="chat-box"><b>[CHAT 3] The Daily Raid</b><br>- storico degli annunci del clan</div>
                <div class="chat-box"><b>[CHAT 4] OPERATION EPIC DEMISE</b><br>- coordinamento degli attacchi ai mostri epici</div>
                <div class="chat-box"><b>[CHAT 5] ROC DARK OMENS</b><br>- chat dedicata all evento Dark Omens</div>
                <div class="chat-box"><b>[CHAT 6] ROC OLYMPUS</b><br>- chat dedicata all evento Olympus</div>
                <div class="chat-box"><b>[CHAT 7] ROC TORCH</b><br>- dedicata a portare l artefatto torcia di tutti a 5 stelle</div>
                <div class="chat-box" style="border-left: 4px solid #7c1a1a; background-color: #241b1b;"><b>[SUB-CLAN] ((76 RoE))</b><br>- Dettagli sotto-alleanza K76 RoE</div>
                """, unsafe_allow_html=True
            )
        elif page == "📊 Minimi Richiesti":
            st.markdown("<h1>📊 Minimi Richiesti per gli Eventi</h1>", unsafe_allow_html=True)
            st.info("⚠️ La partecipazione e richiesta per gli eventi Antichi, Ragnarok, Olympus e Dark Omens.")
            st.write("- **Punti Minimi Mensili:** 1.000.000 di punti *(cripte rare liv 30, cripte epiche liv 30/35 e forzieri mostri epici)*")
            st.write("- **Armageddon:** 50 forzieri")
            st.write("- **Ragnaroc:** 500m")
            st.write("- **Olympus:** 570.000")
            st.write("- **Dark Omens:** 100 forzieri di clan, massimo olio schierato e difesa attiva")
        elif page == "🌐 Server Discord":
            st.markdown("<h1>🌐 Server Discord Ufficiale Raiders of Chaos</h1>", unsafe_allow_html=True)
            st.info("💡 Il pulsante qui sotto verra attivato a breve con il codice d invito.")
            st.link_button("🔮 PULSANTE DISCORD - IN ALLESTIMENTO 🔮", "https://discord.com", use_container_width=True)
        elif page == "⚔️ Calcolatore Truppe":
            st.markdown("<h1>⚔️ Manuale Tattico UFC & Simulatore Marce</h1>", unsafe_allow_html=True)
            capacity = st.slider("Seleziona la tua capacita di marcia massima:", 10000, 600000, 200000, step=5000)
            target = st.selectbox("Seleziona il bersaglio dell attacco:", ["Cripte Livello 35", "Cittadelle dell Alleanza"])
            if target == "Cripte Livello 35":
                st.success(f"💥 **Configurazione Cripte:** Manda **{int(capacity * 0.6):,} Fanteria** e **{int(capacity * 0.4):,} Arcieri**.")
            else: st.warning("⚠️ Manda l intero esercito bilanciato secondo le direttive.")

    # --- FRANÇAIS ---
