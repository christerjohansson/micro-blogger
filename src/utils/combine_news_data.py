#!/usr/bin/env python3
"""
Script to combine news data from both sources into a single JSON file.
This script reads data from the latest News API response and the Sweden RSS feed,
then combines them into one unified JSON file for later use.
"""

import json
import os
import glob
import sys
from datetime import datetime

# Add the data directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))

def get_latest_news_api_file():
    """Get the latest News API response file"""
    try:
        # Define the data directory
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        
        # Find all news response files
        pattern = os.path.join(data_dir, "news_response_*.json")
        news_files = glob.glob(pattern)
        if not news_files:
            print("No News API response files found.")
            return None
            
        # Sort by modification time and get the latest
        news_files.sort(key=os.path.getmtime, reverse=True)
        latest_file = news_files[0]
        print(f"Using latest News API file: {os.path.basename(latest_file)}")
        return latest_file
    except Exception as e:
        print(f"Error finding latest News API file: {e}")
        return None

def load_news_api_data():
    """Load data from the latest News API response"""
    try:
        latest_file = get_latest_news_api_file()
        if not latest_file:
            return None
            
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add source information
        for article in data.get('articles', []):
            article['source_type'] = 'news_api'
            article['source_name'] = 'News API'
            
        print(f"Loaded {len(data.get('articles', []))} articles from News API")
        return data
    except Exception as e:
        print(f"Error loading News API data: {e}")
        return None

def load_rss_data():
    """Load data from the Sweden RSS feed"""
    try:
        # Define the data directory and file path
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        rss_file = os.path.join(data_dir, 'sweden.json')
        
        with open(rss_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert RSS format to match News API format
        articles = []
        for item in data.get('articles', []):
            article = {
                'source': {'name': data.get('title', 'Barometern')},
                'author': None,
                'title': item.get('title', ''),
                'description': item.get('description', ''),
                'url': item.get('link', ''),
                'urlToImage': None,
                'publishedAt': item.get('pubDate', ''),
                'content': item.get('content', ''),
                'source_type': 'rss',
                'source_name': 'Sweden RSS'
            }
            articles.append(article)
        
        # Create a compatible structure
        rss_data = {
            'status': 'ok',
            'totalResults': len(articles),
            'articles': articles
        }
        
        print(f"Loaded {len(articles)} articles from RSS feed")
        return rss_data
    except Exception as e:
        print(f"Error loading RSS data: {e}")
        return None

def combine_news_data():
    """Combine data from both sources into a single JSON file"""
    print("Combining news data from both sources...")
    
    # Load data from both sources
    news_api_data = load_news_api_data()
    rss_data = load_rss_data()
    
    if not news_api_data and not rss_data:
        print("No data available from either source.")
        return False
    
    # Combine articles
    combined_articles = []
    
    if news_api_data and 'articles' in news_api_data:
        combined_articles.extend(news_api_data['articles'])
    
    if rss_data and 'articles' in rss_data:
        combined_articles.extend(rss_data['articles'])
    
    # Create combined data structure
    combined_data = {
        'combined_at': datetime.now().isoformat(),
        'total_articles': len(combined_articles),
        'sources': {
            'news_api_count': len(news_api_data.get('articles', [])) if news_api_data else 0,
            'rss_count': len(rss_data.get('articles', [])) if rss_data else 0
        },
        'articles': combined_articles
    }
    
    # Save to combined file in the data directory
    try:
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        filepath = os.path.join(data_dir, 'combined_news.json')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully saved {len(combined_articles)} articles to {filepath}")
        return True
    except Exception as e:
        print(f"Error saving combined data: {e}")
        return False

def cleanup_intermediate_files():
    """Remove intermediate files (sweden.json and news_response_*.json)"""
    try:
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        
        # Remove sweden.json
        sweden_file = os.path.join(data_dir, 'sweden.json')
        if os.path.exists(sweden_file):
            os.remove(sweden_file)
            print("Removed sweden.json")
        
        # Remove all news_response_*.json files
        pattern = os.path.join(data_dir, "news_response_*.json")
        news_files = glob.glob(pattern)
        for file in news_files:
            os.remove(file)
            print(f"Removed {os.path.basename(file)}")
            
        return True
    except Exception as e:
        print(f"Error during cleanup: {e}")
        return False

def rename_combined_file():
    """Rename combined_news.json to news.json"""
    try:
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        combined_file = os.path.join(data_dir, 'combined_news.json')
        news_file = os.path.join(data_dir, 'news.json')
        
        if os.path.exists(combined_file):
            # Remove the target file if it already exists
            if os.path.exists(news_file):
                os.remove(news_file)
            os.rename(combined_file, news_file)
            print("Renamed combined_news.json to news.json")
            return True
        else:
            print("combined_news.json not found")
            return False
    except Exception as e:
        print(f"Error renaming file: {e}")
        return False

def encrypt_news_file():
    """Encrypt the news.json file"""
    try:
        # Import encryption utilities
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from utils.encryption_utils import encrypt_news_file
        
        # Encrypt the file
        if encrypt_news_file():
            print("Encrypted news.json file")
            return True
        else:
            print("Failed to encrypt news.json file")
            return False
    except Exception as e:
        print(f"Error encrypting news file: {e}")
        return False

def display_summary():
    """Display a summary of the combined data"""
    try:
        # Define the data directory and file path
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        filepath = os.path.join(data_dir, 'news.json')  # Updated to news.json
        
        # Note: In a real implementation, we would decrypt the file before reading it
        # For now, we'll just show a message that the file is encrypted
        print("\n" + "=" * 50)
        print("COMBINED NEWS DATA SUMMARY")
        print("=" * 50)
        print("The news.json file has been encrypted for security.")
        print("To view the data, you would need to decrypt it first.")
        
        # In a real implementation, we would decrypt and then read the file
        # For now, we'll just show generic information
        print(f"Combined at: {datetime.now().isoformat()}")
        print("Total articles: Data encrypted - cannot display count")
        print("News API articles: Data encrypted - cannot display count")
        print("RSS articles: Data encrypted - cannot display count")
        
        return True
    except Exception as e:
        print(f"Error displaying summary: {e}")
        return False

def main():
    """Main function to combine news data"""
    print("Starting news data combination process...")
    
    # Combine the data
    success = combine_news_data()
    
    if success:
        # Cleanup intermediate files
        cleanup_success = cleanup_intermediate_files()
        
        # Rename combined file to news.json
        rename_success = rename_combined_file()
        
        # Encrypt the news.json file
        encrypt_success = encrypt_news_file()
        
        if cleanup_success and rename_success and encrypt_success:
            # Display summary
            display_summary()
            data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
            filepath = os.path.join(data_dir, 'news.json')
            print(f"\nFinal encrypted data has been saved to {filepath}")
            print("Intermediate files have been removed.")
            print("This file can now be used to display data on screen (after decryption).")
        else:
            print("Failed to complete cleanup, rename, or encryption process.")
            return 1
    else:
        print("Failed to combine news data.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())