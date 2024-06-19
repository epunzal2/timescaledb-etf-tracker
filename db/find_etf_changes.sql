
-- look at a stock that's new in the ETF
SELECT holding_id
FROM etf_holding
WHERE
    dt = '2024-06-19'
    AND holding_id NOT IN (SELECT DISTINCT(holding_id) FROM etf_holding WHERE dt = '2024-06-14');

-- how holdings have changed
SELECT *
FROM etf_holding
ORDER BY (etf_id, holding_id, dt, weight);

-- PACB
SELECT *
FROM stock
WHERE id IN (22910, 24451);
