
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub
import os
import sqlite3

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def is_existing_user_id(user_id, conn):
    cursor = conn.execute("SELECT count(*) from temp_user_id WHERE user_id = %s;" % (user_id,) )
    for x in cursor:
        if x[0] == 0:
            return False
    return True     
def add_to_existing_user_id(user_id, conn):
    conn.execute("INSERT INTO temp_user_id (user_id) VALUES(%s);" % (user_id,))       

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file, conn):
    dat_file_dir = "dat_files/"
    if not os.path.exists(dat_file_dir):
        os.makedirs(dat_file_dir)
    with open(json_file, 'r') as f, \
        open(dat_file_dir + 'items.dat', 'a+') as item_dat, \
        open(dat_file_dir + 'users.dat', 'a+') as users_dat, \
        open(dat_file_dir + 'bids.dat', 'a+') as bid_dat, \
        open(dat_file_dir + 'categories.dat', 'a+') as cat_dat:
        
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        
        for item in items:

            # Item parsing
            item_id = item['ItemID']

            item_name = item['Name']
            if item_name is None:
                item_name = '"NULL"'
            item_name = '"' + item_name.replace('"', '""') + '"'

            item_description = item['Description']
            if item_description is None:
                item_description = '"NULL"'
            item_description = '"' + item_description.replace('"', '""')  + '"'

            categories_tmp = item['Category']
            categories = set(categories_tmp)
            for category in categories:
                category = '"' + category.replace('"', '""') + '"'
                cat_dat.write(csv_line((item_id, category)))

            current_bid = transformDollar(item['Currently'])
            if current_bid is None:
                current_bid = '"NULL"'
            #current_bid = '"' + current_bid.replace('"', '""') + '"'

            first_bid = transformDollar(item['First_Bid'])
            if first_bid is None:
                first_bid = '"NULL"'
            #first_bid = '"' + first_bid.replace('"', '""') + '"'

            location = item['Location']
            if location is None:
                location = '"NULL"'
            location = '"' + location.replace('"', '""') + '"'
            
            country = item['Country']
            if country is None:
                country = '"NULL"'
            country = '"' + country.replace('"', '""') + '"'

            bid_started = transformDttm(item['Started'])
            if bid_started is None:
                bid_started = '"NULL"'
            bid_started = '"' + bid_started.replace('"', '""') + '"'

            bid_ends = transformDttm(item['Ends'])
            if bid_ends is None:
                bid_ends = '"NULL"'
            bid_ends = '"' + bid_ends.replace('"', '""') + '"'
            
            seller_id = item['Seller']['UserID']
            seller_id = '"' + seller_id.replace('"', '""') + '"'

            seller_rating = item['Seller']['Rating']
            if seller_rating == None:
                seller_rating = '"NULL"'
            seller_rating = '"' + seller_rating.replace('"', '""') + '"'

            
            if is_existing_user_id(seller_id, conn) is False:
                users_dat.write(csv_line((seller_id, seller_rating, location, country)))
                add_to_existing_user_id(seller_id, conn)

            num_bids = 0
            if item['Bids'] is not None:
                num_bids = len(item['Bids'])
            item_dat.write(csv_line((item_id, item_name, current_bid, first_bid, bid_started, bid_ends, str(num_bids), item_description, seller_id)))

            # Bid parsing
            bids = item['Bids']
            if bids is not None:
                for bid in bids:
                    bid_data = bid['Bid']
                    bidder = bid_data['Bidder']
                    
                    bidder_id = bidder['UserID']
                    bidder_id = '"' + bidder_id.replace('"', '""') + '"'

                    bidder_rating = bidder['Rating']
                    if bidder_rating is None:
                        bidder_rating = 'NULL'
                    bidder_rating = '"' + bidder_rating.replace('"', '""') + '"'

                    bidder_location = None
                    if 'Location' in bidder:
                        bidder_location = bidder['Location']
                    if bidder_location is None:
                        bidder_location = 'NULL'
                    bidder_location = '"' + bidder_location.replace('"', '""') + '"'

                    bidder_country = None
                    if 'Country' in bidder:
                        bidder_country = bidder['Country']
                    if bidder_country is None:
                        bidder_country = '"NULL"'
                    bidder_country = '"' + bidder_country.replace('"', '""') + '"'

                    bid_time = transformDttm(bid_data['Time'])
                    if bid_time is None:
                        bid_time = '"NULL"'
                    bid_time = '"' + bid_time.replace('"', '""') + '"'

                    bid_amount = transformDollar(bid_data['Amount'])
                    if bid_amount is None:
                        bid_amount = '"NULL"'
                    #bid_amount = '"' + bid_amount.replace('"', '""') + '"'
                    
                    if is_existing_user_id(bidder_id, conn) is False:
                        add_to_existing_user_id(bidder_id, conn)
                        users_dat.write(csv_line((bidder_id, bidder_rating, bidder_location, bidder_country)))
                    bid_dat.write(csv_line((item_id, bidder_id, bid_amount, bid_time)))

            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
        
        f.close()
        item_dat.close()
        users_dat.close()
        bid_dat.close()
        cat_dat.close()

# Aggregate data into a csv row
def csv_line(input_list):
    return columnSeparator.join(input_list) + '\n'
    
"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv, conn):
    if len(argv) < 2:
        print('Usage: python skeleton_json_parser.py <path to json files>', file=sys.stderr)
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f, conn)
            print("Success parsing " + f)

def create_tmp_db(db):
    conn = sqlite3.connect(db)
    #conn.execute("DROP TABLE IF EXISTS temp_user_id")
    conn.execute("CREATE TABLE IF NOT EXISTS temp_user_id(user_id TEXT)")
    return conn

if __name__ == '__main__':
    conn = create_tmp_db("user_tmp.db")
    main(sys.argv, conn)
    conn.commit()
    conn.close()
