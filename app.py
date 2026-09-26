import streamlit as st
import os

# 1. IMPOSTAZIONI DEL SITO & GRAFICA DARK WAR (HTML/CSS)
st.set_page_config(page_title="UFC Command Center", layout="wide", page_icon="🛡️")

st.markdown(
    """
    <style>
    /* Sfondo totale scuro grafite e testo oro antico */
    .stApp {
        background-color: #1a1a1a;
        color: #e6c687;
    }
    /* Sfondo della barra laterale grigio scuro metallico */
    [data-testid="stSidebar"] {
        background-color: #262626;
        border-right: 2px solid #bd9b53;
    }
    /* Colore dei titoli principali */
    h1, h2, h3 {
        color: #bd9b53 !important;
        font-family: 'Georgia', serif;
        text-shadow: 2px 2px 4px #000000;
        font-weight: bold;
    }
    /* Personalizzazione dei testi normali */
    .stMarkdown p {
        color: #dfdfdf;
        font-size: 16px;
    }
    /* Scatola informativa modificata in stile bacheca militare */
    .stAlert {
        background-color: #2b2311 !important;
        border: 1px solid #bd9b53 !important;
        color: #e6c687 !important;
    }
    /* Slider interattivo color oro */
    .stSlider > div [data-baseweb="slider"] > div {
        background-color: #bd9b53;
    }
    /* Contenitore per le chat tattiche militarizzato */
    .chat-box {
        background-color: #262626;
        border: 1px solid #444;
        border-left: 4px solid #bd9b53;
        padding: 14px;
        margin-bottom: 12px;
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. FUNZIONE DI SICUREZZA (PASSWORD LOCK)
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    st.markdown("<br>", unsafe_allow_html=True)
    col_v1, col_login, col_v2 = st.columns(3)
    
    with col_login:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=145)
        else:
            st.markdown('<h1 style="text-align: center; font-size: 45px; margin: 0px;">🛡️</h1>', unsafe_allow_html=True)
            
        st.markdown("<h1 style='text-align: center; margin-top: 15px; font-size: 26px;'>UFC RAIDERS OF CHAOS</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; font-size: 13px; letter-spacing: 2px; color: #bd9b53;'>PORTALE ALLEANZA - ACCESSO RISERVATO</h3>", unsafe_allow_html=True)
        password_entered = st.text_input("PASSWORD CLAN:", type="password", placeholder="Inserisci il codice d'accesso...")
        
        if st.button("ACCEDI AL PORTALE", width='stretch'):
            if password_entered == "UFC_Raiders_2026": 
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Password errata! Chiedi il codice corretto ai generali.")
                
    return False

# 3. SE LOGGATO, APRI IL SITO DEL CLAN
if check_password():
    
    # BARRA LATERALE DI NAVIGAZIONE CON LA NUOVA SCHEDA DEI MINIMI
    if os.path.exists("logo.png"):
        st.sidebar.image("logo.png", width=85) 
    else:
        st.sidebar.markdown("<h1 style='font-size: 38px; text-align: center; margin-bottom: 0px;'>🛡️</h1>", unsafe_allow_html=True)
        
    st.sidebar.markdown("<h2 style='font-size: 18px; text-align: center; margin-top: 0px;'>UFC Portal</h2>", unsafe_allow_html=True)
    
    # Menù a 5 voci aggiornato con il nuovo blocco per i minimi
    page = st.sidebar.radio("NAVIGAZIONE:", ["🏠 Home Dashboard", "📋 Clan Info & Chats", "📊 Event Minimums", "🌐 Discord Server", "⚔️ Troops Calculator"])
    st.sidebar.markdown("---")
    st.sidebar.success("Portale protetto attivo.")

    # --- PAGINA 1: DASHBOARD ---
    if page == "🏠 Home Dashboard":
        st.markdown("<h1>🏠 UFC Command Center - Stato dell'Alleanza</h1>", unsafe_allow_html=True)
        st.write("Consulta la classifica ufficiale dei forzieri aggiornata in tempo reale dall'OCR dell'alleanza.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **Notice for UFC Members:** By clicking the button below, the official leaderboard will open safely in a new browser tab in View-Only mode. You can check your scores and goals with maximum security.")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        LINK_PULITO = "LAVORI_IN_CORSO"
        
        st.markdown(
            f'''
            <a href="#" target="_blank" style="text-decoration: none;">
                <div style="background-color: #8b0000; color: #e6c687; text-align: center; padding: 20px 24px; border: 2px solid #bd9b53; border-radius: 10px; font-weight: bold; font-size: 20px; box-shadow: 0px 6px 10px rgba(0,0,0,0.5); cursor: pointer; font-family: 'Georgia', serif; text-shadow: 1px 1px 2px #000000;">
                    ⚔️ CLICCA QUI PER APRIRE LA CLASSIFICA FORZIERI UFC ⚔️
                </div>
            </a>
            ''', 
            unsafe_allow_html=True
        )

    # --- PAGINA 2: INFO & CHAT OPERATIVE PULITE ---
    elif page == "📋 Clan Info & Chats":
        st.markdown("<h1>📋 Alliance Info & Official Channels</h1>", unsafe_allow_html=True)
        st.write("Direttive operative e suddivisione dei canali di comunicazione ufficiali dei Raiders of Chaos.")
        
        st.divider()
        st.markdown("### ⚔️ Clan Chats & Descriptions")
        
        st.markdown(
            """
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold; font-family: 'Courier New';">[CHAT 1]</span> <b style="font-family: 'Courier New';">RoC Vaults</b><br>
                <span style="color: #dfdfdf; font-size: 15px;">- where you will register your created vault</span>
            </div>
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold; font-family: 'Courier New';">[CHAT 2]</span> <b style="font-family: 'Courier New';">RoC CP Swap Cities</b><br>
                <span style="color: #dfdfdf; font-size: 15px;">- where you check in/out CP cities</span>
            </div>
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold; font-family: 'Courier New';">[CHAT 3]</span> <b style="font-family: 'Courier New';">The Daily Raid</b><br>
                <span style="color: #dfdfdf; font-size: 15px;">- history of clan announcements</span>
            </div>
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold; font-family: 'Courier New';">[CHAT 4]</span> <b style="font-family: 'Courier New';">OPERATION EPIC DEMISE</b><br>
                <span style="color: #dfdfdf; font-size: 15px;">- epic monster targeting/coordination</span>
            </div>
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold; font-family: 'Courier New';">[CHAT 5]</span> <b style="font-family: 'Courier New';">ROC DARK OMENS</b><br>
                <span style="color: #dfdfdf; font-size: 15px;">- dedicated chat for Dark Omens event</span>
            </div>
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold; font-family: 'Courier New';">[CHAT 6]</span> <b style="font-family: 'Courier New';">ROC OLYMPUS</b><br>
                <span style="color: #dfdfdf; font-size: 15px;">- dedicated chat for Olympus event</span>
            </div>
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold; font-family: 'Courier New';">[CHAT 7]</span> <b style="font-family: 'Courier New';">ROC TORCH</b><br>
                <span style="color: #dfdfdf; font-size: 15px;">- dedicated to ensuring everyone's torch artifact is 5 stars</span>
            </div>
            <div class="chat-box" style="border-left: 4px solid #7c1a1a; background-color: #241b1b;">
                <span style="color: #ff4b4b; font-weight: bold; font-family: 'Courier New';">[SUB-CLAN]</span> <b style="font-family: 'Courier New';">((76 RoE))</b><br>
                <span style="color: #dfdfdf; font-size: 15px;">- K76 RoE details</span>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # --- NUOVA PAGINA 3: SCHEDA MINIMI RICHIESTI SEPARATA ---
    elif page == "📊 Event Minimums":
        st.markdown("<h1>📊 Official Event Minimums & Targets</h1>", unsafe_allow_html=True)
        st.write("Obiettivi minimi di coalizione richiesti per la partecipazione agli eventi del Regno.")
        
        st.divider()
        st.info("⚠️ **Participation required for events Ancients, Ragnarok, Olympus, and Dark Omens.**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 Event Minimums")
            st.write("- **Armageddon:** 50 chests")
            st.write("- **Ragnaroc:** 500m")
            st.write("- **Olympus:** 570.000")
            st.write("- **Dark Omens:** 100 clan chests, max oil deployed and fair share of defense")
            
        with col2:
            st.markdown("### 📈 Tracker Goals")
            st.write("- **Punti Minimi Settimanali:** 1.000.000 di punti")
            st.write("- **Vault Goals:** Bonus 100%, Summons: 5, Time: 49 minutes")
            st.write("- **Tinman Schedule Reset:** +0.5, +2, +4, -2, -1 (points only, not for kill)")
            st.write("- **Tinman Minimum:** 650M")
            st.write("- **Load number for upcoming week:** 722m (for 4 Ancients) (Ancient points your own weight)")

    # --- PAGINA 4: SCHEDA DISCORD ---
    elif page == "🌐 Discord Server":
        st.markdown("<h1>🌐 Official Raiders of Chaos Discord Server</h1>", unsafe_allow_html=True)
        st.write("Accedi alla base operativa vocale e strategica dell'alleanza su Discord.")
        
        st.divider()
        st.markdown("### 📡 Perché è fondamentale unirsi al server Discord?")
        st.markdown(
            """

