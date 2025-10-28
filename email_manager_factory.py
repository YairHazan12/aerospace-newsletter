#!/usr/bin/env python3
"""
Email Manager Factory
Creates the appropriate email manager based on available configuration
"""

import os
import logging
from typing import Union

logger = logging.getLogger(__name__)

def create_email_manager() -> Union['EmailManager', 'FirebaseEmailManager']:
    """
    Factory function to create the appropriate email manager
    Returns Firebase manager if configured, otherwise JSON manager
    """
    # Check if Firebase credentials are available
    firebase_creds = [
        'FIREBASE_PROJECT_ID',
        'FIREBASE_CLIENT_EMAIL', 
        'FIREBASE_PRIVATE_KEY'
    ]
    
    has_firebase_creds = all(os.getenv(cred) for cred in firebase_creds)
    
    if has_firebase_creds:
        try:
            from firebase_manager import FirebaseEmailManager
            logger.info("Using Firebase Firestore for email management")
            return FirebaseEmailManager()
        except ImportError:
            logger.warning("Firebase credentials found but firebase-admin not installed. Falling back to JSON.")
        except Exception as e:
            logger.warning(f"Firebase initialization failed: {e}. Falling back to JSON.")
    
    # Fallback to JSON storage
    from email_manager import EmailManager
    logger.info("Using JSON file for email management")
    return EmailManager()

# For backward compatibility, export the factory as the main interface
def get_email_manager():
    """Get the appropriate email manager instance"""
    return create_email_manager()

if __name__ == "__main__":
    # Test the factory
    print("🧪 Testing Email Manager Factory...")
    
    manager = create_email_manager()
    print(f"Manager type: {type(manager).__name__}")
    
    # Test basic functionality
    stats = manager.get_stats()
    print(f"Stats: {stats}")
    
    # Test subscription
    result = manager.subscribe("factory-test@example.com", "Factory Test")
    print(f"Subscribe result: {result}")
    
    # Clean up test
    manager.unsubscribe("factory-test@example.com")
    print("Test completed")
