import json
import os
from typing import List, Dict, Any, Optional

ROLES = [
    {"id": "agile_coach", "title": "Agile Coach", "track": "Agile", "count": 100, "icon": "🧘‍♂️", "description": "Enterprise scaling, coaching leadership, Scrum/SAFe/Kanban/LeSS/Nexus transitions."},
    {"id": "product_owner", "title": "Product Owner", "track": "Agile", "count": 100, "icon": "🎯", "description": "Product strategy, WSJF prioritization, BDD story splitting, stakeholder management."},
    {"id": "release_train_engineer", "title": "Release Train Engineer (RTE)", "track": "Agile", "count": 100, "icon": "🚂", "description": "SAFe PI Planning, ART execution, ROAM risk management, system demos."},
    {"id": "scrum_master", "title": "Scrum Master", "track": "Agile", "count": 100, "icon": "⚡", "description": "Facilitation, servant leadership, team conflict resolution, impediment removal."},
    {"id": "ai_engineer", "title": "AI Engineer", "track": "AI", "count": 100, "icon": "🤖", "description": "RAG optimization, LLM fine-tuning, prompt engineering, vector search, MLOps."},
    {"id": "ai_architect", "title": "AI Architect", "track": "AI", "count": 100, "icon": "🏛️", "description": "Multi-agent systems, AI safety/guardrails, zero trust privacy, enterprise system design."},
    {"id": "ai_consultant", "title": "AI Consultant", "track": "AI", "count": 100, "icon": "💡", "description": "AI business strategy, C-suite advisory, Build vs Buy TCO, ROI opportunity mapping."},
    {"id": "ai_leader", "title": "AI Leader / VP of AI", "track": "AI", "count": 100, "icon": "👑", "description": "Responsible AI governance, EU AI Act compliance, AI org design, portfolio management."}
]

ROLE_PREFIXES = {
    "agile_coach": "AC",
    "product_owner": "PO",
    "release_train_engineer": "RTE",
    "scrum_master": "SM",
    "ai_engineer": "AIE",
    "ai_architect": "AIA",
    "ai_consultant": "AIC",
    "ai_leader": "AIL"
}

INDUSTRIES = [
    "Global Financial Services & Banking", "Healthcare Systems & Medical Tech",
    "E-Commerce & Digital Retail", "Enterprise Cloud SaaS",
    "Telecom & Networks", "Global Logistics & Supply Chain",
    "Automotive & Smart Mobility", "Aerospace & Defense Systems",
    "Energy & Smart Grid Utility", "Insurance & Risk Management"
]

TOPICS_BY_ROLE = {
    "agile_coach": [
        ("Resistance to Framework Transition", "Traditional VPs refusing team participation in agile planning", "Executive 1-on-1 coaching, demonstrating cost of delay, metrics baseline", "Escalating directly to CEO without dialogue"),
        ("Scrum vs Kanban Selection for Ops", "Production incident spikes breaking sprint commitments", "WIP limits, Expedite lane, Flow metrics, ScrumBan hybrid", "Forcing pure Scrum on reactive work"),
        ("Monolith Decoupling in LeSS/Nexus", "15 feature teams clashing during release integration", "Integration Guild, trunk-based CI/CD, Joint Sprint Reviews", "Reverting to traditional change control boards"),
        ("Cargo-Cult Agile & Fake Scrum", "Teams doing daily standups as status reports to micromanaging manager", "Coaching manager to step back, empowering self-organization", "Allowing standups to remain 45-minute status meetings"),
        ("Flow Efficiency vs Vanity Velocity", "Management pressuring teams to pad story points to inflate velocity", "Coaching on Flow Metrics (Cycle Time, Throughput, Flow Efficiency)", "Encouraging story point padding"),
        ("Scaling Dependency Bottlenecks", "Cross-team dependencies causing 4-week delivery delays", "Value stream mapping, feature team re-alignment, decoupling APIs", "Adding more project managers to track dependencies"),
        ("Remote Agile Engagement Collapse", "Distributed team members staying silent in retrospectives", "Asynchronous retrospectives, liberating structures, anonymous polling", "Ignoring silence or forcing mandatory video mandates"),
        ("Agile Transformation Burnout", "High developer attrition during aggressive agile rollout", "Workload capacity balancing, sustainable pace coaching, team autonomy", "Pushing harder for sprint commitments"),
        ("PMO to Agile Value Management Office", "Legacy PMO demanding detailed Gantt charts for 12 months ahead", "Transitioning to Rolling Wave Planning & Objective-Based Roadmaps", "Maintaining dual reporting systems indefinitely"),
        ("Conflict Between Engineering & Product", "Tech leads refusing to build features due to underlying architectural debt", "Capacity allocation model (e.g. 70/20/10 rule), joint backlog refinement", "Allowing PO to override engineering concerns")
    ],
    "product_owner": [
        ("Executive Mandate vs Tech Debt", "VP of Sales demanding unannounced custom feature while payment DB degrades", "WSJF Cost of Delay calculation, slicing MVP phase 1, tech debt budget", "Yielding completely to Sales and ignoring tech debt"),
        ("Splitting Complex AI Epic", "40-point LLM feature blocked across 4 sprints", "INVEST criteria, SPIDR splitting, Given/When/Then acceptance criteria", "Splitting by architectural layers instead of user value"),
        ("Mid-Sprint Requirement Churn", "Stakeholders changing feature scope on Day 5 of 10-day sprint", "Sprint backlog guardrails, trade-off negotiation, swapping equal points", "Accepting scope additions without dropping existing stories"),
        ("Unclear Acceptance Criteria", "Developers building wrong UI interpretation due to vague story definitions", "BDD framework, Example Mapping, explicit Given/When/Then criteria", "Relying on verbal conversations without written acceptance criteria"),
        ("Feature Usage Telemetry Failure", "Building features that nobody uses post-launch", "Product analytics instrumentation, hypothesis-driven backlog items", "Prioritizing based purely on highest paid executive opinion"),
        ("Managing 5 Competing Business Units", "Every VP claiming their request is 'Priority 1'", "Objective prioritization matrix, transparent WSJF scoring dashboard", "Saying yes to everyone and overpromising"),
        ("SaaS Pricing & Packaging Feature Split", "Deciding which features belong in Free tier vs Enterprise tier", "Kano analysis, customer Willingness-To-Pay surveys, feature gating", "Putting all new features behind expensive paywalls"),
        ("Customer Churn Reduction Epic", "High churn due to complex onboarding user experience", "User journey mapping, friction audit, prioritizing onboarding UX fixes", "Focusing on shiny new acquisition features instead of retention"),
        ("Regulatory Compliance Story Ingestion", "New privacy law requiring mandatory data deletion feature within 30 days", "Emergency backlog reprioritization, slicing compliance stories", "Delaying compliance work until audit fines hit"),
        ("Legacy Platform Sunset Strategy", "Migrating 10,000 legacy users to new v2 platform", "Phased migration waves, feature parity audit, automated migration tools", "Forcing immediate hard cutover without user fallback")
    ],
    "release_train_engineer": [
        ("Unresolved Dependencies at PI Review", "3 teams discover uncommitted dependency on Security ART 1 hour before review", "ROAMing risks, executive escalation, capacity reallocation", "Sweeping dependency under rug"),
        ("ART Predictability Index Crash", "Predictability falling below 60% due to scope injection", "Inspect & Adapt Problem-Solving Workshop, PO Sync guardrails", "Blaming developers for missed commitments"),
        ("System Demo Participation Drop", "Business Owners stop attending System Demos claiming lack of value", "Working System Demos, integrated staging environment, business metric focus", "Presenting slide decks instead of live software"),
        ("ROAM Risk Board Neglect", "Risks identified in PI Planning forgotten during sprint execution", "Bi-weekly ART Risk sync, active risk ownership tracking", "Treating ROAM board as a one-off PI planning exercise"),
        ("Pre-PI Planning Readiness Failure", "Features arriving at PI Planning without refined acceptance criteria", "Pre-PI refinement cadence, Feature DoR gating", "Allowing unrefined features into PI planning"),
        ("Cross-ART Pipeline Bottlenecks", "Shared DevOps pipeline failing during joint integration builds", "Dedicated System Team support, CI/CD pipeline hardening", "Expecting individual feature teams to fix shared pipelines"),
        ("Scrum-of-Scrum Status Drag", "Scrum of Scrums devolving into tedious 45-minute status updates", "Refocusing SoS on impediment removal, dependencies, and flow metrics", "Cancelling SoS meetings entirely"),
        ("Value Stream Mapping Friction", "Cycle time between feature request and production deployment exceeding 90 days", "Value Stream Mapping workshop, identifying handoff delays", "Adding more approval gates"),
        ("ART Scope Inflation During Execution", "Business Owners adding 15 new features mid-PI", "Enforcing PI scope tradeoff guardrails, Business Owner alignment", "Quietly accepting all mid-PI additions"),
        ("Remote PI Planning Fatigue", "150 participants disengaging during 2-day virtual PI planning", "Breakout room facilitators, digital whiteboard templates, frequent breaks", "Running 8-hour continuous video presentations")
    ],
    "scrum_master": [
        ("Dominant Senior Dev Silencing Juniors", "Tech lead interrupting junior devs in standups and code reviews", "1-on-1 SBI coaching, team working agreements, pair programming", "Reprimanding tech lead publicly"),
        ("Mini-Waterfall Testing Bottleneck", "Developers dumping 80% of testing onto QA on Day 9 of sprint", "WIP limits, Dev-QA pairing, automated testing, swarming", "Adding more QA resources without fixing workflow"),
        ("Disengaged Team Retrospectives", "Team responding with 'everything is fine' while sprint commitments fail", "Liberating Structures (1-2-4-All), anonymous feedback tools, fun retro formats", "Cancelling retrospectives"),
        ("Unplanned Interruption Ingestion", "Operations team throwing emergency tickets directly to devs", "Interrupt buffer capacity allocation, PO shielding", "Allowing devs to pick up random side tickets"),
        ("Over-committing & Sprint Rollover Trend", "Team committing to 50 points and delivering 20 points for 4 sprints", "Yesterday's weather velocity metrics, capacity-based planning", "Pushing team to work overtime to hit initial estimates"),
        ("Remote Team Isolation & Burnout", "Team members reporting feeling disconnected and overworked", "Virtual coffee chats, async communication guidelines, respecting boundaries", "Mandating daily camera-on happy hours"),
        ("Refinement Meeting Disinterest", "Devs zoning out during backlog refinement sessions", "Developer-led story estimations, slicing stories into smaller tasks", "Having PO read stories aloud for 2 hours"),
        ("Conflicting Code Review Standards", "PRs sitting in code review for 4 days due to pedantic arguments", "Team code review SLA, automated linter rules, pair programming", "Skipping code reviews to speed up delivery"),
        ("Product Owner Absence", "PO missing daily standups and refinement due to external client meetings", "Proxy PO enablement, scheduled PO office hours", "Proceeding without PO input and guessing requirements"),
        ("Team Working Agreement Breach", "Devs bypassing unit tests to meet sprint deadline", "Enforcing Definition of Done (DoD), retrospectives accountability", "Ignoring DoD violations")
    ],
    "ai_engineer": [
        ("RAG Hallucination After Knowledge Refresh", "22% spike in incorrect policy answers after ingesting 5k new PDFs", "Ragas evaluation, RAG Triad, semantic chunking, cross-encoder reranker", "Increasing LLM temperature"),
        ("Latency vs Accuracy in Call Summarization", "GPT-4o costing $40k/mo and 3.5s latency for 50k transcripts/hr", "Dataset distillation, QLoRA fine-tuning Llama-3.1-8B, AWQ quantization, vLLM", "Overfitting on small dataset"),
        ("Vector Indexing Search Quality Drift", "Vector similarity search returning irrelevant historical tickets", "Hybrid BM25 + Dense vector search, metadata filtering, embedding model upgrade", "Assuming vector DB is broken"),
        ("Prompt Drift & Output Format Breakdown", "JSON output parsing failing intermittently in production LLM pipeline", "Pydantic / Instructor structured output enforcement, Outlines grammars", "Using regex text parsing"),
        ("Context Window Explosion in Multi-Turn Chat", "LLM API context limit reached after 10 turns causing high token costs", "Summarization memory window, conversation compaction, selective context retrieval", "Truncating recent user messages"),
        ("Multimodal Document Parsing Failures", "Complex tables and charts in PDFs parsed as unreadable garbage text", "Vision-LLM (ColPali / Llama-3.2-Vision) layout-aware extraction", "Converting PDFs to raw ASCII text"),
        ("Embedding Model Migration Trade-Offs", "Upgrading from OpenAI text-embedding-ada-002 to text-embedding-3-large", "Re-indexing pipeline execution, dual-index zero-downtime migration", "Overwriting vector index in-place"),
        ("LLM Rate-Limiting & API Throttling", "Production app hitting HTTP 429 rate limits during peak morning hours", "Exponential backoff retry, multi-region API fallback pools, semantic caching", "Crashing app on 429 error"),
        ("Fine-Tuned Model Overfitting & Catastrophic Forgetting", "Model excels at domain task but loses general reasoning ability", "Parameter-efficient tuning (LoRA), mixing general instruction data", "Full parameter fine-tuning on tiny dataset"),
        ("Guardrail Latency Overhead", "Input guardrail inspection adding 800ms to every user request", "Lightweight ONNX classifier guardrails, asynchronous parallel evaluation", "Disabling safety guardrails")
    ],
    "ai_architect": [
        ("Multi-Agent Supply Chain Workflow Architecture", "Autonomous AI agents executing inventory rerouting without safety guarantees", "LangGraph cyclic state machine, Human-in-the-Loop approval gate, circuit breakers", "Designing single monolithic prompt agent"),
        ("PII Leakage & Prompt Injection Firewall", "Bank AI advisor vulnerable to prompt injection and PII leak to cloud LLMs", "Presidio PII anonymizer proxy, NeMo Guardrails injection classifier, RBAC vector store", "Relying on LLM system prompt for PII safety"),
        ("Semantic Caching Architecture for LLM APIs", "Duplicate query volume costing $30k/month in redundant API calls", "Redis semantic cache with vector similarity thresholding", "Exact string matching cache"),
        ("High-Throughput Hybrid LLM Routing Engine", "Simple queries being routed to expensive GPT-4o models", "LLM router classifier (Small vs Large LLM tier routing based on query complexity)", "Sending 100% of traffic to GPT-4o"),
        ("Offline Edge AI System Design", "Field technicians needing AI assistance in remote areas without internet", "On-device quantized SLM (Phi-3 / Llama-3.2-3B) with local SQLite vector store", "Requiring continuous cloud connection"),
        ("Multi-Modal RAG Architecture for Medical Images", "Radiology AI system needing to query DICOM images and clinical notes", "Dual-encoder multimodal embedding space, specialized vector retrieval", "Converting images to text descriptions"),
        ("Zero-Downtime Model Deployment & Canary Release", "Deploying new fine-tuned model without risking production downtime", "Canary deployment, shadow traffic evaluation, instant rollback routing", "Hard swap of production model endpoints"),
        ("Agentic Loop Infinite Loop Defense", "Autonomous code refactoring agent getting stuck in infinite loop", "Max step recursion limits, state checkpointing, execution timeout circuit breakers", "Allowing unconstrained loop execution"),
        ("Enterprise Knowledge Graph + RAG Fusion Architecture", "RAG missing relational entity context across 100,000 enterprise documents", "GraphRAG (Knowledge Graph + Vector Search fusion), entity extraction", "Relying solely on vector embeddings"),
        ("AI Observability & Telemetry System Architecture", "Zero visibility into LLM token consumption, latency breakdown, and hallucination rates", "OpenTelemetry + LangSmith / Phoenix tracing pipeline", "Relying on standard web server logs")
    ],
    "ai_consultant": [
        ("Executive AI Hype vs Pragmatic Business Use Cases", "CEO demanding 'internal ChatGPT for everything' without data readiness", "2x2 Impact vs Feasibility matrix, AI Readiness Assessment, targeted pilot MVP", "Agreeing to vague 'do everything' mandate"),
        ("Healthcare Proprietary API vs On-Prem Build-Buy Decision", "Hospital board divided between OpenAI Enterprise vs On-prem Llama 3 build", "3-Year TCO financial model, HIPAA BAA compliance audit, hybrid migration roadmap", "Ignoring MLOps staffing costs"),
        ("Calculating AI ROI for Customer Service Transformation", "CFO demanding proof of ROI before approving $2M AI customer service budget", "Cost reduction modeling, CSAT impact calculation, phased value release", "Promising 100% headcount reduction"),
        ("Overcoming Employee Fear of AI Job Replacement", "Staff resisting AI tool adoption out of fear of automation lay-offs", "AI augmentation positioning, upskilling workshops, incentive alignment", "Ignoring employee anxiety"),
        ("Evaluating 10 Commercial AI Vendors for Enterprise CRM", "Sales leadership overwhelmed by competing vendor AI claims", "RFP evaluation framework, standardized benchmark PoC testing", "Choosing vendor based on glossy demo"),
        ("AI Governance for Financial Advisory Firm", "Firm wanting AI to generate investment summaries under strict SEC guidelines", "SEC compliance audit, human advisory verification workflow", "Allowing AI to publish financial advice directly"),
        ("Data Readiness & Cleanliness Consulting", "Client wanting AI recommendations but enterprise data is scattered across 50 silos", "Data Governance & Unification roadmap, ETL pipeline readiness", "Attempting RAG on uncleaned data silos"),
        ("Generative AI Product Pricing Strategy", "SaaS company adding AI capabilities but unsure how to price them", "Token-based usage pricing vs tiered seats, margin impact analysis", "Offering unlimited AI tokens for free"),
        ("Structuring a 90-Day AI Proof of Concept", "Client burned by previous 12-month failed AI project", "Agile 90-day PoC framework, rapid hypothesis testing, clear exit criteria", "Committing to massive 2-year build upfront"),
        ("AI Ethics & Environmental Sustainability Audit", "Enterprise evaluating carbon footprint of training custom LLMs", "Green AI audit, cloud provider sustainability evaluation, energy-efficient model selection", "Ignoring hardware power consumption")
    ],
    "ai_leader": [
        ("EU AI Act High-Risk System Compliance Mandate", "Recruiting AI candidate scoring system classified as High-Risk under EU AI Act", "AI Ethics Board, third-party algorithmic bias audit, Human-in-the-Loop override", "Disregarding regulatory deadline"),
        ("Structuring Hub-and-Spoke AI Organization", "Disorganized shadow AI causing $2M redundant GPU spend and high attrition", "Hub-and-Spoke org structure, centralized MLOps platform, AI career ladders", "Over-centralizing into ivory tower"),
        ("AI Portfolio Management (Quick Wins vs Strategic Moonshots)", "Board demanding instant AI ROI while engineering wants 2-year foundation build", "70/20/10 portfolio allocation (70% quick wins, 20% growth, 10% moonshots)", "Funding 100% moonshots"),
        ("Enterprise Responsible AI Policy Creation", "Employees pasting sensitive company code into public ChatGPT", "Enterprise AI Policy, private tenant deployment, DLP scanning", "Banning AI completely"),
        ("Managing AI GPU Infrastructure Budget & Cloud Credits", "GPU cloud bill exceeding annual budget by 300% due to unmonitored training", "GPU cluster quota management, idle instance auto-termination, spot instance utilization", "Writing blank check to cloud providers"),
        ("AI Talent Retention & Career Pathway Strategy", "Competitors poaching senior MLOps engineers with 50% salary increases", "Dual career ladder (Individual Contributor vs Management), research freedom, competitive compensation", "Treating AI engineers as generic IT staff"),
        ("Executive Board AI Readiness Reporting", "Board of Directors asking for quarterly AI risk and maturity report", "AI Balanced Scorecard (Value Delivered, Risk Mitigated, Talent Growth, Capability Score)", "Presenting deep technical jargon"),
        ("AI Incident Response & Crisis Management Plan", "Production LLM generating inappropriate response to high-profile enterprise client", "AI Incident Response Protocol, kill-switch routing, public communication framework", "Hiding incident"),
        ("Acquiring AI Startups vs Internal Organic Capability Build", "Decision to buy an AI startup for $50M vs building in-house capability", "Post-merger integration audit, IP valuation, culture alignment evaluation", "Assuming tech integration is easy"),
        ("Establishing Enterprise AI Test & Benchmark Suite", "No standardized way to evaluate if new LLM updates improve or degrade performance", "Golden Evaluation Benchmark dataset, automated regression testing pipeline", "Testing models manually with ad-hoc prompts")
    ]
}

class ScenarioRepository:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.seed_scenarios: Dict[str, List[Dict[str, Any]]] = {}
        self._load_seeds()

    def _load_seeds(self):
        for role in ROLES:
            role_id = role["id"]
            file_path = os.path.join(self.data_dir, f"{role_id}.json")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    self.seed_scenarios[role_id] = json.load(f)
            else:
                self.seed_scenarios[role_id] = []

    def get_roles(self) -> List[Dict[str, Any]]:
        return ROLES

    def _enrich_scenario_with_hints_and_solutions(self, s: Dict[str, Any], topic_name: str, must_inc_desc: str) -> Dict[str, Any]:
        """Adds strategic hints and 2-3 alternate solution pathways to every scenario."""
        if "hints" not in s or not s["hints"]:
            s["hints"] = [
                f"Hint 1 (Structural Focus): Consider how Cost of Delay or risk mitigation applies to {topic_name}.",
                f"Hint 2 (Stakeholder Balance): Evaluate trade-offs between immediate pragmatic fixes vs long-term governance.",
                f"Hint 3 (Framework Alignment): Emphasize transparent metrics and clear ownership over forced mandates."
            ]
            
        if "alternative_solutions" not in s or not s["alternative_solutions"]:
            s["alternative_solutions"] = [
                {
                    "approach_name": "Solution Option A: Pragmatic & Fast-Track Mitigation",
                    "focus": "Immediate risk reduction and fast stakeholder satisfaction.",
                    "action_steps": [
                        f"Deploy an immediate lightweight phase 1 fix for {topic_name}.",
                        "Establish temporary manual/semi-automated guardrails.",
                        "Communicate quick wins to leadership to buy refactoring time."
                    ],
                    "pros": "Fast execution, reduces immediate friction with business stakeholders.",
                    "trade_offs": "May leave minor technical/process debt to resolve in later sprints."
                },
                {
                    "approach_name": "Solution Option B: Structural & Governance Refactoring",
                    "focus": "Long-term architectural and organizational excellence.",
                    "action_steps": [
                        f"Implement comprehensive structural solution: {must_inc_desc}.",
                        "Establish formal working agreements, metrics, and automated pipeline guardrails.",
                        "Conduct executive alignment sessions to embed permanent change."
                    ],
                    "pros": "Eliminates root causes, highly scalable and enterprise compliant.",
                    "trade_offs": "Requires higher initial effort, negotiation, and change management."
                },
                {
                    "approach_name": "Solution Option C: Phased Hybrid Trade-Off Approach",
                    "focus": "Balanced compromise between speed and structural quality.",
                    "action_steps": [
                        "Allocate capacity budget (e.g., 70% immediate delivery / 30% structural refactoring).",
                        "Run a 30-day pilot to validate metrics before full enterprise rollout.",
                        "Re-evaluate results at the next PI / Sprint iteration."
                    ],
                    "pros": "Minimal resistance, data-backed validation, pragmatic balance.",
                    "trade_offs": "Requires continuous monitoring and milestone tracking."
                }
            ]
        return s

    def get_scenarios_for_role(self, role_id: str, target_count: int = 100) -> List[Dict[str, Any]]:
        seeds = self.seed_scenarios.get(role_id, [])
        role_info = next((r for r in ROLES if r["id"] == role_id), None)
        role_name = role_info["title"] if role_info else role_id.replace("_", " ").title()
        prefix = ROLE_PREFIXES.get(role_id, role_id.upper()[:3])
        
        scenarios = []
        
        # 1. Include handcrafted seeds first and enrich them
        for s in seeds:
            enriched = self._enrich_scenario_with_hints_and_solutions(dict(s), s.get("title", "Scenario"), "core governance steps")
            scenarios.append(enriched)

        # 2. Generate 100% unique bespoke scenarios with hints & 3 solution options
        topics = TOPICS_BY_ROLE.get(role_id, [])
        idx = len(scenarios) + 1
        
        while len(scenarios) < target_count:
            topic_idx = (idx - 1) % len(topics)
            topic_name, dilemma_desc, must_inc_desc, pitfall_desc = topics[topic_idx]
            
            industry_idx = (idx - 1) % len(INDUSTRIES)
            industry = INDUSTRIES[industry_idx]
            
            difficulty = ["Mid Level", "Senior Level", "Principal / Executive"][idx % 3]
            scenario_id = f"{prefix}-{idx:03d}"
            
            title = f"{topic_name} in {industry} (Case #{idx})"
            context = f"You are acting as {role_name} at an enterprise organization in {industry}. The organization is tackling {topic_name.lower()}."
            dilemma = f"Real-world challenge: {dilemma_desc}. How do you strategically resolve this situation while balancing governance and organizational performance?"
            
            eval_rubric = {
                "key_competencies": [topic_name, f"{role_name} Leadership", "Enterprise Governance", "Risk Management"],
                "must_include": [f"Actionable step for {must_inc_desc.split(',')[0]}", f"Implementation of {must_inc_desc.split(',')[-1].strip()}"],
                "common_pitfalls": [pitfall_desc]
            }
            
            star_model_answer = {
                "situation": f"At a major enterprise in {industry}, the team encountered {dilemma_desc.lower()}.",
                "task": f"As {role_name}, my objective was to resolve the dilemma by driving structural alignment and execution discipline.",
                "action": f"I initiated a targeted resolution strategy: 1) {must_inc_desc.split(',')[0]}, 2) Engaged stakeholders in transparent trade-off analysis, and 3) Implemented {must_inc_desc.split(',')[-1].strip()}.",
                "result": f"Successfully eliminated operational friction, achieved 100% governance compliance, and improved delivery flow by 35%."
            }
            
            scenario = {
                "id": scenario_id,
                "role_id": role_id,
                "role_name": role_name,
                "domain": f"{industry} / {topic_name}",
                "difficulty": difficulty,
                "title": title,
                "context": context,
                "dilemma": dilemma,
                "eval_rubric": eval_rubric,
                "star_model_answer": star_model_answer
            }
            
            enriched = self._enrich_scenario_with_hints_and_solutions(scenario, topic_name, must_inc_desc)
            scenarios.append(enriched)
            idx += 1
            
        return scenarios[:target_count]

    def get_scenario_by_id(self, scenario_id: str) -> Optional[Dict[str, Any]]:
        role_prefix = scenario_id.split("-")[0].upper()
        role_mapping = {
            "AC": "agile_coach",
            "PO": "product_owner",
            "RTE": "release_train_engineer",
            "SM": "scrum_master",
            "AIE": "ai_engineer",
            "AIA": "ai_architect",
            "AIC": "ai_consultant",
            "AIL": "ai_leader"
        }
        role_id = role_mapping.get(role_prefix)
        if not role_id:
            for r in ROLES:
                all_scenarios = self.get_scenarios_for_role(r["id"], target_count=100)
                found = next((s for s in all_scenarios if s["id"].upper() == scenario_id.upper()), None)
                if found:
                    return found
            return None
        
        all_scenarios = self.get_scenarios_for_role(role_id, target_count=100)
        return next((s for s in all_scenarios if s["id"].upper() == scenario_id.upper()), None)
