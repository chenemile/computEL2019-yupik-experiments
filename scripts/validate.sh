#!/bin/bash

cat $1 \
    | ../tools/moses-scripts/scripts/tokenizer/detokenizer.perl -l en 2>/dev/null \
    | ../tools/moses-scripts/scripts/generic/multi-bleu-detok.perl /nas/data/yupik/neural-analyzer/demPtcl.valid.underlying \
    | sed -r 's/BLEU = ([0-9.]+),.*/\1/'
