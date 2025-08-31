import requests
import pandas as pd

# Load scraped tweets
df = pd.read_csv("tweets_dataset.csv")  

url = "http://127.0.0.1:8000/predict"

predictions = []

for text in df['content']:
    response = requests.post(url, json={"text": text})
    result = response.json()
    predictions.append({
        "prediction": result['final_prediction'],
        "confidence": result['confidence']
    })

pred_df = pd.DataFrame(predictions)
df = pd.concat([df, pred_df], axis=1)

df.to_csv("tweets_with_predictions.csv", index=False)
print("Predictions added and saved to tweets_with_predictions.csv")
