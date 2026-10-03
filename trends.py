import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

def mostra_trends_e_stats(ctx):
    # 1. LOGICA LOCALE CARICAMENTO SFONDO BASE64
    def applica_sfondo_locale(image_path):
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                bin_str = base64.b64encode(img_file.read()).decode()
            bg_src = f"data:image/jpeg;base64,{bin_str}"
            st.markdown(f"""<style>.stApp {{ background: linear-gradient(rgba(14,11,6,0.93), rgba(20,16,9,0.93)), url("{bg_src}") no-repeat center center fixed !important; background-size: cover !important; }}</style>""", unsafe_allow_html=True)
        else:
            st.markdown("""<style>.stApp { background: linear-gradient(rgba(14,11,6,0.93), rgba(20,16,9,0.93)), url("bg_info.jpg") no-repeat center center fixed !important; background-size: cover !important; }</style>""", unsafe_allow_html=True)

    applica_sfondo_locale("bg_info.jpg")
    
    # Titolo pagina dinamico
    titolo_pagina = ctx.get('menu_trends', '📊 CLAN TRENDS & STATS')
    st.markdown(f"<h4 style='text-align: center; margin: 0 auto 20px auto; font-family: \"Cinzel\", serif; font-size: 18px !important; font-weight: bold; color: #d4b373; border-bottom: 2px solid #bd9b53; padding-bottom: 10px; max-width: 500px;'>{titolo_pagina}</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    SPREADSHEET_ID = "1yfJe8DyYX5QQmIBeXeW0BDfyv7A9FEw_mdDLmo3_VOQ"
    GID_LIVE_REALE = "1972335307"
    gids_storici = ["1281719474", "1240125232", "958114297", "676719910"]
    
    url_live = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={GID_LIVE_REALE}"
    try:
        df_live_raw = pd.read_csv(url_live, header=None)
        df_live = df_live_raw.iloc[3:107].copy()
    except Exception:
        st.warning("⚠️ Waiting for data synchronisation... Please try to reload.")
        return

    mappa_periodi_gid = {}
    label_live = ctx.get("trends_current_period", "Current Observation Period")
    
    for v_gid in gids_storici:
        try:
            url_check = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={v_gid}"
            df_check = pd.read_csv(url_check, header=None)
            titolo_rilevato = f"Archive Period ({v_gid[-4:]})"
            if df_check is not None and len(df_check) > 1 and len(df_check.columns) > 3:
                cella_val = str(df_check.iloc[1, 3]).strip()
                if cella_val and cella_val.lower() != "nan" and cella_val != "":
                    titolo_rilevato = cella_val
            mappa_periodi_gid[titolo_rilevato] = v_gid
        except Exception:
            mappa_periodi_gid[f"Archive Sheet ({v_gid[-4:]})"] = v_gid

    st.markdown(f"<h4 style='text-align: center; font-family: \"Cinzel\", serif; font-size: 14px !important; font-weight: bold; color: #bd9b53;'>📈 {ctx.get('trends_clan_title', 'Clan Performance Progression')}</h4>", unsafe_allow_html=True)

    try:
        df_solo_giocatori = df_live.iloc[0:103, 3].dropna().astype(str).str.strip()
        g_list = [n for n in df_solo_giocatori.unique() if n and n.lower() not in ["nan", "", "total", "totale", "union of triumph"]]
        g_list = sorted(g_list)

        if mappa_periodi_gid:
            p_holder = ctx.get("select_name_placeholder", "-- Select Name --")
            clan_holder = ctx.get("select_entire_clan_lbl", "-- Entire Clan --")
            period_holder = ctx.get("select_period_placeholder", "-- Choose Period --")
            lista_periodi = [period_holder] + list(mappa_periodi_gid.keys())
            
            c_w1, c_w2 = st.columns(2)
            with c_w1: g_scelto = st.selectbox(ctx.get("select_player_lbl", "Profile:"), [p_holder, clan_holder] + g_list, key="p_sel_tr")
            with c_w2: p_scelto = st.selectbox(ctx.get("trends_select_period_lbl", "Period:"), lista_periodi, key="t_p_sel")
                
            if g_scelto != p_holder and p_scelto != period_holder:
                url_h = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={mappa_periodi_gid[p_scelto]}"
                df_h_raw = pd.read_csv(url_h, header=None)
                df_h_data = df_h_raw.iloc[3:107].copy()

                # RISOLTO: Indici numerici espliciti fissi sulla riga totali (103) per l'intero clan
                if g_scelto == clan_holder:
                    r_p_l = df_live.iloc[[103]]
                    r_p_h = df_h_data.iloc[[103]]
                else:
                    r_p_l = df_live.iloc[0:103][df_live.iloc[0:103, 3].astype(str).str.strip().str.lower() == g_scelto.lower()]
                    r_p_h = df_h_data.iloc[0:103][df_h_data.iloc[0:103, 3].astype(str).str.strip().str.lower() == g_scelto.lower()]
                
                mappa_colonne_forzieri = {
                    "Rare Crypt 30": 32, "Epic Crypt 30": 36, "Epic Crypt 35": 37, "Arachne's Swarm": 44,
                    "Epic Undead Squad": 45, "Shadow City": 46, "Armageddon": 47, "Hellforge": 48,
                    "Epic Fenrir Squad": 49, "Jormungandr Squad": 50, "Epic Chimera Squad": 51,
                    "Epic Basilisk Squad": 52, "Epic Briareus Squad": 53, "Sands of Eternity": 92,
                    "Arcanomancer squad": 93, "Yokai": 94
                }

                if not r_p_l.empty:
                    g_data = []
                    lbl_timeline = ctx.get("trends_graph_timeline", "Timeline")
                    lbl_volume = ctx.get("trends_graph_volume", "Volume")
                    lbl_chest_type = ctx.get("trends_graph_chest_type", "Chest Type")

                    for nome_forziere, idx_colonna in mappa_colonne_forzieri.items():
                        val_l, val_h = 0, 0
                        if idx_colonna < len(r_p_l.columns):
                            v = str(r_p_l.iloc[0, idx_colonna]).strip().replace('.', '').replace(',', '')
                            if v.isdigit(): val_l = int(v)
                        if not r_p_h.empty and idx_colonna < len(r_p_h.columns):
                            v_h = str(r_p_h.iloc[0, idx_colonna]).strip().replace('.', '').replace(',', '')
                            if v_h.isdigit(): val_h = int(v_h)
                            
                        lbl_tradotto = ctx.get(nome_forziere, nome_forziere)
                        g_data.append({lbl_chest_type: lbl_tradotto, lbl_timeline: p_scelto, lbl_volume: val_h})
                        g_data.append({lbl_chest_type: lbl_tradotto, lbl_timeline: label_live, lbl_volume: val_l})

                    df_grafico = pd.DataFrame(g_data)
                    fig = px.bar(df_grafico, x=lbl_chest_type, y=lbl_volume, color=lbl_timeline, barmode="group", color_discrete_sequence=["#bd9b53", "#f0e6d2"])
                    fig.update_traces(marker_line_color='#14120e', marker_line_width=1.5, opacity=0.95)
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f0e6d2'), 
                        margin=dict(t=10, b=80, l=10, r=10), height=350, dragmode=False,
                        xaxis=dict(tickangle=-45, title=None, fixedrange=True),
                        yaxis=dict(title=None, gridcolor='rgba(240, 230, 210, 0.1)', fixedrange=True),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, title=None)
                    )
                    # INSERITO: Mostra effettivamente il grafico a schermo
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    
                    p_l, p_h = 0, 0
                    
                    def pulisci_valore_totale(cella):
                        try:
                            # Convertiamo direttamente in numero float (decimale) e poi in intero.
                            # Questo elimina matematicamente il .0 finale senza aggiungere zeri!
                            return int(float(str(cella).strip()))
                        except Exception:
                            return 0

                    # Estrazione e pulizia nativa senza manipolazione di stringhe o punti
                    if g_scelto == clan_holder:
                        try:
                            p_l = pulisci_valore_totale(r_p_l.iloc)
                            p_h = pulisci_valore_totale(r_p_h.iloc) if not r_p_h.empty else 0
                        except Exception: pass
                    else:
                        try: 
                            p_l = pulisci_valore_totale(r_p_l.iloc)
                        except Exception: pass
                        if not r_p_h.empty:
                            try: 
                                p_h = pulisci_valore_totale(r_p_h.iloc)
                            except Exception: pass
                    
                    gap = p_l - p_h
                    col_g = "#4CAF50" if gap > 0 else "#F44336" if gap < 0 else "#a69e8d"
                    
                    lbl_box_title = ctx.get("trends_box_title", "EVOLUZIONE PUNTI FORZIERI")
                    lbl_box_live = ctx.get("trends_box_live", "Corrente")
                    lbl_box_past = ctx.get("trends_box_past", "Passato")
                    lbl_box_gap = ctx.get("trends_box_gap", "Differenza")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"""<div class="chat-box" style="padding: 12px !important; border-left: 5px solid #d4b373 !important; max-width: 600px; margin: 0 auto;"><span style="color: #a69e8d; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;">{lbl_box_title}</span><br><span style="font-size: 14px; color: #f0e6d2;">{lbl_box_live}: <b>{p_l:,}</b> | {lbl_box_past}: {p_h:,}</span><br><span style="font-size: 14px; color: {col_g}; font-weight: bold;">{lbl_box_gap}: {"+" if gap > 0 else ""}{gap:,}</span></div>""".replace(',', '.'), unsafe_allow_html=True)
                else:
                    st.info("👤 Player details not found in the live log database.")
    except Exception as e:
        st.error(f"Error rendering trends page: {e}")
