# GitHub Upload Checklist

Follow these steps to upload your Medical Symptom Checker to GitHub:

## 1. Initialize Git Repository (if not already done)

```bash
cd C:\Users\Draxler\Documents\Norton\NU_ExpertSystems\Y3S1\medical-symptom-checker
git init
```

## 2. Configure Git (first time only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 3. Create Repository on GitHub

1. Go to https://github.com
2. Click the "+" icon in the top right
3. Select "New repository"
4. Name it: `medical-symptom-checker`
5. Description: "Intelligent medical symptom diagnosis system with Flask"
6. Keep it **Public**
7. **DO NOT** initialize with README, .gitignore, or license (we have these already)
8. Click "Create repository"

## 4. Add Files to Git

```bash
git add .gitignore
git add README.md
git add QUICKSTART.md
git add CONTRIBUTING.md
git add LICENSE
git add requirements.txt
git add app.py
git add templates/
git add static/
git add screenshots/
```

**Note:** The `main.py` file will be ignored (it's in .gitignore)

## 5. Create Initial Commit

```bash
git commit -m "Initial commit: Medical Symptom Checker v1.0"
```

## 6. Connect to GitHub Repository

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/medical-symptom-checker.git
git branch -M main
```

## 7. Push to GitHub

```bash
git push -u origin main
```

## 8. Update README with Correct URL

After uploading, update the README.md:
- Replace `YOUR_USERNAME` with your actual GitHub username in the clone command

## 9. Add Repository Topics (Optional but Recommended)

On GitHub repository page:
1. Click the gear icon next to "About"
2. Add topics: `flask`, `medical`, `python`, `healthcare`, `symptom-checker`, `expert-system`, `diagnosis`
3. Save changes

## 10. Verify Upload

Check that these files are visible on GitHub:
- ✅ README.md (with badges and screenshots)
- ✅ app.py
- ✅ requirements.txt
- ✅ LICENSE
- ✅ QUICKSTART.md
- ✅ CONTRIBUTING.md
- ✅ .gitignore
- ✅ templates/index.html
- ✅ static/style.css
- ✅ static/script.js
- ✅ screenshots/ (3 PNG files)
- ❌ main.py (should NOT be there)
- ❌ .idea/ (should NOT be there)
- ❌ .venv/ (should NOT be there)

## Future Updates

When making changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

## Troubleshooting

**Authentication Required:**
- Use personal access token instead of password
- Generate at: Settings → Developer settings → Personal access tokens

**Port Already in Use:**
```bash
# Kill process on port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

## Quick Command Summary

```bash
# Status check
git status

# View changes
git diff

# Add all changes
git add .

# Commit
git commit -m "Your message"

# Push
git push

# View history
git log --oneline
```

---

**Ready to upload!** 🚀

