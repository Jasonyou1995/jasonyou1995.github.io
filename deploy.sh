#!/bin/bash
# Deploy Academic Profile to GitHub Pages

echo "🚀 GitHub Pages Deployment Helper"
echo "=================================="
echo ""

# Check if photo exists
if [ ! -f "photo.jpg" ]; then
    echo "⚠️  Warning: photo.jpg not found!"
    echo "Please add your profile photo first."
    echo ""
fi

# Get GitHub username
echo "Enter your GitHub username:"
read USERNAME

REPO="$USERNAME.github.io"

echo ""
echo "📋 Deployment Checklist:"
echo "========================"
echo ""
echo "1. ✅ Website files created"
echo "2. ⏳ Create GitHub repository: $REPO"
echo "3. ⏳ Upload files to repository"
echo "4. ⏳ Enable GitHub Pages"
echo ""

echo "🔗 Quick Links:"
echo "==============="
echo "Create repo: https://github.com/new"
echo "Your site will be: https://$USERNAME.github.io"
echo ""

echo "📖 Next Steps:"
echo "=============="
echo ""
echo "Option 1 - Web Upload (Easiest):"
echo "  1. Go to https://github.com/new"
echo "  2. Name: $REPO"
echo "  3. Make it Public"
echo "  4. Upload index.html and photo.jpg"
echo "  5. Settings → Pages → Enable"
echo ""
echo "Option 2 - Git CLI:"
echo "  git init"
echo "  git add ."
echo "  git commit -m 'Initial commit'"
echo "  git remote add origin https://github.com/$USERNAME/$REPO.git"
echo "  git push -u origin main"
echo ""

echo "✨ After deployment, your site will be live at:"
echo "   https://$USERNAME.github.io"
echo ""
