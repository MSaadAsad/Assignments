import requests
import json
import os
import random
from dotenv import load_dotenv
load_dotenv()

# Google API Key for function calls
# Note: this key is editable from cloud console and has preset limits 
gc_virtual_api_key = os.environ.get("GC_API_KEY")

# kept dormant now for testing purposes
def get_scoresSA(text):
    # Constructing the URL with the API key
    url_SA = f'https://us-central1-starcai.cloudfunctions.net/entry_pointSA?apikey={gc_virtual_api_key}'
    # Making the POST request with JSON data, this returns a response object in string format here for 'text' 
    response_SA = requests.post(url_SA, json={'text': text})

    # Parse the response text to a Python list
    scores = json.loads(response_SA.text)
    # Check if the scores are list and convert each element to float to be stored in our database
    if isinstance(scores, list):
        scores = [float(score) for score in scores]
        
    # return the sentiment scores from the cloud function
    # Order: Overall Score, Optimism, Confidence, Strategic Forecasts
    return scores

# base function for placeholder scores
def get_scores(text):
    random_numbers = [random.uniform(1,100) for _ in range(4)]
    return random_numbers

def get_rewrite(original_text):
    # Constructing the URL with the API key
    url_GPT = f'https://us-central1-starcai.cloudfunctions.net/entry_pointGPT?apikey={gc_virtual_api_key}'
    # Making the POST request with JSON data
    response = requests.post(url_GPT, json={'text': original_text})
    # return rewritten text from the cloud function
    return response.text
