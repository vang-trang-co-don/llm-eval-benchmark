# Evaluation Audit 02: SQL Semantic Flaw & NULL Handling Trap

## 1. Metadata
- **Domain:** SQL / Relational Databases
- **Primary Tag:** `[LOGIC-EDGE]`
- **Secondary Tag:** `[SEMANTIC-HALLUC]`
- **Model Evaluated:** Hypothetical Synthetic LLM Output

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
The generated SQL query is logically flawed due to a failure in handling `NULL` values within the subquery, which will result in an empty result set if any `customer_id` in the `Orders` table is `NULL`.

### Evidence
1. **Three-Valued Logic Violation:** In SQL, `NOT IN` evaluates to `UNKNOWN` (which is treated as `FALSE` in a `WHERE` clause) if the subquery returns even a single `NULL` value. 
2. **State-Space Collapse:** If the `Orders` table contains a row where `customer_id IS NULL` (e.g., a guest checkout or corrupted data row), the condition `id NOT IN (..., NULL, ...)` becomes `id <> val1 AND id <> val2 AND id <> NULL`. Since `id <> NULL` evaluates to `UNKNOWN`, the entire `AND` chain evaluates to `UNKNOWN`, filtering out *all* customers, including those who truly have no orders.

### Reasoning
The model failed to account for the standard SQL three-valued logic (True, False, Unknown) regarding `NULL` comparisons. Using `NOT IN` with unvalidated subqueries is a well-known anti-pattern in database engineering. A robust query must either filter out `NULL`s in the subquery or use a semantically safe operator like `NOT EXISTS`.

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
- **Verification:** Both approaches safely ignore `NULL` values in the `Orders` table and correctly isolate customers with zero corresponding order records.
