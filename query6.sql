SELECT COUNT (DISTINCT user_id) FROM User, Bid, Item WHERE User.user_id=Item.seller_id AND User.user_id=Bid.bidder_id;
