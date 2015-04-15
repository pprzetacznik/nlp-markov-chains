# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import regex
import re
import random

def clean_corpus(corpus):
  corpus = [word.lower() for word in corpus]
  corpus = filter(regex.compile('^[a-zA-Z\p{L}]+$').match, corpus)
  return corpus

def count_n_grams_word_statistic(corpus):
  successors = {}
  for i in xrange(len(corpus)-1):
    if corpus[i] not in successors:
      successors[corpus[i]] = [corpus[i+1]]
    else:
      successors[corpus[i]].append(corpus[i+1])
  return successors

def generate_note(corpus, marcov_statistic, length):
  last_word = random.choice(corpus)
  note = last_word
  while length > 0 and last_word in marcov_statistic:
    length -= 1
    last_word = random.choice(marcov_statistic[last_word])
    note = note + " " + last_word
  return note

def get_n_grams_from_string(string, n_grams=3):
  n_grams_list = []
  for i in xrange(len(string)-n_grams+1):
    n_grams_list.append(string[i:i+n_grams])
  return n_grams_list

def count_n_grams_statistic(corpus):
  successors = {}
  first_n_grams = []
  for i in xrange(len(corpus)-1):
    n_grams = get_n_grams_from_string(corpus[i])
    if len(n_grams) > 0:
      first_n_grams.append(n_grams[0])

      for j in xrange(len(n_grams)-1):
        if n_grams[j] not in successors:
          successors[n_grams[j]] = [n_grams[j+1]]
        else:
          successors[n_grams[j]].append(n_grams[j+1])
  return first_n_grams, successors

def generate_word(first_n_grams, marcov_statistic, length=0):
  last_n_gram = random.choice(first_n_grams)
  word = last_n_gram
  while length > 0 and last_n_gram in marcov_statistic:
    length -= 1
    last_n_gram = random.choice(marcov_statistic[last_n_gram])
    word = word + last_n_gram[-1]
  return word

if __name__ == '__main__':
  if len(sys.argv) >= 4:
    corpus_file = sys.argv[1]
    note_or_word = 'note' if sys.argv[2] == 'note' else 'word'
    length = int(sys.argv[3])

    corpus = []
    with open(corpus_file) as f:
      for line in f:
        corpus += line.split()

    corpus = clean_corpus(corpus)
    print "corpus cleaned"

    if note_or_word == 'note':
      marcov_statistic = count_n_grams_word_statistic(corpus)
      print "generated statistic"
      print "########## GENERATED NOTE ##########"
      print generate_note(corpus, marcov_statistic, length)
    else:
      # print get_n_grams_from_string('stringlalal', n_grams=2)
      first_n_grams, marcov_statistic = count_n_grams_statistic(corpus)
      print "generated statistic"
      print "########## GENERATED WORD ##########"
      print generate_word(first_n_grams, marcov_statistic, length)
  else:
    print("python markov.py [corpus] [note|word] [length of note or word]")
