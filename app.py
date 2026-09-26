import streamlit as st
import os

# 1. IMPOSTAZIONI PAGINA & TEMA DARK WAR
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

# 2. SCHERMATA DI LOGIN
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
    # 3. INTERFACCIA PORTALE (ACCESSO EFFETTUATO)
    if os.path.exists("logo.png"):
        st.sidebar.image("logo.png", width=85)
    else:
        st.sidebar.markdown("<h1 style='font-size: 38px; text-align: center; margin-bottom: 0px;'>🛡️</h1>", unsafe_allow_html=True)
        
    st.sidebar.markdown("<h2 style='font-size: 18px; text-align: center; margin-top: 0px;'>UFC Portal</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    lang = st.sidebar.selectbox("🌐 INTERFACE LANGUAGE / LINGUA:", ["English", "Italiano", "Español"])
    st.sidebar.markdown("---")

    menu_config = {
        "English": ["🏠 Home Dashboard", "📋 Clan Info & Chats", "📊 Event Minimums", "🌐 Discord Server", "⚔️ Troops Calculator"],
        "Italiano": ["🏠 Dashboard Principale", "📋 Info Clan & Chat", "📊 Minimi Richiesti", "🌐 Server Discord", "⚔️ Calcolatore Truppe"],
        "Español": ["🏠 Panel Principal", "📋 Info & Chats del Clan", "📊 Mínimos de Eventos", "🌐 Servidor Discord", "⚔️ Calculadora de Tropas"]
    }
    
    options = menu_config[lang]
    selected_page = st.sidebar.radio("NAVIGATION / NAVIGAZIONE:", options)
    st.sidebar.markdown("---")
    
    page_index = options.index(selected_page)

    # --- PAGINA 0: DASHBOARD PRINCIPALE ---
    if page_index == 0:
        if lang == "English":
            st.markdown("<h1>🏠 UFC Command Center - Alliance Status</h1>", unsafe_allow_html=True)
            st.write("Check the official chest leaderboard updated in real-time by alliance OCR.")
            st.info("💡 **Notice for UFC Members:** By clicking the button below, the official leaderboard will open safely in view mode.")
            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("⚔️ CLICK HERE TO OPEN UFC CHESTS LEADERBOARD ⚔️", "https://google.com", use_container_width=True)
        elif lang == "Italiano":
            st.markdown("<h1>🏠 UFC Command Center - Stato dell Alleanza</h1>", unsafe_allow_html=True)
            st.write("Consulta la classifica ufficiale dei forzieri aggiornata in tempo reale dall OCR.")
            st.info("💡 **Nota per i membri UFC:** Cliccando sul pulsante sotto, la classifica si aprira in modalita protetta di Sola Lettura.")
            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("⚔️ CLICCA QUI PER APRIRE LA CLASSIFICA FORZIERI UFC ⚔️", "https://google.com", use_container_width=True)
        elif lang == "Español":
            st.markdown("<h1>🏠 Panel Principal - Estado de la Alianza</h1>", unsafe_allow_html=True)
            st.write("Consulte la tabla de clasificación oficial de cofres actualizada en tiempo real por el OCR.")
            st.info("💡 **Aviso para los miembros de UFC:** Al hacer clic en el botón de abajo, la clasificación oficial se abrirá de forma segura en modo de Solo Lectura.")
            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("⚔️ HAGA CLIC AQUÍ PARA ABRIR LA CLASIFICACIÓN DE COFRES UFC ⚔️", "https://google.com", use_container_width=True)

    # --- PAGINA 1: CLAN INFO & CHATS ---
    elif page_index == 1:
        if lang == "English":
            st.markdown("<h1>📋 Alliance Info and Official Channels</h1>", unsafe_allow_html=True)
            st.write("Operational directives and channels of Raiders of Chaos.")
            st.markdown("### ⚔️ Clan Chats & Descriptions")
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
        elif lang == "Italiano":
            st.markdown("<h1>📋 Informazioni Clan & Canali Ufficiali</h1>", unsafe_allow_html=True)
            st.write("Direttive operative e canali ufficiali dei Raiders of Chaos.")
            st.markdown("### ⚔️ Chat del Clan & Descrizioni")
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
        elif lang == "Español":
            st.markdown("<h1>📋 Información de la Alianza & Canales Oficiales</h1>", unsafe_allow_html=True)
            st.write("Directivas operativas y canales oficiales de comunicación de los Raiders of Chaos.")
            st.markdown("### ⚔️ Chats del Clan & Descripciones")
            st.markdown(
                """
                <div class="chat-box"><b>[CHAT 1] RoC Vaults</b><br>- donde registrará sus criptas creadas</div>
                <div class="chat-box"><b>[CHAT 2] RoC CP Swap Cities</b><br>- donde gestionará las ciudades CP</div>
                <div class="chat-box"><b>[CHAT 3] The Daily Raid</b><br>- historial de anuncios del clan</div>
                <div class="chat-box"><b>[CHAT 4] OPERATION EPIC DEMISE</b><br>- coordinación de ataques contra monstruos épicos</div>
                <div class="chat-box"><b>[CHAT 5] ROC DARK OMENS</b><br>- chat dedicado al evento Dark Omens</div>
                <div class="chat-box"><b>[CHAT 6] ROC OLYMPUS</b><br>- chat dedicado al evento Olympus</div>
                <div class="chat-box"><b>[CHAT 7] ROC TORCH</b><br>- dedicado a asegurar que el artefacto antorcha de todos esté en 5 estrellas</div>
                <div class="chat-box" style="border-left: 4px solid #7c1a1a; background-color: #241b1b;"><b>[SUB-CLAN] ((76 RoE))</b><br>- Detalles de la sub-alianza K76 RoE</div>
                """, unsafe_allow_html=True
            )

    # --- PAGINA 2: EVENT MINIMUMS (RIPRISTINATA AL 100% IN TUTTE LE LINGUE) ---
    elif page_index == 2:
        if lang == "English":
            st.markdown("<h1>📊 Official Event Minimums and Targets</h1>", unsafe_allow_html=True)
            st.info("⚠️ Participation required for events Ancients, Ragnarok, Olympus, and Dark Omens.")
            st.markdown("### 📋 Event Minimums")
            st.write("- **Monthly Minimum Points:** 1,000,000 points *(points to earn with level 30 rare crypts, level 30/35 epic crypts, and epic monster chests)*")
            st.write("- **Armageddon:** 50 chests")
