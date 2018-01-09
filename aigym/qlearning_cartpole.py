import os,sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import pandas as pd
import numpy as np
import gym
import random
from gym import spaces
import matplotlib.pyplot as plt

env = gym.make('CartPole-v0')

pole_angle_max = env.observation_space.high[2]
pole_angle_min = env.observation_space.low[2]

angle_vel_max = env.observation_space.high[3]
angle_vel_min = env.observation_space.low[3]

x_pos_max = env.observation_space.high[0]
x_pos_min = env.observation_space.low[0]

#discretize continuous values to discrete buckets
x_pos = pd.cut([-2.4, 2.4], bins=2, retbins=True, right = False)[1]
pole_angle = pd.cut([pole_angle_min, pole_angle_max], bins=9, retbins=True, right = False)[1]
angle_vel = pd.cut([angle_vel_min, angle_vel_max], bins=2, retbins=True, right = False)[1]

q = np.zeros([3 , 10,3, 2])

#Q-Learning Parameters
learning_rate = 0.1
start_explore = 1 
explore_decay = 0.999
explore_rate_min = 0.1
discount_factor = 0.9  

ep_num = 10000
max_t = 200
solved_t = 199
solved_num  = 0
solved_max = 100

    
def main():
    solved_count = 0
    rewardsum = 0
    reward_max = 0

    num_streaks = 0
    solved_num = 0
    explore_rate = start_explore

    plt.axis([0, 1000, 0, 200])
    plt.ion()

 
    for ep in range(ep_num):
        obv = env.reset()
        in_state = get_ob_to_ind(obv)

        for t in range(max_t):
            obv = env.render()

            explore_rate *= explore_decay
            explore_rate = max(explore_rate, explore_rate_min)
            action = select_action(in_state, explore_rate)
            obv, reward , done, info = env.step(action)
            state = get_ob_to_ind(obv)
            best_q = np.amax(q[  int((state)[0]) ,  int((state)[1]) , int((state)[2])   ])

           #update q table with reward from this the previous action
            q[int((in_state)[0]) ,  int((in_state)[1]), int((in_state)[2])][action] += learning_rate * (reward + discount_factor*(best_q) - q[int((in_state)[0]) ,  int((in_state)[1]) , int((in_state)[2]) ][action])

            in_state = state
            
#           if ep % 1000 == 0:
#                print q
            
            if done:
               print("Episode %d finished after %f time steps" % (ep , t))
               if (t >= solved_t):
                   solved_num += 1
                   print "success"
               else:
                   solved_num = 0
               break

        plt.scatter(ep, t)
        plt.pause(0.05)

def get_ob_to_ind(obv):
    bin0 = np.digitize(obv[0],x_pos)
    bin1 = np.digitize(obv[2],pole_angle)
    bin2 = np.digitize(obv[3],angle_vel)
    q_index =  str(bin0) + str(bin1) + str(bin2)
    return q_index

def select_action(state, explore_rate):
    if random.random() < explore_rate: 
        action = env.action_space.sample()
    else:
         action = np.argmax(     q[int((state)[0]) ,int((state)[1]), int((state)[2])]       )   
    return action
        
if __name__ == "__main__":
    main()
