WITH tmp as (
    SELECT c.description from Category c
JOIN Item i on c.item_id=i.item_id
WHERE i.current_price >100.0 and i.num_bids >=1
GROUP BY c.description
            )
SELECT count(*) from tmp;
