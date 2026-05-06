# 🏗️ Builder.io Integration (Phase 2)

**Status:** ⏳ Planned for Week 4  
**Complexity:** Medium  
**Goal:** Enable client to edit Puyehue without code

---

## 📌 What is Builder.io?

Builder.io is a **visual page builder** (like Figma for web):
- Drag-and-drop content editor
- Visual block builder (no code)
- Real-time preview
- Auto-sync with Git/CMS
- API-first architecture

**For Puyehue:** Client can edit hero text, prices, images directly without touching code.

---

## 🎯 Architecture

```
Builder.io Admin UI (Client edits here)
        ↓
Builder.io API
        ↓
Next.js (news-ai-cms)
        ↓
Rendered Page (puyehue.cl)
```

**Flow:**
1. Client logs into Builder.io dashboard
2. Edits content (hero title, price, gallery images)
3. Builder sends changes via API
4. Next.js fetches from Builder API
5. Page re-renders with new content

---

## 🚀 Implementation Steps (Week 4)

### STEP 1: Setup Builder.io Account
```
1. Create account at builder.io
2. Create new project "Puyehue"
3. Generate API key (builder.io settings → API keys)
4. Add to Cloud Secret Manager:
   - BUILDER_IO_API_KEY
   - BUILDER_IO_API_KEY_PRIVATE
```

### STEP 2: Map Content Blocks

Identify which sections are editable:

```
Hero Section
  ├─ Title (text)
  ├─ Subtitle (text)
  └─ Background Image (image)

Pricing Section
  ├─ Package 1 (card)
  │  ├─ Name (text)
  │  ├─ Price (number)
  │  └─ Features (list)
  ├─ Package 2 (card)
  └─ Package 3 (card)

Gallery
  ├─ Image 1 (image + caption)
  ├─ Image 2 (image + caption)
  └─ ... (dynamic)

About Section
  ├─ Title (text)
  └─ Description (rich text)
```

### STEP 3: Create Builder.io Models

```json
{
  "name": "puyehue_page",
  "fields": [
    {
      "name": "hero_title",
      "type": "text",
      "required": true
    },
    {
      "name": "hero_subtitle",
      "type": "text"
    },
    {
      "name": "hero_image",
      "type": "image"
    },
    {
      "name": "packages",
      "type": "list",
      "subFields": [
        {"name": "name", "type": "text"},
        {"name": "price", "type": "number"},
        {"name": "features", "type": "list"}
      ]
    }
  ]
}
```

### STEP 4: Fetch Content in Next.js

```typescript
// pages/index.tsx
import { getContent } from '@builder.io/sdk';

export async function getStaticProps() {
  const content = await getContent({
    model: 'puyehue_page',
    apiKey: process.env.BUILDER_IO_API_KEY,
    options: {
      cacheSeconds: 3600 // Cache 1 hour
    }
  });

  return {
    props: { content },
    revalidate: 3600 // ISR: revalidate every hour
  };
}

export default function Home({ content }) {
  return (
    <>
      <Hero
        title={content.hero_title}
        subtitle={content.hero_subtitle}
        image={content.hero_image}
      />
      <Pricing packages={content.packages} />
    </>
  );
}
```

### STEP 5: Setup Webhooks

When client edits in Builder.io, notify Next.js:

```json
{
  "url": "https://puyehue.cl/api/builder-webhook",
  "events": ["content.updated"],
  "secret": "webhook-secret"
}
```

Handler in Next.js:
```typescript
// pages/api/builder-webhook.ts
export async function POST(req) {
  const signature = req.headers['x-builder-signature'];
  
  // Verify webhook signature
  if (!verifySignature(signature, req.body)) {
    return { error: 'Unauthorized' };
  }

  // Trigger ISR revalidation
  await res.revalidate('/');
  
  return { revalidated: true };
}
```

---

## 🔒 Security Considerations

### 1. API Key Protection
```
- Store in Cloud Secret Manager
- Never commit to GitHub
- Rotate API keys every 90 days
```

### 2. Webhook Signature Verification
```
- Builder.io signs each webhook with secret
- Always verify before processing
- Reject unverified webhooks
```

### 3. Content Validation
```typescript
// Validate that edits comply with brand guidelines
function validateContent(content) {
  // Title length < 100 chars
  if (content.hero_title.length > 100) {
    throw new Error('Title too long');
  }
  
  // Price must be positive number
  if (content.price < 0) {
    throw new Error('Invalid price');
  }
  
  // Image must be HTTPS
  if (!content.image.startsWith('https')) {
    throw new Error('Images must be HTTPS');
  }
}
```

### 4. Audit Logging
```
Every edit logged:
- Who: username@email.com
- What: Changed hero_title from "X" to "Y"
- When: 2026-05-06 14:30:00 UTC
- Status: Success / Failed
```

---

## 📋 Client Training (Week 4)

When Builder.io is live, client needs training:

**Session 1: Basics (30 min)**
- Log into Builder.io dashboard
- Edit text (title, subtitle)
- Change images
- Save & preview

**Session 2: Advanced (1 hour)**
- Manage pricing cards
- Add/remove packages
- Upload images
- Test on mobile

**Materials:**
- Video walkthrough
- Quick reference PDF
- Email support process

---

## 🧪 Testing Checklist (Week 4)

```
[ ] API key securely stored in Cloud Secret Manager
[ ] Content fetches correctly from Builder.io
[ ] Images display at correct sizes
[ ] Mobile responsive layout works
[ ] Webhook updates trigger ISR revalidation
[ ] Performance doesn't degrade (Lighthouse > 90)
[ ] Audit logging captures all edits
[ ] Client can edit and see changes in 10 seconds
[ ] Rollback works if edit is bad
[ ] Secure: API key never exposed in browser
```

---

## 🔄 Content Sync with Git

Optional: Keep Git history of content edits

```bash
# Scheduled job (daily at 2am)
node scripts/sync-builder-to-git.mjs

# Downloads current content from Builder.io
# Commits to git as: "content: update via Builder.io"
# Keeps full history for recovery
```

---

## ⚠️ Known Limitations

1. **Styling:** Builder.io uses inline styles (not ideal for CSS-in-JS)
   - **Workaround:** Use Tailwind classes in content

2. **Complex Layouts:** Some custom layouts may not work in visual builder
   - **Workaround:** Create custom "template blocks" for complex sections

3. **API Rate Limits:** 1000 requests/month on free tier
   - **Workaround:** Cache content server-side

---

## 🚀 Phase 2 Timeline

| Week | Task | Owner |
|------|------|-------|
| Week 4 (Jun 3-9) | Setup Builder.io + API integration | Luis |
| Week 4 | Create content models | Luis + Client |
| Week 4 | Client training | Luis |
| Week 5 | Monitor & iterate | Luis |
| Ongoing | Support + updates | Luis/Client |

---

## 📚 References

- [Builder.io Documentation](https://www.builder.io/c/docs)
- [Next.js ISR](https://nextjs.org/docs/basic-features/data-fetching/incremental-static-regeneration)
- [Webhook Security](https://webhooks.fyi/)

---

*This integration makes Puyehue a self-managing platform.*  
*Client never needs to ask for changes again.*
