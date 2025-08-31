from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="./fine-tuned-twitter-model",
    tokenizer="./fine-tuned-twitter-model"
)

app = FastAPI(title="Anti-India Sentiment Classifier API")

class TextRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Welcome to Anti-India Sentiment Classifier API 🚀"}

@app.post("/predict")
def predict_sentiment(request: TextRequest):
    result = classifier(request.text)[0]
    
    label = result['label']
    score = result['score']

    if label == "LABEL_1":
        final_label = "Anti-India"
    elif label == "LABEL_0":
        final_label = "Pro-India"
    else:
        final_label = "Unknown"

    return {
        "text": request.text,
        "raw_label": label,
        "confidence": round(score, 4),
        "final_prediction": final_label
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

