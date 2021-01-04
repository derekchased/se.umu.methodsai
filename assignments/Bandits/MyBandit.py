import random
import numpy as np
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


class Bandit:
    """
    Upper confidence bound bandit
    """

    def __init__(self, arms, epsilon=0.6):
        """
        Initiates the bandits

        :param arms: List of arms
        :param epsilon: The learning rate for UCB
        """
        self.arms = arms
        self.epsilon = epsilon
        self.observations = [[] for x in range(len(arms))]
        self.history = []
        self.frequencies = [0] * len(arms)
        self.sums = [0] * len(arms)


    def N(self):
        """
        Calculate the number of runs
        
        Returns:
            int: total number of runs for this bandit object
        """
        return len(self.history)

    def expected_values(self):
        """
        The expected value (mean) of each arm
        
        Returns:
            Numpy array: elements correspond by arm index
        """
        return np.array(self.sums)/np.array(self.frequencies)

    def run(self):
        """
        Asks the bandit to recommend the next arm

        :return: Returns the arm the bandit recommends pulling
        """


        if min(self.frequencies) == 0:
            return self.arms[self.frequencies.index(min(self.frequencies))]
        
        return self.arms[self.ucb_index()]

    def ucb_index(self):
        """
        The Upper confidence bound algorithm
        
        Returns:
            int: the index of the arm based on ucb
        """
        return np.argmax(self.expected_values() + self.epsilon * np.sqrt(np.log(self.N())/self.frequencies))


    def give_feedback(self, arm, reward):
        """
        Sets the bandit's reward for the most recent arm pull.
        Stores observations for each arm


        :param arm: The arm that was pulled to generate the reward
        :param reward: The reward that was generated
        """
        arm_index = self.arms.index(arm)
        self.history.append(arm_index)
        self.observations[arm_index].append(reward)
        self.sums = [sum(x) for x in self.observations]
        self.frequencies = [len(x) for x in self.observations]
