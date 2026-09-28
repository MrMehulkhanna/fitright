# Development Methodology: Why Scrum?

## Overview

FitRight was developed using **Scrum**, an agile framework built around short, time-boxed iterations (sprints), regular inspect-and-adapt ceremonies, and a prioritised product backlog.

## Why Scrum over Kanban?

Kanban is a flow-based system with no fixed cadence. It works well for support teams or maintenance work with unpredictable, continuous demand. FitRight, however, had **clearly bounded features** (auth, catalog, recommendation engine, admin dashboard) and a stakeholder who wanted **predictable delivery checkpoints**. Scrum’s fixed sprint rhythm (1 week) gave us:

- A forcing function to slice stories to completable chunks
- Regular retrospectives that caught process issues early (e.g., missing `.env.example`, no linting)
- Velocity tracking that let us replan Sprint 3 when the Chart.js work was faster than estimated

Kanban would have been appropriate if the team were in a pure operations mode, continuously triaging bugs and support requests without a defined feature roadmap.

## Why Scrum over Waterfall?

Waterfall requires complete requirements upfront and delivers working software only at the end of the project. FitRight’s **recommendation engine logic** — particularly the return-feedback bias threshold — was a design decision that needed real data and stakeholder feedback to validate. With Waterfall, we would have built it once, shipped it at the end, and discovered too late that the 30% threshold was wrong. Scrum let us demo the engine at the end of Sprint 2, get feedback (“the confidence label needs a tooltip explaining what ‘Low’ means”), and adjust in Sprint 3.

Waterfall also assumes stable requirements. In fashion e-commerce, category structures, sizing conventions, and return reason taxonomies change frequently. Scrum’s backlog grooming let us reprioritise without derailing the project.

## Summary

| Factor | Waterfall | Kanban | **Scrum** |
|---|---|---|---|
| Predictable delivery dates | ✔ (plan-driven) | ✖ | ✔ (sprint boundaries) |
| Handles changing requirements | ✖ | ✔ | ✔ |
| Regular stakeholder feedback | ✖ | Partial | ✔ (sprint reviews) |
| Suits a fixed-scope MVP | Partial | ✖ | ✔ |
| Team size fit (1–3 people) | ✔ | ✔ | ✔ |

Scrum was the right tool: it imposed just enough structure to keep a solo developer accountable and goal-directed, while preserving the flexibility to refine the recommendation engine based on real feedback.
