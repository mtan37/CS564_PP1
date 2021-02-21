DROP TABLE if exists User;
create table User(
    user_id TEXT PRIMARY KEY,
    rating INTEGER NOT NULL,
    location TEXT,
    country TEXT
);


DROP TABLE if exists Item;
DROP TRIGGER if exists seller_location_check;

create table Item(
    item_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    current_price REAL NOT NULL,
    first_bid REAL NOT NULL,
    bid_started TEXT NOT NULL,
    bid_ends TEXT NOT NULL,
    num_bids INTEGER NOT NULL,
    description TEXT,
    seller_id TEXT NOT NULL,
    FOREIGN KEY(seller_id) REFERENCES User (user_id)
);

CREATE TRIGGER seller_location_check
BEFORE INSERT on Item
BEGIN
    SELECT CASE
        WHEN null == (SELECT location from User WHERE User.user_id=NEW.seller_id)
            OR null == (SELECT country from User WHERE User.user_id=NEW.seller_id)
        THEN RAISE (ABORT, "seller's location or country can't be null")    
    END;
END;


DROP TABLE if exists Bid;
create table Bid(
    item_id TEXT,
    bidder_id TEXT,
    time TEXT,
    amount REAL NOT NULL,
    PRIMARY KEY(item_id, bidder_id, time),
    FOREIGN KEY(item_id) REFERENCES Item (item_id),
    FOREIGN KEY(bidder_id) REFERENCES User (user_id)
);


DROP TABLE if exists Category;
create table Category(
    item_id INTEGER,
    description TEXT,
    PRIMARY KEY(item_id, description),
    FOREIGN KEY(item_id) REFERENCES Item (item_id)
);
