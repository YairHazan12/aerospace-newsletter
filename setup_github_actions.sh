#!/bin/bash

# GitHub Actions Setup Script for Aerospace Newsletter
# This script helps you set up the GitHub Actions automation

echo "🚀 GitHub Actions Setup for Aerospace Newsletter"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_warning "Not in a git repository. Initializing..."
    git init
fi

echo ""
print_info "This script will help you set up GitHub Actions for your newsletter."
echo ""

# Get GitHub repository URL
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/aerospace-newsletter): " REPO_URL

if [[ -z "$REPO_URL" ]]; then
    print_error "Repository URL is required!"
    exit 1
fi

# Extract repository name from URL
REPO_NAME=$(basename "$REPO_URL" .git)
print_info "Repository name: $REPO_NAME"

# Check if remote is already set
if git remote get-url origin &> /dev/null; then
    print_warning "Remote 'origin' already exists. Updating..."
    git remote set-url origin "$REPO_URL"
else
    print_info "Adding remote origin..."
    git remote add origin "$REPO_URL"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    print_info "Creating .gitignore..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Environment variables
.env
.env.local
.env.*.local

# Logs
logs/
*.log

# macOS
.DS_Store

# IDE
.vscode/
.idea/
*.swp
*.swo

# Temporary files
*.tmp
*.temp
EOF
    print_status ".gitignore created"
fi

# Check if all required files exist
REQUIRED_FILES=("fetch_articles.py" "requirements.txt" ".github/workflows/newsletter.yml")

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Required file missing: $file"
        exit 1
    fi
done

print_status "All required files found"

# Add all files to git
print_info "Adding files to git..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    print_warning "No changes to commit"
else
    print_info "Committing changes..."
    git commit -m "🚀 Add automated aerospace newsletter with GitHub Actions"
    print_status "Changes committed"
fi

# Push to GitHub
print_info "Pushing to GitHub..."
if git push -u origin main 2>/dev/null; then
    print_status "Successfully pushed to GitHub!"
elif git push -u origin master 2>/dev/null; then
    print_status "Successfully pushed to GitHub!"
else
    print_error "Failed to push to GitHub. Please check your repository URL and permissions."
    exit 1
fi

echo ""
echo "🎉 GitHub Actions Setup Complete!"
echo "================================"
echo ""
print_info "Next steps:"
echo ""
echo "1. 📧 Set up Gmail secrets in GitHub:"
echo "   • Go to: https://github.com/$(echo $REPO_URL | sed 's/.*github.com\///')/settings/secrets/actions"
echo "   • Add secret: GMAIL_EMAIL = your_email@gmail.com"
echo "   • Add secret: GMAIL_APP_PASSWORD = your_app_password"
echo ""
echo "2. 🧪 Test the workflow:"
echo "   • Go to: https://github.com/$(echo $REPO_URL | sed 's/.*github.com\///')/actions"
echo "   • Click '🛰️ Aerospace Newsletter'"
echo "   • Click 'Run workflow'"
echo ""
echo "3. 📅 Schedule:"
echo "   • Tuesday: 9:00 AM UTC (4:00 AM EST)"
echo "   • Friday: 9:00 AM UTC (4:00 AM EST)"
echo ""
print_info "Your newsletter will now run automatically in the cloud! 🚀"
echo ""
print_warning "Remember to set up your Gmail App Password if you haven't already:"
echo "• Google Account → Security → 2-Step Verification → App passwords"
