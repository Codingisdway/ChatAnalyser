import streamlit as slt
import preprocessor,appUtil
from matplotlib import pyplot as plt

slt.sidebar.title('Chat Analyzer')

#space to upload file

upload_file=slt.sidebar.file_uploader("Choose a file")
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode('utf-8')
    #slt.text(data)
    df=preprocessor.preprocess(data)

    slt.dataframe(df.head())

    #   fetch unique user
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=slt.sidebar.selectbox('show analysis',user_list)
    if slt.sidebar.button("Show analysis"):
        num_messages,words,num_media_messages,num_links=appUtil.fetch_stats(selected_user,df)
        #col1,col2,col3,col4=slt.beta_columns(4)
        #with col1:
        slt.header("total messages")
        slt.title(num_messages)
        #with col2:
        slt.header("Total Words")
        slt.title(words)
        #with col3:
        slt.header('Media Shared')
        slt.title(num_media_messages)
        #with col4:
        slt.header('Link Shared')
        slt.title(num_links)
        
        #finding the busiest user in the group
        if selected_user=='Overall':
            slt.title('most busy user')
            x,new_df=appUtil.most_busy_user(df)
            #fig,ax=plt.subplot()
            
            #col1,col2=slt.beta_columns(2)

            #with col1:
            plt.bar(x.index,x.values,color='red')
            plt.xticks(rotation='vertical')
            slt.pyplot(plt.show())
            #with col2:
            slt.title('chat contribution of each')
            slt.dataframe(new_df)
        
        #emoji
        emoji_df=appUtil.emoji_helper(selected_user,df)
        slt.dataframe(emoji_df)
        

