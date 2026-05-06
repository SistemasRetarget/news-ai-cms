# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: landing-pages.spec.ts >> Landing Pages Collection >> 7. Add CTA block
- Location: tests/landing-pages.spec.ts:91:7

# Error details

```
Error: expect(received).toBeTruthy()

Received: false
```

# Test source

```ts
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
  22  |     const page = await createRes.json();
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
> 108 |     expect(res.ok()).toBeTruthy();
      |                      ^ Error: expect(received).toBeTruthy()
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
  199 |     const page = await createRes.json();
  200 |     const updateRes = await request.patch(`${API_BASE}/landing-pages/${page.doc.id}`, {
  201 |       data: {
  202 |         blocks: [
  203 |           { blockType: 'features', title: 'Block 2' },
  204 |           { blockType: 'hero', headline: 'Block 1' },
  205 |         ],
  206 |       },
  207 |     });
  208 |     expect(updateRes.ok()).toBeTruthy();
```