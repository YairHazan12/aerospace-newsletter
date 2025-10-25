import feedparser
from openai import OpenAI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
sendgrid_client = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))

# Step 1: Gather latest news
FEEDS = [
    "https://www.defensenews.com/rss/",
    "https://www.flightglobal.com/rss",
    "https://breakingdefense.com/feed/",
    "https://www.nasa.gov/rss/dyn/breaking_news.rss"
]

def fetch_latest_articles(limit_per_feed=5):
    articles = []
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:limit_per_feed]:
            articles.append(f"- [{entry.title}]({entry.link})")
    return "\n".join(articles)

# Step 2: Summarize & format newsletter
def generate_newsletter(content):
    prompt = f"""
    You are an assistant that writes a professional newsletter.
    Create a short, engaging newsletter (around 200 words) summarizing the following aerospace and defense news:
    {content}

    Structure:
    - Short intro line about the week in aerospace & defense
    - 3–4 key highlights
    - End with “See you next update!”
    """
    completion = openai_client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()

# Step 3: Send email
def send_email(subject, html_content):
    message = Mail(
        from_email=os.getenv("FROM_EMAIL"),
        to_emails=os.getenv("TO_EMAIL"),
        subject=subject,
        html_content=html_content
    )
    try:
        sendgrid_client.send(message)
        print("✅ Newsletter sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Step 4: Run
if __name__ == "__main__":
    print("🛰️ Fetching latest aerospace & defense news...")
    news = fetch_latest_articles()

    print("🧠 Generating newsletter summary with GPT-5...")
    newsletter_text = generate_newsletter(news)

    print("📤 Sending newsletter via email...")
    send_email("Aerospace & Defense Weekly Update", newsletter_text)
