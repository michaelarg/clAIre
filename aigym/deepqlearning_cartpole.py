import os,sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import pandas as pd
import numpy as np
import gym
from keras.models import Sequential
from keras.layers import Activation,Dense
from keras.optimizers import Adam
import random
import time
from gym import spaces
import matplotlib.pyplot as plt

#With DQN we don't need to discretise the observations and put the observations into distinct state buckets.
#Why because neural networks are darn good at handling continuous inputs, after all they are general function approximators
# The NN will predict Q values for a state

class QAgent:
    def __init__(self, state_num , action_num, capacity):
        self.state_num = state_num
        self.action_num = action_num
        self.memory = [] #initialise replay memory, this needs to have some capacity limit - so we out with old and in with the new so to speak
        self.capacity = capacity
        self.times = []
        self.learning_rate = 0.1
        self.explore_rate = 1
        self.updatetargetat = 10000
        self.explore_decay = 0.995
        self.explore_rate_min = 0.1
        self.discount_factor = 0.9
        self.model = self._buildnn()
        self.targetModel = self._buildnn()

    def _buildnn(self):
        model = Sequential()
        model.add(Dense(24, input_shape =(4,), activation = 'relu'))
        model.add(Dense(24, input_shape =(4,), activation = 'relu'))
        model.add(Dense(self.action_num, activation='linear'))
        model.compile(loss='mse',optimizer = Adam(lr=0.01))        
        return model

    def getQValues(self, state):
        predicted = self.model.predict(state)
        return predicted[0]

    def updateTargetNetwork(self):
        self.backupNetwork(self.model, self.targetModel)

    def backupNetwork(self, model, backup):
        weights = model.get_weights()
        backup.set_weights(weights)

    def getTargetQValues(self, state):
 #       print state
        predicted = self.targetModel.predict(state)
#        print predicted[0]
        return predicted[0]

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
 #      print self.capacity
 #      if len(self.memory) > self.capacity:
#            self.memory.pop(0)
#            print "popped it!"    #remember needs to be changed

    def replay(self, batch_size):
        x_batch, y_batch = [], []
        minibatch = random.sample(self.memory, min(len(self.memory), batch_size))
        #we wil use these observations to train our network
       # print "mini batch" , minibatch
        for state, action, reward, next_state, done in minibatch:
            qVals = self.getQValues(state)           
            qValsNewState = self.getTargetQValues(next_state)

            y_target = self.getTargetQValues(state) #this predicts the reward from the stat
            y_target[action] = reward if done else reward + self.discount_factor * np.max(self.getTargetQValues(next_state))

            x_batch.append(state[0])
            y_batch.append(y_target)
        self.model.fit(np.array(x_batch), np.array(y_batch), batch_size=len(x_batch), verbose=0) #train the model

        if self.explore_rate > self.explore_rate_min:
            self.explore_rate *= self.explore_decay

    def select_action(self, qValues):
 #       print self.explore_rate
        if np.random.rand() <= self.explore_rate:
            return random.randrange(self.action_num)
        else:
            return np.argmax(qValues)  # returns action

    
def main():
    ep_num = 100000
    max_t = 500
    start = 0
    solved_t = 199
    solved_num  = 0
    capacity = 100000
    solved_max = 100
    env = gym.make('CartPole-v1')
    state_num = env.observation_space.shape[0]
    action_num = env.action_space.n
    agent = QAgent(state_num, action_num, capacity) 
    batch_size = 32
    done = False

    for ep in range(ep_num):
        obv = env.reset()
        obv = np.reshape(obv, [1, 4])
        for t in range(max_t):
            env.render()
            qVals = agent.getQValues(obv)
            
            agent.explore_rate *= agent.explore_decay
            agent.explore_rate = max(agent.explore_rate, agent.explore_rate_min)

            action = agent.select_action(qVals) 
            newobv, reward, done, info = env.step(action)

        
            newobv = np.reshape(newobv, [1, state_num])

            agent.remember(obv, action, reward, newobv, done)

            obv = newobv
            

            if done:
               # print("Episode %d finished after %f time steps" % (ep , t))
                agent.times.append(t)
                if (t >= solved_t):
                    solved_num += 1
                    print "success"
                else:
                    solved_num = 0
                break

        if solved_num == solved_max:
            print "solved!"
            break

            print "agent memory", len(agent.memory)


        agent.replay(batch_size)

        if ep % agent.updatetargetat == 0:
            agent.updateTargetNetwork()
            print "updating target network"        


        if ep % 100 == 0:
            end = time.time() - start
            print "it tooks %f to do 100 episodes" %(end)
            print ep
            print t
            print agent.explore_rate
            print "before", len(agent.times)
            print "mean survival score" , np.mean(agent.times)
            print agent.times
            del agent.times[0:99]
            print "number of times record after deletion" , len(agent.times)
            start = time.time()

        agent.replay(batch_size)
                        

if __name__ == "__main__":
    main()
