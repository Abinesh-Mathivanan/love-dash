# src/dashboard.py

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

from data_extraction import parse_chat
from analysis import (
    get_most_common_words,
    sentiment_analysis,
    get_peak_hours,
    get_peak_days,
    get_messages_by_month,
    get_emoji_usage,
)

sns.set_style("darkgrid")
plt.rcParams.update({
    'font.size': 8,
    'axes.titlesize': 10,
    'axes.labelsize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    'figure.titlesize': 10
})


st.set_page_config(layout="wide")
st.title("WhatsApp Chat Analysis Dashboard")

uploaded_file = st.file_uploader("Upload WhatsApp Chat Export (.txt)", type="txt")
if uploaded_file is not None:
    df = parse_chat(uploaded_file)
    
    st.sidebar.header("Options")
    if st.sidebar.checkbox("Show Raw Data"):
        st.subheader("Raw Chat Data")
        st.dataframe(df.head(), height=200)
    
    # --- Most Common Words (Table) ---
    st.header("Most Common Words")
    common_words = get_most_common_words(df)
    common_words_df = pd.DataFrame(common_words, columns=["Word", "Count"])
    st.dataframe(common_words_df, height=250, use_container_width=True)
    
    # -------------------------------
    # ROW 1: Common Words Chart & Sentiment Distribution
    # -------------------------------
    
    row1_cols = st.columns(2)
    
    # Common Words Chart
    with row1_cols[0]:
        st.subheader("Common Words Chart")
        fig, ax = plt.subplots(figsize=(5, 3), dpi=150)
        if common_words:
            words, counts = zip(*common_words)
            y_pos = np.arange(len(words))
            colors = plt.cm.plasma(np.linspace(0.2, 0.8, len(words)))
            ax.barh(y_pos, counts, color=colors, height=0.8)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(words)
            ax.invert_yaxis()
            ax.set_xlabel("Count")
            plt.tight_layout()
        st.pyplot(fig)
    
    # Sentiment Distribution
    with row1_cols[1]:
        st.subheader("Sentiment Distribution")
        df = sentiment_analysis(df)
        fig, ax = plt.subplots(figsize=(5, 3), dpi=150)
        ax.hist(df["sentiment"], bins=30, color='#2ecc71', alpha=0.8, edgecolor='black')
        ax.set_xlabel("Sentiment Score")
        ax.set_ylabel("Frequency")
        plt.tight_layout()
        st.pyplot(fig)
    
    # -------------------------------
    # ROW 2: Peak Chat Hours & Peak Chat Days
    # -------------------------------

    row2_cols = st.columns(2)
    
    # Peak Chat Hours
    with row2_cols[0]:
        st.subheader("Peak Chat Hours")
        fig, ax = plt.subplots(figsize=(5, 3), dpi=150)
        hour_counts = get_peak_hours(df)
        ax.plot(hour_counts.index, hour_counts.values, 
               color='#3498db', marker='o', markersize=4, linewidth=2)
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Messages")
        ax.set_xticks(range(0, 24))
        plt.tight_layout()
        st.pyplot(fig)
    
    # Peak Chat Days
    with row2_cols[1]:
        st.subheader("Peak Chat Days")
        fig, ax = plt.subplots(figsize=(5, 3), dpi=150)
        day_counts = get_peak_days(df)
        order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_counts.index = day_counts.index.str[:3]
        day_counts = day_counts.reindex(order)
        ax.bar(day_counts.index, day_counts.values, 
              color='#9b59b6', alpha=0.8, edgecolor='black')
        ax.set_xlabel("Day of Week")
        ax.set_ylabel("Messages")
        plt.tight_layout()
        st.pyplot(fig)
    
    # -------------------------------
    # ROW 3: Messages by Month & Emoji Analysis
    # -------------------------------

    row3_cols = st.columns(2)
    
    # Messages by Month
    with row3_cols[0]:
        st.subheader("Messages by Month")
        fig, ax = plt.subplots(figsize=(5, 3), dpi=150)
        month_counts = get_messages_by_month(df)
        month_counts = month_counts.sort_index()
        ax.plot(month_counts.index.astype(str), month_counts.values,
               color='#e74c3c', marker='s', markersize=4, linewidth=2)
        ax.set_xlabel("Month")
        ax.set_ylabel("Messages")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    
    # Emoji Analysis
    with row3_cols[1]:
        st.subheader("Emoji Analysis")
        emoji_counts = get_emoji_usage(df)
        if emoji_counts:
            fig, ax = plt.subplots(figsize=(5, 3), dpi=150)
            emojis, counts = zip(*emoji_counts)
            y_pos = np.arange(len(emojis))
            colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(emojis)))
            ax.barh(y_pos, counts, color=colors, height=0.8)
            ax.set_yticks(y_pos)
            
            try:
                from matplotlib import font_manager
                emoji_font = font_manager.FontProperties(fname="C:/Windows/Fonts/seguiemj.ttf")
            except Exception as e:
                st.error("Could not load emoji font: " + str(e))
                emoji_font = None

            if emoji_font:
                ax.set_yticklabels(emojis, fontproperties=emoji_font, fontsize=10)
            else:
                ax.set_yticklabels(emojis, fontsize=10)
            
            ax.invert_yaxis()
            ax.set_xlabel("Count")
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No emojis found in the chat")
