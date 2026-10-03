import streamlit as st
import pandas as pd
import plotly.express as px

def mostra_trends_e_stats(ctx):
    # Sfondo ufficiale dorato UFC a specchio con la pagina dei Risultati Clan
    st.markdown("""<style>.stApp { background: linear-gradient(rgba(14,11,6,0.93), rgba(20,16,9,0.93)), url("https://githubusercontent.com") no-repeat center center fixed !important; background-size: cover !important; }</style>""", unsafe_allow_html=True)
    
    # Titolo principale sottile ed elegante (Dimensione massima 18px per mobile)
    st.markdown(f"<h4 style='text-align: center; margin: 0 auto 20px auto; font-family: \"Cinzel\", serif; font-size: 18px !important; font-weight: bold; color: #d4b373; border-bottom: 2px solid #bd9b53; padding-bottom: 10px; max-width: 500px;'>{ctx.get('menu_trends', '📊 CLAN TRENDS & STATS')}</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    SPREADSHEET_ID = "1yfJe8DyYX5QQmIBeXeW0BDfyv7A9FEw_mdDLmo3_VOQ"
    GID_LIVE_REALE = "1972335307"
    gids_storici = ["1281719474", "1240125232", "958114297", "676719910"]
    
    # URL di caricamento del Foglio 1 (Dati correnti live verticali) con la sintassi nativa ufficiale ://google.com
    url_live = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={GID_LIVE_REALE}"
    try:
        df_live_raw = pd.read_csv(url_live, header=None)
        # CORRETTO: Estrazione pulita della riga 2 (la terza riga con le intestazioni dei forzieri)
        headers_live = df_live_raw.iloc[2].astype(str).str.strip().tolist()
        df_live = df_live_raw.iloc[3:106].copy()
        df_live.columns = headers_live
    except Exception:
        st.warning("⚠️ Waiting for data synchronisation... Please try to reload.")
        return

    # --- MOTORE AD ESTRAZIONE TITOLI REALI DA CELLA D2 VIA CSV ---
    mappa_periodi_gid = {}
    label_live = ctx.get("trends_current_period", "Current Observation Period")
    
    for v_gid in gids_storici:
        try:
            url_check = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={v_gid}"
            df_check = pd.read_csv(url_check, header=None)
            titolo_rilevato = f"Period GID {v_gid}"
            if df_check is not None and len(df_check) > 1 and len(df_check.columns) > 3:
                cella_val = str(df_check.iloc[1, 3]).strip()
                if cella_val and cella_val.lower() != "nan" and cella_val != "":
                    titolo_rilevato = cella_val
            mappa_periodi_gid[titolo_rilevato] = v_gid
        except Exception:
            mappa_periodi_gid[f"Archive Sheet ({v_gid[-4:]})"] = v_gid

    # LISTA DEI FORZIERI CON LA DEVIAZIONE SU DARK OMENS (COLONNA CP) E SENZA TRIUMPHAL
    nomi_forzieri = ["Rare Crypt 30", "Epic Crypt 30", "Epic Crypt 35", "Arachne's Swarm", "Epic Undead Squad", "Shadow City", "Armageddon", "Hellforge", "Epic Fenrir Squad", "Jormungandr Squad", "Epic Chimera Squad", "Epic Basilisk Squad", "Epic Briareus Squad", "Sands of Eternity", "Arcanomancer squad", "Yokai", "Dark Omens"]
    st.markdown(f"<h4 style='text-align: center; font-family: \"Cinzel\", serif; font-size: 14px !important; font-weight: bold; color: #bd9b53;'>📈 {ctx.get('trends_clan_title', 'Clan Performance Progression')}</h4>", unsafe_allow_html=True)

    try:
        col_n = [h for h in headers_live if "name" in h.lower() or "nickname" in h.lower() or "giocatore" in h.lower()]
        g_list = [n for n in df_live[col_n[0]].dropna().astype(str).str.strip().unique() if n and n.lower() not in ["nan", "total", "totale", "union of triumph"]]
        
        if g_list and mappa_periodi_gid:
            p_holder = ctx.get("select_name_placeholder", "-- Select Name --")
            c_w1, c_w2 = st.columns(2)
            with c_w1: g_scelto = st.selectbox(ctx.get("select_player_lbl", "Profile:"), [p_holder] + sorted(g_list), key="p_sel_tr")
            with c_w2: p_scelto = st.selectbox(ctx.get("trends_select_period_lbl", "Period:"), list(mappa_periodi_gid.keys()), key="t_p_sel")
                
            if g_scelto != p_holder:
                url_h = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={mappa_periodi_gid[p_scelto]}"
                df_h_raw = pd.read_csv(url_h, header=None)
                
                headers_hist = df_h_raw.iloc[2].astype(str).str.strip().tolist()
                df_h = df_h_raw.iloc[3:106].copy()
                df_h.columns = headers_hist
                col_n_h = [h for h in headers_hist if "name" in h.lower() or "nickname" in h.lower() or "giocatore" in h.lower()]

                r_p_l = df_live[df_live[col_n[0]].astype(str).str.strip().lower() == g_scelto.lower()]
                r_p_h = df_h[df_h[col_n_h[0]].astype(str).str.strip().lower() == g_scelto.lower()]
                
                if not r_p_l.empty and not r_p_h.empty:
                    g_data = []
                    for item in nomi_forzieri:
                        val_l, val_h = 0, 0
                        colonna_vera = "CP" if item == "Dark Omens" else item
                        
                        if colonna_vera in r_p_l.columns:
                            v = str(r_p_l[colonna_vera].iloc[0]).strip().replace('.', '').replace(',', '')
                            if v.isdigit(): val_l = int(v)
                        if colonna_vera in r_p_h.columns:
                            v_h = str(r_p_h[colonna_vera].iloc[0]).strip().replace('.', '').replace(',', '')
                            if v_h.isdigit(): val_h = int(v_h)
                            
                        lbl = ctx.get(item, item)
                        g_data.append({"Chest Type": lbl, "Timeline": p_scelto, "Volume": val_h})
                        g_data.append({"Chest Type": lbl, "Timeline": label_live, "Volume": val_l})
                    
                    fig = px.line(pd.DataFrame(g_data), x="Chest Type", y="Volume", color="Timeline", markers=True, color_discrete_sequence=["#bd9b53", "#f0e6d2"])
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f0e6d2'), margin=dict(t=20,b=10,l=10,r=10), height=280)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    
                    p_l, p_h = 0, 0
                    c_p_l = [h for h in r_p_l.columns if "punti" in h.lower() or "points" in h.lower()]
                    c_p_h = [h for h in r_p_h.columns if "punti" in h.lower() or "points" in h.lower()]
                    try: p_l = int(str(r_p_l[c_p_l[0]].iloc[0]).replace('.', '').replace(',', '').strip())
                    except Exception: pass
                    try: p_h = int(str(r_p_h[c_p_h[0]].iloc[0]).replace('.', '').replace(',', '').strip())
                    except Exception: pass
                    
                    gap = p_l - p_h
                    col_g = "#4CAF50" if gap > 0 else "#F44336" if gap < 0 else "#a69e8d"
                    c_g_l = [h for h in r_p_l.columns if "progress" in h.lower() or "goal" in h.lower() or "o_live" in h.lower() or "obiettivo" in h.lower()]
                    c_g_h = [h for h in r_p_h.columns if "progress" in h.lower() or "goal" in h.lower() or "o_hist" in h.lower() or "obiettivo" in h.lower()]
                    o_l = str(r_p_l[c_g_l[0]].iloc[0]).strip()
                    o_h = str(r_p_h[c_g_h[0]].iloc[0]).strip()
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    res1, res2 = st.columns(2)
                    with res1: st.markdown(f"""<div class="chat-box" style="padding: 10px !important; border-left: 3px solid #d4b373 !important;"><span style="color: #a69e8d; font-size: 10px;">CHEST POINTS EVOLUTION</span><br><span style="font-size: 12px; color: #f0e6d2;">Live: <b>{p_l:,}</b> | Past: {p_h:,}</span><br><span style="font-size: 13px; color: {col_g}; font-weight: bold;">Gap: {"+" if gap > 0 else ""}{gap:,}</span></div>""".replace(',', '.'), unsafe_allow_html=True)
                    with res2: st.markdown(f"""<div class="chat-box" style="padding: 10px !important; border-left: 3px solid #d4b373 !important;"><span style="color: #a69e8d; font-size: 10px;">GOAL PROGRESS COMPARISON</span><br><span style="font-size: 12px; color: #f0e6d2;">Current: <b>{o_l}</b></span><br><span style="font-size: 12px; color: #bd9b53;">Previous: <b>{o_h}</b></span></div>""", unsafe_allow_html=True)
    except Exception: pass
