import streamlit as st

# 1. WEBSITE SETTINGS
st.set_page_config(page_title="UFC Command Center", layout="wide", page_icon="🛡️")

# 2. SECURITY FUNCTION (PASSWORD LOCK)
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    st.markdown("<br><br>", unsafe_allow_html=True)
    col_v1, col_login, col_v2 = st.columns(3)
    
    with col_login:
        st.title("🛡️ UFC Highland Raiders")
        st.subheader("Alliance Portal - Restricted Access")
        password_entered = st.text_input("CLAN PASSWORD:", type="password", placeholder="Enter alliance security code...")
        
        if st.button("ACCESS PORTAL", width='stretch'):
            if password_entered == "UFC_Raiders_2026": 
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Invalid password! Please check with alliance generals.")
                
    return False

# 3. IF LOGGED IN, LOAD THE WEBSITE DATA
if check_password():
    
    # SIDEBAR NAVIGATION
    st.sidebar.image("https://icons8.com", width=50)
    st.sidebar.title("UFC Portal")
    page = st.sidebar.radio("NAVIGATION:", ["🏠 Home Dashboard", "⚔️ Troops Calculator"])
    st.sidebar.success("Secure connection active.")

    # --- PAGE 1: SAFE LINK TO GOOGLE SHEETS (Bypasses Firefox redirect blocks!) ---
    if page == "🏠 Home Dashboard":
        st.header("🏠 UFC Command Center - Alliance Status")
        st.write("Check the chests leaderboard updated in real-time by the alliance OCR script.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Elegant information box
        st.info("💡 **Notice for UFC Members:** By clicking the button below, the official leaderboard will open safely in a new browser tab in View-Only mode. You can check your scores and goals with maximum security.")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # IL TRUCCO DEFINITIVO: Usiamo il comando nativo st.link_button con il link pulito senza parametri spuri.
        # Questo forza il browser ad aprire la scheda direttamente senza passare dai controlli X-Frame!
        LINK_PULITO = "https://google.com"
        
        st.link_button("🛡️ OPEN OFFICIAL UFC LEADERBOARD", LINK_PULITO, width='stretch')

    # --- PAGE 2: INTERACTIVE MARCH SIMULATOR ---
    elif page == "⚔️ Troops Calculator":
        st.header("⚔️ UFC Tactical Manual & March Simulator")
        st.write("Set your hero parameters to calculate army composition. Each player session is completely private.")
        
        capacity = st.slider("Select your maximum Hero March Capacity:", 10000, 600000, 200000, step=5000)
        target = st.selectbox("Select your target:", ["Level 35 Crypts", "Alliance Citadels", "Epic Undead Squads"])
        
        st.markdown("#### 📋 Recommended Army Composition:")
        if target == "Level 35 Crypts":
            infantry = int(capacity * 0.6)
            archers = int(capacity * 0.4)
            st.success(f"💥 **Crypts Setup:** Send **{infantry:,} Infantry** and **{archers:,} Archers** (Optimized for zero losses).".replace(",", "."))
        elif target == "Alliance Citadels":
            st.warning("⚠️ **Coalition Order:** Send your full army balanced according to the orders issued by the Marshal in game chat.")
        else:
            balanced = int(capacity / 3)
            st.info(f"📌 **Standard Setup:** Send **{balanced:,} Infantry, {balanced:,} Archers, {balanced:,} Cavalry**.")
