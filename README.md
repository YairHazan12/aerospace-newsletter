# 🛰️ Aerospace Newsletter

Automated newsletter that fetches the latest aerospace and defense news and sends it via email twice a week using GitHub Actions.

## 📁 Project Structure

```
aerospace_newsletter/
├── fetch_articles.py              # Main newsletter script
├── test.py                       # Test suite
├── setup_github_actions.sh       # Setup script
├── requirements.txt               # Python dependencies
├── .github/workflows/newsletter.yml # GitHub Actions workflow
├── .gitignore                    # Git ignore file
├── SETUP.md                      # Setup guide
└── README.md                     # This file
```

## 🚀 Quick Setup

1. **Create GitHub repository** (must be public)
2. **Set up Gmail App Password:**
   - Google Account → Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Set GitHub secrets:**
   - `GMAIL_EMAIL` = your_email@gmail.com
   - `GMAIL_APP_PASSWORD` = your_16_character_app_password
   - `TO_EMAIL` = recipient@gmail.com (optional)
4. **Run setup script:**
   ```bash
   ./setup_github_actions.sh
   ```
5. **Test workflow** in GitHub Actions tab

## 📅 Schedule

- **Tuesday**: 9:00 AM UTC (4:00 AM EST)
- **Friday**: 9:00 AM UTC (4:00 AM EST)

## 📧 Features

- Fetches from 5 RSS feeds:
  - Defense News
  - Breaking Defense
  - NASA Breaking News
  - DroneLife
  - MIT Drones News
- Beautiful HTML email formatting
- Automatic cloud-based delivery
- Manual trigger capability

## 🧪 Testing

```bash
# Run tests
python test.py

# Test locally with environment variables
export GMAIL_EMAIL="your_email@gmail.com"
export GMAIL_APP_PASSWORD="your_app_password"
export TO_EMAIL="recipient@gmail.com"
python fetch_articles.py
```

## 🔧 Management

- **View runs**: GitHub → Actions tab
- **Manual test**: Actions → Run workflow
- **Update script**: Edit locally, commit, push

## 📖 Documentation

See `SETUP.md` for detailed setup instructions.
