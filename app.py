import streamlit as st
import os

st.set_page_config(page_title="UFC Command Center", layout="wide", page_icon="🛡️")

if "lang" not in st.session_state:
    st.session_state["lang"] = "English"

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

# MULTILANGUAGE TEXTS (SANITY CHECKED)
translations = {
    "English": {
        "sub": "ALLIANCE PORTAL - RESTRICTED ACCESS", "pass": "CLAN PASSWORD:", "ph": "Enter access code...",
        "btn": "ACCESS PORTAL", "err": "❌ Incorrect password! Ask the generals for the correct code.",
        "nav": ["🏠 Home Dashboard", "📋 Clan Info & Chats", "📊 Event Minimums", "🌐 Discord Server", "⚔️ Troops Calculator"],
        "status": "Protected portal active.",
        "h1_home": "🏠 UFC Command Center - Alliance Status", "w_home": "Check the official chest leaderboard updated in real-time by alliance OCR.",
        "info_home": "💡 **Notice for UFC Members:** By clicking the button below, the official leaderboard will open safely in a new browser tab in View-Only mode.",
        "btn_home": "⚔️ CLICK HERE TO OPEN UFC CHESTS LEADERBOARD ⚔️",
        "h1_info": "📋 Alliance Info & Official Channels", "w_info": "Operational directives and official communication channels of the Raiders of Chaos.",
        "sub_info": "### ⚔️ Clan Chats & Descriptions",
        "h1_min": "📊 Official Event Minimums & Targets", "w_min": "Minimum coalition targets required for event participation.",
        "warn_min": "⚠️ Participation required for events Ancients, Ragnarok, Olympus, and Dark Omens.",
        "pt_min": "- **Monthly Minimum Points:** 1,000,000 points *(points to earn with level 30 rare crypts, level 30/35 epic crypts, and epic monster chests)*",
        "h1_disc": "🌐 Official Raiders of Chaos Discord Server", "w_disc": "Access the alliance voice and strategic operational base on Discord.",
        "inf_disc": "💡 Access instructions: The button below will be activated soon with the official invite code.", "btn_disc": "🔮 DISCORD BUTTON - COMING SOON 🔮",
        "h1_calc": "⚔️ UFC Tactical Manual & March Simulator", "sl_calc": "Select your maximum march capacity:", "sb_calc": "Select attack target:",
        "opts_calc": ["Level 35 Crypts", "Alliance Citadels"], "res_title": "📋 Recommended Army Composition:",
        "res_crypt": "💥 **Crypt Configuration:** Send **{inf:,} Infantry** and **{arc:,} Archers** (Optimized for zero losses).",
        "res_cit": "⚠️ **Coalition Order:** Send the entire balanced army according to directives."
    },
    "Italiano": {
        "sub": "PORTALE ALLEANZA - ACCESSO RISERVATO", "pass": "PASSWORD CLAN:", "ph": "Inserisci il codice d'accesso...",
        "btn": "ACCEDI AL PORTALE", "err": "❌ Password errata! Chiedi il codice corretto ai generali.",
        "nav": ["🏠 Dashboard Principale", "📋 Info Clan & Chat", "📊 Minimi Richiesti", "🌐 Server Discord", "⚔️ Calcolatore Truppe"],
        "status": "Portale protetto attivo.",
        "h1_home": "🏠 UFC Command Center - Stato dell'Alleanza", "w_home": "Consulta la classifica ufficiale dei forzieri aggiornata in tempo reale dall'OCR dell'alleanza.",
        "info_home": "💡 **Nota per i membri UFC:** Cliccando sul pulsante qui sotto, la classifica ufficiale si aprirà in una nuova scheda del browser in modalità protetta di Sola Lettura.",
        "btn_home": "⚔️ CLICCA QUI PER APRIRE LA CLASSIFICA FORZIERI UFC ⚔️",
        "h1_info": "📋 Informazioni Clan & Canali Ufficiali", "w_info": "Direttive operative e suddivisione dei canali di comunicazione ufficiali dei Raiders of Chaos.",
        "sub_info": "### ⚔️ Chat del Clan & Descrizioni Tattiche",
        "h1_min": "📊 Minimi Richiesti per gli Eventi", "w_min": "Obiettivi minimi di coalizione obbligatori per la partecipazione agli eventi del Regno.",
        "warn_min": "⚠️ La partecipazione è richiesta per gli eventi Antichi, Ragnarok, Olympus e Dark Omens.",
        "pt_min": "- **Punti Minimi Mensili:** 1.000.000 di punti *(punti da guadagnare tramite cripte rare liv 30, cripte epiche liv 30/35 e forzieri dei mostri epici)*",
        "h1_disc": "🌐 Server Discord Ufficiale Raiders of Chaos", "w_disc": "Accedi alla base operativa vocale e strategica dell'alleanza su Discord.",
        "inf_disc": "💡 Istruzioni per l'accesso: Il pulsante qui sotto verrà attivato a breve con il codice d'invito ufficiale.", "btn_disc": "🔮 PULSANTE DISCORD - IN ALLESTIMENTO 🔮",
        "h1_calc": "⚔️ Manuale Tattico UFC & Simulatore Marce", "sl_calc": "Seleziona la tua capacità di marcia massima:", "sb_calc": "Seleziona il bersaglio dell'attacco:",
        "opts_calc": ["Cripte Livello 35", "Cittadelle dell'Alleanza"], "res_title": "📋 Composizione Esercito Consigliata:",
        "res_crypt": "💥 **Configurazione Cripte:** Manda **{inf:,} Fanteria** e **{arc:,} Arcieri** (Ottimizzato per zero perdite).",
        "res_cit": "⚠️ **Ordine di Coalizione:** Manda l'intero esercito bilanciato secondo le direttive del Maresciallo."
    },
    "Français": {
        "sub": "PORTAIL DE L ALLIANCE - ACCES RESTREINT", "pass": "MOT DE PASSE DU CLAN:", "ph": "Entrez le code d acces...",
        "btn": "ACCEDER AU PORTAIL", "err": "❌ Mot de passe incorrect ! Demandez le code aux generaux.",
        "nav": ["🏠 Tableau de Bord", "📋 Infos & Chats du Clan", "📊 Minimums des Evenements", "🌐 Serveur Discord", "⚔️ Simulateur de Troupes"],
        "status": "Portail protege actif.",
        "h1_home": "🏠 UFC Command Center - Statut de l Alliance", "w_home": "Consultez le classement officiel des coffres mis a jour en temps reel.",
        "info_home": "💡 **Avis aux membres:** En cliquant ci-dessous, le classement s ouvrira en mode lecture seule.",
        "btn_home": "⚔️ CLIQUEZ ICI POUR OUVRIR LE CLASSEMENT DES COFFRES ⚔️",
        "h1_info": "📋 Infos de l Alliance & Canaux Officiels", "w_info": "Directives operationnelles des Raiders of Chaos.",
        "sub_info": "### ⚔️ Chats du Clan & Descriptions",
        "h1_min": "📊 Minimums et Objectifs des Evenements", "w_min": "Objectifs minimums requis pour participer.",
        "warn_min": "⚠️ Participation obligatoire aux Ancients, Ragnarok, Olympus et Dark Omens.",
        "pt_min": "- **Points Minimums Mensuels:** 1 000 000 points *(cryptes rares niv 30, cryptes epiques niv 30/35, et coffres de monstres epiques)*",
        "h1_disc": "🌐 Serveur Discord Officiel", "w_disc": "Accedez a la base operationnelle sur Discord.",
        "inf_disc": "💡 Le bouton ci-dessous sera bientot active.", "btn_disc": "🔮 BOUTON DISCORD - BIENTOT DISPONIBLE 🔮",
        "h1_calc": "⚔️ Manuel Tactique & Simulateur de Marche", "sl_calc": "Capacite maximale de marche:", "sb_calc": "Cible de l attaque:",
        "opts_calc": ["Cryptes Niveau 35", "Citadelles de l Alliance"], "res_title": "📋 Composition d Armee Recommandee:",
        "res_crypt": "💥 **Configuration:** Envoyez **{inf:,} Infanterie** et **{arc:,} Archers**.",
        "res_cit": "⚠️ **Ordre de Coalition:** Envoyez toute l armee equilibree."
    },
    "Español": {
        "sub": "PORTAL DE ALIANZA - ACCESO RESTRINGIDO", "pass": "CONTRASENA DEL CLAN:", "ph": "Ingrese el codigo...",
        "btn": "ACCEDER AL PORTAL", "err": "❌ ¡Contrasena incorrecta! Pidela a los generales.",
        "nav": ["🏠 Panel Principal", "📋 Info y Chats", "📊 Minimos de Eventos", "🌐 Servidor de Discord", "⚔️ Calculadora de Tropas"],
        "status": "Portal protegido activo.",
        "h1_home": "🏠 UFC Command Center - Estado de Alianza", "w_home": "Consulta la clasificacion de cofres en tiempo real.",
        "info_home": "💡 **Aviso:** El boton abrira la tabla de clasificacion en una nueva pestana.",
        "btn_home": "⚔️ CLIC AQUI PARA ABRIR LA CLASIFICACION ⚔️",
        "h1_info": "📋 Info de Alianza y Canales", "w_info": "Directivas operativas de los Raiders of Chaos.",
        "sub_info": "### ⚔️ Chats del Clan y Descripciones",
        "h1_min": "📊 Minimos y Objetivos Oficiales", "w_min": "Objetivos minimos de coalicion requeridos.",
        "warn_min": "⚠️ Participacion requerida en Ancients, Ragnarok, Olympus y Dark Omens.",
        "pt_min": "- **Puntos Minimos Mensuales:** 1,000,000 puntos *(criptas raras niv 30, epicas niv 30/35 y cofres de monstruos epicos)*",
        "h1_disc": "🌐 Servidor Discord Oficial", "w_disc": "Accede a la base estrategica en Discord.",
        "inf_disc": "💡 El boton se activara pronto.", "btn_disc": "🔮 BOTON DISCORD - PROXIMAMENTE 🔮",
        "h1_calc": "⚔️ Manual Tactico y Simulador", "sl_calc": "Capacidad maxima de marcha:", "sb_calc": "Seleccionar objetivo:",
        "opts_calc": ["Criptas Nivel 35", "Ciudadela de Alianza"], "res_title": "📋 Composicion de Ejercito Recomendada:",
        "res_crypt": "💥 **Configuracion:** Enviar **{inf:,} Infanteria** y **{arc:,} Arqueros**.",
        "res_cit": "⚠️ **Orden de Coalition:** Enviar el ejercito completo y equilibrado."
    },
    "Deutsch": {
        "sub": "ALLIANZ PORTAL - GESCHÜTZTER ZUGANG", "pass": "KLAN PASSWORT:", "ph": "Zugangscode eingeben...",
        "btn": "PORTAL BETRETEN", "err": "❌ Falsches Passwort! Frage die Generale.",
        "nav": ["🏠 Haupt Dashboard", "📋 Klan Infos & Chats", "📊 Event Mindestwerte", "🌐 Discord Server", "⚔️ Truppen Rechner"],
