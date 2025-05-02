# Updated version of your app with fixed light/dark theme toggling using Streamlit native settings

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

# --- CSS Styling Fix ---
# Apply theme-specific styling directly to elements that Streamlit renders
base_color = "#0A0A0A" if mode == "Dark" else "#FFFFFF"
text_color = "white" if mode == "Dark" else "black"
section_color = "#FF4136" if mode == "Dark" else "#8B0000"
rightbar_bg = base_color

# --- Entire Theme Styling (fixes visual issues with body override) ---
custom_styles = f"""
<style>
html, body, [class*="st-"], .stApp {{
    background-color: {base_color} !important;
    color: {text_color} !important;
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

    # Debug: Show feed counts by source
    if st.sidebar.checkbox("🧪 Show Feed Counts", value=False):
            feed_counts = df['Source'].value_counts().reset_index()
            feed_counts.columns = ["Source", "# of Articles"]
            st.sidebar.dataframe(feed_counts)

    if df.empty:
        st.error("No news data available. Please try refreshing later.")
    else:
        def news_section(title, source_list, key_prefix):
            st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
            df_filtered = df[df['Source'].isin(source_list)]
            if df_filtered.empty:
                st.info(f"No recent articles from these sources. Showing older content.")
                df_filtered = df[df['Source'].isin(source_list)].sort_values(by='date', ascending=False).head(10)
            if not df_filtered.empty:
                col1, col2 = st.columns(2)
                with col1:
                    min_d, max_d = df_filtered['date'].min(), df_filtered['date'].max()
                    selected_dates = st.date_input(f"{title} - Date Range", (min_d, max_d), key=f"{key_prefix}_dates")
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

        ai_sources = [s for s in df['Source'].unique() if "AI" in s or "Anthropic" in s or "DeepMind" in s or "OpenAI" in s]
        fuel_sources = [
            s for s in df['Source'].unique()
            if any(x in s for x in ["Oil", "Bloomberg", "Reuters", "EIA", "Colorado Traffic", "Colorado Weather", "DTN"])
        ].unique()
            if any(x in s for x in ["Oil", "Bloomberg", "Reuters", "EIA", "Colorado Traffic", "Colorado Weather", "DTN"])
        ]
        erp_sources = [
            "TechCrunch Enterprise", "VentureBeat – Data and AI", "CIO Dive",
            "Google Workspace Blog", "Intuit Developer Blog", "Stack Overflow - Apps Script",
            "https://medium.com/feed/tag/python", "https://medium.com/feed/tag/ai", "https://medium.com/feed/tag/quickbooks", "https://medium.com/feed/tag/erp", "https://medium.com/feed/tag/streamlit", "https://medium.com/feed/tag/machine-learning", "https://medium.com/feed/tag/data-visualization", "https://medium.com/feed/tag/business-intelligence", "https://medium.com/feed/tag/quickbooks-online"
        ]

        news_section(" 📈 ERP & Automation Feeds", erp_sources, "erp")
        news_section(" 🧠 AI Industry News", ai_sources, "ai")
        news_section(" 🚛 Fuel & Energy News", fuel_sources, "fuel")
