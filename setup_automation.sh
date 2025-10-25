#!/bin/bash

# Aerospace Newsletter Automation Setup Script
# This script sets up the LaunchAgent automation for macOS

echo "🚀 Setting up Aerospace Newsletter Automation..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS. Please use the manual setup guide for other systems."
    exit 1
fi

# Get user's Gmail credentials
echo ""
echo "📧 Gmail Configuration Required"
echo "================================"
echo "You need to provide your Gmail credentials for the automation."
echo ""

read -p "Enter your Gmail address: " GMAIL_EMAIL
read -s -p "Enter your Gmail App Password: " GMAIL_APP_PASSWORD
echo ""

# Validate inputs
if [[ -z "$GMAIL_EMAIL" || -z "$GMAIL_APP_PASSWORD" ]]; then
    print_error "Gmail credentials are required!"
    exit 1
fi

# Update the plist files with actual credentials
echo "📝 Updating configuration files..."

# Update Tuesday plist
sed -i '' "s/your_email@gmail.com/$GMAIL_EMAIL/g" com.aerospace.newsletter.tuesday.plist
sed -i '' "s/your_app_password/$GMAIL_APP_PASSWORD/g" com.aerospace.newsletter.tuesday.plist

# Update Friday plist
sed -i '' "s/your_email@gmail.com/$GMAIL_EMAIL/g" com.aerospace.newsletter.friday.plist
sed -i '' "s/your_app_password/$GMAIL_APP_PASSWORD/g" com.aerospace.newsletter.friday.plist

print_status "Configuration files updated with your credentials"

# Copy plist files to LaunchAgents directory
echo "📁 Installing LaunchAgent configurations..."

# Create LaunchAgents directory if it doesn't exist
mkdir -p ~/Library/LaunchAgents

# Copy the plist files
cp com.aerospace.newsletter.tuesday.plist ~/Library/LaunchAgents/
cp com.aerospace.newsletter.friday.plist ~/Library/LaunchAgents/

print_status "LaunchAgent files installed"

# Load the LaunchAgents
echo "🔄 Loading LaunchAgents..."

launchctl load ~/Library/LaunchAgents/com.aerospace.newsletter.tuesday.plist
launchctl load ~/Library/LaunchAgents/com.aerospace.newsletter.friday.plist

print_status "LaunchAgents loaded successfully"

# Test the setup
echo ""
echo "🧪 Testing the setup..."
echo "======================"

# Test the script manually
echo "Running test newsletter..."
/Users/yairhazan/projects/aerospace_newsletter/run_newsletter.sh

if [ $? -eq 0 ]; then
    print_status "Test run completed successfully!"
else
    print_warning "Test run had issues. Check the logs for details."
fi

# Show status
echo ""
echo "📊 Automation Status"
echo "===================="
echo "Tuesday Newsletter:"
launchctl list | grep tuesday || echo "  Not found in launchctl list"

echo "Friday Newsletter:"
launchctl list | grep friday || echo "  Not found in launchctl list"

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo "Your newsletter will now run automatically:"
echo "• Every Tuesday at 9:00 AM"
echo "• Every Friday at 9:00 AM"
echo ""
echo "📁 Logs location: /Users/yairhazan/projects/aerospace_newsletter/logs/"
echo "🔧 Management commands:"
echo "  • Check status: launchctl list | grep aerospace"
echo "  • Unload: launchctl unload ~/Library/LaunchAgents/com.aerospace.newsletter.*.plist"
echo "  • Reload: launchctl load ~/Library/LaunchAgents/com.aerospace.newsletter.*.plist"
echo ""
echo "📖 For troubleshooting, see: automation_setup_guide.md"
