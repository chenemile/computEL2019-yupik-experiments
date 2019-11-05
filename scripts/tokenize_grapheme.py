#!/usr/bin/env python

# Script inserts a space between each token of the input,
# where a token is a Yupik grapheme or a tag

import csv
import os
from helper_functions import tokenize


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
				underlying_result = tokenize(underlying)
				underlyingFormsFile.write(' '.join(underlying_result) + "\n")
		
				# SURFACE 
				surface_result = tokenize(surface)	
				surfaceFormsFile.write(' '.join(surface_result) + "\n")
			# End 'for' Loop
		
			underlyingFormsFile.close()
			surfaceFormsFile.close()
