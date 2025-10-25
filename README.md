# 🛰️ Aerospace Newsletter

Automated newsletter that fetches the latest aerospace and defense news and sends it via email twice a week using GitHub Actions.

## 📁 Project Structure

```
aerospace_newsletter/
├── fetch_articles.py              # Main newsletter script
├── requirements.txt               # Python dependencies
├── .github/workflows/newsletter.yml # GitHub Actions workflow
├── setup_github_actions.sh       # Setup script
├── github_actions_setup_guide.md # Complete setup guide
└── README.md                     # This file
```

## 🚀 Quick Setup

1. **Create GitHub repository** (public)
2. **Run setup script:**
   ```bash
   ./setup_github_actions.sh
   ```
3. **Set GitHub secrets:**
   - `GMAIL_EMAIL` = your_email@gmail.com
   - `GMAIL_APP_PASSWORD` = your_app_password
4. **Test workflow** in GitHub Actions

## 📅 Schedule

- **Tuesday**: 9:00 AM UTC (4:00 AM EST)
- **Friday**: 9:00 AM UTC (4:00 AM EST)

## 📧 Features

- Fetches from 4 RSS feeds:
  - Defense News
  - Flight Global
  - Breaking Defense
  - NASA Breaking News
- Beautiful HTML email formatting
- Automatic cloud-based delivery
- Manual trigger capability

## 🔧 Management

- **View runs**: GitHub → Actions tab
- **Manual test**: Actions → Run workflow
- **Update script**: Edit locally, commit, push

## 📖 Documentation

See `github_actions_setup_guide.md` for detailed setup instructions.
