---
name: puyehue-site-evolution
description: Auto-optimize puyehue.cl visually and for performance. Analyzes design, Core Web Vitals, and auto-admin setup. Validates changes before deployment and learns from results. Use this whenever the user mentions Puyehue site improvements, performance issues, visual updates, or auto-administration setup.
compatibility: Requires access to Google Cloud, GitHub, BigQuery, Builder.io API (Phase 2)
---

# 🚀 Puyehue Site Evolution Skill

**Input:** URL (puyehue.cl) + optimization type (visual/performance/admin)  
**Output:** Optimized site + validation evidence + recommendations

---

## 📋 WHAT THIS SKILL DOES

1. **Analyzes** the current site (visual audit, performance metrics)
2. **Recommends** specific improvements (scores each by impact)
3. **Validates** changes before deployment (visual diff + performance comparison)
4. **Auto-deploys** if quality checks pass
5. **Learns** from results (captures what worked, what didn't)

---

## 🎯 THREE MODES

### Mode 1: Visual Optimization
```
User: "puyehue images look pixelated"
↓
Skill: Analyze images, compare with competitors
       Propose: compression, CDN strategy, responsive sizes
       Generate visual mockup showing improvement
       Deploy with validation
```

### Mode 2: Performance Optimization
```
User: "Core Web Vitals are bad"
↓
Skill: Fetch Core Web Vitals data
       Identify bottleneck (LCP? CLS? FID?)
       Propose: lazy load, image optimization, caching
       A/B test improvement
       Deploy if metrics improve
```

### Mode 3: Auto-Administration Setup
```
User: "Client needs to edit without code"
↓
Skill: Analyze content structure
       Prepare Builder.io blocks
       Configure content schemas
       Train client on visual editor
```

---

## 🔄 COMPLETE WORKFLOW

### STEP 1: INTAKE
```
User provides:
✓ Site URL (https://puyehue.cl)
✓ What to optimize (visual/performance/admin)
✓ Success metric (CLS < 0.1, LCP < 2.5s, etc.)

Skill extracts:
✓ Current Core Web Vitals (from CrUX or Lighthouse)
✓ Visual state (screenshot)
✓ Performance profile (Lighthouse audit)
✓ Content structure (for auto-admin mapping)
```

### STEP 2: ANALYSIS

#### Visual Analysis (VISUAL_AUDIT)
```bash
# 1. Screenshot current state
node scripts/analyze-site.mjs \
  --url "https://puyehue.cl" \
  --mode visual \
  --output evidence/visual-audit.json

# Output:
{
  "images": [
    {"src": "hero.jpg", "size": 2.7, "format": "jpg", "potential_saving": "60%"},
    {"src": "gallery.jpg", "size": 1.8, "format": "jpg", "potential_saving": "50%"}
  ],
  "colors": ["#1a3a3a", "#ffffff", "#d4a574"],
  "typography": ["Inter", "Playfair Display"],
  "issues": ["Images not optimized", "No WebP fallback", "Mobile responsiveness gap"]
}
```

#### Performance Analysis (LIGHTHOUSE)
```bash
node scripts/analyze-site.mjs \
  --url "https://puyehue.cl" \
  --mode performance \
  --output evidence/lighthouse.json

# Output:
{
  "core_web_vitals": {
    "lcp": 2.8,        # Largest Contentful Paint (target < 2.5)
    "cls": 0.12,       # Cumulative Layout Shift (target < 0.1)
    "fid": 45          # First Input Delay (target < 100)
  },
  "score": 72,
  "opportunities": [
    "Image optimization: potential LCP -200ms",
    "Lazy load below-the-fold: potential LCP -150ms",
    "Remove unused CSS: potential FID -20ms"
  ]
}
```

### STEP 3: CLAUDE ANALYSIS & RECOMMENDATIONS

Skill feeds analysis to Claude:
```
Given these metrics + visual audit + competitor analysis,
generate 3 prioritized recommendations:
- Specific change description
- Estimated impact on Core Web Vitals
- Estimated time to implement
- Risk level (low/medium/high)
- Confidence score (1-10)
```

Claude Response Format:
```
## Recommendation 1: Image Optimization [CONFIDENCE: 9/10]
**Change:** Compress hero.jpg to WebP + generate responsive sizes
**Impact:** LCP: 2.8s → 2.1s (-250ms) | CLS: unaffected
**Time:** 30 minutes (using ImageOptim + Cloudinary)
**Risk:** Low (tested, no visual degradation)
**Why:** 2.7MB JPG on hero is blocking render. WebP + responsive saves 70%.

## Recommendation 2: Lazy Load Gallery [CONFIDENCE: 8/10]
**Change:** Intersection Observer API for below-the-fold images
**Impact:** LCP: unaffected | FID: 45ms → 30ms (-15ms)
**Time:** 1 hour
**Risk:** Low (standard pattern)

## Recommendation 3: Preload Critical Resources [CONFIDENCE: 7/10]
**Change:** Add <link rel="preload"> for hero image + fonts
**Impact:** LCP: 2.1s → 1.8s (-300ms)
**Time:** 15 minutes
**Risk:** Low
```

### STEP 4: IMPLEMENTATION

For each recommendation:

```bash
# 4a. Create PR with changes
node scripts/generate-changes.mjs \
  --recommendation "image-optimization" \
  --branch "feat/optimize-images-puyehue" \
  --output evidence/changes.json

# 4b. Build & test locally
npm run build
npm test -- --coverage

# 4c. Deploy to staging
node scripts/deploy.mjs \
  --environment staging \
  --branch "feat/optimize-images-puyehue"
```

### STEP 5: VALIDATION

Before deploying to production:

```bash
# 5a. Visual diff (before vs. after)
node /Users/spam11/github/MCP/tools/visual-diff.mjs \
  evidence/visual-audit/before.png \
  evidence/visual-audit/after.png \
  evidence/visual-audit/diff.png \
  2.0

# 5b. Performance regression test
node scripts/validate-changes.mjs \
  --staging-url "https://staging-puyehue.cl" \
  --metric "core_web_vitals" \
  --threshold "no_regression"

# 5c. Run E2E tests (via MCP: site-qa)
# Uses existing skill: /site-qa
```

### STEP 6: DECISION

```
✓ If visual diff < 2% AND metrics improved AND tests pass
  → Auto-deploy to production
  → Register in audit log
  → Capture learning

✗ If anything failed
  → Revert staging deployment
  → Report issues to Claude
  → Ask for alternative recommendation
```

### STEP 7: LEARNING & FEEDBACK

```bash
# Capture what worked
node scripts/capture-learning.mjs \
  --recommendation "image-optimization" \
  --result "success" \
  --impact_actual "LCP: 2.8s → 2.0s" \
  --time_actual "25 minutes" \
  --notes "Compression to WebP + responsive sizes was most effective"

# Output saved to knowledge-base.md for future optimizations
```

---

## 🛠️ REQUIRED SCRIPTS

### 1. analyze-site.mjs
```javascript
// Usage: node scripts/analyze-site.mjs --url [URL] --mode [visual|performance]
// Outputs: JSON with metrics, images, performance data
// Dependencies: Playwright (screenshots), Lighthouse API
```

### 2. generate-recommendations.mjs
```javascript
// Takes analysis + calls Claude API
// Returns structured recommendations with impact scores
```

### 3. deploy.mjs
```javascript
// Deploys to staging/production via Cloud Build
// Integrates with news-ai-cms CI/CD pipeline
// Waits for all checks (CodeQL, tests, Lighthouse)
```

### 4. validate-changes.mjs
```javascript
// Runs visual diff, performance comparison
// Returns pass/fail + metrics
```

### 5. capture-learning.mjs
```javascript
// Logs results to knowledge-base for ML training
// Updates "what works for Puyehue" knowledge base
```

---

## 📚 REFERENCES (See /references/)

- **[performance-metrics.md](references/performance-metrics.md)** — Core Web Vitals targets, tooling, interpretation
- **[builder-io-integration.md](references/builder-io-integration.md)** — Auto-admin setup (Phase 2)
- **[knowledge-base.md](references/knowledge-base.md)** — What we've learned about Puyehue, what works, what doesn't
- **[competitor-analysis.md](references/competitor-analysis.md)** — Benchmark against similar sites (Parque Futangue, Termas Aguas Calientes)

---

## 🔐 SECURITY & COMPLIANCE

This skill follows **Secure Development Framework**:

- ✅ Changes submitted as PRs (not direct commits)
- ✅ CodeQL scanning before merge
- ✅ Test coverage > 80%
- ✅ Visual validation before deployment
- ✅ Immutable audit log of all changes
- ✅ Automatic rollback if performance degrades

See `SECURE_FRAMEWORK.md` for full compliance checklist.

---

## 🎯 CURRENT STATUS

- ✅ Visual analysis framework (screenshots, comparison)
- ✅ Performance analysis (Lighthouse integration)
- ✅ Claude recommendation engine (ready)
- ⏳ Auto-deployment (Week 2: integrate with Cloud Build)
- ⏳ A/B testing validation (Week 3)
- ⏳ Builder.io integration (Week 4)
- ⏳ Knowledge base ML (Week 5+)

---

## 🚀 INVOKE THIS SKILL WHEN:

- "Optimize puyehue performance"
- "Images look bad on puyehue"
- "Client needs to edit puyehue content"
- "Compare puyehue with competitors"
- "What's working/not working on puyehue?"
- "Set up auto-admin for puyehue"

---

## 📞 QUICK START

```bash
# Analyze current state
/puyehue-optimize --analyze-only

# Get recommendations
/puyehue-optimize --recommend

# Implement + validate best recommendation
/puyehue-optimize --implement --validate

# Deploy to production
/puyehue-optimize --deploy

# Check learning history
/puyehue-optimize --knowledge
```

---

*Part of Retarget's Secure Development Framework*  
*Reusable template for all client site evolution*  
*See IMPLEMENTATION_PLAN.md for development timeline*
