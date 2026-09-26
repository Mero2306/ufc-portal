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

    # --- CHAT DICTIONARIES FOR CHAT 1 TO 7 ---
    chat_titles = ["[CHAT 1] RoC Vaults", "[CHAT 2] RoC CP Swap Cities", "[CHAT 3] The Daily Raid", "[CHAT 4] OPERATION EPIC DEMISE", "[CHAT 5] ROC DARK OMENS", "[CHAT 6] ROC OLYMPUS", "[CHAT 7] ROC TORCH", "[SUB-CLAN] ((76 RoE))"]
    
    chat_descs = {
        "English": ["where you will register your created vault", "where you check in/out CP cities", "history of clan announcements", "epic monster targeting/coordination", "dedicated chat for Dark Omens event", "dedicated chat for Olympus event", "dedicated to ensuring everyone torch artifact is 5 stars", "K76 RoE details"],
        "Italiano": ["dove registrare i vault creati", "dove fare il check in/out delle citta CP", "storico degli annunci del clan", "coordinamento degli attacchi ai mostri epici", "chat dedicata all evento Dark Omens", "chat dedicata all evento Olympus", "dedicata a portare l artefatto torcia di tutti a 5 stelle", "Dettagli sotto-alleanza K76 RoE"],
        "Français": ["ou vous enregistrerez vos cryptes creees", "ou vous gerez les villes CP", "historique des annonces du clan", "coordination contre les monstres epiques", "chat dedie a l evenement Dark Omens", "chat dedie a l evenement Olympus", "dedie a l artefact torche 5 etoiles pour tous", "details K76 RoE"],
        "Español": ["donde registrara sus criptas creadas", "donde gestionar las ciudades CP", "historial de anuncios del clan", "coordinacion contra monstruos epicos", "chat dedicado al evento Dark Omens", "chat dedicado al evento Olympus", "dedicado al artefacto antorcha de 5 estrellas para todos", "detalles K76 RoE"],
        "Deutsch": ["Wo Sie Ihre erstellten Krypten registrieren", "Wo Sie CP-Stadte verwalten", "Verlauf der Klan-Ankündigungen", "Koordination gegen epische Monster", "Chat fur das Dark Omens Event", "Chat fur das Olympus Event", "Fur das Fackel-Artefakt auf 5 Sterne fur alle", "K76 RoE Details"],
        "Русский": ["где вы регистрируете свои созданные крипты", "где вы управляете городами CP", "история объявлений клана", "координация против эпических монстров", "чат для события Dark Omens", "чат для события Olympus", "для прокачки факела на 5 звезд для всех", "подробности K76 RoE"]
    }

    # --- MINIMUMS DICTIONARIES ---
    min_labels = {
        "English": {
            "h1": "📊 Official Event Minimums and Targets", "warn": "Participation required for events Ancients, Ragnarok, Olympus, and Dark Omens.",
            "pt": "Monthly Minimum Points: 1,000,000 points (crypts level 30 rare, level 30/35 epic, and epic monster chests)",
            "arm": "Armageddon: 50 chests", "rag": "Ragnaroc: 500m", "oly": "Olympus: 570.000", "dark": "Dark Omens: 100 chests, max oil deployed and fair share of defense"
        },
        "Italiano": {
            "h1": "📊 Minimi Richiesti per gli Eventi", "warn": "La partecipazione e richiesta per gli eventi Antichi, Ragnarok, Olympus e Dark Omens.",
            "pt": "Punti Minimi Mensili: 1.000.000 di punti (cripte rare liv 30, cripte epiche liv 30/35 e forzieri mostri epici)",
            "arm": "Armageddon: 50 forzieri", "rag": "Ragnaroc: 500m", "oly": "Olympus: 570.000", "dark": "Dark Omens: 100 forzieri, massimo olio schierato e difesa attiva"
        },
        "Français": {
            "h1": "📊 Minimums et Objectifs des Événements", "warn": "Participation requise aux Ancients, Ragnarok, Olympus et Dark Omens.",
            "pt": "Points Minimums Mensuels: 1 000 000 points (cryptes rare 30, cryptes epique 30/35, et coffres de monstres)",
            "arm": "Armageddon: 50 coffres", "rag": "Ragnaroc: 500m", "oly": "Olympus: 570.000", "dark": "Dark Omens: 100 coffres de clan, max huile deployee"
        },
        "Español": {
            "h1": "📊 Mínimos y Objetivos Oficiales", "warn": "Participación requerida en Ancients, Ragnarok, Olympus y Dark Omens.",
            "pt": "Puntos Mínimos Mensuales: 1,000,000 puntos (criptas raras 30, epicas 30/35 y monstruos)",
            "arm": "Armageddon: 50 cofres", "rag": "Ragnaroc: 500m", "oly": "Olympus: 570.000", "dark": "Dark Omens: 100 cofres, maximo petroleo"
        },
        "Deutsch": {
            "h1": "📊 Offizielle Event Mindestwerte", "warn": "Teilnahme erforderlich fur Ancients, Ragnarok, Olympus und Dark Omens.",
            "pt": "Monatliche Mindestpunkte: 1.000.000 Punkte (Stufe 30 Krypten, Stufe 30/35 epische Krypten)",
            "arm": "Armageddon: 50 Kisten", "rag": "Ragnaroc: 500m", "oly": "Olympus: 570.000", "dark": "Dark Omens: 100 Kisten, max Ol"
        },
        "Русский": {
            "h1": "📊 Минимальные требования к событиям", "warn": "Требуется участие в событиях Ancients, Ragnarok, Olympus и Dark Omens.",
            "pt": "Минимальные месячные очки: 1 000 000 очков (редкие крипты 30, эпические крипты 30/35)",
            "arm": "Armageddon: 50 сундуков", "rag": "Ragnaroc: 500m", "oly": "Olympus: 570.000", "dark": "Dark Omens: 100 сундуков, макс нефть"
        }
    }

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
