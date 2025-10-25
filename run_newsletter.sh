#!/bin/bash

# Aerospace Newsletter Runner Script
# This script runs the newsletter fetching and email sending

# Set the project directory
PROJECT_DIR="/Users/yairhazan/projects/aerospace_newsletter"
LOG_DIR="$PROJECT_DIR/logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log file with timestamp
LOG_FILE="$LOG_DIR/newsletter_$(date +%Y%m%d_%H%M%S).log"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_message "🚀 Starting Aerospace Newsletter automation..."

# Change to project directory
cd "$PROJECT_DIR" || {
    log_message "❌ Failed to change to project directory: $PROJECT_DIR"
    exit 1
}

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    log_message "✅ Virtual environment activated"
else
    log_message "❌ Virtual environment not found at venv/bin/activate"
    exit 1
fi

# Check if required environment variables are set
if [ -z "$GMAIL_EMAIL" ] || [ -z "$GMAIL_APP_PASSWORD" ]; then
    log_message "❌ Gmail credentials not found in environment variables"
    log_message "📝 Please set GMAIL_EMAIL and GMAIL_APP_PASSWORD"
    exit 1
fi

# Run the newsletter script
log_message "📧 Running newsletter script..."
python fetch_articles.py >> "$LOG_FILE" 2>&1

# Check the exit status
if [ $? -eq 0 ]; then
    log_message "✅ Newsletter sent successfully!"
else
    log_message "❌ Newsletter failed to send. Check logs for details."
fi

log_message "🏁 Newsletter automation completed"
