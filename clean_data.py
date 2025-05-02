# clean_data.py

import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def clean_html(text):
    try:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()
    except Exception as e:
        print(f"Error cleaning HTML: {e}")
        return text

def extract_date(date_str):
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
    if df.empty:
        return df

    try:
        df['date'] = df['Published'].apply(extract_date)
        df = df.dropna(subset=['date'])

        # 📅 Year-to-Date (YTD) filter instead of last 7 days
        today = datetime.now()
        start_of_year = datetime(today.year, 1, 1)
        df_filtered = df[(df['date'] >= start_of_year) & (df['date'] <= today)]
        df_filtered = df_filtered.sort_values(by='date', ascending=False)

        df_filtered['Description'] = df_filtered['Description'].apply(
            lambda x: clean_html(x)[:500].replace("\n", "") if isinstance(x, str) else ""
        )

        df_filtered.drop(columns=['Published'], inplace=True)
        return df_filtered

    except Exception as e:
        print(f"Error processing data: {e}")
        return pd.DataFrame()
