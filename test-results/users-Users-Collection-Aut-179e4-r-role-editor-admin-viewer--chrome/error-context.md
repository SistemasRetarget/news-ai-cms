# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: users.spec.ts >> Users Collection (Auth & Roles) >> 7. Assign user role (editor, admin, viewer)
- Location: tests/users.spec.ts:78:7

# Error details

```
Error: expect(received).toBeTruthy()

Received: false
```

# Test source

```ts
  1   | import { test, expect } from '@playwright/test';
  2   | 
  3   | const API_BASE = process.env.PW_API_BASE || 'http://localhost:3000/api';
  4   | 
  5   | test.describe('Users Collection (Auth & Roles)', () => {
  6   |   test('1. Create user with email', async ({ request }) => {
  7   |     const res = await request.post(`${API_BASE}/users`, {
  8   |       data: {
  9   |         email: `user-${Date.now()}@test.com`,
  10  |         password: 'SecurePass123!',
  11  |       },
  12  |     });
  13  |     expect(res.ok()).toBeTruthy();
  14  |     expect((await res.json()).doc.email).toBeTruthy();
  15  |   });
  16  | 
  17  |   test('2. Read user by ID', async ({ request }) => {
  18  |     const createRes = await request.post(`${API_BASE}/users`, {
  19  |       data: {
  20  |         email: `read-${Date.now()}@test.com`,
  21  |         password: 'SecurePass123!',
  22  |       },
  23  |     });
  24  |     const user = await createRes.json();
  25  |     const readRes = await request.get(`${API_BASE}/users/${user.doc.id}`);
  26  |     expect(readRes.ok()).toBeTruthy();
  27  |     expect((await readRes.json()).email).toBeTruthy();
  28  |   });
  29  | 
  30  |   test('3. Update user email', async ({ request }) => {
  31  |     const createRes = await request.post(`${API_BASE}/users`, {
  32  |       data: {
  33  |         email: `old-${Date.now()}@test.com`,
  34  |         password: 'SecurePass123!',
  35  |       },
  36  |     });
  37  |     const user = await createRes.json();
  38  |     const newEmail = `new-${Date.now()}@test.com`;
  39  |     const updateRes = await request.patch(`${API_BASE}/users/${user.doc.id}`, {
  40  |       data: { email: newEmail },
  41  |     });
  42  |     expect((await updateRes.json()).email).toBe(newEmail);
  43  |   });
  44  | 
  45  |   test('4. Delete user', async ({ request }) => {
  46  |     const createRes = await request.post(`${API_BASE}/users`, {
  47  |       data: {
  48  |         email: `delete-${Date.now()}@test.com`,
  49  |         password: 'SecurePass123!',
  50  |       },
  51  |     });
  52  |     const user = await createRes.json();
  53  |     const deleteRes = await request.delete(`${API_BASE}/users/${user.doc.id}`);
  54  |     expect(deleteRes.ok()).toBeTruthy();
  55  |   });
  56  | 
  57  |   test('5. Enforce unique email', async ({ request }) => {
  58  |     const email = `unique-${Date.now()}@test.com`;
  59  |     await request.post(`${API_BASE}/users`, {
  60  |       data: { email, password: 'SecurePass123!' },
  61  |     });
  62  |     const dupRes = await request.post(`${API_BASE}/users`, {
  63  |       data: { email, password: 'SecurePass123!' },
  64  |     });
  65  |     expect(dupRes.ok()).toBeFalsy();
  66  |   });
  67  | 
  68  |   test('6. Require strong password', async ({ request }) => {
  69  |     const res = await request.post(`${API_BASE}/users`, {
  70  |       data: {
  71  |         email: `weak-${Date.now()}@test.com`,
  72  |         password: 'weak',
  73  |       },
  74  |     });
  75  |     expect(res.ok()).toBeFalsy();
  76  |   });
  77  | 
  78  |   test('7. Assign user role (editor, admin, viewer)', async ({ request }) => {
  79  |     const res = await request.post(`${API_BASE}/users`, {
  80  |       data: {
  81  |         email: `editor-${Date.now()}@test.com`,
  82  |         password: 'SecurePass123!',
  83  |         role: 'editor',
  84  |       },
  85  |     });
> 86  |     expect(res.ok()).toBeTruthy();
      |                      ^ Error: expect(received).toBeTruthy()
  87  |     expect((await res.json()).doc.role).toBe('editor');
  88  |   });
  89  | 
  90  |   test('8. Lock/unlock user account', async ({ request }) => {
  91  |     const createRes = await request.post(`${API_BASE}/users`, {
  92  |       data: {
  93  |         email: `lock-${Date.now()}@test.com`,
  94  |         password: 'SecurePass123!',
  95  |       },
  96  |     });
  97  |     const user = await createRes.json();
  98  |     const lockRes = await request.patch(`${API_BASE}/users/${user.doc.id}`, {
  99  |       data: { locked: true },
  100 |     });
  101 |     expect((await lockRes.json()).locked).toBe(true);
  102 |   });
  103 | 
  104 |   test('9. Track last login', async ({ request }) => {
  105 |     const createRes = await request.post(`${API_BASE}/users`, {
  106 |       data: {
  107 |         email: `login-${Date.now()}@test.com`,
  108 |         password: 'SecurePass123!',
  109 |       },
  110 |     });
  111 |     const user = await createRes.json();
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
```