#!/usr/bin/env python3
"""
Git utilities for committing and pushing changes to remote repository.
"""

import os
import subprocess
import sys
from datetime import datetime

def is_git_repository():
    """Check if the current directory is a git repository"""
    try:
        result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        return result.returncode == 0
    except Exception:
        return False

def get_current_branch():
    """Get the current git branch name"""
    try:
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception:
        return None

def git_commit_and_push(commit_message=None):
    """Commit and push changes to remote repository"""
    try:
        # Check if this is a git repository
        if not is_git_repository():
            print("Not a git repository. Initializing...")
            subprocess.run(['git', 'init'], check=True)
            
            # Add remote origin (user will need to set this up)
            print("Please set up your remote repository with:")
            print("  git remote add origin <your-github-repo-url>")
            return False
        
        # Get current timestamp for commit message if none provided
        if not commit_message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Automated commit: News data update - {timestamp}"
        
        # Add all changes
        print("Adding changes to git...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Check if there are changes to commit
        result = subprocess.run(['git', 'diff', '--cached', '--quiet'], capture_output=True)
        if result.returncode == 0:
            print("No changes to commit.")
            return True
        
        # Commit changes
        print(f"Committing changes with message: {commit_message}")
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Get current branch
        branch = get_current_branch()
        if not branch:
            print("Could not determine current branch.")
            return False
        
        # Push changes to remote origin
        print(f"Pushing changes to remote repository on branch '{branch}'...")
        push_result = subprocess.run(['git', 'push', 'origin', branch], capture_output=True, text=True)
        
        if push_result.returncode != 0:
            # Check if we need to set upstream
            if "set-upstream" in push_result.stderr:
                print("Setting upstream branch...")
                push_result = subprocess.run(['git', 'push', '--set-upstream', 'origin', branch], 
                                           capture_output=True, text=True)
            
            if push_result.returncode != 0:
                print(f"Error pushing changes: {push_result.stderr}")
                return False
        
        print("Successfully committed and pushed changes to remote repository.")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error during git operation: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def setup_git_config(name, email):
    """Setup git user configuration"""
    try:
        subprocess.run(['git', 'config', '--global', 'user.name', name], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', email], check=True)
        print(f"Git configuration set for {name} <{email}>")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error setting git configuration: {e}")
        return False

def check_git_status():
    """Check git repository status"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            if result.stdout.strip():
                print("Modified files:")
                print(result.stdout)
                return True
            else:
                print("No changes in the repository.")
                return False
        else:
            print("Not a git repository or error occurred.")
            return False
    except Exception as e:
        print(f"Error checking git status: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    print("Git Utilities")
    print("=" * 20)
    
    # Check if this is a git repository
    if is_git_repository():
        print("Git repository detected.")
        
        # Check status
        has_changes = check_git_status()
        
        if has_changes:
            # Try to commit and push
            if git_commit_and_push():
                print("Git operations completed successfully.")
            else:
                print("Git operations failed.")
        else:
            print("No changes to commit.")
    else:
        print("Not a git repository.")