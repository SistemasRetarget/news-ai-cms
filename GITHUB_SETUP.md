# 🔒 GitHub Security Setup Guide

**Date:** 2026-05-06  
**Project:** news-ai-cms  
**Repository:** https://github.com/SistemasRetarget/news-ai-cms

---

## ✅ COMPLETED: Security Headers

Content-Security-Policy, X-Frame-Options, HSTS, and other headers are configured in `next.config.mjs`.

**Verification:** `curl -I https://news-ai-cms.example.com | grep -E "X-|Content-Security|Strict-Transport"`

---

## ⏳ TODO: GitHub Configuration (Manual Steps Required)

These require GitHub UI access at https://github.com/SistemasRetarget/news-ai-cms/settings

### 1. Enable CodeQL (SAST Scanning)

**Location:** Settings → Code Security & Analysis → Code Scanning

**Steps:**
```
1. Go to Settings → Code Security & Analysis
2. Find "Code scanning"
3. Click "Set up code scanning"
4. Select "CodeQL analysis" → Configure
5. Create default workflow (use default configuration)
6. Create pull request to add .github/workflows/codeql.yml
7. Approve & merge to main
```

**Expected behavior:**
- CodeQL runs on every push to main and every PR
- Blocks merge if critical/high vulnerabilities found
- Results appear in "Security" → "Code scanning" tab

---

### 2. Enable Dependabot (Dependency Scanning)

**Location:** Settings → Code Security & Analysis → Dependabot

**Steps:**
```
1. Go to Settings → Code Security & Analysis
2. Find "Dependabot version updates"
3. Click "Enable" 
4. Create default configuration OR customize:
   - Package ecosystems: npm
   - Schedule: daily
   - Auto-merge: enabled for security updates
5. Find "Dependabot security updates"
6. Ensure this is enabled (auto-creates PRs for known vulnerabilities)
```

**Expected behavior:**
- Dependabot creates PRs automatically for:
  - Vulnerable dependencies (security)
  - Version updates (daily schedule)
- Security update PRs auto-merge if tests pass

---

### 3. Enable Secret Scanning

**Location:** Settings → Code Security & Analysis → Secret Scanning

**Steps:**
```
1. Go to Settings → Code Security & Analysis
2. Find "Secret scanning"
3. Click "Enable" for "Push protection"
4. This prevents credentials from being committed
```

**Expected behavior:**
- Any commit containing secrets (API keys, tokens) is blocked
- Admin gets alert if secret accidentally pushed
- Prevents credential leaks to GitHub

---

### 4. Configure Branch Protection Rules

**Location:** Settings → Branches → Branch Protection Rules

**Steps:**
```
1. Go to Settings → Branches
2. Click "Add rule"
3. Branch name pattern: main
4. Enable:
   ✓ Require status checks to pass before merging
   ✓ Require Code Scanning (CodeQL) to pass
   ✓ Require at least 1 approval before merging
   ✓ Dismiss stale PR approvals when new commits pushed
   ✓ Require branches to be up to date before merging
   ✓ Do not allow bypassing the above settings
5. Save
```

**Expected behavior:**
- No one (including admins) can merge to main without:
  - CodeQL passing
  - Dependabot checks passing
  - 1 code review approval
  - Branch up to date with main

---

## 📋 Verification Checklist

```
[ ] CodeQL scanning enabled and working
[ ] Dependabot version updates configured
[ ] Dependabot security updates enabled
[ ] Secret scanning with push protection enabled
[ ] Branch protection rule on main requires CodeQL + approval
[ ] Test: Create a PR with intentional security issue
    [ ] CodeQL flags the issue
    [ ] Merge is blocked
    [ ] Fix the issue
    [ ] CodeQL passes
    [ ] Merge succeeds
```

---

## 🔗 Reference

- [GitHub Code Scanning Setup](https://docs.github.com/en/code-security/code-scanning/enabling-code-scanning/configuring-code-scanning-for-a-repository)
- [GitHub Dependabot Configuration](https://docs.github.com/en/code-security/dependabot)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning/protecting-pushes-with-secret-scanning)
- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/managing-a-branch-protection-rule)

---

*Week 1: Monday-Tuesday Deliverable*  
*See IMPLEMENTATION_PLAN.md for full timeline*
