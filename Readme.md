📈 TrueNorth Data Strategies News Dashboard
AI & Automation Industry News Aggregator and Dashboard
Built with ❤️ using Streamlit, Python, and a sprinkle of badassery.

🚀 Project Overview
The TrueNorth News Dashboard is a sleek, mobile-optimized Streamlit web app that fetches and displays the latest news in:

🧠 Artificial Intelligence

🤖 Automation Industry

📝 Medium.com Articles

The dashboard allows users to:

Toggle between Dark and Light themes

Filter news articles by source and date range

Leave comments and feedback for each section

Access TrueNorth's website and social media directly

Fully customized with side logos, hover effects, a manual theme switcher, and even glow effects for that extra pizzazz. 🎉

🗂️ Project Structure
```
📂 project-root/
├── app.py           # Main Streamlit application
├── clean_data.py    # Functions for cleaning and preparing news data
├── fetch_data.py    # Functions for fetching RSS feeds and converting to clean DataFrame
├── requirements.txt # Python package dependencies
├── vercel.json      # Vercel deployment configuration
├── setup.sh         # Setup script for deployment
├── Procfile         # Process file for deployment
├── README.md        # This beautiful documentation
├── 📂 images/        # Folder for logos
```

⚙️ Setup Instructions
1. Clone the Repo
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Install Python Dependencies
First, create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

3. Run the App Locally
```bash
streamlit run app.py
```

Boom — it will open in your browser at http://localhost:8501.

🚀 Deploying to Vercel

1. Install Vercel CLI (optional)
```bash
npm install -g vercel
```

2. Deploy using Vercel CLI
```bash
vercel
```

3. Alternative: Deploy via GitHub
   - Push your code to GitHub
   - Connect your GitHub account to Vercel
   - Select your repository and deploy

4. Important Settings for Vercel
   - Make sure to set the Framework Preset to "Other"
   - The production command should be: `sh setup.sh && streamlit run app.py`
   - The output directory can be left as default (public)

📡 How It Works
fetch_data.py grabs RSS feeds from selected AI and automation industry sources asynchronously for faster loading.

clean_data.py processes, cleans HTML junk, extracts dates, and filters news from the current year.

app.py renders the dashboard beautifully with:

- Sidebar theme toggle
- AI, Automation, and Medium.com news sections
- Date range and source filters
- Manual data refresh button
- User comment boxes
- Links to TrueNorth's website and Facebook page

🖼️ Screenshot
(Drop a nice screenshot here if you want more brownie points.)

🏷️ Key Features
- 🌗 Manual Dark/Light Theme Toggle
- 📅 Date range filtering
- 📰 Source-based filtering
- 🚀 Threaded fetching for faster news loading
- 📱 Fully mobile-optimized
- ✨ Logo sidebar, hover effects, soft glows, and footer credits
- 🔄 Manual data refresh to get the latest news instantly
- 🌐 Vercel deployment ready
- 🔗 Direct links to TrueNorth's online presence

🔮 Future Improvements
- Email notifications when new news is posted
- Admin-only comments panel
- Integrate AI summarization for long articles
- Allow user-defined RSS feed imports
- Additional news sources and categories

🤖 Credits
Built by TrueNorth Data Strategies Team

📱 Connect with TrueNorth
- 🌐 [Website](https://www.truenorthstrategyops.com/)
- 📘 [Facebook](https://www.facebook.com/profile.php?viewas=100000686899395&id=61577047841328)