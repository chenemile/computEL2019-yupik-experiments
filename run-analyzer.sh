#!/bin/bash

MARIAN=../..

./scripts/tokenize_char.sh

DIR="./data/oov/*.char"

for f in $DIR; do
	output=${f%.char}.out

	# analyze given set of words
	cat $f |\
    	$MARIAN/build/marian-decoder -c /nas/data/yupik/neural-analyzer/naacl2019/allPOS/allPOS.model.deep/model.npz.decoder.yml -b 12 -n1 \
    	--mini-batch 64 --maxi-batch 10 --maxi-batch-sort src |\
    	../tools/moses-scripts/scripts/tokenizer/detokenizer.perl -l en \
		> $output

	sed -i 's/ //g' $output

	rm -f $f
done


# undouble output
#./scripts/undouble.py
