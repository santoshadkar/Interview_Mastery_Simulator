# Program Increment (PI-1) Planning Board
**Agile Release Train (ART)**: Scenario Interview Mastery Train  
**RTE**: Release Train Engineer  
**Status**: APPROVED & ACTIVE  

---

## 1. Executive Summary & PI Objectives

### Strategic Theme
Deliver an enterprise-grade Scenario-Based Interview Simulation Portal enabling professionals in Agile Transformation (Agile Coach, PO, RTE, SM) and AI Leadership (AI Engineer, AI Architect, AI Consultant, AI Leader) to master high-stakes real-world interview scenarios.

### Target KPI
- 8 Dedicated Professional Roles/Tracks.
- 100+ High-Impact Scenario Definitions per Role (800+ total scenario database generator & repository).
- Real-time STAR evaluation rubric scoring, missed nuance detection, and feedback reports.
- Zero-hardcoding, clean REST API architecture, full unit test coverage.

---

## 2. Feature & User Story Backlog (PI-1 Sprints)

### Sprint 1: Architecture & Scenario Repository Engine
- **US-101 (Domain Data Model)**: Design and validate standard JSON schema for 8 role tracks.
  - *Given* the scenario generator repository is initialized, *When* querying any of the 8 roles, *Then* it must return structured scenario items containing context, dilemma, evaluation rubrics, and STAR model answers.
- **US-102 (API Specification)**: Solutions Architect produces `docs/api_spec.json`.
  - *Given* an API client, *When* calling `/api/v1/scenarios`, *Then* it returns filtered scenarios with pagination and search metadata.

### Sprint 2: Evaluation Engine & Scoring Matrix
- **US-201 (STAR & Rubric Evaluator)**: Implement heuristic and semantic answer evaluation.
  - *Given* a candidate's submitted text response, *When* evaluated by the engine, *Then* it returns a score percentage (0-100%), competency match breakdown, missed key points, and actionable improvement recommendations.
- **US-202 (Session & Statistics Tracker)**: Track interview drill progress across roles.
  - *Given* a user completes practice drills, *When* accessing the stats dashboard, *Then* it displays overall readiness score, strength areas, and suggested weak-spot scenarios.

### Sprint 3: Interactive Single Page Portal (UI/UX)
- **US-301 (Scenario Master Dashboard)**: Interactive multi-role selection UI.
  - *Given* a user lands on the portal, *When* selecting any of the 8 roles, *Then* it seamlessly displays available scenarios, difficulty filters, and mode selection (Practice, AI Interviewer, Speed Drill).
- **US-302 (Interactive Mock Interviewer View)**: Real-time scenario practice interface with live feedback modal.
  - *Given* a user answers a scenario, *When* clicking "Submit for AI Feedback", *Then* it triggers the evaluation pipeline and renders detailed STAR breakdown cards.

### Sprint 4: QA, CAB Gating & Inspect & Adapt
- **US-401 (Automated Testing & QA Audit)**: Execute unit & integration test suites, output `docs/qa_test_report.md`.
- **US-402 (Retrospective & I&A Report)**: Draft `docs/retrospective.md` concluding PI-1.

---

## 3. ROAM Risk Board

| Risk ID | Description | Impact | Mitigation Strategy | Status |
|---|---|---|---|---|
| R-01 | Large scenario dataset payload causing slow initial UI rendering | Medium | Implement dynamic client-side pagination & lazy loading | **Resolved** |
| R-02 | Inconsistent answer scoring across diverse roles | High | Standardize rubrics with strict keyword & semantic match scoring algorithm | **Resolved** |
| R-03 | Missing role-specific depth for executive AI roles | High | Structure AI Leader/Architect scenarios using NIST AI RMF and EU AI Act standards | **Resolved** |

---

## 4. PI Predictability Index Target

| Sprint | Planned Story Points | Capacity | Commitment Status |
|---|---|---|---|
| Sprint 1 | 13 | 13 | Committed |
| Sprint 2 | 13 | 13 | Committed |
| Sprint 3 | 21 | 21 | Committed |
| Sprint 4 | 8 | 8 | Committed |
| **Total** | **55** | **55** | **100% Target Predictability** |
