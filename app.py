import streamlit as st
import preprocessing,helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessing.preprocess(data)

    # st.dataframe(df)

    user_list=df['User'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")


    selected_user = st.sidebar.selectbox("Show Analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        total_messages,words,total_media,links = helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        # fetching stats
        with col1:
            st.header("Total Messages")
            st.title(total_messages)

        with col2:
            st.header("Toatal Words")
            st.title(words)

        with col3:
            st.header("Total Media Shared")
            st.title(total_media)

        with col4:
            st.header("Total Links shared")
            st.title(links)


        # timeline

        st.title("Monthly Timeline")
        timeline = helper.timeline_monthly(selected_user,df)

        fig,ax= plt.subplots()
        ax.plot(timeline['time'], timeline['Message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #Weekly_activity
        st.title("Activity Map")



        col1,col2 = st.columns(2)

        with col1:
            weekly = helper.week_activity(selected_user, df)

            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')

            ax.bar(weekly.index,weekly.values)

            st.pyplot(fig)

        with col2:
            month = helper.month_activity(selected_user, df)

            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')

            ax.bar(month.index,month.values)

            st.pyplot(fig)






        # finding active person im group (only for group chat)
        if selected_user == "Overall":

            st.title("Most Active user")
            x,new_df= helper.mostacive(df)
            fig,ax =plt.subplots()


            col5, col6 = st.columns(2)

            with col5:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col6:
                st.dataframe(new_df)

        st.title("WordCloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("Most Common words")
        most_common_df=helper.most_common_word(selected_user,df)

        # fig,ax=plt.subplots()
        # ax.bar(most_common_df[0],most_common_df[1])
        # plt.xticks(rotation='vertical')

        # st.pyplot(fig)
        st.dataframe(most_common_df)

        # emoji analysis

        st.title("Emoji Analysis")
        emoji_df = helper.emoji_analysis(selected_user,df)

        st.dataframe(emoji_df)


















