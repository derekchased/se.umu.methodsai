# epsilon-greedy example implementation of a multi-armed bandit
import random
import numpy as np
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


class Bandit:
    """
    Generic epsilon-greedy bandit that you need to improve
    """

    def __init__(self, arms, epsilon=0.6):
        """
        Initiates the bandits

        :param arms: List of arms
        :param epsilon: Epsilon value for random exploration
        """
        self.arms = arms
        self.epsilon = epsilon
        self.observations = [[] for x in range(len(arms))]
        self.history = []
        self.window_size = 20
        self.frequencies = [0] * len(arms)
        self.sums = [0] * len(arms)

    def N(self):
        return len(self.history)

    def expected_values(self):
        return np.array(self.sums)/np.array(self.frequencies)

    def run(self):
        """
        Asks the bandit to recommend the next arm

        :return: Returns the arm the bandit recommends pulling
        """


        if min(self.frequencies) == 0:
            return self.arms[self.frequencies.index(min(self.frequencies))]
        
        ucb_index = np.argmax(self.expected_values() + self.epsilon * np.sqrt(np.log(self.N())/self.frequencies))
        #print("ucb",ucb_index,self.expected_values() + c * np.sqrt(np.log(self.N())/self.frequencies))

        return self.arms[ucb_index]

        
        if random.random() < self.epsilon:
            return self.arms[random.randint(0, len(self.arms) - 1)]


        return self.arms[ np.argmax(self.expected_values())  ]

    def give_feedback(self, arm, reward):
        """
        Sets the bandit's reward for the most recent arm pull

        :param arm: The arm that was pulled to generate the reward
        :param reward: The reward that was generated
        """
        arm_index = self.arms.index(arm)
        self.history.append(arm_index)
        self.observations[arm_index].append(reward)
        self.sums = [sum(x) for x in self.observations]
        self.frequencies = [len(x) for x in self.observations]
