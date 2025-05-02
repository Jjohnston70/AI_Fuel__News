# clean_data.py

import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def clean_html(text):
    """Remove HTML tags and return clean text."""
    try:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()
    except Exception as e:
        print(f"Error cleaning HTML: {e}")
        return text

def extract_date(date_str):
    """Try to parse date from different RSS formats."""
    patterns = [
        r'(?:\w+,\s+)?(\d{1,2}\s+\w{3}\s+\d{4})',  # Ex: Mon, 01 May 2023
        r'(\d{1,2}\s+\w{3}\s+\d{4})',              # Ex: 01 May 2023
        r'(\d{4}-\d{2}-\d{2})'                     # ISO format
    ]
    for pattern in patterns:
        match = re.search(pattern, date_str)
        if match:
            try:
                return pd.to_datetime(match.group(1), errors='coerce')
            except:
                continue
    return pd.NaT

def extract_and_clean_data(df):
    """Extract and clean RSS feed dataframe for display in dashboard."""
    if df.empty:
        return df

    try:
        # Extract and convert date
        df['date'] = df['Published'].apply(extract_date)
        df = df.dropna(subset=['date'])

        # Filter to past 7 days
        today = datetime.now()
        week_ago = today - timedelta(days=7)
        df_filtered = df[(df['date'] >= week_ago) & (df['date'] <= today)]
        df_filtered = df_filtered.sort_values(by='date', ascending=False)

        # Clean up descriptions
        df_filtered['Description'] = df_filtered['Description'].apply(
            lambda x: clean_html(x)[:500].replace("\n", "") if isinstance(x, str) else ""
        )

        # Drop the raw Published column
        df_filtered.drop(columns=['Published'], inplace=True)

        return df_filtered

    except Exception as e:
        print(f"Error processing data: {e}")
        return pd.DataFrame()
