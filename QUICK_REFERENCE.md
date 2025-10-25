# 🚀 Aerospace Newsletter - Quick Reference

## 📅 Schedule
- **Tuesday**: 9:00 AM
- **Friday**: 9:00 AM

## 🛠️ Setup (One-time)
```bash
cd /Users/yairhazan/projects/aerospace_newsletter
./setup_automation.sh
```

## 📊 Management Commands

### Check Status
```bash
launchctl list | grep aerospace
```

### Manual Test
```bash
./run_newsletter.sh
```

### View Logs
```bash
# Recent logs
tail -f logs/newsletter_*.log

# All logs
ls -la logs/
```

### Stop Automation
```bash
launchctl unload ~/Library/LaunchAgents/com.aerospace.newsletter.tuesday.plist
launchctl unload ~/Library/LaunchAgents/com.aerospace.newsletter.friday.plist
```

### Restart Automation
```bash
launchctl load ~/Library/LaunchAgents/com.aerospace.newsletter.tuesday.plist
launchctl load ~/Library/LaunchAgents/com.aerospace.newsletter.friday.plist
```

## 🔧 Troubleshooting

### Newsletter Not Sending
1. Check Gmail credentials: `echo $GMAIL_EMAIL`
2. Test manually: `./run_newsletter.sh`
3. Check logs: `tail -f logs/newsletter_*.log`

### LaunchAgent Not Running
```bash
# Check if loaded
launchctl list | grep aerospace

# Force start
launchctl start com.aerospace.newsletter.tuesday
launchctl start com.aerospace.newsletter.friday
```

### Update Credentials
1. Edit the plist files in `~/Library/LaunchAgents/`
2. Reload: `launchctl unload` then `launchctl load`

## 📁 File Locations
- **Script**: `/Users/yairhazan/projects/aerospace_newsletter/run_newsletter.sh`
- **Logs**: `/Users/yairhazan/projects/aerospace_newsletter/logs/`
- **Config**: `~/Library/LaunchAgents/com.aerospace.newsletter.*.plist`

## 📧 Email Recipient
- **To**: felihazan@gmail.com
- **Subject**: "Latest Aerospace & Defense News"
