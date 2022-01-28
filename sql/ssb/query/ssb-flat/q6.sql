--Q2.3
SELECT
    sum(LO_REVENUE),
    (LO_ORDERDATE DIV 10000) AS year,
    P_BRAND
FROM lineorder_flat
WHERE P_BRAND = 'MFGR#2239' AND S_REGION = 'EUROPE'
GROUP BY
    year,
    P_BRAND
ORDER BY
    year,
    P_BRAND;
