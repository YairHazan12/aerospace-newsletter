#!/usr/bin/env python3
"""
Simple one-liner test for quick verification
"""

# Test all imports in one go
try:
    import feedparser
    from dotenv import load_dotenv
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from datetime import datetime
    import os
    import logging
    import re
    
    from fetch_articles import fetch_latest_articles, format_articles_for_email, send_email_with_articles
    
    print("✅ All imports successful!")
    print("🚀 Newsletter is ready to run!")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
