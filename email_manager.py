#!/usr/bin/env python3
"""
Email Management System for Aerospace Newsletter
Handles email collection, storage, and management
"""

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class EmailManager:
    """Manages newsletter email subscriptions"""
    
    def __init__(self, storage_file: str = "subscribers.json"):
        self.storage_file = storage_file
        self.subscribers = self._load_subscribers()
    
    def _load_subscribers(self) -> List[Dict]:
        """Load subscribers from storage file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    return data.get('subscribers', [])
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.error(f"Error loading subscribers: {e}")
                return []
        return []
    
    def _save_subscribers(self) -> bool:
        """Save subscribers to storage file"""
        try:
            data = {
                'subscribers': self.subscribers,
                'last_updated': datetime.now().isoformat(),
                'total_count': len(self.subscribers)
            }
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving subscribers: {e}")
            return False
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def subscribe(self, email: str, name: str = None) -> Dict:
        """Subscribe a new email to the newsletter"""
        email = email.strip().lower()
        
        # Validate email
        if not self._validate_email(email):
            return {
                'success': False,
                'message': 'Invalid email format',
                'email': email
            }
        
        # Check if already subscribed
        if self.is_subscribed(email):
            return {
                'success': False,
                'message': 'Email already subscribed',
                'email': email
            }
        
        # Add new subscriber
        subscriber = {
            'email': email,
            'name': name.strip() if name else None,
            'subscribed_at': datetime.now().isoformat(),
            'active': True,
            'unsubscribe_token': self._generate_unsubscribe_token(email)
        }
        
        self.subscribers.append(subscriber)
        
        if self._save_subscribers():
            logger.info(f"New subscriber added: {email}")
            return {
                'success': True,
                'message': 'Successfully subscribed to newsletter',
                'email': email,
                'subscriber': subscriber
            }
        else:
            return {
                'success': False,
                'message': 'Failed to save subscription',
                'email': email
            }
    
    def unsubscribe(self, email: str = None, token: str = None) -> Dict:
        """Unsubscribe an email from the newsletter"""
        if not email and not token:
            return {
                'success': False,
                'message': 'Email or unsubscribe token required'
            }
        
        # Find subscriber
        subscriber = None
        if email:
            email = email.strip().lower()
            subscriber = next((s for s in self.subscribers if s['email'] == email), None)
        elif token:
            subscriber = next((s for s in self.subscribers if s['unsubscribe_token'] == token), None)
        
        if not subscriber:
            return {
                'success': False,
                'message': 'Email not found in subscribers'
            }
        
        # Mark as unsubscribed
        subscriber['active'] = False
        subscriber['unsubscribed_at'] = datetime.now().isoformat()
        
        if self._save_subscribers():
            logger.info(f"Subscriber unsubscribed: {subscriber['email']}")
            return {
                'success': True,
                'message': 'Successfully unsubscribed from newsletter',
                'email': subscriber['email']
            }
        else:
            return {
                'success': False,
                'message': 'Failed to save unsubscription'
            }
    
    def is_subscribed(self, email: str) -> bool:
        """Check if email is subscribed and active"""
        email = email.strip().lower()
        subscriber = next((s for s in self.subscribers if s['email'] == email), None)
        return subscriber is not None and subscriber.get('active', False)
    
    def get_active_subscribers(self) -> List[Dict]:
        """Get all active subscribers"""
        return [s for s in self.subscribers if s.get('active', False)]
    
    def get_all_subscribers(self) -> List[Dict]:
        """Get all subscribers (active and inactive)"""
        return self.subscribers
    
    def get_subscriber_count(self) -> int:
        """Get count of active subscribers"""
        return len(self.get_active_subscribers())
    
    def _generate_unsubscribe_token(self, email: str) -> str:
        """Generate a unique unsubscribe token for an email"""
        import hashlib
        import secrets
        
        # Create a unique token based on email and timestamp
        salt = secrets.token_hex(16)
        token_data = f"{email}{datetime.now().isoformat()}{salt}"
        token = hashlib.sha256(token_data.encode()).hexdigest()[:32]
        return token
    
    def get_stats(self) -> Dict:
        """Get subscription statistics"""
        active_count = self.get_subscriber_count()
        total_count = len(self.subscribers)
        inactive_count = total_count - active_count
        
        return {
            'active_subscribers': active_count,
            'total_subscribers': total_count,
            'inactive_subscribers': inactive_count,
            'last_updated': datetime.now().isoformat()
        }
    
    def export_subscribers(self, include_inactive: bool = False) -> List[Dict]:
        """Export subscribers for external use"""
        if include_inactive:
            return self.get_all_subscribers()
        else:
            return self.get_active_subscribers()

def main():
    """Test the EmailManager functionality"""
    print("🧪 Testing EmailManager...")
    
    # Initialize manager
    manager = EmailManager()
    
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
