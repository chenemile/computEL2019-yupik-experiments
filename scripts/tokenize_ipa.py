#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script inserts a space between each token of the input,
# where a token is the IPA symbol for a Yupik grapheme or tag

import csv
import os
from helper_functions import redouble


graphemeToIPA = {'*':'*', '-':'-', "'":"'", 'ngngw':'ŋ̊ʷ', 'ghhw':'χʷ', 'ngng':'ŋ̊', 'ghh':'χ', 'ghw':'ʁʷ', 'ngw':'ŋʷ', 'gg':'x', 'gh':'ʁ', 'kw':'kʷ', 'll':'ɬ', 'mm':'m̥', 'ng':'ŋ', 'nn':'n̥', 'qw':'qʷ', 'rr':'ʂ', 'wh':'xʷ', 'a':'ɑ', 'e':'ə', 'f':'f', 'g':'ɣ', 'h':'h', 'i':'i', 'k':'k', 'l':'l', 'm':'m', 'n':'n', 'p':'p', 'q':'q', 'r':'ɻ', 's':'s', 't':'t', 'u':'u', 'v':'v', 'w':'ɣʷ', 'y':'j', 'z':'z'}


for filename in os.listdir('../data'):
	if filename.endswith('.tsv'):

		with open('../data/' + filename, 'r') as tsvfile:
			underlyingFormsFile = open('../data/' + os.path.splitext(filename)[0] + '.underlying', 'w')
			surfaceFormsFile = open('../data/' + os.path.splitext(filename)[0] + '.surface', 'w')
		
			sequences = csv.reader(tsvfile, delimiter='\t')
		
			for seq in sequences:
				underlying = seq[0]
				surface = seq[1]
		
				# UNDERLYING
				underlying_redoubled = redouble(underlying)	
				underlying_ipa = [graphemeToIPA[tok] for tok in underlying_redoubled if tok in graphemeToIPA]
				underlyingFormsFile.write(' '.join(underlying_ipa) + "\n")
		
				# SURFACE
				surface_redoubled = redouble(surface)
				surface_ipa = [graphemeToIPA[tok] for tok in surface_redoubled if tok in graphemeToIPA] 
				surfaceFormsFile.write(' '.join(surface_ipa) + "\n")
			# End 'for' Loop
		
			underlyingFormsFile.close()
			surfaceFormsFile.close()
