# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: sources.spec.ts >> Sources Collection (RSS/API feeds) >> 8. Enable/disable source aggregation
- Location: tests/sources.spec.ts:94:7

# Error details

```
SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

# Test source

```ts
  2   | 
  3   | const API_BASE = process.env.PW_API_BASE || 'http://localhost:3000/api';
  4   | 
  5   | test.describe('Sources Collection (RSS/API feeds)', () => {
  6   |   test('1. Create news source with URL', async ({ request }) => {
  7   |     const res = await request.post(`${API_BASE}/sources`, {
  8   |       data: {
  9   |         name: 'BBC News',
  10  |         feedUrl: 'https://feeds.bbc.co.uk/news/rss.xml',
  11  |         type: 'rss',
  12  |       },
  13  |     });
  14  |     expect(res.ok()).toBeTruthy();
  15  |     expect((await res.json()).doc.name).toBe('BBC News');
  16  |   });
  17  | 
  18  |   test('2. Read source by ID', async ({ request }) => {
  19  |     const createRes = await request.post(`${API_BASE}/sources`, {
  20  |       data: {
  21  |         name: 'CNN',
  22  |         feedUrl: 'https://cnn.com/feed.xml',
  23  |         type: 'rss',
  24  |       },
  25  |     });
  26  |     const source = await createRes.json();
  27  |     const readRes = await request.get(`${API_BASE}/sources/${source.doc.id}`);
  28  |     expect(readRes.ok()).toBeTruthy();
  29  |     expect((await readRes.json()).name).toBe('CNN');
  30  |   });
  31  | 
  32  |   test('3. Update source URL', async ({ request }) => {
  33  |     const createRes = await request.post(`${API_BASE}/sources`, {
  34  |       data: {
  35  |         name: 'Reuters',
  36  |         feedUrl: 'https://reuters.com/old.xml',
  37  |         type: 'rss',
  38  |       },
  39  |     });
  40  |     const source = await createRes.json();
  41  |     const updateRes = await request.patch(`${API_BASE}/sources/${source.doc.id}`, {
  42  |       data: { feedUrl: 'https://reuters.com/new.xml' },
  43  |     });
  44  |     expect((await updateRes.json()).feedUrl).toBe('https://reuters.com/new.xml');
  45  |   });
  46  | 
  47  |   test('4. Delete source', async ({ request }) => {
  48  |     const createRes = await request.post(`${API_BASE}/sources`, {
  49  |       data: {
  50  |         name: 'Temp Source',
  51  |         feedUrl: 'https://example.com/feed',
  52  |         type: 'rss',
  53  |       },
  54  |     });
  55  |     const source = await createRes.json();
  56  |     const deleteRes = await request.delete(`${API_BASE}/sources/${source.doc.id}`);
  57  |     expect(deleteRes.ok()).toBeTruthy();
  58  |   });
  59  | 
  60  |   test('5. Validate RSS feed URL format', async ({ request }) => {
  61  |     const res = await request.post(`${API_BASE}/sources`, {
  62  |       data: {
  63  |         name: 'Invalid Feed',
  64  |         feedUrl: 'not-a-valid-url',
  65  |         type: 'rss',
  66  |       },
  67  |     });
  68  |     expect(res.ok()).toBeFalsy();
  69  |   });
  70  | 
  71  |   test('6. Support multiple feed types (RSS, Atom, JSON)', async ({ request }) => {
  72  |     const rssRes = await request.post(`${API_BASE}/sources`, {
  73  |       data: { name: 'RSS Feed', feedUrl: 'https://example.com/rss', type: 'rss' },
  74  |     });
  75  |     const atomRes = await request.post(`${API_BASE}/sources`, {
  76  |       data: { name: 'Atom Feed', feedUrl: 'https://example.com/atom', type: 'atom' },
  77  |     });
  78  |     expect(rssRes.ok()).toBeTruthy();
  79  |     expect(atomRes.ok()).toBeTruthy();
  80  |   });
  81  | 
  82  |   test('7. Set source as active/inactive', async ({ request }) => {
  83  |     const createRes = await request.post(`${API_BASE}/sources`, {
  84  |       data: {
  85  |         name: 'Active Source',
  86  |         feedUrl: 'https://example.com/feed',
  87  |         type: 'rss',
  88  |         active: true,
  89  |       },
  90  |     });
  91  |     expect((await createRes.json()).doc.active).toBe(true);
  92  |   });
  93  | 
  94  |   test('8. Enable/disable source aggregation', async ({ request }) => {
  95  |     const createRes = await request.post(`${API_BASE}/sources`, {
  96  |       data: {
  97  |         name: 'Test Source',
  98  |         feedUrl: 'https://example.com/feed',
  99  |         type: 'rss',
  100 |       },
  101 |     });
> 102 |     const source = await createRes.json();
      |                    ^ SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
  103 |     const updateRes = await request.patch(`${API_BASE}/sources/${source.doc.id}`, {
  104 |       data: { aggregationEnabled: false },
  105 |     });
  106 |     expect(updateRes.ok()).toBeTruthy();
  107 |   });
  108 | 
  109 |   test('9. Track last fetch time', async ({ request }) => {
  110 |     const createRes = await request.post(`${API_BASE}/sources`, {
  111 |       data: {
  112 |         name: 'Track Source',
  113 |         feedUrl: 'https://example.com/feed',
  114 |         type: 'rss',
  115 |       },
  116 |     });
  117 |     const source = await createRes.json();
  118 |     const updateRes = await request.patch(`${API_BASE}/sources/${source.doc.id}`, {
  119 |       data: { lastFetchedAt: new Date().toISOString() },
  120 |     });
  121 |     expect((await updateRes.json()).lastFetchedAt).toBeTruthy();
  122 |   });
  123 | 
  124 |   test('10. Store fetch error log', async ({ request }) => {
  125 |     const createRes = await request.post(`${API_BASE}/sources`, {
  126 |       data: {
  127 |         name: 'Error Source',
  128 |         feedUrl: 'https://example.com/feed',
  129 |         type: 'rss',
  130 |       },
  131 |     });
  132 |     const source = await createRes.json();
  133 |     const updateRes = await request.patch(`${API_BASE}/sources/${source.doc.id}`, {
  134 |       data: { lastError: 'Connection timeout' },
  135 |     });
  136 |     expect((await updateRes.json()).lastError).toBe('Connection timeout');
  137 |   });
  138 | 
  139 |   test('11. List all active sources', async ({ request }) => {
  140 |     await request.post(`${API_BASE}/sources`, {
  141 |       data: {
  142 |         name: 'Active 1',
  143 |         feedUrl: 'https://example1.com',
  144 |         type: 'rss',
  145 |         active: true,
  146 |       },
  147 |     });
  148 |     const res = await request.get(`${API_BASE}/sources?where[active][equals]=true`);
  149 |     expect(res.ok()).toBeTruthy();
  150 |     const data = await res.json();
  151 |     data.docs.forEach((s: any) => {
  152 |       expect(s.active).toBe(true);
  153 |     });
  154 |   });
  155 | 
  156 |   test('12. Filter sources by type', async ({ request }) => {
  157 |     await request.post(`${API_BASE}/sources`, {
  158 |       data: {
  159 |         name: 'Atom Example',
  160 |         feedUrl: 'https://example.com/atom',
  161 |         type: 'atom',
  162 |       },
  163 |     });
  164 |     const res = await request.get(`${API_BASE}/sources?where[type][equals]=atom`);
  165 |     expect(res.ok()).toBeTruthy();
  166 |   });
  167 | 
  168 |   test('13. Pagination for sources', async ({ request }) => {
  169 |     const res = await request.get(`${API_BASE}/sources?limit=10&page=1`);
  170 |     expect(res.ok()).toBeTruthy();
  171 |     expect((await res.json()).docs.length).toBeLessThanOrEqual(10);
  172 |   });
  173 | 
  174 |   test('14. Sort sources by name', async ({ request }) => {
  175 |     const res = await request.get(`${API_BASE}/sources?sort=name`);
  176 |     expect(res.ok()).toBeTruthy();
  177 |     const data = await res.json();
  178 |     let prevName = '';
  179 |     data.docs.forEach((s: any) => {
  180 |       expect(s.name.localeCompare(prevName)).toBeGreaterThanOrEqual(0);
  181 |       prevName = s.name;
  182 |     });
  183 |   });
  184 | 
  185 |   test('15. Bulk enable/disable sources', async ({ request }) => {
  186 |     const s1 = await (await request.post(`${API_BASE}/sources`, {
  187 |       data: { name: 'Bulk1', feedUrl: 'https://bulk1.com', type: 'rss', active: true },
  188 |     })).json();
  189 |     const s2 = await (await request.post(`${API_BASE}/sources`, {
  190 |       data: { name: 'Bulk2', feedUrl: 'https://bulk2.com', type: 'rss', active: true },
  191 |     })).json();
  192 | 
  193 |     const u1 = await request.patch(`${API_BASE}/sources/${s1.doc.id}`, {
  194 |       data: { active: false },
  195 |     });
  196 |     const u2 = await request.patch(`${API_BASE}/sources/${s2.doc.id}`, {
  197 |       data: { active: false },
  198 |     });
  199 | 
  200 |     expect(u1.ok()).toBeTruthy();
  201 |     expect(u2.ok()).toBeTruthy();
  202 |   });
```