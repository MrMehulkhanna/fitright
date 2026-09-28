# FitRight — Product Backlog

> Sprint velocity assumption: 40 story points per week.

| # | User Story | Acceptance Criteria | Story Points |
|---|---|---|---|
| US-01 | As a **customer**, I want to register with email and password so I can have a personal account. | Registration form validates email uniqueness, password ≥8 chars, CSRF token present; password stored hashed. | 3 |
| US-02 | As a **customer**, I want to log in and log out securely. | Login checks hashed password; session created; logout destroys session; unauthenticated routes redirect to login. | 2 |
| US-03 | As an **admin**, I want to log in with an elevated role so I can access the dashboard. | Admin role set in DB; non-admin users receive 403 on admin routes. | 2 |
| US-04 | As a **customer**, I want to browse products by category so I can find what I’m looking for. | Catalog page shows product cards; category filter narrows results; URL params preserved on pagination. | 5 |
| US-05 | As a **customer**, I want to search products by name or brand so I can find specific items quickly. | Search query filters products case-insensitively; empty results show a helpful message. | 3 |
| US-06 | As a **customer**, I want to view a product detail page so I can see full product info. | Page shows image, name, brand, category, price, description, size chart table. | 3 |
| US-07 | As a **customer**, I want to enter my body measurements (chest, waist, hip) so the app can recommend sizes. | Measurement form validates numeric range (cm); saves to DB; updates existing record on re-submit. | 5 |
| US-08 | As a **customer**, I want to see a recommended size on each product page so I don’t have to guess. | Recommendation visible only when measurements saved; shows size + confidence badge; links to measurements page if not set. | 8 |
| US-09 | As a **customer**, I want the size recommendation to account for return feedback so it’s more accurate over time. | If >30% of returns for a product are too_small/too_large, size shifts up/down; product page shows adjustment note. | 8 |
| US-10 | As a **customer**, I want a confidence label (High/Medium/Low) on my size recommendation so I know how reliable it is. | Label computed from Euclidean distance; colour-coded badge (green/yellow/red) shown on product page. | 3 |
| US-11 | As a **customer**, I want to place an order for a product in a chosen size. | Order form requires authentication; order created with status ‘pending’; confirmation flash shown. | 5 |
| US-12 | As a **customer**, I want to view all my orders with their statuses so I can track them. | My Orders page lists orders ordered by date descending; shows product, size, status, date. | 3 |
| US-13 | As a **customer**, I want to submit a return for a delivered or shipped order with a reason. | Return form shows reason dropdown + optional note; order status updated to ‘returned’; duplicate returns blocked. | 5 |
| US-14 | As an **admin**, I want to see return rate by category as a bar chart so I can identify problem categories. | Chart.js bar chart rendered; data fetched from DB via SQLAlchemy aggregation; percentages shown on y-axis. | 5 |
| US-15 | As an **admin**, I want to see top return reasons as a doughnut chart so I can understand customer complaints. | Doughnut chart shows all four reasons with counts; legend visible. | 3 |
| US-16 | As an **admin**, I want to see products with the most size-related returns as a horizontal bar chart. | Top 10 products ranked by (too_small + too_large) count; chart sorted descending. | 5 |
| US-17 | As an **admin**, I want to see KPI cards (total orders, returns, return rate, products) at the top of the dashboard. | Four cards visible; values reflect live DB counts. | 2 |
| US-18 | As a **developer**, I want a seed script that populates 30 products and 200 orders/returns so I can demo the app. | Script runs without errors; creates 30 products with size charts, 50 users, and ≥200 orders including returns. | 5 |
| US-19 | As a **developer**, I want unit tests for the recommendation engine so I can verify logic changes don’t break it. | Tests cover: exact match, closest match, no size chart, XS/XXL edge cases, too_small/too_large bias shifts. Pytest passes. | 8 |
| US-20 | As a **developer**, I want unit tests for auth routes so I can prevent regressions. | Tests cover: register success/duplicate/mismatch, login success/failure, logout, role-based 403. | 5 |
| US-21 | As a **developer**, I want a GitHub Actions CI pipeline that runs pytest on every PR. | Workflow runs on push/PR to main/develop; tests pass on Python 3.11 and 3.12; build fails if tests fail. | 3 |
| US-22 | As a **developer**, I want a Dockerfile and docker-compose.yml so the app runs in containers. | `docker-compose up` starts MySQL + Flask; app accessible on port 5000; migrations + seed run automatically. | 5 |
| US-23 | As a **developer**, I want database indexes on brand_id, category, and product_id so queries are fast. | SQLAlchemy models declare `index=True` on these columns; verified in migration. | 2 |
| US-24 | As a **customer**, I want all forms protected by CSRF tokens so my account is safe. | Flask-WTF CSRF enabled globally; all POST forms include `{{ form.hidden_tag() }}`; CSRF errors return 400. | 3 |
| US-25 | As a **developer**, I want a comprehensive README with setup steps, ER diagram, and architecture notes so new contributors can onboard quickly. | README includes: problem statement, Mermaid ER diagram, local + Docker setup, how recommendation works, Definition of Done, future improvements. | 3 |
