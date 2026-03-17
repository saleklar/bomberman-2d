# GitHub Setup Instructions

Follow these steps to push your Bomberman game to GitHub:

## Step 1: Create a GitHub Account (if you don't have one)
1. Go to https://github.com
2. Click "Sign up"
3. Follow the registration steps

## Step 2: Create a New Repository on GitHub

1. Log in to GitHub
2. Click the **+** icon in the top-right corner
3. Select **New repository**
4. Fill in the details:
   - **Repository name**: `bomberman-2d`
   - **Description**: `A fun 2D Bomberman game with AI and multiplayer modes`
   - **Public** (or Private if you prefer)
   - **DO NOT** initialize with README (we already have one)
5. Click **Create repository**

## Step 3: Get Your Repository URL

After creating the repository, GitHub will show you commands. Copy your repository URL.
It should look like: `https://github.com/YOUR_USERNAME/bomberman-2d.git`

## Step 4: Add Remote and Push

Run these commands in your project directory:

```powershell
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/bomberman-2d.git

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Bomberman 2D game with AI, multiplayer, powerups, and 3-lives system"

# Push to GitHub
git branch -M main
git push -u origin main
```

### If You Already Have Commits Locally

```powershell
git remote add origin https://github.com/YOUR_USERNAME/bomberman-2d.git
git branch -M main
git push -u origin main
```

## Step 5: Add Your Game Executable as a Release

Once pushed to GitHub:

1. Build the executable locally:
   ```powershell
   .\build.ps1
   ```

2. Go to your GitHub repository page

3. Click **Releases** (on the right side)

4. Click **Create a new release**

5. Fill in:
   - **Tag**: `v1.0.0`
   - **Release title**: `Bomberman 1.0.0 - Executable`
   - **Description**: Copy from README features section
   
6. Upload `dist/Bomberman.exe` as a binary attachment

7. Click **Publish release**

## Step 6: Update GitHub Profile

In your GitHub repository settings, you can:
- Add a repository image/logo
- Set the display URL
- Add topics: `game`, `pygame`, `bomberman`, `python`

## Troubleshooting

### "fatal: remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/bomberman-2d.git
```

### "fatal: refusing to merge unrelated histories"
```powershell
git pull --allow-unrelated-histories origin main
```

### Authentication Issues
If you get authentication errors:

**Option 1: Use Personal Access Token (Recommended)**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token
3. Use token instead of password when pushing

**Option 2: Set SSH Key**
1. Generate SSH key: `ssh-keygen -t rsa -b 4096`
2. Add to GitHub: Settings → SSH and GPG keys → New SSH key
3. Update remote: `git remote set-url origin git@github.com:YOUR_USERNAME/bomberman-2d.git`

## Keeping Your Game Updated

After making changes:

```powershell
git add .
git commit -m "Your message describing the changes"
git push origin main
```

## Share Your Game

Once on GitHub, share the link:
- Direct repository: `https://github.com/YOUR_USERNAME/bomberman-2d`
- Release page (for .exe): `https://github.com/YOUR_USERNAME/bomberman-2d/releases`

## Next Steps

- Add issues for feature requests
- Invite collaborators
- Enable GitHub Pages for a project website
- Set up GitHub Actions for automated builds (advanced)

---

Happy sharing! 🎮
