# Micro AI Blogger - News Collection System

This project contains scripts to fetch news data from multiple sources and save the responses to JSON files. The system is organized into a clean directory structure for better maintainability.

## Project Structure

```
micro-ai-blogger/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (encryption key)
├── .gitignore              # Git ignore file
├── README.md               # This file
├── src/                    # Source code
│   ├── collectors/         # News collection scripts
│   │   ├── news_api_client.py
│   │   ├── sweden_rss_collector.py
│   │   └── run_all_collectors.py
│   └── utils/              # Utility scripts
│       ├── combine_news_data.py
│       ├── encryption_utils.py
│       ├── git_utils.py
│       ├── inspect_response.py
│       └── compare_sources.py
└── data/                   # Data storage
    └── news.json           # Final encrypted output (intermediate files are removed)
```

## Components

1. **News API Client** - Fetches business headlines from the US using the News API
2. **Sweden RSS Collector** - Collects news from Sweden via RSS feed
3. **Unified Runner** - Runs both collectors with a single command
4. **Data Combiner** - Combines data from both sources into a single JSON file
5. **Encryption Utilities** - Encrypts the final data file for security
6. **Git Utilities** - Automatically commits and pushes changes to remote repository

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Initialize git repository (if not already done):
   ```
   git init
   git remote add origin <your-github-repo-url>
   ```

3. Set up git user configuration:
   ```
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

## Usage

### Run Both Collectors and Combine Data (Recommended)
Run both collectors and combine the data with one command:
```
python main.py
```

This will:
1. Collect data from both news sources
2. Combine and encrypt the data
3. Automatically commit and push changes to the remote repository

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

#### Encrypt/Decrypt News File
```
python src/utils/encryption_utils.py
```

#### Git Operations
```
python src/utils/git_utils.py
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

## Security

The final output file (`news.json`) is encrypted using the Fernet encryption scheme for security. The encryption key is stored in the `.env` file. Make sure to keep this file secure and never commit it to version control systems.

To decrypt the file for viewing, you would need to use the decryption utilities provided in `src/utils/encryption_utils.py`.

## Output Files

The final output is stored in the `data/` directory:
- `news.json`: Final encrypted combined data from both sources (this is the only file kept)

Intermediate files are automatically removed after processing:
- `news_response_*.json`: Temporary News API responses
- `sweden.json`: Temporary RSS feed data

## Git Integration

The system automatically commits and pushes changes to the remote repository after successful data collection. This is useful for:
- Tracking changes over time
- Using with CRON jobs for automated updates
- Deploying to servers with SSH key authentication

To use with a CRON job and SSH key:
1. Set up SSH key authentication with your GitHub account
2. Configure the git remote to use SSH instead of HTTPS
3. Set up the CRON job to run `python main.py` at desired intervals

## Notes

- The News API has different tiers of service. The free tier may have limitations on the number of requests per day.
- Different country codes may return different numbers of articles. For example, "us" returns more results than "se" (Sweden).
- If you're getting 0 articles in the News API response, try changing the country or category.
- The scripts include error handling and will save error responses to help with debugging.
- The final encrypted data file (`news.json`) is formatted for easy use in displaying data on screen (after decryption).
- Git operations will only run if the data collection is successful.