# Trump tweet LSTM model

This is a fun application of neural networks to tweet data. The network takes in a history of letters, and predicts what the next letter should be. Amazingly, this often creates real words and phrases characteristic of the training data (Trump tweets).

A good explanation of these networks can be found here: http://colah.github.io/posts/2015-08-Understanding-LSTMs/

The code here borrows very heavily from this: https://github.com/fchollet/keras/blob/master/examples/lstm_text_generation.py

The training data is from here: https://www.reddit.com/r/datasets/comments/6f9862/all_publicly_available_tweets_from_donald_trumps/

The most recent version of the model is a 2-layer LSTM model with 128 nodes in each layer. The second layer then connects to a dense layer with one node for every character in the output set. The model was written in Keras with a tensorflow backend.

---
This project has no license, and you may use any portion of the code without additional permission and without attribution. 
