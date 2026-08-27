-- The exact queries api/main.py runs for GET /api/olist/kpis.
-- Paste any of these into Supabase's SQL editor to see them work directly
-- against your data, independent of the API.

-- Total number of orders ever placed
SELECT COUNT(*) FROM orders;

-- Total revenue collected (sum of all payments, across all orders)
SELECT SUM(payment_value) FROM order_payments;

-- Average customer review score (1-5)
SELECT AVG(review_score) FROM order_reviews;

-- Average delivery time in days, for orders that actually arrived
SELECT AVG(
    EXTRACT(EPOCH FROM (order_delivered_customer_date - order_purchase_timestamp)) / 86400
) AS avg_delivery_days
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL;
