import os,sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import numpy as np
import gym
from gym import spaces
env = gym.make('CartPole-v1')
#https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py
#Solve with Q Learning - basically
#action observe reward
#our aim is to create a policy using q learning to keep the cart pole up right. 
#which is really just asking ourselves, if we are here and we do this - is it good is it bad?


print(env.action_space)
#action space is 2: it can move left or right, discrete
print(env.observation_space)
print(env.observation_space.low)
print(env.observation_space.high)

jh = env.observation_space.high
jp = env.observation_space.low

print jh[2]
print jp[2]
#environment space has x position, x velocity, angle of stick and stick velocity

ep_num = 10000
max_t = 200
solved_num  = 0
solved_max = 100

def run_sim(max_t,ep_num , weights, ep):
    solved_num=0
    totalreward = 0
    observation = env.reset()
    reward_sum = 0
    for t in range(max_t):
        env.render()
        action = 0 if np.matmul(weights, observation) < 0 else 1
        observation, reward, done, info = env.step(action)
        totalreward += reward

        if t+1 == max_t:
            print "Epsiode %d survived all %d time steps" %(ep,t+1)
            print "reward of %d produced" %(totalreward)
            solved_num += 1
            break
          
        if done:
            #print reward_sum
            print "done"
            print "Epsiode %d failed after %d time steps" %(ep,t+1)
            print "reward of %d produced" %(totalreward)
            solved_num = 0
            break

    return totalreward
    
def main():
    solved_count = 0
    rewardsum = 0
    reward_max = 0
    rand_scale = 0.1
    weights =  np.random.uniform(-1,1,4)

    
    for ep in range(ep_num):
        
        updated_weights = weights + (np.random.uniform(-1,1,4) * rand_scale)
        reward = run_sim(max_t, ep_num, updated_weights, ep)
        print reward
        print updated_weights
        if reward > reward_max:
            reward_max = reward
            weights = updated_weights

        print reward_max

        if reward == max_t:
            print "solved number"
            solved_count += 1
        else:
            solved_count = 0
 
        if solved_max == solved_count:
            print "yes consistency baby!"
            print "solution passed %d times in succession" %(solved_max)
            break
        
if __name__ == "__main__":
    main()
