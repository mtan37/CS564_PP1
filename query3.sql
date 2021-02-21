WITH tmp as (
    SELECT c.item_id, count(*) as category_count 
    from Category c
GROUP BY c.item_id)
SELECT count(*) from tmp 
WHERE tmp.category_count = 4;
