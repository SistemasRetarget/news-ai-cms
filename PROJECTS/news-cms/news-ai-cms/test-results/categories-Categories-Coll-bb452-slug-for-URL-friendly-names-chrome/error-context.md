# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: categories.spec.ts >> Categories Collection >> 17. Category with slug for URL-friendly names
- Location: tests/categories.spec.ts:154:7

# Error details

```
Error: expect(received).toBeTruthy()

Received: false
```

# Test source

```ts
  61  |     await request.post(`${API_BASE}/categories`, { data: { name } });
  62  |     const dupRes = await request.post(`${API_BASE}/categories`, { data: { name } });
  63  |     expect(dupRes.ok()).toBeFalsy();
  64  |   });
  65  | 
  66  |   test('8. Add description field (optional)', async ({ request }) => {
  67  |     const res = await request.post(`${API_BASE}/categories`, {
  68  |       data: { name: 'News', description: 'Latest news stories' },
  69  |     });
  70  |     expect(res.ok()).toBeTruthy();
  71  |     expect((await res.json()).doc.description).toBe('Latest news stories');
  72  |   });
  73  | 
  74  |   test('9. Add icon field (optional)', async ({ request }) => {
  75  |     const res = await request.post(`${API_BASE}/categories`, {
  76  |       data: { name: 'Sports', icon: '⚽' },
  77  |     });
  78  |     expect(res.ok()).toBeTruthy();
  79  |     expect((await res.json()).doc.icon).toBe('⚽');
  80  |   });
  81  | 
  82  |   test('10. Filter categories by name', async ({ request }) => {
  83  |     const name = 'FilterTest-' + Date.now();
  84  |     await request.post(`${API_BASE}/categories`, { data: { name } });
  85  |     const res = await request.get(`${API_BASE}/categories?where[name][contains]=${name}`);
  86  |     expect(res.ok()).toBeTruthy();
  87  |     const data = await res.json();
  88  |     expect(data.docs.some((c: any) => c.name.includes(name))).toBeTruthy();
  89  |   });
  90  | 
  91  |   test('11. Count articles per category', async ({ request }) => {
  92  |     const catRes = await request.post(`${API_BASE}/categories`, {
  93  |       data: { name: 'Article Count Test' },
  94  |     });
  95  |     const cat = await catRes.json();
  96  |     // Ensure articles can reference this category
  97  |     const res = await request.get(`${API_BASE}/categories/${cat.doc.id}`);
  98  |     expect(res.ok()).toBeTruthy();
  99  |   });
  100 | 
  101 |   test('12. Soft delete category (archive)', async ({ request }) => {
  102 |     const createRes = await request.post(`${API_BASE}/categories`, {
  103 |       data: { name: 'Archive Test' },
  104 |     });
  105 |     const cat = await createRes.json();
  106 |     const updateRes = await request.patch(`${API_BASE}/categories/${cat.doc.id}`, {
  107 |       data: { archived: true },
  108 |     });
  109 |     expect(updateRes.ok()).toBeTruthy();
  110 |   });
  111 | 
  112 |   test('13. Pagination for categories', async ({ request }) => {
  113 |     const res = await request.get(`${API_BASE}/categories?limit=5&page=1`);
  114 |     expect(res.ok()).toBeTruthy();
  115 |     expect((await res.json()).docs.length).toBeLessThanOrEqual(5);
  116 |   });
  117 | 
  118 |   test('14. Sort categories by name ascending', async ({ request }) => {
  119 |     const res = await request.get(`${API_BASE}/categories?sort=name`);
  120 |     expect(res.ok()).toBeTruthy();
  121 |     const data = await res.json();
  122 |     let prevName = '';
  123 |     data.docs.forEach((c: any) => {
  124 |       expect(c.name.localeCompare(prevName)).toBeGreaterThanOrEqual(0);
  125 |       prevName = c.name;
  126 |     });
  127 |   });
  128 | 
  129 |   test('15. Get total count of categories', async ({ request }) => {
  130 |     const res = await request.get(`${API_BASE}/categories`);
  131 |     const data = await res.json();
  132 |     expect(data.totalDocs).toBeGreaterThanOrEqual(0);
  133 |   });
  134 | 
  135 |   test('16. Bulk update multiple categories', async ({ request }) => {
  136 |     const cat1 = await (await request.post(`${API_BASE}/categories`, {
  137 |       data: { name: 'Bulk1' },
  138 |     })).json();
  139 |     const cat2 = await (await request.post(`${API_BASE}/categories`, {
  140 |       data: { name: 'Bulk2' },
  141 |     })).json();
  142 | 
  143 |     const update1 = await request.patch(`${API_BASE}/categories/${cat1.doc.id}`, {
  144 |       data: { description: 'Updated 1' },
  145 |     });
  146 |     const update2 = await request.patch(`${API_BASE}/categories/${cat2.doc.id}`, {
  147 |       data: { description: 'Updated 2' },
  148 |     });
  149 | 
  150 |     expect(update1.ok()).toBeTruthy();
  151 |     expect(update2.ok()).toBeTruthy();
  152 |   });
  153 | 
  154 |   test('17. Category with slug for URL-friendly names', async ({ request }) => {
  155 |     const res = await request.post(`${API_BASE}/categories`, {
  156 |       data: {
  157 |         name: 'Breaking News',
  158 |         slug: 'breaking-news-' + Date.now(),
  159 |       },
  160 |     });
> 161 |     expect(res.ok()).toBeTruthy();
      |                      ^ Error: expect(received).toBeTruthy()
  162 |   });
  163 | });
  164 | 
```