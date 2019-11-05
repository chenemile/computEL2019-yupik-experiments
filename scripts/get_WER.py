#!/usr/bin/env python
# -*- coding: utf-8 -*-

from helper_functions import convertFromIPA, undouble
import glob
import numpy as np
np.set_printoptions(threshold=np.inf)

from foma import *
import re


# Dictionaries of format:
#	{ 0 : output for first seq  }
#	{ 1 : output for second seq }	
#   ...
gold  = {}
guess = {}


for filename in glob.glob('../data/*.testset.*'):

	# Populate 'gold' dict
	if filename.endswith("underlying"):

		with open(filename, 'r') as f:
			lines = f.readlines()

			keys = range(len(lines))
			for i in keys:
				gold[i] = lines[i].lower().strip().replace(" ", "")


	# Populate 'guess' dict
	if filename.endswith("output"):
		with open(filename, 'r') as f:
			lines = f.readlines()
		
			keys = range(len(lines))
			for i in keys:
				guess[i] = lines[i].lower().strip().replace(" ", "")

# Compare outputs against the gold standard for each output item
# Of format:
#			(guess)
# 	Item1 	  0
# 	Item2	  1
# 	...
# where 1 denotes a match and 0 denotes a mismatch

length = len(gold)
tbl = np.zeros((length, 2))

for idx in range(length):
	tbl[idx][0] = idx

	if gold[idx] == guess[idx]:
		tbl[idx,1] = 1	


# Prints and stores all incorrect outputs and calculates WER 
numWrong = 0
wrongItems = {}

# col_width = max(len(guess[key]) for key in guess if tbl[key,1] == 0)

print("-----------------------")
print("Output Errors from Run:")
print("-----------------------")

for idx in range(length):
	if tbl[idx][1] == 0:
		wrongItems[gold[idx]] = guess[idx]
		numWrong += 1	
		# print("  " + gold[idx].ljust(col_width) + " --   " + guess[idx])
		print("  " + gold[idx] + " --   " + guess[idx])

print("\n")

print("---------------------")
print("Word Error Rate (WER)")
print("---------------------")
print("  WER = {:.2f}".format(numWrong/float(length) * 100))

print("\n")

print("------------------")
print("Percentage Correct")
print("------------------")
print("  WER = {:.2f}".format((length - numWrong)/float(length) * 100))




'''
---------------
- Description -
---------------
A script that calculates the true word error rate from each training run by
  distinguishing between the items that are ambiguous in their surface forms,
  such as "sufluni" (with five possible parses) and those that are not.
  Ambiguous items are removed from the original WER count, and non-ambiguous
  items AKA those the neural network actually analyzed incorrectly are printed.

  Generates these forms via the Foma-Python API, where the loaded transducer,
  ess.fomabin, is treated like a Python dictionary.

IMPORTS: wrongItems : Dictionary where each key is the gold standard test item
                      and each key's value is the network's corresponding guess
         length     : Total number of training items // Length of 'gold' dictionary

'''


# GET ACTUAL WER / COVERAGE PERCENTAGE

def replaceTags(string):
	capitalizeTags = {	'[n]':'[N]',
						'[abl_mod]':'[Abl_Mod]',
						'[abs]':'[Abs]',
						'[equ]':'[Equ]',
						'[loc]':'[Loc]',
						'[rel]':'[Rel]',
						'[ter]':'[Ter]',
						'[via]':'[Via]',
						'[unpd]':'[Unpd]',
						'[sg]':'[Sg]',
						'[du]':'[Du]',
						'[pl]':'[Pl]',
						'[1sgposs]':'[1SgPoss]',
						'[1duposs]':'[1DuPoss]',
						'[1plposs]':'[1PlPoss]',
						'[2sgposs]':'[2SgPoss]',
						'[2duposs]':'[2DuPoss]',
						'[2plposs]':'[2PlPoss]',
						'[3sgposs]':'[3SgPoss]',
						'[3duposs]':'[3DuPoss]',
						'[3plposs]':'[3PlPoss]',
						'[4sgposs]':'[4SgPoss]',
						'[4duposs]':'[4DuPoss]',
						'[4plposs]':'[4PlPoss]',
						'[sgposd]':'[SgPosd]',
						'[duposd]':'[DuPosd]',
						'[plposd]':'[PlPosd]',
						'[n→n]':'[N→N]',
						'[n→v]':'[N→V]',
						'[v→v]':'[V→V]',
						'[v→n]':'[V→N]',
						'[v]':'[V]',
						'[intr]':'[Intr]',
						'[trns]':'[Trns]',
						'[ind]':'[Ind]',
						'[intrg]':'[Intrg]',
						'[opt]':'[Opt]',
						'[prs]':'[PRS]',
						'[neg]':'[NEG]',
						'[fut]':'[FUT]',
						'[ptcp]':'[Ptcp]',
						'[prec] ':'[Prec]',
						'[conc]':'[Conc]',
						'[cnsqi]':'[CnsqI]',
						'[cnsqii]':'[CnsqII]',
						'[cond':'[Cond]',
						'[ctmp]':'[Ctmp]',
						'[sbrd]':'[Sbrd]',
						'[ptcp_bol]':'[Ptcp_Obl]',
						'[cmpd_vbl]':'[Cmpd_Vbl]',
						'[quant_qual]':'[Quant_Qual]',
						'[encl]':'[Encl]',
						'[1sg]':'[1Sg]',
						'[1pl]':'[1Pl]',
						'[1du]':'[1Du]',
						'[2sg]':'[2Sg]',
						'[2pl]':'[2Pl]',
						'[2du]':'[2Du]',
						'[3sg]':'[3Sg]',
						'[3pl]':'[3Pl]',
						'[3du]':'[3Du]',
						'[4sg]':'[4Sg]',
						'[4pl]':'[4Pl]',
						'[4du]':'[4Du]'	}

	for key in capitalizeTags:
		if key in string:
			string = string.replace(key, capitalizeTags[key])

	return string


t = FST.load("./scripts/ess.fomabin")

numWrong = len(wrongItems)

#col_width = max(len(key) for key in wrongItems)

print("\n")

print("------------------------------")
print("Actual Output Errors from Run:")
print("------------------------------")


for keyWithCaret, valueWithCaret in wrongItems.items():

	# Capitalizes tags to match FST analyzer's formatting
	key   = keyWithCaret.replace("^", "-")
	value = valueWithCaret.replace("^", "-")

	capitalizedKey   = replaceTags(key)
	capitalizedValue = replaceTags(value)

	# Checks if surface forms of the reformatted gold and guess match
	if t[capitalizedKey.strip()] == t[capitalizedValue.strip()]:	# surface forms are identical
			numWrong -= 1
	else:
		# print("  " + key.ljust(col_width) + " --   " + value)
		print("  " + key + " --   " + value)

print("\n")

print("---------------------")
print("Word Error Rate (WER)")
print("---------------------")
print("  WER = {:.2f}".format(numWrong/float(length) * 100))

print("\n")

print("------------------")
print("Percentage Correct")
print("------------------")
print("  WER = {:.2f}".format((length - numWrong)/float(length) * 100))
