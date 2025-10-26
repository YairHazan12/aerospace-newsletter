import feedparser
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load the environment variables
load_dotenv()

# Step 1: Gather latest news
FEEDS = [
    "https://www.defensenews.com/rss/",
    "https://breakingdefense.com/feed/",
    "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "https://dronelife.com/feed",
    "https://news.mit.edu/topic/drones"
]

def fetch_latest_articles(limit_per_feed=5):
    """Fetch latest articles from aerospace and defense RSS feeds"""
    articles = []
    total_articles = 0
    
    logger.info("🛰️ Fetching latest aerospace & defense news...")
    
    for i, url in enumerate(FEEDS, 1):
        logger.info(f"📡 Fetching from feed {i}/{len(FEEDS)}: {url}")
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
            logger.info(f"✅ Fetched {len(feed_articles)} articles from {url}")
            
        except Exception as e:
            logger.error(f"❌ Error fetching from {url}: {e}")
    
    logger.info(f"📊 Total articles fetched: {total_articles}")
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
    recipient_email = os.getenv("TO_EMAIL", "yair99hazan@gmail.com")
    logger.debug(f"TO_EMAIL env var: {os.getenv('TO_EMAIL')}")
    logger.debug(f"recipient_email: {recipient_email}")

    # Debug information
    logger.info("📧 Email configuration:")
    logger.info(f"  • Sender: {sender_email}")
    logger.info(f"  • Recipient: {recipient_email}")
    logger.info(f"  • Password set: {'Yes' if sender_password else 'No'}")
    
    if not sender_email or not sender_password:
        logger.error("❌ Gmail credentials not found!")
        logger.error("📝 Please set the following environment variables:")
        logger.error("  • GMAIL_EMAIL=your_email@gmail.com")
        logger.error("  • GMAIL_APP_PASSWORD=your_app_password")
        logger.info("\n💡 To get an App Password:")
        logger.info("  1. Go to Google Account settings")
        logger.info("  2. Security > 2-Step Verification > App passwords")
        logger.info("  3. Generate a new app password for 'Mail'")
        return False
    
    if not recipient_email:
        logger.error("❌ Recipient email not found!")
        logger.error("📝 Please set TO_EMAIL environment variable or use default: felihazan@gmail.com")
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
        logger.info("📧 Connecting to Gmail SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        logger.info("🔐 Authenticating with Gmail...")
        server.login(sender_email, sender_password)
        
        # Send email
        logger.info("📤 Sending email...")
        logger.info(f"  • From: {sender_email}")
        logger.info(f"  • To: {recipient_email}")
        logger.info(f"  • Subject: Latest Aerospace & Defense News")
        
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        
        logger.info("✅ Articles sent successfully to recipient email!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error("❌ Authentication failed!")
        logger.error("📝 This usually means:")
        logger.error("  • Wrong Gmail App Password")
        logger.error("  • 2-Factor Authentication not enabled")
        logger.error("  • App Password not generated for 'Mail'")
        logger.error(f"  • Error: {str(e)}")
        return False
        
    except smtplib.SMTPRecipientsRefused as e:
        logger.error("❌ Recipient email rejected!")
        logger.error(f"📝 Invalid recipient email: {recipient_email}")
        logger.error(f"  • Error: {str(e)}")
        return False
        
    except Exception as e:
        logger.error("❌ Failed to send email")
        logger.error("📝 Error details:")
        logger.error(f"  • Error type: {type(e).__name__}")
        logger.error(f"  • Error message: {str(e)}")
        return False

def format_articles_for_email(articles):
    """Format articles for email HTML content with modern, sleek design"""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Aerospace & Defense News</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                line-height: 1.6;
                color: #2d3748;
                background-color: #f7fafc;
                margin: 0;
                padding: 20px;
            }}
            
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
                position: relative;
            }}
            
            .header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
                opacity: 0.3;
            }}
            
            .header-content {{
                position: relative;
                z-index: 1;
            }}
            
            .header h1 {{
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 10px;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }}
            
            .header .subtitle {{
                font-size: 1.1rem;
                opacity: 0.9;
                font-weight: 300;
            }}
            
            .content {{
                padding: 40px 30px;
            }}
            
            .stats {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                text-align: center;
            }}
            
            .stats h3 {{
                font-size: 1.5rem;
                margin-bottom: 5px;
            }}
            
            .article {{
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 25px;
                margin-bottom: 25px;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }}
            
            .article::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 4px;
                height: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            
            .article:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            }}
            
            .article-number {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                text-align: center;
                line-height: 30px;
                font-weight: bold;
                font-size: 14px;
                margin-right: 15px;
                vertical-align: top;
            }}
            
            .article-content {{
                display: inline-block;
                width: calc(100% - 50px);
                vertical-align: top;
            }}
            
            .title {{
                font-size: 1.3rem;
                font-weight: 600;
                color: #2d3748;
                margin-bottom: 12px;
                line-height: 1.4;
            }}
            
            .meta {{
                display: flex;
                align-items: center;
                margin-bottom: 15px;
                font-size: 0.9rem;
                color: #718096;
            }}
            
            .meta-item {{
                display: flex;
                align-items: center;
                margin-right: 20px;
            }}
            
            .meta-icon {{
                margin-right: 5px;
                font-size: 14px;
            }}
            
            .summary {{
                color: #4a5568;
                line-height: 1.6;
                margin-bottom: 20px;
                font-size: 0.95rem;
            }}
            
            .read-more {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 24px;
                border-radius: 25px;
                text-decoration: none;
                font-weight: 600;
                font-size: 0.9rem;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }}
            
            .read-more:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }}
            
            .footer {{
                background: #f8fafc;
                padding: 30px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
            }}
            
            .footer p {{
                color: #718096;
                font-size: 0.9rem;
                margin-bottom: 10px;
            }}
            
            .footer .powered-by {{
                font-size: 0.8rem;
                color: #a0aec0;
            }}
            
            @media (max-width: 600px) {{
                .container {{
                    margin: 10px;
                    border-radius: 8px;
                }}
                
                .header {{
                    padding: 30px 20px;
                }}
                
                .header h1 {{
                    font-size: 2rem;
                }}
                
                .content {{
                    padding: 30px 20px;
                }}
                
                .article {{
                    padding: 20px;
                }}
                
                .article-content {{
                    width: calc(100% - 40px);
                }}
                
                .title {{
                    font-size: 1.1rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="header-content">
                    <h1>🛰️ Aerospace & Defense News</h1>
                    <p class="subtitle">Latest Articles - {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
            </div>
            
            <div class="content">
                <div class="stats">
                    <h3>📊 {len(articles)} Articles This Week</h3>
                    <p>Curated from top aerospace and defense sources</p>
                </div>
    """
    
    for i, article in enumerate(articles, 1):
        # Clean up the summary by removing HTML tags
        clean_summary = article['summary']
        if '<' in clean_summary and '>' in clean_summary:
            import re
            clean_summary = re.sub(r'<[^>]+>', '', clean_summary)
        
        html_content += f"""
                <div class="article">
                    <span class="article-number">{i}</span>
                    <div class="article-content">
                        <div class="title">{article['title']}</div>
                        <div class="meta">
                            <div class="meta-item">
                                <span class="meta-icon">📅</span>
                                <span>{article['published']}</span>
                            </div>
                        </div>
                        <div class="summary">{clean_summary[:200]}{'...' if len(clean_summary) > 200 else ''}</div>
                        <a href="{article['link']}" class="read-more">Read Full Article →</a>
                    </div>
                </div>
        """
    
    html_content += """
            </div>
            
            <div class="footer">
                <p>🚀 Delivered automatically from aerospace and defense RSS feeds</p>
                <p class="powered-by">Powered by GitHub Actions</p>
            </div>
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
            logger.info(f"\n🎉 Successfully fetched and sent {len(articles)} articles to recipient email!")
        else:
            logger.error("❌ Failed to send articles via email.")
    else:
        logger.error("❌ No articles were fetched.")
