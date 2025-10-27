# 🚀 GitHub Deployment Guide

This guide shows you how to deploy the newsletter signup system to GitHub.

## 📋 Prerequisites

- GitHub repository (public for free GitHub Actions)
- Gmail App Password set up
- Repository secrets configured

## 🎯 Deployment Options

### Option 1: GitHub Pages + GitHub Actions (Recommended)

**What it does:**
- Deploys a static signup page to GitHub Pages
- Runs newsletter automation via GitHub Actions
- Stores subscribers in the repository

**Steps:**

1. **Enable GitHub Pages:**
   - Go to your repository → Settings → Pages
   - Source: "GitHub Actions"
   - Save

2. **Set up repository secrets:**
   - Go to Settings → Secrets and variables → Actions
   - Add these secrets:
     - `GMAIL_EMAIL` = your_email@gmail.com
     - `GMAIL_APP_PASSWORD` = your_app_password

3. **Push to main branch:**
   ```bash
   git checkout main
   git merge feature/newsletter-signup
   git push origin main
   ```

4. **Access your newsletter:**
   - Signup page: `https://yourusername.github.io/aerospace-newsletter/`
   - Newsletter runs automatically on schedule

### Option 2: Heroku Deployment (Full Web Interface)

**What it does:**
- Deploys the full Flask web interface
- Includes admin panel and real-time management
- Requires Heroku account

**Steps:**

1. **Create Heroku app:**
   ```bash
   # Install Heroku CLI
   heroku create your-newsletter-app
   ```

2. **Add Heroku-specific files:**
   ```bash
   # Create Procfile
   echo "web: python signup_server.py" > Procfile
   
   # Create runtime.txt
   echo "python-3.11.0" > runtime.txt
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set GMAIL_EMAIL=your_email@gmail.com
   heroku config:set GMAIL_APP_PASSWORD=your_app_password
   heroku config:set SECRET_KEY=your-secret-key
   ```

4. **Deploy:**
   ```bash
   git add .
   git commit -m "Add Heroku deployment files"
   git push heroku main
   ```

### Option 3: Vercel Deployment (Serverless)

**What it does:**
- Deploys as serverless functions
- Automatic scaling
- Free tier available

**Steps:**

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Create vercel.json:**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "signup_server.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "signup_server.py"
       }
     ]
   }
   ```

3. **Deploy:**
   ```bash
   vercel --prod
   ```

## 🔧 Configuration

### GitHub Actions Secrets

Required secrets in your repository:

```
GMAIL_EMAIL=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_character_app_password
```

### Environment Variables (for web deployment)

```bash
GMAIL_EMAIL=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
SECRET_KEY=your-secret-key-for-sessions
PORT=5000
FLASK_DEBUG=False
```

## 📊 Monitoring

### GitHub Actions
- Go to your repository → Actions tab
- Monitor newsletter runs
- Check logs for errors

### Subscriber Management
- **GitHub Pages**: Contact form submission
- **Heroku/Vercel**: Full admin panel at `/admin`

## 🚨 Troubleshooting

### Common Issues

1. **Newsletter not sending:**
   - Check Gmail credentials
   - Verify subscribers exist
   - Check GitHub Actions logs

2. **Web interface not working:**
   - Check deployment logs
   - Verify environment variables
   - Test locally first

3. **No subscribers:**
   - Add subscribers manually via CLI
   - Check signup form functionality
   - Verify email validation

### Debug Commands

```bash
# Test locally
python signup_server.py

# Check subscribers
python manage_subscribers.py stats

# Test newsletter
python fetch_articles.py
```

## 📈 Scaling

### For High Volume

1. **Database Migration:**
   - Move from JSON to PostgreSQL
   - Use environment variables for connection

2. **Queue System:**
   - Use Celery for async email processing
   - Redis for task queue

3. **CDN:**
   - Use CloudFlare for static assets
   - Optimize images and CSS

4. **Monitoring:**
   - Add Sentry for error tracking
   - Use New Relic for performance monitoring

## 🔒 Security

### Production Checklist

- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS
- [ ] Set up rate limiting
- [ ] Validate all inputs
- [ ] Use environment variables for secrets
- [ ] Regular security updates
- [ ] Monitor for abuse

## 📞 Support

If you encounter issues:

1. Check the GitHub Actions logs
2. Test locally with the same environment
3. Verify all secrets are set correctly
4. Check the deployment platform logs

## 🎉 Success!

Once deployed, your newsletter will:
- ✅ Automatically collect subscribers
- ✅ Send newsletters twice weekly
- ✅ Provide admin management
- ✅ Scale with your audience
