rm -f pp1.db
sqlite3 pp1.db < create.sql
sqlite3 pp1.db < load.txt
