# 🚀 Quick Start: Push to GitHub

Follow these steps to push your MyNaga Dashboard to a new GitHub repository.

## Step 1: Check for Sensitive Files

**IMPORTANT:** Make sure these files are NOT committed:

```bash
# Check if .gitignore is working
cd /Users/jirehb.custodio/Python/mynaga-dashboard
git status --ignored
```

**Should be ignored:**
- ✅ `backend/credentials.json` (Google service account)
- ✅ `backend/*.db` (Database files)
- ✅ `backend/*.log` (Log files)
- ✅ `frontend/node_modules/` (Dependencies)
- ✅ `backend/__pycache__/` (Python cache)

**If you see these in `git status`, STOP!** They should be ignored.

## Step 2: Initialize Git (if not already done)

```bash
cd /Users/jirehb.custodio/Python/mynaga-dashboard

# Initialize git
git init

# Add .gitignore
git add .gitignore

# Check what will be committed
git status
```

## Step 3: Create GitHub Repository

1. **Go to GitHub:** https://github.com/new
2. **Repository name:** `mynaga-dashboard` (or your choice)
3. **Description:** "Real-time dashboard for Naga City Government - MyNaga reports management"
4. **Visibility:** 
   - ✅ **Private** (recommended for government project)
   - Or Public if you want
5. **DO NOT** initialize with README (we already have one)
6. Click **Create repository**

## Step 4: Add All Files

```bash
# Add all files (respecting .gitignore)
git add .

# Check what's being added
git status

# Review the files
git diff --cached --name-only
```

**Double-check:** Make sure NO sensitive files are listed!

## Step 5: Make First Commit

```bash
# Commit all files
git commit -m "Initial commit: MyNaga Dashboard v1.0

Features:
- Real-time dashboard with auto-sync
- Google Sheets integration
- MyNaga API integration
- Media gallery
- Case management
- Statistics and analytics"
```

## Step 6: Connect to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/mynaga-dashboard.git

# Verify remote is added
git remote -v
```

## Step 7: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

**Enter your GitHub credentials when prompted.**

## Step 8: Verify on GitHub

1. Go to: `https://github.com/YOUR_USERNAME/mynaga-dashboard`
2. Check that files are there
3. **VERIFY** these are NOT visible:
   - ❌ credentials.json
   - ❌ .env files
   - ❌ .db files
   - ❌ node_modules/

## ✅ Success Checklist

After pushing, verify:

- [ ] Repository is created on GitHub
- [ ] All code files are pushed
- [ ] README.md is displaying correctly
- [ ] .gitignore is working (no sensitive files)
- [ ] Frontend and backend folders are present
- [ ] Documentation files are included

---

## 🔐 Security Checklist

**CRITICAL:** Before making repository public:

- [ ] No Google credentials in code
- [ ] No API tokens hardcoded
- [ ] No database files committed
- [ ] No .env files committed
- [ ] All secrets use environment variables

---

## 📝 Quick Command Reference

```bash
# Navigate to project
cd /Users/jirehb.custodio/Python/mynaga-dashboard

# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your message here"

# Push changes
git push

# Pull latest changes
git pull

# View commit history
git log --oneline

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

---

## 🆘 Troubleshooting

### "Updates were rejected because the remote contains work..."

```bash
# Pull first, then push
git pull origin main --rebase
git push
```

### "Credentials.json is in the commit!"

```bash
# Remove from staging
git reset HEAD credentials.json

# Add to .gitignore if not already
echo "credentials.json" >> backend/.gitignore

# Commit again
git add .gitignore
git commit -m "Add .gitignore for credentials"
```

### "Large files preventing push"

```bash
# Check file sizes
du -sh backend/* frontend/*

# If node_modules is too large:
cd frontend
rm -rf node_modules
cd ..
git add .
git commit -m "Remove node_modules"
```

---

## 🎯 Next Steps After Pushing

1. **Add Collaborators** (if team project)
   - Go to Settings → Collaborators
   - Add team members

2. **Enable GitHub Actions** (optional)
   - Set up CI/CD for automated testing
   - Auto-deploy on push

3. **Deploy to Production**
   - Follow [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
   - Deploy frontend to Vercel
   - Deploy backend to Railway

4. **Set up Branch Protection**
   - Require pull request reviews
   - Protect main branch

---

**Ready to push? Run the commands above!** 🚀
