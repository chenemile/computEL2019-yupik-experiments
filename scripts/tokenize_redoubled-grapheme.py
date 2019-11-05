#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import csv
import os
import re
from helper_functions import redouble

mpSymbols = ["@", "~f", "~sf", "~", "––", "–", ":", "(e)", "(g/t)", "(p/v)", "(t/y)", "(s/z)",
			 "(q/t)", "(ng)", "(g)", "(t)", "(i)", "(i/u)", "(u)", "(a)", "(s)", "(at)", "(pete)fte"]


for filename in os.listdir('/nas/data/yupik/neural-analyzer/'):
#for filename in os.listdir('../data/'):
	if filename.endswith('.tsv'):

		with open('../data/' + filename, 'r') as tsvfile:
			underlyingFormsFile = open('../data/' + os.path.splitext(filename)[0] + '.underlying', 'w')
			surfaceFormsFile = open('../data/' + os.path.splitext(filename)[0] + '.surface', 'w')
		
			sequences = csv.reader(tsvfile, delimiter='\t')
		
			for undoubled_seq in sequences:
				underlying = undoubled_seq[0]
				surface = undoubled_seq[1]

				# UNDERLYING
				underlying_redoubled = []

				# Separates the tags from the remainder of the underlying string
				seq_chars = []
				seq_tags = []

				idx = re.search(r"\[N\]|\[V\]", underlying).start()

				if idx == -1:
					seq_chars = underlying 
				else:
					seq_chars = underlying[:idx]
					seq_tags = ["[" + tag for tag in underlying[idx+1:].split("[")]


				# Tokenizes the remainder of the underlying strings into its base and postbases
				# Tokenizes the MP symbols if they exist and redoubles the morphemes of each base/postbase

				postbases = seq_chars.split("^")	# [base, postbase1, postbase2, etc.]

				if len(postbases) > 1:
					for postbase in postbases:
						morphemeAndTypeTag = postbase.split("[")	# [postbaseMorpheme, [N-->N]]
					
						for symbol in mpSymbols:
							if symbol in morphemeAndTypeTag[0]:
								underlying_redoubled.append(symbol)
								morphemeAndTypeTag[0] = morphemeAndTypeTag[0][len(symbol):]

						if len(morphemeAndTypeTag) > 1:
							redoubled_postbase = redouble(morphemeAndTypeTag[0])	# Redouble the postbase's morpheme
							redoubled_postbase.append("[" + morphemeAndTypeTag[1])	# Append the postbase's tag type, e.g. [N-->N]
						else:
							redoubled_postbase = redouble(morphemeAndTypeTag[0])	

						underlying_redoubled.extend(redoubled_postbase)
						underlying_redoubled.append("^")

					underlyingFormsFile.write(' '.join(underlying_redoubled[:-1]) + " " + ' '.join(seq_tags) + "\n")
				else:
					underlying_redoubled = redouble(seq_chars)
					underlyingFormsFile.write(' '.join(underlying_redoubled) + " " + ' '.join(seq_tags) + "\n")
					#underlyingFormsFile.write(underlying + "\n")


				# SURFACE
				surface_redoubled = redouble(surface)
				surfaceFormsFile.write(' '.join(surface_redoubled) + "\n")

			# End 'for' Loop
		
			underlyingFormsFile.close()
			surfaceFormsFile.close()
