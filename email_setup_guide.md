# Email Setup Guide

## Option 1: Gmail SMTP (Recommended)

### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Navigate to Security > 2-Step Verification
3. Enable 2-Step Verification if not already enabled

### Step 2: Generate App Password
1. In Google Account settings, go to Security > 2-Step Verification
2. Scroll down to "App passwords"
3. Click "App passwords"
4. Select "Mail" as the app
5. Copy the generated 16-character password

### Step 3: Set Environment Variables
Run these commands in your terminal:

```bash
export GMAIL_EMAIL="your_email@gmail.com"
export GMAIL_APP_PASSWORD="your_16_character_app_password"
```

### Step 4: Run the Script
```bash
cd /Users/yairhazan/projects/aerospace_newsletter
source venv/bin/activate
python fetch_articles.py
```

## Option 2: Other Email Providers

### Outlook/Hotmail
```python
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587
```

### Yahoo
```python
smtp_server = "smtp.mail.yahoo.com"
smtp_port = 587
```

## Troubleshooting

- **Authentication Error**: Make sure you're using an App Password, not your regular Gmail password
- **Connection Error**: Check your internet connection and firewall settings
- **2FA Required**: Gmail requires 2-Factor Authentication to be enabled for App Passwords

## Security Notes

- Never commit your App Password to version control
- Use environment variables to store credentials
- Consider using a dedicated email account for automated sending
