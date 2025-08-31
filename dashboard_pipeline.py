import pandas as pd
from collections import Counter
import streamlit as st
from transformers import pipeline


full_df = pd.read_csv("tweets_dataset.csv")  
TEXT_COL = 'content'  


@st.cache_resource
def load_model():
    return pipeline("text-classification", model=r"C:\Users\Priyansh Singh\Desktop\Netra\fine-tuned-twitter-model")  

classifier = load_model()

def predict_label(text):
    result = classifier(
        text,
        truncation=True,  
        max_length=512
    )[0]
    label = 1 if result['label'].lower() in ["1", "anti-india"] else 0
    return label


st.title("Anti-India Campaign Dashboard")

st.subheader("Flagged Posts")
st.write(f"Dataset has {len(full_df)} posts.")

if st.button("Run Predictions"):
    full_df['predicted_label'] = 0

    progress_bar = st.progress(0)
    
    for i, row in full_df.iterrows():
        full_df.at[i, 'predicted_label'] = predict_label(row[TEXT_COL])
        progress_bar.progress((i+1)/len(full_df))
    
    st.success("Predictions completed!")

    full_df['engagement'] = full_df['likes'] + 2*full_df['retweets'] + 3*full_df['replies']


    top_influencers = full_df.groupby('user')['engagement'].sum().sort_values(ascending=False).head(10)

    hashtags_list = full_df['query'].dropna().apply(lambda x: x.split(','))  
    all_hashtags = [tag.strip() for sublist in hashtags_list for tag in sublist]
    trending_hashtags = Counter(all_hashtags).most_common(10)

    ALERT_HASHTAG_COUNT = 50
    ALERT_ENGAGEMENT_SCORE = 10000

    high_activity_hashtags = [tag for tag, count in Counter(all_hashtags).items() if count > ALERT_HASHTAG_COUNT]
    high_engagement_posts = full_df[full_df['engagement'] > ALERT_ENGAGEMENT_SCORE]


    st.subheader("Flagged Posts with Predictions")
    st.dataframe(full_df[['user', TEXT_COL, 'predicted_label', 'likes', 'retweets', 'replies', 'engagement']])

    st.subheader("Top Influencers")
    st.table(top_influencers)

    st.subheader("Trending Hashtags")
    st.write(trending_hashtags)

    st.subheader("Alerts")
    st.write(f"High-activity hashtags: {high_activity_hashtags}")
    st.write(f"High-engagement posts:")
    st.dataframe(high_engagement_posts[['user', TEXT_COL, 'predicted_label', 'engagement']])
