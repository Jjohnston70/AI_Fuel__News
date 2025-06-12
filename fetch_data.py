# fetch_data.py

import feedparser
import concurrent.futures
import pandas as pd
from clean_data import extract_and_clean_data

def fetch_single_feed(link_source_tuple):
    link, source = link_source_tuple
    entries = {"Title": [], "Link": [], "Published": [], "Description": [], "Source": []}

    try:
        feed = feedparser.parse(link)
        for entry in feed.entries:
            entries["Title"].append(entry.get("title", "No Title"))
            entries["Link"].append(entry.get("link", "No Link"))
            entries["Published"].append(entry.get("published", "No Date"))
            entries["Description"].append(entry.get("description", "No Description"))
            entries["Source"].append(source)
    except Exception as e:
        print(f"Error fetching {link}: {e}")

    return entries

def fetch_feed(links):
    all_entries = {"Title": [], "Link": [], "Published": [], "Description": [], "Source": []}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_link = {
            executor.submit(fetch_single_feed, (link, source)): (link, source)
            for link, source in links.items()
        }
        for future in concurrent.futures.as_completed(future_to_link):
            try:
                result = future.result()
                for key in all_entries:
                    all_entries[key].extend(result[key])
            except Exception as e:
                print(f"Exception: {e}")

    df = pd.DataFrame(all_entries)
    return df

def main():
    links = {
        # AI Industry News
        "https://www.artificialintelligence-news.com/feed/": "Artificial Intelligence News",
        "https://techcrunch.com/category/artificial-intelligence/feed/": "TechCrunch AI",
        "https://bair.berkeley.edu/blog/feed.xml": "Berkeley AI Research Blog",
        "https://feeds.feedburner.com/nvidiablog": "NVDIA Blog",
        "https://openai.com/news/rss.xml": "OpenAI News",
        "https://deepmind.google/blog/feed/basic/": "Google DeepMind Blog",
        "https://news.mit.edu/rss/topic/artificial-intelligence2": "MIT News - AI",
        "https://www.technologyreview.com/topic/artificial-intelligence/feed": "MIT Technology Review - AI",
        "https://www.wired.com/feed/tag/ai/latest/rss": "Wired: AI Latest",
        "https://raw.githubusercontent.com/Olshansk/rss-feeds/refs/heads/main/feeds/feed_anthropic.xml": "Anthropic News",

        # Automation Feeds
        "https://www.automationworld.com/rss/all": "Automation World",
        "https://www.automationanywhere.com/company/press-room/rss.xml": "Automation Anywhere",
        "https://www.ciodive.com/rss/": "CIO Dive",
        "https://www.industryweek.com/taxonomy/term/6786/feed": "IndustryWeek Automation",
        "https://www.machinedesign.com/taxonomy/term/28301/feed": "Machine Design Automation",
        "https://www.controleng.com/rss/topic/5348": "Control Engineering",
        "https://www.designnews.com/taxonomy/term/43261/feed": "Design News - Automation",
        
        # Medium.com Feeds
        "https://medium.com/feed/tag/python": "Medium: Python",
        "https://medium.com/feed/tag/ai": "Medium: AI",
        "https://medium.com/feed/tag/machine-learning": "Medium: Machine Learning",
        "https://medium.com/feed/tag/data-visualization": "Medium: Data Visualization",
        "https://medium.com/feed/tag/business-intelligence": "Medium: Business Intelligence",
        "https://medium.com/feed/tag/automation": "Medium: Automation",
        "https://medium.com/feed/tag/data-science": "Medium: Data Science",
        "https://medium.com/feed/tag/programming": "Medium: Programming",
        "https://medium.com/feed/tag/technology": "Medium: Technology",
        "https://medium.com/feed/tag/software-development": "Medium: Software Development",
        "https://medium.com/feed/tag/coding": "Medium: Coding",
        "https://medium.com/feed/tag/web-development": "Medium: Web Development",
        "https://medium.com/feed/tag/productivity": "Medium: Productivity",
    }

    raw_df = fetch_feed(links)
    clean_df = extract_and_clean_data(raw_df)
    return clean_df
