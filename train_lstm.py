#!/usr/bin/python
# -*- coding: utf-8 -*-

from keras.models import Sequential, Model
from keras.layers import Input, Dense, Activation, LSTM, Concatenate, concatenate, Multiply, multiply
from keras.optimizers import RMSprop, Adagrad
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import string
import re
import gzip
import json
    
maxlen = 40
stripped = lambda s: re.sub("http[^ ]*", "", "".join(i for i in s if 31 < ord(i) < 127))+u''

with gzip.open('datasets/realdonaldtrump.gz', "r") as f:
    corpus = [(u'' * (maxlen-1)) + u'' + stripped(json.loads(l)['text']) for l in f if json.loads(l)['screen_name'] == 'realDonaldTrump']


parcels = []
chars_remaining = []
next_chars = []
labels = []
chars = set()

for j, text in enumerate(corpus):
    punc = 0
    for i in range(0, len(text) - maxlen):
        parcels.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])
        chars = chars.union(set(text))
        chars_remaining.append((140-i)/140.0)
        punc +=1
        if text[i + maxlen] in ".!?":
            punc = 0
        

print 'Parcels created'
        
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

with open("indices_char.json", 'w') as f:
    json.dump(indices_char, f)    
with open("char_indices.json", 'w') as f:
    json.dump(char_indices, f)

print 'Transforming data...'
X_char = np.zeros((len(parcels), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(parcels), len(chars)), dtype=np.bool)
for i, parcel in enumerate(parcels):
    for t, char in enumerate(parcel):
        X_char[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

chars_input = Input(shape = (maxlen, len(chars)))

first_layer = LSTM(128, return_sequences = True)(chars_input)
second_layer = LSTM(128, )(first_layer)
output_layer = Dense(len(chars), activation = 'softmax')(second_layer)
model = Model(inputs = [chars_input], outputs = output_layer)
optimizer = RMSprop()
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

batchsize = 2**15

for batch in range((y.shape[0] / batchsize)):
    batch_ind = range(batch * batchsize, min((batch + 1) * batchsize, y.shape[0]))
    X_char_samp = X_char[batch_ind,:,:]
    y_samp = y[batch_ind,:]

    print('-' * 50)
    print('Batch', batch)
    model.fit([X_char_samp], y_samp,
              batch_size=1024,
              epochs=10)
    model.save('trumptweet.h5')

    for diversity in [0.6]:
        generated = ''
        sentence = (' ' * (maxlen - 1)) + random.sample(string.ascii_lowercase, 1)[0]
        next_char = '0'

        while((len(generated) < 140) & (next_char != u'')):
            x_char = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x_char[0, t, char_indices[char]] = 1.

            preds = model.predict([x_char], verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char
        print generated