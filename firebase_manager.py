#!/usr/bin/env python3
"""
Firebase Firestore Email Management System for Aerospace Newsletter
Handles email collection, storage, and management using Firebase Firestore
"""

import os
import re
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    logger.warning("Firebase Admin SDK not available. Install with: pip install firebase-admin")

class FirebaseEmailManager:
    """Manages newsletter email subscriptions using Firebase Firestore"""
    
    def __init__(self, collection_name: str = "newsletter_subscribers"):
        self.collection_name = collection_name
        self.db = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        if not FIREBASE_AVAILABLE:
            logger.error("Firebase Admin SDK not available")
            return False
        
        try:
            # Check if Firebase is already initialized
            if firebase_admin._apps:
                self.db = firestore.client()
                logger.info("Using existing Firebase app")
                return True
            
            # Initialize Firebase with environment variables
            project_id = os.getenv('FIREBASE_PROJECT_ID')
            client_email = os.getenv('FIREBASE_CLIENT_EMAIL')
            private_key = os.getenv('FIREBASE_PRIVATE_KEY')
            database_url = os.getenv('FIREBASE_DATABASE_URL')
            
            if not all([project_id, client_email, private_key]):
                logger.warning("Firebase credentials not found in environment variables")
                return False
            
            # Replace escaped newlines in private key
            if private_key:
                private_key = private_key.replace('\\n', '\n')
            
            # Create credentials
            cred_dict = {
                "type": "service_account",
                "project_id": project_id,
                "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID', ''),
                "private_key": private_key,
                "client_email": client_email,
                "client_id": os.getenv('FIREBASE_CLIENT_ID', ''),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{client_email}"
            }
            
            cred = credentials.Certificate(cred_dict)
            
            # Initialize Firebase Admin
            firebase_admin.initialize_app(cred, {
                'databaseURL': database_url
            })
            
            self.db = firestore.client()
            logger.info("Firebase initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            return False
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _generate_unsubscribe_token(self, email: str) -> str:
        """Generate a unique unsubscribe token for an email"""
        import hashlib
        import secrets
        
        # Create a unique token based on email and timestamp
        salt = secrets.token_hex(16)
        token_data = f"{email}{datetime.now().isoformat()}{salt}"
        token = hashlib.sha256(token_data.encode()).hexdigest()[:32]
        return token
    
    def subscribe(self, email: str, name: str = None) -> Dict:
        """Subscribe a new email to the newsletter"""
        if not self.db:
            return {
                'success': False,
                'message': 'Firebase not initialized',
                'email': email
            }
        
        email = email.strip().lower()
        
        # Validate email
        if not self._validate_email(email):
            return {
                'success': False,
                'message': 'Invalid email format',
                'email': email
            }
        
        try:
            # Check if already subscribed
            doc_ref = self.db.collection(self.collection_name).document(email)
            doc = doc_ref.get()
            
            if doc.exists and doc.to_dict().get('active', False):
                return {
                    'success': False,
                    'message': 'Email already subscribed',
                    'email': email
                }
            
            # Add new subscriber
            subscriber_data = {
                'email': email,
                'name': name.strip() if name else None,
                'subscribed_at': datetime.now().isoformat(),
                'active': True,
                'unsubscribe_token': self._generate_unsubscribe_token(email)
            }
            
            doc_ref.set(subscriber_data)
            logger.info(f"New subscriber added to Firestore: {email}")
            
            return {
                'success': True,
                'message': 'Successfully subscribed to newsletter',
                'email': email,
                'subscriber': subscriber_data
            }
            
        except Exception as e:
            logger.error(f"Error subscribing {email}: {e}")
            return {
                'success': False,
                'message': f'Failed to save subscription: {str(e)}',
                'email': email
            }
    
    def unsubscribe(self, email: str = None, token: str = None) -> Dict:
        """Unsubscribe an email from the newsletter"""
        if not self.db:
            return {
                'success': False,
                'message': 'Firebase not initialized'
            }
        
        if not email and not token:
            return {
                'success': False,
                'message': 'Email or unsubscribe token required'
            }
        
        try:
            # Find subscriber
            if email:
                email = email.strip().lower()
                doc_ref = self.db.collection(self.collection_name).document(email)
                doc = doc_ref.get()
                
                if not doc.exists:
                    return {
                        'success': False,
                        'message': 'Email not found in subscribers'
                    }
                
                # Mark as unsubscribed
                doc_ref.update({
                    'active': False,
                    'unsubscribed_at': datetime.now().isoformat()
                })
                
                logger.info(f"Subscriber unsubscribed in Firestore: {email}")
                return {
                    'success': True,
                    'message': 'Successfully unsubscribed from newsletter',
                    'email': email
                }
            
            elif token:
                # Find by token
                subscribers = self.db.collection(self.collection_name).where('unsubscribe_token', '==', token).get()
                
                if not subscribers:
                    return {
                        'success': False,
                        'message': 'Unsubscribe token not found'
                    }
                
                for doc in subscribers:
                    doc.reference.update({
                        'active': False,
                        'unsubscribed_at': datetime.now().isoformat()
                    })
                    logger.info(f"Subscriber unsubscribed via token: {doc.id}")
                    return {
                        'success': True,
                        'message': 'Successfully unsubscribed from newsletter',
                        'email': doc.id
                    }
            
        except Exception as e:
            logger.error(f"Error unsubscribing: {e}")
            return {
                'success': False,
                'message': f'Failed to unsubscribe: {str(e)}'
            }
    
    def is_subscribed(self, email: str) -> bool:
        """Check if email is subscribed and active"""
        if not self.db:
            return False
        
        try:
            email = email.strip().lower()
            doc_ref = self.db.collection(self.collection_name).document(email)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                return data.get('active', False)
            return False
            
        except Exception as e:
            logger.error(f"Error checking subscription for {email}: {e}")
            return False
    
    def get_active_subscribers(self) -> List[Dict]:
        """Get all active subscribers"""
        if not self.db:
            return []
        
        try:
            subscribers = self.db.collection(self.collection_name).where('active', '==', True).get()
            return [doc.to_dict() for doc in subscribers]
            
        except Exception as e:
            logger.error(f"Error getting active subscribers: {e}")
            return []
    
    def get_all_subscribers(self) -> List[Dict]:
        """Get all subscribers (active and inactive)"""
        if not self.db:
            return []
        
        try:
            subscribers = self.db.collection(self.collection_name).get()
            return [doc.to_dict() for doc in subscribers]
            
        except Exception as e:
            logger.error(f"Error getting all subscribers: {e}")
            return []
    
    def get_subscriber_count(self) -> int:
        """Get count of active subscribers"""
        return len(self.get_active_subscribers())
    
    def get_stats(self) -> Dict:
        """Get subscription statistics"""
        if not self.db:
            return {
                'active_subscribers': 0,
                'total_subscribers': 0,
                'inactive_subscribers': 0,
                'last_updated': datetime.now().isoformat()
            }
        
        try:
            active_subscribers = self.get_active_subscribers()
            all_subscribers = self.get_all_subscribers()
            
            active_count = len(active_subscribers)
            total_count = len(all_subscribers)
            inactive_count = total_count - active_count
            
            return {
                'active_subscribers': active_count,
                'total_subscribers': total_count,
                'inactive_subscribers': inactive_count,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                'active_subscribers': 0,
                'total_subscribers': 0,
                'inactive_subscribers': 0,
                'last_updated': datetime.now().isoformat()
            }
    
    def export_subscribers(self, include_inactive: bool = False) -> List[Dict]:
        """Export subscribers for external use"""
        if include_inactive:
            return self.get_all_subscribers()
        else:
            return self.get_active_subscribers()

def main():
    """Test the FirebaseEmailManager functionality"""
    print("🧪 Testing FirebaseEmailManager...")
    
    # Initialize manager
    manager = FirebaseEmailManager()
    
    if not manager.db:
        print("❌ Firebase not initialized. Check your environment variables.")
        return
    
    # Test subscription
    result1 = manager.subscribe("test1@example.com", "Test User 1")
    print(f"Subscribe test1: {result1}")
    
    result2 = manager.subscribe("test2@example.com", "Test User 2")
    print(f"Subscribe test2: {result2}")
    
    # Test duplicate subscription
    result3 = manager.subscribe("test1@example.com", "Test User 1")
    print(f"Duplicate subscribe: {result3}")
    
    # Test stats
    stats = manager.get_stats()
    print(f"Stats: {stats}")
    
    # Test active subscribers
    active = manager.get_active_subscribers()
    print(f"Active subscribers: {len(active)}")
    
    # Test unsubscription
    result4 = manager.unsubscribe("test1@example.com")
    print(f"Unsubscribe test1: {result4}")
    
    # Test final stats
    final_stats = manager.get_stats()
    print(f"Final stats: {final_stats}")

if __name__ == "__main__":
    main()
