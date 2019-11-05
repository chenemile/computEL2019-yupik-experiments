#!/usr/bin/env bash

# partitions data into
#   training set
#   validation set
#   test set

DIR="./data/*.orig"

for f in $DIR; do
	train=${f%.orig}.train.tsv
	valid=${f%.orig}.valid.tsv
	testset=${f%.orig}.testset.tsv

    totalItems=$(wc -l < $f)

	# split data into a 0.8/0.1/0.1 ratio
    numInTrain=$(echo "$totalItems*0.8" | bc | xargs printf %.0f)
    numInValid=$(echo "($totalItems - $numInTrain) / 2" | bc | xargs printf %.0f)
    numInTest=$(echo "$totalItems - $numInTrain - $numInValid" | bc | xargs printf %.0f)

    shuf -n $numInTrain $f | sort > $train

    comm -23 $f $train | shuf -n $numInValid | sort > $valid

    comm -23 $f <(cat $train $valid | sort) > $testset

	shuf -o $train < $train
	shuf -o $valid < $valid
	shuf -o $testset < $testset
done
