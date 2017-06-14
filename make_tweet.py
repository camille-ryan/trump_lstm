from keras.models import load_model
import json
import numpy as np

model = load_model('trumptweet.h5')
with open('indices_char.json') as f:
	indices_char = json.load(f)
with open('char_indices.json') as f:
	char_indices = json.load(f)
maxlen = 40
chars = set(char_indices)

def sample(preds, temperature=1.0):
	# helper function to sample an index from a probability array
	preds = np.asarray(preds).astype('float64')
	preds = np.log(preds) / temperature
	exp_preds = np.exp(preds)
	preds = exp_preds / np.sum(exp_preds)
	probas = np.random.multinomial(1, preds, 1)
	return np.argmax(probas)

def generate_tweet(input, temperature, prepend = ''):
	generated = prepend
	sentence = (' ' * (maxlen - 1)) + input
	sentence = ''.join(e for e in sentence if e in chars )
	sentence = sentence[(len(sentence) - 40):]
	next_char = '0'

	while((len(generated) < 140) & (next_char != u'')):
		x_char = np.zeros((1, maxlen, len(chars)))
		for t, char in enumerate(sentence):
			x_char[0, t, char_indices[char]] = 1.

		preds = model.predict([x_char], verbose=0)[0]
		next_index = str(sample(preds, temperature))
		next_char = indices_char[next_index]

		if next_char not in u'':
			generated += next_char
			sentence = sentence[1:] + next_char
	if next_char != u'':
		generated = generated[:generated.rfind(' ')]
	return generated
