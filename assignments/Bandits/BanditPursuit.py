# epsilon-greedy example implementation of a multi-armed bandit
import random

import os,sys,inspect
import numpy as np
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


class BanditPursuit:
    """
    Generic epsilon-greedy bandit that you need to improve
    """

    def __init__(self, arms, epsilon=0.1):
        """
        Initiates the bandits

        :param arms: List of arms
        :param epsilon: Epsilon value for random exploration
        """
        self.arms = arms
        self.epsilon = epsilon
        self.frequencies = [0] * len(arms)
        self.sums = [0] * len(arms)
        self.expected_values = [0] * len(arms)
        self.observations = [[] for x in range(len(arms))]
        self.std_devs = [0] * len(arms)
        #self.filtered_arms = []
        self.probs = [1/len(arms)] * len(arms)
        #print(np.sum([0.10276779754004604, 0.196567797540046, 0.0027677975400460103, 0.69236101229977, 0.0027677975400460103, 0.0027677975400460103]))
        self.rng = np.random.default_rng()


    def run(self):
        """
        Asks the bandit to recommend the next arm

        :return: Returns the arm the bandit recommends pulling
        """

        # decision making part

        # if arm has not been run, run it
        #if min(self.frequencies) == 0:
        if min(self.frequencies) == 0:
            return self.arms[self.frequencies.index(min(self.frequencies))]
                

        # randomly pick an arm based on distribution
        index = self.rng.choice(len(self.arms), p= self.probs)
        return self.arms[index]

        # otherwise, return the best arm
        #return self.arms[self.expected_values.index(max(self.expected_values))]

    def give_feedback(self, arm, reward,alpha):
        """
        Sets the bandit's reward for the most recent arm pull

        :param arm: The arm that was pulled to generate the reward
        :param reward: The reward that was generated
        """

        # more precise history of the arm runs

        # get the specific arm
        arm_index = self.arms.index(arm)

        # calculate the new sum for this arm by adding current reward total to the new reward
        sum = self.sums[arm_index] + reward
        self.sums[arm_index] = sum

        # increment this arm's frequency counter
        frequency = self.frequencies[arm_index] + 1
        self.frequencies[arm_index] = frequency

        # Update this arm's average reward value
        expected_value = sum / frequency
        self.expected_values[arm_index] = expected_value


        if min(self.frequencies) != 0:
            bestindex = self.expected_values.index(max(self.expected_values))
            curr_prob = self.probs[bestindex]
            next_prob = curr_prob + alpha*(1-curr_prob)
            self.probs[bestindex] = next_prob
            decrease_prob = (next_prob-curr_prob)/(len(self.arms)-1)

            #print("BEFORE")
            #print(self.probs)
            for armindex,arm in enumerate(self.arms):
                if(armindex != bestindex):
                    curr_prob = self.probs[armindex]
                    next_prob = curr_prob - decrease_prob
                    if(next_prob<0):
                        correction = abs(next_prob)
                        curr_best = self.probs[bestindex]
                        self.probs[bestindex] = curr_best-correction
                        self.probs[armindex] = 0
                    else:
                        self.probs[armindex] = next_prob
                    
            #print("AFTER")
            #print(self.probs)
