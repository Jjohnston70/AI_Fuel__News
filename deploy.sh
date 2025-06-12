#!/bin/bash

echo "Preparing for deployment to Vercel..."

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "Vercel CLI not found. Would you like to install it? (y/n)"
    read -r answer
    if [ "$answer" = "y" ]; then
        npm install -g vercel
    else
        echo "Please install Vercel CLI manually with: npm install -g vercel"
        exit 1
    fi
fi

# Check if Git is available
if command -v git &> /dev/null; then
    # Commit any changes
    echo "Committing changes to Git..."
    git add .
    git commit -m "Prepare for Vercel deployment"
    
    echo "Would you like to push to GitHub? (y/n)"
    read -r push_answer
    if [ "$push_answer" = "y" ]; then
        git push
    fi
fi

# Deploy to Vercel
echo "Deploying to Vercel..."
vercel

echo "Deployment process completed!" 