#!/usr/bin/env python3
"""
Encryption utilities for securing the news.json file.
"""

import os
import json
import base64
import sys

def get_encryption_key():
    """Get the encryption key from environment variables or generate a default one"""
    # Try to get key from environment
    key = os.getenv('ENCRYPTION_KEY')
    if key:
        # If the key is already a valid 32-byte base64 encoded string, use it directly
        try:
            # Try to decode it to see if it's already a valid base64 key
            decoded = base64.urlsafe_b64decode(key)
            if len(decoded) == 32:
                # It's already a valid Fernet key
                return key.encode()
        except Exception:
            pass
        
        # If it's not a valid key, try to convert it
        try:
            # Use the key as a password to derive a proper Fernet key
            # Pad or truncate the key to 32 bytes and encode it
            key_bytes = key.encode()[:32].ljust(32, b'\0')
            key = base64.urlsafe_b64encode(key_bytes).decode()
        except Exception:
            # Use a default key if conversion fails
            key_bytes = b'default_key_for_micro_ai_blogger_32_bytes_long'
            key = base64.urlsafe_b64encode(key_bytes).decode()
    else:
        # Generate a proper Fernet key
        try:
            from cryptography.fernet import Fernet
            key = Fernet.generate_key().decode()
            print("Generated new encryption key: {}".format(key))
            print("Please add this key to your .env file as ENCRYPTION_KEY={}".format(key))
        except Exception:
            # Use a default key if generation fails
            key_bytes = b'default_key_for_micro_ai_blogger_32_bytes_long'
            key = base64.urlsafe_b64encode(key_bytes).decode()
    
    return key.encode()

def encrypt_file(file_path):
    """Encrypt a file using Fernet encryption"""
    try:
        # Try to import cryptography
        from cryptography.fernet import Fernet
    except ImportError:
        print("Encryption skipped: cryptography module not available.")
        return True
    
    try:
        # Get the encryption key
        key = get_encryption_key()
        # Ensure the key is properly formatted
        try:
            decoded_key = base64.urlsafe_b64decode(key)
            if len(decoded_key) != 32:
                raise ValueError("Key must be 32 bytes")
        except Exception:
            # If key is not valid, generate a new one
            key = Fernet.generate_key()
            print("Generated new valid encryption key")
        
        fernet = Fernet(key)
        
        # Read the file
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        # Encrypt the data
        encrypted_data = fernet.encrypt(file_data)
        
        # Write the encrypted data back to the file
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
        
        print("Successfully encrypted {}".format(file_path))
        return True
        
    except Exception as e:
        print("Error encrypting file: {}".format(e))
        return False

def decrypt_file(file_path):
    """Decrypt a file using Fernet encryption"""
    try:
        # Try to import cryptography
        from cryptography.fernet import Fernet
    except ImportError:
        print("Decryption skipped: cryptography module not available.")
        return True
    
    try:
        # Get the encryption key
        key = get_encryption_key()
        # Ensure the key is properly formatted
        try:
            decoded_key = base64.urlsafe_b64decode(key)
            if len(decoded_key) != 32:
                raise ValueError("Key must be 32 bytes")
        except Exception:
            print("Invalid encryption key format")
            return False
        
        fernet = Fernet(key)
        
        # Read the encrypted file
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        
        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Write the decrypted data back to the file
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)
        
        print("Successfully decrypted {}".format(file_path))
        return True
        
    except Exception as e:
        print("Error decrypting file: {}".format(e))
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
        print("Error encrypting news file: {}".format(e))
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
        print("Error decrypting news file: {}".format(e))
        return False

if __name__ == "__main__":
    # Example usage
    print("Encryption Utilities")
    print("=" * 20)
    
    # Test encryption
    if encrypt_news_file():
        print("Encryption test completed")
    else:
        print("Encryption test failed")