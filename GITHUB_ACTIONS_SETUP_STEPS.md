# 🚀 GitHub Actions Setup - Step by Step Guide

## Problem: Secrets Not Being Read Properly

If your GitHub Actions workflow isn't reading the secrets correctly, follow these steps to fix it.

---

## 📋 Step 1: Verify Your Repository Setup

### 1.1 Check Repository Type
- ✅ **Your repository MUST be PUBLIC** for free GitHub Actions
- ❌ Private repositories have limited free minutes

### 1.2 Verify Files Are Pushed
Make sure these files are in your repository:
- `fetch_articles.py`
- `requirements.txt`
- `.github/workflows/newsletter.yml`

---

## 🔐 Step 2: Set Up GitHub Secrets (CRITICAL)

### 2.1 Go to Your Repository
1. Navigate to: `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`
2. Click **Settings** (in the repository menu)
3. Click **Secrets and variables** → **Actions**

### 2.2 Add Required Secrets
Click **"New repository secret"** for each:

#### Secret 1: GMAIL_EMAIL
- **Name**: `GMAIL_EMAIL`
- **Value**: `your_email@gmail.com` (the Gmail account sending emails)

#### Secret 2: GMAIL_APP_PASSWORD
- **Name**: `GMAIL_APP_PASSWORD`
- **Value**: `your_16_character_app_password` (NOT your regular password)

#### Secret 3: TO_EMAIL (Optional)
- **Name**: `TO_EMAIL`
- **Value**: `felihazan@gmail.com` (recipient email)

### 2.3 Verify Secrets Are Added
You should see all three secrets listed in the repository secrets page.

---

## 📧 Step 3: Set Up Gmail App Password

### 3.1 Enable 2-Factor Authentication
1. Go to [Google Account](https://myaccount.google.com)
2. Go to **Security** → **2-Step Verification**
3. Enable 2-Step Verification if not already enabled

### 3.2 Generate App Password
1. In Google Account → **Security** → **2-Step Verification**
2. Scroll down to **"App passwords"**
3. Click **"App passwords"**
4. Select **"Mail"** as the app
5. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### 3.3 Use App Password in GitHub
- Use the 16-character password (with or without spaces)
- **NEVER use your regular Gmail password**

---

## 🔧 Step 4: Update Your Workflow File

Make sure your `.github/workflows/newsletter.yml` looks like this:

```yaml
name: 🛰️ Aerospace Newsletter

on:
  schedule:
    - cron: '0 9 * * 2,5'
  workflow_dispatch:

jobs:
  send-newsletter:
    runs-on: ubuntu-latest
    
    steps:
    - name: 📥 Checkout repository
      uses: actions/checkout@v4
      
    - name: 🐍 Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: 📦 Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: 🛰️ Send Newsletter
      env:
        GMAIL_EMAIL: ${{ secrets.GMAIL_EMAIL }}
        GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
        TO_EMAIL: ${{ secrets.TO_EMAIL }}
      run: |
        echo "🚀 Starting newsletter automation..."
        python fetch_articles.py
        echo "✅ Newsletter process completed"
```

---

## 🧪 Step 5: Test the Workflow

### 5.1 Manual Test
1. Go to your repository → **Actions** tab
2. Click **"🛰️ Aerospace Newsletter"**
3. Click **"Run workflow"** (top right)
4. Click the green **"Run workflow"** button

### 5.2 Check the Logs
1. Click on the workflow run
2. Click on **"🛰️ Send Newsletter"** step
3. Look for these debug messages:
   ```
   📧 Email configuration:
     • Sender: your_email@gmail.com
     • Recipient: felihazan@gmail.com
     • Password set: Yes
   ```

### 5.3 Common Issues and Solutions

#### Issue: "Gmail credentials not found!"
**Solution**: Check that `GMAIL_EMAIL` and `GMAIL_APP_PASSWORD` secrets are set correctly

#### Issue: "Authentication failed!"
**Solution**: 
- Verify you're using App Password, not regular password
- Ensure 2-Factor Authentication is enabled
- Check the App Password is for "Mail" app

#### Issue: "Recipient email not found!"
**Solution**: Either set `TO_EMAIL` secret or the script will use the default

---

## 🔍 Step 6: Debug Common Problems

### 6.1 Check Secret Names
Make sure secret names are EXACTLY:
- `GMAIL_EMAIL` (not `gmail_email` or `Gmail_Email`)
- `GMAIL_APP_PASSWORD` (not `GMAIL_PASSWORD`)
- `TO_EMAIL` (optional)

### 6.2 Check Secret Values
- **GMAIL_EMAIL**: Should be a valid Gmail address
- **GMAIL_APP_PASSWORD**: Should be 16 characters (App Password)
- **TO_EMAIL**: Should be a valid email address

### 6.3 Verify Repository Access
- Repository must be public for free GitHub Actions
- Check that the workflow file is in `.github/workflows/` directory

---

## 📊 Step 7: Monitor the Workflow

### 7.1 Check Schedule
- **Tuesday**: 9:00 AM UTC (4:00 AM EST)
- **Friday**: 9:00 AM UTC (4:00 AM EST)

### 7.2 View Logs
1. Go to **Actions** tab
2. Click on any workflow run
3. Click on **"🛰️ Send Newsletter"** step
4. See detailed logs of the process

### 7.3 Success Indicators
Look for these messages in the logs:
```
✅ Articles sent successfully to recipient email!
🎉 Successfully fetched and sent X articles to recipient email!
```

---

## 🚨 Troubleshooting Checklist

### ✅ Repository Setup
- [ ] Repository is public
- [ ] Workflow file exists in `.github/workflows/`
- [ ] All required files are committed and pushed

### ✅ Secrets Setup
- [ ] `GMAIL_EMAIL` secret is set
- [ ] `GMAIL_APP_PASSWORD` secret is set (App Password, not regular password)
- [ ] `TO_EMAIL` secret is set (optional)
- [ ] Secret names are exactly as shown (case-sensitive)

### ✅ Gmail Setup
- [ ] 2-Factor Authentication is enabled
- [ ] App Password is generated for "Mail"
- [ ] Using App Password, not regular password

### ✅ Testing
- [ ] Manual workflow run works
- [ ] No authentication errors
- [ ] Email is received

---

## 🎯 Quick Fix Commands

If you need to update the workflow:

```bash
# Update the workflow file
git add .github/workflows/newsletter.yml
git commit -m "Update workflow with proper secret handling"
git push origin main
```

If you need to test locally:

```bash
# Set environment variables locally
export GMAIL_EMAIL="your_email@gmail.com"
export GMAIL_APP_PASSWORD="your_app_password"
export TO_EMAIL="felihazan@gmail.com"

# Test the script
python fetch_articles.py
```

---

## 📞 Still Having Issues?

1. **Check the workflow logs** for specific error messages
2. **Verify all secrets are set** in the repository settings
3. **Test with a simple email** first to isolate the issue
4. **Make sure your Gmail account** has 2FA enabled and App Password generated

The most common issue is using the regular Gmail password instead of the App Password! 🔑

