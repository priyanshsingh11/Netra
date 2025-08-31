import pandas as pd

df = pd.read_csv("tweets.csv")

# Drop duplicates
df.drop_duplicates(subset="text", inplace=True)

print(df.head())
print(df.shape)
