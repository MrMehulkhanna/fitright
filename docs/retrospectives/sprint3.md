# Sprint 3 Retrospective — Orders, Returns & Admin Dashboard

**Date:** Week 3 end
**Attendees:** Full-stack developer, QA
**Facilitator:** Developer

---

## What Went Well ✔

- Chart.js integration was fast; all three chart types rendered correctly first try.
- Admin KPI cards gave instant visual impact in the stakeholder demo.
- The horizontal bar chart for size-related returns by product was immediately actionable — stakeholders identified two products to fix.
- Return flow (order → return form → status update) worked end-to-end without regressions.
- 403 error page was clean and on-brand.

---

## What to Improve ⚠️

- Admin dashboard has no date range filter; all charts show all-time data only.
- The ‘Place Order’ button on the product page needs a confirmation step to prevent accidental orders.
- Return form allowed submission for ‘pending’ orders initially; fixed with status check in route.
- Chart.js data is embedded as Jinja template variables; should be fetched via AJAX for real-time updates.

---

## Actions ➙

| Action | Owner | Due |
|---|---|---|
| Add date range filter to admin dashboard | Developer | Backlog (future sprint) |
| Add order confirmation modal (JS) to product page | Developer | Sprint 4 buffer |
| Refactor chart data to API endpoints for real-time fetching | Developer | Backlog |
