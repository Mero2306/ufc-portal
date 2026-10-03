import streamlit as st
import pandas as pd
import plotly.express as px

def mostra_trends_e_stats(ctx):
    st.markdown("""<style>.stApp { background: linear-gradient(rgba(14,11,6,0.93), rgba(20,16,9,0.93)), url("https://githubusercontent.com") no-repeat center center fixed !important; background-size: cover !important; }</style>""", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; margin: 0 auto 20px auto; font-family: \"Cinzel\", serif; font-size: 18px !important; font-weight: bold; color: #d4b373; border-bottom: 2px solid #bd9b53; padding-bottom: 10px; max-width: 500px;'>{ctx.get('menu_trends', '📊 CLAN TRENDS & STATS')}</h4>", unsafe_allow_html=True)
    
    SPREADSHEET_ID = "1yfJe8DyYX5QQmIBeXeW0BDfyv7A9FEw_mdDLmo3_VOQ"
    url_ods = f"https://google.com{SPREADSHEET_ID}/export?format=ods"
    
    try:
        fogli_file = pd.read_excel(url_ods, sheet_name=None, header=None)
        elenco_nomi = list(fogli_file.keys())
        df_live_raw = fogli_file[elenco_nomi[0]]
        headers_live = df_live_raw.iloc[2].astype(str).str.strip().tolist()
        df_live = df_live_raw.iloc[3:106].copy()
        df_live.columns = headers_live
        
        mappa_periodi_gid = {}
        label_live = ctx.get("trends_current_period", "Current Observation Period")
        
        for idx in range(1, len(elenco_nomi)):
            df_h_temp = fogli_file[elenco_nomi[idx]]
            titolo_p = f"Period {idx}"
            if len(df_h_temp) > 1 and len(df_h_temp.columns) > 3:
                cella_d2 = str(df_h_temp.iloc[1, 3]).strip()
                if cella_d2 and cella_d2.lower() != "nan": titolo_p = cella_d2
            mappa_periodi_gid[titolo_p] = elenco_nomi[idx]
    except Exception:
        st.warning("⚠️ Waiting for data synchronisation... Please try to reload.")
        return

    nomi_forzieri = ["Rare Crypt 30", "Epic Crypt 30", "Epic Crypt 35", "Arachne's Swarm", "Epic Undead Squad", "Shadow City", "Armageddon", "Hellforge", "Epic Fenrir Squad", "Jormungandr Squad", "Epic Chimera Squad", "Epic Basilisk Squad", "Epic Briareus Squad", "Sands of Eternity", "Arcanomancer squad", "Yokai", "Union of Triumph"]
    st.markdown(f"<h4 style='text-align: center; font-family: \"Cinzel\", serif; font-size: 14px !important; font-weight: bold; color: #bd9b53;'>📈 {ctx.get('trends_clan_title', 'Clan Performance Progression')}</h4>", unsafe_allow_html=True)
    try:
        col_n = [h for h in headers_live if "name" in h.lower() or "nickname" in h.lower() or "giocatore" in h.lower()][0]
        g_list = [n for n in df_live[col_n].dropna().astype(str).str.strip().unique() if n and n.lower() not in ["nan", "total", "totale", "union of triumph"]]
        
        if g_list and mappa_periodi_gid:
            p_holder = ctx.get("select_name_placeholder", "-- Select Name --")
            c_w1, c_w2 = st.columns(2)
            with c_w1: g_scelto = st.selectbox(ctx.get("select_player_lbl", "Profile:"), [p_holder] + sorted(g_list), key="p_sel_tr")
            with c_w2: p_scelto = st.selectbox(ctx.get("trends_select_period_lbl", "Period:"), list(mappa_periodi_gid.keys()), key="t_p_sel")
                
            if g_scelto != p_holder:
                df_h_raw = fogli_file[mappa_periodi_gid[p_scelto]]
                r_h_h = 2
                for r in range(5):
                    row_vals = df_h_raw.iloc[r].astype(str).str.lower().tolist()
                    if any("crypt" in val or "punti" in val or "points" in val for val in row_vals): r_h_h = r; break
                        
                headers_hist = df_h_raw.iloc[r_h_h].astype(str).str.strip().tolist()
                df_h = df_h_raw.iloc[r_h_h+1:106].copy()
                df_h.columns = headers_hist
                col_n_h = [h for h in headers_hist if "name" in h.lower() or "nickname" in h.lower() or "giocatore" in h.lower()][0]

                r_p_l = df_live[df_live[col_n].astype(str).str.strip().lower() == g_scelto.lower()]
                r_p_h = df_h[df_h[col_n_h].astype(str).str.strip().lower() == g_scelto.lower()]
                
                if not r_p_l.empty and not r_p_h.empty:
                    g_data = []
                    for item in nomi_forzieri:
                        val_l, val_h = 0, 0
                        if item in r_p_l.columns:
                            v = str(r_p_l[item].values[0]).strip().replace('.', '').replace(',', '')
                            if v.isdigit(): val_l = int(v)
                        if item in r_p_h.columns:
                            v_h = str(r_p_h[item].values[0]).strip().replace('.', '').replace(',', '')
                            if v_h.isdigit(): val_h = int(v_h)
                            
                        lbl = ctx.get(item, item)
                        g_data.append({"Chest Type": lbl, "Timeline": p_scelto, "Volume": val_h})
                        g_data.append({"Chest Type": lbl, "Timeline": label_live, "Volume": val_l})
                    
                    fig = px.line(pd.DataFrame(g_data), x="Chest Type", y="Volume", color="Timeline", markers=True, color_discrete_sequence=["#bd9b53", "#f0e6d2"])
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f0e6d2'), margin=dict(t=20,b=10,l=10,r=10), height=280)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    
                    p_l, p_h = 0, 0
                    c_p_l = [h for h in r_p_l.columns if "punti" in h.lower() or "points" in h.lower()][0]
                    c_p_h = [h for h in r_p_h.columns if "punti" in h.lower() or "points" in h.lower()][0]
                    try: p_l = int(str(r_p_l[c_p_l].values[0]).replace('.', '').replace(',', '').strip())
                    except Exception: pass
                    try: p_h = int(str(r_p_h[c_p_h].values[0]).replace('.', '').replace(',', '').strip())
                    except Exception: pass
                    
                    gap = p_l - p_h
                    col_g = "#4CAF50" if gap > 0 else "#F44336" if gap < 0 else "#a69e8d"
                    c_g_l = [h for h in r_p_l.columns if "progress" in h.lower() or "goal" in h.lower() or "o_live" in h.lower() or "obiettivo" in h.lower()][0]
                    c_g_h = [h for h in r_p_h.columns if "progress" in h.lower() or "goal" in h.lower() or "o_hist" in h.lower() or "obiettivo" in h.lower()][0]
                    o_l = str(r_p_l[c_g_l].values[0]).strip()
                    o_h = str(r_p_h[c_g_h].values[0]).strip()
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    res1, res2 = st.columns(2)
                    with res1: st.markdown(f"""<div class="chat-box" style="padding: 10px !important; border-left: 3px solid #d4b373 !important;"><span style="color: #a69e8d; font-size: 10px;">CHEST POINTS EVOLUTION</span><br><span style="font-size: 12px; color: #f0e6d2;">Live: <b>{p_l:,}</b> | Past: {p_h:,}</span><br><span style="font-size: 13px; color: {col_g}; font-weight: bold;">Gap: {"+" if gap > 0 else ""}{gap:,}</span></div>""".replace(',', '.'), unsafe_allow_html=True)
                    with res2: st.markdown(f"""<div class="chat-box" style="padding: 10px !important; border-left: 3px solid #d4b373 !important;"><span style="color: #a69e8d; font-size: 10px;">GOAL PROGRESS COMPARISON</span><br><span style="font-size: 12px; color: #f0e6d2;">Current: <b>{o_l}</b></span><br><span style="font-size: 12px; color: #bd9b53;">Previous: <b>{o_h}</b></span></div>""", unsafe_allow_html=True)
    except Exception: pass
