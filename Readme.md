📈 Chief Petroleum News Dashboard
Fuel & AI Industry News Aggregator and Dashboard
Built with ❤️ using Streamlit, Python, and a sprinkle of badassery.

🚀 Project Overview
The Chief Petroleum News Dashboard is a sleek, mobile-optimized Streamlit web app that fetches and displays the latest news in:

🧠 Artificial Intelligence

🚛 Fuel & Petroleum Industry

The dashboard allows users to:

Toggle between Dark and Light themes

Filter news articles by source and date range

Leave comments and feedback for each section

Fully customized with side logos, hover effects, a manual theme switcher, and even glow effects for that extra pizzazz. 🎉

🗂️ Project Structure
bash
Copy
Edit
📂 project-root/
├── app.py           # Main Streamlit application
├── clean_data.py    # Functions for cleaning and preparing news data
├── fetch_data.py    # Functions for fetching RSS feeds and converting to clean DataFrame
├── requirements.txt # Python package dependencies (to be created)
├── README.md        # This beautiful documentation
├── 📂 images/        # Folder for logos (Chief_Logo.png, TrueNorthLogo.jpg)
⚙️ Setup Instructions
1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2. Install Python Dependencies
First, create and activate a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
Install the required libraries:

bash
Copy
Edit
pip install -r requirements.txt
If you don't have a requirements.txt yet, here's a starter:

nginx
Copy
Edit
streamlit
pandas
beautifulsoup4
feedparser
Pillow
3. Run the App
bash
Copy
Edit
streamlit run app.py
Boom — it will open in your browser at http://localhost:8501.

📡 How It Works
fetch_data.py grabs RSS feeds from selected AI and Fuel industry sources asynchronously for faster loading.

clean_data.py processes, cleans HTML junk, extracts dates, and filters news from the past 7 days.

app.py renders the dashboard beautifully with:

Sidebar theme toggle

AI and Fuel news sections

Date range and source filters

Manual data refresh button

User comment boxes

🖼️ Screenshot
(Drop a nice screenshot here if you want more brownie points.)

🏷️ Key Features
🌗 Manual Dark/Light Theme Toggle

📅 Date range filtering

📰 Source-based filtering

🚀 Threaded fetching for faster news loading

📱 Fully mobile-optimized

✨ Logo sidebar, hover effects, soft glows, and footer credits

🔄 Manual data refresh to get the latest news instantly

🔮 Future Improvements (Optional Ideas)
Email notifications when new news is posted

Admin-only comments panel

Integrate AI summarization for long articles

Allow user-defined RSS feed imports

Deploy to Streamlit Community Cloud (easy 1-click deployment!)

🤖 Credits
Built by Jacob Johnston
(aka the Chief of Petroleum and Captain of Cool Dashboards.)