# deep model with four hidden layers

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

# check if using the correct validation set
if ! grep -q "nounInfl.valid.underlying" scripts/validate.sh; then
    echo -e "\nHEY, validate.sh is not using the correct validation set"
    exit 1
fi

# check if data has been partitioned into training, validation, and test sets
if [ ! -e "data/nounInfl.train.tsv" ]
then
    scripts/partition_data.sh
fi

mkdir -p data/model.deep

# preprocess data
if [ ! -e "data/nounInfl.train.underlying" ]
then
    scripts/tokenize_char.sh
#    scripts/tokenize_grapheme.py
#    scripts/tokenize_redoubled-grapheme.py
#    scripts/tokenize_ipa.py
fi

# train model
if [ ! -e "data/model.deep/model.npz" ]
then
    $MARIAN/build/marian \
        --devices $GPUS \
        --type s2s \
        --train-sets data/nounInfl.train.surface data/nounInfl.train.underlying \
        --valid-sets data/nounInfl.valid.surface data/nounInfl.valid.underlying \
        --vocabs data/model.deep/vocab.surface.yml data/model.deep/vocab.underlying.yml \
        --model data/model.deep/model.npz \
        --enc-depth 4 --enc-type alternating --enc-cell lstm --enc-cell-depth 2 \
        --dec-depth 4 --dec-cell lstm --dec-cell-base-depth 4 --dec-cell-high-depth 2 \
        --tied-embeddings --layer-normalization --skip \
        --dim-vocabs 0 0 \
        --mini-batch-fit --workspace 6500 \
        --dropout-rnn 0.2 --dropout-src 0.1 --exponential-smoothing \
        --early-stopping 5 --disp-freq 1000 \
        --log data/model.deep/train.log --valid-log data/model.deep/valid.log
fi

# translate test set with n-best lists
#cat data/nounInfl.testset.surface \
#    | $MARIAN/build/marian-decoder -c /nas/data/yupik/model.deep/model.npz.decoder.yml -d $GPUS -b 12 -n1 \
#      --mini-batch 64 --maxi-batch 10 --maxi-batch-sort src --n-best \
#    | ../tools/moses-scripts/scripts/tokenizer/detokenizer.perl -l en \
#    > data/nounInfl.testset.nbest

# translate test set
cat data/nounInfl.testset.surface \
    | $MARIAN/build/marian-decoder -c data/model.deep/model.npz.decoder.yml -d $GPUS -b 12 -n1 \
      --mini-batch 64 --maxi-batch 10 --maxi-batch-sort src \
    | ../tools/moses-scripts/scripts/tokenizer/detokenizer.perl -l en \
    > data/nounInfl.testset.output

# calculate WER
scripts/get_WER.py
