rm -rf dat_files/
rm -f user_tmp.db

for X in $(seq 0 39)
do
   python parser.py ebay_data/items-${X}.json 
done
