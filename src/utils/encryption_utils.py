#!/usr/bin/env python3
"""
Encryption utilities for securing the news.json file.
"""

import os
import json
import base64
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_encryption_key():
    """Get the encryption key from environment variables"""
    key = os.getenv('ENCRYPTION_KEY')
    if not key:
        # Generate a new key if none exists
        key = Fernet.generate_key().decode()
        print(f"Generated new encryption key: {key}")
        print("Please add this key to your .env file")
    else:
        # If the key is not 44 characters, we need to derive a proper Fernet key
        if len(key) != 44:
            # Use the key as a password to derive a proper Fernet key
            # Pad or truncate the key to 32 bytes and encode it
            key_bytes = key.encode()[:32].ljust(32, b'\0')
            key = base64.urlsafe_b64encode(key_bytes).decode()
    
    # Convert to bytes
    return key.encode()

def encrypt_file(file_path):
    """Encrypt a file using Fernet encryption"""
    try:
        # Get the encryption key
        key = get_encryption_key()
        fernet = Fernet(key)
        
        # Read the file
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        # Encrypt the data
        encrypted_data = fernet.encrypt(file_data)
        
        # Write the encrypted data back to the file
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
        
        print(f"Successfully encrypted {file_path}")
        return True
        
    except Exception as e:
        print(f"Error encrypting file: {e}")
        return False

def decrypt_file(file_path):
    """Decrypt a file using Fernet encryption"""
    try:
        # Get the encryption key
        key = get_encryption_key()
        fernet = Fernet(key)
        
        # Read the encrypted file
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        
        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Write the decrypted data back to the file
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)
        
        print(f"Successfully decrypted {file_path}")
        return True
        
    except Exception as e:
        print(f"Error decrypting file: {e}")
        return False

def encrypt_news_file():
    """Encrypt the news.json file"""
    try:
        # Define the data directory and file path
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        news_file = os.path.join(data_dir, 'news.json')
        
        if not os.path.exists(news_file):
            print("news.json file not found")
            return False
        
        return encrypt_file(news_file)
        
    except Exception as e:
        print(f"Error encrypting news file: {e}")
        return False

def decrypt_news_file():
    """Decrypt the news.json file"""
    try:
        # Define the data directory and file path
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        news_file = os.path.join(data_dir, 'news.json')
        
        if not os.path.exists(news_file):
            print("news.json file not found")
            return False
        
        return decrypt_file(news_file)
        
    except Exception as e:
        print(f"Error decrypting news file: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    print("Encryption Utilities")
    print("=" * 20)
    
    # Test encryption
    if encrypt_news_file():
        print("Encryption test successful")
    else:
        print("Encryption test failed")