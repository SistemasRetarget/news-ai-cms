# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: articles.spec.ts >> Articles Collection >> 2. Read article by ID
- Location: tests/articles.spec.ts:22:7

# Error details

```
SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | 
  3   | const API_BASE = process.env.PW_API_BASE || 'http://localhost:3000/api';
  4   | const ADMIN_URL = process.env.PW_ADMIN_URL || 'http://localhost:3000/admin';
  5   | 
  6   | test.describe('Articles Collection', () => {
  7   |   // Article CRUD tests
  8   |   test('1. Create article with required fields', async ({ request }) => {
  9   |     const response = await request.post(`${API_BASE}/articles`, {
  10  |       data: {
  11  |         title: 'Test Article',
  12  |         slug: 'test-article-' + Date.now(),
  13  |         category: 'test-category',
  14  |         status: 'draft',
  15  |       },
  16  |     });
  17  |     expect(response.ok()).toBeTruthy();
  18  |     const data = await response.json();
  19  |     expect(data.doc?.title).toBe('Test Article');
  20  |   });
  21  | 
  22  |   test('2. Read article by ID', async ({ request }) => {
  23  |     const createRes = await request.post(`${API_BASE}/articles`, {
  24  |       data: { title: 'Read Test', slug: 'read-test-' + Date.now(), status: 'draft' },
  25  |     });
> 26  |     const article = await createRes.json();
      |                     ^ SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
  27  |     const readRes = await request.get(`${API_BASE}/articles/${article.doc.id}`);
  28  |     expect(readRes.ok()).toBeTruthy();
  29  |     expect((await readRes.json()).title).toBe('Read Test');
  30  |   });
  31  | 
  32  |   test('3. Update article title', async ({ request }) => {
  33  |     const createRes = await request.post(`${API_BASE}/articles`, {
  34  |       data: { title: 'Old Title', slug: 'update-test-' + Date.now(), status: 'draft' },
  35  |     });
  36  |     const article = await createRes.json();
  37  |     const updateRes = await request.patch(`${API_BASE}/articles/${article.doc.id}`, {
  38  |       data: { title: 'New Title' },
  39  |     });
  40  |     expect(updateRes.ok()).toBeTruthy();
  41  |     expect((await updateRes.json()).title).toBe('New Title');
  42  |   });
  43  | 
  44  |   test('4. Delete article', async ({ request }) => {
  45  |     const createRes = await request.post(`${API_BASE}/articles`, {
  46  |       data: { title: 'Delete Test', slug: 'delete-test-' + Date.now(), status: 'draft' },
  47  |     });
  48  |     const article = await createRes.json();
  49  |     const deleteRes = await request.delete(`${API_BASE}/articles/${article.doc.id}`);
  50  |     expect(deleteRes.ok()).toBeTruthy();
  51  |   });
  52  | 
  53  |   // Status workflow tests
  54  |   test('5. Transition article from draft to review', async ({ request }) => {
  55  |     const createRes = await request.post(`${API_BASE}/articles`, {
  56  |       data: { title: 'Workflow Test', slug: 'workflow-' + Date.now(), status: 'draft' },
  57  |     });
  58  |     const article = await createRes.json();
  59  |     const updateRes = await request.patch(`${API_BASE}/articles/${article.doc.id}`, {
  60  |       data: { status: 'review' },
  61  |     });
  62  |     expect((await updateRes.json()).status).toBe('review');
  63  |   });
  64  | 
  65  |   test('6. Transition article from review to published', async ({ request }) => {
  66  |     const createRes = await request.post(`${API_BASE}/articles`, {
  67  |       data: { title: 'Publish Test', slug: 'publish-' + Date.now(), status: 'review' },
  68  |     });
  69  |     const article = await createRes.json();
  70  |     const updateRes = await request.patch(`${API_BASE}/articles/${article.doc.id}`, {
  71  |       data: { status: 'published', publishedAt: new Date().toISOString() },
  72  |     });
  73  |     expect((await updateRes.json()).status).toBe('published');
  74  |   });
  75  | 
  76  |   test('7. Set rejection reason on draft articles', async ({ request }) => {
  77  |     const createRes = await request.post(`${API_BASE}/articles`, {
  78  |       data: { title: 'Rejection Test', slug: 'reject-' + Date.now(), status: 'draft' },
  79  |     });
  80  |     const article = await createRes.json();
  81  |     const updateRes = await request.patch(`${API_BASE}/articles/${article.doc.id}`, {
  82  |       data: { rejectionReason: 'Needs more sources' },
  83  |     });
  84  |     expect((await updateRes.json()).rejectionReason).toBe('Needs more sources');
  85  |   });
  86  | 
  87  |   // Field validation tests
  88  |   test('8. Require article title', async ({ request }) => {
  89  |     const response = await request.post(`${API_BASE}/articles`, {
  90  |       data: { slug: 'no-title-' + Date.now(), status: 'draft' },
  91  |     });
  92  |     expect(response.ok()).toBeFalsy();
  93  |   });
  94  | 
  95  |   test('9. Enforce unique slug', async ({ request }) => {
  96  |     const slug = 'unique-slug-' + Date.now();
  97  |     await request.post(`${API_BASE}/articles`, {
  98  |       data: { title: 'First', slug, status: 'draft' },
  99  |     });
  100 |     const dupRes = await request.post(`${API_BASE}/articles`, {
  101 |       data: { title: 'Second', slug, status: 'draft' },
  102 |     });
  103 |     expect(dupRes.ok()).toBeFalsy();
  104 |   });
  105 | 
  106 |   test('10. Limit excerpt to 300 chars', async ({ request }) => {
  107 |     const longExcerpt = 'a'.repeat(400);
  108 |     const response = await request.post(`${API_BASE}/articles`, {
  109 |       data: {
  110 |         title: 'Excerpt Test',
  111 |         slug: 'excerpt-' + Date.now(),
  112 |         excerpt: longExcerpt,
  113 |         status: 'draft',
  114 |       },
  115 |     });
  116 |     expect(response.ok()).toBeFalsy();
  117 |   });
  118 | 
  119 |   // AI metadata tests
  120 |   test('11. Store AI provider metadata', async ({ request }) => {
  121 |     const createRes = await request.post(`${API_BASE}/articles`, {
  122 |       data: {
  123 |         title: 'AI Test',
  124 |         slug: 'ai-' + Date.now(),
  125 |         aiProvider: 'anthropic',
  126 |         aiModel: 'claude-opus',
```