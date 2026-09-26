import streamlit as st
import os

# 1. SITE CONFIGURATION & DARK WAR THEME
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

# 2. SECURITY FUNCTION (PASSWORD LOCK)
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
        st.markdown("<h3 style='text-align: center; font-size: 13px; letter-spacing: 2px; color: #bd9b53;'>ALLIANCE PORTAL - RESTRICTED ACCESS</h3>", unsafe_allow_html=True)
        password_entered = st.text_input("CLAN PASSWORD:", type="password", placeholder="Enter access code...")
        
        if st.button("ACCESS PORTAL", width='stretch'):
            if password_entered == "UFC_Raiders_2026": 
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Incorrect password! Ask the generals for the correct code.")
    return False

# 3. LOGGED IN PORTAL INTERFACE
if check_password():
    if os.path.exists("logo.png"):
        st.sidebar.image("logo.png", width=85) 
    else:
        st.sidebar.markdown("<h1 style='font-size: 38px; text-align: center; margin-bottom: 0px;'>🛡️</h1>", unsafe_allow_html=True)
        
    st.sidebar.markdown("<h2 style='font-size: 18px; text-align: center; margin-top: 0px;'>UFC Portal</h2>", unsafe_allow_html=True)
    page = st.sidebar.radio("NAVIGATION:", ["🏠 Home Dashboard", "📋 Clan Info & Chats", "📊 Event Minimums", "🌐 Discord Server", "⚔️ Troops Calculator"])
    st.sidebar.markdown("---")
    st.sidebar.success("Protected portal active.")

    # --- PAGE 1: DASHBOARD ---
    if page == "🏠 Home Dashboard":
        st.markdown("<h1>🏠 UFC Command Center - Alliance Status</h1>", unsafe_allow_html=True)
        st.write("Check the official chest leaderboard updated in real-time by alliance OCR.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **Notice for UFC Members:** By clicking the button below, the official leaderboard will open safely in a new browser tab in View-Only mode.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("⚔️ CLICK HERE TO OPEN UFC CHESTS LEADERBOARD ⚔️", "https://google.com", use_container_width=True)

    # --- PAGE 2: INFO & CHATS ---
    elif page == "📋 Clan Info & Chats":
        st.markdown("<h1>📋 Alliance Info & Official Channels</h1>", unsafe_allow_html=True)
        st.write("Operational directives and official communication channels of the Raiders of Chaos.")
        st.divider()
        st.markdown("### ⚔️ Clan Chats & Descriptions")
        
        st.markdown(
            """
            <div class="chat-box"><b>[CHAT 1] RoC Vaults</b><br>- where you will register your created vault</div>
            <div class="chat-box"><b>[CHAT 2] RoC CP Swap Cities</b><br>- where you check in/out CP cities</div>
            <div class="chat-box"><b>[CHAT 3] The Daily Raid</b><br>- history of clan announcements</div>
            <div class="chat-box"><b>[CHAT 4] OPERATION EPIC DEMISE</b><br>- epic monster targeting/coordination</div>
            <div class="chat-box"><b>[CHAT 5] ROC DARK OMENS</b><br>- dedicated chat for Dark Omens event</div>
            <div class="chat-box"><b>[CHAT 6] ROC OLYMPUS</b><br>- dedicated chat for Olympus event</div>
            <div class="chat-box"><b>[CHAT 7] ROC TORCH</b><br>- dedicated to ensuring everyone's torch artifact is 5 stars</div>
            <div class="chat-box" style="border-left: 4px solid #7c1a1a; background-color: #241b1b;"><b>[SUB-CLAN] ((76 RoE))</b><br>- K76 RoE details</div>
            """, 
            unsafe_allow_html=True
        )

    # --- PAGE 3: EVENT MINIMUMS ---
    elif page == "📊 Event Minimums":
        st.markdown("<h1>📊 Official Event Minimums & Targets</h1>", unsafe_allow_html=True)
        st.write("Minimum coalition targets required for event participation.")
        st.divider()
        st.info("⚠️ Participation required for events Ancients, Ragnarok, Olympus, and Dark Omens.")
        
        st.markdown("### 📋 Event Minimums")
        st.write("- **Monthly Minimum Points:** 1,000,000 points *(points to earn with level 30 rare crypts, level 30/35 epic crypts)*")
        st.write("- **Armageddon:** 50 chests")
        st.write("- **Ragnaroc:** 500m")
        st.write("- **Olympus:** 570.000")
        st.write("- **Dark Omens:** 100 clan chests, max oil deployed and fair share of defense")

    # --- PAGE 4: DISCORD ---
    elif page == "🌐 Discord Server":
        st.markdown("<h1>🌐 Official Raiders of Chaos Discord Server</h1>", unsafe_allow_html=True)
        st.write("Access the alliance's voice and strategic operational base on Discord.")
        st.divider()
        st.info("💡 Access instructions: The button below will be activated soon with the official invite code.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("🔮 DISCORD BUTTON - COMING SOON 🔮", "https://discord.com", use_container_width=True)

    # --- PAGE 5: TROOPS CALCULATOR ---
    elif page == "⚔️ Troops Calculator":
        st.markdown("<h1>⚔️ UFC Tactical Manual & March Simulator</h1>", unsafe_allow_html=True)
        capacity = st.slider("Select your maximum march capacity:", 10000, 600000, 200000, step=5000)
        target = st.selectbox("Select attack target:", ["Level 35 Crypts", "Alliance Citadels"])
        
        if target == "Level 35 Crypts":
            infantry = int(capacity * 0.6)
            archers = int(capacity * 0.4)
            st.success(f"💥 Crypt Configuration: Send {infantry:,} Infantry and {archers:,} Archers.")
        else:
            st.warning("⚠️ Coalition Order: Send the entire balanced army according to directives.")
