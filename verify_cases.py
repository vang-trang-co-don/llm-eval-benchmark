"""
Automated Verification Suite for Benchmark Case Studies & Data Schemas.
Tests algorithmic ground truths and validates DPO JSONL format integrity.
"""

import json
from pathlib import Path
import unittest
from typing import Iterator, Dict, Any


# --- Ground Truth Functions ---
def find_subarray_sum_gt(nums: list[int], target: int) -> list[int]:
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
    for line in lines:
        if line.strip():
            yield json.loads(line)


# --- Test Suite ---
class TestBenchmarkSuite(unittest.TestCase):

    def test_case_01_subarray_sum(self):
        self.assertEqual(find_subarray_sum_gt([1, 2, 3, 7, 5], 12), [1, 3])
        self.assertEqual(find_subarray_sum_gt([-1, -2, 3, 4], 1), [1, 2])
        self.assertEqual(find_subarray_sum_gt([5, 1, 2], 5), [0, 0])
        self.assertEqual(find_subarray_sum_gt([1, 2, 3], 100), [-1, -1])

    def test_case_03_jsonl_streaming(self):
        raw_mock_jsonl = [
            '{"event_id": 1, "status": "ok"}\n',
            '   \n',
            '{"event_id": 2, "status": "error"}\n'
        ]
        records = list(stream_jsonl_gt(raw_mock_jsonl))
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["event_id"], 1)

    def test_preference_dataset_schema(self):
        dataset_path = Path("data/preference_dataset.jsonl")
        self.assertTrue(dataset_path.exists(), "Dataset file data/preference_dataset.jsonl does not exist!")

        required_keys = {"prompt", "chosen", "rejected", "critique", "taxonomy", "preference_strength"}
        valid_rows = 0

        with open(dataset_path, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                data = json.loads(line)
                missing = required_keys - set(data.keys())
                self.assertFalse(missing, f"Row {line_idx} is missing required fields: {missing}")
                self.assertIsInstance(data["taxonomy"], list)
                self.assertTrue(len(data["taxonomy"]) > 0)
                valid_rows += 1

        self.assertGreaterEqual(valid_rows, 4, "Dataset must contain at least 4 validated rows.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
