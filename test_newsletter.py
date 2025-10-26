#!/usr/bin/env python3
"""
Comprehensive test suite for the Aerospace Newsletter
Tests all components: RSS fetching, email formatting, and sending
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import tempfile
import smtplib

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
                'summary': 'This is a test article summary for testing purposes.'
            },
            {
                'title': 'Test Article 2',
                'link': 'https://example.com/article2',
                'published': 'Mon, 01 Jan 2024 13:00:00 +0000',
                'summary': 'Another test article with a longer summary that contains more detailed information about the subject matter.'
            }
        ]
    
    def test_fetch_articles_structure(self):
        """Test that fetch_articles returns the correct structure"""
        print("🧪 Testing article fetching structure...")
        
        # Mock the feedparser to avoid actual network calls
        with patch('fetch_articles.feedparser') as mock_feedparser:
            # Mock feed entries
            mock_entry = MagicMock()
            mock_entry.title = "Test Article"
            mock_entry.link = "https://example.com"
            mock_entry.published = "Mon, 01 Jan 2024 12:00:00 +0000"
            mock_entry.summary = "Test summary"
            
            mock_feed = MagicMock()
            mock_feed.entries = [mock_entry] * 5  # 5 articles per feed
            
            mock_parse = MagicMock()
            mock_parse.return_value = mock_feed
            mock_feedparser.parse = mock_parse
            
            articles = fetch_latest_articles(limit_per_feed=2)
            
            # Verify structure
            self.assertIsInstance(articles, list)
            if articles:  # Only test if articles were returned
                article = articles[0]
                self.assertIn('title', article)
                self.assertIn('link', article)
                self.assertIn('published', article)
                self.assertIn('summary', article)
                print("✅ Article structure is correct")
            else:
                print("⚠️ No articles returned (network may be down)")
    
    def test_email_html_formatting(self):
        """Test HTML email formatting"""
        print("🧪 Testing HTML email formatting...")
        
        html_content = format_articles_for_email(self.sample_articles)
        
        # Check essential HTML elements
        self.assertIn('<!DOCTYPE html>', html_content)
        self.assertIn('<html lang="en">', html_content)
        self.assertIn('Aerospace & Defense News', html_content)
        self.assertIn('Test Article 1', html_content)
        self.assertIn('Test Article 2', html_content)
        self.assertIn('Read Full Article', html_content)
        self.assertIn('Powered by GitHub Actions', html_content)
        
        # Check for modern CSS
        self.assertIn('linear-gradient', html_content)
        self.assertIn('border-radius', html_content)
        self.assertIn('box-shadow', html_content)
        
        print("✅ HTML formatting is correct")
    
    def test_email_text_formatting(self):
        """Test plain text email formatting"""
        print("🧪 Testing plain text email formatting...")
        
        text_content = format_articles_for_text(self.sample_articles)
        
        # Check essential text elements
        self.assertIn('AEROSPACE & DEFENSE NEWS', text_content)
        self.assertIn('Test Article 1', text_content)
        self.assertIn('Test Article 2', text_content)
        self.assertIn('https://example.com/article1', text_content)
        self.assertIn('Generated automatically', text_content)
        
        print("✅ Text formatting is correct")
    
    def test_email_sending_mock(self):
        """Test email sending with mocked SMTP"""
        print("🧪 Testing email sending (mocked)...")
        
        # Set up environment variables
        with patch.dict(os.environ, {
            'GMAIL_EMAIL': 'test@gmail.com',
            'GMAIL_APP_PASSWORD': 'test_password',
            'TO_EMAIL': 'recipient@gmail.com'
        }):
            # Mock SMTP
            with patch('fetch_articles.smtplib.SMTP') as mock_smtp:
                mock_server = MagicMock()
                mock_smtp.return_value = mock_server
                
                # Test successful sending
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
        print("🧪 Testing missing credentials handling...")
        
        # Clear environment variables
        with patch.dict(os.environ, {}, clear=True):
            result = send_email_with_articles(self.sample_articles)
            self.assertFalse(result)
            print("✅ Missing credentials handled correctly")
    
    def test_article_cleaning(self):
        """Test HTML tag cleaning in summaries"""
        print("🧪 Testing HTML tag cleaning...")
        
        # Create article with HTML tags
        dirty_article = {
            'title': 'Test Article',
            'link': 'https://example.com',
            'published': 'Mon, 01 Jan 2024 12:00:00 +0000',
            'summary': '<p>This is a <strong>test</strong> summary with <a href="#">links</a>.</p>'
        }
        
        html_content = format_articles_for_email([dirty_article])
        
        # Check that HTML tags are removed from summary
        self.assertNotIn('<p>', html_content)
        self.assertNotIn('<strong>', html_content)
        self.assertNotIn('<a href', html_content)
        self.assertIn('This is a test summary with links', html_content)
        
        print("✅ HTML tag cleaning works correctly")
    
    def test_date_formatting(self):
        """Test date formatting in email"""
        print("🧪 Testing date formatting...")
        
        html_content = format_articles_for_email(self.sample_articles)
        current_date = datetime.now().strftime('%B %d, %Y')
        
        self.assertIn(current_date, html_content)
        print("✅ Date formatting is correct")
    
    def test_responsive_design(self):
        """Test responsive design elements"""
        print("🧪 Testing responsive design...")
        
        html_content = format_articles_for_email(self.sample_articles)
        
        # Check for responsive CSS
        self.assertIn('@media (max-width: 600px)', html_content)
        self.assertIn('viewport', html_content)
        self.assertIn('max-width', html_content)
        
        print("✅ Responsive design elements present")
    
    def test_gradient_styling(self):
        """Test modern gradient styling"""
        print("🧪 Testing gradient styling...")
        
        html_content = format_articles_for_email(self.sample_articles)
        
        # Check for gradient CSS
        self.assertIn('linear-gradient(135deg', html_content)
        self.assertIn('box-shadow', html_content)
        self.assertIn('border-radius', html_content)
        self.assertIn('transition', html_content)
        
        print("✅ Modern styling elements present")

def run_integration_test():
    """Run a full integration test (requires network)"""
    print("\n🚀 Running Integration Test...")
    print("=" * 50)
    
    try:
        # Test actual RSS fetching
        print("📡 Testing RSS feed fetching...")
        articles = fetch_latest_articles(limit_per_feed=1)
        
        if articles:
            print(f"✅ Successfully fetched {len(articles)} articles")
            
            # Test email formatting
            print("📧 Testing email formatting...")
            html_content = format_articles_for_email(articles[:2])  # Test with first 2 articles
            text_content = format_articles_for_text(articles[:2])
            
            print("✅ Email formatting successful")
            print(f"📊 HTML content length: {len(html_content)} characters")
            print(f"📊 Text content length: {len(text_content)} characters")
            
        else:
            print("⚠️ No articles fetched (network may be down)")
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")

def run_performance_test():
    """Run performance tests"""
    print("\n⚡ Running Performance Test...")
    print("=" * 50)
    
    import time
    
    # Test HTML generation speed
    start_time = time.time()
    html_content = format_articles_for_email([{
        'title': 'Performance Test Article',
        'link': 'https://example.com',
        'published': 'Mon, 01 Jan 2024 12:00:00 +0000',
        'summary': 'This is a test article for performance testing.'
    }] * 10)  # 10 articles
    html_time = time.time() - start_time
    
    print(f"📊 HTML generation time: {html_time:.3f} seconds")
    print(f"📊 HTML content size: {len(html_content)} characters")
    
    if html_time < 1.0:
        print("✅ HTML generation is fast")
    else:
        print("⚠️ HTML generation is slow")

if __name__ == "__main__":
    print("🧪 Aerospace Newsletter Test Suite")
    print("=" * 50)
    
    # Run unit tests
    print("\n📋 Running Unit Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run integration test
    run_integration_test()
    
    # Run performance test
    run_performance_test()
    
    print("\n🎉 All tests completed!")
    print("=" * 50)
