import gym

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import quandl

import gym_perudo

env = gym.make('perudo_game-v0')


gamma = 0.95
alpha = 0.05
n_eps = 1

epsilon_max = 1.0
epsilon_min = 0.05
epsilon_step = (epsilon_max - epsilon_min) / n_eps
epsilon_decay = 0.999

# Q-table
q_table = np.zeros((env.observation_space.n, env.action_space.n))

ep_reward = []
# init epsilon
epsilon = epsilon_max

for _ in range(n_eps):
    ob = env.reset()
    done = False
    while not done:
        #env.render()
        # epsilon-greedy
        if np.random.uniform(0,1) >= epsilon:
            a = np.argmax(q_table[ob])
        else:
            a = env.action_space.sample()

        new_ob, r, done, _ = env.step(a)
        # update Q value
        q_table[ob][a] += alpha * (r + gamma * np.max(q_table[new_ob]) - q_table[ob][a])
        ob = new_ob

    final_reward = r
    ep_reward.append(final_reward)

    #epsilon *= epsilon_decay
    epsilon = max(epsilon-epsilon_step, epsilon_min)

#print('Q table \n', q_table)

#plt.plot(ep_reward)
#plt.title('rewards')
#plt.show()


#def smooth_reward(ep_reward, smooth_over):
#    smoothed_r = []
#    for ii in range(smooth_over, len(ep_reward)):
#        smoothed_r.append(np.mean(ep_reward[ii-smooth_over:ii]))
#    return smoothed_r

#plt.plot(smooth_reward(ep_reward, 20))
#plt.title('smoothed reward')
#plt.show()

# game performance
#ep_reward_validation = []
#for ii in range(1):
#    ob = env.reset()
#    total_reward = 0.0
#    done = False
#    while not done:
#        env.render()
#        a = np.argmax(q_table[ob])
#        ob_, r, done, _ = env.step(a)
#        total_reward += r
#        ob = ob_
#    ep_reward_validation.append(total_reward)
#
#print('average game score over 100 eps: ', np.mean(ep_reward_validation))
