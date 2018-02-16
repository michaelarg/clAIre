import os,sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import tensorflow as tf
import gym
import numpy as np
import random

#Tensorflow has four main parts to the script
#tensors
#Operations
#Sessions - operations are done in a session
#Graphs - graph is initiated in a session

env = gym.make('CartPole-v0')

tf.reset_default_graph()

input = tf.placeholder(tf.float32, shape=(1, 100))
weights = tf.Variable(tf.random_uniform([100,2] , 0, 0.01))
q = tf.matmul(input,weights)
predict = tf.argmax(q,1)

qnext = tf.placeholder(tf.float32, shape=(1, 2))
loss = tf.reduce_sum(tf.square(qnext-q))
trainer = tf.train.GradientDescentOptimizer(0.1)
updateModel = trainer.minimize(loss)
init = tf.global_variables_initializer()

y = .99
e = 0.1
num_episodes = 2000

reward = []
eps = []

with tf.Session() as sess:
    sess.run(init)
    for i in range(num_epsiodes):
        obv = env.reset()
        rAll = 0
        d = False
        j = 0

        while j < 99:
            j+=1
            















    
