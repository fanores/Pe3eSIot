---
name: commit-message
description: Generate a git commit message — title (what was done) and body (why it was done) — from current git changes
allowed-tools: [Bash]
---

Generate a commit message for the current git changes in this repository.

Use the Bash tool to gather context:
1. `git status` — which files changed
2. `git diff HEAD` — full diff of all changes (staged + unstaged)
3. `git log --oneline -8` — recent commits to match project style

Then write a two-part commit message:

**Title** — one line, imperative mood ("Add", "Fix", "Remove", …), describes *what* changed, ≤72 characters.

**Body** — one or more sentences explaining *why* the change was made: the problem it solves, the motivation behind it, or the goal it achieves. Do not restate the diff; focus on intent.

Output the commit message exactly in this format (blank line between title and body), with no surrounding explanation:

<title>

<body>
