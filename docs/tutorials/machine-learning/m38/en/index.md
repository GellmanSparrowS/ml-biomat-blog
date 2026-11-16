# From experience to action: offline learning, predictive control, and multiple agents

Source: https://ml-biomat.com/tutorials/machine-learning/m38/en/
Language: en

Use recorded experience, dynamical models, and information from other agents to understand how decisions reach the real world.

## A delivery cart needs more than a reward table

Imagine a cart delivering books through a library. You have recordings of staff driving it, so you would like it to learn familiar routes before operating on its own. Once moving, it must brake using its current position and speed. When another cart approaches a narrow entrance, the two must coordinate. Each problem involves choosing actions, but the available information differs. Demonstrations describe what someone previously did, a motion model predicts what an action might cause, and information about a partner determines which choices work together. Identifying these information sources is often more useful than beginning with a complicated network.

Earlier reinforcement learning examples allowed the agent to act, observe a reward, and try again. This chapter separates that loop into its parts. Sometimes a fixed collection of records is all that learning can use. Sometimes a model can predict future states before an action is executed. Sometimes other decision makers are learning at the same time. Offline, model-based, and multi-agent reinforcement learning address these changes, and their methods can be combined. A robot arm might first imitate recorded demonstrations, plan with learned dynamics, and then coordinate with a mobile platform. These categories describe information and interaction patterns rather than mutually exclusive architectures.

Three small experiments make the mechanisms visible. The first has two states and two actions, so we can follow the consequences of missing data in a value table. The second controls a moving object with position and velocity, comparing an initial plan with repeated feedback. The third trains two cooperating agents and asks how a shared reward should be assigned to individual decisions. Knowing the complete rules gives every number a clear interpretation. It also reveals which additional observations, constraints, and data would be required when the same ideas are used in robotics.

## Learning demonstrations and reasoning about missing actions

Behavior cloning treats driving records as supervised learning examples. The input is the observation available to the driver, and the label is the demonstrated steering action. For discrete actions, a model predicts probabilities and increases the probability of the demonstrated choice. For continuous actions, it may predict a position, velocity, or torque command with a suitable regression loss. Rewards are not required for this training objective. The observations in the demonstrations determine the situations that the policy practices. An expert who usually stays in the middle of a road may provide few examples of recovering after the vehicle has already drifted toward its edge.

$$
\mathcal L_{\rm BC}(\theta)=-\frac1N\sum_{i=1}^{N}\log\pi_\theta(a_i\mid o_i)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/738f6e53c5d5b713b7e0925a.svg) | N is the number of records and i indexes them; both are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0edfd5e80a775cd134ebe2cf.svg) | Observation and demonstrated action in record i; both are categorical integers here. |
| ![Formula](https://ml-biomat.com/static/agent-math/a14a05c17a6f753c12e01c4a.svg) | Action probability parameterized by theta; probabilities are dimensionless, with two logits per state here. |
| ![Formula](https://ml-biomat.com/static/agent-math/3fd1ba0c6b5f2dff6c6bb973.svg) | Mean negative natural log likelihood, dimensionless; log is the natural logarithm. |

For demonstrated action 0, assigning probability 0.8 gives loss −ln(0.8)=0.2231; assigning 0.2 gives 1.6094. Averaging lets every example influence the update toward the demonstrated conditional action distribution.

This distribution issue motivates DAgger: run the current learner to collect observations, ask an expert which actions should be taken there, and add those labeled observations to the training set. Future training then includes situations that the learner itself tends to encounter. The procedure requires continued environment interaction and expert queries, whereas purely offline cloning uses an already collected dataset. For robot manipulation, useful collection decisions include recording recovery attempts, variation in object pose, execution timestamps, and the alignment of cameras with joint sensors. A good demonstration dataset needs both useful actions and adequate coverage of observations.

Offline reinforcement learning also uses recorded rewards to seek better decisions. A difficulty appears when value updates compare all available actions while the dataset supplies evidence for only some of them. Consider state s0, where action 0 leads to s1 with reward 0. At s1, action 0 ends the episode with reward 1. One hundred repetitions provide 200 transitions. At discount 0.9, the demonstrated route has value 0.9 from s0. Action 1 never appears, but suppose its initial estimated value is 3. Ordinary offline Q-learning cannot correct those unsupported entries and propagates their optimism backward: even the recorded action at s0 reaches an estimate of 2.7.

$$
\mathcal L(Q)=\frac{1}{2N}\sum_i\left[Q(s_i,a_i)-y_i\right]^2+\frac{\alpha}{N}\sum_i\left[\log\sum_a e^{Q(s_i,a)}-Q(s_i,a_i)\right],\qquad y_i=r_i+\gamma(1-d_i)\max_{a'}\bar Q(s_i',a')
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5f7947c05c98be410cc3d116.svg) | Transition count and index, current state, recorded action, reward, next state, and terminal indicator d in {0,1}; rewards are normalized and dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/462b3a536c9dc2f497facce9.svg) | Q is a 2 by 2 action-value table; bar Q is a frozen target table and y a fixed regression target, all in discounted reward units. |
| ![Formula](https://ml-biomat.com/static/agent-math/6dad6f354c6551df5aab8c6b.svg) | The sum and maximum range over available actions; gamma=0.9 is the dimensionless discount. |
| ![Formula](https://ml-biomat.com/static/agent-math/12a26ef968e68bff378e02ae.svg) | Alpha weights the conservative term, 0 or 1 here; L is a scalar objective. Log and e denote natural logarithm and exponential, applied to Q on the normalized reward scale. |

With Q=[1,3] and only action 0 recorded, the penalty is ln(e¹+e³)−1≈2.1269. With [1,0], it falls to 0.3133. Optimization discourages unsupported actions from towering over recorded actions. A terminal transition has d=1, so its target is just its reward.

The 2020 CQL work addressed unsupported high action values through a conservative training objective. The discrete-action version above combines Bellman regression with a log-sum-exp penalty relative to recorded actions. After 1,000 updates in our experiment, ordinary Q chooses the unrecorded action in both states, while CQL and greedy behavior cloning choose recorded actions. If action 1 actually ends the episode with reward −2, their discounted returns from s0 are −2, 0.9, and 0.9. Adding five action-1 transitions with reward −2 at each state also lets ordinary Q recover the supported route. Changing data coverage changes the learning problem itself.

![Why fixed data leave multiple answers. The upper row shows value tables and original coverage. The bottom compares Q, CQL, and greedy BC trained on the same 200 records in two worlds differing only in the unrecorded action reward. The coverage-augmented Q uses ten additional −2 transitions and appears only above. The shared color scale runs from −4 to 4.](https://ml-biomat.com/static/tutorials/machine-learning/figures/28dff367dd2e7c6e16065975.svg?v=28dff367dd2e)

Figure 1Why fixed data leave multiple answers. The upper row shows value tables and original coverage. The bottom compares Q, CQL, and greedy BC trained on the same 200 records in two worlds differing only in the unrecorded action reward. The coverage-augmented Q uses ten additional −2 transitions and appears only above. The shared color scale runs from −4 to 4.

Now change only the unrecorded action reward to +2. The original 200 records remain identical. Ordinary Q happens to obtain 2, while CQL and cloning retain 0.9. Additional evidence is needed to distinguish these worlds; conservative preferences determine how an algorithm acts in its absence. Read the table numerically as well: after finite optimization, CQL’s recorded-action values are approximately 0.920 and 1.010, slightly above the true values 0.9 and 1. Its objective encourages conservatism, but individual cells in this run are not strict lower bounds. The deliberately optimistic initialization makes the unsupported-value mechanism easy to inspect.

## Predicting the next state before selecting an action

A cyclist estimates whether braking will stop the bicycle before an obstacle using distance, speed, and experience with the brakes. Model-based decision making makes that prediction explicit. A dynamics model takes a state and action and predicts the next state; additional models can predict rewards and termination. Its rules may come from physics or from fitted data. A planner then compares the consequences of candidate action sequences. Compared with predicting an action value directly, a dynamics model provides an interpretable intermediate question: was the predicted velocity wrong, or did the chosen objective simply prefer faster motion?

$$
x_{t+1}=Ax_t+Bu_t,\qquad x_t=\begin{bmatrix}p_t\\v_t\end{bmatrix},\quad A=\begin{bmatrix}1&\Delta t\\0&1\end{bmatrix},\quad B=\begin{bmatrix}\tfrac12\Delta t^2\\\Delta t\end{bmatrix}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d0da4b4e06aa18f369f7ff17.svg) | t indexes steps; delta t=0.2 seconds is the main experiment interval. |
| ![Formula](https://ml-biomat.com/static/agent-math/80c07f2de91d2a3f9cb14a45.svg) | x is a 2 by 1 state vector, p is position in meters, and v velocity in meters per second. |
| ![Formula](https://ml-biomat.com/static/agent-math/06f429a3f1595f2f96e26ad6.svg) | u is constant acceleration within a step in m/s²; A is 2 by 2 and B is 2 by 1. The nonzero off-diagonal A entry has units s, while B rows have units s² and s. |

Constant acceleration changes velocity by u times delta t. Position adds the distance at the initial velocity and the additional uniformly accelerated displacement. Starting from p=1 m, v=0.5 m/s, and u=−1 m/s², after 0.2 s the state is p=1.08 m and v=0.3 m/s.

Our state contains position and velocity, and acceleration is held constant for each 0.2-second interval. Elementary constant-acceleration motion gives the update equation. Position alone would be insufficient: a cart at the same location could be moving forward or backward, producing different next positions. Including velocity supplies that missing information. The units of each column remain meaningful inside an array. Position in meters and velocity in meters per second become compatible additions because the matrix contains the appropriate time factors. This is also a useful check on a learned model: an unexplained change of units can alter its inputs without changing their numerical shape.

For system identification, the program generates 200 independent combinations of position, velocity, and acceleration. Position ranges from −2 to 2 meters, with velocity and acceleration each between −1 and 1 in their respective units. The true model produces the next state, then measurement noise with standard deviation 0.01 is added separately in meters and meters per second. The first 150 transitions fit a least-squares model; the last 50 evaluate it. The fitted control coefficients are approximately 0.02076 and 0.20225, compared with true values 0.02 and 0.2. Against noise-free held-out truth, position RMSE is 0.00115 m and velocity RMSE 0.00191 m/s.

![Dynamics identified from 150 noisy transitions. Each left cell is fitted minus true coefficient on reference scales 1 m, 1 m/s, and 1 m/s², at a 0.2-second interval. The right panel shows actual position–velocity trajectories, with a star at the stationary target. Error against noise-free truth on 50 independent inputs is reported in the text.](https://ml-biomat.com/static/tutorials/machine-learning/figures/1501233cdeb004dc191f93ec.svg?v=1501233cdeb0)

Figure 2Dynamics identified from 150 noisy transitions. Each left cell is fitted minus true coefficient on reference scales 1 m, 1 m/s, and 1 m/s², at a 0.2-second interval. The right panel shows actual position–velocity trajectories, with a star at the stationary target. Error against noise-free truth on 50 independent inputs is reported in the text.

A long plan repeatedly feeds predictions back into the model, giving small one-step errors opportunities to accumulate. A planner requesting acceleration 10 from a model trained only between −1 and 1 also relies on extrapolation. Model ensembles can expose disagreement between predictors, while shorter imagined trajectories and frequent real observations reduce the time over which errors compound. World-model methods such as DreamerV3 learn latent representations and train behavior using imagined trajectories. Our two-dimensional physical model keeps states directly readable while preserving the basic structure: predict consequences, compare actions, and reconnect predictions to observations.

## LQR gives feedback; MPC plans within constraints

Penalizing distance alone can leave a cart moving quickly as it approaches its destination, so it overshoots. A useful objective also accounts for speed and the effort spent accelerating. Linear quadratic regulation, or LQR, studies linear dynamics with quadratic costs: larger deviations receive a squared penalty, and larger actions cost more. The structure makes dynamic programming tractable and produces a linear feedback law. At each measurement, multiplying position and velocity by a gain gives the next command. The controller need not enumerate a long action tree during execution, because the infinite-horizon optimization has already been summarized in that gain.

$$
P=Q+A^TPA-A^TPB(R+B^TPB)^{-1}B^TPA,\qquad K=(R+B^TPB)^{-1}B^TPA,\qquad u_t=-Kx_t
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/03989545ad94aaeaa348c0bf.svg) | Linear dynamics matrices, state, and action, with shapes 2 by 2, 2 by 1, 2 by 1, and scalar. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb70477a5508a528bdcbf292.svg) | State weight diag(1,0.1) and action weight [0.1], shapes 2 by 2 and 1 by 1, specified on reference scales 1 m, 1 m/s, and 1 m/s². |
| ![Formula](https://ml-biomat.com/static/agent-math/2afee757440eae1fd37defb2.svg) | P is the symmetric 2 by 2 infinite-horizon value matrix; K is a 1 by 2 gain. T means transpose and superscript −1 means matrix inverse. Normalized costs are dimensionless. |

Minimizing the current quadratic cost plus the next quadratic value over the action gives linear feedback and the Riccati equation. Here K=[2.41456,2.32640]. At p=1 and v=0 the unconstrained command is −2.41456 m/s²; an actuator bound of 1 produces −1 instead. This clipped controller differs from the unconstrained optimum.

We use reference scales of 1 m, 1 m/s, and 1 m/s² so that state and action costs can be combined, with weights 1, 0.1, and 0.1 on squared position, velocity, and acceleration. Increasing the position weight favors returning to the target sooner; increasing the action weight values smaller commands. This example uses undiscounted infinite-horizon LQR. Its stabilization conditions hold for the controllable double integrator with positive state and action weights. The code solves the discrete Riccati equation, then clips the command to ±1. Clipping is useful for a limited actuator, but it changes the problem from the unconstrained optimization that produced the gain.

Model predictive control, or MPC, places the action bounds inside each optimization. Starting from the current measured state, it plans 12 steps, or 2.4 seconds, while respecting the acceleration limit throughout the plan. Only the first command is applied. After 0.2 seconds, a new measurement initializes another optimization. This resembles navigating with a planned route that can be recalculated as conditions change. Here the linear dynamics make every predicted state a linear function of the planned actions. The quadratic objective therefore becomes a bounded least-squares problem that SciPy can solve directly.

$$
\min_{u_0,\ldots,u_{H-1}}\left[\sum_{j=1}^{H-1}x_j^TQx_j+x_H^TPx_H+\sum_{j=0}^{H-1}u_j^TRu_j\right]\quad\text{subject to }x_{j+1}=\hat A x_j+\hat B u_j,\ |u_j|\le u_{\max}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b81cfed776f3a3c36f7417e8.svg) | H is the planning horizon, 12 here; j indexes steps relative to the present; x0 is the measured current state, and xj and uj are predicted states and planned actions. |
| ![Formula](https://ml-biomat.com/static/agent-math/dbd2b2a01b5fbeeae983157e.svg) | Hats indicate dynamics fitted to 150 training transitions; Q and R weight states and actions, while P is the Riccati terminal weight for the fitted model. Shapes and normalized units are as above. |
| ![Formula](https://ml-biomat.com/static/agent-math/1a5a77c2df23d512bac667fd.svg) | Maximum acceleration 1 m/s²; T means transpose and vertical bars absolute value. |

Predicted states depend linearly on the planned actions, turning this quadratic problem into bounded least squares. The current-state cost is constant during planning and can be omitted. With H=1 only the next-state terminal cost and current action cost remain. Execute the first action, measure again, and solve a new problem.

![The same eight-second motion and velocity impulse at three seconds. Position, applied acceleration with ±1 m/s² bounds, and accumulated normalized stage costs are shown. MPC remeasures and replans every 0.2 seconds; the open-loop comparison executes its original plan without responding to the disturbance.](https://ml-biomat.com/static/tutorials/machine-learning/figures/b6960cbdac557af0bade4421.svg?v=b6960cbdac55)

Figure 3The same eight-second motion and velocity impulse at three seconds. Position, applied acceleration with ±1 m/s² bounds, and accumulated normalized stage costs are shown. MPC remeasures and replans every 0.2 seconds; the open-loop comparison executes its original plan without responding to the disturbance.

The cart starts at position 1.5 m with zero velocity, runs for eight seconds, and receives a sudden velocity increase of 0.7 m/s at three seconds. Executing a previously computed 40-step plan without feedback leads to growing displacement and a total cost of about 110.41. Clipped LQR scores 13.89274 and MPC using identified dynamics scores 13.89256. The two feedback controllers perform almost identically here; responding to the disturbance is the major distinction. MPC provides a way to combine multi-step commands, state constraints, and more general prediction models within one planning problem. Its practical benefit depends on those constraints, model accuracy, and available computation.

The interactive planner replaces continuous acceleration with three selectable levels so that every short plan can be enumerated. It uses a 0.5-second interval, terminal position and velocity weights 2 and 0.5, intermediate weights 1 and 0.1, and action weight 0.1. A longer horizon increases the candidate count and can change when braking begins. Each execution button applies only the first action of the current best plan, then replans from the resulting state. A velocity impulse after the third step shows why the future trajectory is a proposal that changes with measurement.

## Replan after every executed step

Change the initial state and horizon, then execute one step at a time. A specified velocity impulse is applied after step three. Gray curves show the five plans following the optimum; unexecuted plans change with new measurements.

[Figure: Replan after every executed step](https://ml-biomat.com/tutorials/machine-learning/m38/en/#M38-plot)

Time step 0.5 seconds; actions are −limit, 0, or +limit. Terminal state weights (2,0.5), intermediate weights (1,0.1), action weight 0.1. Manual stepping, with no automatic playback.

## Learning partners change the environment

When two people carry a table, moving in opposite directions can be worse than moving together in either direction. Cooperative agents face the same dependence: the value of one action depends on another agent’s action. If a learner treats its partner as a fixed environment while both update their policies, older experience describes an older partner. This is one source of non-stationarity in multi-agent learning. Centralized training with decentralized execution addresses the information problem by allowing training to use global state and joint actions while restricting each deployed actor to its own permitted observations.

MADDPG, introduced in 2017, supplies other agents’ actions to the critic during training, helping distinguish partner choices from unexplained environment variation. Actors can still execute using local information. QMIX, introduced in 2018, combines individual action values through a monotonic mixing network. Its monotonicity connects local greedy choices with greedy selection of the mixed value, while restricting which joint value functions can be represented. Tasks where success depends on asymmetric combinations can require richer interactions than additive local values. A centralized-training design must specify exactly which information reaches each component and which of it remains available at execution time.

$$
J(p,q)=(1-p)(1-q)-p(1-q)-(1-p)q+3pq,\qquad A^A(a,b)=G(a,b)-\sum_{a'}\pi_A(a')G(a',b)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3c86914474b1db6c13af3d27.svg) | Probabilities that agents A and B choose action 1, each between 0 and 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/395b9a6193444ab3c59e86ee.svg) | J is expected shared reward; G is the 2 by 2 table [[1,−1],[−1,3]]; a and b are the chosen actions and a prime ranges over A alternatives. Rewards are normalized and dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/202deea885e03a4e37720ce6.svg) | Pi A is the current action distribution for agent A; superscript A identifies the agent and A superscript A is its counterfactual advantage in reward units. |

The four terms multiply each joint-action probability by its reward. At p=q=0.5, J=(1−1−1+3)/4=0.5. If B chose 1, holding B fixed gives A a baseline of 0.5×(−1)+0.5×3=1. A choosing 1 receives advantage 2; A choosing 0 receives advantage −2.

Our cooperative game has a compact payoff table: both choosing 0 earns 1, both choosing 1 earns 3, and disagreement earns −1. Each policy is a Bernoulli probability, making all four joint outcomes enumerable. If both agents choose 1 with probability 0.5, expected reward is 0.5. Raising one probability to 0.8 while the other remains 0.5 raises expected reward to 0.8. However, if the partner almost always chooses 0, increasing the probability of 1 can create more disagreements. The table makes the dependence between a good action and the current partner policy visible without requiring a large simulator.

Competitive tasks require different evaluation logic. In rock–paper–scissors, always choosing rock invites a paper-playing opponent to exploit the policy. Equal probabilities across the three actions remove the systematic advantage of any fixed opponent. A competitive policy should therefore be tested against an opponent collection or an explicitly defined opponent distribution, rather than only the final training partner. Self-play creates evolving opponents, while pools of historical policies preserve previous styles. Cooperative shared return and competitive exploitability measure different properties, even when both systems use similar neural networks and policy-gradient machinery.

Action timing is part of the task definition. PettingZoo’s Parallel API submits actions for simultaneously acting agents together; its AEC API processes agent turns and can represent simultaneous games under appropriate update rules. If a rock–paper–scissors implementation accidentally reveals the first player’s current move to the second before it acts, it implements a different game. Observations, valid-action masks, individual termination signals, and access to partners’ current actions must match the intended rules. A multi-agent dataset contains more than an additional agent dimension: it describes who knows what, and when that knowledge becomes available.

## Assigning credit after a shared outcome

Giving every agent the same team reward provides a workable starting point, but its learning signal includes the randomness of other agents. A sensible action may receive a poor update because a partner made an unfortunate choice. Counterfactual credit assignment asks a more specific question: holding the other agents’ actual actions fixed, what would happen if only my action changed? COMA expresses this through a baseline that averages over one agent’s alternative actions. A centralized critic estimates joint action values, and each actor receives an advantage relative to that counterfactual average.

$$
g_A=(a-p)\,[G(a,b)-b_A(b)],\qquad b_A(b)=\sum_{a'}\pi_A(a')G(a',b)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f45b7f6b64a4cd71bdeb9bdb.svg) | g A is the single-sample policy gradient with respect to agent A’s Bernoulli logit; a is 0 or 1 and p its probability of 1. a minus p is the log-probability derivative. |
| ![Formula](https://ml-biomat.com/static/agent-math/d8ac0f4ccf5d1edfd23ff034.svg) | G is shared reward, b is B’s action, and b A averages reward over A’s current action distribution with b fixed; the sum ranges over A actions. The baseline is detached in the policy gradient. |

Enumerating the four equally likely outcomes gives uncentered gradients −0.5,0.5,−0.5,1.5, with mean 0.25 and variance 0.6875. Counterfactual centering gives −0.5,1,−0.5,1, with the same mean and variance 0.5625. This variance reduction is specific to this payoff table and policy.

Our game has a known four-cell reward table, so the counterfactual baseline is exact and requires no learned critic. At uniform policies, raw-reward and counterfactual gradients both have mean 0.25, while their variances are 0.6875 and 0.5625. Their means agree because the expected derivative of an action’s log probability is zero, causing an action-independent baseline to cancel. The code detaches the baseline during the actor update. Otherwise, automatic differentiation would also differentiate its dependence on policy parameters, producing a different update. This small example connects the probability identity to an implementation choice that is easy to overlook.

![Shared rewards, credit assignment, and learning curves. Upper gradient means and variances are exact enumeration over four joint actions. Below are four seeds, 32 joint decisions per update, and 180 real training updates. Lines show seed means, bands the minimum and maximum, and the vertical axis the exact expected payoff of the current policy.](https://ml-biomat.com/static/tutorials/machine-learning/figures/a38879839fda8096afe0cc44.svg?v=a38879839fda)

Figure 4Shared rewards, credit assignment, and learning curves. Upper gradient means and variances are exact enumeration over four joint actions. Below are four seeds, 32 joint decisions per update, and 180 real training updates. Lines show seed means, bands the minimum and maximum, and the vertical axis the exact expected payoff of the current policy.

The actual experiment trains one Bernoulli logit per agent using batches of 32 joint actions, 180 Adam updates, and four random seeds. Both approaches learn to select the high-paying joint outcome more often. Final expected returns range from approximately 2.893 to 2.899 with raw rewards and 2.874 to 2.886 with the counterfactual baseline, approaching the optimum of 3. The baseline does not produce higher final returns in these runs. The exact variance result concerns one gradient at the uniform policy; the training trajectories additionally involve changing probabilities, finite batches, and Adam’s adaptive updates.

This comparison suggests how to design a useful evaluation. A credit-assignment study should examine the mean and variability of learning signals alongside team learning. A decentralized-execution study should inspect the observations actually available to each actor. A cooperation study should vary partners when partner robustness is the question. A single final score can conceal which mechanism improved. Here every seed is retained, and the shaded band displays the observed minimum and maximum rather than an uncertainty interval for a population mean. A smooth average line should not be read as the exact path taken by every run.

## From complete states to cameras and physical actuators

A simulator can expose precise position, velocity, and contact forces, while a robot receives images, encoder readings, and delayed sensor signals. A single image may not reveal the direction of motion; identical joint positions can accompany different velocities and loads. Partial observability makes observation history useful for state estimation. Stacking frames, using a recurrent network, explicitly estimating velocity, or maintaining probabilities over hidden states all address missing information. The appropriate representation depends on whether the missing quantity is a movement trend, an occluded object, or an unknown physical parameter.

$$
b_{t+1}(s')=\eta\,O(o_{t+1}\mid s')\sum_s P(s'\mid s,a_t)b_t(s)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6287735b28999d9ded38a578.svg) | b is a probability distribution over hidden states; s and s prime range over current and next hidden states. Probabilities are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/f29fa5b53beed1a41e25d98a.svg) | a is the executed action, o the new observation, P the transition probability, and O the observation likelihood. This model assumes the observation depends only on the new state. |
| ![Formula](https://ml-biomat.com/static/agent-math/2092c6227405ee2600312c46.svg) | Eta normalizes the new probabilities to sum to 1; t is a time index and the sum propagates uncertainty over old states. |

First predict through the dynamics, then correct with the observation. For a stationary target equally likely left or right, a left report has likelihood 0.8 if truly left and 0.2 otherwise. Unnormalized masses 0.4 and 0.1 become posterior probabilities 0.8 and 0.2 after multiplying by eta=2.

The action interface also needs a concrete definition. A network output of 0.5 could mean 0.5 newton-meters of torque or a normalized target position; those commands drive different physical behavior. Action scale, coordinate frame, update frequency, and low-level servo mode must agree. If a high-level policy updates ten times per second while the motor loop updates a thousand times per second, interpolation and command-holding rules become part of the dynamics. Delays can be represented using recent actions and observation timestamps. Contact and friction changes may require nonlinear or piecewise models rather than a single global linear approximation.

Simulation transfer depends on matching training variation to real variation. The 2017 visual domain-randomization work varied simulated appearance for object localization. In control, a related design can vary mass, friction, sensor noise, and action delay. The range should represent interpretable equipment differences, such as how an increased payload changes acceleration under the same torque. System identification offers another route: estimate parameters from real transitions, then plan or train around the fitted dynamics. The approaches combine naturally when measurements determine the center of a parameter distribution and uncertainty determines its width.

Constraints deserve an explicit place in the system. A collision penalty invites an optimizer to trade collision cost against other rewards; a hard joint-angle, velocity, or torque bound removes commands from the feasible set. MPC can incorporate constraints into planning, and an execution layer can check command bounds and apply a defined stopping action. Maintaining state constraints also depends on model error, disturbances, and whether the optimization remains feasible. Naming the constrained quantity, its units, measurement process, and recovery procedure turns a broad requirement into scenarios that can actually be tested.

## Evaluating a policy using someone else’s records

Offline policy evaluation estimates the return of a new policy from data collected by an older one. Importance sampling changes the weight of each trajectory according to how likely its actions would be under the target policy relative to the behavior policy. Ratios multiply along a trajectory because its action probability factors into conditional probabilities at successive steps. If the target policy selects an action that the behavior policy never selected under the same history, there are no matching experiences to reweight. The two indistinguishable offline worlds earlier in this chapter express the same coverage problem.

$$
\hat V_{\rm IS}=\frac1N\sum_{i=1}^N w_iG_i,\qquad w_i=\prod_{t=0}^{T_i-1}\frac{\pi(a_{it}\mid h_{it})}{\beta(a_{it}\mid h_{it})}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e855114b6328e693859ab863.svg) | N is the number of independent episodes, i their index, t a step index, and Ti the episode length; all are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/6dd7ff37e2727fe45f4771fd.svg) | Gi is episode discounted return, wi a dimensionless importance weight, and V hat the estimated target-policy value in reward units. |
| ![Formula](https://ml-biomat.com/static/agent-math/d634b295bfd681b8684a500f.svg) | Pi is the target policy and beta the data-collection policy; a is the recorded action and h the available history or sufficient state. Behavior probabilities must be positive on target-policy support. |

Two target-to-behavior ratios 0.8/0.5 and 0.6/0.3 produce weight 3.2. For returns 2 and 1 with weights 3.2 and 0.4, ordinary IS estimates (3.2×2+0.4×1)/2=3.4. Self-normalization divides by total weight 3.6 instead, giving 1.8889, with a different finite-sample bias–variance tradeoff.

Longer trajectories multiply more ratios, potentially producing extremely large or small weights and leaving an estimate dominated by a few episodes. Self-normalization, per-decision estimators, and hybrid methods manage different aspects of that variability. Fitted Q evaluation takes another approach: hold the evaluation policy fixed, average the next-step value over its actions, and fit the resulting Bellman target. Substituting a maximum over actions would change evaluation into an improvement problem. Model-based evaluation fits transition and reward models and runs the target policy inside them. These approaches depend on different ingredients: behavior probabilities, value approximations, or dynamics estimates.

Real datasets should be divided by complete episode, device, or time period when adjacent records share information. Useful metadata include the behavior-policy version, action probabilities when available, reward definitions, natural termination versus time limits, and delays between observation and execution. Minari provides an interface for organizing and iterating episodes; the selected dataset still determines field conversion, loader design, and applicable data rights. Inspecting state and action coverage before choosing cloning, conservative value learning, or further collection gives the experiment a more precise question than immediately applying an algorithm to a large replay buffer.

If the intended claim concerns completing a task under a new payload, the environment has changed as well as the policy. Separate same-environment policy comparisons from load-change and observation-noise experiments, recording success, task duration, and constraint events. This makes improvements in policy choice, dynamics adaptation, and sensing distinguishable. Our experiments disclose the true rules, allowing direct evaluation to provide a known answer. That known answer helps explain what an offline estimator requires; in physical tasks, independent executions provide evidence with which to calibrate the estimation process.

## Running three experiments with traceable outputs

The complete program generates offline records, identifies dynamics and runs controllers, then trains cooperative policies and saves all plots and numbers. Offline Q and CQL use Adam at learning rate 0.03 for 1,000 updates, with the target table copied every 20 steps. Cloning uses the same rate for 300 updates. System identification uses seed 38, trains on the first 150 transitions, and evaluates on the remaining 50. Cooperation uses seeds 38, 138, 238, and 338 with learning rate 0.04. The experiments report different quantities: discounted return, normalized control cost, and one-step shared reward. Keep those definitions separate when comparing their plots.

### Complete experiment: offline coverage, disturbed motion, and cooperative credit

Uses NumPy, SciPy, PyTorch, and Matplotlib. Select an output directory with --output and figure language with --language. summary.json stores numbers, data.npz curves and trajectories, and models.npz value tables, BC probabilities, fitted dynamics, and the feedback gain. All data are generated by the displayed rules.

```
"""Offline learning, receding-horizon control, and cooperative credit assignment.

All environments and datasets are generated here. No external weights or data.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.linalg import solve_discrete_are, block_diag
from scipy.optimize import lsq_linear

torch.set_num_threads(2)
COLORS = ['#256d85', '#e58f38', '#8a5a9e', '#4c9571']


def offline_fit(alpha, covered=False):
    # Repeated rows are repeated observations, not independent environments.
    s = torch.tensor([0, 1] * 100)
    a = torch.zeros(200, dtype=torch.long)
    reward = torch.tensor([0., 1.] * 100)
    nxt = torch.ones(200, dtype=torch.long)
    done = torch.tensor([0., 1.] * 100)
    if covered:
        s = torch.cat((s, torch.tensor([0, 1] * 5)))
        a = torch.cat((a, torch.ones(10, dtype=torch.long)))
        reward = torch.cat((reward, -2 * torch.ones(10)))
        nxt = torch.cat((nxt, torch.zeros(10, dtype=torch.long)))
        done = torch.cat((done, torch.ones(10)))
    q = torch.nn.Parameter(torch.tensor([[0., 3.], [0., 3.]]))
    target = q.detach().clone()
    optimizer = torch.optim.Adam([q], lr=.03)
    curve = []
    for step in range(1000):
        y = reward + .9 * (1-done) * target[nxt].max(dim=1).values
        error = .5 * (q[s, a]-y).square().mean()
        penalty = (torch.logsumexp(q[s], dim=1)-q[s, a]).mean()
        loss = error + alpha * penalty
        optimizer.zero_grad(); loss.backward(); optimizer.step()
        if (step+1) % 20 == 0:
            target = q.detach().clone()
            curve.append(q.detach().numpy().copy())
    logits = torch.nn.Parameter(torch.zeros(2, 2))
    opt_bc = torch.optim.Adam([logits], lr=.03)
    for _ in range(300):
        loss = torch.nn.functional.cross_entropy(logits[s], a)
        opt_bc.zero_grad(); loss.backward(); opt_bc.step()
    return q.detach().numpy(), np.array(curve), logits.detach().softmax(1).numpy()


def rollout_table(q, unobserved_reward):
    state, value = 0, 0.
    for t in range(2):
        action = int(np.argmax(q[state]))
        if action == 1:
            return value + .9**t * unobserved_reward
        if state == 1:
            return value + .9**t
        state = 1
    return value


def mpc_plan(A, B, Q, R, P, x, horizon=12, limit=1.):
    # Stack x_1,...,x_H = S x_0 + T [u_0,...,u_(H-1)].
    n = len(x)
    S = np.vstack([np.linalg.matrix_power(A, i+1) for i in range(horizon)])
    T = np.zeros((n*horizon, horizon))
    for i in range(horizon):
        for j in range(i+1):
            T[n*i:n*(i+1), j] = (np.linalg.matrix_power(A, i-j) @ B).ravel()
    weights = block_diag(*([Q]*(horizon-1)+[P]))
    L = np.linalg.cholesky(weights).T
    design = np.vstack((L @ T, np.sqrt(R[0, 0])*np.eye(horizon)))
    rhs = np.r_[-L @ S @ x, np.zeros(horizon)]
    result = lsq_linear(design, rhs, bounds=(-limit, limit), tol=1e-10)
    assert result.success
    return result.x


def control_experiment():
    rng = np.random.default_rng(38)
    dt = .2
    A = np.array([[1., dt], [0., 1.]])
    B = np.array([[.5*dt*dt], [dt]])
    features = rng.uniform([-2., -1., -1.], [2., 1., 1.], size=(200, 3))
    exact = features[:, :2] @ A.T + features[:, 2:] @ B.T
    measured = exact + rng.normal(0., .01, exact.shape)
    fit = np.linalg.lstsq(features[:150], measured[:150], rcond=None)[0].T
    Ah, Bh = fit[:, :2], fit[:, 2:]
    test_error = features[150:] @ fit.T - exact[150:]
    Q, R = np.diag([1., .1]), np.array([[.1]])
    P = solve_discrete_are(A, B, Q, R)
    Ph = solve_discrete_are(Ah, Bh, Q, R)
    K = np.linalg.solve(R+B.T@P@B, B.T@P@A)
    outputs = {}
    initial = np.array([1.5, 0.])
    initial_plan = mpc_plan(A, B, Q, R, P, initial, horizon=40)
    for name in ['Open loop', 'LQR clipped', 'Learned MPC']:
        x = initial.copy(); states = [x.copy()]; actions = []; cost = 0.
        for t in range(40):
            if name == 'Open loop':
                u = initial_plan[t]
            elif name == 'LQR clipped':
                u = float(np.clip((-K@x).item(), -1., 1.))
            else:
                u = mpc_plan(Ah, Bh, Q, R, Ph, x)[0]
            cost += float(x@Q@x + R[0, 0]*u*u)
            x = A@x + B[:, 0]*u
            if t == 14:
                x[1] += .7
            actions.append(u); states.append(x.copy())
        outputs[name] = {'states': np.array(states), 'actions': np.array(actions), 'cost': cost}
    return A, B, Ah, Bh, K, outputs, np.sqrt(np.mean(test_error**2, axis=0))


PAYOFF = np.array([[1., -1.], [-1., 3.]])


def credit_statistics(p=.5, q=.5):
    pa, pb = np.array([1-p, p]), np.array([1-q, q])
    probability = pa[:, None]*pb[None, :]
    baseline = pa @ PAYOFF
    score = np.array([-p, 1-p])[:, None]
    shared = score * PAYOFF
    counterfactual = score * (PAYOFF-baseline[None, :])
    result = []
    for gradient in [shared, counterfactual]:
        mean = float((probability*gradient).sum())
        variance = float((probability*(gradient-mean)**2).sum())
        result.append([mean, variance])
    return np.array(result)


def cooperative_train(seed, counterfactual):
    torch.manual_seed(seed)
    logits = torch.nn.Parameter(torch.zeros(2))
    optimizer = torch.optim.Adam([logits], lr=.04)
    payoff = torch.tensor(PAYOFF, dtype=torch.float32)
    curves = []
    for _ in range(180):
        probs = torch.sigmoid(logits)
        distribution = torch.distributions.Bernoulli(probs=probs)
        actions = distribution.sample((32,)).long()
        rewards = payoff[actions[:, 0], actions[:, 1]]
        advantages = rewards[:, None].expand(-1, 2).clone()
        if counterfactual:
            weights = torch.stack((1-probs, probs), dim=1).detach()
            b0 = (weights[0, :, None]*payoff[:, actions[:, 1]]).sum(0)
            b1 = (weights[1, None, :]*payoff[actions[:, 0], :]).sum(1)
            advantages -= torch.stack((b0, b1), dim=1)
        loss = -(distribution.log_prob(actions.float())*advantages.detach()).sum(1).mean()
        optimizer.zero_grad(); loss.backward(); optimizer.step()
        p, q = torch.sigmoid(logits).detach().numpy()
        expected = np.array([1-p, p]) @ PAYOFF @ np.array([1-q, q])
        curves.append([float(p), float(q), float(expected)])
    return np.array(curves)


def draw(out, language, q_values, control, curves, statistics, model):
    zh = language == 'zh'
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],
                         'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    def save(fig, name):
        fig.savefig(out/f'{name}-{language}.svg', bbox_inches='tight', facecolor='white')
        fig.savefig(out/f'{name}-{language}.png', dpi=155, bbox_inches='tight', facecolor='white')
        plt.close(fig)
    fig = plt.figure(figsize=(12.8, 6.7), layout='constrained')
    grid = fig.add_gridspec(2, 4, height_ratios=[1, .8])
    names = ['离线 Q','CQL α=1','补齐动作后的 Q'] if zh else ['Offline Q','CQL α=1','Q with action coverage']
    for i, (name, q) in enumerate(zip(names, q_values)):
        ax = fig.add_subplot(grid[0, i]); im = ax.imshow(q, vmin=-4, vmax=4, cmap='RdBu')
        for row in range(2):
            for col in range(2):
                ax.text(col, row, f'{q[row,col]:.2f}', ha='center', va='center', color='white' if abs(q[row,col])>2.5 else '#172838')
        ax.set_xticks([0,1],['a0','a1']); ax.set_yticks([0,1],['s0','s1']); ax.set_title(name)
    fig.colorbar(im, ax=fig.axes, shrink=.75, label='Q（折扣奖励）' if zh else 'Q (discounted reward)', ticks=[-4,0,4])
    ax = fig.add_subplot(grid[0, 3]); counts = np.array([[100,0],[100,0]])
    ax.imshow(counts, cmap='Blues',vmin=0,vmax=100)
    for i in range(2):
        for j in range(2): ax.text(j,i,str(counts[i,j]),ha='center',va='center',color='white' if j==0 else '#172838')
    ax.set_xticks([0,1],['a0','a1']);ax.set_yticks([0,1],['s0','s1']);ax.set_title('原始数据次数' if zh else 'Original transition counts')
    ax = fig.add_subplot(grid[1,:]); rows = ['未知动作奖励 −2','未知动作奖励 +2'] if zh else ['Unobserved action reward −2','Unobserved action reward +2']
    values = np.array([[rollout_table(q,-2),rollout_table(q,2)] for q in q_values[:2]]+[[.9,.9]])
    labels = names[:2]+(['行为克隆（贪心）'] if zh else ['Behavior cloning (greedy)'])
    for i in range(3):ax.bar(np.arange(2)+(i-1)*.2, values[i],width=.19,label=labels[i],color=COLORS[i])
    ax.axhline(0,color='#687b88',lw=.7);ax.set_xticks([0,1],rows);ax.set_ylabel('真实折扣回报' if zh else 'True discounted return');ax.legend(ncols=4,loc='lower center',bbox_to_anchor=(.5,1.04),frameon=False)
    save(fig,'offline')
    fig, axes = plt.subplots(3,1,figsize=(12,8.6),layout='constrained',height_ratios=[1.4,1,.8])
    names_zh={'Open loop':'初始计划持续执行','LQR clipped':'限幅 LQR 反馈','Learned MPC':'学习模型 + MPC'}
    for i,(name,result) in enumerate(control.items()):
        label=names_zh[name] if zh else name
        axes[0].plot(np.arange(41)*.2,result['states'][:,0],label=label,color=COLORS[i],lw=2.1)
        axes[1].step(np.arange(40)*.2,result['actions'],where='post',color=COLORS[i],lw=1.7)
    for ax in axes[:2]:ax.axvline(3,color='#c74f48',ls='--',lw=1.2);ax.grid(alpha=.14)
    axes[0].set_ylabel('位置 / m' if zh else 'Position / m');axes[0].legend(ncols=3,frameon=False);axes[0].set_title('3 s 时速度突然增加 0.7 m/s' if zh else 'Velocity impulse +0.7 m/s at t = 3 s')
    axes[1].set_ylabel('加速度 / (m/s²)' if zh else 'Acceleration / (m/s²)');axes[1].axhline(1,ls=':',color='gray');axes[1].axhline(-1,ls=':',color='gray');axes[1].set_xlabel('时间 / s' if zh else 'Time / s')
    names=list(control);costs=[control[n]['cost'] for n in names]
    axes[2].barh(range(3), costs,color=COLORS[:3]);axes[2].set_yticks(range(3),[names_zh[n] if zh else n for n in names]);axes[2].invert_yaxis();axes[2].set_xlabel('40 步累积代价（归一化）' if zh else '40-step accumulated cost (normalized)')
    for i,c in enumerate(costs):axes[2].text(c+.3,i,f'{c:.2f}',va='center')
    axes[2].set_xlim(0,max(costs)*1.15)
    save(fig,'control')
    fig=plt.figure(figsize=(12.4,7.4),layout='constrained');gs=fig.add_gridspec(2,3,height_ratios=[1,1.15])
    ax=fig.add_subplot(gs[0,0]);im=ax.imshow(PAYOFF,cmap='RdBu',vmin=-3,vmax=3)
    for i in range(2):
        for j in range(2):ax.text(j,i,str(int(PAYOFF[i,j])),ha='center',va='center',fontsize=23,color='white' if PAYOFF[i,j]==3 else '#172838')
    ax.set_xticks([0,1],['0','1']);ax.set_yticks([0,1],['0','1']);ax.set_xlabel('智能体 B 动作' if zh else 'Agent B action');ax.set_ylabel('智能体 A 动作' if zh else 'Agent A action');ax.set_title('共同奖励矩阵' if zh else 'Shared reward matrix');fig.colorbar(im,ax=ax,shrink=.8,ticks=[-3,0,3])
    ax=fig.add_subplot(gs[0,1:]);bar_names=['共同奖励','反事实基线'] if zh else ['Shared reward','Counterfactual baseline']
    for i in range(2):ax.bar(np.arange(2)+(i-.5)*.3,statistics[:,i],.28,color=COLORS[i],label=['梯度均值','梯度方差'][i] if zh else ['Gradient mean','Gradient variance'][i])
    ax.set_xticks([0,1],bar_names);ax.set_ylim(0,.9);ax.legend(frameon=False,ncols=2,loc='upper center');ax.set_title('两方均以 0.5 概率选择动作 1' if zh else 'Both agents choose action 1 with probability 0.5');ax.set_ylabel('精确枚举值' if zh else 'Exact enumeration')
    for i in range(2):
        for j in range(2):ax.text(j+(i-.5)*.3,statistics[j,i]+.015,f'{statistics[j,i]:.4f}',ha='center',fontsize=10)
    ax=fig.add_subplot(gs[1,:])
    for i,c in enumerate(curves):
        y=c[:,:,2];ax.plot(np.arange(1,181),y.mean(0),color=COLORS[i],label=bar_names[i]);ax.fill_between(np.arange(1,181),y.min(0),y.max(0),color=COLORS[i],alpha=.17)
    ax.axhline(3,color='gray',ls=':',label='最优共同奖励' if zh else 'Optimal shared reward');ax.set_xlabel('更新次数（每次 32 次同步决策）' if zh else 'Updates (32 simultaneous decisions each)');ax.set_ylabel('策略的精确期望奖励' if zh else 'Exact expected policy reward');ax.legend(ncols=3,frameon=False)
    save(fig,'cooperation')
    fig,axes=plt.subplots(1,2,figsize=(11.8,4.9),layout='constrained')
    A,B,Ah,Bh=model
    true=np.column_stack((A,B));estimated=np.column_stack((Ah,Bh))
    error=estimated-true;lim=np.max(abs(error))
    im=axes[0].imshow(error,cmap='RdBu',vmin=-lim,vmax=lim)
    for i in range(2):
        for j in range(3):axes[0].text(j,i,f'{error[i,j]:+.4f}',ha='center',va='center',color='white' if abs(error[i,j])>.65*lim else '#172838')
    axes[0].set_xticks(range(3),['p','v','u']);axes[0].set_yticks(range(2),['下一步 p','下一步 v'] if zh else ['p next','v next']);axes[0].set_title('归一化模型系数误差' if zh else 'Normalized model-coefficient error');fig.colorbar(im,ax=axes[0],shrink=.8,label='无量纲' if zh else 'Dimensionless')
    for i,(name,result) in enumerate(control.items()):axes[1].plot(result['states'][:,0],result['states'][:,1],color=COLORS[i],label=names_zh[name] if zh else name)
    axes[1].scatter([0],[0],s=70,marker='*',c='#172838');axes[1].set_xlabel('位置 / m' if zh else 'Position / m');axes[1].set_ylabel('速度 / (m/s)' if zh else 'Velocity / (m/s)');axes[1].legend(frameon=False,fontsize=9);axes[1].set_title('同一扰动下的状态轨迹' if zh else 'State trajectories under the same impulse')
    save(fig,'identification')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args()
    out=args.output;out.mkdir(parents=True,exist_ok=True)
    q0,c0,bc=offline_fit(0);qc,cc,_=offline_fit(1);qcov,ccov,_=offline_fit(0,True)
    A,B,Ah,Bh,K,control,error=control_experiment()
    curves=np.array([[cooperative_train(seed,mode)for seed in [38,138,238,338]]for mode in [False,True]])
    statistics=credit_statistics()
    summary={'offline_q':q0.tolist(),'cql_q':qc.tolist(),'covered_q':qcov.tolist(),'bc_probabilities':bc.tolist(),
             'bad_world_returns':[rollout_table(q,-2) for q in [q0,qc,qcov]],'good_world_returns_original_data':[rollout_table(q,2) for q in [q0,qc]],
             'A_true':A.tolist(),'B_true':B.tolist(),'A_fit':Ah.tolist(),'B_fit':Bh.tolist(),'lqr_gain':K.tolist(),'heldout_model_rmse':error.tolist(),
             'control_costs':{k:v['cost']for k,v in control.items()},'max_abs_action':max(float(abs(v['actions']).max())for v in control.values()),
             'credit_mean':statistics[:,0].tolist(),'credit_variance':statistics[:,1].tolist(),'cooperation_final_return':curves[:,:,-1,2].tolist(),
             'one_step_state':(A@np.array([1.,.5])+B[:,0]*-1).tolist(),'discounted_demonstration_return':.9,
             'importance_weight_hand':(.8/.5)*(.6/.3),'is_hand_return':((.8/.5)*(.6/.3)*2+.4*1)/2}
    np.savez(out/'data.npz',offline_q=q0,cql_q=qc,covered_q=qcov,bc=bc,q_curve=c0,cql_curve=cc,covered_curve=ccov,cooperation=curves,
             **{k.replace(' ','_')+'_'+vname:v for k,result in control.items()for vname,v in result.items()})
    np.savez(out/'models.npz',offline_q=q0,cql_q=qc,bc_probabilities=bc,A_fit=Ah,B_fit=Bh,lqr_gain=K)
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    draw(out,args.language,[q0,qc,qcov],control,curves,statistics,(A,B,Ah,Bh))
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

After execution, summary.json provides the values discussed in the text, data.npz retains value-learning curves, state and action trajectories, and every cooperative training seed, and models.npz stores value tables, cloning probabilities, fitted dynamics, and feedback gains for reuse. Useful variations begin with a concrete question. Does adding a few action-1 records remove overestimation? What changes when the identification data cover a narrower acceleration range? How does one learner respond when its partner’s probability is fixed? Changing one information condition at a time makes the resulting figures easier to connect to a mechanism.

When moving to a robotics or multi-agent platform, keep the same sequence: define observations and actions, inspect coverage, specify dynamics and rewards, and choose an evaluation procedure. Recorded experience supports learning before new interaction; predictive models compare possible futures; feedback corrects action after conditions change; and credit assignment gives participants more specific learning signals. Understanding how these components connect makes it possible to assemble a decision system around the task instead of treating the name of one algorithm as the whole solution.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M38.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Conservative Q-Learning for Offline Reinforcement Learning](https://arxiv.org/abs/2006.04779)

   Pages 2–4, equation 4, and implementation appendix: distribution shift and the discrete-action penalty.
2. [imitation: Behavioral Cloning and DAgger](https://imitation.readthedocs.io/en/latest/algorithms/dagger.html)

   Official expert-query and data-aggregation description, alongside the BC supervised-training API.
3. [Minari: Basic Usage](https://minari.farama.org/content/basic_usage/)

   Episode sampling, iterate_episodes, and the dataset-to-loader boundary.
4. [Underactuated Robotics: LQR](https://underactuated.mit.edu/lqr.html)

   Discrete-time Riccati equations, feedback gains, and quadratic costs.
5. [Underactuated Robotics: Trajectory Optimization](https://underactuated.mit.edu/trajopt.html)

   Trajectory optimization formulation and the Model Predictive Control section.
6. [DreamerV3: Mastering Diverse Domains through World Models](https://arxiv.org/abs/2301.04104)

   Abstract describing learned world models and behavior learning in imagination.
7. [Counterfactual Multi-Agent Policy Gradients](https://arxiv.org/html/1705.08926v3)

   Section 4: centralized critics and baselines that marginalize one agent action.
8. [Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments](https://arxiv.org/abs/1706.02275)

   Abstract: non-stationarity and additional agent information during training.
9. [QMIX: Monotonic Value Function Factorisation](https://arxiv.org/abs/1803.11485)

   Abstract: monotonic mixing and decentralized greedy consistency.
10. [PettingZoo: AEC and Parallel API](https://pettingzoo.farama.org/api/parallel/)

    Parallel and AEC action timing, valid actions, and termination handling.
11. [Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World](https://arxiv.org/abs/1703.06907)

    Abstract: visual appearance randomization for object localization.
12. [Empirical Study of Off-Policy Policy Evaluation](https://arxiv.org/abs/1911.06854)

    PDF page 4 method families, page 13 importance ratios, and horizon discussion.
