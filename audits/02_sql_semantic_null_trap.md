# Evaluation Audit 02: SQL Semantic Flaw & NULL Handling Trap

## 1. Metadata
- **Domain:** SQL / Relational Databases
- **Primary Tag:** `[LOGIC-EDGE]`
- **Secondary Tag:** `[LOGIC-SEMANTIC]`
- **Model Evaluated:** Hypothetical Synthetic LLM Output

### Evaluation Scorecard
| Metric | Score (1-5) | Operational Justification |
| :--- | :---: | :--- |
| **Instruction Following** | 4/5 | Followed schema instructions, outputted valid syntax. |
| **Truthfulness / Logic** | 1/5 | Critical semantic flaw under Three-Valued Logic (3VL). |
| **Code Executability** | 5/5 | Syntax executes cleanly but yields a false empty set. |
| **Rationale Quality** | 5/5 | Complete breakdown of SQL truth-table resolution. |

## 2. Input Prompt
> "Write a SQL query to find all customers who have never placed an order. 
> Tables: `Customers` (id, name, email), `Orders` (id, customer_id, order_date)."

## 3. Model Output (Under Evaluation)
```sql
SELECT * 
FROM Customers 
WHERE id NOT IN (SELECT customer_id FROM Orders);
```

## 4. Structured Technical Rationale (CER Framework)

### Claim
The generated SQL query is semantically invalid due to improper handling of `NULL` values within the subquery predicate, resulting in an empty result set (false negative) whenever the `Orders` table contains at least one `NULL` entry in `customer_id`.

### Evidence
1. **Three-Valued Logic (3VL) Violation:** In ANSI SQL, `NOT IN` expands to a sequence of inequality comparisons chained by `AND`:
   $$\text{id} \neq \text{val}_1 \land \text{id} \neq \text{val}_2 \land \dots \land \text{id} \neq \text{NULL}$$
2. **State-Space Collapse:** Any direct comparison with `NULL` (e.g., `id <> NULL`) evaluates to `UNKNOWN`. Under standard SQL truth tables, `TRUE AND UNKNOWN` resolves to `UNKNOWN`. Since a `WHERE` clause filters out rows that do not evaluate strictly to `TRUE`, the entire predicate collapses to `UNKNOWN`, purging all records from the output.

### Reasoning
The model failed to distinguish between a syntactically valid query and a semantically robust relational operation. Relying on `NOT IN` over nullable foreign key columns is a critical database anti-pattern. The model must utilize operators resilient to `NULL` pollution, such as `NOT EXISTS` (correlated subquery) or an anti-join via `LEFT JOIN ... WHERE IS NULL`.

## 5. Corrected Ground Truth (Production-Grade)

### Approach 1: NOT EXISTS (Safest & Most Performant)
```sql
SELECT c.id, c.name, c.email
FROM Customers c
WHERE NOT EXISTS (
    SELECT 1 
    FROM Orders o 
    WHERE o.customer_id = c.id
);
```

### Approach 2: LEFT JOIN (Anti-Join Pattern)
```sql
SELECT c.id, c.name, c.email
FROM Customers c
LEFT JOIN Orders o ON c.id = o.customer_id
WHERE o.customer_id IS NULL;
```
- **Verification:** Both approaches safely isolate customers with zero orders, maintaining deterministic execution regardless of `NULL` presence in `Orders.customer_id`.
