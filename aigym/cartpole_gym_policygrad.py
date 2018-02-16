import os,sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import pandas as pd
import numpy as np
import gym
import random
from gym import spaces
env = gym.make('CartPole-v0')
#https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py
#Solve with Q Learning - basically
#action observe reward
#our aim is to create a policy using q learning to keep the cart pole up right. 
#which is really just asking ourselves, if we are here and we do this - is it good is it bad?

DEBUG_MODE = False

import matplotlib.pyplot as plt

print(env.action_space)
#action space is 2: it can move left or right, discrete
print(env.observation_space)
print(env.observation_space.low)
print(env.observation_space.high)

x_pos_max = env.observation_space.high[0]
x_pos_min = env.observation_space.low[0]

x_vel_max = env.observation_space.high[1]
x_vel_min = env.observation_space.low[1]

pole_angle_max = env.observation_space.high[2]
pole_angle_min = env.observation_space.low[2]

angle_vel_max = env.observation_space.high[3]
angle_vel_min = env.observation_space.low[3]

#define buckets
x_position = pd.cut([-2.4, 2.4], bins=4, retbins=True, right = False)[1]
x_vel = pd.cut([x_vel_min, x_vel_max], bins=2, retbins=True, right = False)[1]
pole_angle = pd.cut([pole_angle_min, pole_angle_max], bins=10, retbins=True, right = False)[1]
angle_vel = pd.cut([angle_vel_min, angle_vel_max], bins=2, retbins=True, right = False)[1]


#try removing x_position and x_vel



q = np.zeros([5, 4, 11, 4, 2])
print "x length" , q.size

q

#print "x velocity" , x_vel

learning_rate = 0.1
start_explore = 1 #at the beginning we want the exploration rate to be high but as we develop our q values we want it to be less random
explore_decay = 0.999
explore_rate_min = 0.1
discount_factor = 0.9  # since the world is unchanging

ep_num = 1000
max_t = 199
solved_num  = 0
solved_max = 100

    
def main():
    solved_count = 0
    rewardsum = 0
    reward_max = 0
    rand_scale = 0.8
    weights =  np.random.uniform(-1,1,4)
    num_streaks = 0
    solved_num = 0
    explore_rate = start_explore

    plt.axis([0, 1000, 0, 200])
 #   plt.axis([0,1000,0,1])
    plt.ion()
 #  plt2.ion()
 
    for ep in range(ep_num):
        obv = env.reset()
        #initial state
        in_state = get_ob_to_ind(obv)

        for t in range(max_t):
            obv = env.render()


            explore_rate *= explore_decay
            explore_rate = max(explore_rate, explore_rate_min)

           # print explore_rate , "explore_rate"
            
            action = select_action(in_state, explore_rate)
            
            obv, reward , done, info = env.step(action)
 
            state = get_ob_to_ind(obv)

            best_q = np.amax(q[  int((state)[0]) ,  int((state)[1])   ,int((state)[2]) , int((state)[3])  ])

           #update q table with reward from this the previous action
            q[int((in_state)[0]) ,  int((in_state)[1])   ,int((in_state)[2]) , int((in_state)[3])][action] += learning_rate * (reward + discount_factor*(best_q) - q[int((in_state)[0]) ,  int((in_state)[1])   ,int((in_state)[2]) , int((in_state)[3])  ][action])

            in_state = state

            if (DEBUG_MODE):
                #print(obv)
                #print x_position
                #print x_vel
                print("\nEpisode = %d" % ep)
                print("t = %d" % t)
                print("Action: %d" % action)
                print("State: %s" % str(state))
                print("Reward: %f" % reward)
                print("Best Q: %f" % best_q)
                print("Explore rate: %f" % explore_rate)
                print("Learning rate: %f" % learning_rate)
                print("Streaks: %d" % num_streaks)
                print("")
            

            if done:
               print("Episode %d finished after %f time steps" % (ep , t))
               if (t >= max_t):
                   solved_num += 1
               else:
                   solved_num = 0
               break

 #           print explore_rate
#            plt.scatter(ep , explore_rate)
#            plt.pause(0.05)


        plt.scatter(ep, t)
        plt.pause(0.05)

       

       # print q
def get_ob_to_ind(obv):

    bin0 = np.digitize(obv[0],x_position)
    bin1 = np.digitize(obv[1],x_vel)
    bin2 = np.digitize(obv[2],pole_angle)
    bin3 = np.digitize(obv[3],angle_vel)
 
    #print str(bin0) + str(bin1) + str(bin2) + str(bin3) , "here"
    return str(bin0) + str(bin1) + str(bin2) + str(bin3)

def select_action(state, explore_rate):
 
    # Select a random action
    if random.random() < explore_rate: #act randomly with a small probability
        action = env.action_space.sample()

    else:
         action = np.argmax(q[int((state)[0]) ,int((state)[1]),int((state)[2]) ,int((state)[3])])          
    return action
        
if __name__ == "__main__":
    main()
