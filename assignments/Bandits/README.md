# AI Lab 3 Multi-Armed Bandits
Multi-armed bandits are a simple reinforcement learning method that forms the foundation of many large-scale recommender systems.

To get an overview of multi-armed bandits in their implementation take a look at:

* ["Towards Data Science" introduction to multi-armed bandits](https://towardsdatascience.com/solving-multiarmed-bandits-a-comparison-of-epsilon-greedy-and-thompson-sampling-d97167ca9a50)

* [Academic overview paper](https://arxiv.org/pdf/1402.6028)

## Task
In the lab, you will implement a multi-armed bandit to solve an example problem.
Your bandit will need to beat a “naïve” benchmark.
Also, we will determine the best-performing bandit of all submissions.
**You can (and are encouraged to) work in pairs**.

## Requirements
You need to have the following software installed and accounts set up to solve this exercise:

* [Python 3.7.x or 3.8.x](https://www.python.org/);

* You can use [git](https://git-scm.com/) to check out the repository, but this is not required;

* A text editor or development environment like [Visual Studio Code](https://code.visualstudio.com/) or [PyCharm](https://www.jetbrains.com/pycharm/).

We recommend using a Unix-based operating system (Mac OS, Linux) or Windows with a bash emulator for this exercise.
If you don't know ``Python``, search online for some tutorials.
If you don't know ``git``, consider learning it, but you'll be able to solve the assignment without git knowledge.

## Getting Started

**Note that we will have an online "lab session" to get you started with the assignment.**
**Attending the session will help you solve the assignment quickly and accurately.**

Open the GitLab repository we use for this exercise: [https://git.cs.umu.se/courses/5dv181ht18](https://git.cs.umu.se/courses/5dv181ht18).

Download (click the **Download** button) or ``clone`` the repository:

```
git@git.cs.umu.se:courses/5dv181ht18.git
```

If you have already cloned the repository, you can run ``git pull --rebase`` to get the latest changes.
In case you have made changes to the repository, you need to stash them beforehand (``git stash``); you can apply them afterwards with ``git stash apply``.

Navigate into the ``assignments/Bandits/`` folder in the project.
Install the dependencies for the assignment:

```
cd multi-armed-bandits
pip install -r requirements.txt
```

Open the ``MyBandit.py`` file in the project's root directory. You will see an implementation of a simple epsilon-greedy bandit.
Your task is to improve the bandit and so that you can beat the initial bandit's performance reliably.
Out of 20 simulation runs with 1.000 +/-500 "pulled arms" each, your new bandit should outperform the reference bandit by at least 25% (25% more reward gained) in at least 16 runs.
**Note that the rewards per arm will be adjusted after each of the 20 simulation runs; i.e., your bandit must be capable of adjusting to these changes.**

To test your implementation, run ``pytest`` in the repository's root directory.

## Report
Once you have achieved satisfactory performance, don't hesitate to improve further ;-), but more importantly, write a short report that describes:

1. how you proceeded;

2. what your results are;

3. how you could improve further.

The report should be approximately one page long; not much shorter, not much longer.
The report must have a title page including your name, your username at computing science (of both students if you work in pair), the course name, course code, and the assignment name.

## Hand-in

Hand-in the report and a copy of your code in [Labres](https://webapps.cs.umu.se/labresults/v2/courseadmin.php?courseid=458).
The only program code you need to hand in is the ``MyBandit.py`` file.
**Do not hand in a .zip file.**
**Also, ensure your implementation only depends on changes made to ``MyBandit.py``.**

Upon hand-in, the test (``pytest``) will automatically run to check if your submissions fulfills the technical requirements.
Please check to make sure the test passes. If not, you can re-submit.
