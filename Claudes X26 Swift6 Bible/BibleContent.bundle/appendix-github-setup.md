# Appendix: Setting Up GitHub and Connecting It to Xcode

*Claude's Xcode 26 Swift Reference — Prerequisite Setup*

---

This appendix gets you set up with GitHub and connected to Xcode before you write a single line of code. Every app appendix in this book assumes this is already done. Do this once and you never think about it again.

If you already have a GitHub account connected to Xcode, skip this appendix. Otherwise, follow along — it takes about ten minutes.

---

## 1. What GitHub Is

1.1 GitHub is where your code lives online. Think of it as a backup drive that also tracks every change you ever make. You save a version, it remembers it. You break something next Tuesday, you roll back to last Tuesday. That's it.

1.2 The free account does everything you need. Unlimited public repositories, unlimited private repositories. You're not hitting a paywall here.

1.3 One thing that trips people up: **Git** and **GitHub** are not the same thing. Git is the tool — it runs on your Mac, inside Xcode, tracking changes locally. GitHub is the website that hosts your Git repositories online. Git is the engine. GitHub is the parking garage. Xcode talks to both.

---

## 2. Creating a GitHub Account

2.1 Open a browser and go to **github.com**. Click **Sign up** in the top-right corner.

2.2 GitHub walks you through it:

- **Email:** Use whatever email you check regularly. This is where verification and notifications go.
- **Password:** Pick something strong. You know the drill.
- **Username:** This one matters. Your username becomes part of every repository URL you create — `github.com/yourname/YourApp`. Pick something professional. If you're building a portfolio, this is what people see.

2.3 Pick the **Free** plan. That's the one you want. The paid tiers are for teams and enterprises — you don't need them.

2.4 GitHub sends a verification email. Open it, click the link. You're in.

2.5 Your profile lives at `github.com/yourname`. Every repository you create shows up there. When you publish an app and someone asks "where's the source code?" — you point them here.

**[Fig. GS.1 — GitHub signup page]**

---

## 3. Creating a Personal Access Token

3.1 GitHub doesn't let you sign in from Xcode with just your password. You need a **personal access token** — a long generated string that acts as your password. It's like an API key. GitHub uses it to verify that Xcode is authorized to push code to your account.

3.2 Here's the path. It's buried in settings, so follow exactly:

1. Click your **avatar** (top-right corner of any GitHub page)
2. Click **Settings**
3. Scroll down the left sidebar to **Developer settings** (very bottom)
4. Click **Personal access tokens**
5. Click **Tokens (classic)**
6. Click **Generate new token** > **Generate new token (classic)**

3.3 Fill it in:

- **Note:** Give it a name like `Xcode` so you remember what it's for six months from now.
- **Expiration:** 90 days is reasonable. Or pick **No expiration** if you don't want to deal with regenerating it. Your call. No expiration is less hassle; 90 days is more secure.
- **Scopes:** Check these two boxes:
  - `repo` — Full control of private repositories. This is the one that matters. Without it, Xcode can't push code.
  - `workflow` — Optional, but check it if you ever plan to use GitHub Actions for automated builds or testing.

3.4 Click **Generate token** at the bottom.

**[Fig. GS.2 — Personal access token settings: scopes selected]**

3.5 GitHub shows you the token exactly once. It's a long string starting with `ghp_`. **Copy it now.** Right now. Not in a minute. Now.

3.6 If you navigate away without copying it, that token is gone. You can't retrieve it. You'd have to generate a new one. So copy it and save it somewhere safe — Notes app, password manager, a text file you won't delete. Whatever works for you, just don't lose it.

**[Fig. GS.3 — Generated token displayed (copy it immediately)]**

---

## 4. Adding GitHub to Xcode

4.1 Open Xcode. Go to **Settings** (Cmd+Comma, or **Xcode > Settings** from the menu bar). Click the **Accounts** tab.

4.2 Click the **+** button in the bottom-left corner. A dropdown appears with account types — Apple ID, GitHub, GitHub Enterprise, Bitbucket Cloud, Bitbucket Server. Pick **GitHub**.

**[Fig. GS.4 — Xcode Settings > Accounts: empty, before adding GitHub]**

4.3 Xcode asks for two things:

- **Account:** Your GitHub username (the one you picked in section 2.2).
- **Token:** Paste the personal access token you copied in section 3.5.

4.4 Click **Sign In**.

4.5 Your GitHub account appears in the accounts list. You'll see your username with a GitHub icon next to it. If everything worked, there's no error message — just your account sitting there, connected and ready.

**[Fig. GS.5 — Xcode Settings > Accounts: GitHub account added with green checkmark]**

---

## 5. Verifying the Connection

5.1 Still in **Xcode > Settings > Accounts**, click on your GitHub account in the list. The right side shows your account details — your username, the server (github.com), and your repositories.

5.2 If you just created your GitHub account, the repository list will be empty. That's normal. Once you start creating projects and pushing them, they show up here.

5.3 If you see a red error instead of your account details, check two things:

- **Token scopes:** Go back to GitHub (section 3.2) and verify your token has the `repo` scope checked. If it doesn't, generate a new token with the right scopes.
- **Token expiration:** If your token expired, you'll need to generate a fresh one and update it in Xcode. Delete the old account entry (select it, click the **-** button), then add it again with the new token.

5.4 Close Settings. You're done with setup.

---

## 6. What You Just Set Up

6.1 Your code has an online backup from day one. Every project you create in Xcode can push to GitHub with a couple of clicks. No FTP, no manual file copying, no emailing zip files to yourself. You commit, you push, it's up there.

6.2 Every change is tracked. Git records what you changed, when you changed it, and what it looked like before. If you delete a function on Wednesday and need it back on Friday, it's still there in the history. This isn't theoretical — you will use this, and you'll be glad it was running the whole time.

6.3 If the repository is public, other people can see your code. That's how you build a portfolio. When you apply for a gig or want to show someone what you can do, you hand them a GitHub link. The code speaks for itself.

6.4 This is a one-time setup. You won't touch these settings again unless you switch to a new Mac or your token expires. Every app you build from here on out — Claude's Web Wrapper (Wraply), Tally Matrix, whatever comes next — uses this same connection.

---

Now you're ready to start building. Turn to the next appendix and create your first app.

---

*Claude's Xcode 26 Swift Reference*
*License: GPL v3 — Share and share alike with attribution required.*
