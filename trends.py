import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

def mostra_trends_e_stats(ctx):
    # 1. FUNZIONE LOCALE PER CARICARE LO SFONDO IN BASE64
    def applica_sfondo_locale(image_path):
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                bin_str = base64.b64encode(img_file.read()).decode()
            bg_src = f"data:image/jpeg;base64,{bin_str}"
            st.markdown(f"""<style>.stApp {{ background: linear-gradient(rgba(14,11,6,0.93), rgba(20,16,9,0.93)), url("{bg_src}") no-repeat center center fixed !important; background-size: cover !important; }}</style>""", unsafe_allow_html=True)
        else:
            st.markdown("""<style>.stApp { background: linear-gradient(rgba(14,11,6,0.93), rgba(20,16,9,0.93)), url("bg_info.jpg") no-repeat center center fixed !important; background-size: cover !important; }</style>""", unsafe_allow_html=True)

    # Attivazione immediata dello sfondo
    applica_sfondo_locale("bg_info.jpg")
    
    # Titolo della pagina
    st.markdown(f"<h4 style='text-align: center; margin: 0 auto 20px auto; font-family: \"Cinzel\", serif; font-size: 18px !important; font-weight: bold; color: #d4b373; border-bottom: 2px solid #bd9b53; padding-bottom: 10px; max-width: 500px;'>{ctx.get('menu_trends', '📊 CLAN TRENDS & STATS')}</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    SPREADSHEET_ID = "1yfJe8DyYX5QQmIBeXeW0BDfyv7A9FEw_mdDLmo3_VOQ"
    GID_LIVE_REALE = "1972335307"
    gids_storici = ["1281719474", "1240125232", "958114297", "676719910"]
    
    url_live = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={GID_LIVE_REALE}"
    try:
        df_live_raw = pd.read_csv(url_live, header=None)
        df_live = df_live_raw.iloc[3:106].copy()
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
        df_live_names = df_live.iloc[:, 3].dropna().astype(str).str.strip()
        g_list = [n for n in df_live_names.unique() if n and n.lower() not in ["nan", "", "total", "totale", "union of triumph"]]
        g_list = sorted(g_list)

        if g_list and mappa_periodi_gid:
            p_holder = ctx.get("select_name_placeholder", "-- Select Name --")
            
            # AGGIUNTA SELEZIONE VUOTA PER IL PERIODO (TRADUCIBILE)
            period_holder = ctx.get("select_period_placeholder", "-- Choose Period --")
            lista_periodi = [period_holder] + list(mappa_periodi_gid.keys())
            
            c_w1, c_w2 = st.columns(2)
            with c_w1: g_scelto = st.selectbox(ctx.get("select_player_lbl", "Profile:"), [p_holder] + g_list, key="p_sel_tr")
            with c_w2: p_scelto = st.selectbox(ctx.get("trends_select_period_lbl", "Period:"), lista_periodi, key="t_p_sel")
                
# ATTIVAZIONE SOLO SE ENTRAMBI I FILTRI SONO SELEZIONATI CORRETTAMENTE
            if g_scelto != p_holder and p_scelto != period_holder:
                url_h = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={mappa_periodi_gid[p_scelto]}"
                df_h_raw = pd.read_csv(url_h, header=None)
                df_h_data = df_h_raw.iloc[3:106].copy()

                # LOGICA DINAMICA: Controllo singolo profilo o Intero Clan
                if g_scelto == clan_holder:
                    r_p_l = df_live[df_live.iloc[:, 3].astype(str).str.strip().str.lower().isin([x.lower() for x in g_list])]
                    r_p_h = df_h_data[df_h_data.iloc[:, 3].astype(str).str.strip().str.lower().isin([x.lower() for x in g_list])]
                    is_clan = True
                else:
                    r_p_l = df_live[df_live.iloc[:, 3].astype(str).str.strip().str.lower() == g_scelto.lower()]
                    r_p_h = df_h_data[df_h_data.iloc[:, 3].astype(str).str.strip().str.lower() == g_scelto.lower()]
                    is_clan = False
                
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
                        if idx_colonna < len(r_p_l.columns):
                            if is_clan:
                                val_l = sum(pd.to_numeric(r_p_l.iloc[:, idx_colonna].astype(str).str.replace('.', '').str.replace(',', ''), errors='coerce').fillna(0).astype(int))
                            else:
                                v = str(r_p_l.iloc[0, idx_colonna]).strip().replace('.', '').replace(',', '')
                                if v.isdigit(): val_l = int(v)
                        if idx_colonna < len(r_p_h.columns):
                            if is_clan:
                                val_h = sum(pd.to_numeric(r_p_h.iloc[:, idx_colonna].astype(str).str.replace('.', '').str.replace(',', ''), errors='coerce').fillna(0).astype(int))
                            else:
                                if not r_p_h.empty:
                                    v_h = str(r_p_h.iloc[0, idx_colonna]).strip().replace('.', '').replace(',', '')
                                    if v_h.isdigit(): val_h = int(v_h)
                            
                        lbl_tradotto = ctx.get(nome_forziere, nome_forziere)
                        g_data.append({"Chest Type": lbl_tradotto, "Timeline": p_scelto, "Volume": val_h})
                        g_data.append({"Chest Type": lbl_tradotto, "Timeline": label_live, "Volume": val_l})

                    # NUOVO GRAFICO A BARRE CON BLOCCO ZOOM PER CELLULARI
                    df_grafico = pd.DataFrame(g_data)
                    fig = px.bar(
                        df_grafico, 
                        x="Chest Type", 
                        y="Volume", 
                        color="Timeline", 
                        barmode="group",
                        color_discrete_sequence=["#bd9b53", "#f0e6d2"]
                    )
                    
                    fig.update_traces(
                        marker_line_color='#14120e', 
                        marker_line_width=1.5, 
                        opacity=0.95
                    )
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', 
                        plot_bgcolor='rgba(0,0,0,0)', 
                        font=dict(color='#f0e6d2'), 
                        margin=dict(t=10, b=80, l=10, r=10), 
                        height=350, 
                        dragmode=False,
                        xaxis=dict(
                            tickangle=-45,
                            title=None,
                            fixedrange=True
                        ),
                        yaxis=dict(
                            title=None,
                            gridcolor='rgba(240, 230, 210, 0.1)',
                            fixedrange=True
                        ),
                        legend=dict(
                            orientation="h", 
                            yanchor="bottom", 
                            y=1.02, 
                            xanchor="center", 
                            x=0.5
                        )
                    )
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    
                    # LOGICA DI CONVERSIONE NUMERICA ULTRA-SICURA PER I TOTALI
                    p_l, p_h = 0, 0
                    
                    def pulisci_valore_totale(cella):
                        val_str = str(cella).strip().lower()
                        if val_str == "nan" or val_str == "": return 0
                        if val_str.endswith(".0"): val_str = val_str[:-2]
                        val_str = val_str.replace('.', '').replace(',', '')
                        return int(val_str) if val_str.isdigit() else 0

                    if is_clan:
                        p_l = sum(r_p_l.iloc[:, 4].apply(puliisci_valore_totale))
                        p_h = sum(r_p_h.iloc[:, 4].apply(puliisci_valore_totale)) if not r_p_h.empty else 0
                    else:
                        try: p_l = pulisci_valore_totale(r_p_l.iloc[0, 4])
                        except Exception: pass
                        if not r_p_h.empty:
                            try: p_h = pulisci_valore_totale(r_p_h.iloc[0, 4])
                            except Exception: pass
                    
                    gap = p_l - p_h
                    col_g = "#4CAF50" if gap > 0 else "#F44336" if gap < 0 else "#a69e8d"
                    
                    # BOX UNICO PULITO (RIMOSSO IL BOX OBIETTIVI)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"""<div class="chat-box" style="padding: 12px !important; border-left: 5px solid #d4b373 !important; max-width: 600px; margin: 0 auto;"><span style="color: #a69e8d; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;">CHEST POINTS EVOLUTION</span><br><span style="font-size: 14px; color: #f0e6d2;">Live: <b>{p_l:,}</b> | Past: {p_h:,}</span><br><span style="font-size: 14px; color: {col_g}; font-weight: bold;">Gap: {"+" if gap > 0 else ""}{gap:,}</span></div>""".replace(',', '.'), unsafe_allow_html=True)
                else:
                    st.info("👤 Player details not found in the live log database.")
    except Exception as e:
        st.error(f"Error rendering trends page: {e}")
