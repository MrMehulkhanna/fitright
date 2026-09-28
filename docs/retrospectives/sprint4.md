# Sprint 4 Retrospective — Quality, CI & Documentation

**Date:** Week 4 end
**Attendees:** Full-stack developer, QA
**Facilitator:** QA

---

## What Went Well ✔

- pytest suite covered all critical paths: recommendation engine edge cases (XS clamp, XXL clamp, bias shift), auth (register, login, logout, role access).
- GitHub Actions CI ran green on first push with both Python 3.11 and 3.12 matrix.
- SQLite in-memory DB for tests meant the CI pipeline needed no MySQL service container, keeping it fast (~20 seconds).
- README Mermaid ER diagram rendered correctly on GitHub.
- `docker-compose up --build` worked end-to-end including automatic seed.

---

## What to Improve ⚠️

- Test coverage is functional but doesn’t cover the admin dashboard charts or catalog search.
- No integration test for the full order → return flow.
- `requirements.txt` should be split into `requirements.txt` (prod) and `requirements-dev.txt` (dev + test tools).
- Seed script uses `db.drop_all()` which is destructive; should check for existing data first.

---

## Actions ➙

| Action | Owner | Due |
|---|---|---|
| Add catalog search + admin dashboard tests in next sprint | Developer | Sprint 5 |
| Split requirements into prod/dev files | Developer | Sprint 5 |
| Add `--no-drop` flag to seed script | Developer | Sprint 5 |
| Add `pytest-cov` HTML report to CI artifacts | Developer | Sprint 5 |
