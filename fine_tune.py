import pandas as pd
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
from datasets import Dataset
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
import os


# Load dataset
df = pd.read_csv('twitter_csv.csv')

# Split data
train_texts, test_texts, train_labels, test_labels = train_test_split(
    df['content'].tolist(), 
    df['label'].tolist(), 
    test_size=0.2, 
    random_state=42,
    stratify=df['label']
)

print(f"Train samples: {len(train_texts)}")
print(f"Test samples: {len(test_texts)}")

# Load model and tokenizer
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"  # Smaller version
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME, 
    num_labels=2,
    ignore_mismatched_sizes=True
)

# Tokenize function
def tokenize_function(examples):
    return tokenizer(examples['text'], truncation=True, padding=True, max_length=256)

# Prepare datasets
train_dataset = Dataset.from_dict({'text': train_texts, 'labels': train_labels})
test_dataset = Dataset.from_dict({'text': test_texts, 'labels': test_labels})

tokenized_train = train_dataset.map(tokenize_function, batched=True)
tokenized_test = test_dataset.map(tokenize_function, batched=True)

# Training arguments for Transformers 4.56.0
training_args = TrainingArguments(
    output_dir='./fine-tuned-model',
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=50,
    eval_strategy='epoch',  
    save_strategy='epoch',
    load_best_model_at_end=True,
)

# Compute metrics
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    accuracy = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average='weighted')
    return {'accuracy': accuracy, 'f1': f1}


# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_test,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# Train
trainer.train()

# Save model
trainer.save_model('./fine-tuned-twitter-model')
tokenizer.save_pretrained('./fine-tuned-twitter-model')

# Evaluate
results = trainer.evaluate()
print(f"Final Accuracy: {results['eval_accuracy']:.4f}")
print(f"Final F1 Score: {results['eval_f1']:.4f}")