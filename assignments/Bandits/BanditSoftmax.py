# epsilon-greedy example implementation of a multi-armed bandit
import random

import os,sys,inspect
import numpy as np
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


class BanditSoftmax:
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
        self.reset_frequencies = [0] * len(arms)
        self.sums = [0] * len(arms)
        self.reset_sums = [0] * len(arms)
        self.expected_values = [0] * len(arms)
        #self.observations = [[] for x in range(len(arms))]
        #self.std_devs = [0] * len(arms)
        #self.filtered_arms = []
        #print(np.sum([0.10276779754004604, 0.196567797540046, 0.0027677975400460103, 0.69236101229977, 0.0027677975400460103, 0.0027677975400460103]))
        self.probs = []
        self.rng = np.random.default_rng()


    def run(self):
        """
        Asks the bandit to recommend the next arm

        :return: Returns the arm the bandit recommends pulling
        """

        # decision making part

        # if arm has not been run, run it
        #if min(self.frequencies) == 0:
        if min(self.reset_frequencies) == 0:
            return self.arms[self.reset_frequencies.index(min(self.reset_frequencies))]

        #if random.random() < self.epsilon:
            #self.epsilon = self.epsilon*.90
        #    return self.arms[random.randint(0, len(self.arms) - 1)]
        
        
        # randomly pick an arm based on distribution
        index = self.rng.choice(len(self.arms), p= self.probs)
        #print("probs", np.around(self.probs,5))
        #print("self.expected_values", self.expected_values)
        #print("index",index)
        #return self.arms[self.frequencies.index(min(self.frequencies))]
        return self.arms[index]

        # otherwise, return the best arm
        #return self.arms[self.expected_values.index(max(self.expected_values))]

    def give_feedback(self, arm, reward):
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

        reset_sum = self.reset_sums[arm_index] + reward
        self.reset_sums[arm_index] = reset_sum

        # increment this arm's frequency counter
        frequency = self.frequencies[arm_index] + 1
        self.frequencies[arm_index] = frequency

        # increment this arm's reset frequency counter
        reset_frequency = self.reset_frequencies[arm_index] + 1
        self.reset_frequencies[arm_index] = reset_frequency

        # Update this arm's average reward value
        expected_value = reset_sum / reset_frequency
        self.expected_values[arm_index] = expected_value

        tau = self.epsilon
        expected_values_np = np.array(self.expected_values)
        numerator = np.exp(expected_values_np/tau)
        denominator = np.sum(numerator)
        self.probs = numerator/denominator

        #if(np.sum(self.reset_frequencies) >= 4000):
            #print("probs", np.around(self.probs,5))
            #print("self.expected_values", self.expected_values)
         #   self.reset_frequencies = [0] * len(self.sums)
          #  self.reset_sums = [0] * len(self.sums)
          #  self.expected_values = [0] * len(self.sums)

