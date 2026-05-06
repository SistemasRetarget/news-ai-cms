# 🔐 Secrets Management Guide

**Status:** ⏳ READY FOR IMPLEMENTATION  
**Date:** 2026-05-06  
**Framework:** Google Cloud Build + Environment Variables

---

## 1. Environment Template (.env.example)

**Status:** ✅ EXISTS

The `.env.example` file is committed to GitHub with placeholder values (NO SECRETS).

**Check:** `git show HEAD:.env.example` should show only example values.

---

## 2. Secret Types & Storage

### Development Secrets (Local)
```
Location: .env.local (NOT committed to git)
Usage: npm run dev
Scope: Development only
Rotation: As needed
```

**File structure:**
```
DATABASE_URL=sqlite://./data.db
PAYLOAD_SECRET=dev-secret-key-change-in-production
NEXT_PUBLIC_GTM_ID=GTM-XXXXXXX
JWT_SECRET=dev-jwt-secret
```

### Production Secrets (Google Cloud Build)
```
Location: Cloud Build Secret Manager
Usage: Deployed container
Scope: Production only
Rotation: 90 days
```

**Secrets in Cloud Build:**
```
- DATABASE_PASSWORD: PostgreSQL password
- JWT_SECRET: JWT signing key (rotate 90 days)
- PAYLOAD_SECRET: Payload CMS secret (rotate 90 days)
- SENTRY_DSN: Error tracking token
- API_KEY_GOOGLE_ANALYTICS: GA4 API key
- STRIPE_SECRET_KEY: Stripe API key (if payments enabled)
```

---

## 3. Scanning for Hardcoded Secrets

### Automated Scanning Tools

**GitHub Secret Scanning** (automatic)
- Scans for: API keys, tokens, private keys
- Blocks: Any commits containing known secret patterns
- Action: Admin notified immediately

**Snyk Secret Detection** (configured in Week 2)
- Scans: npm dependencies for exposed secrets
- Reports: Secrets in package.json or lock files
- Action: Fails CI/CD if high/critical secrets found

**Git Hooks** (local prevention)
```bash
# Install pre-commit hook to catch secrets locally
npm run prepare
```

### Manual Verification

```bash
# Check for hardcoded secrets in codebase
grep -r "PRIVATE_KEY\|API_KEY\|SECRET\|PASSWORD" src/ | grep -v "\.example\|test\|mock"

# Check git history for accidentally committed secrets
git log --all --oneline -- ".env" | head -5

# Scan entire repo (careful - slow on large repos)
truffleHog filesystem . --max-depth 3
```

---

## 4. Cloud Build Secret Configuration

### How Cloud Build Accesses Secrets

**cloudbuild.yaml example:**
```yaml
steps:
  - name: 'gcr.io/cloud-builders/npm'
    env:
      - 'DATABASE_URL=${_DATABASE_URL}'
      - 'JWT_SECRET=${_JWT_SECRET}'
    args: ['run', 'build']

substitutions:
  _DATABASE_URL: '$$DATABASE_PASSWORD'
  _JWT_SECRET: '$$JWT_SECRET'

secretManager:
  - versionName: 'projects/$PROJECT_ID/secrets/DATABASE_PASSWORD/versions/latest'
    env: 'DATABASE_PASSWORD'
  - versionName: 'projects/$PROJECT_ID/secrets/JWT_SECRET/versions/latest'
    env: 'JWT_SECRET'
```

### Cloud Build Service Account Permissions

Ensure service account has:
```
roles/secretmanager.secretAccessor  # Read secrets
roles/logging.logWriter             # Write logs
roles/artifactregistry.writer       # Push Docker images
```

---

## 5. Secret Rotation Policy

### Rotation Schedule
```
JWT_SECRET:            Every 90 days
PAYLOAD_SECRET:        Every 90 days
API_KEYS:              Every 6 months
Database credentials:  Every year
```

### Rotation Process
1. Generate new secret in Cloud Secret Manager
2. Add new version (old version remains accessible)
3. Deploy with new version
4. Verify application still works
5. Mark old version as deprecated
6. After 30 days grace period, delete old version

---

## 6. Verification Checklist

```
[ ] .env.example exists and has NO secrets
[ ] .env.local NOT in .gitignore (explicitly excluded)
[ ] GitHub Secret Scanning enabled (Week 1)
[ ] No hardcoded secrets found by grep scan
[ ] Git history clean (no accidentally committed secrets)
[ ] Cloud Build service account has secretmanager.secretAccessor role
[ ] All production secrets in Cloud Secret Manager
[ ] Secrets accessible to Cloud Build
[ ] Test: Build succeeds with injected secrets
[ ] Test: Application reads secrets correctly
[ ] Document rotation schedule
```

---

## 7. What NOT to Do

❌ DON'T: Commit .env.local
❌ DON'T: Log secrets in error messages
❌ DON'T: Pass secrets as command-line arguments
❌ DON'T: Store secrets in Docker images
❌ DON'T: Hardcode secrets in source code
❌ DON'T: Email secrets
❌ DON'T: Share secrets in Slack/Teams
✅ DO: Use environment variables
✅ DO: Rotate secrets regularly
✅ DO: Audit secret access logs
✅ DO: Use GitHub Secret Scanning

---

## 8. Incident Response: Secret Leaked

If a secret is leaked:

1. **Immediately** (within 5 minutes)
   - Revoke the exposed secret
   - Generate a new one in Cloud Secret Manager
   - Deploy new version to production

2. **Within 30 minutes**
   - Review Cloud Audit Logs for unauthorized access
   - Check error logs for abnormal activity
   - Notify security team

3. **Within 24 hours**
   - Document root cause
   - Create follow-up task to prevent recurrence
   - Update team on incident

---

## References

- [Google Cloud Secret Manager](https://cloud.google.com/secret-manager)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [OWASP: Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

*Week 1: Friday Deliverable*  
*See IMPLEMENTATION_PLAN.md for full timeline*
