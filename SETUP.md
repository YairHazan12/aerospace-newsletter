# 🚀 Setup Guide

## Quick Start

1. **Create GitHub repository** (must be public for free GitHub Actions)
2. **Set up Gmail App Password:**
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Set GitHub secrets:**
   - `GMAIL_EMAIL` = your_email@gmail.com
   - `GMAIL_APP_PASSWORD` = your_16_character_app_password
   - `TO_EMAIL` = recipient@gmail.com (optional, defaults to felihazan@gmail.com)
4. **Run setup script:**
   ```bash
   ./setup_github_actions.sh
   ```
5. **Test workflow** in GitHub Actions tab

## Schedule
- **Tuesday**: 9:00 AM UTC (4:00 AM EST)
- **Friday**: 9:00 AM UTC (4:00 AM EST)

## RSS Feeds
- Defense News
- Breaking Defense  
- NASA Breaking News
- DroneLife
- MIT Drones News

## Troubleshooting

### Common Issues
- **Authentication failed**: Use App Password, not regular password
- **Workflow not running**: Ensure repository is public
- **No articles**: Check RSS feed URLs are accessible

### Manual Testing
```bash
# Set environment variables
export GMAIL_EMAIL="your_email@gmail.com"
export GMAIL_APP_PASSWORD="your_app_password"
export TO_EMAIL="recipient@gmail.com"

# Test locally
python fetch_articles.py
```

## Management
- **View runs**: GitHub → Actions tab
- **Manual trigger**: Actions → Run workflow
- **Update script**: Edit locally, commit, push
