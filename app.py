import streamlit as st
from collections import Counter
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import preprocessor,helper
st.sidebar.title("Whatsapp Chat Analyser")

#get the below part from documentation
uploaded_file =st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data =uploaded_file.getvalue()
    #This is a stream so I have to convert to string
    data = bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    #Now basics are finished
    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user=st.sidebar.selectbox("Show analysis for",user_list)

    if st.sidebar.button("Analyze"):

        st.title("Top Statistics")
        num_messages,words,num_med,num_link=helper.fetch_stats(selected_user, df)
        #Now we will be showing the stats
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        
        with col3:
            st.header("Total media shared")
            st.title(num_med)
        with col4:
            st.header("Total links shared")
            st.title(num_link)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Daily timeline
        st.title('Daily Timeline')

        timeline2=helper.daily_timeline(selected_user,df)
        fig, ax= plt.subplots()
        ax.plot(timeline2['only_date'],timeline2['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity map
        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #finding busiest users in the group
        if(selected_user=='Overall'):
            st.title('Most busy users')
            x,new_df=helper.most_busy_users(df)
            fig, ax =plt.subplots()
            
            col1, col2 =st.columns(2)

            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical',color='red')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #Make Wordcloud
        st.title("Wordcloud:")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        