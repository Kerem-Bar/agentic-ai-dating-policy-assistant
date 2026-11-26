# <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/robot.svg" width="28" height="28" valign="middle"> Agentic AI Dating Policy Assistant: Architectural Design, Bounded Verification, and Failure Analysis

An empirical Agentic AI policy decision assistant operating over a modular regulatory corpus (`doc_01`–`doc_06`). The architecture integrates an exact Vector Space Model (VSM) lexical retriever, a Pydantic-validated quantitative scoring tool, a deterministic fixed-workflow controller with bounded execution limits, and a frozen 12-item gold benchmark (`gold.jsonl`) to diagnose retrieval bottlenecks and synthesis failure modes.

![](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![](https://img.shields.io/badge/Pydantic-v2.0%2B_Schemas-E92063?style=flat&logo=pydantic&logoColor=white)
![](https://img.shields.io/badge/Architecture-Fixed_Workflow_Agent-009688?style=flat)
![](https://img.shields.io/badge/Retrieval-VSM_%2F_Cosine_Similarity-5C6BC0?style=flat)
![](https://img.shields.io/badge/Evaluation-Gold_Benchmark_(JSONL)-FF6F00?style=flat)

---

## 📌 Project Overview

This project implements an **Agentic Dating Policy Assistant** designed as a decision-support system for evaluating candidate profiles and chat scenarios encountered on an online dating application. Operating over a modular regulatory corpus (`doc_01`–`doc_06`), the assistant analyzes user-submitted information to recommend grounded platform actions, such as a *Left Swipe (Pass)*, *Right Swipe (Like)*, *Super-Like*, or *Immediate Unmatch*, while reporting `insufficient_evidence` when corpus rules are absent.

Specifically, the system handles four core regulatory tasks:
- **Eligibility & Dealbreaker Screening:** Verifying demographic, lifestyle, visual, and relationship-intent criteria.
- **Communication, Conduct & Date Protocol Enforcement:** Monitoring messaging cadence, conversational tone, in-person dinner logistics, and identity/privacy safety boundaries.
- **Quantitative Compatibility Scoring:** Computing composite candidate scores via a Pydantic-validated scoring tool.
- **Grounded Abstention & Bounded Execution:** Enforcing strict call budgets and refusing to answer out-of-scope queries lacking corpus support.

To evaluate retrieval and reasoning limitations under strict execution limits, the system deploys an exact Vector Space Model (VSM / Smoothed TF-IDF) as a deterministic baseline, benchmarked across 12 source-based evaluation cases (`gold.jsonl`) and 3 isolated engineering constraint checks.

---

## 📁 Repository Structure

```text
agentic-ai-dating-policy-assistant/
├── corpus/                             # Permitted Policy Corpus (6 documents, 30 passages)
│   ├── doc_01.txt                      # Foundational Screening & Core Dealbreakers
│   ├── doc_02.txt                      # Communication Cadence & Latency Boundaries
│   ├── doc_03.txt                      # Conduct Boundaries & Linguistic Tone
│   ├── doc_04.txt                      # In-Person Date Logistics & Protocol
│   ├── doc_05.txt                      # Identity Verification & Physical Privacy Protocols
│   └── doc_06.txt                      # Quantitative Scoring Matrix & Off-Platform Progression
├── dating_agent.py                     # Core Agent Pipeline, VSM Retriever, Pydantic Tool & Controller
├── gold.jsonl                          # 12 Frozen Evaluation Cases with Ground-Truth Annotations
├── results.jsonl                       # Recorded Benchmark Outputs, Citations & Execution Traces
├── requirements.txt                    # Pinned Runtime Dependencies (Pydantic v2+)
├── report.pdf                          # 4-Page Technical & Empirical Evaluation Report
└── README.md                           # System Documentation & Reproducibility
```

---

## 📑 Corpus Topology & Chunking Strategy

The corpus consists of six modular, self-authored synthetic policy documents totaling 2,121 words across foundational screening (`doc_01`), communication cadence (`doc_02`), conduct boundaries (`doc_03`), date protocol (`doc_04`), security verification (`doc_05`), and quantitative scoring (`doc_06`).

The corpus was segmented into natural **paragraph-level passages** demarcated by blank lines (`\n\n`), producing an indexed registry of exactly **30 discrete passages** across the six documents (`doc_XX#pYY`). Only source `.txt` documents are indexed; `gold.jsonl`, `results.jsonl`, and `report.pdf` are strictly excluded from the index.

Sentence-level micro-chunking was deliberately avoided based on three information retrieval principles:

- **Contextual Integrity:** Policy directives possess vertical logical dependencies. In `doc_04#p01`, banning takeaway coffee or park walks is grounded in the opening mandate requiring formal restaurant dining. Isolating sentences severs sanctions from their underlying rationale.
- **Mitigating Vector Sparsity:** In sparse lexical models, isolated sentences contain too few tokens to match paraphrased inquiries. Paragraph units preserve sufficient term density for reliable cosine similarity matching.
- **Narrative Policy Structure:** Regulatory texts follow a narrative progression rather than an "inverted pyramid." General principles appear first, while operative sanctions (e.g., *"results in an immediate unmatch"*) appear at paragraph ends. Paragraph chunking ensures the entire regulatory envelope is indexed intact.

### Corpus Registry Table

<table>
  <thead>
    <tr>
      <th align="left"><small>Document ID</small></th>
      <th align="left"><small>Canonical Title</small></th>
      <th align="center"><small>Origin & Version</small></th>
      <th align="center"><small>Passages</small></th>
      <th align="center"><small>Words</small></th>
      <th align="left"><small>Core Regulatory Scope</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><small><code>doc_01.txt</code></small></td>
      <td><small>Foundational Screening</small></td>
      <td align="center"><small>Synthetic (v1.0)</small></td>
      <td align="center"><small>8 (<code>p01</code>–<code>p08</code>)</small></td>
      <td align="center"><small>632</small></td>
      <td><small>Age bracket (27–36), 15km Tel Aviv perimeter, solo photo, non-smoking, fitness, degree, job, bio, relationship intent.</small></td>
    </tr>
    <tr>
      <td><small><code>doc_02.txt</code></small></td>
      <td><small>Communication Cadence</small></td>
      <td align="center"><small>Synthetic (v1.0)</small></td>
      <td align="center"><small>5 (<code>p01</code>–<code>p05</code>)</small></td>
      <td align="center"><small>371</small></td>
      <td><small>24h initiation window, 72h / 20-turn in-app lock, quiet hours (23:00–07:00), no unsolicited media/double-texting, 5-day stalling limit.</small></td>
    </tr>
    <tr>
      <td><small><code>doc_03.txt</code></small></td>
      <td><small>Conduct Boundaries</small></td>
      <td align="center"><small>Synthetic (v1.0)</small></td>
      <td align="center"><small>6 (<code>p01</code>–<code>p06</code>)</small></td>
      <td align="center"><small>424</small></td>
      <td><small>Substantive openers, linguistic effort, no premature endearments, question reciprocity, 6-month post-breakup buffer (≥4y), intent consistency.</small></td>
    </tr>
    <tr>
      <td><small><code>doc_04.txt</code></small></td>
      <td><small>Date Protocol</small></td>
      <td align="center"><small>Synthetic (v1.0)</small></td>
      <td align="center"><small>4 (<code>p01</code>–<code>p04</code>)</small></td>
      <td align="center"><small>270</small></td>
      <td><small>Sit-down restaurant mandate, public venues only, 48h advance notice & reservation under candidate's name, independent transportation.</small></td>
    </tr>
    <tr>
      <td><small><code>doc_05.txt</code></small></td>
      <td><small>Security Verification</small></td>
      <td align="center"><small>Synthetic (v1.0)</small></td>
      <td align="center"><small>3 (<code>p01</code>–<code>p03</code>)</small></td>
      <td align="center"><small>193</small></td>
      <td><small>Mandatory blue biometric checkmark, ≥4 unobstructed diverse photos, exact address/workplace privacy defense, anti-solicitation rules.</small></td>
    </tr>
    <tr>
      <td><small><code>doc_06.txt</code></small></td>
      <td><small>Quantitative Scoring</small></td>
      <td align="center"><small>Synthetic (v1.0)</small></td>
      <td align="center"><small>4 (<code>p01</code>–<code>p04</code>)</small></td>
      <td align="center"><small>231</small></td>
      <td><small>Scoring: 60-pt baseline + bonuses (+15 grad, +10 fitness ≥4/wk, +10 pet, +5 witty bio)<br>Thresholds: Pass (&lt;70), Like (70–84), Super-Like (≥85)<br>Policy: Post-match progression rules</small></td>
  </tbody>
</table>

---

## 🔬 System Architecture, Settings & Execution Limits

### Operational Configuration & Design Rationale

The retrieval, routing, and runtime parameters governing the controller are configured to balance precision, determinism, and bounded execution:

- **Retrieval Model & Index:** Pure-Python Vector Space Model using Smoothed TF-IDF weighting and cosine similarity over lowercased, tokenized source passages.
- **Top-k Selection (`k`):** Supports any `k >= 1`, defaulting to `k = 3`. Setting `k = 3` enables multi-clause quantitative scoring queries (e.g., `case_09`, `case_10`) to capture up to three rule passages (`doc_06#p01`–`p03`) while functioning as a noise buffer. When distracting profile attributes push unrelated documents into the top two ranks, a `k = 3` window prevents `doc_06` passages from being completely crowded out during post-retrieval filtering, ensuring the tool output remains grounded in explicit policy citations rather than returning an ungrounded calculation.
- **Deterministic Tie Handling:** Ties in cosine similarity scores are broken deterministically via Python's stable sort over passages indexed in ascending `passage_id` order, ensuring reproducible ordering.
- **Query Routing & Response Formulation:** Post-retrieval routing separates the two query pipelines:
  - *Standard Policy Q&A Queries:* Narrows citations to the top two passages (`relevant_passages[:2]`) to preserve precision and returns an extractive snippet capped at the leading 220 characters (`top_passage.text[:220]`).
  - *Quantitative Calculation Queries:* Triggered by scoring keywords (`composite score`, `score`, `calculate`, `points`), restricts citations exclusively to `doc_06` passages and delegates computation to the external scoring tool (detailed in the following section).
- **Similarity Noise Gate (`tau = 0.08`):** Sparse lexical TF-IDF relies on exact token overlap rather than dense semantic embeddings, meaning paraphrased queries naturally yield low cosine similarity scores. A conservative threshold of `tau = 0.08` is designed to filter out near-zero noise and unsupported out-of-scope queries (e.g., `case_11`, `case_12`) while retaining valid paraphrased matches.
- **Execution Limits:** Hard limit of `max_budget = 6` retrieval or tool calls per query (1 retrieval call for standard Q&A; 1 retrieval + 1 tool call for scoring queries) and an explicit loop guard (`max_steps = 6`) to prevent infinite loops.
- **Runtime & Environment:** Local Python 3.10+ execution using standard library modules (`math`, `re`, `json`, `pathlib`, `dataclasses`) and `pydantic` (`>=2.0`), with zero external LLM APIs, vector databases, or network calls.

### Deterministic Query Execution Workflow

Execution is governed by a deterministic **fixed workflow controller** (`DatingAgentController`). The controller itself selects every sequential transition without autonomous looping, enforcing bounded execution and citation provenance:

```text
                   +---------------------------------------+
                      |              User Query               |
                      +---------------------------------------+
                                          |
                                          v
+--------------------------------------------------------------------------------------+
| DatingAgentController (Fixed Workflow | Hard Limit: max_budget = 6 calls)            |
|                                                                                      |
| 1. Spend Call: retrieve_passages(query, k=3)                                         |
|    +--> CorpusRetriever: Smoothed IDF + Euclidean Cosine Similarity                  |
|    +--> Similarity Noise Gate: tau = 0.08                                            |
|                                                                                      |
| 2. Deterministic Routing Branch:                                                     |
|    |-- [Calculation Query: "composite score", "score", "calculate", "points"]        |
|    |    +--> Evidence Provenance Filter (doc_06 passages only)                       |
|    |    +--> Spend Call: execute_tool                                                |
|    |    +--> Pre-execution Authorization (is_blacklisted_user)                       |
|    |    +--> Schema Validation (ProfileScoreInput / ProfileScoreOutput)              |
|    |    +--> profile_scoring_calculator() -> Score, Decision & Breakdown             |
|    |                                                                                 |
|    \-- [Standard Policy Q&A]                                                         |
|         +--> Evidence Provenance Filter (relevant_passages[:2])                      |
|         +--> Extractive Output Budget (top_passage.text[:220])                       |
|                                                                                      |
| 3. Structured Output Formulation:                                                    |
|    +--> AgentFinalResponse (logged to results.jsonl):                                |
|         * status     : "answered" | "insufficient_evidence" | "stopped"              |
|         * answer     : Concise string (agent_answer in results.jsonl)                |
|         * citations  : Grounded passage IDs (actual_citations in results.jsonl)      |
|         * stop_reason: "supported_answer" | "insufficient_evidence" | "budget_limit" |
+--------------------------------------------------------------------------------------+
```
---

## 🛠️ Additional Tool: Profile Scoring Calculator

Quantitative scoring queries invoke `profile_scoring_calculator` via `safe_execute_scoring_tool`:

- **Input Schema (`ProfileScoreInput`):** Validates `passed_core_eligibility` (`bool`), `has_advanced_degree` (`bool`, `+15`), `weekly_fitness_frequency` (`int` bounded to `[0, 14]` via `Field(ge=0, le=14)`, `+10` if `>= 4`), `has_pet_photo` (`bool`, `+10`), and `has_witty_bio` (`bool`, `+5`).
- **Output Schema (`ProfileScoreOutput`):** Validates `base_score` (`60`), `bonus_points`, `total_score`, `decision` (`Pass` `< 70`, `Like` `70–84`, `Super-Like` `>= 85`), and itemized `breakdown`.
- **Pre-Execution Defense:** Rejects unauthorized requests (`is_blacklisted_user=True` → `ForbiddenOperation`) and invalid schema inputs (`weekly_fitness_frequency=-5` → `InvalidInput`) prior to tool execution (`executed=False`).

---

## 📊 Benchmark Evaluation & Results

Evaluated under the frozen runtime configuration across all 12 cases in `gold.jsonl` and the 3 engineering constraint checks:

### 🏆 Empirical Benchmark Results Table

<table>
  <thead>
    <tr>
      <th align="left"><small>Case ID</small></th>
      <th align="left"><small>Query Category / Depth</small></th>
      <th align="center"><small>Exp.</small></th>
      <th align="center"><small>Act.</small></th>
      <th align="center"><small>Recall</small></th>
      <th align="left"><small>Actual Citations</small></th>
      <th align="left"><small>Observed Behavior / Outcome</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><small><code>case_01</code></small></td>
      <td><small>Single: Dealbreaker</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>0/1</small></td>
      <td><small><code>doc_01#p02</code>, <code>doc_01#p05</code></small></td>
      <td><small>🔴 Retrieval Miss (Rank drift on age)</small></td>
    </tr>
    <tr>
      <td><small><code>case_02</code></small></td>
      <td><small>Single: Boundary</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>0/1</small></td>
      <td><small><code>doc_02#p01</code>, <code>doc_04#p03</code></small></td>
      <td><small>🔴 Retrieval Miss (Keyword mismatch)</small></td>
    </tr>
    <tr>
      <td><small><code>case_03</code></small></td>
      <td><small>Single: Venue</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>1/1</small></td>
      <td><small><code>doc_04#p01</code>, <code>doc_04#p04</code></small></td>
      <td><small>🟢 Success (Grounded venue rule)</small></td>
    </tr>
    <tr>
      <td><small><code>case_04</code></small></td>
      <td><small>Single: Security</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>1/1</small></td>
      <td><small><code>doc_05#p01</code>, <code>doc_03#p04</code></small></td>
      <td><small>🟢 Success (Grounded checkmark rule)</small></td>
    </tr>
    <tr>
      <td><small><code>case_05</code></small></td>
      <td><small>Single (Para): Linguistic</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>1/1</small></td>
      <td><small><code>doc_03#p03</code>, <code>doc_02#p01</code></small></td>
      <td><small>🟢 Success (Grounded endearment rule)</small></td>
    </tr>
    <tr>
      <td><small><code>case_06</code></small></td>
      <td><small>Single (Para): Breakup Rule</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>1/1</small></td>
      <td><small><code>doc_03#p05</code>, <code>doc_03#p06</code></small></td>
      <td><small>🟢 Success (Grounded breakup rule)</small></td>
    </tr>
    <tr>
      <td><small><code>case_07</code></small></td>
      <td><small>Two-Pass: Progression</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>0/2</small></td>
      <td><small><code>doc_06#p04</code>, <code>doc_04#p04</code></small></td>
      <td><small>🔴 Multi-hop Miss (Missed phone rule)</small></td>
    </tr>
    <tr>
      <td><small><code>case_08</code></small></td>
      <td><small>Two-Pass (Para): Privacy</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>1/2</small></td>
      <td><small><code>doc_04#p04</code>, <code>doc_06#p04</code></small></td>
      <td><small>🟡 Partial Success (Missed privacy)</small></td>
    </tr>
    <tr>
      <td><small><code>case_09</code></small></td>
      <td><small>Tool: Like</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>1/3</small></td>
      <td><small><code>doc_06#p03</code></small></td>
      <td><small>🟡 Calculation Disparity (85 vs 75 pts)</small></td>
    </tr>
    <tr>
      <td><small><code>case_10</code></small></td>
      <td><small>Tool (Para): Super-Like</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>2/3</small></td>
      <td><small><code>doc_06#p02</code>, <code>doc_06#p03</code></small></td>
      <td><small>🟢 Success (Calculated 95 pts)</small></td>
    </tr>
    <tr>
      <td><small><code>case_11</code></small></td>
      <td><small>Out-of-Scope: Height</small></td>
      <td align="center"><small>Insuff</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>0/0</small></td>
      <td><small><code>doc_03#p06</code>, <code>doc_02#p01</code></small></td>
      <td><small>🔴 False Positive (Gate leak on height)</small></td>
    </tr>
    <tr>
      <td><small><code>case_12</code></small></td>
      <td><small>Out-of-Scope: Bill</small></td>
      <td align="center"><small>Insuff</small></td>
      <td align="center"><small>Ans</small></td>
      <td align="center"><small>0/0</small></td>
      <td><small><code>doc_06#p04</code>, <code>doc_04#p04</code></small></td>
      <td><small>🔴 False Positive (Gate leak on bill)</small></td>
    </tr>
    <tr>
      <td colspan="7"><small><strong>Engineering Constraint Checks (All Passed 3/3)</strong></small></td>
    </tr>
    <tr>
      <td><small><code>ctrl_01</code></small></td>
      <td colspan="4"><small>Invalid Input Check: Negative fitness (-5) rejected by schema</small></td>
      <td colspan="2"><small>🟢 Passed (0 tool executions)</small></td>
    </tr>
    <tr>
      <td><small><code>ctrl_02</code></small></td>
      <td colspan="4"><small>Forbidden Request Check: Authorization gate blocked blacklisted user</small></td>
      <td colspan="2"><small>🟢 Passed (0 tool executions)</small></td>
    </tr>
    <tr>
      <td><small><code>ctrl_03</code></small></td>
      <td colspan="4"><small>Call Budget Ceiling Check: Hard budget limit halted execution</small></td>
      <td colspan="2"><small>🟢 Passed (Status: <code>stopped</code>)</small></td>
    </tr>
  </tbody>
</table>

### 📈 Aggregate Quantitative Counts
- **Answerable Task Success:** `6/10` (`60.0%`) - 5 full successes (`case_03`, `case_04`, `case_05`, `case_06`, `case_10`) plus 1 partial-citation success (`case_08`, where `recall_hit = True` on 1/2 passages with an accurate grounded answer).
- **Correct Insufficient Evidence Responses:** `0/2` (`0.0%`) - `case_11` and `case_12` breached `τ = 0.08` due to background tokens.
- **Overall Task Success:** `6/12` (`50.0%`) across the entire gold suite.
- **Material Unsupported Claims:** `3/12` (`25.0%`) - `case_11`, `case_12` (hallucinated answers on absent topics), and `case_09` (score inflation).
- **Engineering Controls Verification:** `3/3` (`100.0%`) - all schema, authorization, and call-limit checks passed.

---

## 🔍 Failure Diagnosis & Next Architectural Improvement

### Root Failure Modes
1. **Lexical Representation Failure, Numerical Blindness & Rank Drift (`case_01`, `case_02`):** In `case_01`, the prompt omitted the keyword `"age"`. Sparse VSM could neither match digits (`"24"`) against textual bounds (*"between twenty-seven and thirty-six"* in `doc_01#p01`) nor evaluate `24 < 27`. Concurrently, compliant attributes (*"Tel Aviv"*, *"bachelor's degree"*) diluted the vector toward `doc_01#p02` and `doc_01#p05` (`Recall = 0/1`). In `case_02`, the model cannot interpret temporal intervals, leaving `"01:30 AM"` with zero lexical overlap against `"23:00"` or `"quiet hours"` (`doc_02#p03`). Instead, query tokens drifted toward `doc_02#p01` (`Recall = 0/1`).
2. **Multi-Hop Retrieval & Extractive Synthesis Bottlenecks (`case_07`, `case_08`):** In `case_07` (sharing a phone number after 4 days and 25 messages to coordinate dinner), dominant dining tokens skewed the undivided query vector toward `doc_06#p04` and `doc_04#p04`, missing both required gold passages: `doc_02#p02` and `doc_04#p01` (`Recall = 0/2`). In `case_08` (a rideshare offer coupled with an exact apartment address request), retrieval captured `doc_04#p04` (`Recall = 1/2`) but missed `doc_05#p03`; furthermore, slicing `retrieved_passages[0].text[:220]` truncated `doc_04#p04` before its refusal directive, and the architecture lacked a generative layer to merge `doc_04#p04` and `doc_05#p03` into a composite verdict preserving the `unmatch` sanction.
3. **Tool-Input Negation Blindness (`case_09`):** Although retrieval successfully grounded the query in `doc_06#p03` (`Recall = 1/3`), naive substring matching detected `"pet"` inside *"has no pet photos"* while ignoring `"no"`, setting `has_pets = True` and inflating the score from `75` (`Like`) to `85` (`Super-Like`).
4. **Permissive Noise-Floor Threshold Leakage (`case_11`, `case_12`):** Generic background tokens (`"candidate"` on height in `case_11`, `"restaurant"` on bill splitting in `case_12`) created incidental lexical overlap with top-cited unrelated passages (`doc_03#p06` and `doc_06#p04`, respectively; `Recall = 0/0`), crossing `τ = 0.08` and triggering false-positive answers instead of abstaining.

### Proposed Upgrade & Target Metrics
Transitioning to a **Two-Stage Semantic Pipeline** pairing a **Dense Vector Index** (dense embeddings) with a **Local LLM Controller** (e.g., LLaMA via Ollama) directly targets all failure modes:
- **Dense Semantic Indexing (`case_01`, `case_02`):** Maps numerical (`"24"` vs. *"twenty-seven"*) and time (`"01:30 AM"` vs. *"quiet hours"*) expressions into a shared semantic space while the LLM evaluates numerical and time bounds.
- **Query Decomposition & Dense Routing (`case_07`):** Decomposes multi-hop prompts into targeted sub-queries routed directly to `doc_02#p02` and `doc_04#p01`.
- **Multi-Passage Synthesis (`case_08`):** Replaces hardcoded `text[:220]` slicing with an LLM generation layer that reconciles disjoint policy rules into a composite verdict and also preserves paragraph-end sanctions in single-passage queries.
- **Syntactic Slot-Filling (`case_09`):** Leveraging the LLM's syntactic dependency awareness to properly interpret negation particles (*"has no pet photos"* -> `has_pets = False`) prevents corrupted tool arguments and decision flipping (`Like` to `Super-Like`), while eliminating reliance on rigid keyword triggers (`"score"`, `"calculate"`, `"points"`).
- **Threshold Recalibration (`case_11`, `case_12`):** Continuous, non-zero semantic vectors naturally yield higher baseline cosine similarity scores, requiring the similarity gate to be calibrated well above `tau = 0.08` to filter out absent topics and prevent false positives.
- **Target Validation:** Re-running the frozen benchmark will test raising **Correct Insufficient Evidence Responses** from `0/2` (`0.0%`) to `2/2` (`100.0%`), alongside gains in **Answerable Task Success** (`> 6/10`) and **Overall Task Success** (`> 6/12`).

---

## 🛡️ Engineering Constraint Checks

Executed separately from the gold content cases, all three engineering controls passed (`3/3`):

```text
[Check 1] Testing Invalid Input schema defense...
-> Result: PASSED (Rejected by Pydantic schema: weekly_fitness_frequency = -5 violates ge=0; 0 tool executions)

[Check 2] Testing Forbidden Request policy defense...
-> Result: PASSED (Blocked by authorization gate: is_blacklisted_user = True denied; 0 tool executions)

[Check 3] Testing Bounded Execution Call Budget ceiling...
-> Result: PASSED (Halted deterministically: max_budget = 1 halted execution with stop_reason = 'budget_limit')
```

---

## 🚀 Setup, Rebuild & Execution Commands

1. **Install Pinned Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Rebuild the Corpus Index:**
   `CorpusRetriever` builds a fresh in-memory TF-IDF index from `corpus/*.txt` on every initialization. To explicitly rebuild and verify the 30 indexed passages:
   ```bash
   python -c "from dating_agent import CorpusRetriever; r = CorpusRetriever('corpus'); print(f'Indexed {r.total_docs} passages across 6 documents.')"
   ```

3. **Run a Single Question:**
   ```bash
   python -c "from dating_agent import CorpusRetriever, DatingAgentController; agent = DatingAgentController(CorpusRetriever('corpus')); print(agent.answer_query('The candidate suggests meeting for takeaway coffee in the park. Is this acceptable?').model_dump_json(indent=2))"
   ```

4. **Evaluate All 12 Gold Cases & Run the 3 Engineering Checks:**
   ```bash
   python dating_agent.py
   ```
   This executes `run_engineering_checks()` (`ctrl_01`–`ctrl_03`), evaluates all 12 cases in `gold.jsonl`, prints summary accuracy/recall metrics, and writes full execution traces to `results.jsonl`.

---


## 👤 Author

**Kerem Bar**<br>
*Master's Student in Applied Data Science & AI Applications*<br>
*Department of Information Science & Artificial Intelligence Applications, Bar-Ilan University*
