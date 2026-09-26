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

translations = {
    "English": {
        "sub": "ALLIANCE PORTAL - RESTRICTED ACCESS", "pass": "CLAN PASSWORD:", "ph": "Enter access code...",
        "btn": "ACCESS PORTAL", "err": "Incorrect password",
        "nav": ["Home Dashboard", "Clan Info and Chats", "Event Minimums", "Discord Server", "Troops Calculator"],
        "status": "Protected portal active.",
        "h1_home": "UFC Command Center - Alliance Status", "w_home": "Check the official chest leaderboard updated in real-time by alliance OCR.",
        "info_home": "Notice for UFC Members: By clicking the button below, the leaderboard will open safely in view mode.",
        "btn_home": "CLICK HERE TO OPEN UFC CHESTS LEADERBOARD",
        "h1_info": "Alliance Info and Official Channels", "w_info": "Operational directives and channels of Raiders of Chaos.",
        "sub_info": "Clan Chats and Descriptions",
        "h1_min": "Official Event Minimums and Targets", "w_min": "Minimum coalition targets required for event participation.",
        "warn_min": "Participation required for events Ancients, Ragnarok, Olympus, and Dark Omens.",
        "pt_min": "Monthly Minimum Points: 1,000,000 points (crypts level 30 rare, level 30/35 epic, and epic monster chests)",
        "h1_disc": "Official Raiders of Chaos Discord Server", "w_disc": "Access the alliance voice and strategic base on Discord.",
        "inf_disc": "The button below will be activated soon with the official invite code.", "btn_disc": "DISCORD BUTTON - COMING SOON",
        "h1_calc": "UFC Tactical Manual and March Simulator", "sl_calc": "Select your maximum march capacity:", "sb_calc": "Select attack target:",
        "opts_calc": ["Level 35 Crypts", "Alliance Citadels"], "res_title": "Recommended Army Composition:",
        "res_crypt": "Crypt Configuration: Send {inf} Infantry and {arc} Archers.",
        "res_cit": "Coalition Order: Send the entire balanced army according to directives."
    },
    "Italiano": {
        "sub": "PORTALE ALLEANZA - ACCESSO RISERVATO", "pass": "PASSWORD CLAN:", "ph": "Inserisci il codice...",
        "btn": "ACCEDI AL PORTALE", "err": "Password errata",
        "nav": ["Dashboard Principale", "Info Clan and Chat", "Minimi Richiesti", "Server Discord", "Calcolatore Truppe"],
        "status": "Portale protetto attivo.",
        "h1_home": "UFC Command Center - Stato dell Alleanza", "w_home": "Consulta la classifica ufficiale dei forzieri in tempo reale.",
        "info_home": "Nota per i membri UFC: Cliccando sul pulsante sotto, la classifica si aprira in Sola Lettura.",
        "btn_home": "CLICCA QUI PER APRIRE LA CLASSIFICA FORZIERI UFC",
        "h1_info": "Informazioni Clan and Canali Ufficiali", "w_info": "Direttive operative dei Raiders of Chaos.",
        "sub_info": "Chat del Clan and Descrizioni Tattiche",
        "h1_min": "Minimi Richiesti per gli Eventi", "w_min": "Obiettivi minimi obbligatori per la partecipazione agli eventi.",
        "warn_min": "La partecipazione e richiesta per gli eventi Antichi, Ragnarok, Olympus e Dark Omens.",
        "pt_min": "Punti Minimi Mensili: 1.000.000 di punti (cripte rare liv 30, cripte epiche liv 30/35 e forzieri mostri epici)",
        "h1_disc": "Server Discord Ufficiale Raiders of Chaos", "w_disc": "Accedi alla base operativa vocale su Discord.",
        "inf_disc": "Il pulsante qui sotto verra attivato a breve con il codice d invito.", "btn_disc": "PULSANTE DISCORD - IN ALLESTIMENTO",
        "h1_calc": "Manuale Tattico UFC and Simulatore Marce", "sl_calc": "Seleziona la tua capacita di marcia massima:", "sb_calc": "Seleziona il bersaglio dell attacco:",
        "opts_calc": ["Cripte Livello 35", "Cittadelle dell Alleanza"], "res_title": "Composizione Esercito Consigliata:",
        "res_crypt": "Configurazione Cripte: Manda {inf} Fanteria e {arc} Arcieri.",
        "res_cit": "Ordine di Coalizione: Manda l intero esercito bilanciato."
    },
    "Français": {
        "sub": "PORTAIL DE L ALLIANCE - ACCES RESTREINT", "pass": "MOT DE PASSE:", "ph": "Entrez le code...",
        "btn": "ACCEDER AU PORTAIL", "err": "Mot de passe incorrect",
        "nav": ["Tableau de Bord", "Infos and Chats", "Minimums", "Serveur Discord", "Simulateur"],
        "status": "Portail protege actif.",
        "h1_home": "UFC Command Center - Statut", "w_home": "Consultez le classement officiel des coffres.",
        "info_home": "Avis aux membres: Le classement s ouvrira en mode lecture seule.",
        "btn_home": "CLIQUEZ ICI POUR OUVRIR LE CLASSEMENT",
        "h1_info": "Infos de l Alliance", "w_info": "Directives operationnelles des Raiders of Chaos.",
        "sub_info": "Chats du Clan",
        "h1_min": "Minimums et Objectifs", "w_min": "Objectifs minimums requis pour participer.",
        "warn_min": "Participation obligatoire aux Ancients, Ragnarok, Olympus et Dark Omens.",
        "pt_min": "Points Minimums Mensuels: 1 000 000 points (cryptes rare 30, cryptes epique 30/35, et coffres de monstres)",
        "h1_disc": "Serveur Discord Officiel", "w_disc": "Accedez a la base operationnelle sur Discord.",
        "inf_disc": "Le bouton ci-dessous sera bientot active.", "btn_disc": "BOUTON DISCORD - BIENTOT DISPONIBLE",
        "h1_calc": "Manuel Tactique", "sl_calc": "Capacite maximale de marche:", "sb_calc": "Cible de l attaque:",
        "opts_calc": ["Cryptes Niveau 35", "Citadelles"], "res_title": "Composition recommandee:",
        "res_crypt": "Configuration: Envoyez {inf} Infanterie et {arc} Archers.",
        "res_cit": "Ordre de Coalition: Envoyez toute l armee equilibree."
    },
    "Español": {
        "sub": "PORTAL DE ALIANZA - ACCESO RESTRINGIDO", "pass": "CONTRASENA:", "ph": "Ingrese el codigo...",
        "btn": "ACCEDER", "err": "Contrasena incorrecta",
        "nav": ["Panel Principal", "Info y Chats", "Minimos de Eventos", "Servidor Discord", "Calculadora"],
        "status": "Portal protegido activo.",
        "h1_home": "UFC Command Center - Estado", "w_home": "Consulta la clasificacion de cofres.",
        "info_home": "Aviso: El boton abrira la tabla de clasificacion en View-Only.",
        "btn_home": "CLIC AQUI PARA ABRIR LA CLASIFICACION",
        "h1_info": "Info de Alianza", "w_info": "Directivas operativas de Raiders of Chaos.",
        "sub_info": "Chats del Clan",
        "h1_min": "Minimos Oficiales", "w_min": "Objetivos minimos de coalicion requeridos.",
        "warn_min": "Participacion requerida en Ancients, Ragnarok, Olympus y Dark Omens.",
        "pt_min": "Puntos Minimos Mensuales: 1,000,000 puntos (criptas raras 30, epicas 30/35 y monstruos epicos)",
        "h1_disc": "Servidor Discord Oficial", "w_disc": "Accede a la base estrategica en Discord.",
        "inf_disc": "El boton se activara pronto.", "btn_disc": "BOTON DISCORD - PROXIMAMENTE",
        "h1_calc": "Manual Tactico", "sl_calc": "Capacidad maxima de marcha:", "sb_calc": "Seleccionar objetivo:",
        "opts_calc": ["Criptas Nivel 35", "Ciudadela"], "res_title": "Composicion recomendada:",
        "res_crypt": "Configuracion: Enviar {inf} Infanteria y {arc} Arqueros.",
        "res_cit": "Orden de Coalition: Enviar el ejercito completo."
    },
    "Deutsch": {
        "sub": "ALLIANZ PORTAL - GESCHÜTZTER ZUGANG", "pass": "PASSWORT:", "ph": "Code eingeben...",
        "btn": "PORTAL BETRETEN", "err": "Falsches Passwort",
        "nav": ["Haupt Dashboard", "Klan Infos", "Event Mindestwerte", "Discord Server", "Truppen Rechner"],
        "status": "Geschutztes Portal aktiv.",
        "h1_home": "UFC Command Center - Allianz Status", "w_home": "Überprufe die offizielle Bestenliste.",
        "info_home": "Hinweis: Die Bestenliste offnet sich in einem neuen Tab.",
        "btn_home": "HIER KLICKEN FÜR BESTENLISTE",
        "h1_info": "Allianz Infos", "w_info": "Einsatzrichtlinien der Raiders of Chaos.",
        "sub_info": "Klan Chats Beschreibungen",
        "h1_min": "Offizielle Mindestwerte", "w_min": "Erforderliche Mindestziele fur die Teilnahme.",
        "warn_min": "Teilnahme erforderlich fur Ancients, Ragnarok, Olympus und Dark Omens.",
        "pt_min": "Monatliche Mindestpunkte: 1.000.000 Punkte (Stufe 30 Krypten, Stufe 30/35 epische Krypten)",
        "h1_disc": "Offizieller Discord Server", "w_disc": "Greife auf die Basis auf Discord zu.",
        "inf_disc": "Der Button wird bald aktiviert.", "btn_disc": "DISCORD BUTTON - DEMNÄCHST",
        "h1_calc": "Marsch Simulator", "sl_calc": "Maximale Marschkapazitat:", "sb_calc": "Angriffsziel wählen:",
        "opts_calc": ["Krypten Stufe 35", "Zitadellen"], "res_title": "Empfohlene Armee:",
        "res_crypt": "Krypta Konfiguration: Sende {inf} Infanterie und {arc} Bogenschutzen.",
        "res_cit": "Koalitionsbefehl: Sende die gesamte Armee."
    },
    "Русский": {
        "sub": "ПОРТАЛ АЛЬЯНСА - ОГРАНИЧЕННЫЙ ДОСТУП", "pass": "ПАРОЛЬ КЛАНА:", "ph": "Введите код...",
        "btn": "ВОЙТИ НА ПОРТАЛ", "err": "Неверный пароль",
