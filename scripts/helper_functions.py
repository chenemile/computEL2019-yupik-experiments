#!/usr/bin/env python
# -*- coding: utf-8 -*-


# -----------------
# CONVERT FROM IPA 
# -----------------

# TODO: "'ɣ":"'g"
IPA2Grapheme = {'*':'*', '-':'-', "'":"'", 'ŋ̊ʷ':'ngngw', 'χʷ':'ghhw', 'ŋ̊':'ngng', 'χ':'ghh', 'ʁʷ':'ghw', 'ŋʷ':'ngw', 'x':'gg', 'ʁ':'gh', 'kʷ':'kw', 'ɬ':'ll', 'm̥':'mm', 'ŋ':'ng', 'n̥':'nn', 'qʷ':'qw', 'ʂ':'rr', 'xʷ':'wh', 'ɑ':'a', 'ə':'e', 'f':'f', 'ɣ':'g', 'h':'h', 'i':'i', 'k':'k', 'l':'l', 'm':'m', 'n':'n', 'p':'p', 'q':'q', 'ɻ':'r', 's':'s', 't':'t', 'u':'u', 'v':'v', 'ɣʷ':'w', 'j':'y', 'z':'z', "'ɣ":"'g"}

def convertFromIPA(sequences):
	convertedSeqs = []

	for seq in sequences:

		result = []
		IPA_symbol = ""
		seq_idx = 0	# Keeps track of where we actually are in the sequence

		for i, char in enumerate(seq):
			if seq_idx != i:
				continue

			elif char == "[":
				break

			elif not char.isspace():
				# Accounts for graphemes corresponding to multiple IPA symbols
				while not seq[seq_idx+1].isspace():
					IPA_symbol += char
					seq_idx += 1

				IPA_symbol += seq[seq_idx]
				result.append(IPA2Grapheme[IPA_symbol.lower()])
				IPA_symbol = ""

			seq_idx +=1

		# Append the tags
		result.append(seq[seq_idx:].replace(" ", "").strip())

		convertedSeqs.append(''.join(result))

	return convertedSeqs



# ---------
# TOKENIZE 
# ---------

graphemes = ['*', '-', "'", 'ngngw', 'ghhw', 'ngng', 'ghh', 'ghw', 'ngw', 'gg', 'gh', 'kw', 'll', 'mm', 'ng', 'nn', 'qw', 'rr', 'wh', 'a', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z', 'b', 'c', 'd', 'j', 'o', 'x']

tags = ['[N]', '[Abl_Mod]', '[Abs]', '[Equ]', '[Loc]', '[Rel]', '[Ter]', '[Via]', '[Unpd]', '[Sg]', '[Du]', '[Pl]',
		'[1SgPoss]', '[1DuPoss]', '[1PlPoss]', '[2SgPoss]', '[2DuPoss]', '[2PlPoss]', '[3SgPoss]', '[3DuPoss]', '[3PlPoss]', '[4SgPoss]', '[4DuPoss]', '[4PlPoss]', '[SgPosd]', '[DuPosd]', '[PlPosd]']


# Tokenizes by iterating through the 'tags' or 'graphemes' list and checking if the
# sequence ends with the current tag or grapheme. Adds the grapheme or tag
# to the list 'result' and shifts the 'end' marker left in increments equivalent to
# the length of the added grapheme or tag

def tokenize(sequence):

	result = []
	end = len(sequence)

	while (end > 0):
		if sequence[0:end].endswith("]"):
			for tag in tags:
				if (sequence[0:end].endswith(tag)):
					result.insert(0, tag)
					end -= len(tag)
					break
		else:
			for grapheme in graphemes:
				if (sequence[0:end].endswith(grapheme)):
					result.insert(0, grapheme)
					end -= len(grapheme)
					break

	return result



# -----------------
# REDOUBLE FUNCTION
# -----------------
#   Redoubles the appropriate graphemes in a given sequence
#   Input  -- <str> input sequence
#   Return -- the redoubled sequence tokenized into a <list>

def redouble(seq):

	# Tokenize input sequence into Yupik graphemes
	sequence = tokenize(seq)

	doubled_fricative = set(['ll', 'rr', 'gg', 'ghh', 'ghhw'])

	doubleable_fricative = set(['l', 'r', 'g', 'gh', 'ghw'])
	doubleable_nasal = set(['n', 'm', 'ng', 'ngw'])

	undoubleable_unvoiced_consonant = set(['p', 't', 'k', 'kw', 'q', 'qw', 'f', 's', 'wh'])

	double = {	'l'  : 'll',
				'r'  : 'rr',
				'g'  : 'gg',
				'gh' : 'ghh',
				'ghw': 'ghhw',
				'n'  : 'nn',
				'm'  : 'mm',
				'ng' : 'ngng',
				'ngw': 'ngngw'	}


	# Redouble the input sequence, excluding tags
	i = 0
	while (i + 1 < len(sequence)):
		first = sequence[i]
		second = sequence[i+1]
	
		# Rule 1A
		if (first in doubleable_fricative and second in undoubleable_unvoiced_consonant):
			sequence[i] = double[first]
			i += 2

		# Rule 1B
		elif (first in undoubleable_unvoiced_consonant and second in doubleable_fricative):
			sequence[i+1] = double[second]
			i += 2

		# Rule 2
		elif (first in undoubleable_unvoiced_consonant and second in doubleable_nasal):
			sequence[i+1] = double[second]
			i += 2

		# Rule 3A
		elif (first in doubled_fricative and (second in doubleable_fricative or second in doubleable_nasal)):
			sequence[i+1] = double[second]
			i += 2

		# Rule 3B
		elif ((first in doubleable_fricative or first in doubleable_nasal) and second == 'll'):
			sequence[i] = double[first]
			i += 2

		else:
			i += 1	

	# End 'while' Loop


	# Return redoubled sequence
	return sequence


# -----------------
# UNDOUBLE FUNCTION
# -----------------
#   Undoubles the appropriate graphemes in a given sequence
#   Input  -- <str> input sequence
#   Return -- the undoubled sequence tokenized into a <list>

def undouble(seq):

	# Tokenize input sequence into Yupik graphemes
	sequence = tokenize(seq)

	doubleable_fricative = set(['l', 'r', 'g', 'gh', 'ghw'])

	doubled_fricative = set(['ll', 'rr', 'gg', 'ghh', 'ghhw'])
	doubled_nasal = set(['mm', 'nn', 'ngng', 'ngngw'])

	undoubleable_unvoiced_consonant = set(['p', 't', 'k', 'kw', 'q', 'qw', 'f', 's', 'wh'])

	undouble = {'ll'   : 'l',
				'rr'   : 'r',
				'gg'   : 'g',
				'ghh'  : 'gh',
				'ghhw' : 'ghw',
				'mm'   : 'm',
				'nn'   : 'n',
				'ngng' : 'ng',
				'ngngw': 'ngw'}


	undoubled = []
	seq_chars = []
	seq_tags  = []

	idxAndToken = next(((idx, token) for idx, token in enumerate(sequence) if "[" in token), None)
	
	if idxAndToken != None:
		idx = idxAndToken[0]
		seq_chars = sequence[:idx]
		seq_tags = sequence[idx:]
	else:
		seq_chars = sequence


	# Undouble the input sequence, excluding tags
	i = 0
	while (i + 1 < len(seq_chars)):
		first = seq_chars[i]
		second = seq_chars[i+1]
	
		# Rule 1A
		if (first in doubled_fricative and second in undoubleable_unvoiced_consonant):
			seq_chars[i] = undouble[first]
			i += 2

		# Rule 1B
		elif (first in undoubleable_unvoiced_consonant and second in doubled_fricative):
			seq_chars[i+1] = undouble[second]
			i += 2

		# Rule 2
		elif (first in undoubleable_unvoiced_consonant and second in doubled_nasal):
			seq_chars[i+1] = undouble[second]
			i += 2

		# Rule 3B
		elif ((first in doubled_fricative or first in doubled_nasal) and second == 'll'):
			seq_chars[i] = undouble[first]
			i += 2

		# Rule 3A
		elif (first in doubled_fricative and (second in doubled_fricative or second in doubled_nasal)):
			seq_chars[i+1] = undouble[second]
			i += 2

		else:
			i += 1	

	# End 'while' Loop


	# Return undoubled sequence
	undoubled = seq_chars + seq_tags
	return undoubled
