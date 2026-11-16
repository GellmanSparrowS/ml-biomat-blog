# Reinforcement learning: from exploration to decisions

Source: https://ml-biomat.com/tutorials/machine-learning/m24/en/
Language: en

Use restaurant choices and cliff-side routes to understand bandits, MDPs, Bellman updates, TD, SARSA and Q-learning.

## Choosing lunch, then learning to walk

On your first day in an unfamiliar neighbourhood, you can return to a restaurant you already enjoyed or try somewhere new. The familiar choice offers a reasonably predictable benefit; the new one offers information that may improve future choices. If you have one lunch left in the neighbourhood, that information has little time to pay off. If you will live there for a year, learning about the alternatives early can be valuable. This is one of the central problems of reinforcement learning: actions produce outcomes, and they also influence what the learner gets to discover. Recommender systems, game characters and warehouse robots encounter different versions of this problem.

Choosing lunch and learning a route have an important difference. In the simplest multi-armed bandit model, choosing one restaurant today does not change the restaurants available tomorrow. A reward depends on the selected option, but there is no evolving position to manage. Walking is sequential: moving right takes you somewhere else and changes the actions available afterwards. A detour that appears wasteful now may avoid a dangerous section later. We will therefore start with exploration in a bandit, introduce states and long-term returns, and then compare SARSA with Q-learning in a small cliff-walking task. A table of numbers is sufficient to reveal the main ideas.

The feedback also differs from ordinary supervised learning. A labelled digit image tells a classifier the desired answer for that image. An environment usually tells a moving agent how much time a step cost, whether it reached a goal, or whether it fell; it does not supply a correct action at every location. The learner must determine which earlier decisions contributed to later outcomes. This is the problem of delayed credit assignment. Before selecting an algorithm, establish whether actions affect future states, what feedback is available, and how expensive exploration will be. Those decisions determine the appropriate model and experimental setting.

![Actions produce rewards and new states; values and policies influence the next action. The lower strip connects the TD (1988) and Q-learning (1992) papers to prediction and control. Original conceptual diagram.](https://ml-biomat.com/static/tutorials/machine-learning/figures/9635c30676af262d7dd2726b.svg?v=9635c30676af)

Figure 1Actions produce rewards and new states; values and policies influence the next action. The lower strip connects the TD (1988) and Q-learning (1992) papers to prediction and control. Original conceptual diagram.

## The cost of exploring and the cost of never exploring

Represent four restaurants by four buttons. Pressing a button produces a noisy score whose expectation describes its long-run quality. Individual scores fluctuate, just as a meal can vary with waiting time or the day's preparation. Averaging the scores observed for an option gives an estimate of its action value. The average can be updated incrementally: subtract the old estimate from the new observation, multiply that difference by a suitable step size, and add it back to the estimate. When the step size is the reciprocal of the observation count, this operation exactly reproduces the ordinary sample mean while storing only the count and the current estimate.

$$
\widehat q_{n+1}(a)=\widehat q_n(a)+\frac{R_{n+1}-\widehat q_n(a)}{n+1}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Index of an option or action; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/1dcdc987095eab8d037d9299.svg) | Estimated mean reward for action a after n observations; reward units. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Number of previous observations of this action; a positive integer. The first sample initializes a new action. |
| ![Formula](https://ml-biomat.com/static/agent-math/e9bd7eea834fbc463ff80d4e.svg) | New reward observed for this action; the same units as its estimated value. |

Write the previous sum as n times the old mean, add one observation and divide by n+1. Rearranging gives the incremental expression. Rewards 1 and 3 give a mean of 2; observing 8 next updates it to 2+(8−2)/3=4, exactly the mean of all three rewards.

A greedy policy always selects the option with the highest current estimate. A good option that happened to receive a poor first score may then never be tried again, leaving its estimate permanently uncorrected. An ε-greedy policy reserves a probability ε for a uniformly random action and uses a greedy action otherwise. With four options and ε=0.1, each option receives at least 0.025 probability. A unique greedy option also receives the remaining 0.9, giving it probability 0.925 in total. Exploration does not necessarily mean choosing a different option: a random action can select the current favourite again.

Upper confidence bound selection, or UCB, makes exploration depend on what is still uncertain. It adds an exploration bonus to the estimated reward. Options with fewer observations receive larger bonuses; increasing the total number of decisions also encourages occasional reconsideration of neglected options. The bonus is a score used for choosing actions, not additional reward supplied by the restaurant. In our synthetic experiment, the four true means are 0.2, 0.5, 0.8 and 1.0, with Gaussian observation noise of standard deviation 1. We know those means because we constructed the environment. The learning algorithm sees only one noisy observation from its selected option at each decision.

$$
A_t=\operatorname*{arg\,max}_{a}\left[\widehat q_t(a)+\sqrt{\frac{2\ln t}{N_t(a)}}\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/697849e3b4a294a61c884ddf.svg) | Action chosen at decision t; dimensionless index. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Total decision count, dimensionless inside the natural logarithm. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | An available action index. |
| ![Formula](https://ml-biomat.com/static/agent-math/92f660195cb755b8afcb07a1.svg) | Current estimated mean reward for action a. |
| ![Formula](https://ml-biomat.com/static/agent-math/10dc61f0abc250b5fa83fc7d.svg) | Number of previous selections of action a; strictly positive. |
| ![Formula](https://ml-biomat.com/static/agent-math/aefc7a76c9ed1e58f8195e33.svg) | Natural logarithm; the bonus uses the normalized reward scale of this experiment. |

Select each action once before applying this expression. At t=100, N=4 and estimated mean 0.5, the exploration bonus is about 1.517 and the selection score about 2.017. This score guides action selection; it does not change the environment reward. Other confidence bonuses use assumptions matched to different reward distributions.

Cumulative pseudo-regret adds the difference between the best true mean and the mean of the option selected at every step. It measures the quality of the choices separately from the particular reward noise. A mediocre option that happens to produce a large random reward has not become the best option. Across 32 seeds and 400 decisions per run, the mean final pseudo-regrets in this experiment are approximately 96.84 for greedy selection, 42.13 for ε-greedy and 37.38 for UCB. The right panel retains one point per run, revealing experiences hidden by a mean curve. If the true means change over time, a sample average can adapt slowly; a moving window or a constant step size changes how strongly recent evidence influences the estimate.

![Four synthetic stationary arms, 32 seeds and 400 choices per run. Lines show mean cumulative pseudo-regret and bands show interquartile ranges across seeds. Each right-panel point is one run. Reward noise standard deviation is 1.](https://ml-biomat.com/static/tutorials/machine-learning/figures/c782932ef731525e790c44d1.svg?v=c782932ef731)

Figure 2Four synthetic stationary arms, 32 seeds and 400 choices per run. Lines show mean cumulative pseudo-regret and bands show interquartile ranges across seeds. Each right-panel point is one run. Reward noise standard deviation is 1.

## A map for sequential decisions

Once an action changes what happens next, the model needs a state. A Markov decision process, or MDP, specifies states, actions, transition rules, rewards and a discount factor. The state should contain the information needed to predict the next transition. Position is sufficient for the grid world in this chapter. Position alone is often insufficient for a moving robot: velocity, battery charge and observations of obstacles may also matter. The Markov property says that, conditional on the current state and action, earlier history supplies no further information about the next transition. A description such as “in the middle of the corridor” can omit essential information if the robot's direction and speed affect what happens next.

A policy maps a state to a distribution over actions. A deterministic policy might be drawn as one arrow per grid cell. A stochastic policy assigns probabilities to up, right, down and left. Reward expresses a preference for an individual transition, whereas return combines rewards over the future. A useful step towards the goal can receive a negative immediate reward because it takes time, even though it improves the eventual outcome. The discount factor γ controls the weight of distant rewards. It can represent a preference concerning delay and, for continuing tasks, help make an infinite sum finite. Our cliff-walking training task ends at the goal and uses γ=1, so its reported return is the ordinary sum of rewards collected during the episode.

$$
G_t=\sum_{k=0}^{T-t-1}\gamma^kR_{t+k+1}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33cb70bd20d03f7b40d90d58.svg) | Discounted return following time t; reward units. |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | Terminal time of this episode, counted in action steps. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Current time step. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Nonnegative offset into the future; summation index. |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | Dimensionless discount factor; training uses 1 for this episodic task. |
| ![Formula](https://ml-biomat.com/static/agent-math/6780ac06aa49cd1f2d595b2a.svg) | Reward received after action at time t+k. |

The next reward has weight 1, the following reward γ, and the third γ². Rewards −1, −1 and 10 give return −1−0.9+8.1=6.2 when γ=0.9. With γ=1 the same trajectory has return 8. Discounting changes the aggregation of rewards, not the observed rewards themselves.

A value function estimates the expected return from being in a state and subsequently following a particular policy. State value V evaluates the starting position; action value Q additionally specifies the first action. Both average over future randomness rather than predicting one exact trajectory. An exploratory action may cause one run to fall while another run reaches the goal smoothly. A value estimate combines these possibilities according to their probabilities. Policy evaluation can therefore examine mean return, failure probability and the complete return distribution. When a task values the worst outcomes differently, that preference belongs in the objective or constraints rather than being silently delegated to a mean score.

## Why a long journey can be decomposed into one step

A trajectory's return can be separated into the reward from the next transition and the discounted return from everything after that transition. The second part has the same structure as the original problem, with a different starting state. This is the basis of a Bellman recursion. Think of planning a railway journey: if the remaining cost from every possible interchange were already known, you could compare the first train by adding its cost to the appropriate continuation. The recursion does not make the future disappear. It stores information about the future in values attached to states, allowing neighbouring states to exchange that information through repeated updates.

$$
V^*(s)=\max_a\sum_{s'}P(s'\mid s,a)\left[r(s,a,s')+\gamma V^*(s')\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Current state, such as a grid position. |
| ![Formula](https://ml-biomat.com/static/agent-math/e4e16dc8fdd57e2b4df015df.svg) | A possible next state; the sum ranges over these states. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | An available action. |
| ![Formula](https://ml-biomat.com/static/agent-math/d0a36a87631d65297a8473b9.svg) | Optimal expected return from state s; reward units. |
| ![Formula](https://ml-biomat.com/static/agent-math/839101a417c5f6ac8aea5ab5.svg) | Transition probability conditional on state and action; sums to 1 over next states. |
| ![Formula](https://ml-biomat.com/static/agent-math/4ca32dc98c9920092714bd2f.svg) | Expected immediate reward for the specified transition. |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | Dimensionless discount factor. |

Average possible continuations for each action, then compare the actions. For deterministic transitions, action A gives −1 and leads to value 8, while B gives 0.5 and leads to value 5. At γ=0.9 their targets are 6.2 and 5, so A is preferred despite its smaller immediate reward. A terminal continuation has value zero.

When transition probabilities and rewards are known, these expectations can be calculated directly through dynamic programming. Policy evaluation holds the action-selection rule fixed and updates its state values. Policy improvement then selects actions with better estimated continuations. Value iteration takes the best action within each value update. In an implementation, distinguish a synchronous sweep, which uses the entire previous value table to build a new table, from an in-place sweep, which can use entries already updated during the current pass. Both can be useful, but their intermediate states differ. Synchronous updates make it particularly easy to observe information moving across a grid one sweep at a time.

The interactive experiment below uses known transition rules and synchronous value iteration. The action-slip control makes an intended action deviate to either perpendicular direction with a specified probability. Near a cliff, this uncertainty changes the attractiveness of apparently short routes. “One sweep” updates all cells using values from the previous sweep. Set γ to zero to check that the calculation sees only immediate rewards, then increase it to observe how the influence of distant outcomes spreads. This is planning with a known model. Later, Q-learning will update a table from transitions the agent actually experiences, without enumerating the environment's possible responses during its learning update.

## Propagate a value map yourself

Take one sweep to inspect immediate rewards, then advance by 30 sweeps. Slip is the total probability of moving in either perpendicular direction, split equally. Changing a parameter recomputes the value table for the current number of sweeps.

Initial values are zero.

[Figure: Grid-world value and policy map](https://ml-biomat.com/tutorials/machine-learning/m24/en/#M24-lab)

The terminal cell has zero continuation value. This experiment calculates expectations from known transition rules: dynamic programming. The Python learner instead updates its Q table from each observed transition.

## Learning from the next prediction

An environment's transition rules are often unavailable in advance. A learner can complete an episode and use the observed return as a training target for states visited along the way. This is the Monte Carlo approach. Its target comes from the completed trajectory and contains no estimate of an unseen continuation, but a long trajectory may combine many random events and produce a highly variable return. Waiting until the end also delays learning. The practical question is whether newly obtained information can improve the previous prediction after a single step, even while the eventual outcome is still unknown.

Temporal-difference learning answers with a target consisting of the immediate reward plus the current value estimate of the next state. The difference between this target and the old prediction is the TD error. Using one prediction to help construct a target for another prediction is called bootstrapping. Sutton's 1988 paper examined how differences between predictions at successive times can drive incremental learning. The historical connection is a change in how a prediction is corrected: feedback need not wait for the final outcome if a new intermediate prediction supplies useful information. This idea is visible in a small numerical table and does not depend on a large neural network.

$$
V(s)\leftarrow V(s)+\alpha\left[r+\gamma(1-d)V(s')-V(s)\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Current state. |
| ![Formula](https://ml-biomat.com/static/agent-math/e4e16dc8fdd57e2b4df015df.svg) | Next state actually reached. |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | Immediate reward, in the same units as values. |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | Dimensionless learning step size, between 0 and 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | Dimensionless discount factor. |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Terminal indicator, 1 for a true terminal transition and 0 otherwise; a computational cap is separate. |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | Current state-value table, in reward units. |

The bracket is a TD error: one-step target minus current prediction. For old value 2, reward 1, next value 4, γ=0.9 and α=0.2, a nonterminal transition gives target 4.6 and updated value 2.52. If the transition is terminal, the target is 1 and the update gives 1.8.

For a current value of 2, an immediate reward of 1, a next-state value of 4 and γ=0.9, the target is 4.6 and the TD error is 2.6. A step size of 0.2 moves the old value one fifth of the way towards the target, producing 2.52. The step size controls how quickly evidence changes an estimate; the discount factor controls the weighting of future reward. Their roles remain different even though both appear as multipliers. At a genuine terminal state, the future contribution is zero. Stopping an illustration because its step budget is exhausted is different: if the underlying task continues, treating that interruption as terminal changes the learning target. The code distinguishes arrival at the goal from a computational step cap.

## What SARSA and Q-learning learn

To move from prediction to control, give different actions separate entries in the value table and let those values influence future choices. The name SARSA follows a five-part experience: state, action, reward, next state, next action. Its target uses the value of the next action actually selected according to the current policy. If that policy includes exploration, the learned value includes the consequences of exploratory actions. This is on-policy learning: the policy whose value is being learned matches the behaviour policy that collects experience. “On-policy” describes the relationship between a target and the data-generating policy, rather than whether the program happens to run online in real time.

$$
Q(s,a)\leftarrow Q(s,a)+\alpha\left[r+\gamma(1-d)Q(s',a')-Q(s,a)\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Current state. |
| ![Formula](https://ml-biomat.com/static/agent-math/e4e16dc8fdd57e2b4df015df.svg) | Next state actually reached. |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | Immediate reward, in the same units as values. |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | Dimensionless learning step size, between 0 and 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | Dimensionless discount factor. |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Terminal indicator, 1 for a true terminal transition and 0 otherwise; a computational cap is separate. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Current action. |
| ![Formula](https://ml-biomat.com/static/agent-math/36b400f98b136a84c0280fc3.svg) | Next action actually sampled from the current behaviour policy. |
| ![Formula](https://ml-biomat.com/static/agent-math/4be111afe7c23428ae5024a8.svg) | State-action value table; every entry has reward units. |

SARSA follows the next action sampled from its policy. For old Q=2, reward=1, selected next-action value=1, γ=0.9 and α=0.2, the target is 1.9 and the new Q is 1.98. A different next action may have value 4; SARSA still uses the selected action in this update.

Q-learning instead uses the largest action value at the next state to form its target, even if the behaviour collecting experience remains ε-greedy. Its target concerns a greedy continuation, while its data can come from exploratory behaviour, making it off-policy. Watkins and Dayan's 1992 paper establishes convergence results for the tabular setting under conditions including continued state-action sampling and appropriate learning-rate behaviour. Here we run a finite experiment with a fixed step size and inspect its learned routes and returns directly. A visually flattening curve is useful experimental information, but the theoretical result concerns a precisely specified limiting learning process.

$$
Q(s,a)\leftarrow Q(s,a)+\alpha\left[r+\gamma(1-d)\max_bQ(s',b)-Q(s,a)\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | Current state. |
| ![Formula](https://ml-biomat.com/static/agent-math/e4e16dc8fdd57e2b4df015df.svg) | Next state actually reached. |
| ![Formula](https://ml-biomat.com/static/agent-math/3a4ef1c1b261a53f9c45d0c9.svg) | Immediate reward, in the same units as values. |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | Dimensionless learning step size, between 0 and 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | Dimensionless discount factor. |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Terminal indicator, 1 for a true terminal transition and 0 otherwise; a computational cap is separate. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Current action. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Index ranging over all available next-state actions. |
| ![Formula](https://ml-biomat.com/static/agent-math/4be111afe7c23428ae5024a8.svg) | State-action value table, in reward units. |

Q-learning constructs its target from the largest next-state action value. With the preceding numbers and maximum next-state Q=4, the target is 4.6 and the updated value is 2.52. A subsequently sampled exploratory action does not change this target. Terminal transitions contribute no continuation.

Cliff walking exposes the distinction between these targets. Ten cells in the bottom row are cliffs. Entering one gives reward −100 and returns the agent to the starting cell; every other move gives reward −1, and reaching the bottom-right goal ends the episode. A greedy route just above the cliff is short. With persistent exploration, however, an occasional downward action can be expensive. Q-learning can learn a short greedy route, whereas SARSA often values a route with more clearance because it includes exploration in the continuation it evaluates. Keep training returns under exploratory behaviour separate from routes evaluated after exploration is switched off. They answer different questions about the same learned table.

## Put the objective, route and return into one experiment

The complete program runs both button selection and cliff walking. For the grid task, each algorithm is trained for 500 episodes using eight seeds, ε=0.1 and a step size of 0.5. Ties between maximum action values are resolved randomly; otherwise an all-zero initial table would systematically prefer whichever direction is first in the array. The environment function supplies the next state, reward and terminal flag, while the learning function updates values. This separation allows the same environment to support multiple algorithms and policies. Small assertions check a cliff transition, a transition into the goal and a hand-calculated TD update before the program produces its learning curves.

### Complete experiment: bandit exploration and cliff control

Requires NumPy and Matplotlib. Save as main.py and run python main.py --output results --language en; use zh for Chinese plots. transition defines the environment, learn performs TD control, and bandit compares exploration rules. summary.json and NPZ files retain numerical results, and three SVG figures come from the same computation.

```
"""Tabular reinforcement learning: bandits and the cliff-walking task.

Run: python main.py --output results --language en
Requires NumPy and Matplotlib. All data are synthetic and generated here.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

BLUE, RED, GOLD = '#176b91', '#b04743', '#c18a28'
START, GOAL, ROWS, COLS = 36, 47, 4, 12
MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def transition(state, action):
    row, col = divmod(int(state), COLS)
    dr, dc = MOVES[int(action)]
    row, col = np.clip(row + dr, 0, ROWS-1), np.clip(col + dc, 0, COLS-1)
    next_state = int(row * COLS + col)
    if row == 3 and 0 < col < 11:
        return START, -100., False
    return next_state, -1., next_state == GOAL


def choose(q, rng, epsilon):
    if rng.random() < epsilon:
        return int(rng.integers(len(q)))
    ties = np.flatnonzero(np.isclose(q, q.max(), rtol=0, atol=1e-12))
    return int(rng.choice(ties))


def learn(method, seed, episodes=500, epsilon=.1, alpha=.5, gamma=1.):
    rng = np.random.default_rng(seed)
    q = np.zeros((ROWS * COLS, 4))
    returns, falls, lengths = [], [], []
    for _ in range(episodes):
        state = START
        action = choose(q[state], rng, epsilon)
        total, dropped = 0., 0
        for step in range(600):
            nxt, reward, done = transition(state, action)
            next_action = choose(q[nxt], rng, epsilon)
            future = q[nxt].max() if method == 'Q-learning' else q[nxt, next_action]
            target = reward if done else reward + gamma * future
            q[state, action] += alpha * (target - q[state, action])
            total += reward
            dropped += int(reward == -100)
            state, action = nxt, next_action
            if done:
                break
        returns.append(total); falls.append(dropped); lengths.append(step + 1)
    return q, np.array(returns), np.array(falls), np.array(lengths)


def greedy_route(q):
    state, path, total = START, [START], 0.
    for _ in range(100):
        state, reward, done = transition(state, int(q[state].argmax()))
        path.append(state); total += reward
        if done:
            return path, total, True
    return path, total, False


def bandit(method, seed, steps=400):
    means = np.array([.2, .5, .8, 1.])
    rng = np.random.default_rng(seed)
    q, counts = np.zeros(4), np.zeros(4, dtype=int)
    gaps = []
    for t in range(steps):
        if method == 'UCB':
            action = t if t < 4 else int(np.argmax(q + np.sqrt(2*np.log(t+1)/counts)))
        else:
            action = choose(q, rng, .1 if method == 'epsilon' else 0.)
        reward = means[action] + rng.normal(0, 1)
        counts[action] += 1
        q[action] += (reward - q[action]) / counts[action]
        gaps.append(means.max()-means[action])
    return np.cumsum(gaps), counts


def configure(language):
    plt.rcParams.update({'font.family':'sans-serif', 'font.sans-serif':['Microsoft YaHei','Arial'],
                         'font.size':11, 'axes.spines.top':False, 'axes.spines.right':False,
                         'svg.fonttype':'none', 'pdf.fonttype':42, 'axes.unicode_minus':False,
                         'figure.facecolor':'white', 'axes.facecolor':'white'})


def loop_figure(out, zh):
    fig, ax = plt.subplots(figsize=(11, 4.5)); ax.set(xlim=(0,11), ylim=(0,4.5)); ax.axis('off')
    boxes=[(1,2.0,3,1.2,'学习者：选择动作\n策略与价值估计' if zh else 'Agent: choose action\nPolicy and value estimates',BLUE),
           (7,2.0,3,1.2,'环境：回应动作\n位置变化与奖励' if zh else 'Environment: respond\nNew position and reward',RED)]
    for x,y,w,h,label,color in boxes:
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.12',facecolor=color,edgecolor='none'))
        ax.text(x+w/2,y+h/2,label,color='white',ha='center',va='center',fontsize=13,linespacing=1.6)
    ax.add_patch(FancyArrowPatch((4.2,2.9),(6.8,2.9),arrowstyle='-|>',mutation_scale=18,color=BLUE,lw=2))
    ax.add_patch(FancyArrowPatch((6.8,2.25),(4.2,2.25),arrowstyle='-|>',mutation_scale=18,color=RED,lw=2))
    ax.text(5.5,3.18,'动作 a(t)' if zh else 'Action a(t)',ha='center')
    ax.text(5.5,1.8,'奖励 r(t+1)，状态 s(t+1)' if zh else 'Reward r(t+1), state s(t+1)',ha='center')
    for x,year,text in [(1.1,'规划 / Planning','已知转移，计算价值' if zh else 'Known transitions → values'),(4.3,'1988 · TD','由下一次预测更新' if zh else 'Learn from the next prediction'),(7.5,'1992 · Q-learning','由经验改进动作价值' if zh else 'Improve action values from experience')]:
        ax.text(x,.9,year,color=BLUE,fontweight='bold');ax.text(x,.42,text,fontsize=10)
    fig.tight_layout();fig.savefig(out/f'loop-{lang(zh)}.svg');fig.savefig(out/f'loop-{lang(zh)}.png',dpi=150);plt.close(fig)


def lang(zh):
    return 'zh' if zh else 'en'


def make_figures(out, zh, runs, routes, bandits):
    fig, axes = plt.subplots(1,2,figsize=(11,4.4),gridspec_kw={'width_ratios':[1.45,1]})
    for method,color,label in [('greedy',GOLD,'贪心' if zh else 'Greedy'),('epsilon',RED,'ε=0.1'),('UCB',BLUE,'UCB')]:
        regrets=np.stack([x[0] for x in bandits[method]])
        axes[0].plot(np.arange(1,401),regrets.mean(0),color=color,label=label,lw=2)
        lo,hi=np.quantile(regrets,[.25,.75],axis=0);axes[0].fill_between(np.arange(1,401),lo,hi,color=color,alpha=.12)
        x={'greedy':0,'epsilon':1,'UCB':2}[method]
        axes[1].scatter(np.full(len(regrets),x)+np.linspace(-.12,.12,len(regrets)),regrets[:,-1],c=color,alpha=.65,s=24)
    axes[0].set(xlabel='选择次数' if zh else 'Number of choices',ylabel='累计伪遗憾（奖励单位）' if zh else 'Cumulative pseudo-regret (reward units)');axes[0].legend(frameon=False)
    axes[1].set(xticks=[0,1,2],xticklabels=['贪心' if zh else 'Greedy','ε=0.1','UCB'],ylabel='第400步的累计伪遗憾' if zh else 'Pseudo-regret after 400 choices')
    fig.tight_layout();fig.savefig(out/f'bandits-{lang(zh)}.svg');fig.savefig(out/f'bandits-{lang(zh)}.png',dpi=150);plt.close(fig)
    fig=plt.figure(figsize=(12,7.4));gs=fig.add_gridspec(2,2,height_ratios=[1,1.4],hspace=.5,wspace=.3)
    for j,(method,color) in enumerate([('Q-learning',BLUE),('SARSA',RED)]):
        ax=fig.add_subplot(gs[0,j]);ax.set(xlim=(-.5,11.5),ylim=(3.5,-.5),aspect='equal',xticks=range(12),yticks=range(4))
        for row in range(4):
            for col in range(12):
                face='#efc9c7' if row==3 and 0<col<11 else '#f1f4f5'
                ax.add_patch(Rectangle((col-.48,row-.48),.96,.96,facecolor=face,edgecolor='white'))
        path=routes[method][0];pos=np.array([divmod(s,12) for s in path]);ax.plot(pos[:,1],pos[:,0],color=color,lw=2.3,marker='o',ms=3)
        ax.text(0,3,'S',ha='center',va='center',fontweight='bold');ax.text(11,3,'G',ha='center',va='center',fontweight='bold')
        ax.set_title(method+' · '+('种子0的贪心路径' if zh else 'greedy route, seed 0'));ax.set_xlabel('列' if zh else 'Column');ax.set_ylabel('行' if zh else 'Row')
    ax=fig.add_subplot(gs[1,0]);bx=fig.add_subplot(gs[1,1])
    for j,(method,color) in enumerate([('Q-learning',BLUE),('SARSA',RED)]):
        returns=np.stack([x[1] for x in runs[method]])
        blocks=returns.reshape(len(returns),25,20).mean(2)
        lo,hi=np.quantile(blocks,[.25,.75],axis=0)
        ax.plot(np.arange(20,501,20),blocks.mean(0),color=color,lw=2,label=method)
        ax.fill_between(np.arange(20,501,20),lo,hi,color=color,alpha=.15)
        scores=returns[:,-100:].mean(1);bx.scatter(j+np.linspace(-.12,.12,len(scores)),scores,c=color,s=35)
        bx.plot([j-.2,j+.2],[scores.mean()]*2,color=color,lw=2)
    ax.set(xlabel='训练回合（20回合分组）' if zh else 'Training episode (20-episode blocks)',ylabel='平均未折扣回报' if zh else 'Mean undiscounted return');ax.legend(frameon=False)
    bx.set(xticks=[0,1],xticklabels=['Q-learning','SARSA'],ylabel='末100回合平均回报' if zh else 'Mean return, last 100 episodes')
    fig.savefig(out/f'cliff-{lang(zh)}.svg',bbox_inches='tight');fig.savefig(out/f'cliff-{lang(zh)}.png',dpi=150,bbox_inches='tight');plt.close(fig)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args()
    args.output.mkdir(parents=True,exist_ok=True);zh=args.language=='zh';configure(args.language)
    assert transition(START,1)==(START,-100.,False)
    assert transition(35,2)==(GOAL,-1.,True)
    assert abs(2+.2*(1+.9*4-2)-2.52)<1e-12
    runs={m:[learn(m,s) for s in range(8)] for m in ['Q-learning','SARSA']}
    routes={m:greedy_route(runs[m][0][0]) for m in runs}
    bandits={m:[bandit(m,s) for s in range(32)] for m in ['greedy','epsilon','UCB']}
    summary={'seeds':list(range(8)),'episodes':500,'epsilon':.1,'alpha':.5,'gamma':1.,'max_steps':600,'hand_update':2.52,'algorithms':{}}
    for m,results in runs.items():
        summary['algorithms'][m]={'last100_mean_return':float(np.mean([r[1][-100:].mean() for r in results])),
          'last100_falls_per_episode':float(np.mean([r[2][-100:].mean() for r in results])),
          'greedy_seed0_return':routes[m][1],'greedy_seed0_reached_goal':routes[m][2],'greedy_seed0_steps':len(routes[m][0])-1,
          'capped_episodes':int(sum((r[3]==600).sum() for r in results))}
        np.savez(args.output/f'{m.replace("-","")}-data.npz',returns=np.stack([r[1] for r in results]),q=np.stack([r[0] for r in results]),falls=np.stack([r[2] for r in results]))
    summary['bandit_final_pseudoregret']={m:float(np.mean([r[0][-1] for r in xs])) for m,xs in bandits.items()}
    loop_figure(args.output,zh);make_figures(args.output,zh,runs,routes,bandits)
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

The upper panels show greedy routes after training for seed 0: Q-learning reaches the goal in 13 steps and SARSA in 17. The lower-left panel groups training returns into blocks of 20 episodes. Lines average over eight seeds, and shaded bands show the interquartile range across seeds. In the lower-right panel, every seed contributes one point representing its mean return over the final 100 episodes; horizontal marks show the corresponding means. For this setup those final-window means are approximately −49.66 for Q-learning and −27.06 for SARSA. Mean falls per episode are approximately 0.330 and 0.045. A shorter greedy route and a worse exploratory training return can coexist because the policies being evaluated differ.

![Top: greedy routes after training for seed 0. Bottom: training returns with persistent ε=0.1 exploration. Each algorithm uses 8 seeds and 500 episodes. Shading is the interquartile range; lower-right points average each seed’s last 100 episodes. Routes and training curves evaluate different policies.](https://ml-biomat.com/static/tutorials/machine-learning/figures/6b8facbc370b07224edad654.svg?v=6b8facbc370b)

Figure 3Top: greedy routes after training for seed 0. Bottom: training returns with persistent ε=0.1 exploration. Each algorithm uses 8 seeds and 500 episodes. Shading is the interquartile range; lower-right points average each seed’s last 100 episodes. Routes and training curves evaluate different policies.

Each algorithm reaches the 600-step cap once among its 4,000 training episodes, and the program records that count. Returns include the rewards actually collected, with final comparisons using the same episode window. Sample-efficiency comparisons should additionally plot performance against environment interactions: different policies can require different numbers of steps to finish an episode. Changing ε to zero before retraining changes which data are collected. Switching only the final evaluation policy to greedy preserves the training data while changing execution. Comparing these two modifications is a useful way to check your understanding of behaviour policies, learning targets and evaluation policies.

## Experimental habits that transfer beyond the grid

Reward design defines what the agent works to optimise. If a robot is rewarded for every metre of progress towards a target, check whether moving back and forth can collect the reward repeatedly. If elapsed time is penalised but collisions are absent from the objective, the fastest route may differ from the intended route. Dense rewards can accelerate learning and can also change the task's preferences. Potential-based shaping provides a construction that can preserve policy ordering under suitable conditions: assign a potential to each state and add the discounted next-state potential minus the current-state potential as extra reward. Along a trajectory, intermediate terms cancel. The discounting and terminal-state conventions must match the construction for that reasoning to apply.

The unit of evaluation should match the experiment. One bandit run contains 400 decisions; one grid-world training run contains 500 episodes. Seeds represent repeated random action-selection processes. Treating 500 consecutive episodes from a single learning trajectory as 500 independent experiments would ignore their dependence through the evolving value table. Fix the environment, training budget, evaluation procedure and tuning rule, then report variability across independent runs. Episodes used to choose hyperparameters should be separated from those used for final evaluation. For a physical system, establish the observation, action and reward definitions in inspectable simulation and available data before expanding the scale of interaction.

A small paper-and-pencil experiment can bring the methods together. Draw three states on a route to a terminal goal, assign reward 10 to the final transition and zero to the first two, and initialize all values to zero. Monte Carlo waits until the entire route has been observed and can then assign the discounted observed return to every visited state. One-step TD first changes the state nearest the goal; later visits carry that new information back towards the start through bootstrapped targets. With a known transition model, synchronous value iteration also propagates the reward through a finite number of predecessor states per sweep. Put these three updates next to one another and ask three separate questions: has the trajectory finished, does the target contain a current prediction, and is a complete transition model available? Keeping these questions distinct helps explain why a method can be model-free yet still bootstrap, or use a model without collecting a new trajectory for every update.

You can now describe a sequential decision problem in terms of states, actions, rewards and transitions, explain why values admit a recursion, and calculate a TD, SARSA or Q-learning update by hand. More importantly, a path diagram and a return distribution can tell you which policy an algorithm is evaluating and what it has learned to optimise. Deep reinforcement learning replaces tables with neural networks and adds tools such as replay, target networks and policy gradients. The habits established here remain useful: define the task clearly, work through its target, and connect every training curve to the experience that produced it.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M24.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Dive into Deep Learning — Q-Learning](https://d2l.ai/chapter_reinforcement-learning/qlearning.html)

   Exploration, action values and a tabular implementation.

   CC BY-SA 4.0 (book text and original figures)
2. [Gymnasium — Cliff Walking](https://gymnasium.farama.org/environments/toy_text/cliff_walking/)

   Grid positions, actions, rewards and termination rules for cliff walking.
3. [Sutton (1988), Learning to predict by the methods of temporal differences](https://link.springer.com/article/10.1007/BF00115009)

   Learning from differences between temporally adjacent predictions.

   Original paper reference
4. [Watkins and Dayan (1992), Q-learning](https://link.springer.com/article/10.1007/BF00992698)

   Tabular convergence conditions and the connection to dynamic programming.

   Original paper reference
