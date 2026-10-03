import streamlit as st
import pandas as pd
import plotly.express as px

def mostra_trends_e_stats(ctx):
    # Sfondo dorato immediato per evitare schermate nere
    st.markdown("""<style>.stApp { background: linear-gradient(rgba(14,11,6,0.93), rgba(20,16,9,0.93)), url("https://githubusercontent.com") no-repeat center center fixed !important; background-size: cover !important; }</style>""", unsafe_allow_html=True)
    
    # Titolo principale della pagina (Max 18px per mobile)
    st.markdown(f"<h4 style='text-align: center; margin: 0 auto 20px auto; font-family: \"Cinzel\", serif; font-size: 18px !important; font-weight: bold; color: #d4b373; border-bottom: 2px solid #bd9b53; padding-bottom: 10px; max-width: 500px;'>{ctx.get('menu_trends', '📊 CLAN TRENDS & STATS')}</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    SPREADSHEET_ID = "1yfJe8DyYX5QQmIBeXeW0BDfyv7A9FEw_mdDLmo3_VOQ"
    GID_LIVE_REALE = "1972335307"
    gids_storici = ["1281719474", "1240125232", "958114297", "676719910"]
    
    # Caricamento del database Live (Foglio 1)
    url_live = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={GID_LIVE_REALE}"
    try:
        df_live_raw = pd.read_csv(url_live, header=None)
        # Estrazione dati reali giocatori (Righe 3-106)
        df_live = df_live_raw.iloc[3:106].copy()
    except Exception:
        st.warning("⚠️ Waiting for data synchronisation... Please try to reload.")
        return

    # --- MOTORE SICURO ESTRAZIONE TITOLI PERIODI DA CELLA D2 ---
    mappa_periodi_gid = {}
    label_live = ctx.get("trends_current_period", "Current Observation Period")
    
    for v_gid in gids_storici:
        try:
            url_check = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={v_gid}"
            df_check = pd.read_csv(url_check, header=None)
            titolo_rilevato = f"Archive Period ({v_gid[-4:]})"
            
            # Lettura protetta della cella D2 (Indice riga 1, colonna 3)
            if df_check is not None and len(df_check) > 1 and len(df_check.columns) > 3:
                cella_val = str(df_check.iloc[1, 3]).strip()
                if cella_val and cella_val.lower() != "nan" and cella_val != "":
                    titolo_rilevato = cella_val
            mappa_periodi_gid[titolo_rilevato] = v_gid
        except Exception:
            mappa_periodi_gid[f"Archive Sheet ({v_gid[-4:]})"] = v_gid
    # Sottotitolo della sezione
    st.markdown(f"<h4 style='text-align: center; font-family: \"Cinzel\", serif; font-size: 14px !important; font-weight: bold; color: #bd9b53;'>📈 {ctx.get('trends_clan_title', 'Clan Performance Progression')}</h4>", unsafe_allow_html=True)

    try:
        # Estrazione della lista giocatori reali dalla colonna D (Indice 3) del foglio Live
        # Rimuoviamo i valori non validi, i totali e i nan
        df_live_names = df_live.iloc[:, 3].dropna().astype(str).str.strip()
        g_list = [n for n in df_live_names.unique() if n and n.lower() not in ["nan", "", "total", "totale", "union of triumph"]]
        g_list = sorted(g_list)

        if g_list and mappa_periodi_gid:
            p_holder = ctx.get("select_name_placeholder", "-- Select Name --")
            
            # Generiamo i due menu a tendina affiancati (Profilo e Periodo di confronto)
            c_w1, c_w2 = st.columns(2)
            with c_w1: g_scelto = st.selectbox(ctx.get("select_player_lbl", "Profile:"), [p_holder] + g_list, key="p_sel_tr")
            with c_w2: p_scelto = st.selectbox(ctx.get("trends_select_period_lbl", "Period:"), list(mappa_periodi_gid.keys()), key="t_p_sel")
                
            # Mostriamo i grafici solo se l'utente seleziona un giocatore valido
            if g_scelto != p_holder:
                # Carichiamo il foglio storico selezionato dall'utente
                url_h = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={mappa_periodi_gid[p_scelto]}"
                df_h_raw = pd.read_csv(url_h, header=None)
                df_h_data = df_h_raw.iloc[3:106].copy()

                # LOGICA VLOOKUP: Cerchiamo le righe corrispondenti al giocatore in modo indipendente dalla posizione
                r_p_l = df_live[df_live.iloc[:, 3].astype(str).str.strip().lower() == g_scelto.lower()]
                r_p_h = df_h_data[df_h_data.iloc[:, 3].astype(str).str.strip().lower() == g_scelto.lower()]
                
                # Mappatura dei forzieri con gli indici numerici delle colonne per evitare conflitti con le intestazioni di testo
                # Colonna 4 = E (Punti), Colonna 8 = I (Armageddon), Colonna 9 = J (Dark Omens)
                # Forzieri dettagliati mappati in base alla loro colonna numerica progressiva (A=0, B=1, ecc.)
                mappa_colonne_forzieri = {
                    "Rare Crypt 30": 32, "Epic Crypt 30": 36, "Epic Crypt 35": 37, "Arachne's Swarm": 44,
                    "Epic Undead Squad": 45, "Shadow City": 46, "Armageddon": 47, "Hellforge": 48,
                    "Epic Fenrir Squad": 49, "Jormungandr Squad": 50, "Epic Chimera Squad": 51,
                    "Epic Basilisk Squad": 52, "Epic Briareus Squad": 53, "Sands of Eternity": 92,
                    "Arcanomancer squad": 93, "Yokai": 94, "Dark Omens": 9
                }
                
                if not r_p_l.empty:
                    g_data = []
                    for nome_forziere, idx_colonna in mappa_colonne_forzieri.items():
                        val_l, val_h = 0, 0
                        
                        # Estrazione dato Live
                        if idx_colonna < len(r_p_l.columns):
                            v = str(r_p_l.iloc[0, idx_colonna]).strip().replace('.', '').replace(',', '')
                            if v.isdigit(): val_l = int(v)
                        
                        # Estrazione dato Storico (Se il giocatore esisteva in questo archivio)
                        if not r_p_h.empty and idx_colonna < len(r_p_h.columns):
                            v_h = str(r_p_h.iloc[0, idx_colonna]).strip().replace('.', '').replace(',', '')
                            if v_h.isdigit(): val_h = int(v_h)
                            
                        lbl_tradotto = ctx.get(nome_forziere, nome_forziere)
                        g_data.append({"Chest Type": lbl_tradotto, "Timeline": p_scelto, "Volume": val_h})
                        g_data.append({"Chest Type": lbl_tradotto, "Timeline": label_live, "Volume": val_l})
                    
                    # Generazione del grafico lineare di confronto trend
                    df_grafico = pd.DataFrame(g_data)
                    fig = px.line(df_grafico, x="Chest Type", y="Volume", color="Timeline", markers=True, color_discrete_sequence=["#bd9b53", "#f0e6d2"])
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f0e6d2'), margin=dict(t=20,b=10,l=10,r=10), height=280)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    
                    # Sezione confronto sintetico dei punti totali (Colonna E -> Indice 4)
                    p_l, p_h = 0, 0
                    try: p_l = int(str(r_p_l.iloc[0, 4]).replace('.', '').replace(',', '').strip())
                    except Exception: pass
                    
                    if not r_p_h.empty:
                        try: p_h = int(str(r_p_h.iloc[0, 4]).replace('.', '').replace(',', '').strip())
                        except Exception: pass
                    
                    gap = p_l - p_h
                    col_g = "#4CAF50" if gap > 0 else "#F44336" if gap < 0 else "#a69e8d"
                    
                    # Estrazione Obiettivi (Colonna G -> Indice 6)
                    o_l = str(r_p_l.iloc[0, 6]).strip() if len(r_p_l.columns) > 6 else "N/A"
                    o_h = str(r_p_h.iloc[0, 6]).strip() if not r_p_h.empty and len(r_p_h.columns) > 6 else "N/A"
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    res1, res2 = st.columns(2)
                    with res1: 
                        st.markdown(f"""<div class="chat-box" style="padding: 10px !important; border-left: 3px solid #d4b373 !important;"><span style="color: #a69e8d; font-size: 10px;">CHEST POINTS EVOLUTION</span><br><span style="font-size: 12px; color: #f0e6d2;">Live: <b>{p_l:,}</b> | Past: {p_h:,}</span><br><span style="font-size: 13px; color: {col_g}; font-weight: bold;">Gap: {"+" if gap > 0 else ""}{gap:,}</span></div>""".replace(',', '.'), unsafe_allow_html=True)
                    with res2: 
                        st.markdown(f"""<div class="chat-box" style="padding: 10px !important; border-left: 3px solid #d4b373 !important;"><span style="color: #a69e8d; font-size: 10px;">GOAL PROGRESS COMPARISON</span><br><span style="font-size: 12px; color: #f0e6d2;">Current: <b>{o_l}</b></span><br><span style="font-size: 12px; color: #bd9b53;">Previous: <b>{o_h}</b></span></div>""", unsafe_allow_html=True)
                else:
                    st.info("👤 Player details not found in the live log database.")
    except Exception as e:
        st.error(f"Error rendering trends page: {e}")
