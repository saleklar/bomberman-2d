# 🚀 GitHub Setup Instructions

Your Bomberman 2D game is ready to be pushed to GitHub! Follow these steps:

## Step 1: Create a New Repository on GitHub

1. Go to [GitHub](https://github.com) and log in
2. Click the **+** icon in the top right corner
3. Select **New repository**
4. Fill in the details:
   - **Repository name:** `bomberman-2d`
   - **Description:** "2D Bomberman game with AI, multiplayer, and powerups"
   - **Visibility:** Public (or Private if you prefer)
   - **Do NOT initialize with README** (we already have one)
   - Click **Create repository**

## Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Copy and run these in PowerShell:

```powershell
cd "E:\VIBE_PROJECTS\bomberman test\bomberman_2d"

git remote add origin https://github.com/YOUR_USERNAME/bomberman-2d.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

## Step 3: Configure Git (if not done before)

If this is your first time using git, configure your identity:

```powershell
git config --global user.email "your.email@example.com"
git config --global user.name "Your Name"
```

## Step 4: Push the Code

Run the commands from Step 2 in PowerShell.

## Step 5: Verify

Go to your GitHub repository URL:
```
https://github.com/YOUR_USERNAME/bomberman-2d
```

You should see all your files there!

## Future Updates

To push future changes:

```powershell
cd "E:\VIBE_PROJECTS\bomberman test\bomberman_2d"
git add .
git commit -m "Your commit message here"
git push
```

## Useful Commands

```powershell
# Check status
git status

# View commit history
git log

# View remote URLs
git remote -v

# Create a new branch
git checkout -b feature/name

# Switch branch
git checkout main
```

## Share with Others

Once pushed to GitHub, others can clone your repository with:

```bash
git clone https://github.com/YOUR_USERNAME/bomberman-2d.git
cd bomberman-2d/bomberman_2d
pip install pygame
python main.py
```

---

Happy coding! 🎮
