# 🚀 Automated Newsletter Setup Guide

## Overview
This guide will help you set up automated delivery of your aerospace newsletter twice a week using different scheduling methods.

## 📋 Prerequisites
- ✅ Newsletter script working (`fetch_articles.py`)
- ✅ Gmail credentials configured
- ✅ Virtual environment set up

---

## 🎯 Option 1: macOS LaunchAgent (Recommended for Mac)

### Step 1: Create the LaunchAgent Configuration
Create a new file at `~/Library/LaunchAgents/com.aerospace.newsletter.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aerospace.newsletter</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/yairhazan/projects/aerospace_newsletter/run_newsletter.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>2</integer>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/yairhazan/projects/aerospace_newsletter/logs/newsletter.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/yairhazan/projects/aerospace_newsletter/logs/newsletter_error.log</string>
</dict>
</plist>
```

### Step 2: Create the Shell Script
Create `run_newsletter.sh` in your project directory:

```bash
#!/bin/bash
cd /Users/yairhazan/projects/aerospace_newsletter
source venv/bin/activate
python fetch_articles.py
```

### Step 3: Make Script Executable
```bash
chmod +x /Users/yairhazan/projects/aerospace_newsletter/run_newsletter.sh
```

### Step 4: Create Logs Directory
```bash
mkdir -p /Users/yairhazan/projects/aerospace_newsletter/logs
```

### Step 5: Load the LaunchAgent
```bash
launchctl load ~/Library/LaunchAgents/com.aerospace.newsletter.plist
```

### Step 6: Create Second Schedule (Friday)
Create another file `~/Library/LaunchAgents/com.aerospace.newsletter.friday.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aerospace.newsletter.friday</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/yairhazan/projects/aerospace_newsletter/run_newsletter.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>6</integer>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/yairhazan/projects/aerospace_newsletter/logs/newsletter_friday.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/yairhazan/projects/aerospace_newsletter/logs/newsletter_friday_error.log</string>
</dict>
</plist>
```

Load the Friday schedule:
```bash
launchctl load ~/Library/LaunchAgents/com.aerospace.newsletter.friday.plist
```

---

## 🐧 Option 2: Linux/macOS Cron Jobs

### Step 1: Open Crontab Editor
```bash
crontab -e
```

### Step 2: Add Cron Jobs
Add these lines to run twice a week (Tuesday and Friday at 9 AM):

```bash
# Aerospace Newsletter - Tuesday 9 AM
0 9 * * 2 cd /Users/yairhazan/projects/aerospace_newsletter && source venv/bin/activate && python fetch_articles.py >> logs/cron.log 2>&1

# Aerospace Newsletter - Friday 9 AM  
0 9 * * 5 cd /Users/yairhazan/projects/aerospace_newsletter && source venv/bin/activate && python fetch_articles.py >> logs/cron.log 2>&1
```

### Step 3: Create Logs Directory
```bash
mkdir -p /Users/yairhazan/projects/aerospace_newsletter/logs
```

---

## ☁️ Option 3: GitHub Actions (Cloud-based)

### Step 1: Create GitHub Actions Workflow
Create `.github/workflows/newsletter.yml`:

```yaml
name: Aerospace Newsletter

on:
  schedule:
    # Run every Tuesday and Friday at 9 AM UTC
    - cron: '0 9 * * 2,5'
  workflow_dispatch: # Allow manual triggers

jobs:
  send-newsletter:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install feedparser python-dotenv
        
    - name: Send Newsletter
      env:
        GMAIL_EMAIL: ${{ secrets.GMAIL_EMAIL }}
        GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
      run: python fetch_articles.py
```

### Step 2: Set GitHub Secrets
1. Go to your repository → Settings → Secrets and variables → Actions
2. Add these secrets:
   - `GMAIL_EMAIL`: Your Gmail address
   - `GMAIL_APP_PASSWORD`: Your Gmail app password

---

## 🐳 Option 4: Docker with Systemd (Linux)

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "fetch_articles.py"]
```

### Step 2: Create requirements.txt
```
feedparser
python-dotenv
```

### Step 3: Create Systemd Service
Create `/etc/systemd/system/aerospace-newsletter.service`:

```ini
[Unit]
Description=Aerospace Newsletter Service
After=network.target

[Service]
Type=oneshot
User=your_username
WorkingDirectory=/Users/yairhazan/projects/aerospace_newsletter
ExecStart=/usr/bin/docker run --rm -e GMAIL_EMAIL=%i -e GMAIL_APP_PASSWORD=%i aerospace-newsletter
```

### Step 4: Create Systemd Timer
Create `/etc/systemd/system/aerospace-newsletter.timer`:

```ini
[Unit]
Description=Run Aerospace Newsletter twice weekly
Requires=aerospace-newsletter.service

[Timer]
OnCalendar=weekly
Persistent=true

[Install]
WantedBy=timers.target
```

---

## 🔧 Testing Your Setup

### Test LaunchAgent (macOS)
```bash
# Test the script manually
launchctl start com.aerospace.newsletter

# Check if it's loaded
launchctl list | grep aerospace

# View logs
tail -f /Users/yairhazan/projects/aerospace_newsletter/logs/newsletter.log
```

### Test Cron Jobs
```bash
# List current cron jobs
crontab -l

# Test manually
cd /Users/yairhazan/projects/aerospace_newsletter
source venv/bin/activate
python fetch_articles.py
```

### Test GitHub Actions
1. Go to your repository → Actions tab
2. Click "Run workflow" to test manually
3. Check the logs for any errors

---

## 📊 Monitoring and Maintenance

### Log Files Location
- **LaunchAgent**: `/Users/yairhazan/projects/aerospace_newsletter/logs/`
- **Cron**: `/Users/yairhazan/projects/aerospace_newsletter/logs/cron.log`
- **GitHub Actions**: Repository → Actions tab

### Useful Commands

#### LaunchAgent Management
```bash
# List all loaded agents
launchctl list | grep aerospace

# Unload an agent
launchctl unload ~/Library/LaunchAgents/com.aerospace.newsletter.plist

# Reload an agent
launchctl load ~/Library/LaunchAgents/com.aerospace.newsletter.plist
```

#### Cron Management
```bash
# Edit crontab
crontab -e

# List current jobs
crontab -l

# Remove all jobs
crontab -r
```

---

## 🚨 Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x run_newsletter.sh
   ```

2. **Environment Variables Not Found**
   - Ensure `.env` file exists
   - Check virtual environment activation

3. **Gmail Authentication Failed**
   - Verify App Password is correct
   - Ensure 2FA is enabled

4. **LaunchAgent Not Running**
   ```bash
   launchctl list | grep aerospace
   launchctl start com.aerospace.newsletter
   ```

### Debug Mode
Add this to your script for debugging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📅 Schedule Summary

| Method | Tuesday | Friday | Pros | Cons |
|--------|---------|--------|------|------|
| LaunchAgent | ✅ 9 AM | ✅ 9 AM | Native macOS, reliable | Mac only |
| Cron | ✅ 9 AM | ✅ 9 AM | Universal, simple | Requires always-on machine |
| GitHub Actions | ✅ 9 AM UTC | ✅ 9 AM UTC | Cloud-based, free | Requires GitHub repo |
| Docker + Systemd | ✅ 9 AM | ✅ 9 AM | Isolated, portable | Linux only |

**Recommended**: LaunchAgent for Mac users, GitHub Actions for cloud-based solution.
