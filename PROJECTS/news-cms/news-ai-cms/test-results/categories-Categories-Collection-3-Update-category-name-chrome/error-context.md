# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: categories.spec.ts >> Categories Collection >> 3. Update category name
- Location: tests/categories.spec.ts:24:7

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
  5   | test.describe('Categories Collection', () => {
  6   |   test('1. Create category with name', async ({ request }) => {
  7   |     const res = await request.post(`${API_BASE}/categories`, {
  8   |       data: { name: 'Tech News' },
  9   |     });
  10  |     expect(res.ok()).toBeTruthy();
  11  |     expect((await res.json()).doc.name).toBe('Tech News');
  12  |   });
  13  | 
  14  |   test('2. Read category by ID', async ({ request }) => {
  15  |     const createRes = await request.post(`${API_BASE}/categories`, {
  16  |       data: { name: 'Sports' },
  17  |     });
  18  |     const cat = await createRes.json();
  19  |     const readRes = await request.get(`${API_BASE}/categories/${cat.doc.id}`);
  20  |     expect(readRes.ok()).toBeTruthy();
  21  |     expect((await readRes.json()).name).toBe('Sports');
  22  |   });
  23  | 
  24  |   test('3. Update category name', async ({ request }) => {
  25  |     const createRes = await request.post(`${API_BASE}/categories`, {
  26  |       data: { name: 'Old Name' },
  27  |     });
> 28  |     const cat = await createRes.json();
      |                 ^ SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
  29  |     const updateRes = await request.patch(`${API_BASE}/categories/${cat.doc.id}`, {
  30  |       data: { name: 'New Name' },
  31  |     });
  32  |     expect((await updateRes.json()).name).toBe('New Name');
  33  |   });
  34  | 
  35  |   test('4. Delete category', async ({ request }) => {
  36  |     const createRes = await request.post(`${API_BASE}/categories`, {
  37  |       data: { name: 'Temp Cat' },
  38  |     });
  39  |     const cat = await createRes.json();
  40  |     const deleteRes = await request.delete(`${API_BASE}/categories/${cat.doc.id}`);
  41  |     expect(deleteRes.ok()).toBeTruthy();
  42  |   });
  43  | 
  44  |   test('5. List all categories', async ({ request }) => {
  45  |     await request.post(`${API_BASE}/categories`, { data: { name: 'Cat A' } });
  46  |     await request.post(`${API_BASE}/categories`, { data: { name: 'Cat B' } });
  47  |     const res = await request.get(`${API_BASE}/categories`);
  48  |     expect(res.ok()).toBeTruthy();
  49  |     expect((await res.json()).docs.length).toBeGreaterThan(0);
  50  |   });
  51  | 
  52  |   test('6. Require category name', async ({ request }) => {
  53  |     const res = await request.post(`${API_BASE}/categories`, {
  54  |       data: {},
  55  |     });
  56  |     expect(res.ok()).toBeFalsy();
  57  |   });
  58  | 
  59  |   test('7. Enforce unique category name', async ({ request }) => {
  60  |     const name = 'Unique-' + Date.now();
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
```