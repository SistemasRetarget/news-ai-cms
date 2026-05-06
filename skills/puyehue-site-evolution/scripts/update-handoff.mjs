#!/usr/bin/env node

/**
 * update-handoff.mjs
 *
 * Auto-generates HANDOFF.md at the end of every Claude session.
 * This enables ANY model/account to pick up exactly where we left off.
 *
 * Run: node scripts/update-handoff.mjs --session-summary "What was done this session"
 * Auto-run: Called as last step of every skill execution
 */

import { execSync } from 'child_process';
import fs from 'fs/promises';

// Parse args without external deps: --key value
const args = process.argv.slice(2);
const options = {};
for (let i = 0; i < args.length; i++) {
  if (args[i].startsWith('--')) {
    const key = args[i].slice(2);
    options[key] = args[i + 1] ?? true;
    i++;
  }
}
options.output = options.output || 'HANDOFF.md';

function run(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf8' }).trim();
  } catch {
    return '';
  }
}

async function generateHandoff() {
  const now = new Date().toISOString();
  const branch = run('git branch --show-current');
  const lastCommit = run('git log -1 --format="%h %s"');
  const lastCommitDate = run('git log -1 --format="%ci"');
  const recentCommits = run('git log --oneline -5');
  const gitStatus = run('git status --short');
  const changedFiles = run('git diff --name-only HEAD~1 HEAD 2>/dev/null || git show --name-only HEAD --format="" 2>/dev/null');

  // Read current SECURE_FRAMEWORK status
  let frameworkStatus = '';
  try {
    const plan = await fs.readFile('IMPLEMENTATION_PLAN.md', 'utf8');
    const week1Match = plan.match(/WEEK 1-2.*?(?=WEEK 3|$)/s);
    frameworkStatus = week1Match ? 'IMPLEMENTATION_PLAN.md loaded' : '';
  } catch {
    frameworkStatus = 'IMPLEMENTATION_PLAN.md not found';
  }

  // List skills
  let skills = '';
  try {
    const skillDirs = await fs.readdir('skills');
    skills = skillDirs.join(', ');
  } catch {
    skills = 'No skills directory';
  }

  const handoff = `---
last_updated: ${now}
branch: ${branch}
last_commit: ${lastCommit}
model: claude-sonnet-4-6
account: sistemas@retarget.cl
---

# 🤝 HANDOFF — ESTADO ACTUAL

> Auto-generated at end of session. Read this first when resuming in any account or model.

## 📍 WHERE WE ARE

**Project:** Retarget Agency — Secure Development Framework
**Stack:** Next.js + Payload CMS + Google Cloud Run
**Focus:** Secure Framework + puyehue-site-evolution skill

---

## ✅ DONE THIS SESSION

${options.summary || 'Session summary not provided — check recent git commits below.'}

### Recent Commits
\`\`\`
${recentCommits}
\`\`\`

### Changed Files This Session
\`\`\`
${changedFiles || 'No changes detected'}
\`\`\`

---

## 🚀 IN PROGRESS

### Skills Available
\`\`\`
${skills}
\`\`\`

### Uncommitted Changes
\`\`\`
${gitStatus || 'Working tree clean'}
\`\`\`

---

## 📋 DECISIONS MADE

${options.decisions ? options.decisions.split(',').map(d => `- ${d.trim()}`).join('\n') : `- OPTION B: Use existing frameworks (not custom-built)
- Secure Framework: 6-week implementation plan
- puyehue-site-evolution: Skill with 7-step workflow
- Architecture: User → Skill (MCP) → Claude → Secure Framework → Production
- MCP: Existing skills (req-parse, wp-maintain, etc.) left as-is, will improve in Week 3-5`}

---

## ⏳ PENDING NEXT

${options.next || `1. GitHub manual configuration (30 min):
   - Enable CodeQL (Settings → Code Security)
   - Setup Dependabot
   - Enable Secret Scanning
   - Configure Branch Protection Rules
   → Reference: GITHUB_SETUP.md

2. Week 2 (May 13-19):
   - Snyk integration
   - SonarQube setup
   - Jest configuration (80%+ coverage target)

3. Script implementation (analyze-site.mjs full):
   - Visual analysis with Playwright
   - Lighthouse performance integration
   - Generate recommendations with Claude API`}

---

## 🚨 BLOCKERS

${options.blockers || `None currently. MCP working as-is (wp-maintain, req-parse, site-qa, etc.)
Note: Credentials hardcoded in wp-maintain.md — intentional, will fix in Week 3-5.`}

---

## 📚 KEY FILES TO READ

To get full context, read in this order:

\`\`\`
1. CONTEXT.md                              ← Full project context
2. IMPLEMENTATION_PLAN.md                  ← 6-week roadmap
3. SECURE_FRAMEWORK.md                     ← Framework overview
4. skills/puyehue-site-evolution/SKILL.md  ← Main skill definition
5. ARCHITECTURE_IMPLEMENTATION_PART1.md    ← What was built
6. WEEK1_PROGRESS.md                       ← Week 1 checklist
\`\`\`

---

## 🔌 TOOLS AVAILABLE (MCP)

\`\`\`
~/.claude/skills/
├─ req-parse.md       ← Parse client emails into REQs
├─ wp-maintain.md     ← Execute changes on WordPress sites
├─ site-parity.md     ← Verify site matches template
├─ site-qa.md         ← QA testing for sites
└─ clone-section.md   ← Clone sections between sites

skills/
└─ puyehue-site-evolution/
   └─ SKILL.md        ← Auto-optimize puyehue.cl (documented, scripts pending)
\`\`\`

---

## 🌍 SITES WE MANAGE

\`\`\`
parquefutangue.com   ← WordPress
puyehue.cl           ← WordPress (also Next.js migration planned)
termasaguascalientes.cl ← WordPress
news-ai-cms          ← Next.js + Payload CMS (this repo)
\`\`\`

---

## 🎯 WHERE TO CONTINUE

\`\`\`
IMMEDIATE (< 1 hour):
  → Configure GitHub security (GITHUB_SETUP.md)

THIS WEEK (Week 2):
  → Snyk + SonarQube + Jest setup (IMPLEMENTATION_PLAN.md Week 2)

NEXT SESSION:
  → Implement scripts in skills/puyehue-site-evolution/scripts/
  → Start with: analyze-site.mjs (visual + performance)
\`\`\`

---

## 💾 ACCOUNT RECOVERY

If sistemas@retarget.cl is lost, use another account and:

\`\`\`bash
git clone https://github.com/SistemasRetarget/news-ai-cms.git
git checkout retarget/peaceful-dewdney-43f0f1
# All context, docs, and code is here
\`\`\`

---

## 🔄 HOW TO RESUME

1. Read this HANDOFF.md ← You are here
2. Read CONTEXT.md for deeper context
3. Read relevant skill SKILL.md
4. Continue from "WHERE TO CONTINUE" section above

**You don't need to re-explain anything. Context is complete.**

---

*Auto-generated by update-handoff.mjs*
*${now}*
*Branch: ${branch} | Last commit: ${lastCommit}*
`;

  const outputPath = options.output || 'HANDOFF.md';
  await fs.writeFile(outputPath, handoff);
  console.log(`✅ HANDOFF.md updated: ${outputPath}`);
  console.log(`   Last updated: ${now}`);
  console.log(`   Branch: ${branch}`);
  console.log(`   Last commit: ${lastCommit}`);
}

generateHandoff().catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
