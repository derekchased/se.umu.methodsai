# epsilon-greedy example implementation of a multi-armed bandit
import random

import os,sys,inspect
import numpy as np
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


class Bandit:
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
        self.filtered_arms = [False] * len(arms)
        print("self.filtered_arms",self.filtered_arms)

    def run(self):
        """
        Asks the bandit to recommend the next arm

        :return: Returns the arm the bandit recommends pulling
        """

        # decision making part

        # if arm has not been run, run it
        #if min(self.frequencies) == 0:
        if min(self.frequencies) <= 3:
            return self.arms[self.frequencies.index(min(self.frequencies))]
                
        # randomly pick an arm (less than .1 chance)
        if random.random() < self.epsilon: 

            # decay epsilon
            self.epsilon *= .9

            # Update filter
            max_arm_index = self.expected_values.index(max(self.expected_values))
            max_reward = self.expected_values[max_arm_index]
            max_std_dev = self.std_devs[max_arm_index]
            benchmark = max_reward - 2*max_std_dev
            arm_probs = []
            for arm in range(len(self.filtered_arms)):
                if(self.filtered_arms[arm]):
                    arm_probs.append(0)
                    continue
                max_val_for_arm = self.expected_values[arm] + self.std_devs[arm]
                if(max_val_for_arm < benchmark):
                    self.filtered_arms[arm] = True
                    arm_probs.append(0)
                else:
                    arm_probs.append(random.random())

            print("self.filtered_arms",self.filtered_arms)

            #return self.arms[random.randint(0, len(self.arms) - 1)]

            return self.arms[arm_probs.index(max(arm_probs))]

        # otherwise, return the best arm
        return self.arms[self.expected_values.index(max(self.expected_values))]

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

        # increment this arm's frequency counter
        frequency = self.frequencies[arm_index] + 1
        self.frequencies[arm_index] = frequency

        # Update this arm's average reward value
        expected_value = sum / frequency
        self.expected_values[arm_index] = expected_value

        # append new reward
        self.observations[arm_index].append(reward)

        std_dev = np.std(self.observations[arm_index])
        self.std_devs[arm_index] = std_dev
        
