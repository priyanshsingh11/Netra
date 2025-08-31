import pandas as pd
from datasets import Dataset, ClassLabel

# Load your CSV
df = pd.read_csv("twitte_csv.csv")

df['label'] = df['label'].map({'Negative': 1, 'Positive': 0})

# Save the converted dataset
df.to_csv('twitter_csv_converted.csv', index=False, encoding='utf-8')
print("Converted dataset saved as 'twitter_csv_converted.csv'")