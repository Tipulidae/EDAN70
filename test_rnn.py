import tensorflow as tf
from tensorflow.contrib.rnn import LSTMCell, DropoutWrapper, MultiRNNCell, rnn


def unpack_sequence(data):
    return tf.unpack(tf.transpose(tensor, perm=[1,0,2]))



num_neurons = 128
num_layers = 2
dropout = tf.placeholder(tf.float32)

cell = LSTMCell(num_neurons)
cell = DropoutWrapper(cell, output_keep_prob=dropout)
cell = MultiRNNCell([cell] * num_layers)

max_length = 100
num_features = 28

data = tf.placeholder(tf.float32, [None, max_length, num_features])
output, state = tf.contrib.rnn.rnn(cell, unpack_sequence(data), dtype=tf.float32)





