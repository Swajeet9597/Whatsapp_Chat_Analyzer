from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import wordcloud, WordCloud
from collections import Counter
import pandas as pd
import emoji


def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    total_messages = df.shape[0]
    words = []
    for i in df['Message']:
        words.extend(i.split())

    total_media = df[df['Message'] == "<Media omitted>\n"].shape[0]

    links = []
    extractor = URLExtract()
    for i in df['Message']:
        links.extend(extractor.find_urls(i))

    return total_messages, len(words), total_media, len(links)


def mostacive(df):
    x = df['User'].value_counts().head()
    new_df = round(df['User'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'User': 'Percentage'})

    return x, new_df


def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != "group_notification"]
    temp = temp[temp['Message'] != "<Media omitted>\n"]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Message'].str.cat(sep=" "))

    return df_wc


def most_common_word(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != "group_notification"]
    temp = temp[temp['Message'] != "<Media omitted>\n"]

    words = []

    for messagee in temp['Message']:
        for word in messagee.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df


def emoji_analysis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    emojis = []
    for i in df['Message']:
        emojis.extend([c for c in i if c in emoji.UNICODE_EMOJI])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def timeline_monthly(selected_user,df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def week_activity(selected_user,df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    return df['day_name'].value_counts()

def month_activity(selected_user,df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    return df['month'].value_counts()