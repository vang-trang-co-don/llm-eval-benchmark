"""
Automated Verification Suite for Benchmark Case Studies & Data Schemas.
Tests algorithmic ground truths, SQLite null trap invariants, and validates DPO JSONL format.
"""

import json
from pathlib import Path
import sqlite3
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
        """Case 01: Verifies O(N) Subarray Sum correctness across bounds."""
        self.assertEqual(find_subarray_sum_gt([1, 2, 3, 7, 5], 12), [1, 3])
        self.assertEqual(find_subarray_sum_gt([-1, -2, 3, 4], 1), [1, 2])
        self.assertEqual(find_subarray_sum_gt([5, 1, 2], 5), [0, 0])
        self.assertEqual(find_subarray_sum_gt([1, 2, 3], 100), [-1, -1])

    def test_case_02_sql_null_handling(self):
        """Case 02: Demonstrates Three-Valued Logic NULL collapse in NOT IN vs NOT EXISTS."""
        conn = sqlite3.connect(":memory:")
        cur = conn.cursor()
        
        # Setup schema & seeded data containing a NULL customer_id in orders
        cur.execute("CREATE TABLE Customers (id INT, name TEXT);")
        cur.execute("CREATE TABLE Orders (id INT, customer_id INT);")
        cur.executemany("INSERT INTO Customers VALUES (?, ?);", [(1, "Alice"), (2, "Bob")])
        cur.executemany("INSERT INTO Orders VALUES (?, ?);", [(101, 1), (102, None)])
        
        # 1. Flawed NOT IN Query -> Collapses to UNKNOWN, returning empty set
        flawed_query = "SELECT id FROM Customers WHERE id NOT IN (SELECT customer_id FROM Orders);"
        flawed_results = cur.execute(flawed_query).fetchall()
        self.assertEqual(len(flawed_results), 0, "Flawed NOT IN query must return 0 rows due to NULL trap.")
        
        # 2. Ground Truth NOT EXISTS Query -> Deterministically isolates customer with no orders (Bob)
        gt_query = "SELECT c.id FROM Customers c WHERE NOT EXISTS (SELECT 1 FROM Orders o WHERE o.customer_id = c.id);"
        gt_results = cur.execute(gt_query).fetchall()
        self.assertEqual(len(gt_results), 1)
        self.assertEqual(gt_results[0][0], 2, "Ground truth NOT EXISTS must correctly return Bob (id=2).")
        conn.close()

    def test_case_03_jsonl_streaming(self):
        """Case 03: Verifies O(1) memory generator streaming for JSONL."""
        raw_mock_jsonl = [
            '{"event_id": 1, "status": "ok"}\n',
            '   \n',
            '{"event_id": 2, "status": "error"}\n'
        ]
        records = list(stream_jsonl_gt(raw_mock_jsonl))
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["event_id"], 1)

    def test_preference_dataset_schema(self):
        """Dataset Integrity: Validates DPO JSONL formatting, keys, and row count."""
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

        self.assertGreaterEqual(valid_rows, 5, "Dataset must contain at least 5 validated rows.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
