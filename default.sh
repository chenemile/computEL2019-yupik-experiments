# default script from https://github.com/marian-nmt/marian-examples/tree/master/training-basics

#!/bin/bash -v

MARIAN=../..

# set chosen gpus
GPUS=0
if [ $# -ne 0 ]
then
    GPUS=$@
fi
echo Using GPUs: $GPUS

if [ ! -e $MARIAN/build/marian ]
then
    echo "marian is not installed in $MARIAN/build, you need to compile the toolkit first"
    exit 1
fi

if [ ! -e ../tools/moses-scripts ] || [ ! -e ../tools/subword-nmt ]
then
    echo "missing tools in ../tools, you need to download them first"
    exit 1
fi

# check if data has been partitioned into training, validation, and test sets
if [ ! -e "data/nounInfl.train.tsv" ]
then
    scripts/partition_data.sh
fi

mkdir -p model

# preprocess data
if [ ! -e "data/nounInfl.train.underlying" ]
then
#    scripts/tokenize_char.sh
#    scripts/tokenize_grapheme.py
    scripts/tokenize_redoubled-grapheme.py
#    scripts/tokenize_ipa.py
fi

# train model
if [ ! -e "model/model.npz.best-translation.npz" ]
then
    $MARIAN/build/marian \
        --devices $GPUS \
        --type amun \
        --model model/model.npz \
        --train-sets data/nounInfl.train.surface data/nounInfl.train.underlying \
        --vocabs model/vocab.surface.yml model/vocab.underlying.yml \
        --dim-vocabs 0 0 \
        --mini-batch-fit -w 3000 \
        --layer-normalization --dropout-rnn 0.2 --dropout-src 0.1 --dropout-trg 0.1 \
        --early-stopping 5 \
        --valid-freq 10000 --save-freq 10000 --disp-freq 1000 \
        --valid-metrics cross-entropy translation \
        --valid-sets data/nounInfl.valid.surface data/nounInfl.valid.underlying \
        --valid-script-path scripts/validate.sh \
        --log model/train.log --valid-log model/valid.log \
        --overwrite --keep-best \
        --seed 1111 --exponential-smoothing \
        --normalize=1 --beam-size=12 --quiet-translation
fi

# translate dev set
cat data/nounInfl.valid.surface \
    | $MARIAN/build/marian-decoder -c model/model.npz.best-translation.npz.decoder.yml -d $GPUS -b 12 -n1 \
      --mini-batch 64 --maxi-batch 10 --maxi-batch-sort src \
    | sed 's/\@\@ //g' \
    | ../tools/moses-scripts/scripts/tokenizer/detokenizer.perl -l en \
    > data/nounInfl.valid.output

# translate test set
cat data/nounInfl.testset.surface \
    | $MARIAN/build/marian-decoder -c model/model.npz.best-translation.npz.decoder.yml -d $GPUS -b 12 -n1 \
      --mini-batch 64 --maxi-batch 10 --maxi-batch-sort src \
    | sed 's/\@\@ //g' \
    | ../tools/moses-scripts/scripts/tokenizer/detokenizer.perl -l en \
    > data/nounInfl.testset.output

# calculate bleu scores on dev and test set
#../tools/moses-scripts/scripts/generic/multi-bleu-detok.perl data/nounInfl.valid.underlying < data/nounInfl.valid.output
#../tools/moses-scripts/scripts/generic/multi-bleu-detok.perl data/nounInfl.testset.underlying < data/nounInfl.testset.output

# calculate WER
scripts/get_wer.py
