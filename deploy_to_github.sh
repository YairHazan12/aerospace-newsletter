#!/bin/bash

# GitHub Deployment Script for Aerospace Newsletter
# This script helps you deploy the newsletter signup system to GitHub

echo "🚀 GitHub Deployment for Aerospace Newsletter"
echo "=============================================="

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

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_error "Not in a git repository. Please run this from your project directory."
    exit 1
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
print_info "Current branch: $CURRENT_BRANCH"

# Check if we're on the feature branch
if [ "$CURRENT_BRANCH" != "feature/newsletter-signup" ]; then
    print_warning "You're not on the feature/newsletter-signup branch"
    read -p "Do you want to switch to it? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git checkout feature/newsletter-signup
    else
        print_error "Please switch to the feature branch first"
        exit 1
    fi
fi

# Check if there are uncommitted changes
if ! git diff --quiet; then
    print_warning "You have uncommitted changes"
    read -p "Do you want to commit them? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "🚀 Prepare for GitHub deployment"
    else
        print_error "Please commit your changes first"
        exit 1
    fi
fi

# Merge to main branch
print_info "Merging feature branch to main..."
git checkout main
git merge feature/newsletter-signup --no-ff -m "🚀 Merge newsletter signup system to main"

# Push to GitHub
print_info "Pushing to GitHub..."
git push origin main

# Check if GitHub Pages is enabled
print_info "Checking GitHub Pages setup..."

# Create a simple check for GitHub Pages
echo "📋 Next steps to complete deployment:"
echo ""
echo "1. 🌐 Enable GitHub Pages:"
echo "   • Go to: https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^.]*\).*/\1/')/settings/pages"
echo "   • Source: 'GitHub Actions'"
echo "   • Save"
echo ""
echo "2. 🔐 Set up repository secrets:"
echo "   • Go to: https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^.]*\).*/\1/')/settings/secrets/actions"
echo "   • Add secret: GMAIL_EMAIL = your_email@gmail.com"
echo "   • Add secret: GMAIL_APP_PASSWORD = your_app_password"
echo ""
echo "3. 🧪 Test the deployment:"
echo "   • Go to: https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^.]*\).*/\1/')/actions"
echo "   • Run the 'Deploy Newsletter Web Interface' workflow"
echo "   • Run the 'Aerospace Newsletter' workflow"
echo ""
echo "4. 🌍 Access your newsletter:"
echo "   • Signup page: https://$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^.]*\).*/\1/').github.io/aerospace_newsletter/"
echo "   • Admin panel: Contact form submission"
echo ""

print_status "Deployment preparation complete!"
print_info "Follow the steps above to complete the setup."

# Return to feature branch
git checkout feature/newsletter-signup

echo ""
print_info "You're back on the feature/newsletter-signup branch"
print_info "The main branch now contains the newsletter signup system"
