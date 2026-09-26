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
    /* Allineamento centrale per il blocco login di Streamlit */
    [data-testid="stVerticalBlock"] > div:has(img) {
        text-align: center !important;
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. FUNZIONE DI SICUREZZA (PASSWORD LOCK CON CENTRATURA INTEGRATA)
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    st.markdown("<br>", unsafe_allow_html=True)
    col_v1, col_login, col_v2 = st.columns(3)
    
    with col_login:
        # LETTURA DIRETTA DEL FILE SENZA PERCORSI HTML STRANI (Bypassa i blocchi del server)
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
    
    # BARRA LATERALE DI NAVIGAZIONE CON LOGO COMPATTO
    if os.path.exists("logo.png"):
        st.sidebar.image("logo.png", width=85) 
    else:
        st.sidebar.markdown("<h1 style='font-size: 38px; text-align: center; margin-bottom: 0px;'>🛡️</h1>", unsafe_allow_html=True)
        
    st.sidebar.markdown("<h2 style='font-size: 18px; text-align: center; margin-top: 0px;'>UFC Portal</h2>", unsafe_allow_html=True)
    page = st.sidebar.radio("NAVIGAZIONE:", ["🏠 Home Dashboard", "⚔️ Troops Calculator"])
    st.sidebar.markdown("---")
    st.sidebar.success("Portale protetto attivo.")

    # --- PAGINA 1: DASHBOARD ---
    if page == "🏠 Home Dashboard":
        st.markdown("<h1>🏠 UFC Command Center - Stato dell'Alleanza</h1>", unsafe_allow_html=True)
        st.write("Consulta la classifica ufficiale dei forzieri aggiornata in tempo reale dall'OCR dell'alleanza.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **Nota per i membri UFC:** Cliccando sul pulsante d'acciaio qui sotto, la classifica ufficiale si aprirà in una nuova scheda del browser in modalità protetta di Sola Lettura. Controlla i tuoi punti e gli obiettivi in totale sicurezza.")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Segnaposto temporaneo in attesa del link finale
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

    # --- PAGINA 2: CALCOLATORE TRUPPE INTERATTIVO ---
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
