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
        font-family: 'Courier New', Courier, monospace;
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
    
    # BARRA LATERALE DI NAVIGAZIONE
    if os.path.exists("logo.png"):
        st.sidebar.image("logo.png", width=85) 
    else:
        st.sidebar.markdown("<h1 style='font-size: 38px; text-align: center; margin-bottom: 0px;'>🛡️</h1>", unsafe_allow_html=True)
        
    st.sidebar.markdown("<h2 style='font-size: 18px; text-align: center; margin-top: 0px;'>UFC Portal</h2>", unsafe_allow_html=True)
    page = st.sidebar.radio("NAVIGAZIONE:", ["🏠 Home Dashboard", "📋 Clan Info & Chats", "⚔️ Troops Calculator"])
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

    # --- PAGINA 2: LE TUE CHAT REALI DEL CLAN ---
    elif page == "📋 Clan Info & Chats":
        st.markdown("<h1>📋 Alliance Info & Official Channels</h1>", unsafe_allow_html=True)
        st.write("Direttive operative e suddivisione dei canali di comunicazione ufficiali dei Raiders of Chaos.")
        
        st.divider()
        st.markdown("### ⚔️ Tactical In-Game & Discord Chats")
        st.write("Rimani sincronizzato sui canali operativi corretti in base alle attività militari in corso.")
        
        # Iniezione della tua lista esatta senza toccare maiuscole e minuscole
        st.markdown(
            """
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold;">[CHAT 1]</span> <b>RoC Vaults</b><br>
                <span style="color: #dfdfdf; font-size: 14px;">Canale tattico dedicato al coordinamento e al tracciamento dei forzieri e delle cripte di alleanza.</span>
            </div>
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold;">[CHAT 2]</span> <b>RoC CP Swap Cities</b><br>
                <span style="color: #dfdfdf; font-size: 14px;">Coordinamento militare per la gestione, lo scambio e il controllo dei punti di controllo e delle città.</span>
            </div>
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold;">[CHAT 3]</span> <b>The Daily Raid</b><br>
                <span style="color: #dfdfdf; font-size: 14px;">Canale operativo per gli attacchi giornalieri continui e i raduni standard dell'alleanza.</span>
            </div>
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold;">[CHAT 4]</span> <b>OPERATION EPIC DEMISE</b><br>
                <span style="color: #dfdfdf; font-size: 14px;">Chat di coalizione per le manovre di attacco su larga scala contro i boss e mostri epici del regno.</span>
            </div>
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold;">[CHAT 5]</span> <b>ROC DARK OMENS</b><br>
                <span style="color: #dfdfdf; font-size: 14px;">Canale strategico d'avanguardia riservato alle direttive e agli avvisi critici dei Generali.</span>
            </div>
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold;">[CHAT 6]</span> <b>ROC OLYMPUS</b><br>
                <span style="color: #dfdfdf; font-size: 14px;">Coordinamento per gli eventi supremi del server, tornei maggiori e battaglie d'élite.</span>
            </div>
            <div class="chat-box">
                <span style="color: #bd9b53; font-weight: bold;">[CHAT 7]</span> <b>ROC TORCH</b><br>
                <span style="color: #dfdfdf; font-size: 14px;">Canale di supporto tattico, logistica e comunicazioni interne del Clan.</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.divider()
        st.markdown("### 📜 Weekly Regulations")
        st.info("⚠️ Tutti i membri sono tenuti a seguire i canali sopra indicati e gli obiettivi settimanali estratti dal sistema OCR.")

    # --- PAGINA 3: CALCOLATORE TRUPPE ---
    elif page == "⚔️ Troops Calculator":
        st.markdown("<h1>⚔️ Manuale Tattico UFC & Simulatore Marce</h1>", unsafe_allow_html=True)
        st.write("Imposta la tua capacità massima dell'eroe per calcolare la configurazione ottimale dell'esercito.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        capacity = st.slider("Seleziona la tua capacità di marcia massima:", 10000, 600000, 200000, step=5000)
        target = st.selectbox("Seleziona il bersaglio dell'attacco:", ["Cripte Livello 35", "Cittadelle dell'Alleanza", "Squadre Non-Morti Epiche"])
        
        st.markdown("<br><h3>📋 Composizione Esercito Consigliata:</h3>", unsafe_allow_html=True)
        if target == "Cripte Livello 35":
            infantry = int(capacity * 0.6)
            archers = int(capacity * 0.4)
            st.success(f"💥 **Configurazione Cripte:** Manda **{infantry:,} Fanteria** e **{archers:,} Arcieri** (Ottimizzato per zero perdite).".replace(",", "."))
        elif target == "Cittadelle dell'Alleanza":
            st.warning("⚠️ **Ordine di Coalizione:** Manda l'intero esercito bilanciato secondo le precise direttive del Maresciallo in chat di gioco.")
        else:
            balanced = int(capacity / 3)
            st.info(f"📌 **Configurazione Standard:** Manda una ripartizione perfetta: **{balanced:,} Fanteria, {balanced:,} Arcieri, {balanced:,} Cavalleria**.".replace(",", "."))

   
