# LLM Technical Evaluation & Logic Auditing Benchmark

A curated benchmark portfolio demonstrating rigorous evaluation, error taxonomy classification, and structured technical rationale authoring for synthetic Large Language Model (LLM) outputs.

## Evaluation Framework
Evaluations in this repository follow the **HHH (Helpful, Honest, Harmless)** alignment criteria and the **CER (Claim - Evidence - Reasoning)** rationale structure:

1. **Claim:** Explicitly state the category of failure, boundary violation, or logical inconsistency.
2. **Evidence:** Isolate specific lines of generated code, execution traces, or guideline contradictions.
3. **Reasoning:** Provide algorithmic proof explaining *why* the output fails.
4. **Ground Truth:** Supply an optimized, production-grade correction adhering strictly to all prompt constraints.

## Mock Grading Rubric
| Dimension | Weight | Criteria for 5/5 (Excellent) |
| :--- | :--- | :--- |
| **Instruction Following** | 30% | Strict adherence to all negative constraints and formatting rules. |
| **Truthfulness / Honesty** | 30% | Zero hallucinations; explicitly states uncertainty if applicable. |
| **Logical Rigor** | 20% | Code handles edge-cases (NULLs, empty arrays, negative bounds). |
| **Rationale Quality** | 20% | CER framework applied; algorithmic complexity mathematically proven. |

## Error Taxonomy
- **[LOGIC-EDGE]**: Boundary value failure, infinite loops, off-by-one errors, NULL traps.
- **[PERF-DEGRADE]**: Sub-optimal algorithmic complexity (e.g., $O(N^2)$ when $O(N)$ is requested/feasible).
- **[CONSTRAINT-NEG]**: Explicit negative constraint violation (e.g., using unauthorized libraries).
- **[SEMANTIC-HALLUC]**: Inventing non-existent parameters, functions, or documentation APIs.

## Case Studies
- [Case 01: Algorithmic Inefficiency & Boundary Failure in Python](./audits/01_python_complexity_edge_case.md)
- [Case 02: SQL Semantic Flaw & NULL Handling Trap](./audits/02_sql_semantic_null_trap.md)
- [Case 03: Negative Constraint Violation & I/O Streaming Hallucination](./audits/03_negative_constraint_hallucination.md)
