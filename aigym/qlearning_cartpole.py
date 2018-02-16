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

x_pos = pd.cut([-2.4, 2.4], bins=8, retbins=True, right = False)[1]
x_vel = pd.cut([-1, 1], bins=8, retbins=True, right = False)[1]
pole_angle = pd.cut([-1, 1], bins=6 , retbins=True, right = False)[1]
angle_vel = pd.cut([-3.5, 3.5], bins=6, retbins=True, right = False)[1]

q = np.zeros([10 ,10, 8 ,8 , 2])
#q = np.random.rand(10,10,10,10,2)
#print q[2,6,2,1]
#Q-Learning Parameters
learning_rate = 0.1
start_explore = 1 
explore_decay = 0.995
explore_rate_min = 0.1
discount_factor = 0.9  

ep_num = 10000
max_t = 200
solved_t = 199
solved_num  = 0
solved_max = 100

DEBUG = False
    
def main():
    solved_count = 0
    rewardsum = 0
    reward_max = 0

    num_streaks = 0
    solved_num = 0
    explore_rate = start_explore
    rand_count = 0
    max_count = 0

    count_list = [0,0]
    
    fig = plt.gcf()
    fig.set_size_inches(30, 30, forward=True)
    fig.show()
    fig.canvas.draw()
  #  plt.axis([0, 2000, 0, 200])

#    fig = plt.gcf()
#    fig.show()
#    fig.canvas.draw()
 #   plt.axis([0, 1000, 0, 2])
 
 
    for ep in range(ep_num):
        count_list = [0,0]
        obv = env.reset()
        in_stateone  , in_statetwo , in_statethree, in_statefour = get_ob_to_ind(obv)
   
        for t in range(max_t):
            env.render()
            explore_rate *= explore_decay
            explore_rate = max(explore_rate, explore_rate_min)

            
            action = select_action(in_stateone, in_statetwo, in_statethree, in_statefour, explore_rate)[0]
 #           print select_action(in_stateone, in_statetwo, in_statethree, in_statefour, explore_rate)[1]

            if select_action(in_stateone, in_statetwo, in_statethree, in_statefour, explore_rate)[1] == 'random':
                count_list[0] += 1
 #               print "random"
            else:
                count_list[1] += 1
#                print "max"

           # print count_list
            
            obv, reward , done, info = env.step(action)
           # print obv           
            stateone  , statetwo , statethree , statefour = get_ob_to_ind(obv)

            if DEBUG == True:
                print obv
                print "action = " , action
                print stateone  , statetwo , statethree, statefour
                print in_stateone, in_statetwo , in_statethree, in_statefour

            try: 
                best_q = np.amax( q[ stateone  , statetwo  , statethree, statefour]   )
                
            except IndexError:
                print "index error on best_q"
                print "stateone",stateone
                print "statetwo",statetwo
                print "statethre",statethree
                print "statefour",statefour

            try:
 #              print "reward", reward
#                print "best q" , best_q
                q[ in_stateone , in_statetwo  , in_statethree , in_statefour][action] += learning_rate * (reward + discount_factor*(best_q) - q[ in_stateone , in_statetwo  , in_statethree, in_statefour ][action])
                #print q[ in_stateone , in_statetwo  , in_statethree , in_statefour][action]
                #print "reward", reward

            except IndexError:
                print "index error on q"
                print in_stateone
                print in_statetwo
                print in_statethree
                print in_statefour

            in_stateone = stateone
            in_statetwo = statetwo
            in_statethree = statethree
            in_statefour = statefour
            
            if ep % 100 == 0 & ep != 0:
                print q
 #               statevisited = np.count_nonzero(q)
                print np.count_nonzero(q)
               # print q
                print best_q
            
            if done:
               print("Episode %d finished after %f time steps" % (ep , t))
               if (t >= solved_t):
                   solved_num += 1
                   print "success"
               else:
 #                  print "you get nothing"
 #                 q[ in_stateone , in_statetwo  , in_statethree , in_statefour][action] -= .1
 #                 print q[ in_stateone , in_statetwo  , in_statethree , in_statefour][action]

                   solved_num = 0
               break

        if solved_num == solved_max:
            print "solved!"
            break

       # print count_list

        plt.figure(1)
        plt.subplot(221)
        plt.title("explore rate and q matrix average")
        plt.scatter(ep, explore_rate)
        plt.scatter(ep, np.mean(q) , c='g')
 #       fig.canvas.draw() 

        plt.subplot(222)
        plt.scatter(ep, np.count_nonzero(q) , c = 'yellow')
        plt.scatter(ep, t)
        plt.axis([0, 1000, 0, 200])
        plt.title("episode reward (blue) number of Q(s,a) visited states (red)")


        plt.subplot(223)
        plt.title("q matrix average")
        plt.scatter(ep, np.mean(q) , c='g')

        plt.subplot(224)
        plt.title("count of random (blue) vs greedy actions (red)")
        plt.bar(ep  , count_list[0])
        plt.bar(ep  , count_list[1], bottom = count_list[0],color = 'r')
 #       plt.xticks(ep, ("randoms","maexes"))
 #      plt.xticks(ep, ('random', 'max'))

        fig.canvas.draw() 

    

def get_ob_to_ind(obv):
    bin0 = np.digitize(obv[0],x_pos)
    bin1 = np.digitize(obv[1],x_vel)
    bin2 = np.digitize(obv[2],pole_angle)
    bin3 = np.digitize(obv[3],angle_vel)
    return int(bin0) , int(bin1), int(bin2), int(bin3)

def select_action(stateone, statetwo , statethree,statefour, explore_rate):
    if random.random() < explore_rate: 
        action = env.action_space.sample()
        return [int(action), "random"]
        #print "random"
    else:
         action = np.argmax( q[stateone, statetwo, statethree, statefour] )
         return [int(action), "max"]
    #return int(action)
        
if __name__ == "__main__":
    main()
