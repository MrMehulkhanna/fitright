# Sprint 2 Retrospective — Catalog & Sizing

**Date:** Week 2 end
**Attendees:** Full-stack developer, QA
**Facilitator:** QA

---

## What Went Well ✔

- Euclidean distance recommendation logic was clean and easy to unit-test.
- Bootstrap 5 card grid for the product catalog looked polished immediately.
- Pagination with Flask-SQLAlchemy’s `.paginate()` worked without custom code.
- The return-feedback bias mechanism was well-received in demo; stakeholders liked the transparency note on the product page.
- Category filter via URL params preserved across pagination correctly.

---

## What to Improve ⚠️

- Measurement form lacked ‘how to measure’ guidance initially; added after QA flagged it.
- Product images used placeholder URLs (picsum); need real images for production demo.
- The recommendation widget on the product page is only visible after login; some testers expected a prompt earlier.
- No loading state shown when the recommendation is computed (though it’s fast, it could feel laggy on slow connections).

---

## Actions ➙

| Action | Owner | Due |
|---|---|---|
| Add a ‘Login to see your size’ prompt prominently on product cards (not just detail page) | Developer | Sprint 3 |
| Investigate real product image sources (Unsplash API, internal assets) | Developer | Backlog |
| Write recommendation unit tests during Sprint 3 buffer, not Sprint 4 | Developer | Sprint 3 |
