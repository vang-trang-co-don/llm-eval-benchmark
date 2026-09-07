# LLM Technical Evaluation & Logic Auditing Benchmark

![Verification Suite](https://github.com/vang-trang-co-don/llm-eval-benchmark/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Data Format](https://img.shields.io/badge/Dataset-DPO%20JSONL-blue.svg)

A production-grade benchmark portfolio demonstrating rigorous evaluation, error taxonomy classification, and structured technical rationale authoring for synthetic Large Language Model (LLM) outputs.

## Evaluation Framework
Evaluations follow **HHH (Helpful, Honest, Harmless)** alignment principles, **Pairwise Preference Optimization (DPO)**, and the **CER (Claim - Evidence - Reasoning)** rationale structure:

1. **Claim:** Explicitly identify the failure taxonomy, constraint violation, or semantic degradation.
2. **Evidence:** Isolate specific lines of code, execution traces, or guideline contradictions.
3. **Reasoning:** Deliver formal computational/linguistic proofs explaining *why* the response fails.
4. **Ground Truth / Chosen Response:** Provide the production-ready corrected output.

## Benchmark Case Studies
| Case | Target Domain | Mode | Primary Taxonomy | Key Focus |
| :---: | :--- | :---: | :---: | :--- |
| [**Case 01**](./audits/01_python_complexity_edge_case.md) | Python / Algorithms | Single Audit | `[PERF-DEGRADE]` | $O(N^2)$ to $O(N)$ prefix sum refactor & boundary safety. |
| [**Case 02**](./audits/02_sql_semantic_null_trap.md) | SQL / Relational Databases | Single Audit | `[LOGIC-SEMANTIC]` | ANSI SQL Three-Valued Logic (3VL) & NULL trap mitigation. |
| [**Case 03**](./audits/03_negative_constraint_hallucination.md) | Python / Systems I/O | Single Audit | `[CONSTRAINT-NEG]` | Negative constraint verification & $O(1)$ JSONL streaming. |
| [**Case 04**](./audits/04_vietnamese_bilingual_localization.md) | Vietnamese / Bilingual NLP | Pairwise (DPO) | `[REGISTER-MISMATCH]` | Administrative register fidelity & Labor Code terminology. |

## Production Dataset (`data/preference_dataset.jsonl`)
All audit cases are formatted in machine-readable JSONL format for direct consumption in DPO and RLHF training pipelines:
```json
{
  "prompt": "...",
  "chosen": "...",
  "rejected": "...",
  "critique": "Structured CER Rationale...",
  "taxonomy": ["PERF-DEGRADE", "LOGIC-EDGE"],
  "preference_strength": "significantly_better"
}
```

## Automated Verification Suite
To execute the automated regression suite locally:
```bash
python3 verify_cases.py
```
