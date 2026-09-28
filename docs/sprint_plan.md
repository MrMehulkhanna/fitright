# FitRight — Sprint Plan

> **Team:** 1 full-stack developer + 1 QA
> **Sprint length:** 1 week
> **Velocity:** 40 story points per sprint

---

## Sprint 1 — Foundation
**Goal:** Running Flask app with auth, DB models, and seed data.

| Story | Points |
|---|---|
| US-01 Register | 3 |
| US-02 Login / Logout | 2 |
| US-03 Admin role | 2 |
| US-23 DB indexes | 2 |
| US-24 CSRF protection | 3 |
| US-18 Seed script | 5 |
| US-22 Dockerfile + docker-compose | 5 |
| US-25 README skeleton | 3 |
| **Buffer / setup** | **15** |
| **Total** | **40** |

**Definition of Done for Sprint 1:**
- `flask run` starts without errors
- Register, login, logout flow works in browser
- `python seeds/seed.py` populates 30 products + 200 orders
- Docker Compose brings up app + MySQL

---

## Sprint 2 — Catalog & Sizing
**Goal:** Full product catalog, measurement input, and size recommendation engine.

| Story | Points |
|---|---|
| US-04 Category filter | 5 |
| US-05 Search | 3 |
| US-06 Product detail | 3 |
| US-07 Measurements form | 5 |
| US-08 Size recommendation on product page | 8 |
| US-09 Return-feedback adjustment | 8 |
| US-10 Confidence label | 3 |
| **Buffer** | **5** |
| **Total** | **40** |

**Definition of Done for Sprint 2:**
- Product grid renders with search + category filter
- Logged-in user with measurements sees size recommendation on product page
- Recommendation shifts when >30% of returns signal wrong sizing
- Confidence badge colour-coded correctly

---

## Sprint 3 — Orders, Returns & Admin Dashboard
**Goal:** Order placement, return submission, and admin analytics.

| Story | Points |
|---|---|
| US-11 Place order | 5 |
| US-12 My Orders page | 3 |
| US-13 Submit return | 5 |
| US-14 Return rate chart | 5 |
| US-15 Reasons doughnut chart | 3 |
| US-16 Size returns bar chart | 5 |
| US-17 KPI cards | 2 |
| **Buffer** | **12** |
| **Total** | **40** |

**Definition of Done for Sprint 3:**
- Customer can place order and see it in My Orders
- Customer can submit return; order status flips to ‘returned’
- Admin dashboard shows all three Chart.js charts with live data
- Non-admin users receive 403 on /admin/

---

## Sprint 4 — Quality, CI & Documentation
**Goal:** Full test coverage, CI pipeline, and complete documentation.

| Story | Points |
|---|---|
| US-19 Recommendation unit tests | 8 |
| US-20 Auth unit tests | 5 |
| US-21 GitHub Actions CI | 3 |
| US-25 README finalised | 3 |
| Bug fixes / polish | 10 |
| Backlog docs | 5 |
| Sprint retrospective docs | 3 |
| **Buffer** | **3** |
| **Total** | **40** |

**Definition of Done for Sprint 4:**
- `pytest` passes with 0 failures
- CI workflow green on GitHub for Python 3.11 + 3.12
- README complete with ER diagram, setup steps, recommendation explanation
- All documentation files committed
