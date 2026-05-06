# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: users.spec.ts >> Users Collection (Auth & Roles) >> 17. User session management and logout
- Location: tests/users.spec.ts:205:7

# Error details

```
SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
```

# Test source

```ts
  112 |     const updateRes = await request.patch(`${API_BASE}/users/${user.doc.id}`, {
  113 |       data: { lastLogin: new Date().toISOString() },
  114 |     });
  115 |     expect((await updateRes.json()).lastLogin).toBeTruthy();
  116 |   });
  117 | 
  118 |   test('10. Send password reset email', async ({ request }) => {
  119 |     const createRes = await request.post(`${API_BASE}/users`, {
  120 |       data: {
  121 |         email: `reset-${Date.now()}@test.com`,
  122 |         password: 'SecurePass123!',
  123 |       },
  124 |     });
  125 |     const user = await createRes.json();
  126 |     const resetRes = await request.patch(`${API_BASE}/users/${user.doc.id}`, {
  127 |       data: { resetPasswordToken: 'reset-token-' + Date.now() },
  128 |     });
  129 |     expect(resetRes.ok()).toBeTruthy();
  130 |   });
  131 | 
  132 |   test('11. List all users with pagination', async ({ request }) => {
  133 |     const res = await request.get(`${API_BASE}/users?limit=10&page=1`);
  134 |     expect(res.ok()).toBeTruthy();
  135 |     expect((await res.json()).docs.length).toBeLessThanOrEqual(10);
  136 |   });
  137 | 
  138 |   test('12. Filter users by role', async ({ request }) => {
  139 |     await request.post(`${API_BASE}/users`, {
  140 |       data: {
  141 |         email: `admin-${Date.now()}@test.com`,
  142 |         password: 'SecurePass123!',
  143 |         role: 'admin',
  144 |       },
  145 |     });
  146 |     const res = await request.get(`${API_BASE}/users?where[role][equals]=admin`);
  147 |     expect(res.ok()).toBeTruthy();
  148 |   });
  149 | 
  150 |   test('13. Search users by email', async ({ request }) => {
  151 |     const email = `search-${Date.now()}@test.com`;
  152 |     await request.post(`${API_BASE}/users`, {
  153 |       data: { email, password: 'SecurePass123!' },
  154 |     });
  155 |     const res = await request.get(`${API_BASE}/users?where[email][contains]=${encodeURIComponent(email)}`);
  156 |     expect(res.ok()).toBeTruthy();
  157 |   });
  158 | 
  159 |   test('14. Sort users by email', async ({ request }) => {
  160 |     const res = await request.get(`${API_BASE}/users?sort=email`);
  161 |     expect(res.ok()).toBeTruthy();
  162 |     const data = await res.json();
  163 |     let prevEmail = '';
  164 |     data.docs.forEach((u: any) => {
  165 |       if (prevEmail) {
  166 |         expect(u.email.localeCompare(prevEmail)).toBeGreaterThanOrEqual(0);
  167 |       }
  168 |       prevEmail = u.email;
  169 |     });
  170 |   });
  171 | 
  172 |   test('15. Track user activity (articles approved/rejected)', async ({ request }) => {
  173 |     const createRes = await request.post(`${API_BASE}/users`, {
  174 |       data: {
  175 |         email: `activity-${Date.now()}@test.com`,
  176 |         password: 'SecurePass123!',
  177 |       },
  178 |     });
  179 |     const user = await createRes.json();
  180 |     const updateRes = await request.patch(`${API_BASE}/users/${user.doc.id}`, {
  181 |       data: { articlesReviewed: 42 },
  182 |     });
  183 |     expect((await updateRes.json()).articlesReviewed).toBe(42);
  184 |   });
  185 | 
  186 |   test('16. Bulk enable/disable user accounts', async ({ request }) => {
  187 |     const u1 = await (await request.post(`${API_BASE}/users`, {
  188 |       data: { email: `bulk1-${Date.now()}@test.com`, password: 'SecurePass123!' },
  189 |     })).json();
  190 |     const u2 = await (await request.post(`${API_BASE}/users`, {
  191 |       data: { email: `bulk2-${Date.now()}@test.com`, password: 'SecurePass123!' },
  192 |     })).json();
  193 | 
  194 |     const lock1 = await request.patch(`${API_BASE}/users/${u1.doc.id}`, {
  195 |       data: { locked: true },
  196 |     });
  197 |     const lock2 = await request.patch(`${API_BASE}/users/${u2.doc.id}`, {
  198 |       data: { locked: true },
  199 |     });
  200 | 
  201 |     expect(lock1.ok()).toBeTruthy();
  202 |     expect(lock2.ok()).toBeTruthy();
  203 |   });
  204 | 
  205 |   test('17. User session management and logout', async ({ request }) => {
  206 |     const createRes = await request.post(`${API_BASE}/users`, {
  207 |       data: {
  208 |         email: `session-${Date.now()}@test.com`,
  209 |         password: 'SecurePass123!',
  210 |       },
  211 |     });
> 212 |     const user = await createRes.json();
      |                  ^ SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
  213 |     const updateRes = await request.patch(`${API_BASE}/users/${user.doc.id}`, {
  214 |       data: { lastLogout: new Date().toISOString() },
  215 |     });
  216 |     expect(updateRes.ok()).toBeTruthy();
  217 |   });
  218 | });
  219 | 
```