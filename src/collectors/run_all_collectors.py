#!/usr/bin/env python3
"""
Unified script to run all news collectors.
This script runs both the News API client and the Sweden RSS collector.
"""

import sys
import os
import json

# Add the utils directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

def run_news_api_collector():
    """Run the News API collector script"""
    print("=" * 50)
    print("Running News API Collector...")
    print("=" * 50)
    
    try:
        # Import and run the news API collector
        from .news_api_client import fetch_news, CATEGORY, COUNTRY
        
        print(f"Fetching top {CATEGORY} headlines from {COUNTRY.upper()}...")
        news_data = fetch_news()
        
        if news_data:
            articles_count = len(news_data.get('articles', []))
            print(f"Successfully fetched {articles_count} articles")
            if articles_count == 0:
                print("Note: No articles were returned. This might be due to API limitations,")
                print("such as exceeding the daily request limit or the API key not being active.")
            print("Check the JSON file for full details.")
        else:
            print("Failed to fetch news data from News API.")
            
    except Exception as e:
        print(f"Error running News API collector: {e}")
        return False
    
    return True

def run_rss_collector():
    """Run the Sweden RSS collector script"""
    print("\n" + "=" * 50)
    print("Running Sweden RSS Collector...")
    print("=" * 50)
    
    try:
        # Import and run the RSS collector
        from .sweden_rss_collector import fetch_rss_feed, display_summary
        
        print("Collecting RSS feed data from Sweden...")
        data = fetch_rss_feed()
        
        if data:
            display_summary(data)
            print("\nData saved to sweden.json")
        else:
            print("Failed to collect RSS feed data.")
            
    except Exception as e:
        print(f"Error running RSS collector: {e}")
        return False
    
    return True

def combine_data():
    """Combine data from both sources into a single JSON file"""
    print("\n" + "=" * 50)
    print("Combining Data from Both Sources...")
    print("=" * 50)
    
    try:
        # Import the combination function
        from ..utils.combine_news_data import combine_news_data, display_summary
        
        # Run the combination process
        success = combine_news_data()
        
        if success:
            # Display summary
            print(f"\nData has been saved to combined_news.json")
            print("This file can now be used to display data on screen.")
        else:
            print("Failed to combine data.")
            
        return success
        
    except Exception as e:
        print(f"Error combining data: {e}")
        return False

def main():
    """Main function to run all collectors"""
    print("Starting all news collectors...")
    
    # Run News API collector
    news_api_success = run_news_api_collector()
    
    # Run RSS collector
    rss_success = run_rss_collector()
    
    # Combine data
    combine_success = combine_data()
    
    # Summary
    print("\n" + "=" * 50)
    print("COLLECTION SUMMARY")
    print("=" * 50)
    print(f"News API Collector: {'SUCCESS' if news_api_success else 'FAILED'}")
    print(f"RSS Collector: {'SUCCESS' if rss_success else 'FAILED'}")
    print(f"Data Combination: {'SUCCESS' if combine_success else 'FAILED'}")
    
    if news_api_success and rss_success and combine_success:
        print("\nAll processes completed successfully!")
        print("Combined data is available in data/combined_news.json")
    else:
        print("\nSome processes failed. Check the output above for details.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())