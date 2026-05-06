# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: landing-pages.spec.ts >> Landing Pages Collection >> 15. Reorder blocks on landing page
- Location: tests/landing-pages.spec.ts:187:7

# Error details

```
SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

# Test source

```ts
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
  123 |     const slug = 'unique-slug-' + Date.now();
  124 |     await request.post(`${API_BASE}/landing-pages`, {
  125 |       data: { title: 'Page 1', slug, published: true },
  126 |     });
  127 |     const dupRes = await request.post(`${API_BASE}/landing-pages`, {
  128 |       data: { title: 'Page 2', slug, published: true },
  129 |     });
  130 |     expect(dupRes.ok()).toBeFalsy();
  131 |   });
  132 | 
  133 |   test('10. Require title field', async ({ request }) => {
  134 |     const res = await request.post(`${API_BASE}/landing-pages`, {
  135 |       data: { slug: 'no-title-' + Date.now(), published: true },
  136 |     });
  137 |     expect(res.ok()).toBeFalsy();
  138 |   });
  139 | 
  140 |   test('11. List published pages only', async ({ request }) => {
  141 |     await request.post(`${API_BASE}/landing-pages`, {
  142 |       data: { title: 'Public', slug: 'public-' + Date.now(), published: true },
  143 |     });
  144 |     const res = await request.get(`${API_BASE}/landing-pages?where[published][equals]=true`);
  145 |     expect(res.ok()).toBeTruthy();
  146 |     const data = await res.json();
  147 |     data.docs.forEach((p: any) => {
  148 |       expect(p.published).toBe(true);
  149 |     });
  150 |   });
  151 | 
  152 |   test('12. Add SEO metadata', async ({ request }) => {
  153 |     const res = await request.post(`${API_BASE}/landing-pages`, {
  154 |       data: {
  155 |         title: 'SEO Page',
  156 |         slug: 'seo-' + Date.now(),
  157 |         meta: {
  158 |           description: 'Test page description',
  159 |           keywords: 'test, page, seo',
  160 |           ogImage: 'https://example.com/og.jpg',
  161 |         },
  162 |         published: true,
  163 |       },
  164 |     });
  165 |     expect(res.ok()).toBeTruthy();
  166 |   });
  167 | 
  168 |   test('13. Pagination for landing pages', async ({ request }) => {
  169 |     const res = await request.get(`${API_BASE}/landing-pages?limit=10&page=1`);
  170 |     expect(res.ok()).toBeTruthy();
  171 |     expect((await res.json()).docs.length).toBeLessThanOrEqual(10);
  172 |   });
  173 | 
  174 |   test('14. Sort pages by title', async ({ request }) => {
  175 |     const res = await request.get(`${API_BASE}/landing-pages?sort=title`);
  176 |     expect(res.ok()).toBeTruthy();
  177 |     const data = await res.json();
  178 |     let prevTitle = '';
  179 |     data.docs.forEach((p: any) => {
  180 |       if (prevTitle) {
  181 |         expect(p.title.localeCompare(prevTitle)).toBeGreaterThanOrEqual(0);
  182 |       }
  183 |       prevTitle = p.title;
  184 |     });
  185 |   });
  186 | 
  187 |   test('15. Reorder blocks on landing page', async ({ request }) => {
  188 |     const createRes = await request.post(`${API_BASE}/landing-pages`, {
  189 |       data: {
  190 |         title: 'Reorder Test',
  191 |         slug: 'reorder-' + Date.now(),
  192 |         blocks: [
  193 |           { blockType: 'hero', headline: 'Block 1' },
  194 |           { blockType: 'features', title: 'Block 2' },
  195 |         ],
  196 |         published: true,
  197 |       },
  198 |     });
> 199 |     const page = await createRes.json();
      |                  ^ SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
  200 |     const updateRes = await request.patch(`${API_BASE}/landing-pages/${page.doc.id}`, {
  201 |       data: {
  202 |         blocks: [
  203 |           { blockType: 'features', title: 'Block 2' },
  204 |           { blockType: 'hero', headline: 'Block 1' },
  205 |         ],
  206 |       },
  207 |     });
  208 |     expect(updateRes.ok()).toBeTruthy();
  209 |   });
  210 | 
  211 |   test('16. Track page views/analytics', async ({ request }) => {
  212 |     const createRes = await request.post(`${API_BASE}/landing-pages`, {
  213 |       data: {
  214 |         title: 'Analytics',
  215 |         slug: 'analytics-' + Date.now(),
  216 |         published: true,
  217 |       },
  218 |     });
  219 |     const page = await createRes.json();
  220 |     const updateRes = await request.patch(`${API_BASE}/landing-pages/${page.doc.id}`, {
  221 |       data: { viewCount: 1234 },
  222 |     });
  223 |     expect((await updateRes.json()).viewCount).toBe(1234);
  224 |   });
  225 | 
  226 |   test('17. Clone/duplicate landing page', async ({ request }) => {
  227 |     const original = await (await request.post(`${API_BASE}/landing-pages`, {
  228 |       data: { title: 'Original', slug: 'orig-' + Date.now(), published: true },
  229 |     })).json();
  230 | 
  231 |     const clone = await request.post(`${API_BASE}/landing-pages`, {
  232 |       data: {
  233 |         title: 'Clone of Original',
  234 |         slug: 'clone-' + Date.now(),
  235 |         blocks: original.doc.blocks,
  236 |         published: false,
  237 |       },
  238 |     });
  239 |     expect(clone.ok()).toBeTruthy();
  240 |   });
  241 | });
  242 | 
```