# From Action Values to Policy Updates: Deep Reinforcement Learning

Source: https://ml-biomat.com/tutorials/machine-learning/m37/en/
Language: en

Run DQN and PPO in one stochastic corridor, then connect replay, advantages, clipping, and continuous control.

## 1. When the state space no longer fits in a table

A delivery vehicle chooses a direction, a thermostat changes power, and a game character selects its next move. Each decision affects what happens afterward. Tabular reinforcement learning stores a value for each state–action pair, but camera images, joint angles, and sensor histories make exhaustive tables impractical. Deep reinforcement learning uses a neural network to map observations to values or action distributions, sharing computation across similar situations. That sharing also couples predictions: correcting one state can change others. Training data, target values, and update size consequently need to be designed together.

Our environment is a seven-position corridor. A courier starts uniformly at positions one through five, with its target chosen uniformly between endpoints zero and six. Reaching the other endpoint is failure. It commands left or right, but the environment reverses the action with probability 0.1, and an episode lasts at most twenty steps. Goal arrival earns one, wrong-endpoint arrival earns minus one, and ordinary movement earns minus 0.02. Position, goal, and remaining time answer where the agent is, where it should go, and how much time remains. Known transition rules also permit exact baseline calculations.

Value learning estimates future returns and selects actions from those estimates. Policy learning directly outputs action probabilities and adjusts them from experience. Actor–Critic combines an actor with an evaluator. OpenAI’s 2018 teaching diagram locates these choices, while its tree structure cannot express every combination: PPO also has a value network, SAC combines a stochastic policy with off-policy data, and model-based methods can join planning and policy training. Understanding what each component learns and where its data comes from is more useful than remembering a single branch label.

![Historical teaching taxonomy of reinforcement-learning methods](https://ml-biomat.com/static/tutorials/machine-learning/figures/5644a5526a9b2735bbec0000.svg?v=5644a5526a9b)

Figure 1OpenAI, Spinning Up, 2018 teaching taxonomy, reproduced unchanged. Read it by learned policy, value, or model; the chapter explains combinations across branches. Source: https://spinningup.openai.com/en/latest/spinningup/rl_intro2.html; MIT: https://raw.githubusercontent.com/openai/spinningup/master/LICENSE.

## 2. DQN learns a value for each discrete action

A DQN receives a state representation and outputs one value per discrete action. Here ten inputs produce left and right values, and the larger value determines a greedy choice. Mnih and colleagues’ 2013 Atari work connected visual representation learning with Q-learning, using images to estimate future rewards. Our small fully connected network exposes target construction and data organization without an image encoder. An observed reward plus an estimated continuation value supplies the target for the action actually taken. The network then adjusts its prediction toward that target rather than learning from a manually supplied optimal-action label.

$$
y_i=r_i+\gamma(1-d_i)\max_{a'}Q_{\bar\theta}(s'_i,a'),\quad\mathcal L=\frac1B\sum_{i=1}^{B}\ell(Q_\theta(s_i,a_i)-y_i),\quad\ell(e)=\begin{cases}e^2/2&|e|\le1\\|e|-1/2&|e|>1\end{cases}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/91ddd31201411affadf62bd0.svg) | State, executed action, reward, next state, and termination flag for transition i. d is 0 or 1; rewards are dimensionless task scores. |
| ![Formula](https://ml-biomat.com/static/agent-math/0d9eb9fa4d1c85e9b3562044.svg) | Minibatch size, sample index, and candidate next action. |
| ![Formula](https://ml-biomat.com/static/agent-math/25466d762a2d1f840409be64.svg) | Online and target-network parameters; target computation stops gradients. |
| ![Formula](https://ml-biomat.com/static/agent-math/4be111afe7c23428ae5024a8.svg) | Action value; the example maps 10 inputs to 2 outputs and selects a scalar by action, on the return scale. |
| ![Formula](https://ml-biomat.com/static/agent-math/05fe78b5b68e2122cf068260.svg) | Discount and target value; code gamma=0.97, with targets on the return scale. |
| ![Formula](https://ml-biomat.com/static/agent-math/b50fd96b3413648e1f224a9f.svg) | Mean regression loss, Huber-style loss with threshold 1, and prediction-minus-target error; all task quantities here are dimensionless. |

The target adds immediate reward and continuation value if the task has not ended, while regression selects the recorded action output. Reward 1, gamma 0.9, next maximum 2, and nontermination give target 2.8. Prediction 2 yields error−0.8 and loss 0.32. True termination instead gives target 1. The piecewise loss is quadratic near zero and has bounded slope magnitude for large errors.

If a rapidly changing network produces both a prediction and its target, optimization chases a moving reference. A target network stores slower-changing parameters and computes targets without gradient tracking; this example copies online parameters every 128 environment steps. Replay stores state, action, reward, next state, and genuine termination, then samples transitions to reduce strong temporal correlations and reuse costly experience. These mechanisms address different problems: the target network slows reference drift, while replay reorganizes training samples. The program uses a Huber-style regression loss and gradient clipping to control large numerical updates.

Replay actions may come from an earlier exploratory policy, while the Q-learning target evaluates a maximum at the next state. This is off-policy learning. Recorded actions need not all be optimal under the current policy, but the data still needs useful coverage of states and actions. A tiny buffer can forget important experience, whereas very old data can mismatch a changing environment. Prioritized replay samples high-error transitions more often and changes the sampling distribution, requiring appropriate importance weighting and coverage checks. Uniform replay provides a transparent baseline for understanding these later extensions.

Termination determines whether a continuation value remains. The twenty-step deadline here belongs to the task itself, and remaining time is observed, so reaching the deadline is genuine termination with zero future value. A collection process that merely cuts an otherwise continuing trajectory should instead bootstrap from its last state. PPO’s thirty-two-step sampling window can contain several complete episodes and end partway through another. Recording each transition’s next-state value and terminal mask distinguishes these cases. Using a reset observation as the continuation of a terminated episode would connect two unrelated trajectories.

## 3. Double and Dueling change different components

Taking the maximum of noisy estimates tends to select positive errors as well as high values. Suppose every action has true value zero and receives independent zero-mean estimation noise. Each estimate averages to zero, but their maximum averages above zero, with more candidates creating more opportunities for an accidental high value. Double DQN separates action selection from evaluation: the online network chooses an action and the target network evaluates that action. The networks are not independent, so the effect depends on their error correlation. This separation addresses selection bias rather than making every value estimate exact.

$$
a^*=\arg\max_a Q_\theta(s',a),\qquad y_{\rm Double}=r+\gamma(1-d)Q_{\bar\theta}(s',a^*)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/65d5791718d5cb558a50141f.svg) | Next state, candidate action, and action selected by the online network. |
| ![Formula](https://ml-biomat.com/static/agent-math/6141b2d51d1b502b926964cf.svg) | Online and target action-value networks and their parameters; each selected output is a scalar. |
| ![Formula](https://ml-biomat.com/static/agent-math/57afd3dd2741fa5223bfcb35.svg) | Current reward, discount, genuine termination flag, and Double target; rewards and targets share the dimensionless task scale. |

The online network selects while the target network evaluates. Online outputs(4,3)choose the first action; target outputs(2,5)evaluate it as 2. Reward 1 and gamma 0.9 give Double target 2.8, whereas ordinary DQN takes the target maximum 5 and obtains 5.5. The target network’s preference for the other action does not change the selected action in this update.

The figure isolates this statistical effect using 50000 noise experiments. The mean maximum is about 0.568 for two actions and 1.865 for twenty actions. Evaluating the selected action with an independent second set of noise yields means close to zero. Independence is an explicit assumption of this mechanism experiment. Real Double DQN networks share training history, so their effects should be measured through value errors and environment returns. The 2015 Double DQN work extended this separation from tabular estimation to deep action-value networks, providing a concrete response to overestimation observed in the earlier approach.

Dueling instead changes the output representation. One branch estimates how favorable a state is overall; another estimates differences between its actions. A vehicle already on an open road can have a good outlook even when several small steering choices have similar consequences. Sharing a state-value estimate can avoid relearning that common component separately for every action. Subtracting the mean advantage defines a consistent decomposition. Dueling and Double DQN can be combined because one changes how values are represented and the other changes how the learning target selects and evaluates an action.

$$
Q(s,a)=V(s)+A(s,a)-\frac1m\sum_{j=1}^{m}A(s,a_j)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/09e33249fb2a44b3a16b695b.svg) | State, queried action, and discrete action j. |
| ![Formula](https://ml-biomat.com/static/agent-math/5f441d5a733f02391d4cb1a7.svg) | Scalar state-branch output on the return scale. |
| ![Formula](https://ml-biomat.com/static/agent-math/07378df13b4f41d9096644ef.svg) | Advantage-branch output for action a; the complete branch has m values on the return scale. |
| ![Formula](https://ml-biomat.com/static/agent-math/5d562bcaafa96061616f6969.svg) | Action count, action index, and combined action value; m=2 in the example, with dimensionless task quantities. |

Subtracting the action mean makes the advantage branch express relative differences, with V representing the mean combined value. V=2 and advantages(−1,1)produce Q=(1,3). Adding 5 to both advantages gives(4,6), whose increased mean cancels the shift and leaves Q unchanged. This fixes a constant-shift ambiguity without changing greedy selection.

## 4. REINFORCE adjusts action probabilities directly

A policy network can produce a distribution without first estimating an action value. Two logits become normalized left/right probabilities through softmax, and an action is sampled. Experience then changes the probability of sampled actions according to their returns. REINFORCE makes this computable by weighting the gradient of an action’s log probability by a return. The environment itself need not be differentiable: a road disturbance or a game engine can be treated as an external process from which transitions and rewards are sampled. Gradients pass through the policy’s probability calculation rather than through the physical action outcome.

$$
\nabla_\theta J=\mathbb E_{\tau\sim\pi_\theta}\!\left[\sum_{t=0}^{T-1}\nabla_\theta\log\pi_\theta(a_t\mid s_t)\big(G_t-b(s_t)\big)\right],\qquad G_t=\sum_{k=t}^{T-1}r_k
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a8f5ed8b1adff646d1cbe95e.svg) | Policy parameters, finite-episode undiscounted expected return, and parameter gradient; returns use dimensionless task scores. |
| ![Formula](https://ml-biomat.com/static/agent-math/d530b1794a9754a597787ed8.svg) | Policy action probability, complete trajectory sampled under the current policy, and expectation. |
| ![Formula](https://ml-biomat.com/static/agent-math/7ea051e99f790acbb94bb2ce.svg) | Current index, later index, episode length, state, action, and reward at step k. |
| ![Formula](https://ml-biomat.com/static/agent-math/d5033980c206f50bdff43e45.svg) | Undiscounted return from the current step and a state-only baseline, with shared scale and treated as fixed weights for the actor update. |
| ![Formula](https://ml-biomat.com/static/agent-math/5c6218d94f5cfc1cfe45060d.svg) | Natural logarithm of dimensionless action probability. |

Environment transitions in trajectory probability do not depend on policy parameters, and logs turn policy-probability products into sums. Past rewards have zero expected contribution for the current sampled action, leaving reward-to-go. This expression uses an undiscounted finite episode; GAE below has an explicit discount. For a binary right-action probability 0.25 parameterized by one logit, sampling right gives log-probability derivative 0.75. Advantage 2 supplies an ascent signal 1.5.

Returns are noisy. A sensible direction can be reversed by the environment, while an unhelpful command can succeed by chance. A baseline estimates the return usually expected from the current state, turning an observed return into a relative signal. A baseline depending on state but not on the sampled action has zero expected policy-gradient contribution: action probabilities sum to one, and the derivative of that sum is zero. This allows variance reduction while preserving the expected gradient under the stated assumptions. A learned state-value function is a common baseline, with a simple average serving as an introductory comparison.

If a state normally returns three, an observed return of five gives a positive-two signal and a return of one gives negative two. Both raw returns are positive, yet the second experience can appropriately reduce the sampled action’s probability. During the actor update, returns or advantages act as fixed weights with gradients stopped through them. Otherwise optimization also pushes on the evaluator to alter the weighting signal. The PPO implementation keeps this separation: collected values produce detached advantages, while a separate value loss trains the critic. Shared network features make the distinction in the objective especially useful.

## 5. Actor–Critic and GAE connect immediate feedback to later rewards

The actor outputs an action distribution and the critic estimates state value. They can have separate networks or share a feature extractor with distinct heads. Here two shared 32-dimensional hidden layers feed two policy logits and one scalar value. The critic learns from experience-based targets, and the actor uses relative-value signals. A2C commonly gathers short trajectories from several environments synchronously and combines them for an update. Synchronization describes how collection and parameter updates are organized; it does not imply that the environments visit identical states or produce identical rewards.

Waiting for a complete episode uses realized rewards but may delay updates and produce variable targets. A one-step temporal-difference error arrives quickly but depends more strongly on the current value estimate. Generalized advantage estimation accumulates a sequence of TD errors with geometric weights. Lambda controls how far the signal propagates: smaller values emphasize nearby errors, while larger values carry distant feedback farther backward. The 2015 GAE work connected this estimator to policy optimization, using the critic to reduce gradient noise rather than treating value prediction as an unrelated diagnostic output.

$$
\delta_t=r_t+\gamma(1-d_t)V(s_{t+1})-V(s_t),\qquad\hat A_t=\delta_t+\gamma\lambda(1-d_t)\hat A_{t+1},\qquad\hat A_T=0
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f9815edca06dc233accaf513.svg) | Transition index and rollout-window length; recursion proceeds from T−1 to 0. |
| ![Formula](https://ml-biomat.com/static/agent-math/053bcaf18fe5f8c8317c15a6.svg) | Current/next state, reward, and genuine terminal flag, with one indicating termination. |
| ![Formula](https://ml-biomat.com/static/agent-math/5a9105ba2001ee110accdf47.svg) | Collected state value, TD residual, and GAE advantage, all on the return scale. |
| ![Formula](https://ml-biomat.com/static/agent-math/2b94ab8bc94736dd0f6657df.svg) | Discount and advantage-propagation coefficient, usually 0 to 1; code values 0.97 and 0.95. |

A TD residual compares reward plus continuation value with the current estimate, then the next advantage propagates backward with a geometric discount. Rewards(0,0,1), values(0.2,0.3,0.4), final termination, gamma 0.9 and lambda 0.8 give residuals(0.07,0.06,0.6)and advantages(0.42424,0.492,0.6). A zero advantage beyond the rollout does not imply zero final state value: the last residual still bootstraps if not terminal. The terminal flag cuts both terms when appropriate.

The three-step example has rewards zero, zero, one and state values 0.2,0.3,0.4, followed by genuine termination. With discount 0.9 and lambda 0.8, the TD errors are 0.07,0.06,0.6. Backward accumulation produces advantages 0.6,0.492,0.42424 in reverse temporal order. The terminal reward reaches earlier actions while value estimates supply local corrections. The code adds advantages to the old values to form value-regression targets. For the policy objective, it normalizes advantages using the mean and standard deviation of the complete collected batch before splitting that batch into minibatches.

Normalization improves numerical scale but changes relative weighting in a finite sample, so the convention should be recorded. Normalizing separately in tiny minibatches can differ from normalizing the complete rollout. Trajectory boundaries matter just as much: a true terminal state cuts off later advantages, preventing rewards after reset from entering the previous episode. A rollout ending during a continuing episode uses a bootstrap value. Drawing these positions along a timeline often reveals implementation mistakes more quickly than memorizing the GAE expression alone. The program retains explicit arrays for rewards, values, next values, and terminal masks.

## 6. PPO limits the reward for changing probabilities too far

Advantages collected under an old policy describe experience near that policy. Repeated large updates on the same batch can move the model into behavior poorly represented by those samples. TRPO constrains an average KL distance between old and new policies and solves a locally approximated optimization problem. PPO offers first-order alternatives. In the 2017 PPO-Clip formulation, a new-to-old action-probability ratio enters a surrogate objective that removes incentives for excessive movement in a favorable direction. This supports several minibatch optimization passes over a recently collected batch rather than a single update followed immediately by new sampling.

$$
\rho_i(\theta)=\frac{\pi_\theta(a_i\mid s_i)}{\pi_{\rm old}(a_i\mid s_i)},\qquad L_{\rm clip}=\frac1B\sum_{i=1}^{B}\min\!\left(\rho_i\hat A_i,\operatorname{clip}(\rho_i,1-\epsilon,1+\epsilon)\hat A_i\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8bd9750df1a9d94604e32c16.svg) | Sample index, batch size, sampled state, and executed action. |
| ![Formula](https://ml-biomat.com/static/agent-math/fa5000290880458fe08d11fc.svg) | Current policy, fixed policy used to collect data, and current parameters; both probabilities refer to the same sampled action. |
| ![Formula](https://ml-biomat.com/static/agent-math/b7986769e3dcf2f5576a7fd9.svg) | Dimensionless new/old probability ratio and clipping width; code epsilon=0.2. |
| ![Formula](https://ml-biomat.com/static/agent-math/9f0b4490f9c43d63aee296ca.svg) | Fixed advantage estimate, dimensionless after whole-rollout normalization in the code. |
| ![Formula](https://ml-biomat.com/static/agent-math/d9944c7c9378cf7deef406a6.svg) | Surrogate to maximize, interval clipping, and minimum of two terms; the code minimizes the negative objective. |

The ratio measures how the sampled action probability changed. Advantage 2, ratio 1.5, and epsilon 0.2 give min(3,2.4)=2.4. Advantage−2 and ratio 0.5 give min(−1,−1.6)=−1.6. A positive advantage below the lower boundary still penalizes reducing probability, and a negative advantage above the upper boundary still penalizes worsening behavior. Simply clipping the ratio before multiplying would lose this distinction. The objective limits an incentive, not all network outputs.

Consider advantage positive two, old action probability 0.4, and new probability 0.6. The ratio is 1.5. With clipping width 0.2, the unclipped contribution is three while the clipped contribution is 2.4; the objective takes the smaller value and no longer rewards increasing this sampled probability further. For advantage negative two and ratio 0.5, it takes−1.6 rather than−1, limiting the extra benefit of reducing an unfavorable action too far. The positive and negative cases flatten on different sides. The interactive plot shows both curves and the actual selected contribution for editable probabilities and advantages.

Clipping operates on the objective, not as a hard constraint forcing every network probability ratio into the interval. Shared parameters also change other states and actions, so KL estimates, clip fraction, policy entropy, and evaluation return remain useful diagnostics. Excessive KL can trigger early stopping of batch updates; rapidly falling entropy indicates increasingly concentrated action choices. The example records the sampled mean of old log probability minus new log probability as a finite-sample KL estimate. It can be slightly negative because of sampling and should not be interpreted as an exact nonnegative distributional divergence.

PPO mainly updates from trajectories collected under the recent policy. Saving old probabilities for four passes over one batch differs from repeatedly sampling an arbitrarily old replay buffer. Each collection round here gathers 32 steps from 16 environments, totaling 512 transitions, then fixes old log probabilities and advantages. Four optimization epochs use minibatches of 128. The next collection round uses the updated policy. Distinguishing environment samples, optimization steps, and data reuse makes training budgets interpretable. A single word such as epoch can otherwise hide several different quantities.

## Lab: which incentive does PPO remove?

Set old and new probabilities for one action, its advantage, and clipping width. Both advantage signs are plotted, with a dot on the selected sample; the other action’s probability completes the distribution. Reduce a positive-advantage probability or increase a negative-advantage probability to inspect why the objective still worsens.

[Figure: PPO positive and negative advantage curves, selected sample and clipped contribution](https://ml-biomat.com/tutorials/machine-learning/m37/en/#M37-svg)

The vertical scale adjusts with labeled values. This is one sample’s surrogate contribution; a network update also affects other actions and states. A flat segment does not imply that the entire network gradient is zero.

## 7. Continuous actions require DDPG, TD3, or SAC-style choices

Two directions permit direct comparison of two Q-values. A joint torque or valve opening varies continuously and cannot be enumerated as one output per possible value. DDPG uses an actor to propose a continuous action and a critic to evaluate it. Differentiating the critic with respect to its action input gives a direction for improving the actor. Replay and target networks remain, while behavior commonly adds exploration noise to the actor output. Actions must be scaled to their physical bounds, distinguishing normalized network coordinates from torque, velocity, or power units supplied to the environment.

$$
\nabla_\theta J_\mu\approx\mathbb E_{s\sim\mathcal D}\left[\left.\nabla_a Q_\phi(s,a)\right|_{a=\mu_\theta(s)}\nabla_\theta\mu_\theta(s)\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a22dfd6872fc5c2e8a1f6913.svg) | State and replay-state sampling distribution. |
| ![Formula](https://ml-biomat.com/static/agent-math/bab5907dbf1b11459409f0e7.svg) | Deterministic actor and parameters; output is an m-dimensional continuous action. |
| ![Formula](https://ml-biomat.com/static/agent-math/e46ee6754305e295e1862db5.svg) | Critic and parameters; inputs are a state and m-dimensional action, output a scalar value. |
| ![Formula](https://ml-biomat.com/static/agent-math/cb0c8a1ff671b47f0377effc.svg) | Action gradient of value, actor parameter Jacobian, and actor objective; their product gives a parameter-update direction. |

The chain rule connects how an action changes value to how parameters change the action. At a fixed state, let Q(a)=−(a−0.5)² and actor output equal theta. At theta 0 the action derivative is 1; an ascent step 0.1 moves the action to 0.1 and value from−0.25 to−0.16. These action coordinates are dimensionless; physical actions require a recorded normalization. Freeze critic parameters during actor optimization while retaining derivatives through its action input.

A critic can mistakenly create a sharp value peak at an action that is not actually useful. The actor then learns to exploit that error. TD3 addresses this through three mechanisms: the smaller of two critic estimates enters the target; clipped noise smooths the target action within legal bounds; and actor and target updates occur less frequently than critic updates. These address estimation bias, local action sensitivity, and update timing respectively. They can be studied through separate ablations rather than treated as an indivisible algorithm name. The target-smoothing noise is part of learning, not simply extra randomness added during deployment.

SAC learns a stochastic policy and includes entropy in its objective. Higher entropy retains more action choices, and a temperature coefficient balances that diversity against environment return. Some implementations adjust temperature to meet a target entropy. SAC also uses replay and twin critics, with next-action log probability entering a soft-value target. Its relationship to TD3 includes continuous-action value learning and replay, while stochastic policy optimization and the entropy objective change the update. The resulting exploration behavior is tied to the learned distribution rather than only to an external noise schedule.

$$
y_{\rm SAC}=r+\gamma(1-d)\left[\min_{j=1,2}Q_{\bar\phi_j}(s',a')-\alpha\log\pi_\theta(a'\mid s')\right],\quad a'\sim\pi_\theta(\cdot\mid s'),\qquad\mathcal L_\pi=\mathbb E\left[\alpha\log\pi_\theta(a\mid s)-\min_jQ_{\phi_j}(s,a)\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/44beed4c16cc97bd1f78b2ae.svg) | Reward, discount, genuine terminal flag, current/next state, and associated policy-sampled actions. |
| ![Formula](https://ml-biomat.com/static/agent-math/6e7af4ff6d55320bb687c795.svg) | Two current critics and target copies, j=1 or 2; values share the return scale. |
| ![Formula](https://ml-biomat.com/static/agent-math/a14a05c17a6f753c12e01c4a.svg) | Stochastic policy and parameters; continuous actions use probability density in normalized action coordinates. |
| ![Formula](https://ml-biomat.com/static/agent-math/a95c2d3c3aa75e4332e4f3fd.svg) | Positive temperature, soft-value target, and policy loss to minimize; alpha places the log-probability term on the reward scale. |
| ![Formula](https://ml-biomat.com/static/agent-math/f66e75ac05c3b7325c622f41.svg) | Current/target critic parameters and expectation over replay states and policy actions. |

The smaller critic value combines with an entropy term to form a soft continuation value. Reward 1, gamma 0.9, nontermination, target values 2 and 3, alpha 0.2, and next-action log density−0.7 give 1+0.9×(2+0.14)=2.926. Minimizing the actor loss favors value while retaining temperature-controlled distribution breadth. Continuous differential entropy can be negative and depends on action units; tanh transformations require density correction. This is a common twin-Q continuous SAC form; discrete versions modify the action expectation.

A continuous policy often samples a Gaussian variable and applies tanh to obtain bounded actions. This transformation changes the probability density, so log-probability calculations require a Jacobian correction. Using the original Gaussian density after squashing gives the wrong entropy term. Three superficially similar noise sources should therefore be distinguished: DDPG behavior noise collects different actions, TD3 target smoothing modifies learning targets, and SAC policy randomness belongs to the optimized distribution. Evaluation may use a policy mean or retain sampling, but the choice changes the behavior being measured and belongs in the experimental description.

Method choice depends on the action space and data budget. DQN has a straightforward discrete-action maximum. PPO handles discrete or continuous distributions with a direct collection/update workflow. DDPG, TD3, and SAC emphasize replay reuse and continuous-action optimization. High-dimensional actions, sparse rewards, contacts, and limited physical trials change the tradeoffs. The next chapter connects these methods to offline data, learned environment models, classical control, and robotic observations. The actual training comparison here remains the shared discrete corridor; continuous-control mechanisms are developed through explicit equations and action examples.

## 8. Compare learning routes under the same interaction budget

The full experiment trains DQN and PPO with seeds 37,137,237 and 6144 environment steps per run. DQN stores up to 3000 transitions, starts learning after 128 samples, and draws 64 transitions without replacement every four interaction steps. Epsilon decreases from one to 0.05 over the first half of the budget. PPO uses the 16-environment,32-step rollouts and four-pass updates described above. Both have 32-dimensional hidden layers, but their numbers of gradient updates differ. Equal interaction budgets therefore do not imply equal computational cost. All initializations, transition rules, learning rates, and sampling conventions appear in the complete script.

### Complete DQN and PPO experiment in one stochastic corridor

Includes environment, networks, replay, target updates, GAE, PPO clipping, independent evaluation, exact policy recursion, and checkpoint reload.

```
"""DQN and PPO on the same finite-horizon stochastic courier task."""
import argparse,copy,json,math
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.distributions import Categorical
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
torch.set_num_threads(2)
GAMMA=.97;HORIZON=20

class Courier:
 """Position1..5, target0or6; other endpoint is failure; action flips withp=.1."""
 def __init__(self,seed,n=1):self.rng=np.random.default_rng(seed);self.n=n;self.reset(np.arange(n))
 def reset(self,indices):
  if not hasattr(self,'position'):self.position=np.zeros(self.n,dtype=int);self.goal=np.zeros(self.n,dtype=int);self.remaining=np.zeros(self.n,dtype=int)
  self.position[indices]=self.rng.integers(1,6,len(indices));self.goal[indices]=self.rng.integers(0,2,len(indices))*6;self.remaining[indices]=HORIZON
 def observe(self):return np.column_stack([np.eye(7)[self.position],np.eye(2)[self.goal//6],self.remaining/HORIZON]).astype('float32')
 def step(self,actions):
  actual=np.asarray(actions,dtype=int)^(self.rng.random(self.n)<.1);self.position+=2*actual-1;self.remaining-=1
  reached=self.position==self.goal;wrong=(self.position==0)|(self.position==6);done=wrong|(self.remaining==0);reward=np.where(reached,1,np.where(wrong,-1,-.02)).astype('float32');next_observation=self.observe();return next_observation,reward,done,reached

class QNet(nn.Module):
 def __init__(self):super().__init__();self.net=nn.Sequential(nn.Linear(10,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh(),nn.Linear(32,2))
 def forward(self,x):return self.net(x)
class ActorCritic(nn.Module):
 def __init__(self):super().__init__();self.body=nn.Sequential(nn.Linear(10,32),nn.Tanh(),nn.Linear(32,32),nn.Tanh());self.policy=nn.Linear(32,2);self.value=nn.Linear(32,1)
 def forward(self,x):h=self.body(x);return self.policy(h),self.value(h).squeeze(-1)

def evaluate(model,kind,seed=9001,episodes=100):
 returns=[];success=[];lengths=[]
 for episode in range(episodes):
  env=Courier(seed+episode);total=0
  for t in range(HORIZON):
   with torch.no_grad():out=model(torch.from_numpy(env.observe()));logits=out[0]if kind=='PPO'else out;action=logits.argmax(-1).numpy()
   obs,reward,done,reached=env.step(action);total+=float(reward[0])
   if done[0]:break
  returns.append(total);success.append(bool(reached[0]));lengths.append(t+1)
 return {'mean_return':float(np.mean(returns)),'success_rate':float(np.mean(success)),'mean_length':float(np.mean(lengths)),'returns':returns}

def exact_policy_value(toward_goal):
 values=np.zeros((2,7));success=np.zeros((2,7))
 for remaining in range(1,HORIZON+1):
  new=np.zeros_like(values);new_success=np.zeros_like(success)
  for target_index,goal in enumerate([0,6]):
   for position in range(1,6):
    right_probability=(.9 if goal==6 else .1)if toward_goal else .5
    for delta,probability in [(-1,1-right_probability),(1,right_probability)]:
     nxt=position+delta;end=nxt in (0,6);reward=1 if nxt==goal else -1 if end else -.02
     new[target_index,position]+=probability*(reward+(0 if end else values[target_index,nxt]))
     new_success[target_index,position]+=probability*((nxt==goal)+(0 if end else success[target_index,nxt]))
  values,success=new,new_success
 return float(values[:,1:6].mean()),float(success[:,1:6].mean())

def train_dqn(seed,steps=6144):
 torch.manual_seed(seed);rng=np.random.default_rng(seed+1);env=Courier(seed+2);net=QNet();target=copy.deepcopy(net).eval();opt=torch.optim.Adam(net.parameters(),lr=.003);buffer=[];curve=[];losses=[];obs=env.observe()[0]
 for step in range(1,steps+1):
  epsilon=max(.05,1-.95*step/(steps/2))
  with torch.no_grad():action=int(net(torch.from_numpy(obs)).argmax())
  if rng.random()<epsilon:action=int(rng.integers(2))
  nxt,reward,done,reached=env.step([action]);buffer.append((obs.copy(),action,float(reward[0]),nxt[0].copy(),bool(done[0])))
  if len(buffer)>3000:buffer.pop(0)
  obs=nxt[0]
  if done[0]:env.reset(np.array([0]));obs=env.observe()[0]
  if len(buffer)>=128 and step%4==0:
   batch=[buffer[i]for i in rng.choice(len(buffer),64,replace=False)];s,a,r,ns,d=map(np.array,zip(*batch));s=torch.tensor(s);ns=torch.tensor(ns);a=torch.tensor(a);r=torch.tensor(r,dtype=torch.float32);d=torch.tensor(d,dtype=torch.float32)
   with torch.no_grad():y=r+GAMMA*(1-d)*target(ns).max(1).values
   prediction=net(s).gather(1,a[:,None]).squeeze(1);loss=nn.functional.smooth_l1_loss(prediction,y);opt.zero_grad();loss.backward();nn.utils.clip_grad_norm_(net.parameters(),1);opt.step();losses.append(float(loss.detach()))
  if step%128==0:target.load_state_dict(net.state_dict())
  if step%512==0:curve.append([step,evaluate(net,'DQN',9001,100)['mean_return']])
 return net,curve,losses

def gae(rewards,values,next_values,dones,gamma,lam):
 advantages=np.zeros_like(rewards);last=np.zeros(rewards.shape[1],dtype=np.float32)
 for t in range(len(rewards)-1,-1,-1):
  mask=1-dones[t];delta=rewards[t]+gamma*mask*next_values[t]-values[t];last=delta+gamma*lam*mask*last;advantages[t]=last
 return advantages

def train_ppo(seed,steps=6144):
 torch.manual_seed(seed);rng=np.random.default_rng(seed+1);env=Courier(seed+2,16);net=ActorCritic();opt=torch.optim.Adam(net.parameters(),lr=.006);curve=[];diagnostics=[];horizon=32
 for update in range(steps//(16*horizon)):
  storage=[]
  for _ in range(horizon):
   obs=env.observe()
   with torch.no_grad():logits,value=net(torch.from_numpy(obs));dist=Categorical(logits=logits);action=dist.sample();oldlog=dist.log_prob(action)
   nxt,reward,done,reached=env.step(action.numpy())
   with torch.no_grad():nv=net(torch.from_numpy(nxt))[1]
   storage.append((obs,action.numpy(),oldlog.numpy(),value.numpy(),reward,done.astype('float32'),nv.numpy()));env.reset(np.flatnonzero(done))
  obs,act,oldlog,values,rewards,dones,nextvalues=[np.array(x)for x in zip(*storage)];adv=gae(rewards,values,nextvalues,dones,GAMMA,.95);returns=adv+values
  obs=torch.tensor(obs.reshape(-1,10));act=torch.tensor(act.ravel());oldlog=torch.tensor(oldlog.ravel());returns=torch.tensor(returns.ravel());adv=torch.tensor(adv.ravel());adv=(adv-adv.mean())/(adv.std(unbiased=False)+1e-8)
  for epoch in range(4):
   for ids in np.array_split(rng.permutation(len(obs)),4):
    logits,v=net(obs[ids]);dist=Categorical(logits=logits);ratio=(dist.log_prob(act[ids])-oldlog[ids]).exp();objective=torch.minimum(ratio*adv[ids],ratio.clamp(.8,1.2)*adv[ids]);vloss=(v-returns[ids]).square().mean();loss=-objective.mean()+.5*vloss-.01*dist.entropy().mean();opt.zero_grad();loss.backward();nn.utils.clip_grad_norm_(net.parameters(),.5);opt.step()
  with torch.no_grad():logits,_=net(obs);dist=Categorical(logits=logits);ratio=(dist.log_prob(act)-oldlog).exp();diagnostics.append([float(((ratio<.8)|(ratio>1.2)).float().mean()),float((oldlog-dist.log_prob(act)).mean()),float(dist.entropy().mean())])
  curve.append([(update+1)*16*horizon,evaluate(net,'PPO',9001,100)['mean_return']])
 return net,curve,diagnostics

def run(out,language):
 out.mkdir(parents=True,exist_ok=True);tr=lambda z,e:z if language=='zh'else e;plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def save(fig,n):fig.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');fig.savefig(out/f'{n}-{language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
 seeds=[37,137,237];curves={};scores={};models={};diag=[]
 for kind,train in [('DQN',train_dqn),('PPO',train_ppo)]:
  curves[kind]=[];scores[kind]=[]
  for seed in seeds:
   net,curve,detail=train(seed);curves[kind].append(curve);scores[kind].append(evaluate(net,kind,19001,500))
   if seed==37:models[kind]=net
   if kind=='PPO':diag.append(detail)
  print(kind,[x['mean_return']for x in scores[kind]],flush=True)
 # Positive max bias with independent zero-mean estimation noise.
 rng=np.random.default_rng(3700);action_counts=[2,5,10,20];bias=[];spread=[]
 for k in action_counts:
  online=rng.normal(size=(50000,k));independent=rng.normal(size=(50000,k));selected=online.argmax(1);maxima=online.max(1);double=independent[np.arange(len(online)),selected];bias.append([maxima.mean(),double.mean()]);spread.append([maxima.std()/math.sqrt(len(maxima)),double.std()/math.sqrt(len(double))])
 hand=gae(np.array([[0],[0],[1]],dtype='float32'),np.array([[.2],[.3],[.4]],dtype='float32'),np.array([[.3],[.4],[0]],dtype='float32'),np.array([[0],[0],[1]],dtype='float32'),.9,.8).ravel()
 torch.save({kind:model.state_dict()for kind,model in models.items()},out/'policies.pt');loaded=torch.load(out/'policies.pt',weights_only=True);probe=torch.eye(10);reload_errors={}
 for kind,cls in [('DQN',QNet),('PPO',ActorCritic)]:
  fresh=cls();fresh.load_state_dict(loaded[kind]);before=models[kind](probe);after=fresh(probe)
  if kind=='PPO':before,after=before[0],after[0]
  reload_errors[kind]=float((before-after).abs().max().detach())
 oracle_value,oracle_success=exact_policy_value(True);random_value,random_success=exact_policy_value(False)
 summary={'seeds':seeds,'steps_per_seed':6144,'evaluation_episodes_per_seed':500,'gamma':GAMMA,'finite_horizon':20,'slip_probability':.1,'exact_toward_goal_return':oracle_value,'exact_toward_goal_success':oracle_success,'exact_random_return':random_value,'exact_random_success':random_success,'evaluation':{kind:{'seed_mean_returns':[s['mean_return']for s in values],'seed_success_rates':[s['success_rate']for s in values],'mean_return':float(np.mean([s['mean_return']for s in values]))}for kind,values in scores.items()},'gae_hand':hand.tolist(),'dqn_hand_target':1+.9*5,'double_dqn_hand_target':1+.9*2,'dueling_hand_q':[1,3],'ppo_positive_clipped':min(1.5*2,1.2*2),'ppo_negative_clipped':min(.5*(-2),.8*(-2)),'max_bias':np.array(bias).tolist(),'action_counts':action_counts,'reload_errors':reload_errors}
 (out/'evaluation.json').write_text(json.dumps(scores,indent=2),encoding='utf-8')
 (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(out/'configuration.json').write_text(json.dumps({'environment':'finite-horizon courier','observation':'onehotposition7,onehotgoal2,remaining/20','actions':['left','right'],'reward':'goal+1,wrong endpoint-1,otherwise-0.02','architecture':'10-32tanh-32tanh;Q2 or policy2/value1','saved_seed':37,'steps':6144,'evaluation_seed':19001},indent=2),encoding='utf-8');np.savez_compressed(out/'data.npz',dqn_curves=curves['DQN'],ppo_curves=curves['PPO'],ppo_diagnostics=diag,bias=bias,bias_standard_error=spread,gae=hand)
 fig,axs=plt.subplots(1,2,figsize=(11,4.1),layout='constrained')
 for kind,color in [('DQN','#176b91'),('PPO','#bc6945')]:
  data=np.array(curves[kind]);x=data[0,:,0];vals=data[:,:,1];axs[0].plot(x,vals.mean(0),label=kind,color=color);axs[0].fill_between(x,vals.min(0),vals.max(0),color=color,alpha=.15)
  means=[s['mean_return']for s in scores[kind]];axs[1].scatter(np.full(3,0 if kind=='DQN' else 1)+np.array([-.1,0,.1]),means,color=color,s=60,label=kind)
 axs[0].axhline(oracle_value,color='#267c6a',ls=':',label=tr('朝目标策略精确期望','Exact toward-goal expectation'));axs[0].axhline(random_value,color='#999',ls='--',label=tr('随机策略精确期望','Exact random expectation'));axs[0].set(xlabel=tr('环境交互步数 / 每个种子','Environment steps / seed'),ylabel=tr('贪心评价回报','Greedy evaluation return'),title=tr('3个种子：均值与最小—最大范围','3 seeds: mean and min–max range'));axs[0].legend(fontsize=8);axs[1].set(xticks=[0,1],xticklabels=['DQN','PPO'],ylabel=tr('独立500回合的平均回报','Mean return over 500 independent episodes'),title=tr('固定最终预算，不挑最好检查点','Fixed final budget; no best-checkpoint selection'));save(fig,'learning')
 fig,axs=plt.subplots(2,2,figsize=(11,4.8),layout='constrained')
 for row,kind in enumerate(['DQN','PPO']):
  for col,goal in enumerate([0,6]):
   ax=axs[row,col];positions=np.arange(1,6);obs=np.column_stack([np.eye(7)[positions],np.tile(np.eye(2)[goal//6],(5,1)),np.ones(5)]).astype('float32')
   with torch.no_grad():res=models[kind](torch.tensor(obs));values=res[0].softmax(-1).numpy()if kind=='PPO'else res.numpy()
   im=ax.imshow(values.T,aspect='auto',cmap='viridis',vmin=0 if kind=='PPO'else -1.1,vmax=1 if kind=='PPO'else 1.1);ax.set(xticks=range(5),xticklabels=positions,yticks=[0,1],yticklabels=tr('向左|向右','Left|Right').split('|'),xlabel=tr('初始位置','Starting position'),title=f'{kind} / '+tr('目标','target')+f'={goal}')
   for i in range(2):
    for j in range(5):ax.text(j,i,f'{values[j,i]:.2f}',ha='center',va='center',color='white'if values[j,i]<(values.max()+values.min())/2 else'#102f43')
   fig.colorbar(im,ax=ax,ticks=[0,.5,1]if kind=='PPO'else[-1,0,1],label=tr('概率'if kind=='PPO'else'Q值','Probability'if kind=='PPO'else'Q value'))
 save(fig,'policy')
 fig,axs=plt.subplots(1,3,figsize=(12,3.6),layout='constrained');bias=np.array(bias);spread=np.array(spread)
 for j,label,color in [(0,tr('同一估计取最大','Max of one estimate'),'#bc6945'),(1,tr('独立估计评价所选动作','Independent evaluation'),'#176b91')]:axs[0].errorbar(action_counts,bias[:,j],yerr=1.96*spread[:,j],fmt='o-',label=label,color=color)
 axs[0].axhline(0,color='#888',ls='--');axs[0].set(xticks=action_counts,xlabel=tr('候选动作数','Number of actions'),ylabel=tr('真实值0时的平均估计','Mean estimate when true values are 0'),title=tr('50000次噪声算例','50000 noise experiments'));axs[0].legend(fontsize=7)
 ratio=np.linspace(.3,1.7,200)
 for adv,color in [(2,'#176b91'),(-2,'#bc6945')]:axs[1].plot(ratio,np.minimum(ratio*adv,np.clip(ratio,.8,1.2)*adv),label=f'A={adv}',color=color)
 axs[1].axvspan(.8,1.2,color='#d9e4e9',alpha=.6);axs[1].set(xlabel=tr('新旧策略概率比','New/old probability ratio'),ylabel=tr('单样本代理目标','Single-sample surrogate'),title='PPO-Clip');axs[1].legend()
 axs[2].bar(range(3),hand,color='#267c6a');axs[2].set(xticks=range(3),xticklabels=['t=0','t=1','t=2'],ylabel=tr('优势估计','Advantage estimate'),title=tr('GAE手算：γ=.9，λ=.8','GAE example: γ=.9, λ=.8'));save(fig,'mechanisms');print(json.dumps(summary,indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('output'));p.add_argument('--language',choices=['zh','en'],default='en');args=p.parse_args();run(args.output,args.language)
```

Every 512 environment steps, the learning curve evaluates 100 fixed episodes. Final reporting uses the final-budget models on another 500 episodes. Each evaluation episode has its own deterministic seed, giving models identical initial conditions and stepwise random numbers. Evaluation removes DQN epsilon exploration and selects PPO’s highest-probability action. All three training seeds learn goal-directed greedy behavior, so both methods obtain mean undiscounted return about 0.9084 and success rate 0.98 on these common evaluation conditions. Identical final results arise from identical greedy behavior under shared evaluation episodes, even though learned probabilities and value estimates need not match.

![Three training seeds with 6144 interactions each. Left: 100 fixed greedy episodes/checkpoint, shading is the seed min–max range. Right: final means on another 500 episodes. Baselines are exact dynamic-programming expectations.](https://ml-biomat.com/static/tutorials/machine-learning/figures/cd4103461b35c1b9a8c83500.svg?v=cd4103461b35)

Figure 2Three training seeds with 6144 interactions each. Left: 100 fixed greedy episodes/checkpoint, shading is the seed min–max range. Right: final means on another 500 episodes. Baselines are exact dynamic-programming expectations.

Known transition rules provide a complementary exact calculation. Starting with zero remaining steps and proceeding backward, the always-toward-goal policy has twenty-step expected return about 0.89874365 and success probability about 0.97499151. Uniform random actions yield expected return about−0.11324238. The 500-episode sample mean exceeding the toward-goal expectation is ordinary finite-sample variation. Training discounts rewards by 0.97, whereas plotted evaluation sums undiscounted rewards; these are different quantities. The policy panels display actual Q-values or action probabilities across starting positions and both goals, with remaining time fixed at twenty.

![Actual seed 37 outputs with 20 steps remaining. Top: DQN action values; bottom: PPO action probabilities. Quantities have separate color scales, shared within each kind.](https://ml-biomat.com/static/tutorials/machine-learning/figures/0755aeb366653dcbacc71215.svg?v=0755aeb36665)

Figure 3Actual seed 37 outputs with 20 steps remaining. Top: DQN action values; bottom: PPO action probabilities. Quantities have separate color scales, shared within each kind.

One displayed Q-value is about 1.05, above the maximum return of one in this task. This is a function-approximation error, illustrating that selecting the right action and estimating its value accurately are different goals. Relative left/right values can still support correct decisions. The PPO panels instead contain probabilities between zero and one, summing to one at each position. Distinct color scales prevent larger values in these two outputs from being mistaken for the same kind of confidence.

The mechanism panels expose three independently checkable calculations: selection bias under noisy estimates, positive/negative PPO clipping curves, and the three-step GAE result. These explain components without replacing environment-based algorithm comparisons. The program saves seed 37 weights for both models, architecture and environment configuration, per-episode final returns, and plotting arrays. Fresh networks reload the saved parameters and reproduce their outputs with maximum difference zero. Readers can therefore retrain the experiment or inspect the already saved policies rather than receiving figures alone.

![Left: 50,000 selection experiments with independent zero-mean Gaussian noise; error bars show the mean plus or minus 1.96 standard errors. Middle: the single-sample PPO objective with clipping width 0.2. Right: a three-step GAE worked example.](https://ml-biomat.com/static/tutorials/machine-learning/figures/4ddc70c4f0f39451099bf8c4.svg?v=4ddc70c4f0f3)

Figure 4Left: 50,000 selection experiments with independent zero-mean Gaussian noise; error bars show the mean plus or minus 1.96 standard errors. Middle: the single-sample PPO objective with clipping width 0.2. Right: a three-step GAE worked example.

## 9. Separate exploration, sample efficiency, and evaluation stability

A training return combines learning, exploration, and environmental randomness. DQN’s random actions can reduce immediate training return while discovering useful routes, and PPO entropy changes sampled behavior. Evaluation should specify whether this randomness remains, and final reporting should use episodes separate from those repeatedly inspected during development. Selecting the highest checkpoint on an evaluation curve makes those episodes part of selection, requiring another independent assessment. Here final models are fixed by budget, with three seeds and the training min–max range shown. An unusually successful individual episode is not treated as the method’s typical performance.

Sample efficiency asks how much environmental experience learning requires; computational efficiency asks how much time and hardware it consumes. Replay can save interaction while increasing optimization work. Parallel environments accelerate collection while changing correlation and update schedules. Comparisons should record environment steps, optimization steps, replay ratio, network size, and measured runtime. Three curves converging to the same behavior describe these seeds on this task, while altered action-flip rates, goal distributions, or deadlines create useful new evaluations. Training-seed variation and finite-episode evaluation variation are separate sources of uncertainty, even when the final seed results happen to coincide.

Reward design also determines the learned behavior. Increasing movement penalties encourages shorter episodes and can eventually change whether reaching the goal is worth the risk. Rewarding every move toward a target requires checking whether repeated back-and-forth motion can accumulate bonuses. Besides mean return, record success, failure categories, completion time, and constraint violations. Connecting these measures to the application reveals what the network actually learned. Neural networks expand representation, while explicit state, reward, data, and evaluation conventions make that capacity usable for continued decision-making research.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M37.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Spinning Up — Algorithm Taxonomy](https://spinningup.openai.com/en/latest/spinningup/rl_intro2.html)

   Learned objects and data relationships across methods.
2. [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602)

   Early connection between pixel representations and deep action values.
3. [CleanRL — DQN](https://docs.cleanrl.dev/rl-algorithms/dqn/)

   Target networks, replay, and implementation choices.
4. [Deep Reinforcement Learning with Double Q-learning](https://arxiv.org/abs/1509.06461)

   Separate selection from evaluation.
5. [Dueling Network Architectures](https://arxiv.org/abs/1511.06581)

   State-value and action-advantage branches.
6. [Spinning Up — Policy Optimization](https://spinningup.openai.com/en/latest/spinningup/rl_intro3.html)

   Trajectory probabilities, log derivatives, and policy gradients.
7. [Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438)

   Value baselines and advantage propagation.
8. [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)

   Clipped surrogate and multiple update epochs.
9. [Spinning Up — PPO Implementation](https://raw.githubusercontent.com/openai/spinningup/master/spinup/algos/pytorch/ppo/ppo.py)

   PPOBuffer termination, rollout bootstrapping, and GAE.
10. [Spinning Up — PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html)

    Positive/negative clipping and relation toTRPO.
11. [Spinning Up — DDPG](https://spinningup.openai.com/en/latest/algorithms/ddpg.html)

    Continuous action maximization and differentiable actors.
12. [Spinning Up — TD3](https://spinningup.openai.com/en/latest/algorithms/td3.html)

    Twin critics, delayed updates, and target smoothing.
13. [Spinning Up — SAC](https://spinningup.openai.com/en/latest/algorithms/sac.html)

    Entropy regularization and soft values.
