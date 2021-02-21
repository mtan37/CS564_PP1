SELECT COUNT(DISTINCT user_id) FROM User, Item WHERE rating > 1000 AND Item.seller_id=User.user_id;
