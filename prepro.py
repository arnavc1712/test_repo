import string
from xml.dom import minidom
import xml.etree.cElementTree as ET
# from utilities import *
# from keras.preprocessing import sequence
import numpy as np
# from tqdm import tqdm
import string
# import nltk
import os
import re
from string import punctuation

dataset = "Restaurants"
mode = 'term'
train_sentences = []
test_sentences = []
aspectTerms = []
aspectCats = []
words = []


# print ET.dump(tree)
def strip_punctuation(s):
	return s.translate(string.maketrans("",""), string.punctuation)
    # return ''.join(c for c in s if c not in punctuation)

def process_text(x):
	x = x.lower()
	x = re.sub('[^A-Za-z0-9]+', ' ', x)
	x = x.split(' ')
	x = [strip_punctuation(y) for y in x]
	# ptxt = nltk.word_tokenize(ptxt)
	return x

# sent = "Three courses - choices include excellent mussels, puff pastry goat cheese and salad with a delicious dressing, and a hanger steak au poivre that is out of this world."

# print process_text(sent)

# parse Training File
# tree = ET.ElementTree(file='test.xml')
main_counter = 0 
aspectTerm_counter = 0
aspectCat_counter = 0
tree = ET.ElementTree(file='{}_Train.xml'.format(dataset))

for index, sentence in enumerate(tree.iter(tag='sentence')):
	s = {}
	main_counter+=1
	# print "NEXT"
	for elem in sentence.iter():
		
		# print "NEW sent"
		if(elem.tag=='text'):
			# ptxt = strip_punctuation(elem.text.lower())
			# ptxt = nltk.word_tokenize(ptxt)
			# ptxt = ptxt.split(' ')
			ptxt = process_text(str(elem.text.encode('utf-8')))

			s['text'] = ptxt
			words += ptxt

		elif(elem.tag=='aspectTerms'):
			aspectTerm_counter+=1
			s['aspectTerms'] = []
			for at in elem.iter():
				attr = at.attrib
				
				if('term' not in attr):
					continue
				txt = process_text(at.attrib['term'])
				# print(txt)
				words += txt
				s['aspectTerms'].append([txt, at.attrib])
				aspectTerms.append(txt)

		elif(elem.tag=='aspectCategories'):
			aspectCat_counter+=1
			s['aspectCats'] = []
			for ac in elem.iter():
				attr = ac.attrib
				if('category' not in attr):
					continue
				s['aspectCats'].append([attr['category'],attr])
			aspectCats.append(attr['category'])
	train_sentences.append(s)

print train_sentences[:5]
print main_counter
print aspectTerm_counter
print aspectCat_counter



