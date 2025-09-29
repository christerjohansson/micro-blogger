#!/usr/bin/env python3
"""
Script to install dependencies for the Micro AI Blogger project.
This script will attempt to install the required packages using pip.
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("Successfully installed {}".format(package))
        return True
    except subprocess.CalledProcessError as e:
        print("Failed to install {}: {}".format(package, e))
        return False
    except Exception as e:
        print("Unexpected error installing {}: {}".format(package, e))
        return False

def main():
    """Main function to install all required dependencies"""
    print("Installing dependencies for Micro AI Blogger...")
    print("=" * 50)
    
    # Read requirements from requirements.txt
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read().strip().split("\n")
    except Exception as e:
        print("Error reading requirements.txt: {}".format(e))
        return 1
    
    # Install each package
    failed_packages = []
    for package in requirements:
        if package.strip():  # Skip empty lines
            print("Installing {}...".format(package))
            if not install_package(package):
                failed_packages.append(package)
    
    # Summary
    print("\n" + "=" * 50)
    if failed_packages:
        print("Failed to install the following packages:")
        for package in failed_packages:
            print("  - {}".format(package))
        print("\nPlease install these packages manually.")
        return 1
    else:
        print("All dependencies installed successfully!")
        return 0

if __name__ == "__main__":
    sys.exit(main())