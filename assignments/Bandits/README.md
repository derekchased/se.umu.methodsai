# AI Lab 3 Multi-Armed Bandits
Multi-armed bandits are a simple reinforcement learning method that forms the foundation of many large-scale recommender systems.

To get an overview of multi-armed bandits in their implementation take a look at:

* ["Towards Data Science" introduction to multi-armed bandits](https://towardsdatascience.com/solving-multiarmed-bandits-a-comparison-of-epsilon-greedy-and-thompson-sampling-d97167ca9a50)

* [Academic overview paper](https://arxiv.org/pdf/1402.6028)

## Task
In the lab, you will implement a multi-armed bandit to solve an example problem.
Your bandit will need to beat a “naïve” benchmark.
Also, we will determine the best-performing bandit of all submissions.

## Requirements
You need to have the following software installed and accounts set up to absolve this exercise:

* [Python 3.7.x or 3.8.x](https://www.python.org/);

* You can use [git](https://git-scm.com/) to check out the repository, but this is not required;

* A text editor or development environment like [Visual Studio Code](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/).

We recommend using a Unix-based operating system (Mac OS, Linux) or Windows with a bash emulator for this exercise.
If you don't know either ``git`` or ``Python``, search online for some tutorials and absolve them.

## Getting Started

Open the GitLab repository we use for this exercise: [https://git.cs.umu.se/courses/5dv181ht18](https://git.cs.umu.se/courses/5dv181ht18).

Download (click the **Download** button) or ``clone`` the repository:

```
git@git.cs.umu.se:courses/5dv181ht18.git
```

Navigate into the ``assignments/Bandits/`` folder in the project.
Install the dependencies for the assignment:

```
cd multi-armed-bandits
pip install -r requirements.txt
```

Open the ``MyBandit.py`` file in the ``src`` directory. You will see an implementation of a simple epsilon-greedy bandit.
Your task is to improve the bandit and so that you can beat the initial bandit's performance reliably.
Out of 20 simulation runs with 1.000 "pulled arms" each, your new bandit should outperform the reference bandit by at least 5% (5% more reward gained) in at least 15 runs.

To test your implementation, open the ``test_runner.py`` file.
Delete the line ``assert True`` (line 21) and remove the comment in front of the next line.
Then, run ``pytest`` in the repository's root directory.

## Report
Once you have achieved satisfactory performance, don't hesitate to improve further ;-), but more importantly, write a short report that describes:

1. how you proceeded;

2. what your results are;

3. how you could improve further.

The report should be approximately one page long; not much shorter, not much longer.

## Hand-in
To hand in the exercise, first add, commit and push your changes (**don't forget to adjust the branch name in the example below**):

```
git add --all
git commit -m 'add custom multi-armed bandit implementation'
git push --set-upstream origin <your-branch-name>
git push
```
**Important: NEVER USE THE ``--force`` OPTION WHEN PUSHING A BRANCH!**

Then, go to ``https://github.com/TimKam/multi-armed-bandit-lab/pulls`` and create a pull request for your branch.
Make sure all tests pass for your pull requests.
Then, add the link to your pull request to your report.
Hand-in the report and a copy of your code in [Labres](https://webapps.cs.umu.se/labresults/v2/handin.php?courseid=402).
