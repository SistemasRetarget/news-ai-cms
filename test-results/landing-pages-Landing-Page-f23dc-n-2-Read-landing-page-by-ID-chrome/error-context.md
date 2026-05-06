# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: landing-pages.spec.ts >> Landing Pages Collection >> 2. Read landing page by ID
- Location: tests/landing-pages.spec.ts:18:7

# Error details

```
SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | 
  3   | const API_BASE = process.env.PW_API_BASE || 'http://localhost:3000/api';
  4   | 
  5   | test.describe('Landing Pages Collection', () => {
  6   |   test('1. Create landing page with title', async ({ request }) => {
  7   |     const res = await request.post(`${API_BASE}/landing-pages`, {
  8   |       data: {
  9   |         title: 'Home Page',
  10  |         slug: 'home-' + Date.now(),
  11  |         published: true,
  12  |       },
  13  |     });
  14  |     expect(res.ok()).toBeTruthy();
  15  |     expect((await res.json()).doc.title).toBe('Home Page');
  16  |   });
  17  | 
  18  |   test('2. Read landing page by ID', async ({ request }) => {
  19  |     const createRes = await request.post(`${API_BASE}/landing-pages`, {
  20  |       data: { title: 'About', slug: 'about-' + Date.now(), published: true },
  21  |     });
> 22  |     const page = await createRes.json();
      |                  ^ SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
  23  |     const readRes = await request.get(`${API_BASE}/landing-pages/${page.doc.id}`);
  24  |     expect(readRes.ok()).toBeTruthy();
  25  |   });
  26  | 
  27  |   test('3. Update landing page title', async ({ request }) => {
  28  |     const createRes = await request.post(`${API_BASE}/landing-pages`, {
  29  |       data: { title: 'Old', slug: 'old-' + Date.now(), published: false },
  30  |     });
  31  |     const page = await createRes.json();
  32  |     const updateRes = await request.patch(`${API_BASE}/landing-pages/${page.doc.id}`, {
  33  |       data: { title: 'New Title' },
  34  |     });
  35  |     expect((await updateRes.json()).title).toBe('New Title');
  36  |   });
  37  | 
  38  |   test('4. Delete landing page', async ({ request }) => {
  39  |     const createRes = await request.post(`${API_BASE}/landing-pages`, {
  40  |       data: { title: 'Delete Me', slug: 'delete-' + Date.now(), published: false },
  41  |     });
  42  |     const page = await createRes.json();
  43  |     const deleteRes = await request.delete(`${API_BASE}/landing-pages/${page.doc.id}`);
  44  |     expect(deleteRes.ok()).toBeTruthy();
  45  |   });
  46  | 
  47  |   test('5. Add Hero block to landing page', async ({ request }) => {
  48  |     const res = await request.post(`${API_BASE}/landing-pages`, {
  49  |       data: {
  50  |         title: 'Hero Test',
  51  |         slug: 'hero-' + Date.now(),
  52  |         blocks: [
  53  |           {
  54  |             blockType: 'hero',
  55  |             headline: 'Welcome',
  56  |             subheadline: 'Test landing page',
  57  |             ctaText: 'Get Started',
  58  |             ctaUrl: '/signup',
  59  |           },
  60  |         ],
  61  |         published: true,
  62  |       },
  63  |     });
  64  |     expect(res.ok()).toBeTruthy();
  65  |     const data = await res.json();
  66  |     expect(data.doc.blocks[0].headline).toBe('Welcome');
  67  |   });
  68  | 
  69  |   test('6. Add Features block', async ({ request }) => {
  70  |     const res = await request.post(`${API_BASE}/landing-pages`, {
  71  |       data: {
  72  |         title: 'Features Page',
  73  |         slug: 'features-' + Date.now(),
  74  |         blocks: [
  75  |           {
  76  |             blockType: 'features',
  77  |             title: 'Our Features',
  78  |             items: [
  79  |               { title: 'Feature 1', description: 'Fast' },
  80  |               { title: 'Feature 2', description: 'Reliable' },
  81  |             ],
  82  |           },
  83  |         ],
  84  |         published: true,
  85  |       },
  86  |     });
  87  |     expect(res.ok()).toBeTruthy();
  88  |     expect((await res.json()).doc.blocks[0].items.length).toBe(2);
  89  |   });
  90  | 
  91  |   test('7. Add CTA block', async ({ request }) => {
  92  |     const res = await request.post(`${API_BASE}/landing-pages`, {
  93  |       data: {
  94  |         title: 'CTA Page',
  95  |         slug: 'cta-' + Date.now(),
  96  |         blocks: [
  97  |           {
  98  |             blockType: 'cta',
  99  |             headline: 'Ready to get started?',
  100 |             buttonText: 'Sign Up',
  101 |             buttonUrl: '/signup',
  102 |             variant: 'dark',
  103 |           },
  104 |         ],
  105 |         published: true,
  106 |       },
  107 |     });
  108 |     expect(res.ok()).toBeTruthy();
  109 |   });
  110 | 
  111 |   test('8. Publish/unpublish landing page', async ({ request }) => {
  112 |     const createRes = await request.post(`${API_BASE}/landing-pages`, {
  113 |       data: { title: 'Draft', slug: 'draft-' + Date.now(), published: false },
  114 |     });
  115 |     const page = await createRes.json();
  116 |     const publishRes = await request.patch(`${API_BASE}/landing-pages/${page.doc.id}`, {
  117 |       data: { published: true },
  118 |     });
  119 |     expect((await publishRes.json()).published).toBe(true);
  120 |   });
  121 | 
  122 |   test('9. Enforce unique slug', async ({ request }) => {
```