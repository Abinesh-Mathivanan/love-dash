import matplotlib.pyplot as plt
import seaborn as sns

def plot_common_words(common_words):
    words, counts = zip(*common_words)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(counts), y=list(words))
    plt.xlabel("Count")
    plt.ylabel("Words")
    plt.title("Most Common Words")
    plt.tight_layout()
    plt.show()

def plot_peak_hours(hour_counts):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=hour_counts.index, y=hour_counts.values)
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Messages")
    plt.title("Messages per Hour")
    plt.tight_layout()
    plt.show()

def plot_peak_days(day_counts):
    plt.figure(figsize=(10, 6))
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_counts = day_counts.reindex(order)
    sns.barplot(x=day_counts.index, y=day_counts.values)
    plt.xlabel("Day of Week")
    plt.ylabel("Number of Messages")
    plt.title("Messages per Day")
    plt.tight_layout()
    plt.show()

def plot_messages_by_month(month_counts):
    plt.figure(figsize=(12, 6))
    month_counts = month_counts.sort_index()
    month_counts.plot(kind="bar")
    plt.xlabel("Month-Year")
    plt.ylabel("Number of Messages")
    plt.title("Messages by Month")
    plt.tight_layout()
    plt.show()

def plot_emoji_usage(emoji_counts):
    emojis, counts = zip(*emoji_counts)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(counts), y=list(emojis))
    plt.xlabel("Count")
    plt.ylabel("Emoji")
    plt.title("Most Common Emojis")
    plt.tight_layout()
    plt.show()
