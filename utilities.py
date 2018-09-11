"""
A number of useful functions that are not central to the logic of the api itself.
"""

import re

def contains_curse(sometext):
	"""
	Checks a particular string to see if it contains any 
	NSFW type words. curse words, things innapropriate
	that you might find in lyrics or quotes

	:param sometext: some text 
	:type sometext: Str

	:returns: a boolean stating whether we have a curse word or not
	:rtype: Boolean
	"""
	return re.search(r'bitch*|fag*|pussy|nigg*|fuck*|cunt*|shit*|dick*|cock*',sometext.lower())

