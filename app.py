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
    
    # SELETTORE DELLA LINGUA RICHIESTO (SOLO INGLESE)
    lang = st.sidebar.selectbox("🌐 LANGUAGE:", ["English"])
    st.sidebar.markdown("---")

    # Menu laterale fisso e pulito in lingua inglese
    options = ["🏠 Home Dashboard", "📋 Clan Info & Chats", "📊 Event Minimums", "🌐 Discord Server", "⚔️ Troops Calculator"]
    page = st.sidebar.radio("NAVIGATION:", options)
    st.sidebar.markdown("---")
    
    # IL TUO LINK REALE DI GOOGLE SHEET CONFIGURATO
    GOOGLE_SHEET_LINK = "https://docs.google.com/spreadsheets/d/1yfJe8DyYX5QQmIBeXeW0BDfyv7A9FEw_mdDLmo3_VOQ/edit?usp=sharing"

    # --- PAGINA 0: HOME DASHBOARD ---
    if page == "🏠 Home Dashboard":
        st.markdown("<h1>🏠 UFC Command Center - Alliance Status</h1>", unsafe_allow_html=True)
        st.write("Check the official chest leaderboard updated in real-time by alliance OCR.")
        st.info("💡 **Notice for UFC Members:** By clicking the button below, the official leaderboard will open safely in a new browser tab in View-Only mode.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("⚔️ CLICK HERE TO OPEN UFC CHESTS LEADERBOARD ⚔️", GOOGLE_SHEET_LINK, use_container_width=True)

    # --- PAGINA 1: CLAN INFO & CHATS ---
    elif page == "📋 Clan Info & Chats":
        st.markdown("<h1>📋 Alliance Info and Official Channels</h1>", unsafe_allow_html=True)
        st.write("Operational directives and channels of Raiders of Chaos.")
        st.markdown("### ⚔️ Clan Chats & Descriptions")
        st.markdown(
            """
            <div class="chat-box"><b> RoC Vaults</b><br>- where you will register your created vault</div>
            <div class="chat-box"><b> RoC CP Swap Cities</b><br>- where you check in/out CP cities</div>
            <div class="chat-box"><b> The Daily Raid</b><br>- history of clan announcements</div>
            <div class="chat-box"><b> OPERATION EPIC DEMISE</b><br>- epic monster targeting/coordination</div>
            <div class="chat-box"><b> ROC DARK OMENS</b><br>- dedicated chat for Dark Omens event</div>
            <div class="chat-box"><b> ROC OLYMPUS</b><br>- dedicated chat for Olympus event</div>
            <div class="chat-box"><b> ROC TORCH</b><br>- dedicated to ensuring everyone torch artifact is 5 stars</div>
            <div class="chat-box" style="border-left: 4px solid #7c1a1a; background-color: #241b1b;"><b>[SUB-CLAN] ((76 RoE))</b><br>- K76 RoE details</div>
            """, unsafe_allow_html=True
        )

    # --- PAGINA 2: EVENT MINIMUMS ---
    elif page == "📊 Event Minimums":
        st.markdown("<h1>📊 Official Event Minimums and Targets</h1>", unsafe_allow_html=True)
        st.info("⚠️ Participation required for events Ancients, Armageddon, Ragnarok, Olympus, and Dark Omens.")
        st.markdown("### 📋 Monthly Minimums")
        st.write("- **Monthly Minimum Points:** 1,000,000 points total.")
        st.write("- **Armageddon Minimum:** 50 clan chests.")
        st.write("- **Dark Omens Minimum:** 100 epic clan chests.")
        st.markdown("### 📈 Score Updates & Rules")
        st.write("- **Epic Dark Omens:** Rewards **1,000 points** per chest.")
        st.write("- **Golden Pass:** Rewards **4,000 points** for each Triumphal Challenge chest (no longer a flat 20k bonus).")

    # --- PAGINA 3: DISCORD SERVER ---
    elif page == "🌐 Discord Server":
        st.markdown("<h1>🌐 Official Raiders of Chaos Discord Server</h1>", unsafe_allow_html=True)
        st.info("💡 The button below will be activated soon with the official invite code.")
        st.link_button("🔮 DISCORD BUTTON - COMING SOON 🔮", "https://discord.com", use_container_width=True)

    # --- PAGINA 4: TROOPS CALCULATOR ---
    elif page == "⚔️ Troops Calculator":
        st.markdown("<h1>⚔️ Official Alliance March Calculator</h1>", unsafe_allow_html=True)
        st.write("Access the most efficient stack and army simulator used by elite Total Battle players.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **Tactical Notice:** This button redirects you securely to the official Kaiculator. It dynamically factors in your Captains, Dragons, and multipliers for zero-loss runs.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("🛡️ OPEN OFFICIAL KAICULATOR 🛡️", "https://kaiculator.kaikaiju.com", use_container_width=True)
