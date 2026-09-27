import streamlit as st
import os
import json


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

# 2. SECURITY LOGIN
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
    # 3. PORTAL INTERFACE
    if os.path.exists("logo.png"):
        st.sidebar.image("logo.png", width=85)
    else:
        st.sidebar.markdown("<h1 style='font-size: 38px; text-align: center; margin-bottom: 0px;'>🛡️</h1>", unsafe_allow_html=True)
        
    st.sidebar.markdown("<h2 style='font-size: 18px; text-align: center; margin-top: 0px;'>UFC Portal</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
       # SELETTORE DELLA LINGUA RICHIESTO (COLLEGATO AI TUOI FILE JSON)
    import json
    lang_choice = st.sidebar.selectbox("🌐 LANGUAGE ", ["English", "Italiano", "Français", "Español", "Deutsch", "Русский", "Türkçe"])
    st.sidebar.markdown("---")

    # Mappatura dei file esterni caricati sul tuo GitHub
    lang_files = {"Italiano": "it.json", "Français": "fr.json", "Español": "es.json", "Deutsch": "de.json", "Русский": "ru.json", "Türkçe": "tr.json"}
    
    # Caricamento dinamico dei testi per la barra laterale
    ctx = {}
    if lang_choice in lang_files and os.path.exists(lang_files[lang_choice]):
        try:
            with open(lang_files[lang_choice], "r", encoding="utf-8") as f:
                ctx = json.load(f)
        except Exception:
            ctx = {}

    # Menu laterale che cambia lingua prendendo i dati dai tuoi JSON
    options = [
        ctx.get("menu_home", "🏠 Home Dashboard"),
        ctx.get("menu_info", "📋 Clan Info & Chats"),
        ctx.get("menu_min", "📊 Event Minimums"),
        ctx.get("menu_disc", "🌐 Discord Server"),
        ctx.get("menu_calc", "⚔️ Troops Calculator")
    ]
    page = st.sidebar.radio("NAVIGATION:", options)
    st.sidebar.markdown("---")

    
    # IL TUO LINK REALE DI GOOGLE SHEET CONFIGURATO
    GOOGLE_SHEET_LINK = "https://docs.google.com/spreadsheets/d/1yfJe8DyYX5QQmIBeXeW0BDfyv7A9FEw_mdDLmo3_VOQ/edit?usp=sharing"

       # --- PAGINA 0: HOME DASHBOARD ---
    if page in ["🏠 Home Dashboard", ctx.get("menu_home")]:
        st.markdown(f"<h1>{ctx.get('home_h1', '🏠 UFC Command Center - Alliance Status')}</h1>", unsafe_allow_html=True)
        st.write(ctx.get("home_write", "Check the official chest leaderboard updated in real-time by alliance OCR."))
        st.info(ctx.get("home_info", "💡 **Notice for UFC Members:** By clicking the button below, the official leaderboard will open safely in a new browser tab in View-Only mode."))
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button(ctx.get("home_btn", "⚔️ CLICK HERE TO OPEN UFC CHESTS LEADERBOARD ⚔️"), GOOGLE_SHEET_LINK, use_container_width=True)

    # --- PAGINA 1: CLAN INFO & CHATS ---
    elif page in ["📋 Clan Info & Chats", ctx.get("menu_info")]:
        st.markdown(f"<h1>{ctx.get('info_h1', '📋 Alliance Info and Official Channels')}</h1>", unsafe_allow_html=True)
        st.write(ctx.get("info_write", "Operational directives and channels of Raiders of Chaos."))
        st.markdown(ctx.get("info_h3", "### ⚔️ Clan Chats & Descriptions"))
        
        c1 = ctx.get("info_c1", "<b> RoC Vaults</b><br>- where you will register your created vault")
        c2 = ctx.get("info_c2", "<b> RoC CP Swap Cities</b><br>- where you check in/out CP cities")
        c3 = ctx.get("info_c3", "<b> The Daily Raid</b><br>- history of clan announcements")
        c4 = ctx.get("info_c4", "<b> OPERATION EPIC DEMISE</b><br>- epic monster targeting/coordination")
        c5 = ctx.get("info_c5", "<b> ROC DARK OMENS</b><br>- dedicated chat for Dark Omens event")
        c6 = ctx.get("info_c6", "<b> ROC OLYMPUS</b><br>- dedicated chat for Olympus event")
        c7 = ctx.get("info_c7", "<b> ROC TORCH</b><br>- dedicated to ensuring everyone torch artifact is 5 stars")
        sub = ctx.get("info_sub", "<b>[SUB-CLAN] ((76 RoE))</b><br>- K76 RoE details")
        
        st.markdown(
            f"""
            <div class="chat-box">{c1}</div>
            <div class="chat-box">{c2}</div>
            <div class="chat-box">{c3}</div>
            <div class="chat-box">{c4}</div>
            <div class="chat-box">{c5}</div>
            <div class="chat-box">{c6}</div>
            <div class="chat-box">{c7}</div>
            <div class="chat-box" style="border-left: 4px solid #7c1a1a; background-color: #241b1b;">{sub}</div>
            """, unsafe_allow_html=True
        )

    # --- PAGINA 2: EVENT MINIMUMS ---
    elif page in ["📊 Event Minimums", ctx.get("menu_min")]:
        st.markdown(f"<h1>{ctx.get('min_h1', '📊 Official Event Minimums and Targets')}</h1>", unsafe_allow_html=True)
        st.info(ctx.get("min_info", "⚠️ Participation required for events Ancients, Armageddon, Ragnarok, Olympus, and Dark Omens."))
        st.markdown(ctx.get("min_h3", "### 📋 Monthly Minimums"))
        st.write(ctx.get("min_w1", "- **Monthly Minimum Points:** 1,000,000 points total."))
        st.write(ctx.get("min_w2", "- **Armageddon:** 50 chests"))
        st.write(ctx.get("min_w3", "- **Ragnaroc:** 500m"))
        st.write(ctx.get("min_w4", "- **Olympus:** 570,000"))
        st.write(ctx.get("min_w5", "- **Dark Omens:** 100 clan chests, max oil deployed and fair share of defense"))

    # --- PAGINA 3: DISCORD SERVER ---
    elif page in ["🌐 Discord Server", ctx.get("menu_disc")]:
        st.markdown(f"<h1>{ctx.get('disc_h1', '🌐 Official Raiders of Chaos Discord Server')}</h1>", unsafe_allow_html=True)
        st.info(ctx.get("disc_info", "💡 The button below will be activated soon with the official invite code."))
        st.link_button(ctx.get("disc_btn", "🔮 DISCORD BUTTON - COMING SOON 🔮"), "https://discord.com", use_container_width=True)

    # --- PAGINA 4: TROOPS CALCULATOR ---
    elif page in ["⚔️ Troops Calculator", ctx.get("menu_calc")]:
        st.markdown(f"<h1>{ctx.get('calc_h1', '⚔️ Official Alliance March Calculator')}</h1>", unsafe_allow_html=True)
        st.write(ctx.get("calc_write", "Access the most efficient stack and army simulator used by elite Total Battle players."))
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(ctx.get("calc_info", "💡 **Tactical Notice:** This button redirects you securely to the official Kaiculator. It dynamically factors in your Captains, Dragons, and multipliers for zero-loss runs."))
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button(ctx.get("calc_btn", "🛡️ OPEN OFFICIAL KAICULATOR 🛡️"), "https://kaiculator.kaikaiju.com", use_container_width=True)

