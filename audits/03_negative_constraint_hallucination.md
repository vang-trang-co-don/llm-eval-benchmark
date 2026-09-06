# Evaluation Audit 03: Negative Constraint Violation & I/O Streaming Hallucination

## 1. Metadata
- **Domain:** Python / System Architecture (I/O Operations)
- **Primary Tag:** `[CONSTRAINT-NEG]`
- **Secondary Tag:** `[SEMANTIC-HALLUC]`
- **Model Evaluated:** Hypothetical Synthetic LLM Output

## 2. Input Prompt
> "Write a Python script to read and process a 50GB log file in **JSONL (JSON Lines)** format. 
> Constraint: Do NOT use any third-party libraries (standard library only)."

## 3. Model Output (Under Evaluation)
```python
import json
import ujson # Violates negative constraint

def process_logs(filepath):
    # Hallucinated standard library method
    with json.load_streaming(filepath) as stream: 
        for record in stream:
            print(record['event_type'])
```

## 4. Structured Technical Rationale (CER Framework)

### Claim
The generated code exhibits a dual failure: a direct violation of the explicit negative constraint regarding third-party libraries, and a severe hallucination of a non-existent standard library API for memory-safe I/O streaming.

### Evidence
1. **Negative Constraint Violation:** The code imports `ujson` (line 2), which is a third-party C-extension library, directly contradicting the prompt's instruction to use the standard library only.
2. **API Hallucination:** The method `json.load_streaming()` (line 6) does not exist in Python's standard `json` module. Furthermore, standard `json.load()` requires the entire file to be loaded into memory as a JSON array, which would trigger an immediate `MemoryError` (OOM) on a 50GB file.

### Reasoning
The model confused the concept of a monolithic JSON array with **JSONL (JSON Lines)**, where each line is a distinct, valid JSON object. To process a 50GB JSONL file using only the standard library without exhausting RAM, the script must utilize standard file I/O generators to stream line-by-line, applying `json.loads()` to each individual string.

## 5. Corrected Ground Truth (Production-Grade)
```python
import json
from typing import Iterator, Dict, Any

def stream_jsonl(filepath: str) -> Iterator[Dict[str, Any]]:
    """Streams a JSONL file line-by-line to maintain O(1) memory footprint."""
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # Skip empty lines
            if line.strip():
                yield json.loads(line)

def process_logs(filepath: str):
    for record in stream_jsonl(filepath):
        # Process each record without loading the 50GB file into RAM
        if 'event_type' in record:
            print(record['event_type'])
```
- **Complexity:** $O(1)$ Space complexity (Memory safe); $O(N)$ Time complexity where $N$ is the number of lines.
- **Verification:** Adheres strictly to standard library constraints and prevents OOM crashes on massive datasets.
