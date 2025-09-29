import json
import os

# Add the data directory to the path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))

def compare_sources():
    """Compare data from News API and RSS feed"""
    print("Comparing news sources...")
    
    # Define the data directory
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
    
    # Load News API data (latest file)
    news_files = []
    try:
        news_files = [f for f in os.listdir(data_dir) if f.startswith('news_response_') and f.endswith('.json')]
        if news_files:
            # Sort by modification time and get the latest
            news_files.sort(key=lambda x: os.path.getmtime(os.path.join(data_dir, x)), reverse=True)
            latest_news_file = news_files[0]
            filepath = os.path.join(data_dir, latest_news_file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                news_data = json.load(f)
            print(f"Loaded News API data from: {latest_news_file}")
        else:
            news_data = {"articles": []}
            print("No News API data found")
    except Exception as e:
        print(f"Error loading News API data: {e}")
        news_data = {"articles": []}
    
    # Load RSS feed data
    try:
        rss_filepath = os.path.join(data_dir, 'sweden.json')
        with open(rss_filepath, 'r', encoding='utf-8') as f:
            rss_data = json.load(f)
        print("Loaded RSS feed data from: sweden.json")
    except Exception as e:
        print(f"Error loading RSS data: {e}")
        rss_data = {"articles": []}
    
    # Display comparison
    print("\n--- COMPARISON ---")
    print(f"News API (US business): {len(news_data.get('articles', []))} articles")
    print(f"RSS Feed (Sweden): {len(rss_data.get('articles', []))} articles")
    
    # Show sample titles
    if news_data.get('articles'):
        print(f"\nSample News API titles:")
        for i, article in enumerate(news_data['articles'][:3]):
            print(f"  {i+1}. {article.get('title', 'N/A')[:60]}...")
    
    if rss_data.get('articles'):
        print(f"\nSample RSS titles:")
        for i, article in enumerate(rss_data['articles'][:3]):
            print(f"  {i+1}. {article.get('title', 'N/A')[:60]}...")

if __name__ == "__main__":
    compare_sources()