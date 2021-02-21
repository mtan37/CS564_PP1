#added here in case there is an submission dir exists...
rm -rf submission/
mkdir submission/

cp design.pdf parser.py runParser.sh create.sql load.txt submission/
for x in $(seq 1 7)
do
    cp query${x}.sql submission/
done
zip submission.zip submission/*
#clean up
rm -rf submission/
