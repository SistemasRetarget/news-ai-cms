# 🚀 Puyehue Site Evolution Skill

Auto-optimize puyehue.cl for visual appeal & performance using Claude AI, with secure deployment and learning loops.

---

## 📁 Project Structure

```
puyehue-site-evolution/
├── SKILL.md                          ← Main skill definition (what Claude executes)
├── README.md                         ← This file
├── scripts/                          ← Executable tools
│   ├── analyze-site.mjs              ← Visual + performance analysis
│   ├── generate-recommendations.mjs  ← Claude integration (future)
│   ├── deploy.mjs                    ← Cloud Build deployment
│   └── validate-changes.mjs          ← Visual diff + regression testing
└── references/                       ← Knowledge & guides
    ├── performance-metrics.md        ← Core Web Vitals, benchmarks
    ├── builder-io-integration.md     ← Auto-admin setup (Phase 2)
    └── knowledge-base.md             ← What we've learned about Puyehue
```

---

## 🚀 Quick Start

### For Claude (Invoking the Skill)

```
User: "optimize puyehue performance"
↓
Claude loads this SKILL.md
Claude executes steps from SKILL.md
Claude runs scripts/analyze-site.mjs
Claude calls itself to generate recommendations
Claude deploys & validates
```

### For Developers (Extending the Skill)

#### 1. Add a New Analysis
```bash
# Create new script
touch scripts/my-analysis.mjs

# Implement analysis logic
# Export JSON output

# Update SKILL.md to call it
```

#### 2. Add a New Reference
```bash
# Create new doc
touch references/my-reference.md

# Link from SKILL.md
```

#### 3. Test Locally
```bash
# Analyze site without deploying
node scripts/analyze-site.mjs --url https://puyehue.cl --mode visual

# Review output
cat evidence/analysis.json
```

---

## 📊 How It Works

### Phase 1: Analysis (Week 2-3)
```
Input: URL + optimization type
↓
Script: analyze-site.mjs
  - Visual audit (images, colors, typography)
  - Performance metrics (Lighthouse)
  - Content structure (for Builder.io)
↓
Output: JSON analysis
```

### Phase 2: Recommendations (Week 2-3)
```
Input: Analysis JSON + knowledge base
↓
Claude: Generate 3 ranked recommendations
  - Specific change description
  - Impact estimate (LCP, CLS, conversion)
  - Time & risk assessment
  - Confidence score
↓
Output: Structured recommendations
```

### Phase 3: Validation (Week 3-4)
```
Input: Selected recommendation
↓
Deploy to staging:
  - Create branch + PR
  - Run tests (Jest, CodeQL, Lighthouse)
  - Visual diff (before vs. after)
↓
Output: Pass/fail + metrics
```

### Phase 4: Production Deployment (Week 3-4)
```
If validation passes:
  → Deploy to production
  → Monitor real-world performance
  → Log results to knowledge base
  
If validation fails:
  → Revert staging changes
  → Ask Claude for alternative
```

### Phase 5: Learning (Ongoing)
```
After each deployment:
  → Capture actual impact vs. predicted
  → Store in knowledge-base.md
  → Claude learns for next recommendation
```

---

## 🔧 Development Roadmap

### ✅ COMPLETED (Week 1)
- [x] Skill documentation (SKILL.md)
- [x] Performance reference guide
- [x] Builder.io integration guide
- [x] Knowledge base template

### ⏳ IN PROGRESS (Week 2-3)
- [ ] Implement analyze-site.mjs (visual + performance)
- [ ] Implement generate-recommendations.mjs (Claude integration)
- [ ] Setup Cloud Build integration
- [ ] Create test fixtures (mock site data)

### 📅 PLANNED (Week 3-4)
- [ ] Implement deploy.mjs
- [ ] Implement validate-changes.mjs (visual diff)
- [ ] A/B testing framework
- [ ] Webhook integration

### 🚀 FUTURE (Week 4+)
- [ ] Builder.io integration (auto-admin)
- [ ] ML-based learning from A/B tests
- [ ] Prompt engineering optimization
- [ ] Score models for auto-ranking recommendations

---

## 🧪 Testing

### Manual Testing
```bash
# Analyze current state
node scripts/analyze-site.mjs \
  --url https://puyehue.cl \
  --mode visual \
  --output evidence/analysis.json

# Review output
cat evidence/analysis.json | jq .issues
```

### Integration Testing
```bash
# Test full workflow (when scripts are complete)
npm test -- scripts/analyze-site.test.mjs
npm test -- scripts/deploy.test.mjs
```

### Real-World Testing (Staging)
```bash
# Deploy to staging environment
node scripts/deploy.mjs \
  --environment staging \
  --branch feat/image-optimization

# Measure actual impact
curl https://staging-puyehue.cl/api/metrics
```

---

## 📝 Development Notes

### Script Dependencies

Each script needs:
```javascript
import { CLI } from 'commander';
import { readFile, writeFile } from 'fs/promises';
import path from 'path';

// Parse CLI args
// Execute logic
// Output JSON
// Log results to console
```

### Output Format

All scripts output JSON:
```json
{
  "timestamp": "ISO8601",
  "status": "success|error",
  "data": {...},
  "metadata": {
    "execution_time_ms": 1234,
    "version": "1.0"
  }
}
```

### Error Handling

```javascript
try {
  // Main logic
} catch (error) {
  console.error('❌ Error:', error.message);
  process.exit(1);
}
```

---

## 🔐 Security Checklist

When extending this skill:

- [ ] No hardcoded credentials (use Cloud Secret Manager)
- [ ] All outputs validated before deployment
- [ ] Changes tested before going to production
- [ ] Audit logging captures who/what/when
- [ ] Visual diffs reviewed before approval
- [ ] Rollback procedures documented
- [ ] Secrets never logged to console

---

## 📚 References

- **[SKILL.md](SKILL.md)** — Main skill definition for Claude
- **[performance-metrics.md](references/performance-metrics.md)** — Core Web Vitals guide & benchmarks
- **[builder-io-integration.md](references/builder-io-integration.md)** — Auto-admin setup guide
- **[knowledge-base.md](references/knowledge-base.md)** — Learnings & what works for Puyehue
- **[SECURE_FRAMEWORK.md](../../../SECURE_FRAMEWORK.md)** — Parent framework (GitHub, testing, compliance)
- **[IMPLEMENTATION_PLAN.md](../../../IMPLEMENTATION_PLAN.md)** — 6-week roadmap

---

## 🤝 Contributing

### Adding a New Recommendation Template
1. Create reference doc in `references/`
2. Add to knowledge-base.md
3. Update SKILL.md to reference it

### Improving Existing Scripts
1. Update script with better logic
2. Add tests
3. Update README with new capabilities

### Reporting Issues
- Document in knowledge-base.md under "Anti-patterns"
- Explain why it failed
- Suggest alternative approach

---

## 📞 Support

- Questions about SKILL.md? → Read SKILL.md
- Performance metrics unclear? → See references/performance-metrics.md
- How to setup Builder.io? → See references/builder-io-integration.md
- What's been tried before? → See references/knowledge-base.md
- Full roadmap? → See IMPLEMENTATION_PLAN.md

---

## 📊 Status

- **Created:** 2026-05-06
- **Phase:** 1 (Documentation & Design)
- **Next:** Phase 2 (Implementation of scripts)
- **Expected:** Phase 5 complete by 2026-06-17

---

*Part of Retarget's Secure Development Framework*  
*Reusable for all client site evolution*  
*Integrates with news-ai-cms platform*
