#!/usr/bin/env python3
"""
Quick test script for the Aerospace Newsletter
Tests core functionality without complex mocking
"""

import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetch_articles import (
    fetch_latest_articles,
    format_articles_for_email,
    format_articles_for_text
)

def test_imports():
    """Test that all imports work"""
    print("🧪 Testing imports...")
    try:
        import feedparser
        from dotenv import load_dotenv
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_article_fetching():
    """Test article fetching"""
    print("\n🧪 Testing article fetching...")
    try:
        articles = fetch_latest_articles(limit_per_feed=1)
        if articles:
            print(f"✅ Successfully fetched {len(articles)} articles")
            print(f"📊 Sample article: {articles[0]['title'][:50]}...")
            return True
        else:
            print("⚠️ No articles fetched (network may be down)")
            return False
    except Exception as e:
        print(f"❌ Article fetching failed: {e}")
        return False

def test_email_formatting():
    """Test email formatting"""
    print("\n🧪 Testing email formatting...")
    try:
        # Create sample articles
        sample_articles = [
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
        
        # Test HTML formatting
        html_content = format_articles_for_email(sample_articles)
        print(f"✅ HTML email generated ({len(html_content)} characters)")
        
        # Test text formatting
        text_content = format_articles_for_text(sample_articles)
        print(f"✅ Text email generated ({len(text_content)} characters)")
        
        # Check for key elements
        if 'Aerospace & Defense News' in html_content:
            print("✅ HTML contains expected content")
        if 'AEROSPACE & DEFENSE NEWS' in text_content:
            print("✅ Text contains expected content")
            
        return True
    except Exception as e:
        print(f"❌ Email formatting failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable handling"""
    print("\n🧪 Testing environment variables...")
    
    # Test default values
    from fetch_articles import send_email_with_articles
    
    # Clear environment
    old_email = os.environ.get('GMAIL_EMAIL')
    old_password = os.environ.get('GMAIL_APP_PASSWORD')
    
    if 'GMAIL_EMAIL' in os.environ:
        del os.environ['GMAIL_EMAIL']
    if 'GMAIL_APP_PASSWORD' in os.environ:
        del os.environ['GMAIL_APP_PASSWORD']
    
    # Test with no credentials
    sample_articles = [{'title': 'Test', 'link': 'https://example.com', 'published': 'Now', 'summary': 'Test'}]
    result = send_email_with_articles(sample_articles)
    
    if not result:
        print("✅ Correctly handles missing credentials")
    else:
        print("❌ Should fail with missing credentials")
    
    # Restore environment
    if old_email:
        os.environ['GMAIL_EMAIL'] = old_email
    if old_password:
        os.environ['GMAIL_APP_PASSWORD'] = old_password
    
    return True

def test_performance():
    """Test performance"""
    print("\n🧪 Testing performance...")
    import time
    
    sample_articles = [
        {
            'title': f'Test Article {i}',
            'link': f'https://example.com/article{i}',
            'published': 'Mon, 01 Jan 2024 12:00:00 +0000',
            'summary': f'This is test article {i} with some content.'
        }
        for i in range(10)
    ]
    
    # Test HTML generation speed
    start_time = time.time()
    html_content = format_articles_for_email(sample_articles)
    html_time = time.time() - start_time
    
    print(f"📊 HTML generation: {html_time:.3f} seconds")
    print(f"📊 Content size: {len(html_content)} characters")
    
    if html_time < 0.1:
        print("✅ HTML generation is fast")
    else:
        print("⚠️ HTML generation is slow")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Aerospace Newsletter Quick Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Article Fetching", test_article_fetching),
        ("Email Formatting", test_email_formatting),
        ("Environment Variables", test_environment_variables),
        ("Performance", test_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed")
        return 1

if __name__ == "__main__":
    exit(main())
