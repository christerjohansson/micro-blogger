import requests
import json
import sys
import os
from datetime import datetime
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

# Add the data directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))

# RSS feed URL for Sweden
RSS_URL = "https://www.barometern.se/feed"

def fetch_rss_feed():
    """Fetch and parse RSS feed from Sweden"""
    try:
        # Fetch the RSS feed
        print(f"Fetching RSS feed from: {RSS_URL}")
        response = requests.get(RSS_URL)
        response.raise_for_status()
        
        # Parse the XML
        root = ET.fromstring(response.content)
        
        # Extract feed metadata
        feed_data = {
            'title': '',
            'description': '',
            'link': '',
            'updated': datetime.now().isoformat(),
            'articles': []
        }
        
        # Get channel information
        channel = root.find('channel')
        if channel is not None:
            feed_data['title'] = channel.findtext('title', '')
            feed_data['description'] = channel.findtext('description', '')
            feed_data['link'] = channel.findtext('link', '')
            
            # Get all items (articles)
            items = channel.findall('item')
            for item in items:
                article = {
                    'title': item.findtext('title', ''),
                    'link': item.findtext('link', ''),
                    'description': item.findtext('description', ''),
                    'pubDate': item.findtext('pubDate', ''),
                    'guid': item.findtext('guid', '')
                }
                
                # Handle namespaces if present
                for elem in item:
                    if elem.tag.endswith('encoded'):
                        article['content'] = elem.text or ''
                
                feed_data['articles'].append(article)
        
        # Save to sweden.json in the data directory
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        filepath = os.path.join(data_dir, 'sweden.json')
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(feed_data, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully saved {len(feed_data['articles'])} articles to {filepath}")
        return feed_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed: {e}")
        return None
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def display_summary(feed_data):
    """Display a summary of the fetched data"""
    if not feed_data:
        return
        
    print(f"\nFeed Title: {feed_data.get('title', 'N/A')}")
    print(f"Description: {feed_data.get('description', 'N/A')}")
    print(f"Articles Count: {len(feed_data.get('articles', []))}")
    
    articles = feed_data.get('articles', [])
    if articles:
        print("\nFirst 3 articles:")
        for i, article in enumerate(articles[:3]):
            print(f"\n--- Article {i+1} ---")
            print(f"  Title: {article.get('title', 'N/A')}")
            print(f"  Published: {article.get('pubDate', 'N/A')}")

if __name__ == "__main__":
    print("Collecting RSS feed data from Sweden...")
    data = fetch_rss_feed()
    
    if data:
        display_summary(data)
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        filepath = os.path.join(data_dir, 'sweden.json')
        print(f"\nData saved to {filepath}")
    else:
        print("Failed to collect RSS feed data.")