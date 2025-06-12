# Updated version of your app with TrueNorth colors and modified sections

import streamlit as st
import pandas as pd
from fetch_data import main
from PIL import Image
import os
from database import save_comment, get_comments

# --- Load logos ---
try:
    image_path = os.path.join(os.path.dirname(__file__), "images/truenorth_logo.jpg")
    truenorth_logo = Image.open(image_path)
except Exception as e:
    st.warning(f"Failed to load logo: {e}")
    truenorth_logo = None

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="TrueNorth | News Dashboard",
    page_icon="📊",
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
# TrueNorth blue colors
section_color = "#0078D4" if mode == "Dark" else "#004E8C"
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
    background: #0078D4;
    z-index: 1;
}}
body::before {{ left: 0; }}
body::after {{ right: 0; }}
.stButton > button {{
    background-color: #0078D4;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    box-shadow: 0 0 5px #0078D4;
}}
.stButton > button:hover {{
    background-color: #005EA8;
    box-shadow: 0 0 15px #0078D4;
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
    border-left: 5px solid #0078D4;
    background-color: {rightbar_bg};
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.social-links {{
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;
}}
.social-links a {{
    color: #0078D4;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 5px;
}}
.social-links a:hover {{
    text-decoration: underline;
}}
.comment-box {{
    background-color: rgba(0, 120, 212, 0.1);
    border-left: 3px solid #0078D4;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 0 5px 5px 0;
}}
.comment-user {{
    font-weight: bold;
    margin-bottom: 5px;
}}
.comment-date {{
    font-size: 0.8em;
    color: #888;
    margin-bottom: 5px;
}}
.comment-text {{
    margin-top: 5px;
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
    if truenorth_logo:
        st.image(truenorth_logo, width=180)
    
    # Social links
    st.markdown("<div class='social-links'>", unsafe_allow_html=True)
    st.markdown("<a href='https://www.truenorthstrategyops.com/' target='_blank'>🌐 Visit Our Website</a>", unsafe_allow_html=True)
    st.markdown("<a href='https://www.facebook.com/profile.php?viewas=100000686899395&id=61577047841328' target='_blank'>📱 Follow on Facebook</a>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='footer'>Built by True North Data Strategies</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with left_col:
    st.markdown("<div class='title'>TrueNorth Data Strategies<br>AI & Automation Industry News Dashboard</div>", unsafe_allow_html=True)

    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def load_data():
        return main()

    df = load_data()

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
                
                # Comments Section
                with st.expander("💬 Comments", expanded=True):
                    # Display existing comments
                    comments_df = get_comments(section=key_prefix)
                    if not comments_df.empty:
                        st.subheader("Previous Comments")
                        for _, comment_row in comments_df.iterrows():
                            st.markdown(f"""
                            <div class="comment-box">
                                <div class="comment-user">{comment_row['user_name']}</div>
                                <div class="comment-date">{pd.to_datetime(comment_row['created_at']).strftime('%Y-%m-%d %H:%M')}</div>
                                <div class="comment-text">{comment_row['comment']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # New comment form
                    st.subheader("Add Your Comment")
                    with st.form(key=f"comment_form_{key_prefix}"):
                        user_name = st.text_input("Your Name (optional)", value="Anonymous", key=f"name_{key_prefix}")
                        comment = st.text_area("Your Comment", key=f"comment_{key_prefix}", placeholder="Share your thoughts...")
                        submit_button = st.form_submit_button("Submit Comment")
                        
                        if submit_button:
                            success, message = save_comment(key_prefix, comment, user_name)
                            if success:
                                st.success(message)
                                st.rerun()  # Refresh to show new comment
                            else:
                                st.error(message)

        # Define source lists for each section
        ai_sources = [
            s for s in df['Source'].unique() 
            if any(x in s for x in ["AI", "Artificial Intelligence", "Anthropic", "DeepMind", "OpenAI", "TechCrunch AI"])
        ]
        
        automation_sources = [
            s for s in df['Source'].unique()
            if any(x in s for x in ["Automation", "CIO", "Industry", "Engineering", "Design News", "Control"])
        ]
        
        medium_sources = [
            s for s in df['Source'].unique()
            if "Medium:" in s
        ]

        # Display sections
        news_section(" 🧠 AI Industry News", ai_sources, "ai")
        news_section(" 🤖 Automation Feeds", automation_sources, "automation")
        news_section(" 📝 Medium.com Articles", medium_sources, "medium")

if __name__ == "__main__":
    # This allows the app to run both on Vercel and locally
    pass



