# Micro AI Blogger - News Collection System

This project contains scripts to fetch news data from multiple sources and save the responses to JSON files. The system is organized into a clean directory structure for better maintainability.

## Project Structure

```
micro-ai-blogger/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── src/                    # Source code
│   ├── collectors/         # News collection scripts
│   │   ├── news_api_client.py
│   │   ├── sweden_rss_collector.py
│   │   └── run_all_collectors.py
│   └── utils/              # Utility scripts
│       ├── combine_news_data.py
│       ├── inspect_response.py
│       └── compare_sources.py
└── data/                   # Data storage
    └── news.json           # Final combined output (intermediate files are removed)
```

## Components

1. **News API Client** - Fetches business headlines from the US using the News API
2. **Sweden RSS Collector** - Collects news from Sweden via RSS feed
3. **Unified Runner** - Runs both collectors with a single command
4. **Data Combiner** - Combines data from both sources into a single JSON file

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Run Both Collectors and Combine Data (Recommended)
Run both collectors and combine the data with one command:
```
python main.py
```

### Individual Component Usage

#### News API Client Only
```
python src/collectors/news_api_client.py
```

#### Sweden RSS Collector Only
```
python src/collectors/sweden_rss_collector.py
```

#### Run All Collectors
```
python src/collectors/run_all_collectors.py
```

#### Combine Data Only
```
python src/utils/combine_news_data.py
```

#### Inspect Latest Response
```
python src/utils/inspect_response.py
```

#### Compare Sources
```
python src/utils/compare_sources.py
```

## Configuration

You can modify the following variables in the scripts to change the source of news:

In `src/collectors/news_api_client.py`:
- `COUNTRY`: The country code (e.g., "us", "gb", "ca")
- `CATEGORY`: The news category (e.g., "business", "general", "technology", "sports")

## Output Files

The final output is stored in the `data/` directory:
- `news.json`: Final combined data from both sources (this is the only file kept)

Intermediate files are automatically removed after processing:
- `news_response_*.json`: Temporary News API responses
- `sweden.json`: Temporary RSS feed data

## Notes

- The News API has different tiers of service. The free tier may have limitations on the number of requests per day.
- Different country codes may return different numbers of articles. For example, "us" returns more results than "se" (Sweden).
- If you're getting 0 articles in the News API response, try changing the country or category.
- The scripts include error handling and will save error responses to help with debugging.
- The final data file (`news.json`) is formatted for easy use in displaying data on screen.