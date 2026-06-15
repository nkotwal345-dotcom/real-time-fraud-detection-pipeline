-- Fraud KPI Queries
-- Assumed cleaned table name: credit_card_transactions

-- 1. Total transaction volume
SELECT COUNT(*) AS total_transactions
FROM credit_card_transactions;

-- 2. Fraud transaction count
SELECT COUNT(*) AS fraud_transactions
FROM credit_card_transactions
WHERE class = 1;

-- 3. Fraud rate
SELECT
    ROUND(100.0 * SUM(CASE WHEN class = 1 THEN 1 ELSE 0 END) / COUNT(*), 4) AS fraud_rate_percentage
FROM credit_card_transactions;

-- 4. Fraud amount exposure
SELECT
    ROUND(SUM(amount), 2) AS total_fraud_amount
FROM credit_card_transactions
WHERE class = 1;

-- 5. Average transaction amount by fraud status
SELECT
    class,
    COUNT(*) AS transaction_count,
    ROUND(AVG(amount), 2) AS avg_transaction_amount,
    ROUND(SUM(amount), 2) AS total_amount
FROM credit_card_transactions
GROUP BY class;

-- 6. High-value fraud transactions
SELECT
    *
FROM credit_card_transactions
WHERE class = 1
ORDER BY amount DESC
LIMIT 25;
