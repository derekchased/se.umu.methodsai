from ReferenceBandit import ReferenceBandit
from BanditSoftmax import BanditSoftmax
from BanditPursuit import BanditPursuit
from BanditUCB import BanditUCB
import simulator as simulator
import random
import math


def simulate():
    """
    Simulates the two bandits and returns the simulation results

    :return: simulation results, list, for each entry:
             1 if bandit  beats reference bandit (* 1 + bonus); else 0

    """

    # configuration
    arms = [
        'Configuration a',
        'Configuration b',
        'Configuration c',
        'Configuration d',
        'Configuration e',
        'Configuration f'
    ]

    # instantiate bandits
    banditSoftmax = BanditSoftmax(arms)
    banditPursuit = BanditPursuit(arms)
    banditUCB = BanditUCB(arms)
    ref_bandit = ReferenceBandit(arms)
    
    for sample in range(20):
        for c in range(20):
            results = []
            banditUCB = BanditUCB(arms, c/10)
            ref_bandit = ReferenceBandit(arms)
            for index in range(0, 20):
                random.seed(index)
                iterations = int(math.floor(1000 * (random.random()) + 0.5))
                #bandit_pursuit_reward = simulator.simulate("bandit pursuit",banditPursuit, iterations,.1)
                bandit_softmax_reward = simulator.simulate("bandit softmax",banditSoftmax, iterations,.1)

                #banditUCB_reward = simulator.simulate("bandit UCB",banditUCB, iterations,c)

                #banditSoftmax.reset_frequencies[0]=5000
                ref_bandit_reward = simulator.simulate("bandit reference",ref_bandit, iterations)
                
                ref_plus_bonus = ref_bandit_reward * 1.35
                result = 0
                #print("\n",index,iterations)
                #print("bandit_pursuit_reward",bandit_pursuit_reward)
                #print("bandit_softmax_reward",bandit_softmax_reward)
                #print("ref_bandit_reward",ref_bandit_reward)
                #print("ref_plus_bonus",ref_plus_bonus)
                if (banditUCB_reward > ref_plus_bonus):
                    result = 1
                results.append(result)
                
            print("results",sample,c/10, sum(results),results)
    return results


def test_performance():
    """
    Checks if the simulation is good enough to pass
    """
    assert sum(simulate()) > 15

test_performance()