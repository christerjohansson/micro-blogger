import json
import sys
import os

# Add the data directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))

def inspect_latest_response():
    """Inspect the latest news response file"""
    try:
        # Define the data directory
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        
        # Get all JSON files in the directory
        json_files = [f for f in os.listdir(data_dir) if f.endswith('.json') and not f.startswith('error')]
        
        if not json_files:
            print("No JSON files found in the data directory.")
            return
        
        # Sort files by modification time (newest first)
        json_files.sort(key=lambda x: os.path.getmtime(os.path.join(data_dir, x)), reverse=True)
        
        latest_file = json_files[0]
        filepath = os.path.join(data_dir, latest_file)
        print(f"Latest file: {latest_file}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"Status: {data.get('status', 'N/A')}")
            print(f"Total Results: {data.get('totalResults', 'N/A')}")
            print(f"Articles Count: {len(data.get('articles', []))}")
            
            articles = data.get('articles', [])
            if articles:
                print(f"\nShowing first 3 articles:")
                for i, article in enumerate(articles[:3]):
                    print(f"\n--- Article {i+1} ---")
                    print(f"  Title: {article.get('title', 'N/A')}")
                    print(f"  Source: {article.get('source', {}).get('name', 'N/A')}")
                    print(f"  Author: {article.get('author', 'N/A')}")
                    print(f"  Published At: {article.get('publishedAt', 'N/A')}")
                    print(f"  Description: {article.get('description', 'N/A')[:100]}..." if article.get('description') else "  Description: N/A")
            else:
                print("\nNo articles found in the response.")
                
        except Exception as e:
            print(f"Error reading file: {e}")
            
    except Exception as e:
        print(f"Error accessing data directory: {e}")

if __name__ == "__main__":
    inspect_latest_response()