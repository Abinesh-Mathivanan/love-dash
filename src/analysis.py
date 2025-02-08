import pandas as pd
from collections import Counter
import re
import emoji
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob


nltk.download('stopwords', quiet=True)

def get_most_common_words(df, top_n=20):
    messages = " ".join(df["message"].tolist())
    words = re.findall(r'\w+', messages.lower())
    stop_words = set(stopwords.words('english'))
    words_filtered = [word for word in words if word not in stop_words and len(word) > 2]
    counter = Counter(words_filtered)
    return counter.most_common(top_n)

def sentiment_analysis(df):
    df = df.copy()
    df["sentiment"] = df["message"].apply(lambda x: TextBlob(x).sentiment.polarity)
    return df

def get_peak_hours(df):
    df = df.copy()
    df["hour"] = df["datetime"].dt.hour
    hour_counts = df.groupby("hour").size()
    return hour_counts

def get_peak_days(df):
    df = df.copy()
    df["day_of_week"] = df["datetime"].dt.day_name()
    day_counts = df.groupby("day_of_week").size()
    return day_counts

def get_messages_by_month(df):
    df = df.copy()
    df["month_year"] = df["datetime"].dt.to_period("M")
    month_counts = df.groupby("month_year").size()
    return month_counts

def get_emoji_usage(df, top_n=10):
    all_emojis = []
    for message in df["message"]:
        all_emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_counts = Counter(all_emojis)
    return emoji_counts.most_common(top_n)
