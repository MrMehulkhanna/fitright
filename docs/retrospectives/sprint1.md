# Sprint 1 Retrospective — Foundation

**Date:** Week 1 end
**Attendees:** Full-stack developer, QA
**Facilitator:** Developer

---

## What Went Well ✔

- Project scaffolding with Flask application factory pattern was straightforward and clean.
- Flask-WTF CSRF integration worked out of the box with minimal configuration.
- Werkzeug password hashing was simple to add to the User model.
- Docker Compose setup was faster than estimated; the MySQL healthcheck prevented race conditions.
- Seed script Faker data looks realistic enough for demos.

---

## What to Improve ⚠️

- The `.env.example` was not committed early enough; team member had to ask for DB connection string.
- Flask-Migrate initial migration took longer than expected due to Enum type handling in MySQL.
- No linting (flake8/ruff) enforced yet — some PEP8 drift crept in.
- Test environment was not set up during Sprint 1; left for Sprint 4.

---

## Actions ➙

| Action | Owner | Due |
|---|---|---|
| Commit `.env.example` on day 1 of every sprint | Developer | Sprint 2 Day 1 |
| Add `flake8` to `requirements.txt` and run before commits | Developer | Sprint 2 |
| Document Enum MySQL quirks in README troubleshooting section | Developer | Sprint 2 |
