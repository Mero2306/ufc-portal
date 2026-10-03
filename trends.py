import streamlit as st
import pandas as pd
import plotly.express as px

def mostra_trends_e_stats(ctx):
    # Ripristinato lo sfondo corretto collegato a specchio con i Risultati Clan
    st.markdown("""<style>.stApp { background: linear-gradient(rgba(14,11,6,0.93), rgba(20,16,9,0.93)), url("https://githubusercontent.com") no-repeat center center fixed !important; background-size: cover !important; }</style>""", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; margin: 0 auto 20px auto; font-family: \"Cinzel\", serif; font-size: 18px !important; font-weight: bold; color: #d4b373; border-bottom: 2px solid #bd9b53; padding-bottom: 10px; max-width: 500px;'>{ctx.get('menu_trends', '📊 CLAN TRENDS & STATS')}</h4>", unsafe_allow_html=True)
    
    SPREADSHEET_ID = "1yfJe8DyYX5QQmIBeXeW0BDfyv7A9FEw_mdDLmo3_VOQ"
    
    # Sintonizzato sul secondo foglio reale (la Dashboard)
    GID_DASHBOARD_LIVE = "432024066"
    
    # Mappatura dei codici GID reali estratti dal tuo file Google Sheet
    MAPPA_P = {
        "Periodo 1": "1482810444",
        "Periodo 2": "1738740307",
        "Periodo 3": "349323133",
        "Periodo 4": "1940986756"
    }
    
    # URL di esportazione pulito e ricostruito senza interruzioni di sintassi
    url_live = f"https://google.com{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={GID_DASHBOARD_LIVE}"
    try: 
        df_live = pd.read_csv(url_live, header=None)
    except Exception: 
        st.warning("⚠️ Waiting for data synchronisation... Please try to reload.")
        return

    cripte = ["Rare Crypt 30", "Epic Crypt 30", "Epic Crypt 35", "Arachne's Swarm", "Epic Undead Squad", "Shadow City", "Armageddon", "Hellforge", "Epic Fenrir Squad", "Jormungandr Squad", "Epic Chimera Squad", "Epic Basilisk Squad", "Epic Briareus Squad", "Sands of Eternity", "Arcanomancer squad", "Yokai", "Union of Triumph"]
    st.markdown(f"<h4 style='text-align: center; font-family: \"Cinzel\", serif; font-size: 14px !important; font-weight: bold; color: #bd9b53;'>📈 {ctx.get('trends_clan_title', 'Clan Performance Progression')}</h4>", unsafe_allow_html=True)
    
    c_s1, c_s2, c_s3 = st.columns([0.5, 2.0, 0.5])
    with c_s2: 
        p_clan = st.selectbox(ctx.get("trends_select_period", "Select Period:"), list(MAPPA_P.keys()), key="c_p_sel")
    
    try:
        url_h = f"https://google.com{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={MAPPA_P[p_clan]}"
        df_h = pd.read_csv(url_h, header=None)
        g_data = []
        for item in cripte:
            v_l, v_h = 0, 0
            for r in range(len(df_live)):
                if item.lower() in str(df_live.iloc[r, 0]).lower(): 
                    v_l = int(str(df_live.iloc[r, 1]).replace('.', '').strip()) if str(df_live.iloc[r, 1]).strip().isdigit() else 0
                    break
            for r in range(len(df_h)):
                if item.lower() in str(df_h.iloc[r, 0]).lower(): 
                    v_h = int(str(df_h.iloc[r, 1]).replace('.', '').strip()) if str(df_h.iloc[r, 1]).strip().isdigit() else 0
                    break
            lbl = ctx.get(item, item)
            g_data.append({"Type": lbl, "Timeline": "Historical", "Volume": v_h})
            g_data.append({"Type": lbl, "Timeline": "Current Live", "Volume": v_l})
            
        fig = px.line(pd.DataFrame(g_data), x="Type", y="Volume", color="Timeline", markers=True, color_discrete_sequence=["#bd9b53", "#f0e6d2"])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f0e6d2'), margin=dict(t=20,b=10,l=10,r=10), height=280)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except Exception: 
        pass
        
    st.markdown("<br><hr style='border:1px solid #bd9b53; opacity:0.15;'><br>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; font-family: \"Cinzel\", serif; font-size: 14px !important; font-weight: bold; color: #bd9b53;'>👤 {ctx.get('trends_player_title', 'Player Historical Comparison')}</h4>", unsafe_allow_html=True)

    try:
        df_p = df_live.iloc[3:106, 3].dropna().astype(str).str.strip()
        g_list = [n for n in df_p.unique() if n and n.lower() not in ["nan", "total", "totale", "union of triumph"]]
        if g_list:
            p_holder = ctx.get("select_name_placeholder", "-- Select Name --")
            c_w1, c_w2 = st.columns(2)
            with c_w1: g_scelto = st.selectbox(ctx.get("select_player_lbl", "Profile:"), [p_holder] + sorted(g_list), key="p_sel_tr")
            with c_w2: p_scelto = st.selectbox(ctx.get("trends_select_period_lbl", "Period:"), list(MAPPA_P.keys()), key="t_p_sel")
                
            if g_scelto != p_holder:
                df_p_h = pd.read_csv(f"https://google.com{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={MAPPA_P[p_scelto]}", header=None)
                v_live, o_live, v_hist, o_hist = 0, "0%", 0, "0%"
                for r in range(3, 106):
                    if str(df_live.iloc[r, 3]).strip().lower() == g_scelto.lower():
                        v_live = int(str(df_live.iloc[r, 4]).replace('.', '').strip()) if pd.notna(df_live.iloc[r, 4]) else 0
                        o_live = str(df_live.iloc[r, 7]).strip() if pd.notna(df_live.iloc[r, 7]) else "0%"
                        break
                for r in range(3, 106):
                    if str(df_p_h.iloc[r, 3]).strip().lower() == g_scelto.lower():
                        v_hist = int(str(df_p_h.iloc[r, 4]).replace('.', '').strip()) if pd.notna(df_p_h.iloc[r, 4]) else 0
                        o_hist = str(df_p_h.iloc[r, 7]).strip() if pd.notna(df_p_h.iloc[r, 7]) else "0%"
                        break
                
                gap = v_live - v_hist
                col_g = "#4CAF50" if gap > 0 else "#F44336" if gap < 0 else "#a69e8d"
                st.markdown("<br>", unsafe_allow_html=True)
                res1, res2 = st.columns(2)
                with res1: st.markdown(f"""<div class="chat-box" style="padding: 10px !important; border-left: 3px solid #d4b373 !important;"><span style="color: #a69e8d; font-size: 10px;">CHEST POINTS EVOLUTION</span><br><span style="font-size: 12px; color: #f0e6d2;">Live: <b>{v_live}</b> | Past: {v_hist}</span><br><span style="font-size: 13px; color: {col_g}; font-weight: bold;">Gap: {"+" if gap > 0 else ""}{gap}</span></div>""", unsafe_allow_html=True)
                with res2: st.markdown(f"""<div class="chat-box" style="padding: 10px !important; border-left: 3px solid #d4b373 !important;"><span style="color: #a69e8d; font-size: 10px;">GOAL PROGRESS COMPARISON</span><br><span style="font-size: 12px; color: #f0e6d2;">Current: <b>{o_live}</b></span><br><span style="font-size: 12px; color: #bd9b53;">Previous: <b>{o_hist}</b></span></div>""", unsafe_allow_html=True)
    except Exception: pass
