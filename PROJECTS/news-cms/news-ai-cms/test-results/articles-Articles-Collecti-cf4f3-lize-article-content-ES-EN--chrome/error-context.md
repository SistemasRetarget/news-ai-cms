# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: articles.spec.ts >> Articles Collection >> 15. Localize article content (ES/EN)
- Location: tests/articles.spec.ts:180:7

# Error details

```
SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

# Test source

```ts
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
  127 |         status: 'draft',
  128 |       },
  129 |     });
  130 |     const article = await createRes.json();
  131 |     expect(article.doc.aiProvider).toBe('anthropic');
  132 |     expect(article.doc.aiModel).toBe('claude-opus');
  133 |   });
  134 | 
  135 |   test('12. Query articles by category', async ({ request }) => {
  136 |     await request.post(`${API_BASE}/articles`, {
  137 |       data: {
  138 |         title: 'Category A',
  139 |         slug: 'cat-a-' + Date.now(),
  140 |         category: 'tech',
  141 |         status: 'draft',
  142 |       },
  143 |     });
  144 |     const res = await request.get(`${API_BASE}/articles?where[category][equals]=tech`);
  145 |     expect(res.ok()).toBeTruthy();
  146 |     const data = await res.json();
  147 |     expect(data.docs.length).toBeGreaterThan(0);
  148 |   });
  149 | 
  150 |   test('13. Query published articles only', async ({ request }) => {
  151 |     await request.post(`${API_BASE}/articles`, {
  152 |       data: {
  153 |         title: 'Published',
  154 |         slug: 'pub-' + Date.now(),
  155 |         status: 'published',
  156 |       },
  157 |     });
  158 |     const res = await request.get(`${API_BASE}/articles?where[status][equals]=published`);
  159 |     expect(res.ok()).toBeTruthy();
  160 |     const data = await res.json();
  161 |     data.docs.forEach((doc: any) => {
  162 |       expect(doc.status).toBe('published');
  163 |     });
  164 |   });
  165 | 
  166 |   // Rich text and localization
  167 |   test('14. Store rich text content', async ({ request }) => {
  168 |     const body = { root: { type: 'root', children: [{ type: 'text', text: 'Test' }] } };
  169 |     const createRes = await request.post(`${API_BASE}/articles`, {
  170 |       data: {
  171 |         title: 'RichText Test',
  172 |         slug: 'richtext-' + Date.now(),
  173 |         body,
  174 |         status: 'draft',
  175 |       },
  176 |     });
  177 |     expect(createRes.ok()).toBeTruthy();
  178 |   });
  179 | 
  180 |   test('15. Localize article content (ES/EN)', async ({ request }) => {
  181 |     const createRes = await request.post(`${API_BASE}/articles`, {
  182 |       data: {
  183 |         title_es: 'Artículo Test',
  184 |         title_en: 'Test Article',
  185 |         slug: 'localized-' + Date.now(),
  186 |         status: 'draft',
  187 |       },
  188 |     });
> 189 |     const article = await createRes.json();
      |                     ^ SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
  190 |     expect(article.doc.title_es || article.doc.title).toBeTruthy();
  191 |   });
  192 | 
  193 |   // Bulk and pagination
  194 |   test('16. Paginate articles (limit 10)', async ({ request }) => {
  195 |     const res = await request.get(`${API_BASE}/articles?limit=10&page=1`);
  196 |     expect(res.ok()).toBeTruthy();
  197 |     const data = await res.json();
  198 |     expect(data.docs.length).toBeLessThanOrEqual(10);
  199 |   });
  200 | 
  201 |   test('17. Sort articles by publishedAt descending', async ({ request }) => {
  202 |     const res = await request.get(`${API_BASE}/articles?sort=-publishedAt`);
  203 |     expect(res.ok()).toBeTruthy();
  204 |     const data = await res.json();
  205 |     let prevDate = new Date().toISOString();
  206 |     data.docs.forEach((doc: any) => {
  207 |       if (doc.publishedAt) {
  208 |         expect(doc.publishedAt <= prevDate).toBeTruthy();
  209 |         prevDate = doc.publishedAt;
  210 |       }
  211 |     });
  212 |   });
  213 | });
  214 | 
```