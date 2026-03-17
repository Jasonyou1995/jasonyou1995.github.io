# Academic Profile - Shengwei You

🎓 **AI Agent Security & Web3 Architecture Researcher**

🔗 **Live Site**: [yourusername.github.io](https://yourusername.github.io) *(after deployment)*

---

## 📋 Overview

Modern, responsive academic personal website featuring:
- ✨ Animated gradient background
- 🎯 Research focus sections
- 📚 Publications showcase
- 💼 Professional timeline
- 🛠️ Technical skills grid
- 📱 Fully responsive design

---

## 🚀 Deployment to GitHub Pages

### Step 1: Prepare Your Photo
1. Rename your photo to `photo.jpg`
2. Place it in the same folder as `index.html`
3. Recommended size: 800x800px, square aspect ratio

### Step 2: Create GitHub Repository
1. Go to [github.com/new](https://github.com/new)
2. Repository name: `yourusername.github.io`
   - Replace `yourusername` with your actual GitHub username
3. Make it **Public**
4. Click **Create repository**

### Step 3: Upload Files
#### Option A: Web Upload (Easy)
1. Click **"uploading an existing file"**
2. Drag and drop:
   - `index.html`
   - `photo.jpg`
3. Click **Commit changes**

#### Option B: Git Command Line
```bash
# Clone your repository
git clone https://github.com/yourusername/yourusername.github.io.git
cd yourusername.github.io

# Copy files
cp /path/to/index.html .
cp /path/to/photo.jpg .

# Commit and push
git add .
git commit -m "Initial website upload"
git push origin main
```

### Step 4: Enable GitHub Pages
1. Go to repository **Settings**
2. Click **Pages** in left sidebar
3. Source: Select **Deploy from a branch**
4. Branch: Select **main** / **master**
5. Click **Save**

### Step 5: Access Your Site
- Wait 2-5 minutes for deployment
- Visit: `https://yourusername.github.io`

---

## 🎨 Customization

### Edit Content
Open `index.html` and modify:

| Section | Line | What to Change |
|---------|------|----------------|
| Name | ~150 | `Shengwei` and `You` |
| Title | ~153 | Subtitle text |
| Bio | ~155 | Description paragraph |
| Publications | ~230-260 | Add your papers |
| Experience | ~290-320 | Add your roles |
| Skills | ~380-410 | Update technologies |
| Contact | ~430 | Email, LinkedIn links |

### Change Colors
Edit CSS variables in `<style>`:
```css
:root {
    --primary: #0a0a0f;    /* Background */
    --accent: #00d4aa;      /* Primary color */
    --gradient-2: #3b82f6;  /* Secondary color */
}
```

### Update Photo
Simply replace `photo.jpg` with your image (keep the same filename).

---

## 📁 File Structure

```
academic-profile/
├── index.html          # Main website file
├── photo.jpg           # Your profile photo
├── README.md           # This file
├── css/               # (optional) stylesheets
├── js/                # (optional) scripts
└── images/            # (optional) other images
```

---

## 🌟 Features

### Sections Included
1. **Hero** - Introduction with animated photo frame
2. **Research** - 4 research area cards
3. **Publications** - Paper listings
4. **Experience** - Timeline of roles
5. **Skills** - Technology tags
6. **Contact** - Links and CTA

### Technical Highlights
- Pure HTML/CSS/JS (no dependencies)
- Mobile-first responsive design
- Smooth scroll animations
- Floating card effects
- Gradient animations
- Intersection Observer API

---

## 🔗 Quick Links to Update

In `index.html`, search and replace:
- `shengwei.you@gmail.com` → Your email
- `linkedin.com/in/shengwei-you` → Your LinkedIn
- Twitter/X link → Your handle

---

## 📞 Support

Need help? Check:
1. [GitHub Pages Documentation](https://docs.github.com/en/pages)
2. Open `index.html` in browser locally to preview
3. Use browser DevTools (F12) to debug

---

**Created**: March 15, 2026  
**Template**: Modern Academic Portfolio  
**License**: Free to use and modify
