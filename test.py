#!/usr/bin/env python3
"""
Aerospace Newsletter Test Suite
Tests all functionality: imports, RSS fetching, email formatting, and sending
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetch_articles import (
    fetch_latest_articles,
    format_articles_for_email,
    format_articles_for_text,
    send_email_with_articles
)

class TestNewsletter(unittest.TestCase):
    """Test cases for the newsletter functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_articles = [
            {
                'title': 'Test Article 1',
                'link': 'https://example.com/article1',
                'published': 'Mon, 01 Jan 2024 12:00:00 +0000',
                'summary': 'This is a test article summary.'
            },
            {
                'title': 'Test Article 2',
                'link': 'https://example.com/article2',
                'published': 'Mon, 01 Jan 2024 13:00:00 +0000',
                'summary': 'Another test article with more content.'
            }
        ]
    
    def test_imports(self):
        """Test that all required modules can be imported"""
        try:
            import feedparser
            from dotenv import load_dotenv
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            print("✅ All imports successful")
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_article_fetching(self):
        """Test article fetching with mocked RSS feeds"""
        with patch('fetch_articles.feedparser') as mock_feedparser:
            # Mock feed entries
            mock_entry = MagicMock()
            mock_entry.title = "Test Article"
            mock_entry.link = "https://example.com"
            mock_entry.published = "Mon, 01 Jan 2024 12:00:00 +0000"
            mock_entry.summary = "Test summary"
            
            mock_feed = MagicMock()
            mock_feed.entries = [mock_entry] * 5
            mock_feedparser.parse.return_value = mock_feed
            
            articles = fetch_latest_articles(limit_per_feed=2)
            
            self.assertIsInstance(articles, list)
            if articles:
                article = articles[0]
                self.assertIn('title', article)
                self.assertIn('link', article)
                self.assertIn('published', article)
                self.assertIn('summary', article)
                print("✅ Article structure is correct")
    
    def test_email_html_formatting(self):
        """Test HTML email formatting"""
        html_content = format_articles_for_email(self.sample_articles)
        
        # Check essential HTML elements
        self.assertIn('<!DOCTYPE html>', html_content)
        self.assertIn('Aerospace & Defense News', html_content)
        self.assertIn('Test Article 1', html_content)
        self.assertIn('Read Full Article', html_content)
        print("✅ HTML formatting is correct")
    
    def test_email_text_formatting(self):
        """Test plain text email formatting"""
        text_content = format_articles_for_text(self.sample_articles)
        
        # Check essential text elements
        self.assertIn('AEROSPACE & DEFENSE NEWS', text_content)
        self.assertIn('Test Article 1', text_content)
        self.assertIn('https://example.com/article1', text_content)
        print("✅ Text formatting is correct")
    
    def test_email_sending_mock(self):
        """Test email sending with mocked SMTP"""
        with patch.dict(os.environ, {
            'GMAIL_EMAIL': 'test@gmail.com',
            'GMAIL_APP_PASSWORD': 'test_password',
            'TO_EMAIL': 'recipient@gmail.com'
        }):
            with patch('fetch_articles.smtplib.SMTP') as mock_smtp:
                mock_server = MagicMock()
                mock_smtp.return_value = mock_server
                
                result = send_email_with_articles(self.sample_articles)
                
                # Verify SMTP was called correctly
                mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
                mock_server.starttls.assert_called_once()
                mock_server.login.assert_called_once_with('test@gmail.com', 'test_password')
                mock_server.sendmail.assert_called_once()
                mock_server.quit.assert_called_once()
                
                self.assertTrue(result)
                print("✅ Email sending (mocked) works correctly")
    
    def test_missing_credentials(self):
        """Test handling of missing credentials"""
        with patch.dict(os.environ, {}, clear=True):
            result = send_email_with_articles(self.sample_articles)
            self.assertFalse(result)
            print("✅ Missing credentials handled correctly")

def run_integration_test():
    """Run a full integration test (requires network)"""
    print("\n🚀 Running Integration Test...")
    print("=" * 50)
    
    try:
        print("📡 Testing RSS feed fetching...")
        articles = fetch_latest_articles(limit_per_feed=1)
        
        if articles:
            print(f"✅ Successfully fetched {len(articles)} articles")
            
            print("📧 Testing email formatting...")
            html_content = format_articles_for_email(articles[:2])
            text_content = format_articles_for_text(articles[:2])
            
            print("✅ Email formatting successful")
            print(f"📊 HTML content length: {len(html_content)} characters")
            print(f"📊 Text content length: {len(text_content)} characters")
        else:
            print("⚠️ No articles fetched (network may be down)")
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")

if __name__ == "__main__":
    print("🧪 Aerospace Newsletter Test Suite")
    print("=" * 50)
    
    # Run unit tests
    print("\n📋 Running Unit Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run integration test
    run_integration_test()
    
    print("\n🎉 All tests completed!")
    print("=" * 50)
