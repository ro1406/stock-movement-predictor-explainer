# Stock Movement Predictor & Explainer
Predict stock price movement with timeseries analysis and current news articles and explain the predictions using XAI


Setup steps:

1) NewsAPI.org account → get a free API Key
2) Set the API key in env
    ```export NEWSAPI_KEY = <your_api_key> ```
    (or write to .env file)

3) Run `python train.py` to train the model and save it to `/src/models`
4) If you already have a model saved / downloaded a checkpoint, then run individual predictions using 
    `python run_pipeline.py`
5) If you want to run this through a streamlit frontend interface, then use:
    `python app.py`

