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

    def test_case_05_javascript_event_loop(self):
        """Case 05: Executes Node.js via subprocess to prove forEach race condition vs for...of."""
        import shutil
        import subprocess

        if not shutil.which("node"):
            self.skipTest("Node.js runtime not found on host. Skipping live JS execution test.")

        js_payload = """
        // 1. Flawed model implementation (forEach race condition)
        async function flawed(userIds, fetcher) {
            const results = [];
            userIds.forEach(async (id) => {
                const data = await fetcher(id);
                results.push(data);
            });
            return results; // Returns prematurely
        }

        // 2. Ground truth implementation (for...of sequential loop)
        async function groundTruth(userIds, fetcher) {
            const results = [];
            for (const id of userIds) {
                const data = await fetcher(id);
                results.push(data);
            }
            return results;
        }

        const mockFetcher = (id) => new Promise(resolve => setTimeout(() => resolve(`user_data_${id}`), 15));

        async function runBenchmark() {
            const ids = ['u1', 'u2'];

            // 1. Chạy hàm lỗi và SNAPSHOT NGAY LẬP TỨC độ dài khi hàm vừa resolve
            const flawedRes = await flawed(ids, mockFetcher);
            const flawedLengthAtReturn = flawedRes.length; // Phải là 0 tại thời điểm resolve

            // 2. Chạy Ground Truth (mất 15ms + 15ms = 30ms)
            const gtRes = await groundTruth(ids, mockFetcher);

            console.log(JSON.stringify({
                flawed_length_at_return: flawedLengthAtReturn,
                gt_length: gtRes.length,
                gt_results: gtRes
            }));
        }
        runBenchmark();
        """

        proc = subprocess.run(
            ["node", "-e", js_payload],
            capture_output=True,
            text=True,
            check=True
        )
        
        result_data = json.loads(proc.stdout.strip())

        # Khẳng định tại thời điểm return, hàm lỗi trả về mảng rỗng (vi phạm logic)
        self.assertEqual(
            result_data["flawed_length_at_return"], 
            0, 
            "Flawed forEach must return an empty array at the moment of resolution."
        )

        # Khẳng định Ground Truth trả về đầy đủ 2 phần tử tuần tự
        self.assertEqual(result_data["gt_length"], 2)
        self.assertEqual(result_data["gt_results"], ["user_data_u1", "user_data_u2"])

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
