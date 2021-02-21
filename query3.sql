WITH "NumDescript" AS (
    SELECT item_id, COUNT(description) AS "num_d"
    FROM CATEGORY C
    GROUP BY item_id
)
SELECT COUNT(num_d) AS "result"
FROM NumDescript N, BID B
WHERE N.item_id = B.item_id
  AND num_d = 4;

--Marvin's query
WITH tmp as (
    SELECT c.item_id, count(*) as category_count 
    from Category c
GROUP BY c.item_id)
SELECT count(*) from tmp 
WHERE tmp.category_count = 4;
