"""
Automated Verification Suite for Benchmark Case Studies.
Proves deterministic correctness of Ground Truth implementations.
"""

import json
import unittest
from typing import Iterator, Dict, Any


# ==========================================
# Ground Truth Implementations
# ==========================================

def find_subarray_sum_gt(nums: list[int], target: int) -> list[int]:
    """Case 01 Ground Truth: O(N) Subarray Sum using Prefix Map."""
    prefix_map = {0: -1}
    current_sum = 0
    for current_index, val in enumerate(nums):
        current_sum += val
        complement = current_sum - target
        if complement in prefix_map:
            return [prefix_map[complement] + 1, current_index]
        if current_sum not in prefix_map:
            prefix_map[current_sum] = current_index
    return [-1, -1]


def stream_jsonl_gt(lines: list[str]) -> Iterator[Dict[str, Any]]:
    """Case 03 Ground Truth: Memory-safe line-by-line generator."""
    for line in lines:
        if line.strip():
            yield json.loads(line)


# ==========================================
# Test Suite
# ==========================================

class TestBenchmarkGroundTruth(unittest.TestCase):

    def test_case_01_subarray_sum(self):
        # Normal positive sequence
        self.assertEqual(find_subarray_sum_gt([1, 2, 3, 7, 5], 12), [1, 3])
        # Mixed negatives and zeros
        self.assertEqual(find_subarray_sum_gt([-1, -2, 3, 4], 1), [1, 2])
        # Target at index 0
        self.assertEqual(find_subarray_sum_gt([5, 1, 2], 5), [0, 0])
        # Target not found
        self.assertEqual(find_subarray_sum_gt([1, 2, 3], 100), [-1, -1])

    def test_case_03_jsonl_streaming(self):
        raw_mock_jsonl = [
            '{"event_id": 1, "status": "ok"}\n',
            '   \n',  # Empty/whitespace line
            '{"event_id": 2, "status": "error"}\n'
        ]
        records = list(stream_jsonl_gt(raw_mock_jsonl))
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["event_id"], 1)
        self.assertEqual(records[1]["status"], "error")


if __name__ == "__main__":
    print("[*] Running Verification Suite for LLM Evaluation Benchmark...")
    unittest.main(verbosity=2)