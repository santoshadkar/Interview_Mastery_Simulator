# 🚀 Scenario-Based Interview Simulation Portal

An enterprise-grade, interactive interview simulation platform covering **800+ real-world scenario questions**, **STAR evaluation rubrics**, **3 alternate solution pathways**, and **strategic interview hints** across 8 Agile and AI leadership roles.

---

## 🌟 Supported Roles & Tracks (800+ Unique Scenarios)

### ⚡ Agile Transformation Track (400+ Scenarios)
1. **Agile Coach (100 Scenarios)**: Enterprise scaling, framework transitions (Scrum, SAFe, Kanban, Scrumban, LeSS, Nexus), executive coaching, flow metrics.
2. **Product Owner (100 Scenarios)**: WSJF prioritization, BDD story splitting (Given/When/Then), tech debt vs feature velocity trade-offs.
3. **Release Train Engineer (100 Scenarios)**: SAFe PI Planning facilitation, ROAM risk management, ART predictability index, system demos.
4. **Scrum Master (100 Scenarios)**: Servant leadership, toxic conflict resolution, retrospective facilitation, impediment removal.

### 🤖 AI Leadership & Architecture Track (400+ Scenarios)
5. **AI Engineer (100 Scenarios)**: RAG Triad groundedness, vector DB indexing/reranking, QLoRA fine-tuning, vLLM inference acceleration.
6. **AI Architect (100 Scenarios)**: Multi-Agent LangGraph state machines, PII masking gateways, NeMo Guardrails, zero-trust cloud proxies.
7. **AI Consultant (100 Scenarios)**: C-suite AI strategy advisory, 2x2 Impact vs Feasibility matrices, 3-Year TCO Build vs Buy evaluations.
8. **AI Leader / VP of AI (100 Scenarios)**: EU AI Act & NIST AI RMF compliance, Hub-and-Spoke CoE organization design, AI career ladders.

---

## 🎯 Key Features

- **100% Unique Scenarios**: 800 bespoke scenarios with zero duplicate IDs, titles, or dilemmas.
- **💡 Strategic Hints**: Expandable hints providing structural focus, stakeholder balance, and framework alignment pointers.
- **🔀 3 Alternate Solution Pathways**: Trade-off analysis breakdown for Option A (Pragmatic/Fast-track), Option B (Structural/Governance), and Option C (Phased Hybrid).
- **⚡ STAR Evaluation Engine**: Instant 0-100% readiness score, STAR checklist (Situation, Task, Action, Result), matched competencies, missed rubrics, and gold-standard model answers.
- **📑 Dedicated Role Tabs**: Clean 1-click navigation tabs grouped by Agile and AI tracks.
- **📄 Dynamic Pagination**: Browse questions 1-20, 21-40, 41-60, 61-80, 81-100 effortlessly.

---

## 🛠️ Quick Start & Local Execution

### Prerequisites
- Python 3.10+ installed.
- No third-party dependencies required (uses native Python standard library).

### Running the Server
```bash
# Clone the repository
git clone https://github.com/santoshadkar/Interview_Mastery_Simulator.git
cd Interview_Mastery_Simulator

# Start the web portal server
python run_server.py
```

Open your browser at **`http://localhost:8000`**.

---

## 🧪 Running Automated Tests

To run the full unit and integration test suite:

```bash
python -m unittest discover -s tests
```

Tests cover scenario repository loading, target 100 counts per role, 100% scenario uniqueness checks, evaluation engine scoring, and REST API endpoints.

---

## 🏛️ Project Architecture & Governance

```
scenario-interview-portal/
├── .env.example              # Environment parameters
├── README.md                 # Project documentation
├── run_server.py             # Root execution entrypoint
├── docs/                     # Governance & API documentation
│   ├── pi_planning_board.md  # SAFe PI Planning Board
│   ├── api_spec.json         # OpenAPI 3.0 REST Specification
│   ├── qa_test_report.md     # QA Audit Sign-off Report
│   └── retrospective.md      # PI-1 Retrospective Report
├── data/                     # Data layer (Handcrafted seed datasets)
│   └── scenarios/
├── src/
│   ├── domain/               # Business logic & repository engines
│   │   ├── scenario_repository.py
│   │   ├── evaluation_engine.py
│   │   └── statistics_tracker.py
│   ├── api/
│   │   └── server.py         # REST API HTTP Handler
│   └── ui/
│       └── index.html        # Single Page Application Frontend
└── tests/                    # Automated Test Suite
    ├── test_scenario_repository.py
    ├── test_evaluation_engine.py
    └── test_api.py
```

---

## 📄 License

MIT License. Built for Enterprise Agile & AI Leadership Interview Mastery.
