# Updated version of your app with additional RSS feed sections and fixed theme toggle

import streamlit as st
import pandas as pd
from fetch_data import main
from PIL import Image

# --- Load logos ---
chief_logo = Image.open("images/Chief_Logo.png")
truenorth_logo = Image.open("images/TrueNorthLogo.jpg")

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Chief Petroleum | News Dashboard",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Sidebar Theme Toggle ---
st.sidebar.title("⚙️ Customize Theme")
mode = st.sidebar.radio("Select Theme", options=["Dark", "Light"], index=0)

with st.sidebar.expander("ℹ️ How Theme Works"):
    st.write("""
    Select **Dark** or **Light** mode manually.  
    Dashboard appearance updates instantly!
    """)

# --- CSS Styling ---
base_color = "#0A0A0A" if mode == "Dark" else "#FFFFFF"
text_color = "white" if mode == "Dark" else "black"
section_color = "#FF4136" if mode == "Dark" else "#8B0000"
rightbar_bg = base_color

custom_styles = f"""
<style>
body {{
    background-color: {base_color};
    color: {text_color};
    margin: 0;
    padding: 0;
}}
body::before, body::after {{
    content: "";
    position: fixed;
    top: 0;
    width: 5px;
    height: 100%;
    background: #8B0000;
    z-index: 1;
}}
body::before {{ left: 0; }}
body::after {{ right: 0; }}
.stButton > button {{
    background-color: #8B0000;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    box-shadow: 0 0 5px #8B0000;
}}
.stButton > button:hover {{
    background-color: #A80000;
    box-shadow: 0 0 15px #FF4136;
}}
.title {{
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    margin-bottom: 10px;
    color: {text_color};
}}
.section-title {{
    font-size: 30px;
    font-weight: bold;
    margin-top: 2em;
    margin-bottom: 1em;
    color: {section_color};
}}
.footer {{
    text-align: left;
    font-size: 14px;
    color: grey;
    padding: 10px;
    margin-top: 50px;
}}
.rightbar {{
    padding-left: 20px;
    border-left: 5px solid #8B0000;
    background-color: {rightbar_bg};
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
@media only screen and (max-width: 768px) {{
    .title {{ font-size: 36px; }}
    .section-title {{ font-size: 24px; }}
    .rightbar {{ flex-direction: column; padding: 10px; border-left: none; }}
}}
</style>
"""
st.markdown(custom_styles, unsafe_allow_html=True)

# --- Layout: Main & Right Column ---
left_col, right_col = st.columns([8, 2])

with right_col:
    st.markdown("<div class='rightbar'>", unsafe_allow_html=True)
    st.image(chief_logo, width=180)
    st.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)
    st.image(truenorth_logo, width=80)
    st.markdown("<div class='footer'>Built by Jacob Johnston | True North Data Strategies</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with left_col:
    st.markdown("<div class='title'>Chief Petroleum<br>Fuel, ERP & AI Industry News Dashboard</div>", unsafe_allow_html=True)

    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    df = main()

    if df.empty:
        st.error("No news data available. Please try refreshing later.")
    else:
        # Define sections with shared logic
        def news_section(title, source_list, key_prefix):
            st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
            df_filtered = df[df['Source'].isin(source_list)]
            if not df_filtered.empty:
                col1, col2 = st.columns(2)
                with col1:
                    min_d, max_d = df_filtered['date'].min(), df_filtered['date'].max()
                    selected_dates = st.date_input(f"Date Range", (min_d, max_d), key=f"{key_prefix}_dates")
                    start_d, end_d = selected_dates if len(selected_dates) > 1 else (selected_dates[0], selected_dates[0])
                with col2:
                    sources = ["All"] + sorted(df_filtered['Source'].unique())
                    selected_sources = st.multiselect("Sources", sources, key=f"{key_prefix}_sources")
                if st.button("Show News", key=f"show_{key_prefix}"):
                    filtered = df_filtered[(df_filtered['date'] >= pd.to_datetime(start_d)) & (df_filtered['date'] <= pd.to_datetime(end_d))]
                    if "All" not in selected_sources and selected_sources:
                        filtered = filtered[filtered['Source'].isin(selected_sources)]
                    if not filtered.empty:
                        for _, row in filtered.iterrows():
                            st.markdown(f"### [{row['Title']}]({row['Link']})")
                            st.write(f"**Source**: {row['Source']}")
                            st.write(f"**Description**: {row['Description']}")
                            st.write(f"**Date**: {row['date'].strftime('%Y-%m-%d')}")
                            st.markdown("---")
                    else:
                        st.warning("No news found for that range.")
                st.text_area(f"💬 Leave a comment on {title}", placeholder="Thoughts or questions here...", key=f"comment_{key_prefix}")

        # --- Sections ---
        ai_sources = [s for s in df['Source'].unique() if "AI" in s or "Anthropic" in s or "DeepMind" in s or "OpenAI" in s]
        fuel_sources = [s for s in df['Source'].unique() if "Oil" in s or "Bloomberg" in s or "Reuters" in s or "EIA" in s]
        erp_sources = [
            "TechCrunch Enterprise", "VentureBeat – Data and AI", "CIO Dive",
            "Google Workspace Blog", "Intuit Developer Blog", "Stack Overflow - Apps Script"
        ]

        news_section(" 🧠 AI Industry News", ai_sources, "ai")
        news_section(" 🚛 Fuel & Energy News", fuel_sources, "fuel")
        news_section(" 📈 ERP & Automation Feeds", erp_sources, "erp")

