# 📊 Core Web Vitals & Performance Metrics

---

## 🎯 Core Web Vitals (Google's 2024 Standards)

### 1. LCP (Largest Contentful Paint)
**What:** Time until largest content element (image/text) is visible  
**Target:** < 2.5 seconds  
**Current (Puyehue):** 2.8s ⚠️

| Time | Rating |
|------|--------|
| < 2.5s | ✅ Good |
| 2.5-4s | ⚠️ Needs Work |
| > 4s | ❌ Poor |

**Impact on Puyehue:** Hero image (2.7MB) is main bottleneck
**Solution:** WebP compression, responsive images, lazy load

---

### 2. CLS (Cumulative Layout Shift)
**What:** Unexpected movement of page elements while loading  
**Target:** < 0.1  
**Current (Puyehue):** 0.12 ⚠️

| Score | Rating |
|-------|--------|
| < 0.1 | ✅ Good |
| 0.1-0.25 | ⚠️ Needs Work |
| > 0.25 | ❌ Poor |

**Common Causes:**
- Ads loading late (shift content down)
- Images without explicit dimensions
- Fonts loading mid-render
- Form elements appearing unexpectedly

**Puyehue Issue:** Gallery images loading without reserved space

---

### 3. FID / INP (Interaction to Next Paint)
**What:** Time from user input to visible response  
**Target:** < 100ms (FID) or < 200ms (INP)  
**Current (Puyehue):** 45ms ✅ (good)

---

## 🔍 How to Measure

### Option 1: Google Lighthouse (Free, Local)
```bash
npm install -g lighthouse
lighthouse https://puyehue.cl --view
```

**Output:** Detailed report with opportunities

### Option 2: PageSpeed Insights (Web UI)
https://pagespeed.web.dev/

**Shows:** Real-world data (CrUX) + lab data + opportunities

### Option 3: Chrome DevTools (Real Browser)
```
Open https://puyehue.cl in Chrome
→ DevTools → Performance tab
→ Record page load
→ Scroll down to see Core Web Vitals
```

---

## 📈 Benchmarking: Puyehue vs. Competitors

### Parque Futangue (parquefutangue.com)
| Metric | Futangue | Puyehue | Gap |
|--------|----------|---------|-----|
| LCP | 2.0s | 2.8s | -0.8s |
| CLS | 0.08 | 0.12 | -0.04 |
| FID | 30ms | 45ms | -15ms |
| Performance Score | 85 | 72 | -13 |

**What Futangue does better:**
- Images are compressed (WebP)
- Critical resources preloaded
- Server-side rendering optimized

---

## 💡 Optimization Strategies (Ranked by Impact)

### Quick Wins (< 1 hour, High Impact)

1. **Image Optimization** → LCP -200ms
   - Compress JPG to WebP
   - Generate responsive sizes (480, 768, 1024px)
   - Add loading="lazy" to below-fold images
   - **Estimated saving:** 70% file size

2. **Preload Critical Resources** → LCP -100ms
   - Add `<link rel="preload" href="hero.jpg">`
   - Preload Google Fonts
   - **Implementation:** 15 minutes

3. **Lazy Load Gallery** → CLS -0.02
   - Intersection Observer API
   - Reserve space with height containers
   - **Implementation:** 1 hour

### Medium Effort (1-3 hours, Medium Impact)

4. **Server-Side Caching** → FID -20ms
   - Enable HTTP/2 Server Push
   - Configure CDN caching headers
   - **Implementation:** 2 hours

5. **Code Splitting** → FID -30ms
   - Lazy load non-critical JavaScript
   - Remove unused CSS
   - **Implementation:** 2-3 hours

### Advanced (3+ hours, Diminishing Returns)

6. **Dynamic Rendering** → LCP -300ms
   - Implement ISR (Incremental Static Regeneration)
   - Pre-render critical pages
   - **Implementation:** 4-5 hours

---

## 🧮 Impact Calculation

When evaluating a recommendation:

```
Score = (Estimated LCP Improvement × 2) + 
        (CLS Improvement × 3) + 
        (Implementation Time × -1) +
        (Risk Level × -2)

Example:
- LCP improvement: -200ms = 2 points
- CLS improvement: -0.04 = 0.12 points
- Time: 30 min = -0.5 points
- Risk: Low (0) = 0 points
= 2 + 0.12 - 0.5 = 1.62 score

(Higher = better ROI)
```

---

## 📋 Validation Checklist

Before deploying any performance change:

```
[ ] LCP improved or stable (no regression)
[ ] CLS improved or stable
[ ] FID/INP improved or stable
[ ] Lighthouse score improved
[ ] No visual regression (visual diff < 2%)
[ ] Mobile performance tested
[ ] All tests passing (Jest, Lighthouse CI)
[ ] Audit log updated
```

---

## 🔗 Tools Integration

### Lighthouse CI (In Cloud Build)
```yaml
# .lighthouserc.json
{
  "ci": {
    "uploadArtifacts": true,
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.90}],
        "categories:accessibility": ["error", {"minScore": 0.95}]
      }
    }
  }
}
```

### Real User Monitoring (CrUX)
```
https://console.cloud.google.com/monitoring
→ Web Vitals dashboard
→ Track real-world performance over time
```

---

## 📚 References

- [Web.dev: Core Web Vitals](https://web.dev/vitals/)
- [Google: Page Experience Update](https://developers.google.com/search/blog/2021/04/more-on-page-experience)
- [Lighthouse Documentation](https://developers.google.com/web/tools/lighthouse)
- [WebP Format](https://developers.google.com/speed/webp)

---

*This document guides all performance optimization decisions for Puyehue.*
