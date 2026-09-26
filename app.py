import streamlit as st

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
    /* Centratura logo login */
    .login-logo {
        display: flex;
        justify-content: center;
        margin-bottom: -20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. FUNZIONE DI SICUREZZA (PASSWORD LOCK CON LOGO MEDIEVALE)
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    st.markdown("<br>", unsafe_allow_html=True)
    col_v1, col_login, col_v2 = st.columns(3)
    
    with col_login:
        # TRUCCO GRAFICO: Inseriamo l'icona ufficiale dello scudo da guerra centrato sopra i testi
        st.markdown(
            """
            <div class="login-logo">
                <img src="https://icons8.com" width="130" style="filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.7));">
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown("<h1 style='text-align: center; margin-top: 10px;'>🛡️ UFC HIGHLAND RAIDERS</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; font-size: 16px; letter-spacing: 1px;'>PORTALE ALLEANZA - ACCESSO RISERVATO</h3>", unsafe_allow_html=True)
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
    
    # BARRA LATERALE DI NAVIGAZIONE CON LOGO COORDINATO
    st.sidebar.image("https://icons8.com", width=60)
    st.sidebar.markdown("<h2 style='font-size: 22px; margin-top: 0px;'>UFC Portal</h2>", unsafe_allow_html=True)
    page = st.sidebar.radio("NAVIGAZIONE:", ["🏠 Home Dashboard", "⚔️ Troops Calculator"])
    st.sidebar.markdown("---")
    st.sidebar.success("Portale protetto attivo.")

    # --- PAGINA 1: DASHBOARD (In attesa del link finale) ---
    if page == "🏠 Home Dashboard":
        st.markdown("<h1>🏠 UFC Command Center - Stato dell'Alleanza</h1>", unsafe_allow_html=True)
        st.write("Consulta la classifica ufficiale dei forzieri aggiornata in tempo reale dall'OCR dell'alleanza.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Bacheca informazioni stile bacheca ordini
        st.info("💡 **Nota per i membri UFC:** Cliccando sul pulsante d'acciaio qui sotto, la classifica ufficiale si aprirà in una nuova scheda del browser in modalità protetta di Sola Lettura. Controlla i tuoi punti e gli obiettivi in totale sicurezza.")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Lasciamo il segnaposto temporaneo come stabilito!
        LINK_PULITO = "LAVORI_IN_CORSO"
        
        # Bottone d'acciaio rosso ad impatto visivo massimo
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


