# 🛰️ Aerospace Newsletter

Automated newsletter that fetches the latest aerospace and defense news and sends it via email twice a week using GitHub Actions.

## 📁 Project Structure

```
aerospace_newsletter/
├── fetch_articles.py              # Main newsletter script
├── video_fetcher.py              # YouTube video fetcher for featured videos
├── email_manager.py              # Email subscription management
├── signup_server.py              # Web interface server
├── manage_subscribers.py         # CLI management tool
├── test.py                       # Test suite
├── setup_github_actions.sh       # Setup script
├── requirements.txt               # Python dependencies
├── .github/workflows/newsletter.yml # GitHub Actions workflow
├── .gitignore                    # Git ignore file
├── templates/                    # Web interface templates
│   ├── signup.html              # Newsletter signup form
│   ├── unsubscribe.html         # Unsubscribe form
│   └── admin.html               # Admin panel
├── subscribers.json              # Email storage (auto-created)
├── SETUP.md                      # Setup guide
├── NEWSLETTER_SIGNUP.md          # Signup system documentation
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

### Newsletter Content
- Fetches from 5 RSS feeds:
  - Defense News
  - Breaking Defense
  - NASA Breaking News
  - DroneLife
  - MIT Drones News
- **🎬 Featured Video**: Automatically includes a relevant, recent aerospace video from top YouTube channels (Everyday Astronaut, Scott Manley, NASASpaceflight, SpaceX, NASA, etc.)
- Beautiful HTML email formatting
- Automatic cloud-based delivery
- Manual trigger capability

### Email Management
- **Web Signup Form**: Beautiful, responsive subscription interface
- **Email Collection**: Secure email storage and management
- **Unsubscribe System**: Easy one-click unsubscribe
- **Admin Panel**: Complete subscriber management
- **Multi-recipient**: Send to all active subscribers
- **CLI Tools**: Command-line management utilities

## 🧪 Testing

```bash
# Run tests
python test.py

# Test email management
python email_manager.py

# Test web interface
python signup_server.py
# Then visit http://localhost:5000

# Test newsletter with subscribers
export GMAIL_EMAIL="your_email@gmail.com"
export GMAIL_APP_PASSWORD="your_app_password"
python fetch_articles.py
```

## 🌐 Web Interface

### Start Web Server
```bash
python signup_server.py
```

### Access Points
- **Signup Form**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **Unsubscribe**: http://localhost:5000/unsubscribe

### Management Commands
```bash
# Subscribe an email
python manage_subscribers.py subscribe user@example.com "User Name"

# List subscribers
python manage_subscribers.py list

# Show statistics
python manage_subscribers.py stats
```

## 🔧 Management

- **View runs**: GitHub → Actions tab
- **Manual test**: Actions → Run workflow
- **Update script**: Edit locally, commit, push

## 🚀 GitHub Deployment

### Quick Deploy
```bash
# Run the deployment script
./deploy_to_github.sh
```

### Manual Deploy
1. **Merge to main branch:**
   ```bash
   git checkout main
   git merge feature/newsletter-signup
   git push origin main
   ```

2. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: "GitHub Actions"
   - Save

3. **Set up secrets:**
   - Go to Settings → Secrets and variables → Actions
   - Add: `GMAIL_EMAIL` and `GMAIL_APP_PASSWORD`

4. **Access your newsletter:**
   - Signup: `https://yourusername.github.io/aerospace_newsletter/`
   - Newsletter runs automatically on schedule

## 📖 Documentation

- `SETUP.md` - Basic setup instructions
- `NEWSLETTER_SIGNUP.md` - Signup system documentation  
- `DEPLOYMENT.md` - Complete deployment guide
