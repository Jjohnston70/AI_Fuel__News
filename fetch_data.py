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
        future_to_link = {executor.submit(fetch_single_feed, (link, source)): (link, source) for link, source in links.items()}
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
        "https://bair.berkeley.edu/blog/feed.xml": "The Berkeley Artificial Intelligence Research Blog",
        "https://feeds.feedburner.com/nvidiablog": "NVDIA Blog",
        "https://www.microsoft.com/en-us/research/feed/": "Microsoft Research",
        "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml": "Science Daily",
        "https://research.facebook.com/feed/": "META Research",
        "https://openai.com/news/rss.xml": "OpenAI News",
        "https://deepmind.google/blog/feed/basic/": "Google DeepMind Blog",
        "https://news.mit.edu/rss/topic/artificial-intelligence2": "MIT News - Artificial intelligence",
        "https://www.technologyreview.com/topic/artificial-intelligence/feed": "MIT Technology Review",
        "https://www.wired.com/feed/tag/ai/latest/rss": "Wired: Artificial Intelligence Latest",
        "https://raw.githubusercontent.com/Olshansk/rss-feeds/refs/heads/main/feeds/feed_ollama.xml": "Ollama Blog",
        "https://raw.githubusercontent.com/Olshansk/rss-feeds/refs/heads/main/feeds/feed_anthropic.xml": "Anthropic News","https://www.eia.gov/rss/pressreleases.xml": "EIA Press Releases",
    "https://www.api.org/rss/feed": "API News",
    "https://www.convenience.org/RSS-Feeds/News-Releases": "NACS News",
    "https://oilprice.com/rss/main": "OilPrice.com Energy News",
    "https://www.reutersagency.com/feed/?best-topics=commodities-energy": "Reuters Commodities Energy",
    "https://feeds.marketwatch.com/marketwatch/energy": "MarketWatch Energy",
    "https://www.bloomberg.com/feeds/bpol/news-energy.xml": "Bloomberg Energy News"
    }
    df = fetch_feed(links)
    final_df = extract_and_clean_data(df)
    return final_df
