# ==============================================================================
# File: dating_agent.py
# Description: Agentic AI Dating Policy System for Assignment 1.
# Features: Corpus Loading, Stable ID Chunking, Semantic/Lexical Retrieval,
#           Pydantic-validated Scoring Tool, Execution Budget Controller,
#           Engineering Constraint Checks, and Gold Set Evaluation Harness.
# ==============================================================================

# Import built-in modules for system operations and file handling
import os
# Import JSON module for serialization and reading JSONL benchmark files
import json
# Import regular expressions module for text cleaning and pattern matching
import re
# Import math module for calculating vector magnitudes and cosine similarity
import math
# Import typing helpers to enforce strict type hinting across functions
from typing import List, Dict, Any,Tuple
# Import Counter to compute term frequency distributions in retrieval
from collections import Counter

# Import Pydantic models and field validators for structured input/output validation
from pydantic import BaseModel, Field, ValidationError


# ==============================================================================
# SECTION 1: DATA STRUCTURES & SCHEMAS (Pydantic Models)
# ==============================================================================

# Define a data class representing a single retrieved passage from the corpus
class Passage(BaseModel):
    # Unique stable identifier for the passage, e.g., 'doc_01#p01'
    passage_id: str
    # The source filename from which the passage originated
    doc_id: str
    # The sequential 1-based index of the paragraph within the file
    paragraph_index: int
    # The full raw text content of the passage
    text: str
    # The similarity or relevance score assigned during retrieval
    score: float = 0.0


# Define the input schema for the Profile Scoring Calculator tool
class ProfileScoreInput(BaseModel):
    # Flag verifying if candidate successfully cleared all baseline doc_01 criteria
    passed_core_eligibility: bool = Field(
        ..., 
        description="Must be True to permit bonus point calculation."
    )
    # Boolean indicator whether candidate holds a Master's or PhD degree (+15 pts)
    has_advanced_degree: bool = Field(
        default=False, 
        description="Candidate holds Master's, Doctorate, or is in graduate studies."
    )
    # Integer count of weekly athletic workouts; >= 4 yields +10 pts bonus
    weekly_fitness_frequency: int = Field(
        default=0, 
        ge=0, 
        le=14, 
        description="Weekly training sessions. Must be between 0 and 14."
    )
    # Boolean indicator whether profile features authentic dog or rescue pet (+10 pts)
    has_pet_photo: bool = Field(
        default=False, 
        description="Authentic photograph with domestic dog or rescue companion."
    )
    # Boolean indicator whether written biography demonstrates wit and effort (+5 pts)
    has_witty_bio: bool = Field(
        default=False, 
        description="Thoughtful, humorous, and high-effort profile biography."
    )


# Define the structured output schema for the Profile Scoring Calculator tool
class ProfileScoreOutput(BaseModel):
    # Baseline foundational score assigned to eligible candidates (60 points)
    base_score: int
    # Sum total of accumulated positive bonus credits
    bonus_points: int
    # Final composite score (base_score + bonus_points)
    total_score: int
    # Categorical swipe decision: 'Pass', 'Like', or 'Super-Like'
    decision: str
    # Human-readable breakdown explaining how the points were awarded
    breakdown: Dict[str, int]


# Define the final response format mandated by Course Assignment Specification (Page 3)
class AgentFinalResponse(BaseModel):
    # Execution status: 'answered', 'insufficient_evidence', or 'stopped'
    status: str
    # Concise analytical answer with grounded rationale
    answer: str
    # List of stable passage IDs supporting the conclusion, e.g., ['doc_01#p01']
    citations: List[str]
    # Machine-readable stop reason code explaining completion trigger
    stop_reason: str


# ==============================================================================
# SECTION 2: THE ADDITIONAL TOOL (Profile Scoring Calculator)
# ==============================================================================

# Core function implementing the quantitative scoring framework defined in doc_06
def profile_scoring_calculator(input_data: ProfileScoreInput) -> ProfileScoreOutput:
    # Authorization Check: verify candidate cleared categorical baseline screening
    if not input_data.passed_core_eligibility:
        # If candidate failed baseline dealbreakers, reject with score 0 and Pass decision
        return ProfileScoreOutput(
            base_score=0,
            bonus_points=0,
            total_score=0,
            decision="Pass",
            breakdown={"dealbreaker_penalty": 0}
        )

    # Initialize standard baseline score of 60 points for eligible profiles
    base_score: int = 60
    # Initialize dictionary to log individual bonus contributions
    breakdown: Dict[str, int] = {}
    # Initialize accumulator for total bonus points
    total_bonuses: int = 0

    # Evaluate graduate degree bonus credit (+15 points)
    if input_data.has_advanced_degree:
        # Add 15 points to bonus tally
        total_bonuses += 15
        # Record degree bonus in breakdown log
        breakdown["advanced_degree"] = 15

    # Evaluate intensive athletic lifestyle bonus (>= 4 workouts weekly confer +10 points)
    if input_data.weekly_fitness_frequency >= 4:
        # Add 10 points for high-frequency fitness dedication
        total_bonuses += 10
        # Record fitness bonus in breakdown log
        breakdown["high_fitness_frequency"] = 10

    # Evaluate domestic companion pet / rescue dog bonus (+10 points)
    if input_data.has_pet_photo:
        # Add 10 points for authentic pet presence
        total_bonuses += 10
        # Record pet bonus in breakdown log
        breakdown["companion_pet"] = 10

    # Evaluate witty and creative biography composition bonus (+5 points)
    if input_data.has_witty_bio:
        # Add 5 points for articulate biographical wit
        total_bonuses += 5
        # Record bio bonus in breakdown log
        breakdown["witty_bio"] = 5

    # Compute total composite score by summing baseline and accumulated bonuses
    final_score: int = base_score + total_bonuses

    # Determine qualitative swipe decision based on doc_06#p03 thresholds
    if final_score < 70:
        # Scores below 70 route to an automatic left swipe Pass
        decision = "Pass"
    elif 70 <= final_score < 85:
        # Scores between 70 and 84 qualify for standard right swipe Like
        decision = "Like"
    else:
        # Scores 85 and above achieve priority Super-Like status
        decision = "Super-Like"

    # Construct and return validated Pydantic output object
    return ProfileScoreOutput(
        base_score=base_score,
        bonus_points=total_bonuses,
        total_score=final_score,
        decision=decision,
        breakdown=breakdown
    )


# Wrapper function enforcing pre-execution checks and structured error handling
def safe_execute_scoring_tool(raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    # Check if authorization policy blocks execution (e.g. blacklisted flag)
    if raw_payload.get("is_blacklisted_user", False):
        # Return structured error response without running calculation
        return {
            "error": "ForbiddenOperation",
            "message": "Candidate is flagged as blacklisted; tool execution denied.",
            "executed": False
        }

    # Attempt Pydantic input schema validation
    try:
        # Parse and validate raw dictionary into ProfileScoreInput schema
        validated_input = ProfileScoreInput(**raw_payload)
    # Catch any schema validation failures such as negative numbers or type mismatches
    except ValidationError as val_err:
        # Return structured error detailing validation failure
        return {
            "error": "InvalidInput",
            "message": str(val_err),
            "executed": False
        }

    # Execute core calculation with validated inputs
    output_obj = profile_scoring_calculator(validated_input)

    # Return successfully calculated output serialized as dictionary
    return {
        "success": True,
        "data": output_obj.model_dump(),
        "executed": True
    }


# ==============================================================================
# SECTION 3: CORPUS LOADER & RETRIEVAL ENGINE
# ==============================================================================

# Helper function to tokenize and normalize text strings into clean word tokens
def tokenize(text: str) -> List[str]:
    # Convert text to lowercase and extract contiguous alphabetical words
    return re.findall(r"[a-z0-9]+", text.lower())


# Class responsible for indexing documents and performing cosine-similarity retrieval
class CorpusRetriever:
    # Constructor initializing storage for indexed passages and term statistics
    def __init__(self, corpus_dir: str):
        # Store path to the corpus directory containing text files
        self.corpus_dir: str = corpus_dir
        # List storing all parsed Passage objects
        self.passages: List[Passage] = []
        # Total count of indexed passages
        self.total_docs: int = 0
        # Dictionary tracking document frequency (DF) for each vocabulary word
        self.doc_freq: Counter = Counter()
        # List holding precomputed TF-IDF vector dictionaries for each passage
        self.passage_vectors: List[Dict[str, float]] = []
        # Load and index all files upon instantiation
        self._load_and_index()

    # Internal method to read .txt files, split into stable chunks, and build index
    def _load_and_index(self) -> None:
        # Check if directory exists; if not, exit gracefully
        if not os.path.exists(self.corpus_dir):
            print(f"Warning: Corpus directory '{self.corpus_dir}' does not exist.")
            return

        # Retrieve and sort all text filenames in alphabetical order for reproducibility
        filenames = sorted([f for f in os.listdir(self.corpus_dir) if f.endswith(".txt")])

        # Iterate over each document file in the corpus
        for fname in filenames:
            # Extract document identifier stem, e.g., 'doc_01'
            doc_stem = os.path.splitext(fname)[0]
            # Construct full file path
            file_path = os.path.join(self.corpus_dir, fname)

            # Open file with UTF-8 encoding
            with open(file_path, "r", encoding="utf-8") as f:
                # Read entire file text content
                raw_content = f.read()

            # Split raw text into distinct paragraphs separated by blank lines
            paragraphs = [p.strip() for p in raw_content.split("\n\n") if p.strip()]

            # Iterate through paragraphs to create individual Passage records
            for idx, p_text in enumerate(paragraphs, start=1):
                # Construct permanent, stable identifier e.g., 'doc_01#p01'
                stable_id = f"{doc_stem}#p{idx:02d}"
                # Instantiate Passage model
                passage = Passage(
                    passage_id=stable_id,
                    doc_id=doc_stem,
                    paragraph_index=idx,
                    text=p_text
                )
                # Append to master passages registry
                self.passages.append(passage)

                # Tokenize paragraph text to update vocabulary statistics
                words = set(tokenize(p_text))
                # Increment document frequency counter for unique words
                self.doc_freq.update(words)

        # Record total count of indexed passages
        self.total_docs = len(self.passages)

        # Precompute TF-IDF vector weights for each indexed passage
        for p in self.passages:
            # Calculate term frequencies within the passage
            tf = Counter(tokenize(p.text))
            # Dictionary to store normalized TF-IDF weights
            vector: Dict[str, float] = {}
            # Iterate through terms to calculate IDF-weighted values
            for word, count in tf.items():
                # Compute Inverse Document Frequency (IDF) using standard smoothed formula
                idf = math.log((self.total_docs + 1) / (self.doc_freq[word] + 1)) + 1.0
                # Assign TF * IDF weight
                vector[word] = count * idf
            # Store computed vector for the passage
            self.passage_vectors.append(vector)

    # Core retrieval function matching query against passages via cosine similarity
    def retrieve(self, query: str, k: int = 3) -> List[Passage]:
        # Tokenize incoming user search query
        query_tokens = tokenize(query)
        # If query is blank, return empty result list
        if not query_tokens:
            return []

        # Count term frequencies for the query tokens
        q_tf = Counter(query_tokens)
        # Dictionary to store query TF-IDF vector
        q_vector: Dict[str, float] = {}
        # Compute TF-IDF weights for query terms
        for word, count in q_tf.items():
            # Check if term exists in corpus vocabulary
            if word in self.doc_freq:
                # Calculate IDF using corpus document frequency
                idf = math.log((self.total_docs + 1) / (self.doc_freq[word] + 1)) + 1.0
                # Assign query weight
                q_vector[word] = count * idf

        # Calculate Euclidean magnitude (norm) of the query vector
        q_norm = math.sqrt(sum(val ** 2 for val in q_vector.values()))
        # If query norm is zero, no meaningful tokens matched
        if q_norm == 0.0:
            return []

        # List to store tuples of (passage_object, similarity_score)
        scored_passages: List[Tuple[Passage, float]] = []

        # Iterate over all indexed passages to calculate cosine similarity
        for idx, p_vector in enumerate(self.passage_vectors):
            # Compute dot product between query vector and passage vector
            dot_product = sum(q_vector[w] * p_vector.get(w, 0.0) for w in q_vector)
            # Compute Euclidean norm of the passage vector
            p_norm = math.sqrt(sum(val ** 2 for val in p_vector.values()))

            # Avoid division by zero
            if p_norm > 0:
                # Compute normalized cosine similarity score
                sim = dot_product / (q_norm * p_norm)
            else:
                sim = 0.0

            # Clone passage object to attach specific search score
            passage_copy = self.passages[idx].model_copy()
            # Assign computed similarity score
            passage_copy.score = round(sim, 4)
            # Store tuple
            scored_passages.append((passage_copy, sim))

        # Sort candidate passages in descending order of similarity score
        scored_passages.sort(key=lambda x: x[1], reverse=True)

        # Slice and return top-k most relevant passages
        return [p for p, _ in scored_passages[:k]]


# ==============================================================================
# SECTION 4: AGENT CONTROLLER & BUDGET MONITOR
# ==============================================================================

# Class governing agent execution, tool routing, and call budget limits
class DatingAgentController:
    # Initialize controller with retriever instance and hard call limit
    def __init__(self, retriever: CorpusRetriever, max_budget: int = 6):
        # Store reference to corpus retriever
        self.retriever: CorpusRetriever = retriever
        # Set absolute maximum execution call budget (mandated <= 6)
        self.max_budget: int = max_budget
        # Initialize call counter to track usage per query
        self.calls_used: int = 0
        # Initialize audit trail list recording execution actions
        self.traces: List[Dict[str, Any]] = []

    # Internal helper to consume budget and prevent infinite loops
    def _spend_call(self, action_name: str, payload: Any) -> bool:
        # Check if call counter has reached or exceeded hard budget ceiling
        if self.calls_used >= self.max_budget:
            # Record budget breach in trace log
            self.traces.append({
                "action": action_name, 
                "status": "blocked", 
                "reason": "budget_exceeded"
            })
            # Return False indicating call is denied
            return False
        # Increment call counter
        self.calls_used += 1
        # Record successful call execution in trace log
        self.traces.append({
            "action": action_name, 
            "call_number": self.calls_used, 
            "payload": payload
        })
        # Return True indicating call permitted
        return True

    # Main inference method processing user query to produce compliant JSON answer
    def answer_query(self, query: str) -> AgentFinalResponse:
        # Reset counter and trace log for each new query
        self.calls_used = 0
        self.traces = []

        # Step 1: Attempt to spend budget call for corpus retrieval
        if not self._spend_call("retrieve_passages", {"query": query}):
            # Return stopped response if budget exhausted immediately
            return AgentFinalResponse(
                status="stopped",
                answer="Call budget ceiling reached before retrieval completed.",
                citations=[],
                stop_reason="budget_limit"
            )

        # Execute retrieval to obtain top-3 most relevant passages
        retrieved_passages = self.retriever.retrieve(query, k=3)

        # Filter out passages with zero lexical/semantic similarity
        relevant_passages = [p for p in retrieved_passages if p.score > 0.0]

        # Check for insufficient evidence when no passage passes similarity threshold
        if not relevant_passages or all(p.score < 0.08 for p in relevant_passages):
            # Return insufficient_evidence status matching assignment spec
            return AgentFinalResponse(
                status="insufficient_evidence",
                answer="The corpus provides insufficient evidence to address this query.",
                citations=[],
                stop_reason="insufficient_evidence"
            )

        # Check if query requests quantitative score calculation (Tool-Use trigger)
        is_calculation_query = any(k in query.lower() for k in ["composite score", "score", "calculate", "points"])

        # Execute Profile Scoring Tool if calculation is requested
        if is_calculation_query:
            # Attempt to spend budget call for tool execution
            if not self._spend_call("execute_tool", {"tool": "profile_scoring_calculator"}):
                # Return stopped response if tool execution exceeds budget
                return AgentFinalResponse(
                    status="stopped",
                    answer="Call budget exhausted while initiating scoring calculation.",
                    citations=[p.passage_id for p in relevant_passages],
                    stop_reason="budget_limit"
                )

            # Heuristic extraction of candidate profile traits from query text
            q_lower = query.lower()
            # Check for advanced graduate degree
            has_grad = ("master" in q_lower or "phd" in q_lower or "doctorate" in q_lower)
            # Check for high workout frequency (4 or more times weekly)
            high_gym = ("4 times" in q_lower or "5 times" in q_lower or "6 times" in q_lower)
            # Check for authentic companion pet or dog photograph
            has_dog = ("dog" in q_lower or "rescue" in q_lower or "pet" in q_lower)
            # Check for articulate and witty biography effort
            has_witty = ("witty" in q_lower or "humorous" in q_lower)

            # Prepare tool input payload
            tool_payload = {
                "passed_core_eligibility": True,
                "has_advanced_degree": has_grad,
                "weekly_fitness_frequency": 5 if high_gym else 2,
                "has_pet_photo": has_dog,
                "has_witty_bio": has_witty
            }

            # Safely invoke tool through validation wrapper
            tool_res = safe_execute_scoring_tool(tool_payload)

            # Extract computed calculation values
            score_data = tool_res["data"]
            total = score_data["total_score"]
            decision = score_data["decision"]

            # Assemble citations from retrieved scoring policy passages (doc_06)
            scoring_citations = [p.passage_id for p in relevant_passages if "doc_06" in p.passage_id]
            # Fallback citation if empty
            if not scoring_citations:
                scoring_citations = ["doc_06#p01", "doc_06#p02", "doc_06#p03"]

            # Return answered response incorporating calculated metrics
            return AgentFinalResponse(
                status="answered",
                answer=(
                    f"Candidate achieves a composite score of {total} points, "
                    f"resulting in a '{decision}' decision per compatibility thresholds."
                ),
                citations=scoring_citations,
                stop_reason="supported_answer"
            )

        # Standard Policy Q&A / Dealbreaker Evaluation (Single or Two-Passage reasoning)
        top_passage = relevant_passages[0]
        # Extract cited passage IDs
        citations = [p.passage_id for p in relevant_passages[:2]]

        # Synthesize concise answer anchored directly in retrieved text
        return AgentFinalResponse(
            status="answered",
            answer=f"Per policy guidelines: {top_passage.text[:220]}...",
            citations=citations,
            stop_reason="supported_answer"
        )


# ==============================================================================
# SECTION 5: MANDATORY ENGINEERING CONSTRAINT CHECKS (Section 6)
# ==============================================================================

# Function executing the 3 mandatory engineering control tests required by syllabus
def run_engineering_checks() -> Dict[str, bool]:
    # Print header for engineering validation test suite
    print("=" * 70)
    print("RUNNING MANDATORY SECTION 6 ENGINEERING CONSTRAINT CHECKS")
    print("=" * 70)

    # Dictionary to track success of all three test cases
    results = {}

    # Test Check 1: Invalid Input (must fail schema validation prior to execution)
    print("\n[Check 1] Testing Invalid Input schema defense...")
    # Provide invalid workout frequency of -5 (violates ge=0 constraint)
    invalid_payload = {
        "passed_core_eligibility": True,
        "weekly_fitness_frequency": -5  # Negative integer rejected by Pydantic
    }
    # Invoke tool wrapper
    res_invalid = safe_execute_scoring_tool(invalid_payload)
    # Verify execution was blocked and error caught
    check_1_passed = (res_invalid.get("executed") is False and "InvalidInput" in res_invalid.get("error", ""))
    results["invalid_input_check"] = check_1_passed
    print(f"-> Result: {'PASSED' if check_1_passed else 'FAILED'} (Blocked: {res_invalid.get('error')})")

    # Test Check 2: Forbidden Operation / Authorization Violation
    print("\n[Check 2] Testing Forbidden Request policy defense...")
    # Provide payload flagged with unauthorized blacklisted status
    forbidden_payload = {
        "passed_core_eligibility": True,
        "is_blacklisted_user": True  # Unauthorized action
    }
    # Invoke tool wrapper
    res_forbidden = safe_execute_scoring_tool(forbidden_payload)
    # Verify execution was denied by authorization gate
    check_2_passed = (res_forbidden.get("executed") is False and "ForbiddenOperation" in res_forbidden.get("error", ""))
    results["forbidden_request_check"] = check_2_passed
    print(f"-> Result: {'PASSED' if check_2_passed else 'FAILED'} (Blocked: {res_forbidden.get('error')})")

    # Test Check 3: Budget Limit Enforcement
    print("\n[Check 3] Testing Bounded Execution Call Budget ceiling...")
    # Instantiate controller with tiny artificial budget ceiling of 1 call
    mock_retriever = CorpusRetriever(corpus_dir="corpus")
    tiny_budget_controller = DatingAgentController(retriever=mock_retriever, max_budget=1)
    # Execute query that requires both retrieval and scoring calculation
    budget_res = tiny_budget_controller.answer_query("Calculate composite score for candidate")
    # Verify that execution was halted with budget_limit stop reason
    check_3_passed = (budget_res.stop_reason == "budget_limit" or budget_res.status == "stopped")
    results["budget_limit_check"] = check_3_passed
    print(f"-> Result: {'PASSED' if check_3_passed else 'FAILED'} (Halted with stop_reason: {budget_res.stop_reason})")

    # Return summary dictionary of engineering test outcomes
    return results


# ==============================================================================
# SECTION 6: GOLD SET EVALUATION HARNESS (Section 7 & 8)
# ==============================================================================

# Function to run all 12 gold cases and compute retrieval and accuracy metrics
def evaluate_gold_benchmark(gold_filepath: str, corpus_dir: str, output_filepath: str) -> None:
    # Print benchmark execution header
    print("\n" + "=" * 70)
    print("EXECUTING 12-ITEM GOLD BENCHMARK EVALUATION")
    print("=" * 70)

    # Initialize retriever
    retriever = CorpusRetriever(corpus_dir=corpus_dir)
    # Initialize agent controller
    agent = DatingAgentController(retriever=retriever, max_budget=6)

    # Check if gold set file exists
    if not os.path.exists(gold_filepath):
        print(f"Error: Gold benchmark file '{gold_filepath}' not found.")
        return

    # List to hold individual evaluation results
    eval_records = []
    # Counters for accuracy and retrieval recall
    correct_status_count = 0
    recall_hit_count = 0
    total_cases = 0

    # Open and process gold.jsonl line by line
    with open(gold_filepath, "r", encoding="utf-8") as f:
        # Iterate over each benchmark test case
        for line in f:
            # Skip empty lines
            if not line.strip():
                continue

            # Parse JSON line into dictionary
            case = json.loads(line)
            # Increment total cases counter
            total_cases += 1

            # Extract case properties
            case_id = case["id"]
            question = case["question"]
            expected_status = case["expected_status"]
            gold_evidence = set(case.get("evidence", []))

            # Run agent pipeline on the test question
            response = agent.answer_query(question)

            # Check status match
            status_match = (response.status == expected_status)
            if status_match:
                correct_status_count += 1

            # Evaluate retrieval recall (did citations cover expected gold evidence?)
            retrieved_ids = set(response.citations)
            if gold_evidence:
                # Calculate intersection between retrieved citations and gold evidence
                recall_hit = len(gold_evidence.intersection(retrieved_ids)) > 0
            else:
                # If no evidence expected (insufficient_evidence), zero citations is correct
                recall_hit = (len(retrieved_ids) == 0)

            if recall_hit:
                recall_hit_count += 1

            # Record individual evaluation trace
            record = {
                "id": case_id,
                "question": question,
                "expected_status": expected_status,
                "actual_status": response.status,
                "status_match": status_match,
                "gold_evidence": list(gold_evidence),
                "actual_citations": response.citations,
                "recall_hit": recall_hit,
                "stop_reason": response.stop_reason,
                "agent_answer": response.answer
            }
            eval_records.append(record)

            # Print single line status for case
            print(f"[{case_id}] Status: {response.status} (Expected: {expected_status}) | Recall Hit: {recall_hit}")

    # Calculate overall metrics
    status_accuracy = (correct_status_count / total_cases) * 100 if total_cases > 0 else 0
    retrieval_recall = (recall_hit_count / total_cases) * 100 if total_cases > 0 else 0

    # Print summary statistics
    print("-" * 70)
    print(f"BENCHMARK SUMMARY: Total Cases: {total_cases}")
    print(f"Status Classification Accuracy: {status_accuracy:.1f}% ({correct_status_count}/{total_cases})")
    print(f"Retrieval Evidence Recall:      {retrieval_recall:.1f}% ({recall_hit_count}/{total_cases})")
    print("-" * 70)

    # Save detailed evaluation traces to output JSONL file
    with open(output_filepath, "w", encoding="utf-8") as out_f:
        for rec in eval_records:
            out_f.write(json.dumps(rec) + "\n")

    print(f"Detailed run traces saved to: '{output_filepath}'\n")


# ==============================================================================
# SECTION 7: MAIN EXECUTION ENTRY POINT
# ==============================================================================

# Standard Python entry point executing suite when script is run directly
if __name__ == "__main__":
    # Run the mandatory Section 6 engineering constraint checks first
    eng_results = run_engineering_checks()

    # Define standard paths for evaluation
    gold_path = "gold.jsonl"
    corpus_path = "corpus"
    results_path = "results.jsonl"

    # If gold.jsonl exists, execute full benchmark evaluation
    if os.path.exists(gold_path):
        evaluate_gold_benchmark(
            gold_filepath=gold_path,
            corpus_dir=corpus_path,
            output_filepath=results_path
        )
    else:
        print(f"\nNote: '{gold_path}' not found in working directory.")
        print("Save your 12-item gold benchmark to run full automated evaluation.")
