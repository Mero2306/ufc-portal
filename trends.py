import streamlit as st
import pandas as pd
import plotly.express as px

def mostra_trends_e_stats(ctx):
    # Sfondo epico a specchio con la pagina dei Risultati Clan
    st.markdown("""<style>.stApp { background: linear-gradient(rgba(14,11,6,0.93), rgba(20,16,9,0.93)), url("https://githubusercontent.com") no-repeat center center fixed !important; background-size: cover !important; }</style>""", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; margin: 0 auto 20px auto; font-family: \"Cinzel\", serif; font-size: 18px !important; font-weight: bold; color: #d4b373; border-bottom: 2px solid #bd9b53; padding-bottom: 10px; max-width: 500px;'>{ctx.get('menu_trends', '📊 CLAN TRENDS & STATS')}</h4>", unsafe_allow_html=True)
    
    SPREADSHEET_ID = "1yfJe8DyYX5QQmIBeXeW0BDfyv7A9FEw_mdDLmo3_VOQ"
    GID_LIVE_REALE = "1972335307"  # Foglio 1 (Dati in tempo reale)
    
    MAPPA_P = {
        "21/09 - 27/09 (Foglio 2)": "1281719474",
        "Foglio 3": "1240125232",
        "Foglio 4": "958114297",
        "28/09 - 05/10 (Foglio 5)": "676719910"
    }
    
    # Caricamento pulito del Foglio 1 (Tempo reale corrent)
    url_live = f"https://google.com{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={GID_LIVE_REALE}"
    try:
        # Usiamo la riga delle intestazioni (riga 2 nel tuo modello standard) come nomi di colonna reali
        df_live_raw = pd.read_csv(url_live, header=None)
        # Normalizziamo le intestazioni per la ricerca
        headers_live = df_live_raw.iloc[2].astype(str).str.strip().tolist()
        df_live = df_live_raw.iloc[3:106].copy()
        df_live.columns = headers_live
    except Exception:
        st.warning("⚠️ Waiting for data synchronisation... Please try to reload.")
        return

    # Lista dei forzieri e delle colonne in comune tra tutte le schede
    nomi_forzieri = [
        "Rare Crypt 30", "Epic Crypt 30", "Epic Crypt 35", "Arachne's Swarm", 
        "Epic Undead Squad", "Shadow City", "Armageddon", "Hellforge", 
        "Epic Fenrir Squad", "Jormungandr Squad", "Epic Chimera Squad", 
        "Epic Basilisk Squad", "Epic Briareus Squad", "Sands of Eternity", 
        "Arcanomancer squad", "Yokai", "Union of Triumph"
    ]

    st.markdown(f"<h4 style='text-align: center; font-family: \"Cinzel\", serif; font-size: 14px !important; font-weight: bold; color: #bd9b53;'>👤 {ctx.get('trends_player_title', 'Player Historical Comparison')}</h4>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    
    try:
        # Identifichiamo dinamicamente la colonna dei Nickname cercando tra le intestazioni in comune
        col_nome_chiave = [h for h in headers_live if "name" in h.lower() or "nickname" in h.lower() or "giocatore" in h.lower()][0]
        
        df_p = df_live[col_nome_chiave].dropna().astype(str).str.strip()
        g_list = [n for n in df_p.unique() if n and n.lower() not in ["nan", "total", "totale", "union of triumph"]]
        
        if g_list:
            p_holder = ctx.get("select_name_placeholder", "-- Select Name --")
            c_w1, c_w2 = st.columns(2)
            with c_w1: g_scelto = st.selectbox(ctx.get("select_player_lbl", "Profile:"), [p_holder] + sorted(g_list), key="p_sel_tr")
            with c_w2: p_scelto = st.selectbox(ctx.get("trends_select_period_lbl", "Period:"), list(MAPPA_P.keys()), key="t_p_sel")
                
            if g_scelto != p_holder:
                # Caricamento e normalizzazione dinamica del Foglio Storico selezionato (2, 3, 4 o 5)
                url_h = f"https://google.com{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={MAPPA_P[p_scelto]}"
                df_h_raw = pd.read_csv(url_h, header=None)
                
                # Cerchiamo in quale riga si trovano le intestazioni nel foglio storico (flessibilità totale)
                riga_headers_h = 2
                for r in range(5):
                    row_vals = df_h_raw.iloc[r].astype(str).str.lower().tolist()
                    if any("crypt" in val or "punti" in val or "points" in val for val in row_vals):
                        riga_headers_h = r
                        break
                        
                headers_hist = df_h_raw.iloc[riga_headers_h].astype(str).str.strip().tolist()
                df_h = df_h_raw.iloc[riga_headers_h+1:106].copy()
                df_h.columns = headers_hist
                
                col_nome_hist = [h for h in headers_hist if "name" in h.lower() or "nickname" in h.lower() or "giocatore" in h.lower()][0]

                # --- METODO DATABASE LOOKUP (BATTAGLIA NAVALE SUI NOMI COLONNA IN COMUNE) ---
                riga_player_live = df_live[df_live[col_nome_chiave].astype(str).str.strip().lower() == g_scelto.lower()]
                riga_player_hist = df_h[df_h[col_nome_hist].astype(str).str.strip().lower() == g_scelto.lower()]
                
                if not riga_player_live.empty and not riga_player_hist.empty:
                    g_data_lineare = []
                    
                    for item in nomi_forzieri:
                        val_l, val_h = 0, 0
                        
                        # Estrazione dal Live tramite nome colonna in comune
                        if item in riga_player_live.columns:
                            v_str = str(riga_player_live[item].values[0]).strip().replace('.', '').replace(',', '')
                            if v_str.endswith(".0"): v_str = v_str[:-2]
                            if v_str.isdigit(): val_l = int(v_str)
                            
                        # Estrazione dallo Storico tramite nome colonna in comune (Indipendente dalla posizione fisica!)
                        if item in riga_player_hist.columns:
                            v_str_h = str(riga_player_hist[item].values[0]).strip().replace('.', '').replace(',', '')
                            if v_str_h.endswith(".0"): v_str_h = v_str_h[:-2]
                            if v_str_h.isdigit(): val_h = int(v_str_h)
                            
                        lbl_forziere = ctx.get(item, item)
                        g_data_lineare.append({"Chest Type": lbl_forziere, "Timeline": "Historical Stats", "Chests Volume": val_h})
                        g_data_lineare.append({"Chest Type": lbl_forziere, "Timeline": "Current Live", "Chests Volume": val_l})
                    
                    # GRAFICO LINEARE CONTINUO PER IL GIOCATORE SELEZIONATO
                    df_plot = pd.DataFrame(g_data_lineare)
                    fig = px.line(df_plot, x="Chest Type", y="Chests Volume", color="Timeline", markers=True, color_discrete_sequence=["#bd9b53", "#f0e6d2"])
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f0e6d2'), margin=dict(t=20,b=10,l=10,r=10), height=290)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    
                    # estrazione dei totali punti ed obiettivi basata sui nomi colonna
                    punti_live, punti_hist = 0, 0
                    col_pts_l = [h for h in riga_player_live.columns if "punti" in h.lower() or "points" in h.lower()][0]
                    col_pts_h = [h for h in riga_player_hist.columns if "punti" in h.lower() or "points" in h.lower()][0]
                    
                    try: punti_live = int(str(riga_player_live[col_pts_l].values[0]).replace('.', '').replace(',', '').strip())
                    except Exception: pass
                    try: punti_hist = int(str(riga_player_hist[col_pts_h].values[0]).replace('.', '').replace(',', '').strip())
                    except Exception: pass
                    
                    gap = punti_live - punti_hist
                    col_g = "#4CAF50" if gap > 0 else "#F44336" if gap < 0 else "#a69e8d"
                    
                    col_prg_l = [h for h in riga_player_live.columns if "progress" in h.lower() or "goal" in h.lower() or "obiettivo" in h.lower()][0]
                    col_prg_h = [h for h in riga_player_hist.columns if "progress" in h.lower() or "goal" in h.lower() or "obiettivo" in h.lower()][0]
                    o_live = str(riga_player_live[col_prg_l].values[0]).strip()
                    o_hist = str(riga_player_hist[col_prg_h].values[0]).strip()
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    res1, res2 = st.columns(2)
                    with res1: st.markdown(f"""<div class="chat-box" style="padding: 10px !important; border-left: 3px solid #d4b373 !important;"><span style="color: #a69e8d; font-size: 10px;">CHEST POINTS EVOLUTION</span><br><span style="font-size: 12px; color: #f0e6d2;">Live: <b>{punti_live:,}</b> | Past: {punti_hist:,}</span><br><span style="font-size: 13px; color: {col_g}; font-weight: bold;">Gap: {"+" if gap > 0 else ""}{gap:,}</span></div>""".replace(',', '.'), unsafe_allow_html=True)
                    with res2: st.markdown(f"""<div class="chat-box" style="padding: 10px !important; border-left: 3px solid #d4b373 !important;"><span style="color: #a69e8d; font-size: 10px;">GOAL PROGRESS COMPARISON</span><br><span style="font-size: 12px; color: #f0e6d2;">Current: <b>{o_live}</b></span><br><span style="font-size: 12px; color: #bd9b53;">Previous: <b>{o_hist}</b></span></div>""", unsafe_allow_html=True)
                else:
                    st.info("ℹ️ Profile data not available in the selected historical sheet.")
    except Exception: pass
