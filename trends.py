import streamlit as st
import pandas as pd
import plotly.express as px

def mostra_trends_e_stats(ctx):
    """
    Funzione indipendente che genera la pagina dei Trend Storici del Clan.
    Legge la Dashboard reale (Foglio 2) e la confronta con i fogli storici periodici.
    Titoli perfettamente centrati e uniformati alle dimensioni del portale.
    """
    # APPLICAZIONE DELLO STESSO IDENTICO SFONDO DEI RISULTATI DEL CLAN
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(rgba(14, 11, 6, 0.93), rgba(20, 16, 9, 0.93)), 
                        url("https://githubusercontent.com") no-repeat center center fixed !important;
            background-size: cover !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # TITOLO PRINCIPALE PERFETTAMENTE CENTRATO E FORMATTATO
    st.markdown(f"<h1 style='text-align: center;'>{ctx.get('menu_trends', '📊 CLAN TRENDS & STATS')}</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ID unico del Foglio Google ufficiale del clan UFC
    SPREADSHEET_ID = "1yfJe8DyYX5QQmIBeXeW0BDfyv7A9FEw_mdDLmo3_VOQ"
    
    # GID 0 corrisponde alla Dashboard corrente (il secondo foglio reale del tuo URL)
    GID_DASHBOARD_LIVE = "0"  
    
    # MAPPATURA ORIZZONTALE DEI PERIODI (FOGLI SUCCESSIVI)
    PERIODI_MAPPA = {
        "Period 1 (28/09 - 05/10)": "1482810444",  # Cambiare con i GID reali dei tuoi fogli storici
        "Period 2": "123456789",
        "Period 3": "987654321"
    }
    
    # 1. Caricamento della Dashboard Reale Corrente (Foglio 2)
    url_live = f"https://google.com{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={GID_DASHBOARD_LIVE}"
    try:
        df_live = pd.read_csv(url_live, header=None)
    except Exception:
        st.warning("⚠️ Waiting for data synchronisation... Please reload the page.")
        return

    # LISTA COMPLETA DI TUTTI I FORZIERI E EPICI COME NELLA PAGINA RISULTATI CLAN
    forzieri_selezionati = [
        "Rare Crypt 30", "Epic Crypt 30", "Epic Crypt 35", 
        "Arachne's Swarm", "Epic Undead Squad", "Shadow City",
        "Armageddon", "Hellforge", "Epic Fenrir Squad", 
        "Jormungandr Squad", "Epic Chimera Squad", "Epic Basilisk Squad", 
        "Epic Briareus Squad", "Sands of Eternity", "Arcanomancer squad", 
        "Yokai", "Union of Triumph"
    ]

    # SOTTOTITOLO CENTRATO CON DIMENSIONI CORRETTE
    st.markdown(f"<h4 style='text-align: center; font-family: \"Cinzel\", serif; font-size: 16px; font-weight: bold;'>📈 {ctx.get('trends_clan_title', 'Clan Performance Progression')}</h4>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
    
    # Menu di selezione del periodo per il confronto generale del Clan (Centrato visivamente tramite colonne)
    c_sel_c1, c_sel_c2, c_sel_c3 = st.columns([0.5, 2.0, 0.5])
    with c_sel_c2:
        periodo_confronto_clan = st.selectbox(
            ctx.get("trends_select_period", "Select Historical Period to Compare:"),
            list(PERIODI_MAPPA.keys()),
            key="clan_trend_period_selector"
        )
    
    gid_storico_clan = PERIODI_MAPPA[periodo_confronto_clan]
    url_storico_clan = f"https://google.com{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={gid_storico_clan}"
    
    try:
        df_storico_clan = pd.read_csv(url_storico_clan, header=None)
        conteggi_grafico = []
        
        for item in forzieri_selezionati:
            val_live = 0
            val_storico = 0
            
            try:
                for r_idx in range(len(df_live)):
                    if item.lower() in str(df_live.iloc[r_idx, 0]).lower():
                        val_live = int(str(df_live.iloc[r_idx, 10]).replace('.', '').strip())
                        break
            except Exception: pass
            
            try:
                for r_idx in range(len(df_storico_clan)):
                    if item.lower() in str(df_storico_clan.iloc[r_idx, 0]).lower():
                        val_storico = int(str(df_storico_clan.iloc[r_idx, 10]).replace('.', '').strip())
                        break
            except Exception: pass
            
            nome_etichetta = ctx.get(item, item)
            conteggi_grafico.append({"Chest Type": nome_etichetta, "Timeline": "Historical", "Volume": val_storico})
            conteggi_grafico.append({"Chest Type": nome_etichetta, "Timeline": "Current Live", "Volume": val_live})
            
        df_lineare = pd.DataFrame(conteggi_grafico)
        fig_linee = px.line(
            df_lineare, x="Chest Type", y="Volume", color="Timeline", markers=True,
            title="Loot Category Performance Timeline Comparison", color_discrete_sequence=["#bd9b53", "#f0e6d2"]
        )
        fig_linee.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f0e6d2'), margin=dict(t=30,b=10,l=10,r=10), height=320)
        st.plotly_chart(fig_linee, use_container_width=True, config={'displayModeBar': False})

    except Exception:
        pass

    st.markdown("<br><hr style='border:1px solid #bd9b53; opacity:0.15;'><br>", unsafe_allow_html=True)

    # --- SEZIONE C: CONFRONTO PERSONALE GIOCATORE (DOPPIO FILTRO CENTRATO) ---
    st.markdown(f"<h4 style='text-align: center; font-family: \"Cinzel\", serif; font-size: 16px; font-weight: bold;'>👤 {ctx.get('trends_player_title', 'Player Historical Comparison')}</h4>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
    
    try:
        df_players_raw = df_live.iloc[3:106, 3].dropna().astype(str).str.strip()
        lista_giocatori = [n for n in df_players_raw.unique() if n and n.lower() not in ["nan", "total", "totale", "union of triumph"]]
        
        if lista_giocatori:
            placeholder_nome = ctx.get("select_name_placeholder", "-- Select Name --")
            c_p1, c_p2 = st.columns(2)
            
            with c_p1:
                giocatore_scelto = st.selectbox(
                    ctx.get("select_player_lbl", "Select your profile:"),
                    [placeholder_nome] + sorted(lista_giocatori),
                    key="trends_player_dropdown_final_v12"
                )
            
            with c_p2:
                periodo_scelto_player = st.selectbox(
                    ctx.get("trends_select_period_lbl", "Select Period:"),
                    list(PERIODI_MAPPA.keys()),
                    key="trends_period_player_dropdown_final_v12"
                )
                
            if giocatore_scelto != placeholder_nome:
                gid_storico_player = PERIODI_MAPPA[periodo_scelto_player]
                url_storico_player = f"https://google.com{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&gid={gid_storico_player}"
                df_storico_p = pd.read_csv(url_storico_player, header=None)
                
                punti_live = 0
                progresso_live = "0%"
                for r_idx in range(3, 106):
                    if str(df_live.iloc[r_idx, 3]).strip().lower() == giocatore_scelto.lower():
                        punti_live = int(str(df_live.iloc[r_idx, 4]).replace('.', '').strip()) if pd.notna(df_live.iloc[r_idx, 4]) else 0
                        progresso_live = str(df_live.iloc[r_idx, 7]).strip() if pd.notna(df_live.iloc[r_idx, 7]) else "0%"
                        break
                        
                punti_storici = 0
                progresso_storico = "0%"
                for r_idx in range(3, 106):
                    if str(df_storico_p.iloc[r_idx, 3]).strip().lower() == giocatore_scelto.lower():
                        punti_storici = int(str(df_storico_p.iloc[r_idx, 4]).replace('.', '').strip()) if pd.notna(df_storico_p.iloc[r_idx, 4]) else 0
                        progresso_storico = str(df_storico_p.iloc[r_idx, 7]).strip() if pd.notna(df_storico_p.iloc[r_idx, 7]) else "0%"
                        break
                
                gap_punti = punti_live - punti_storici
                segno_gap = "+" if gap_punti > 0 else ""
                colore_gap = "#4CAF50" if gap_punti > 0 else "#F44336" if gap_punti < 0 else "#a69e8d"
                
                st.markdown("<br>", unsafe_allow_html=True)
                col_p_res1, col_p_res2 = st.columns(2)
                
                with col_p_res1:
                    st.markdown(
                        f"""
                        <div class="chat-box" style="padding: 12px !important; border-left: 3px solid #d4b373 !important;">
                            <span style="color: #a69e8d; font-size: 11px;">CHEST POINTS EVOLUTION</span><br>
                            <span style="font-size: 13px; color: #f0e6d2;">Current: <b>{punti_live}</b> | Past: {punti_storici}</span><br>
                            <span style="font-size: 14px; color: {colore_gap}; font-weight: bold;">Gap: {segno_gap}{gap_punti}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with col_p_res2:
                    st.markdown(
                        f"""
                        <div class="chat-box" style="padding: 12px !important; border-left: 3px solid #d4b373 !important;">
                            <span style="color: #a69e8d; font-size: 11px;">GOAL PROGRESS COMPARISON</span><br>
                            <span style="font-size: 13px; color: #f0e6d2;">Current Goal: <b>{progresso_live}</b></span><br>
                            <span style="font-size: 13px; color: #body; color: #bd9b53;">Previous Goal: <b>{progresso_storico}</b></span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    except Exception:
        pass
