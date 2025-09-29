#!/usr/bin/env python3
"""
Main entry point for the Micro AI Blogger news collection system.
This script provides a unified interface to run all news collectors and data processing functions.
"""

import sys
import os

def main():
    """Main function to run the news collection system"""
    print("Micro AI Blogger - News Collection System")
    print("=" * 50)
    
    # Add the src directory to the path so we can import modules
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.insert(0, src_path)
    
    # Import and run the main collector
    try:
        from src.collectors import run_all_collectors
        return run_all_collectors.main()
    except Exception as e:
        print(f"Error running collectors: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())