#!/usr/bin/env python3
"""
Test imports script for the Aerospace Newsletter
Verifies all required modules can be imported successfully
"""

import sys
import os

def test_core_imports():
    """Test core Python standard library imports"""
    print("🧪 Testing core Python imports...")
    
    try:
        # Standard library modules
        import os
        import smtplib
        from datetime import datetime
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        import logging
        import re
        
        print("✅ Core Python modules imported successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Core import failed: {e}")
        return False

def test_third_party_imports():
    """Test third-party package imports"""
    print("🧪 Testing third-party imports...")
    
    try:
        # Third-party packages
        import feedparser
        from dotenv import load_dotenv
        
        print("✅ Third-party modules imported successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Third-party import failed: {e}")
        print("💡 Try running: pip install feedparser python-dotenv")
        return False

def test_newsletter_imports():
    """Test importing the newsletter functions"""
    print("🧪 Testing newsletter function imports...")
    
    try:
        # Import newsletter functions
        from fetch_articles import (
            fetch_latest_articles,
            format_articles_for_email,
            format_articles_for_text,
            send_email_with_articles
        )
        
        print("✅ Newsletter functions imported successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Newsletter import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of imported modules"""
    print("🧪 Testing basic functionality...")
    
    try:
        # Import datetime again to ensure it's in scope
        from datetime import datetime
        
        # Test datetime
        now = datetime.now()
        print(f"✅ Datetime working: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test logging
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info("✅ Logging working")
        
        # Test email components
        from email.mime.multipart import MIMEMultipart
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Test"
        msg["From"] = "test@example.com"
        msg["To"] = "recipient@example.com"
        print("✅ Email components working")
        
        # Test regex
        import re
        test_text = "This is a <p>test</p> with HTML tags"
        cleaned = re.sub(r'<[^>]+>', '', test_text)
        if cleaned == "This is a test with HTML tags":
            print("✅ HTML cleaning working")
        else:
            print("⚠️ HTML cleaning may have issues")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def test_environment_setup():
    """Test environment variable handling"""
    print("🧪 Testing environment setup...")
    
    try:
        from dotenv import load_dotenv
        
        # Test loading .env file (if it exists)
        load_dotenv()
        print("✅ Environment loading working")
        
        # Test getting environment variables
        test_var = os.getenv("TEST_VAR", "default_value")
        if test_var == "default_value":
            print("✅ Environment variable handling working")
        
        return True
        
    except Exception as e:
        print(f"❌ Environment test failed: {e}")
        return False

def main():
    """Run all import tests"""
    print("🚀 Aerospace Newsletter Import Tests")
    print("=" * 50)
    
    tests = [
        ("Core Python Imports", test_core_imports),
        ("Third-party Imports", test_third_party_imports),
        ("Newsletter Imports", test_newsletter_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Environment Setup", test_environment_setup)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All import tests passed!")
        print("✅ Newsletter is ready to run!")
        return 0
    else:
        print("⚠️ Some import tests failed")
        print("💡 Check the error messages above for solutions")
        return 1

if __name__ == "__main__":
    exit(main())
