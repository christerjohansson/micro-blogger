#!/usr/bin/env python3
"""
Script to setup SSH authentication for GitHub on Synology.
This script helps configure SSH keys for GitHub access.
"""

import os
import subprocess
import sys
import platform

def check_ssh_keys():
    """Check if SSH keys exist"""
    print("Checking for SSH keys...")
    
    # Check common locations based on OS
    if platform.system() == "Windows":
        locations = [
            os.path.expanduser("~/.ssh/id_rsa"),
            os.path.expanduser("~/.ssh/id_ed25519"),
            # Git for Windows default location
            os.path.join(os.environ.get('USERPROFILE', ''), '.ssh', 'id_rsa'),
            os.path.join(os.environ.get('USERPROFILE', ''), '.ssh', 'id_ed25519')
        ]
    else:
        # Unix-like systems (including Synology)
        locations = [
            os.path.expanduser("~/.ssh/id_rsa"),
            os.path.expanduser("~/.ssh/id_ed25519"),
            "/root/.ssh/id_rsa",
            "/root/.ssh/id_ed25519"
        ]
    
    found_keys = []
    for location in locations:
        if os.path.exists(location):
            found_keys.append(location)
            print("  Found: {}".format(location))
        else:
            print("  Not found: {}".format(location))
    
    return found_keys

def setup_ssh_agent():
    """Setup SSH agent"""
    try:
        if platform.system() == "Windows":
            # On Windows, we'll skip agent setup as it's more complex
            print("On Windows, SSH agent setup is skipped. Make sure your key has no passphrase or use ssh-agent manually.")
            return True
        else:
            # Start ssh-agent if not running
            subprocess.run(['eval', '$(ssh-agent -s)'], shell=True, check=True)
            print("SSH agent started successfully.")
            return True
    except Exception as e:
        print("Error starting SSH agent: {}".format(e))
        print("Continuing without agent setup...")
        return False

def add_ssh_key_to_agent(key_path):
    """Add SSH key to agent"""
    try:
        if platform.system() == "Windows":
            # On Windows, we'll skip adding to agent
            print("On Windows, skipping adding key to agent. Make sure your key has no passphrase.")
            return True
        else:
            subprocess.run(['ssh-add', key_path], check=True)
            print("Added SSH key to agent: {}".format(key_path))
            return True
    except Exception as e:
        print("Error adding SSH key to agent: {}".format(e))
        return False

def test_github_connection():
    """Test connection to GitHub"""
    try:
        # Use a shorter timeout and suppress host key checking for testing
        result = subprocess.run(['ssh', '-o', 'ConnectTimeout=10', '-o', 'StrictHostKeyChecking=no', '-T', 'git@github.com'], 
                              capture_output=True, text=True)
        
        # GitHub returns 1 for successful auth but no shell
        if result.returncode in [0, 1]:
            if "successfully authenticated" in result.stderr or "authenticated" in result.stderr:
                print("GitHub SSH authentication successful!")
                return True
            elif "PTY allocation request failed" in result.stderr:
                print("GitHub SSH authentication successful! (PTY allocation failed is normal)")
                return True
            elif "permission denied" not in result.stderr.lower():
                # If it's not a permission denied error, it might be successful
                print("GitHub connection test output: {}".format(result.stderr.strip()))
                return True
        
        print("GitHub SSH test output: {}".format(result.stderr.strip()))
        return "successfully authenticated" in result.stderr.lower()
    except Exception as e:
        print("Error testing GitHub connection: {}".format(e))
        return False

def setup_known_hosts():
    """Setup GitHub in known_hosts"""
    try:
        ssh_dir = os.path.expanduser("~/.ssh")
        known_hosts = os.path.join(ssh_dir, "known_hosts")
        
        # Create .ssh directory if it doesn't exist
        os.makedirs(ssh_dir, exist_ok=True)
        
        # Check if GitHub is already in known_hosts
        if os.path.exists(known_hosts):
            with open(known_hosts, 'r') as f:
                content = f.read()
                if 'github.com' in content:
                    print("GitHub already in known_hosts")
                    return True
        
        # Add GitHub's SSH key to known_hosts
        result = subprocess.run(['ssh-keyscan', 'github.com'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            with open(known_hosts, 'a') as f:
                f.write(result.stdout)
            print("Added GitHub to known_hosts")
            return True
        else:
            print("Failed to scan GitHub SSH keys: {}".format(result.stderr))
            return False
    except Exception as e:
        print("Error setting up known_hosts: {}".format(e))
        return False

def check_git_remote():
    """Check current git remote URL"""
    try:
        result = subprocess.run(['git', 'remote', '-v'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("Current git remotes:")
            print(result.stdout)
            return True
        else:
            print("No git remotes configured or not a git repository")
            return False
    except Exception as e:
        print("Error checking git remotes: {}".format(e))
        return False

def main():
    """Main setup function"""
    print("GitHub SSH Authentication Setup")
    print("=" * 40)
    
    # Check current git remote
    print("\nChecking current git remote...")
    check_git_remote()
    
    # Check for existing SSH keys
    keys = check_ssh_keys()
    
    if not keys:
        print("\nNo SSH keys found. You need to generate SSH keys first.")
        print("On Unix/Linux/Synology, run:")
        print("  ssh-keygen -t ed25519 -C \"your_email@example.com\"")
        print("\nOn Windows with Git Bash:")
        print("  ssh-keygen -t ed25519 -C \"your_email@example.com\"")
        return 1
    
    # Setup known hosts
    print("\nSetting up known hosts...")
    setup_known_hosts()
    
    # Setup SSH agent (if not Windows)
    if platform.system() != "Windows":
        print("\nSetting up SSH agent...")
        setup_ssh_agent()
        
        # Add keys to agent
        print("\nAdding SSH keys to agent...")
        for key in keys:
            add_ssh_key_to_agent(key)
    
    # Test GitHub connection
    print("\nTesting GitHub connection...")
    if test_github_connection():
        print("\nGitHub SSH authentication is ready!")
        print("You can now use SSH to connect to GitHub.")
        print("\nIf you're using HTTPS remote URLs, convert them to SSH:")
        print("  python src/utils/git_utils.py")
        return 0
    else:
        print("\nGitHub SSH authentication test failed.")
        print("Please check your SSH keys and try again.")
        print("\nMake sure:")
        print("1. Your public key is added to your GitHub account")
        print("2. Your private key has correct permissions (600)")
        print("3. Your private key has no passphrase (or ssh-agent is running)")
        return 1

if __name__ == "__main__":
    sys.exit(main())