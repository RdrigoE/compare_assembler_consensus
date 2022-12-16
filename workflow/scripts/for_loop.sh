sample_name="coverage_"
coverage=$1
reference=$2
for i in {1..30}; do
    art_illumina " -p -i $reference  -l 150 -f $coverage -m 350 -s 10  -o $sample_name$i"
done
