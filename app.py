# --- Chief Petroleum News Dashboard ---
# Developer Notes:
# - Right-side mini-sidebar for logos
# - Permanent red side borders + soft side glow
# - Manual Light/Dark mode toggle
# - Hover info next to theme toggle
# - Fully mobile-optimized layout
# - Button hover glow effect

import streamlit as st
import pandas as pd
from fetch_data import main
from PIL import Image

# Load images
chief_logo = Image.open("images/Chief_Logo.png")
truenorth_logo = Image.open("images/TrueNorthLogo.jpg")

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Chief Petroleum | News Dashboard",
    page_icon="⛽",
    layout="wide",  # wider layout for better left/main split
    initial_sidebar_state="expanded",
)

# --- Sidebar: Theme Customization ---
st.sidebar.title("⚙️ Customize Theme")
mode = st.sidebar.radio("Select Theme", options=["Dark", "Light"], index=0)

with st.sidebar.expander("ℹ️ How Theme Works"):
    st.write("""
    Select **Dark** or **Light** mode manually.  
    Dashboard appearance updates instantly!
    """)

# --- Base CSS Styling ---
custom_styles = """
<style>
body {
    background-color: #0A0A0A;
    color: white;
    margin: 0;
    padding: 0;
}
body::before, body::after {
    content: "";
    position: fixed;
    top: 0;
    width: 5px;
    height: 100%;
    background: #8B0000;
    z-index: 1;
}
body::before { left: 0; }
body::after { right: 0; }
.stButton > button {
    background-color: #8B0000;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    box-shadow: 0 0 5px #8B0000;
}
.stButton > button:hover {
    background-color: #A80000;
    box-shadow: 0 0 15px #FF4136;
}
.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    margin-bottom: 10px;
}
.section-title {
    font-size: 30px;
    font-weight: bold;
    margin-top: 2em;
    margin-bottom: 1em;
    color: #FF4136;
}
.footer {
    text-align: left;
    font-size: 14px;
    color: grey;
    padding: 10px;
    margin-top: 50px;
}
.rightbar {
    padding-left: 20px;
    border-left: 5px solid #8B0000;
    background-color: #0A0A0A;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
@media only screen and (max-width: 768px) {
    .title {
        font-size: 36px;
    }
    .section-title {
        font-size: 24px;
    }
    .rightbar {
        flex-direction: column;
        padding: 10px;
        border-left: none;
    }
}
</style>
"""

# --- Inject Base Styles ---
st.markdown(custom_styles, unsafe_allow_html=True)

# --- Theme Override if Light Mode selected ---
if mode == "Light":
    st.markdown(
        """
        <style>
        body {
            background-color: #FFFFFF;
            color: black;
        }
        .title, .section-title, .footer {
            color: black;
        }
        .rightbar {
            background-color: #FFFFFF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Layout Split: Main Content | Right Sidebar ---
left_col, right_col = st.columns([8, 2])

# --- Right Mini Sidebar (for Logos) ---
with right_col:
    st.markdown("<div class='rightbar'>", unsafe_allow_html=True)
    st.image(chief_logo, width=180)
    st.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)  # Spacer
    st.image(truenorth_logo, width=80)
    st.markdown("<div class='footer'>Built by Jacob Johnston | True North Data Strategies</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Main Dashboard Content ---
with left_col:
    st.markdown("<div class='title'>Chief Petroleum<br>Fuel & AI Industry News Dashboard</div>", unsafe_allow_html=True)

    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    df = main()

    if df.empty:
        st.error("No news data available. Please try refreshing later.")
    else:
        # --- AI News Section ---
        st.markdown("<div class='section-title'>🧠 AI Industry News</div>", unsafe_allow_html=True)

        with st.spinner('Loading AI News...'):
            ai_sources = [
                "The Berkeley Artificial Intelligence Research Blog",
                "NVDIA Blog",
                "Microsoft Research",
                "Science Daily",
                "META Research",
                "OpenAI News",
                "Google DeepMind Blog",
                "MIT News - Artificial intelligence",
                "MIT Technology Review - Artificial intelligence",
                "Wired: Artificial Intelligence Latest",
                "Ollama Blog",
                "Anthropic News"
            ]
            df_ai = df[df['Source'].isin(ai_sources)]

            if not df_ai.empty:
                col1, col2 = st.columns(2)
                with col1:
                    min_date_ai, max_date_ai = df_ai['date'].min(), df_ai['date'].max()
                    selected_dates_ai = st.date_input("AI News Date Range", (min_date_ai, max_date_ai), key="ai_dates")
                    start_ai, end_ai = selected_dates_ai if len(selected_dates_ai) > 1 else (selected_dates_ai[0], selected_dates_ai[0])
                with col2:
                    selected_sources_ai = st.multiselect("AI News Sources", ["All"] + sorted(df_ai['Source'].unique()), key="ai_sources")

                if st.button("Show AI News", key="show_ai"):
                    df_filtered_ai = df_ai[(df_ai['date'] >= pd.to_datetime(start_ai)) & (df_ai['date'] <= pd.to_datetime(end_ai))]
                    if "All" not in selected_sources_ai and selected_sources_ai:
                        df_filtered_ai = df_filtered_ai[df_filtered_ai['Source'].isin(selected_sources_ai)]

                    if not df_filtered_ai.empty:
                        for _, row in df_filtered_ai.iterrows():
                            st.markdown(f"### [{row['Title']}]({row['Link']})")
                            st.write(f"**Source**: {row['Source']}")
                            st.write(f"**Description**: {row['Description']}")
                            st.write(f"**Date**: {row['date'].strftime('%Y-%m-%d')}")
                            st.markdown("---")
                    else:
                        st.warning("No AI news found with the selected filters.")

        st.text_area("💬 Leave a comment on AI News:", placeholder="Your thoughts, questions, or feedback here...", key="ai_comment")

        # --- Fuel News Section ---
        st.markdown("<div class='section-title'>🚛 Fuel Industry News</div>", unsafe_allow_html=True)

        with st.spinner('Loading Fuel News...'):
            fuel_sources = [
                "EIA Press Releases",
                "API News",
                "NACS News",
                "OilPrice.com Energy News",
                "Reuters Commodities Energy",
                "MarketWatch Energy",
                "Bloomberg Energy News"
            ]
            df_fuel = df[df['Source'].isin(fuel_sources)]

            if not df_fuel.empty:
                col3, col4 = st.columns(2)
                with col3:
                    min_date_fuel, max_date_fuel = df_fuel['date'].min(), df_fuel['date'].max()
                    selected_dates_fuel = st.date_input("Fuel News Date Range", (min_date_fuel, max_date_fuel), key="fuel_dates")
                    start_fuel, end_fuel = selected_dates_fuel if len(selected_dates_fuel) > 1 else (selected_dates_fuel[0], selected_dates_fuel[0])
                with col4:
                    selected_sources_fuel = st.multiselect("Fuel News Sources", ["All"] + sorted(df_fuel['Source'].unique()), key="fuel_sources")

                if st.button("Show Fuel News", key="show_fuel"):
                    df_filtered_fuel = df_fuel[(df_fuel['date'] >= pd.to_datetime(start_fuel)) & (df_fuel['date'] <= pd.to_datetime(end_fuel))]
                    if "All" not in selected_sources_fuel and selected_sources_fuel:
                        df_filtered_fuel = df_filtered_fuel[df_filtered_fuel['Source'].isin(selected_sources_fuel)]

                    if not df_filtered_fuel.empty:
                        for _, row in df_filtered_fuel.iterrows():
                            st.markdown(f"### [{row['Title']}]({row['Link']})")
                            st.write(f"**Source**: {row['Source']}")
                            st.write(f"**Description**: {row['Description']}")
                            st.write(f"**Date**: {row['date'].strftime('%Y-%m-%d')}")
                            st.markdown("---")
                    else:
                        st.warning("No fuel news found with the selected filters.")

        st.text_area("💬 Leave a comment on Fuel News:", placeholder="Your thoughts, questions, or feedback here...", key="fuel_comment")

