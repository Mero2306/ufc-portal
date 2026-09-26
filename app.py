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

    # NAVIGATION DICTIONARIES
    menu_config = {
        "English": ["🏠 Home Dashboard", "📋 Clan Info & Chats", "📊 Event Minimums", "🌐 Discord Server", "⚔️ Troops Calculator"],
        "Italiano": ["🏠 Dashboard Principale", "📋 Info Clan & Chat", "📊 Minimi Richiesti", "🌐 Server Discord", "⚔️ Calcolatore Truppe"],
        "Français": ["🏠 Tableau de Bord", "📋 Infos & Chats", "📊 Minimums Événements", "🌐 Serveur Discord", "⚔️ Simulateur"],
        "Español": ["🏠 Panel Principal", "📋 Info & Chats", "📊 Mínimos Eventos", "🌐 Servidor Discord", "⚔️ Calculadora"],
        "Deutsch": ["🏠 Haupt Dashboard", "📋 Klan Infos", "📊 Event Mindestwerte", "🌐 Discord Server", "⚔️ Truppen Rechner"],
        "Русский": ["🏠 Главная панель", "📋 Информация и чаты", "📊 Требования", "🌐 Сервер Discord", "⚔️ Калькулятор"]
    }
    
    options = menu_config[lang]
    selected_page = st.sidebar.radio("NAVIGATION / NAVIGAZIONE:", options)
    st.sidebar.markdown("---")
    
    page_index = options.index(selected_page)

    # --- PAGE 0: HOME DASHBOARD ---
    if page_index == 0:
        if lang == "English":
            st.markdown("<h1>🏠 UFC Command Center - Alliance Status</h1>", unsafe_allow_html=True)
            st.write("Check the official chest leaderboard updated in real-time by alliance OCR.")
            st.info("💡 **Notice for UFC Members:** By clicking the button below, the official leaderboard will open safely in view mode.")
            st.link_button("⚔️ CLICK HERE TO OPEN UFC CHESTS LEADERBOARD ⚔️", "https://google.com", use_container_width=True)
        elif lang == "Italiano":
            st.markdown("<h1>🏠 UFC Command Center - Stato dell Alleanza</h1>", unsafe_allow_html=True)
            st.write("Consulta la classifica ufficiale dei forzieri aggiornata in tempo reale.")
            st.info("💡 **Nota per i membri UFC:** Cliccando sul pulsante sotto, la classifica si aprira in Sola Lettura.")
            st.link_button("⚔️ CLICCA QUI PER APRIRE LA CLASSIFICA FORZIERI UFC ⚔️", "https://google.com", use_container_width=True)
        elif lang == "Français":
            st.markdown("<h1>🏠 Tableau de Bord - Statut de l Alliance</h1>", unsafe_allow_html=True)
            st.info("💡 En clicking ci-dessous, le classement s ouvrira en mode lecture seule.")
            st.link_button("⚔️ CLIQUEZ ICI POUR OUVRIR LE CLASSEMENT ⚔️", "https://google.com", use_container_width=True)
        elif lang == "Español":
            st.markdown("<h1>🏠 Panel Principal - Estado de Alianza</h1>", unsafe_allow_html=True)
            st.link_button("⚔️ CLIC AQUI PARA ABRIR LA CLASIFICACION ⚔️", "https://google.com", use_container_width=True)
        elif lang == "Deutsch":
            st.markdown("<h1>🏠 Haupt Dashboard - Allianz Status</h1>", unsafe_allow_html=True)
            st.link_button("⚔️ HIER KLICKEN FÜR BESTENLISTE ⚔️", "https://google.com", use_container_width=True)
        elif lang == "Русский":
            st.markdown("<h1>🏠 Главная панель - Статус альянса</h1>", unsafe_allow_html=True)
            st.link_button("⚔️ НАЖМИТЕ ЗДЕСЬ ДЛЯ ОТКРЫТИЯ РЕЙТИНГА ⚔️", "https://google.com", use_container_width=True)

    # --- PAGE 1: CLAN INFO & CHATS ---
    elif page_index == 1:
        if lang == "English":
            st.markdown("<h1>📋 Alliance Info and Official Channels</h1>", unsafe_allow_html=True)
            st.write("Operational directives and channels of Raiders of Chaos.")
        elif lang == "Italiano":
            st.markdown("<h1>📋 Informazioni Clan and Canali Ufficiali</h1>", unsafe_allow_html=True)
            st.write("Direttive operative dei Raiders of Chaos.")
        elif lang == "Français":
            st.markdown("<h1>📋 Infos de l Alliance</h1>", unsafe_allow_html=True)
            st.write("Directives operationnelles des Raiders of Chaos.")
        elif lang == "Español":
            st.markdown("<h1>📋 Info de Alianza</h1>", unsafe_allow_html=True)
            st.write("Directives operativas de Raiders of Chaos.")
        elif lang == "Deutsch":
            st.markdown("<h1>📋 Allianz Infos</h1>", unsafe_allow_html=True)
            st.write("Einsatzrichtlinien der Raiders of Chaos.")
        elif lang == "Русский":
            st.markdown("<h1>📋 Информация альянса</h1>", unsafe_allow_html=True)
            st.write("Оперативные директивы Raiders of Chaos.")
            
        st.divider()
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

    # --- PAGE 2: EVENT MINIMUMS ---
    elif page_index == 2:
        if lang == "English":
            st.markdown("<h1>📊 Official Event Minimums and Targets</h1>", unsafe_allow_html=True)
            st.info("⚠️ Participation required for events Ancients, Ragnarok, Olympus, and Dark Omens.")
            st.write("- **Monthly Minimum Points:** 1,000,000 points *(crypts level 30 rare, level 30/35 epic, and epic monster chests)*")
        elif lang == "Italiano":
            st.markdown("<h1>📊 Minimi Richiesti per gli Eventi</h1>", unsafe_allow_html=True)
            st.info("⚠️ La partecipazione e richiesta per gli eventi Antichi, Ragnarok, Olympus e Dark Omens.")
            st.write("- **Punti Minimi Mensili:** 1.000.000 di punti *(cripte rare liv 30, cripte epiche liv 30/35 e forzieri mostri epici)*")
        elif lang == "Français":
            st.markdown("<h1>📊 Minimums et Objectifs des Événements</h1>", unsafe_allow_html=True)
            st.write("- **Points Minimums Mensuels:** 1 000 000 points *(cryptes rare 30, cryptes epique 30/35, et coffres de monstres)*")
        elif lang == "Español":
            st.markdown("<h1>📊 Mínimos y Objetivos Oficiales</h1>", unsafe_allow_html=True)
            st.write("- **Puntos Mínimos Mensuales:** 1,000,000 puntos *(criptas raras 30, epicas 30/35 y monstruos)*")
        elif lang == "Deutsch":
            st.markdown("<h1>📊 Offizielle Event Mindestwerte</h1>", unsafe_allow_html=True)
            st.write("- **Monatliche Mindestpunkte:** 1.000.000 Punkte *(Stufe 30 Krypten, Stufe 30/35 epische Krypten)*")
        elif lang == "Русский":
            st.markdown("<h1>📊 Минимальные требования к событиям</h1>", unsafe_allow_html=True)
