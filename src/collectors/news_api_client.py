import requests
import json
import sys
import os
from datetime import datetime

# Add the data directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))

# API configuration
API_KEY = "40ec095521524c0491150ef596d08401"
BASE_URL = "https://newsapi.org/v2/top-headlines"
COUNTRY = "us"  # Changed from "se" to "us"
CATEGORY = "business"  # Try changing this to "general" or "technology" if business returns no results

def fetch_news():
    """Fetch top headlines from the US"""
    # Construct the API URL
    url = f"{BASE_URL}?country={COUNTRY}&category={CATEGORY}&apiKey={API_KEY}"
    
    print(f"Requesting URL: {url}")
    
    response = None  # Initialize response variable
    
    try:
        # Make the API request
        response = requests.get(url)
        print(f"Response status code: {response.status_code}")
        
        # Print response headers for debugging
        print("Response headers:")
        for key, value in response.headers.items():
            if 'rate' in key.lower() or 'limit' in key.lower():
                print(f"  {key}: {value}")
        
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Get the JSON data
        data = response.json()
        
        # Log the response to a file in the data directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"news_response_{timestamp}.json"
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        filepath = os.path.join(data_dir, filename)
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Response saved to {filepath}")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        # Let's also save the error response if possible
        if response is not None:
            try:
                error_data = response.json()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"error_response_{timestamp}.json"
                data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
                filepath = os.path.join(data_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(error_data, f, indent=2, ensure_ascii=False)
                print(f"Error response saved to {filepath}")
            except:
                pass
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

if __name__ == "__main__":
    print(f"Fetching top {CATEGORY} headlines from {COUNTRY.upper()}...")
    news_data = fetch_news()
    
    if news_data:
        articles_count = len(news_data.get('articles', []))
        print(f"Successfully fetched {articles_count} articles")
        if articles_count == 0:
            print("Note: No articles were returned. This might be due to API limitations,")
            print("such as exceeding the daily request limit or the API key not being active.")
            print("Try changing the CATEGORY variable to 'general' or 'technology' in the script.")
        print("Check the JSON file for full details.")
    else:
        print("Failed to fetch news data.")