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
        result = run_all_collectors.main()
        
        # If collection was successful, commit and push changes
        if result == 0:
            print("\n" + "=" * 50)
            print("GIT OPERATIONS")
            print("=" * 50)
            
            # Import git utilities
            sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'utils'))
            from src.utils.git_utils import git_commit_and_push, convert_remote_to_ssh
            
            # Convert remote to SSH if needed
            convert_remote_to_ssh()
            
            # Commit and push changes
            if git_commit_and_push():
                print("Changes successfully committed and pushed to remote repository.")
            else:
                print("Failed to commit and push changes to remote repository.")
        else:
            print("Skipping git operations due to collection failure.")
            
        return result
    except Exception as e:
        print("Error running collectors: {}".format(e))
        return 1

if __name__ == "__main__":
    sys.exit(main())