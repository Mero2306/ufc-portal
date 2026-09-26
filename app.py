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
        if st.button("ACCESS PORTAL"):
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
    
    lang = st.sidebar.selectbox("🌐 INTERFACE LANGUAGE:", ["English", "Italiano", "Français", "Español", "Deutsch", "Русский", "Türkçe"])
    st.sidebar.markdown("---")

    menu_config = {
        "English": ["🏠 Home Dashboard", "📋 Clan Info & Chats", "📊 Event Minimums", "🌐 Discord Server", "⚔️ Troops Calculator"],
        "Italiano": ["🏠 Dashboard Principale", "📋 Info Clan & Chat", "📊 Minimi Richiesti", "🌐 Server Discord", "⚔️ Calcolatore Truppe"],
        "Français": ["🏠 Tableau de Bord", "📋 Infos & Chats", "📊 Minimums Événements", "🌐 Serveur Discord", "⚔️ Simulateur"],
        "Español": ["🏠 Panel Principal", "📋 Info & Chats", "📊 Mínimos Eventos", "🌐 Servidor Discord", "⚔️ Calculadora"],
        "Deutsch": ["🏠 Haupt Dashboard", "📋 Klan Infos", "📊 Event Mindestwerte", "🌐 Discord Server", "⚔️ Truppen Rechner"],
        "Русский": ["🏠 Главная панель", "📋 Информация и чаты", "📊 Требования", "🌐 Сервер Discord", "⚔️ Калькулятор"],
        "Türkçe": ["🏠 Ana Panel", "📋 Klan Bilgisi ve Sohbetler", "📊 Etkinlik Sınırları", "🌐 Discord Sunucusu", "⚔️ Asker Hesaplayıcı"]
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
            st.write("Consulta la classifica ufficiale dei forzieri aggiornata in tempo reale dall OCR.")
            st.info("💡 **Nota per i membri UFC:** Cliccando sul pulsante sotto, la classifica si aprirà in modalità protetta di Sola Lettura.")
            st.link_button("⚔️ CLICCA QUI PER APRIRE LA CLASSIFICA FORZIERI UFC ⚔️", "https://google.com", use_container_width=True)
        elif lang == "Français":
            st.markdown("<h1>🏠 Tableau de Bord - Statut de l Alliance</h1>", unsafe_allow_html=True)
            st.info("💡 En cliquant ci-dessous, le classement s ouvrira en mode lecture seule.")
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
        elif lang == "Türkçe":
            st.markdown("<h1>🏠 Ana Panel - İttifak Durumu</h1>", unsafe_allow_html=True)
            st.write("OCR tarafından gerçek zamanlı olarak güncellenen resmi liderlik tablosunu kontrol edin.")
            st.info("💡 **UFC Üyeleri İçin Not:** Aşağıdaki butona tıkladığınızda resmi liderlik tablosu Salt Okunur modda güvenle açılacaktır.")
            st.link_button("⚔️ UFC LİDERLİK TABLOSUNU AÇMAK İÇİN BURAYA TIKLAYIN ⚔️", "https://google.com", use_container_width=True)

    # --- PAGE 1: CLAN INFO & CHATS ---
    elif page_index == 1:
        st.markdown("<h1>📋 Clan Info & Chats</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="chat-box"><b>[CHAT] Alliance Channels</b><br>- Multi-language descriptions active.</div>
            """, 
            unsafe_allow_html=True
        )

    # --- PAGE 2: EVENT MINIMUMS ---
    elif page_index == 2:
        st.markdown("<h1>📊 Event Minimums</h1>", unsafe_allow_html=True)
        st.write("Participation required for alliance events.")

    # --- PAGE 3: DISCORD SERVER ---
    elif page_index == 3:
        st.markdown("<h1>🌐 Discord Server</h1>", unsafe_allow_html=True)
        st.link_button("🔮 DISCORD LINK", "https://discord.com", use_container_width=True)

    # --- PAGE 4: TROOPS CALCULATOR ---
    elif page_index == 4:
        st.markdown("<h1>⚔️ Troops Calculator</h1>", unsafe_allow_html=True)
        st.warning("⚠️ **Under Construction:** This calculator is under development.")
