#!/usr/bin/env bash

# Script inserts a space between each token of the input,
# where a token is either a char, a morphophonological symbol
# or a tag

DIR="./data/*.tsv"

for f in $DIR; do
#	surface=${f%.in}.char

#	sed 's,\([A-Z]\), \1,g; s,\([a-z]\), \1,g;	s, ,,' $f > $surface

	underlying=${f%.tsv}.underlying
	surface=${f%.tsv}.surface

    # Outputs underlying forms, split by space
	cut -f1 $f | \
	sed 's,\([adegiklmnpqrtuvyz\^]\), \1,g' | \
	sed 's, ,,' | \
	sed 's,( , (,g' | \
	sed "s,', ',g" | \
	sed 's,\[, \[,g' | \
	sed 's,+, +,g' | \

	sed 's,@, @,g' | \
	sed 's,\([^@]\)\*,\1 \*,g' | \
	sed 's,\~, \~,g' | \
	sed 's,\([^\~]\)h,\1 h,g' | \
	sed 's,\([^\~(]\)s,\1 s,g' | \
	sed 's,\([^\~s]\)f,\1 f,g' | \
	sed 's,\([^–]\)–,\1 –,g' | \
	sed 's,%, %,g' | \
	sed 's,\/, \/,g' | \
	sed 's,\([^-]\)w,\1 w,g' | \
	sed 's,-, -,g' | \
	sed -e :1 -e 's,\(\[[^]]*\)[[:space:]],\1,g;t1' | \
	sed -e :1 -e 's,\(([^)]*\)[[:space:]],\1,g;t1'  > $underlying

    # Outputs surface forms, split by space
	cut -f2 $f | \
	sed 's,\([A-Z]\), \1,g' | \
	sed 's,\([a-z]\), \1,g' | \
	sed 's, ,,' > $surface
done
