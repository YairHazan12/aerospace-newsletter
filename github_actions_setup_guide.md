# 🚀 GitHub Actions Setup Guide

## Overview
This guide will help you set up automated delivery of your aerospace newsletter using GitHub Actions. This runs in the cloud and doesn't require your machine to be always on.

## ✅ Prerequisites
- GitHub account
- Newsletter script working locally
- Gmail App Password ready

---

## 📋 Step-by-Step Setup

### Step 1: Create GitHub Repository

1. **Go to GitHub.com** and create a new repository:
   - Repository name: `aerospace-newsletter` (or any name you prefer)
   - Make it **Public** (required for free GitHub Actions)
   - Initialize with README

2. **Clone the repository locally:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/aerospace-newsletter.git
   cd aerospace-newsletter
   ```

### Step 2: Upload Your Files

Copy all your newsletter files to the repository:

```bash
# Copy your files to the repository directory
cp /Users/yairhazan/projects/aerospace_newsletter/*.py .
cp /Users/yairhazan/projects/aerospace_newsletter/requirements.txt .
cp /Users/yairhazan/projects/aerospace_newsletter/.github/workflows/newsletter.yml .github/workflows/
```

### Step 3: Set Up GitHub Secrets

1. **Go to your repository on GitHub**
2. **Click Settings** (in the repository menu)
3. **Click "Secrets and variables" → "Actions"**
4. **Click "New repository secret"**

Add these two secrets:

#### Secret 1: GMAIL_EMAIL
- **Name**: `GMAIL_EMAIL`
- **Value**: `your_email@gmail.com`

#### Secret 2: GMAIL_APP_PASSWORD
- **Name**: `GMAIL_APP_PASSWORD`
- **Value**: `your_16_character_app_password`

### Step 4: Commit and Push

```bash
# Add all files
git add .

# Commit
git commit -m "🚀 Add automated aerospace newsletter with GitHub Actions"

# Push to GitHub
git push origin main
```

### Step 5: Test the Workflow

1. **Go to your repository on GitHub**
2. **Click the "Actions" tab**
3. **Click on "🛰️ Aerospace Newsletter" workflow**
4. **Click "Run workflow" button** (top right)
5. **Click the green "Run workflow" button**

---

## 📅 Schedule Details

### Current Schedule
- **Tuesday**: 9:00 AM UTC (4:00 AM EST / 1:00 AM PST)
- **Friday**: 9:00 AM UTC (4:00 AM EST / 1:00 AM PST)

### Customizing the Schedule

Edit `.github/workflows/newsletter.yml` and modify the cron expression:

```yaml
schedule:
  - cron: '0 9 * * 2,5'  # Tuesday and Friday at 9 AM UTC
```

**Cron Examples:**
- `'0 9 * * 1,3,5'` - Monday, Wednesday, Friday at 9 AM UTC
- `'0 14 * * 2,5'` - Tuesday and Friday at 2 PM UTC
- `'0 9 * * *'` - Every day at 9 AM UTC

---

## 🔧 Management & Monitoring

### View Workflow Runs
1. Go to your repository → **Actions** tab
2. Click on **"🛰️ Aerospace Newsletter"**
3. See all runs with status (✅ success, ❌ failed, ⏳ running)

### Manual Triggers
- **From GitHub UI**: Actions → Run workflow
- **From command line**: 
  ```bash
  gh workflow run "🛰️ Aerospace Newsletter"
  ```

### View Logs
1. Click on any workflow run
2. Click on **"🛰️ Send Newsletter"** step
3. See detailed logs of the newsletter process

### Download Logs
- Logs are automatically saved as artifacts
- Available for 30 days
- Download from the workflow run page

---

## 🚨 Troubleshooting

### Common Issues

#### 1. Workflow Not Running
**Check:**
- Repository is public (required for free GitHub Actions)
- Secrets are set correctly
- Cron schedule is valid

#### 2. Email Not Sending
**Check:**
- Gmail App Password is correct
- 2-Factor Authentication is enabled
- Secrets are named exactly: `GMAIL_EMAIL` and `GMAIL_APP_PASSWORD`

#### 3. Dependencies Issues
**Check:**
- `requirements.txt` is in the repository
- All Python dependencies are listed

### Debug Steps

1. **Check workflow logs:**
   - Go to Actions → Latest run → Send Newsletter step
   - Look for error messages

2. **Test locally:**
   ```bash
   # Set environment variables
   export GMAIL_EMAIL="your_email@gmail.com"
   export GMAIL_APP_PASSWORD="your_app_password"
   
   # Run the script
   python fetch_articles.py
   ```

3. **Verify secrets:**
   - Go to Settings → Secrets and variables → Actions
   - Ensure both secrets exist and are spelled correctly

---

## 📊 Advanced Configuration

### Environment Variables
Add more environment variables to the workflow:

```yaml
env:
  GMAIL_EMAIL: ${{ secrets.GMAIL_EMAIL }}
  GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
  RECIPIENT_EMAIL: ${{ secrets.RECIPIENT_EMAIL }}
  CUSTOM_SUBJECT: "Weekly Aerospace Update"
```

### Multiple Recipients
Modify the script to send to multiple recipients:

```python
recipients = [
    "felihazan@gmail.com",
    "another@email.com"
]
```

### Conditional Sending
Add conditions to only send on certain days or with certain content:

```yaml
- name: 🛰️ Send Newsletter
  if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
  env:
    GMAIL_EMAIL: ${{ secrets.GMAIL_EMAIL }}
    GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
  run: python fetch_articles.py
```

---

## 🎯 Benefits of GitHub Actions

### ✅ Advantages
- **Free**: 2,000 minutes/month for public repositories
- **Reliable**: Runs on GitHub's infrastructure
- **No maintenance**: No need to keep your machine on
- **Logs**: Built-in logging and monitoring
- **Scalable**: Easy to add more features

### 📈 Usage Limits
- **Public repos**: 2,000 minutes/month free
- **Private repos**: 500 minutes/month free
- **Our newsletter**: ~2 minutes per run = ~16 minutes/month

---

## 🔄 Updating the Newsletter

### To Update the Script
1. Edit `fetch_articles.py` locally
2. Commit and push:
   ```bash
   git add fetch_articles.py
   git commit -m "Update newsletter script"
   git push origin main
   ```

### To Change Schedule
1. Edit `.github/workflows/newsletter.yml`
2. Update the cron expression
3. Commit and push

### To Add New RSS Feeds
1. Edit the `FEEDS` list in `fetch_articles.py`
2. Commit and push

---

## 📞 Support

If you encounter issues:

1. **Check the workflow logs** in GitHub Actions
2. **Test locally** with the same environment variables
3. **Verify Gmail settings** (App Password, 2FA)
4. **Check GitHub Actions status** at https://www.githubstatus.com/

---

## 🎉 Success!

Once set up, your newsletter will automatically:
- ✅ Fetch latest aerospace news twice a week
- ✅ Send beautifully formatted emails
- ✅ Log all activities
- ✅ Run reliably in the cloud

**No more manual work required!** 🚀
