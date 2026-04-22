# Chapter 21: Git & GitHub

**Claude's Swift Reference 26** -- Part VI: The Modern Toolchain

---

## What You'll Learn

By the end of this chapter you can:

- Create a Git repository for an Xcode project and make your first commit.
- Understand the mental model behind `add`, `commit`, `branch`, and `merge`.
- Work with a remote on GitHub: clone, push, pull, and open a pull request.
- Write a sane `.gitignore` for an Xcode project.
- Tag a release and publish it on GitHub.

---

## Why Version Control

Every file in your project has a history. Without version control, you have one copy of each file and whatever Time Machine remembered last night. With Git, every saved state is a named point you can return to, compare against, or share.

Git is the version control system. GitHub is one of several places to host Git repositories on the internet. You can use Git locally without ever talking to GitHub; you start needing GitHub (or something like it) when you want to sync across machines or collaborate.

---

## The Mental Model

Git tracks three places your files can live:

1. **Working tree** -- the files you see and edit on disk.
2. **Staging area (index)** -- files you've marked as "I want these changes in the next commit."
3. **Repository** -- the stored history of past commits.

A typical change flow:

- You edit a file. It lives only in the working tree.
- `git add thefile.swift` moves that change from the working tree into the staging area.
- `git commit` moves the staged changes into the repository as a single named snapshot.

You can stage many files at once and commit them together. Each commit is a whole-project snapshot: everything tracked, at a moment in time.

---

## Creating a Repository

From the project directory in Terminal:

```bash
cd ~/Developer/MyApp
git init
git add .
git commit -m "Initial commit"
```

What just happened:

- `git init` created a hidden `.git/` folder, which is the repository.
- `git add .` staged every file in the current directory.
- `git commit` took that snapshot with the message "Initial commit."

Xcode also has a "Create Git repository" checkbox when you make a new project. Either path gets you to the same place.

---

## .gitignore for Xcode Projects

A `.gitignore` file tells Git which paths to never track. Xcode generates a lot of user-specific junk that doesn't belong in shared history. A good starting `.gitignore`:

```
# macOS
.DS_Store
.AppleDouble
.LSOverride

# Xcode -- user-specific
xcuserdata/
*.xcuserstate
*.xcscmblueprint

# Xcode -- builds
build/
DerivedData/

# Swift Package Manager
.swiftpm/
Packages/
Package.resolved

# CocoaPods / Carthage (if you use them)
Pods/
Carthage/Build/

# Secrets
*.env
*.env.local
```

Drop that at the repo root **before** the first `git add .`. Files already tracked aren't automatically untracked by adding them here; that needs `git rm --cached`.

---

## Making Commits as You Work

The everyday cycle:

```bash
# See what changed
git status

# Stage specific files
git add Sources/ContentView.swift

# Or stage everything tracked
git add -u

# Commit
git commit -m "Wire up Home tab"
```

### Good Commit Messages

- Imperative mood: "Add sidebar toggle," not "Added sidebar toggle" or "Adds sidebar toggle."
- Short subject (under ~60 chars).
- Optional body explaining **why**, not what -- the diff shows what.
- One logical change per commit. Don't mix a bug fix with a feature; make two commits.

---

## Branches

A branch is a named line of history. The default name is `main` (older repos use `master`).

```bash
# Create and switch to a new branch
git checkout -b feature/import-csv

# Do work, commit, etc.

# Switch back to main
git checkout main

# Merge the branch in
git merge feature/import-csv

# Delete the merged branch
git branch -d feature/import-csv
```

Why branch? Because a feature in progress shouldn't sit in `main` until it's done. Branches let you keep `main` shippable while experiments live off to the side.

---

## GitHub -- The Remote

GitHub is where your local repo lives on the internet. "Remote" is Git's word for "a copy of this repo somewhere else." The default remote name is `origin`.

### Create and Link a Remote Repo

On GitHub, create an empty repository (no README, no .gitignore -- let the local one be the source of truth). Copy the HTTPS or SSH URL.

```bash
git remote add origin https://github.com/yourname/MyApp.git
git branch -M main
git push -u origin main
```

- `git remote add` registers the URL under the name `origin`.
- `git branch -M main` renames the current branch to `main` (in case your local default is different).
- `git push -u origin main` uploads the `main` branch and remembers the association (`-u` = "upstream").

### Everyday Push / Pull

```bash
# Grab the latest from GitHub (when someone else committed)
git pull

# Push your commits
git push
```

---

## Pull Requests

A pull request (PR) is GitHub's way of saying "I'd like my branch merged into yours; here's the diff, please review."

Typical flow:

1. Create a branch locally and push it to GitHub.
   ```bash
   git checkout -b feature/export-pdf
   # ... commits ...
   git push -u origin feature/export-pdf
   ```
2. On GitHub, click "Compare & pull request."
3. Fill in the title and description. Link related issues.
4. Reviewers comment. You push follow-up commits to the same branch; the PR updates automatically.
5. Merge when approved.

For a solo-developer repo, PRs are still useful: they force you to look at the full diff before merging, which catches things you wouldn't see in individual commits.

---

## Tags and Releases

Tags are named pointers to a specific commit. You use them to mark releases.

```bash
git tag v1.0.0
git push origin v1.0.0
```

On GitHub, navigate to Releases and cut a release from the tag. You can attach a built `.ipa` or `.app` binary, write release notes, and mark it prerelease or production.

Version tags usually follow **semantic versioning**: `MAJOR.MINOR.PATCH`. Bump MAJOR for breaking changes, MINOR for new features, PATCH for bug fixes.

---

## Undoing Things

### Undo Uncommitted Changes to a File

```bash
git checkout -- Sources/ContentView.swift
```

Resets that file to whatever was last committed. Be careful -- this loses your working changes.

### Undo a Commit You Haven't Pushed

```bash
git reset --soft HEAD~1
```

Moves `HEAD` back one commit but keeps the changes staged. You can fix them and recommit.

### Undo a Pushed Commit

```bash
git revert <commit-sha>
```

Creates a new commit that undoes the old one. Safe because history stays linear; nobody has to rebase their work.

Never use `git push --force` on a shared branch. It rewrites history and breaks everybody else's clone.

---

## The Xcode Source Control Integration

Xcode has a Source Control menu that does the common Git operations through GUI. You can:

- View history per file with **Source Control > History**.
- Compare working changes against the last commit via the Changes tab in the navigator.
- Commit from **Source Control > Commit** (`⌥⌘C`).
- Push and pull from **Source Control > Push / Pull**.

The GUI is fine for day-to-day work. Drop to Terminal for anything unusual -- interactive rebases, surgical resets, tag management. The CLI is more powerful; the GUI is faster for the common case.

---

## Chapter Mini-Example -- First Push to GitHub

Walk through exactly what to type the first time you put a new Xcode project on GitHub.

```bash
# 1. Go to the project
cd ~/Developer/MyApp

# 2. (If Xcode didn't already) initialize Git
git init

# 3. Drop a .gitignore at the repo root (paste the template from earlier)
# 4. Check what Git sees
git status

# 5. Stage everything
git add .

# 6. First commit
git commit -m "Initial commit"

# 7. On GitHub: create an empty repo named MyApp, copy its URL.
# 8. Wire up the remote (HTTPS example)
git remote add origin https://github.com/yourname/MyApp.git
git branch -M main

# 9. First push
git push -u origin main
```

Refresh the GitHub repo page. Your code is up. Every future commit is one `git push` away from being backed up.

---

## What Book 22 Does

You've got your code under version control and safely stored. Book 22 turns the lens outward: how to integrate an AI chatbot into your own app, using the Anthropic Claude API from Swift.
