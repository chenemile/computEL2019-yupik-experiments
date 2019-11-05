# computEL2019-yupik-experiments

To train the default model after installing MarianNMT on multiple GPUs: `./default.sh 0 1 2 3`

To train a shallow model with one hidden layer on multiple GPUs: `./shallow-yupik.sh 0 1 2 3`

To train a deep model with four hidden layers on multiple GPUs: `./deep-yupik.sh 0 1 2 3`

In each of these files, there are options to change the tokenization scheme, such that one can tokenize by character, IPA, Yupik grapheme, or Yupik redoubled grapheme.
