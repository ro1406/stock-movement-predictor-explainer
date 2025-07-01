import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
from tqdm import tqdm
from pathlib import Path

# Load model and tokenizer once at module level
MODEL_NAME = "ProsusAI/finbert"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.to(DEVICE)
model.eval()

LABELS = ["negative", "neutral", "positive"]  # Order is fixed in FinBERT


def analyze_sentiment(texts: list[str], batch_size: int = 16) -> pd.DataFrame:
    """
    Run FinBERT sentiment analysis on a list of texts (news headlines).
    
    Returns a DataFrame with probabilities and predicted label.
    """
    results = []

    for i in tqdm(range(0, len(texts), batch_size), desc="Analyzing sentiment"):
        batch = texts[i:i + batch_size]
        encodings = tokenizer(
            batch,
            truncation=True,
            padding=True,
            return_tensors="pt"
        ).to(DEVICE)

        with torch.no_grad():
            outputs = model(**encodings)
            probs = softmax(outputs.logits, dim=1).cpu().numpy()

        for j, text in enumerate(batch):
            result = {
                "text": text,
                "negative": probs[j][0],
                "neutral": probs[j][1],
                "positive": probs[j][2],
                "predicted_sentiment": LABELS[probs[j].argmax()]
            }
            results.append(result)

    return pd.DataFrame(results)

if __name__ == "__main__":
    print("Sentiment analysis with FinBERT")
    print(analyze_sentiment(["AAPL Stocks have come crashing down.", 
                             "AAPL backs F1 movie", 
                             "Apple launches the new and much anticipated iPhone 19ProMax"]))