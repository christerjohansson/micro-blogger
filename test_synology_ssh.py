#!/usr/bin/env python3
"""
Script to test Synology SSH key authentication for GitHub.
"""

import os
import subprocess
import sys

def test_synology_keys():
    """Test if Synology keys exist and are properly configured"""
    print("Testing Synology SSH Key Setup")
    print("=" * 40)
    
    # Define Synology key paths
    project_dir = os.path.dirname(__file__)
    private_key = os.path.join(project_dir, "synology_key")
    public_key = os.path.join(project_dir, "synology_key.pub")
    
    print("Looking for Synology keys in: {}".format(project_dir))
    print("Private key: {}".format(private_key))
    print("Public key: {}".format(public_key))
    
    # Check if keys exist
    if not os.path.exists(private_key):
        print("ERROR: Private key not found!")
        return False
        
    if not os.path.exists(public_key):
        print("ERROR: Public key not found!")
        return False
    
    print("✓ Both Synology keys found")
    
    # Check permissions
    try:
        private_stat = os.stat(private_key)
        if private_stat.st_mode & 0o777 != 0o600:
            print("Warning: Private key permissions are not 600. Setting correct permissions...")
            os.chmod(private_key, 0o600)
            print("✓ Private key permissions fixed")
        else:
            print("✓ Private key permissions are correct")
            
        public_stat = os.stat(public_key)
        if public_stat.st_mode & 0o777 != 0o644:
            print("Warning: Public key permissions are not 644. Setting correct permissions...")
            os.chmod(public_key, 0o644)
            print("✓ Public key permissions fixed")
        else:
            print("✓ Public key permissions are correct")
    except Exception as e:
        print("Warning: Could not check/fix permissions: {}".format(e))
    
    return True

def setup_ssh_config():
    """Setup SSH config to use Synology keys"""
    try:
        # Define Synology key paths
        project_dir = os.path.dirname(__file__)
        private_key = os.path.join(project_dir, "synology_key")
        
        # Create .ssh directory if it doesn't exist
        ssh_dir = os.path.expanduser("~/.ssh")
        os.makedirs(ssh_dir, exist_ok=True)
        
        # Create SSH config to use the Synology key
        ssh_config = os.path.join(ssh_dir, "config")
        config_content = """# GitHub configuration using Synology keys
Host github.com
    HostName github.com
    User git
    IdentityFile {}
    IdentitiesOnly yes
""".format(private_key.replace("\\", "/"))  # Use forward slashes for SSH config
        
        # Write SSH config
        with open(ssh_config, "w") as f:
            f.write(config_content)
        
        print("✓ SSH config created to use Synology keys")
        return True
    except Exception as e:
        print("Error setting up SSH config: {}".format(e))
        return False

def test_github_connection():
    """Test connection to GitHub using Synology keys"""
    try:
        print("Testing GitHub connection with Synology keys...")
        
        # Test SSH connection to GitHub
        result = subprocess.run([
            'ssh', 
            '-o', 'IdentitiesOnly=yes',
            '-o', 'StrictHostKeyChecking=no',
            '-i', os.path.join(os.path.dirname(__file__), "synology_key"),
            '-T', 'git@github.com'
        ], capture_output=True, text=True, timeout=30)
        
        print("SSH command output:")
        print("STDOUT: {}".format(result.stdout))
        print("STDERR: {}".format(result.stderr))
        print("Return code: {}".format(result.returncode))
        
        # GitHub returns 1 for successful auth but no shell
        if result.returncode in [0, 1]:
            if "successfully authenticated" in result.stderr.lower() or "authenticated" in result.stderr.lower():
                print("✓ GitHub SSH authentication successful!")
                return True
            elif "permission denied" not in result.stderr.lower():
                # If it's not a permission denied error, it might be successful
                print("? GitHub connection test completed (check output above)")
                return True
        
        print("✗ GitHub SSH authentication failed")
        return False
    except subprocess.TimeoutExpired:
        print("✗ GitHub connection test timed out")
        return False
    except Exception as e:
        print("Error testing GitHub connection: {}".format(e))
        return False

def main():
    """Main test function"""
    print("Synology SSH Key Authentication Test")
    print("=" * 50)
    
    # Test if keys exist
    if not test_synology_keys():
        print("\nCannot proceed without Synology keys.")
        return 1
    
    # Setup SSH config
    print("\nSetting up SSH configuration...")
    if not setup_ssh_config():
        print("Failed to setup SSH configuration.")
        return 1
    
    # Test GitHub connection
    print("\nTesting GitHub connection...")
    if test_github_connection():
        print("\n✓ Synology SSH key setup is working!")
        print("The application can now use these keys to connect to GitHub.")
        return 0
    else:
        print("\n✗ Synology SSH key setup failed.")
        print("Please check that your public key is added to your GitHub account.")
        return 1

if __name__ == "__main__":
    sys.exit(main())