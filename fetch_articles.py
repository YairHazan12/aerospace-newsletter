import feedparser
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Step 1: Gather latest news
FEEDS = [
    "https://www.defensenews.com/rss/",
    "https://www.flightglobal.com/rss",
    "https://breakingdefense.com/feed/",
    "https://www.nasa.gov/rss/dyn/breaking_news.rss"
]

def fetch_latest_articles(limit_per_feed=5):
    """Fetch latest articles from aerospace and defense RSS feeds"""
    articles = []
    total_articles = 0
    
    print("🛰️ Fetching latest aerospace & defense news...")
    
    for i, url in enumerate(FEEDS, 1):
        print(f"📡 Fetching from feed {i}/{len(FEEDS)}: {url}")
        try:
            feed = feedparser.parse(url)
            feed_articles = []
            
            for entry in feed.entries[:limit_per_feed]:
                article_info = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': getattr(entry, 'published', 'No date available'),
                    'summary': getattr(entry, 'summary', 'No summary available')
                }
                feed_articles.append(article_info)
                total_articles += 1
            
            articles.extend(feed_articles)
            print(f"✅ Fetched {len(feed_articles)} articles from {url}")
            
        except Exception as e:
            print(f"❌ Error fetching from {url}: {e}")
    
    print(f"📊 Total articles fetched: {total_articles}")
    return articles

def format_articles_for_output(articles):
    """Format articles for text output"""
    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append("AEROSPACE & DEFENSE NEWS - LATEST ARTICLES")
    output_lines.append("=" * 80)
    output_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_lines.append(f"Total articles: {len(articles)}")
    output_lines.append("")
    
    for i, article in enumerate(articles, 1):
        output_lines.append(f"{i}. {article['title']}")
        output_lines.append(f"   Link: {article['link']}")
        output_lines.append(f"   Published: {article['published']}")
        output_lines.append(f"   Summary: {article['summary'][:200]}{'...' if len(article['summary']) > 200 else ''}")
        output_lines.append("")
    
    return "\n".join(output_lines)

def send_email_with_articles(articles):
    """Send articles via email using SMTP (Gmail)"""
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("GMAIL_EMAIL")
    sender_password = os.getenv("GMAIL_APP_PASSWORD")  # Use App Password, not regular password
    recipient_email = "felihazan@gmail.com"
    
    if not sender_email or not sender_password:
        print("❌ Gmail credentials not found!")
        print("📝 Please set the following environment variables:")
        print("  • GMAIL_EMAIL=your_email@gmail.com")
        print("  • GMAIL_APP_PASSWORD=your_app_password")
        print("\n💡 To get an App Password:")
        print("  1. Go to Google Account settings")
        print("  2. Security > 2-Step Verification > App passwords")
        print("  3. Generate a new app password for 'Mail'")
        return False
    
    # Format content for email
    html_content = format_articles_for_email(articles)
    text_content = format_articles_for_text(articles)
    
    # Create email message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Latest Aerospace & Defense News"
    message["From"] = sender_email
    message["To"] = recipient_email
    
    # Add both text and HTML versions
    text_part = MIMEText(text_content, "plain")
    html_part = MIMEText(html_content, "html")
    
    message.attach(text_part)
    message.attach(html_part)
    
    try:
        # Connect to Gmail SMTP server
        print("📧 Connecting to Gmail SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(sender_email, sender_password)
        
        # Send email
        print("📤 Sending email...")
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        
        print("✅ Articles sent successfully to felihazan@gmail.com!")
        return True
        
    except Exception as e:
        print("❌ Failed to send email")
        print("📝 Error details:")
        print(f"  • Error type: {type(e).__name__}")
        print(f"  • Error message: {str(e)}")
        return False

def format_articles_for_email(articles):
    """Format articles for email HTML content"""
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background-color: #1a365d; color: white; padding: 20px; text-align: center; }}
            .article {{ margin: 20px 0; padding: 15px; border-left: 4px solid #2d3748; background-color: #f7fafc; }}
            .title {{ font-size: 18px; font-weight: bold; color: #2d3748; margin-bottom: 10px; }}
            .link {{ color: #3182ce; text-decoration: none; }}
            .link:hover {{ text-decoration: underline; }}
            .published {{ color: #718096; font-size: 14px; margin-bottom: 10px; }}
            .summary {{ color: #4a5568; }}
            .footer {{ text-align: center; margin-top: 30px; color: #718096; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🛰️ Aerospace & Defense News</h1>
            <p>Latest Articles - {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
    """
    
    for i, article in enumerate(articles, 1):
        html_content += f"""
        <div class="article">
            <div class="title">{i}. {article['title']}</div>
            <div class="published">📅 Published: {article['published']}</div>
            <div class="summary">📝 {article['summary'][:300]}{'...' if len(article['summary']) > 300 else ''}</div>
            <div style="margin-top: 10px;">
                <a href="{article['link']}" class="link">🔗 Read full article</a>
            </div>
        </div>
        """
    
    html_content += """
        <div class="footer">
            <p>Generated automatically from aerospace and defense RSS feeds</p>
        </div>
    </body>
    </html>
    """
    
    return html_content

def format_articles_for_text(articles):
    """Format articles for plain text email content"""
    text_content = f"""
🛰️ AEROSPACE & DEFENSE NEWS
Latest Articles - {datetime.now().strftime('%B %d, %Y')}
{'=' * 50}

"""
    
    for i, article in enumerate(articles, 1):
        text_content += f"""
{i}. {article['title']}
   📅 Published: {article['published']}
   🔗 Link: {article['link']}
   📝 Summary: {article['summary'][:300]}{'...' if len(article['summary']) > 300 else ''}
   
"""
    
    text_content += """
Generated automatically from aerospace and defense RSS feeds
"""
    
    return text_content

if __name__ == "__main__":
    # Fetch articles
    articles = fetch_latest_articles()
    
    if articles:
        # Send via email
        success = send_email_with_articles(articles)
        
        if success:
            print(f"\n🎉 Successfully fetched and sent {len(articles)} articles to felihazan@gmail.com!")
        else:
            print("❌ Failed to send articles via email.")
    else:
        print("❌ No articles were fetched.")
