from wordcloud import WordCloud
from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji 
extract=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    num_messages=df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split())
    num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]
    
    #   fetch number of link shared
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages,len(words),num_media_messages,len(links)

def most_busy_user(df):
    x=df['user'].value_counts().head()
    df= round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns={'index':'name','user':'percent'}
    )
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    emojis=[]
    for message in df['message']:
        #emojis.extend([c for c in message if c in EMOJI_DATA['en']])
        emojis.extend(emoji.emoji_list(message))
        print(emojis)
        print(type(emojis))
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def hepler(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    df['month_num']=df['date'].df.month
    timeline=df.groupby(['year','month_num']).count()['message']
