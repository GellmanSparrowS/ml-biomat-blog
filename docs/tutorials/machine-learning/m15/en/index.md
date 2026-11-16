# Keeping a memory alive: RNN, LSTM, and GRU

Source: https://ml-biomat.com/tutorials/machine-learning/m15/en/
Language: en

Follow states and gradients through a sequence, then open the gates of recurrent memory.

## After reaching the end, do you still remember the beginning?

Consider the sentence “The restaurant looks wonderful, but I will never return.” Reading only its opening gives a misleading impression of the speaker’s attitude. Speech, weather records, and machine vibrations share this dependence on context: an observation often means something different because of what happened earlier. Classifying every time point independently discards order and context. Concatenating an entire record into one fixed vector makes variable lengths awkward. A recurrent neural network addresses both issues by receiving observations one at a time while updating an internal state.

Think of this state as a notebook used while reading. It need not preserve every word, but it must retain clues that matter for the task. New information continually changes the notebook, however. After dozens of irrelevant observations, can a crucial opening detail still determine the answer? We first unfold a recurrent network through time and follow the gradient across its updates. We then examine the gates in LSTM and GRU networks. A deliberately simple experiment tests the resulting mechanisms: a sign appears at the beginning, distractors follow, and the model must report that original sign after reading the sequence.

The task has a useful property: its answer follows directly from the data-generation rule, and the required memory distance can be varied independently. We can compare familiar and longer sequence lengths and inspect the gates of a trained unit without also learning tokenization, language, or speech processing. By the end, you should be able to distinguish cell state from hidden state, explain why teacher forcing changes the decoder’s inputs during training, and choose a one-way, bidirectional, or sequence-to-sequence arrangement according to the information available when a prediction is made.

## One update rule, used repeatedly through time

A basic RNN combines the next input vector with the previous hidden state and transforms them into a new hidden state. Drawing the recurrence as a loop is compact, but can make the computation seem mysterious. Unfolding it reveals an ordinary computational chain. The first step processes the first item; the second processes the next item together with the state left by the first; later steps continue in the same way. Every step uses the same parameters. The network therefore learns a reusable update rule: a longer sequence requires more applications of that rule, rather than a new parameter set for every position.

$$
h_t=\tanh(W_xx_t+W_hh_{t-1}+b)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Time step, a discrete index. |
| ![Formula](https://ml-biomat.com/static/agent-math/6e03ac25e7bc882dc66c0643.svg) | Current input with d features; dimensionless scaled numbers here. |
| ![Formula](https://ml-biomat.com/static/agent-math/85eedc5e4cf9b6744741f60b.svg) | Current and previous hidden states; m is hidden width, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/157ea1323b2c054eafb68cee.svg) | Input and recurrent weight matrices, dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/10da1fa641a861563af1756d.svg) | Bias vector, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/cbf403b7976b754f4c306eac.svg) | Elementwise hyperbolic tangent, mapping each coordinate between −1 and 1. |

Transform the input and old state into the same m-dimensional space, add them with the bias, then apply the nonlinearity. For scalar weights 1 and 0.5, zero bias and initial state, inputs 1 then 0 give states approximately 0.7616 and 0.3634. A batch adds an outer dimension; batch_first=True uses [batch size, sequence length, feature count].

For a hand calculation, make all quantities scalars. Set the input weight to 1, the state weight to 0.5, both the bias and initial state to zero, and the first input to 1. The first state is tanh(1), approximately 0.7616. If the second input is zero, the next state is tanh(0.5 × 0.7616), approximately 0.3634. Information from the first observation survives despite the absence of a new signal, but its magnitude changes. Having a state does not automatically provide lasting memory. In a vector state, different coordinates can carry different features, and the update rule is learned rather than assigned by hand.

The location of the readout determines the task. Sequence classification produces one answer from a complete record, for example whether an audio clip contains a particular event. Sequence labeling produces an answer at every position, as in tagging words by grammatical role. Sequence generation feeds a produced item into later computation. These tasks can share a recurrent cell while using different targets, loss positions, and available information. Define those choices before adding network layers: the final hidden state is a convenient summary for some tasks, while other tasks need the entire state sequence or a different alignment between inputs and outputs.

## Why learning across a long interval is difficult

Backpropagation through time, or BPTT, applies ordinary backpropagation to the unfolded recurrent graph. For an error at the end to affect computation near the beginning, its derivative must pass through many intervening state transformations. To see the central issue, imagine a scalar linear chain in which each update multiplies the previous state by the same number. Repeated multiplication by a number slightly below 1 shrinks a signal; multiplication by a number slightly above 1 enlarges it. A real RNN also contains nonlinear derivatives and matrix directions, but its gradient still contains products across time.

$$
h_t=a h_{t-1},\qquad \frac{\partial h_T}{\partial h_0}=\prod_{t=1}^{T}a=a^T
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/86e707e5d250917043d81b6e.svg) | Current and initial states of a simplified scalar chain, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/349015631ec44ef653936c85.svg) | Fixed state multiplier at every step, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/f9815edca06dc233accaf513.svg) | Current index and total step count, integers; T in the exponent is a count, not a transpose. |
| ![Formula](https://ml-biomat.com/static/agent-math/e1008907cad09e198dabfbc2.svg) | Local rate of change of the final state with respect to the initial state. |
| ![Formula](https://ml-biomat.com/static/agent-math/eddaa20e15661440b4bf8d78.svg) | Product of the local derivatives across time. |

The chain rule multiplies the derivative from each step. The twentieth power of 0.8 is about 0.01153; that of 1.2 is about 38.34. One shrinks a distant signal, the other enlarges it. This expression describes a scalar model without new inputs or nonlinearities. Real RNNs multiply appropriate Jacobian matrices; the plotted chain isolates the multiplication mechanism.

A multiplier of 0.8 becomes approximately 0.0115 after 20 steps, whereas 1.2 becomes approximately 38.34. In the first case, a distant error contributes very little to an early parameter update. In the second, an update can become excessively large. Gradient clipping addresses the latter situation: if the total gradient norm exceeds a threshold, all components are scaled by the same factor, preserving direction while reducing magnitude. Clipping does not reconstruct a signal that has already become tiny. Truncated BPTT controls the length of the computational graph by stopping gradient connections at chosen boundaries; those boundaries also determine how far an error can directly assign credit in that update.

![Two analytically calculated transmission mechanisms. Left: gradient multiplier in a scalar linear chain, on a logarithmic axis. Right: retained state fraction with a fixed forget gate and no new writing. These panels isolate repeated multiplication and the direct cell pathway.](https://ml-biomat.com/static/tutorials/machine-learning/figures/127487d84657ca93f2350ed5.svg?v=127487d84657)

Figure 1Two analytically calculated transmission mechanisms. Left: gradient multiplier in a scalar linear chain, on a logarithmic axis. Right: retained state fraction with a fixed forget gate and no new writing. These panels isolate repeated multiplication and the direct cell pathway.

The LSTM introduced by Hochreiter and Schmidhuber in 1997 was motivated by learning dependencies across long intervals. Later commonly used forms incorporated a forget gate, allowing memory to be actively retained, revised, or cleared. This history explains the architecture’s choices: gates learn how information is written, retained, and read. When reading a cell diagram, find the state pathway that continues through time, then identify the operations that add new information or expose part of the state to the rest of the network. The structure becomes easier to understand when each component answers one of these concrete questions.

## LSTM separates retention, writing, and reading

An LSTM maintains two related states. The cell state carries continuing storage, while the hidden state is the currently visible output passed to other layers. A notebook and the part of it you read aloud provide a useful analogy: a record can remain in the notebook without being fully announced at every moment. The forget gate controls retention of the old record, the input gate controls how much candidate content is written, and the output gate controls how much of the current cell state becomes visible. Each gate is computed from the current input and previous hidden state. Its values vary continuously between zero and one, so the decisions can be trained by differentiation.

$$
\begin{aligned}q_t&=\sigma(W_qx_t+U_qh_{t-1}+b_q),\quad q\in\{f,i,o\}\\g_t&=\tanh(W_gx_t+U_gh_{t-1}+b_g)\\c_t&=f_t\odot c_{t-1}+i_t\odot g_t\\h_t&=o_t\odot\tanh(c_t)\end{aligned}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cbf32d76af4802a50139ab94.svg) | Forget, input, and output gates; each coordinate is between 0 and 1, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/71d6ab9eefc849614ba23b2b.svg) | Indexes three gates with the same form and different parameters. |
| ![Formula](https://ml-biomat.com/static/agent-math/d0fa9a7f586b22317620a37f.svg) | Candidate content, each coordinate between −1 and 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/ce050e1043335673a387a783.svg) | Current and previous cell states; values need not lie between 0 and 1. |
| ![Formula](https://ml-biomat.com/static/agent-math/85eedc5e4cf9b6744741f60b.svg) | Current and previous hidden states, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/6e03ac25e7bc882dc66c0643.svg) | Current d-dimensional input; t is the time index. |
| ![Formula](https://ml-biomat.com/static/agent-math/e343378f53f518c611668c8b.svg) | Input and hidden-state weight matrices, learned separately for each component. |
| ![Formula](https://ml-biomat.com/static/agent-math/20040137dd3a5d5109d96d6f.svg) | Biases; the library’s separate input and recurrent biases sum to these combined biases. |
| ![Formula](https://ml-biomat.com/static/agent-math/8baa8c92c5b738f80358844d.svg) | Sigmoid maps each coordinate to 0–1; ⊙ multiplies matching coordinates. |

Compute gates and candidate content from the input and previous hidden state, then update the cell coordinate by coordinate. For f=0.9, i=0.2, g=−0.5, and old c=0.8, the new cell value is 0.62; o=0.7 gives h≈0.38579. With a fixed forget gate and no writes, the direct pathway multiplies the initial state by f at each step, so 0.99 retains about 0.81791 after 20 steps.

![LSTM information pathways. The upper line carries cell state; gates control retention, writing, and readout. Figure: Aston Zhang, Zachary C. Lipton, Mu Li, and Alexander J. Smola, Dive into Deep Learning, LSTM chapter, CC BY-SA 4.0. Original notation retained.](https://ml-biomat.com/static/tutorials/machine-learning/figures/d8d08daf8f865dfac92385a3.svg?v=d8d08daf8f86)

Figure 2LSTM information pathways. The upper line carries cell state; gates control retention, writing, and readout. Figure: Aston Zhang, Zachary C. Lipton, Mu Li, and Alexander J. Smola, Dive into Deep Learning, LSTM chapter, CC BY-SA 4.0. Original notation retained.

The elementwise multiplications in the diagram matter. A gate value of 0.9 retains ninety percent of the corresponding old-state coordinate. Each state coordinate can use a different gate value, retaining some information more strongly while updating other information faster. Suppose the previous cell state is 0.8, the forget gate is 0.9, the input gate is 0.2, and the candidate content is −0.5. The next cell state is 0.9 × 0.8 + 0.2 × (−0.5) = 0.62. With an output gate of 0.7, the visible hidden state is approximately 0.7 × tanh(0.62) = 0.3858. Retention, revision, and reading are three separate, checkable operations in this example.

The additive cell-state update provides a direct pathway through time. With no new writes and a forget gate fixed at 0.99, approximately 81.8% of an initial value remains after 20 steps. Fixing that gate at 0.9 leaves about 12.2%. This calculation concerns the direct cell pathway with controlled gate values. In a complete network, gates themselves depend on inputs and hidden states, creating additional derivative paths. LSTM supplies a trainable mechanism for long-range transmission; the task and the learned gate values determine what that mechanism actually preserves.

In an implementation, four affine transformations can be computed together and then separated into the input, forget, candidate, and output components. PyTorch stores these components in a documented concatenation order. Our experiment both calls `nn.LSTM` and unpacks its trained weights to recompute every gate and state one step at a time. Comparing that manual computation with the module’s output connects the diagram, mathematical notation, library interface, and actual numerical values. The same exercise is useful when inspecting an unfamiliar architecture: reconstruct a short numerical sequence before interpreting a much larger trained model.

## GRU and records of unequal length

A GRU organizes memory with update and reset gates and keeps a single hidden state, without a separate cell state. In the convention used here, an update gate near one retains more of the previous hidden state; a value near zero favors candidate content. The reset gate controls how much old information contributes when forming that candidate. Cho and colleagues used this gated structure in their 2014 encoder–decoder work. It offers a more compact parameterization of learned retention and revision, with both functions operating on the same state vector.

$$
\begin{aligned}q_t&=\sigma(W_{iq}x_t+b_{iq}+W_{hq}h_{t-1}+b_{hq}),\quad q\in\{r,z\}\\n_t&=\tanh\!\left(W_{in}x_t+b_{in}+r_t\odot(W_{hn}h_{t-1}+b_{hn})\right)\\h_t&=z_t\odot h_{t-1}+(1-z_t)\odot n_t\end{aligned}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/daeea55e3bce10b0e01fed9a.svg) | Reset and update gates, dimensionless; larger z retains more old state in this convention. |
| ![Formula](https://ml-biomat.com/static/agent-math/20763ce29d53551efab2dad5.svg) | Candidate, current, and previous hidden states, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/6e03ac25e7bc882dc66c0643.svg) | Current input; d is feature count and t is time index. |
| ![Formula](https://ml-biomat.com/static/agent-math/af3bd10bd01b7d3e9dff7bb5.svg) | Input weights; subscript i denotes the input branch and q denotes r or z. |
| ![Formula](https://ml-biomat.com/static/agent-math/5cb27e871bec5f048d93edee.svg) | Recurrent weights; subscript h denotes the hidden-state branch. |
| ![Formula](https://ml-biomat.com/static/agent-math/ba36451946e90d34511793eb.svg) | Branch biases, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/88e066a5cc36eb5e43345466.svg) | Sigmoid, hyperbolic tangent, elementwise multiplication, and coordinatewise complementary weight. |

These equations use PyTorch’s reset placement: apply the hidden-branch affine transformation before multiplying by the reset gate. The next state blends the old state and candidate coordinatewise. Values 0.8, −0.5, and z=0.75 give 0.475. The two mixing weights sum to one, but gates depend on inputs and previous states, so the overall update remains nonlinear.

For example, an old state of 0.8, candidate of −0.5, and update gate of 0.75 produce 0.75 × 0.8 + 0.25 × (−0.5) = 0.475. Compare this with the LSTM calculation: the GRU combines retention and replacement directly in one state. Textbooks and libraries sometimes assign the opposite meaning to the update-gate symbol. They can also place the reset operation before or after the hidden-state linear transformation. Our formula follows PyTorch’s placement. Check the actual operations when moving between implementations, because matrix multiplication and elementwise gating generally cannot be interchanged.

Real records rarely have identical lengths. A common batching scheme pads them to the longest length in a batch and stores their valid lengths separately. Padding arranges storage; it does not automatically tell a network that the added positions contain no observations. Selecting the final padded time step may retrieve a state updated through several artificial zeros. A per-position loss can also accidentally score padding as real targets. Packed sequences let recurrent modules respect valid lengths. Alternatively, gather the correct last valid states and apply masks to positionwise losses. For records of lengths 3, 5, and 2, there are ten valid positions, not the fifteen positions occupied after padding.

$$
L=\frac{\sum_{n=1}^{N}\sum_{t=1}^{T_{\max}}m_{nt}\ell_{nt}}{\sum_{n=1}^{N}\sum_{t=1}^{T_{\max}}m_{nt}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f958f17cbefcc4adc6e30dc0.svg) | Loss averaged over valid positions; cross entropy using natural logarithms is measured in nats. |
| ![Formula](https://ml-biomat.com/static/agent-math/26a66e1ac1aef97aededc3dd.svg) | Number of sequences and sequence index in the batch. |
| ![Formula](https://ml-biomat.com/static/agent-math/af6c1eaa3efa8ef9f3aba00b.svg) | Padded maximum length and position index. |
| ![Formula](https://ml-biomat.com/static/agent-math/6868759f6c37deff85b7865b.svg) | Dimensionless mask: 1 at a valid position and 0 at padding. |
| ![Formula](https://ml-biomat.com/static/agent-math/6a9d0be830f91fed383b9b28.svg) | Prediction loss at that position, such as negative log probability of the target symbol. |

The numerator sums errors only at valid positions; the denominator counts them. Lengths 3, 5, and 2 give ten valid positions. If their total loss is 4, the average is 0.4. Dividing by fifteen padded positions would understate the average error per real item. The average requires at least one valid position in the batch.

Stacked recurrent layers pass one layer’s state sequence into the next, increasing the depth of the transformation at each stage. A bidirectional network reads a complete sequence in both directions and combines the two state streams. Both-sided context is available when analyzing a recorded sentence. A real-time alarm or next-step forecast has no future observations at decision time, so its information flow must reflect that timing. Direction, layer count, and sequence length also affect tensor shapes. Initial states and readout code should therefore be checked against the actual layer configuration rather than copied unchanged from a single-layer example.

## Measure memory distance with a controlled experiment

The complete program generates two-channel sequences. In the first channel, the opening value is randomly +1 or −1; later values are independent Gaussian distractors with standard deviation 0.3. The second channel equals one only at the first position, marking the item to remember. The model reports the initial sign after reading the whole record. Training uses 800 sequences of length 16, and validation uses 300 independently generated sequences of that length. Testing uses 500 fresh sequences at each of lengths 8, 16, 32, and 64, allowing the required memory distance to change while the target rule stays fixed.

RNN, LSTM, and GRU each use a hidden width of 16, with the same epoch budget, batch size, and optimizer settings. Each model retains the parameters with its lowest validation loss. Parameter counts are 337, 1,297, and 977 respectively, so the comparison holds hidden width constant. Gates require additional parameters; a different experiment could instead match parameter count or computation time. The program also plots a model’s readout along one 64-step record. This distinguishes the final answer from the point at which the developing state starts to favor a different answer.

### Complete Python: train three recurrent cells and reconstruct LSTM gates

Requires NumPy, Matplotlib, and PyTorch. Run python main.py --output results --language en to generate three SVG figures, summary.json, raw traces, and model parameters. The program uses two CPU threads and fixed seeds, generates training and validation independently, selects parameters by validation loss, and tests four lengths.

```
"""Remember a marked first observation with RNN, LSTM, and GRU.

Synthetic task: the first channel starts with a random sign; subsequent values
are distractors. The second channel marks the first observation. Predict its sign
after the whole sequence. CPU training and all plots are self-contained.
"""
from pathlib import Path
import argparse,copy,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch
from torch import nn


def make_data(n,length,seed):
    rng=np.random.default_rng(seed)
    labels=rng.integers(0,2,n)
    x=np.zeros((n,length,2),dtype=np.float32)
    x[:,:,0]=rng.normal(0,.3,(n,length))
    x[:,0,0]=2*labels-1
    x[:,0,1]=1
    return torch.from_numpy(x),torch.tensor(labels,dtype=torch.float32)


class Remember(nn.Module):
    def __init__(self,kind):
        super().__init__()
        self.recurrent=getattr(nn,kind)(2,16,batch_first=True)
        self.readout=nn.Linear(16,1)
    def forward(self,x):
        output,_=self.recurrent(x)
        return self.readout(output[:,-1,:]).squeeze(-1)


def run(output,language):
    output.mkdir(parents=True,exist_ok=True)
    torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    zh=language=='zh';tr=lambda a,b:a if zh else b
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,
                         'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    train_x,train_y=make_data(800,16,151)
    val_x,val_y=make_data(300,16,152)
    models={};histories={};metrics={};colors={'RNN':'#0072B2','LSTM':'#D58500','GRU':'#008675'}
    lengths=[8,16,32,64]
    for kind in ['RNN','LSTM','GRU']:
        torch.manual_seed(153)
        model=Remember(kind);opt=torch.optim.Adam(model.parameters(),lr=.01)
        criterion=nn.BCEWithLogitsLoss();history=[];best=float('inf');best_state=None;best_epoch=0
        generator=torch.Generator().manual_seed(154)
        for epoch in range(1,81):
            model.train();order=torch.randperm(len(train_x),generator=generator)
            for indices in order.split(100):
                opt.zero_grad(set_to_none=True)
                loss=criterion(model(train_x[indices]),train_y[indices])
                loss.backward();nn.utils.clip_grad_norm_(model.parameters(),max_norm=1.0);opt.step()
            model.eval()
            with torch.no_grad():
                vl=criterion(model(val_x),val_y).item()
                tl=criterion(model(train_x),train_y).item()
            history.append([epoch,tl,vl])
            if vl<best:best=vl;best_epoch=epoch;best_state=copy.deepcopy(model.state_dict())
        model.load_state_dict(best_state);model.eval();models[kind]=model;histories[kind]=np.array(history)
        accuracies=[]
        with torch.no_grad():
            for length in lengths:
                tx,ty=make_data(500,length,160+length)
                accuracies.append(float(((model(tx)>=0)==ty.bool()).float().mean()))
        metrics[kind]={'parameters':sum(p.numel() for p in model.parameters()),'best_epoch':best_epoch,
                       'validation_loss':best,'test_accuracy_by_length':dict(zip(map(str,lengths),accuracies))}
        torch.save(model.state_dict(),output/f'{kind}.pt')

    # Exact single-cell arithmetic with controlled gates, independent of training.
    f,i,o,g,c_prev=.9,.2,.7,-.5,.8
    c=f*c_prev+i*g;h=o*np.tanh(c)
    assert abs(c-.62)<1e-12
    # PyTorch LSTM gate order: input, forget, candidate, output.
    sample,_=make_data(1,16,999)
    cell=models['LSTM'].recurrent;H=torch.zeros(1,16);C=torch.zeros(1,16);trace=[]
    with torch.no_grad():
        for t in range(16):
            pre=sample[:,t]@cell.weight_ih_l0.T+cell.bias_ih_l0+H@cell.weight_hh_l0.T+cell.bias_hh_l0
            ip,fp,gp,op=pre.chunk(4,dim=1)
            I,F,G,O=torch.sigmoid(ip),torch.sigmoid(fp),torch.tanh(gp),torch.sigmoid(op)
            C=F*C+I*G;H=O*torch.tanh(C)
            trace.append(np.stack([F[0].numpy(),I[0].numpy(),O[0].numpy(),C[0].numpy()]))
        full,_=cell(sample)
        manual_error=float(torch.max(torch.abs(full[:,-1,:]-H)))
    assert manual_error<1e-6
    trace=np.stack(trace)
    # Choose the unit with greatest absolute terminal cell value; selection is explicit.
    unit=int(np.argmax(np.abs(trace[-1,3])))
    # Hold the same first signs fixed while reading every prefix of a 64-step set.
    # Removing distractor amplitudes isolates learned state dynamics from noise.
    diagnostic_x,diagnostic_y=make_data(500,64,4242)
    diagnostic_zero=diagnostic_x.clone();diagnostic_zero[:,1:,0]=0
    prefix_diagnostics={}
    with torch.no_grad():
        for kind,model in models.items():
            for condition,dx in [('noise',diagnostic_x),('zero_suffix',diagnostic_zero)]:
                hidden,_=model.recurrent(dx)
                predictions=model.readout(hidden).squeeze(-1)>=0
                accuracy=(predictions==diagnostic_y[:,None].bool()).float().mean(0)
                prefix_diagnostics[f'{kind}_{condition}']=accuracy.numpy().tolist()

    fig=plt.figure(figsize=(12,7),layout='constrained');gs=fig.add_gridspec(2,3)
    ax=fig.add_subplot(gs[0,:2])
    for kind in models:ax.plot(histories[kind][:,0],histories[kind][:,2],color=colors[kind],label=kind)
    ax.set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('验证交叉熵','Validation cross entropy'));ax.legend()
    ax=fig.add_subplot(gs[0,2])
    for kind in models:ax.plot(lengths,[metrics[kind]['test_accuracy_by_length'][str(t)] for t in lengths],'-o',color=colors[kind],label=kind)
    ax.axvline(16,color='#66737a',ls='--',lw=1);ax.axhline(.5,color='#8c989f',ls=':',lw=1)
    ax.set(xticks=lengths,ylim=(0,1.03),xlabel=tr('测试序列长度','Test sequence length'),ylabel=tr('准确率','Accuracy'))
    ax=fig.add_subplot(gs[1,:])
    probe,probe_y=make_data(1,64,999)
    with torch.no_grad():
        for kind,model in models.items():
            hidden,_=model.recurrent(probe)
            prob=torch.sigmoid(model.readout(hidden)).numpy().ravel()
            correct=prob if int(probe_y[0])==1 else 1-prob
            ax.plot(np.arange(1,65),correct,color=colors[kind],label=kind)
    ax.axvline(16,color='#66737a',ls='--',lw=1)
    ax.set(xticks=[1,8,16,32,48,64],ylim=(0,1.03),xlabel=tr('读到的时间步（离散索引）','Observed time steps (discrete index)'),ylabel=tr('真实首项类别的读出概率','Readout probability of the true first class'));ax.legend(ncol=3)
    fig.savefig(output/f'recall-{language}.svg');plt.close(fig)

    fig=plt.figure(figsize=(12,5.4),layout='constrained');gs=fig.add_gridspec(1,2,width_ratios=[1.5,1])
    ax=fig.add_subplot(gs[0,0]);im=ax.imshow(trace[:,:,unit].T,aspect='auto',origin='lower',cmap='viridis',vmin=0,vmax=1)
    # Show gate rows only because cell state is not constrained to [0,1].
    ax.clear();im=ax.imshow(trace[:,:3,unit].T,aspect='auto',origin='lower',cmap='viridis',vmin=0,vmax=1)
    ax.set(yticks=[0,1,2],yticklabels=[tr('遗忘门 f','Forget f'),tr('输入门 i','Input i'),tr('输出门 o','Output o')],
           xticks=[0,3,7,11,15],xticklabels=[1,4,8,12,16],xlabel=tr('时间步','Time step'))
    fig.colorbar(im,ax=ax,label=tr('门值（0–1）','Gate value (0–1)'),shrink=.7)
    ax=fig.add_subplot(gs[0,1]);ax.plot(np.arange(1,17),trace[:,3,unit],'-o',color=colors['LSTM'])
    ax.set(xlabel=tr('时间步','Time step'),ylabel=tr(f'细胞状态（单元{unit}）',f'Cell state (unit {unit})'))
    fig.savefig(output/f'gates-{language}.svg');plt.close(fig)

    fig,axes=plt.subplots(1,2,figsize=(11.5,4.4),layout='constrained')
    steps=np.arange(0,41)
    for gain in [.8,1,1.2]:axes[0].semilogy(steps,gain**steps,label=f'a={gain}')
    axes[0].set(xlabel=tr('跨越步数','Number of steps'),ylabel=tr('简化线性链的梯度倍率','Gradient multiplier in a linear chain'));axes[0].legend()
    for keep in [.5,.9,.99]:axes[1].plot(steps,keep**steps,label=f'f={keep}')
    axes[1].set(xlabel=tr('跨越步数','Number of steps'),ylabel=tr('固定门、无新写入时保留比例','Retained fraction: fixed gate, no new input'));axes[1].legend()
    fig.savefig(output/f'memory-{language}.svg');plt.close(fig)
    fig,ax=plt.subplots(figsize=(12,4.3),layout='constrained')
    keys=list(prefix_diagnostics)
    im=ax.imshow(np.array([prefix_diagnostics[k] for k in keys]),aspect='auto',cmap='viridis',vmin=0,vmax=1)
    labels=[k.replace('_zero_suffix',tr('：后续全零',': zero suffix')).replace('_noise',tr('：有干扰',': distractors')) for k in keys]
    ax.set(yticks=range(6),yticklabels=labels,xticks=[0,7,15,23,31,39,47,55,63],xticklabels=[1,8,16,24,32,40,48,56,64],xlabel=tr('同一组序列的前缀长度','Prefix length of the same sequence set'))
    ax.axvline(15,color='white',ls='--',lw=1)
    fig.colorbar(im,ax=ax,label=tr('500条序列的分类准确率','Classification accuracy over 500 sequences'),shrink=.8)
    fig.savefig(output/f'prefix-{language}.svg');plt.close(fig)
    summary={'train_size':800,'validation_size':300,'test_per_length':500,'training_length':16,
             'epochs':80,'hidden_size':16,'models':metrics,'manual_cell':{'f':f,'i':i,'o':o,'g':g,'c_previous':c_prev,'c':c,'h':float(h)},
             'manual_lstm_vs_module_error':manual_error,'plotted_unit':unit,
             'linear_gradient_20':{'0.8':.8**20,'1.2':1.2**20},'prefix_diagnostics':prefix_diagnostics,'torch_version':torch.__version__}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez(output/'experiment.npz',sample=sample.numpy(),trace=trace,**{f'history_{k}':v for k,v in histories.items()})
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'))
    p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();run(a.output,a.language)
```

![Top: validation loss and accuracy on 500 fresh sequences at each length. The vertical line marks training length 16. Bottom: readout probability of the true opening class along one 64-step record. Hidden width is 16; RNN/LSTM/GRU have 337/1,297/977 parameters. Data follow the stated synthetic task.](https://ml-biomat.com/static/tutorials/machine-learning/figures/aa59467a069b71bf6d08bcaa.svg?v=aa59467a069b)

Figure 3Top: validation loss and accuracy on 500 fresh sequences at each length. The vertical line marks training length 16. Bottom: readout probability of the true opening class along one 64-step record. Hidden width is 16; RNN/LSTM/GRU have 337/1,297/977 parameters. Data follow the stated synthetic task.

Under this fixed configuration, all three models achieve 100% test accuracy at lengths 8 and 16. At length 32, the RNN accuracy is 0%; at length 64, it is 16.2%. LSTM and GRU achieve 100% at both longer lengths. The zero is a computed result, not an omitted point or an alternative way of writing chance performance: predictions have systematically reversed on that test distribution. The lower panel tracks the readout through time, helping relate the final error to state evolution. Behavior beyond the training length can therefore differ sharply from a familiar-length test score.

Interpret these measurements together with the experimental conditions: the useful signal appears only at the beginning, all later values are distractors, training length is fixed at 16, and the gated models have more parameters. The transferable lesson is an experimental design. Vary the interval over which information must survive, keep the target rule explicit, and inspect states and readouts as well as aggregate accuracy. For speech or text, corresponding interventions might increase the distance between related clues, insert irrelevant material, or evaluate separate length groups. These changes provide concrete evidence about which temporal dependencies a model uses.

![Read out every prefix of the same 500 length-64 sequences, seed 4242. Each model is tested with Gaussian distractors and a zero-valued suffix, retaining identical first items and labels. The shared scale is accuracy; the dashed line marks training endpoint 16. Alternating RNN colors show dependence on stopping position.](https://ml-biomat.com/static/tutorials/machine-learning/figures/d7c7f7e72fc8eb1179ce09ca.svg?v=d7c7f7e72fc8)

Figure 4Read out every prefix of the same 500 length-64 sequences, seed 4242. Each model is tested with Gaussian distractors and a zero-valued suffix, retaining identical first items and labels. The shared scale is accuracy; the dashed line marks training endpoint 16. Alternating RNN colors show dependence on stopping position.

A further check holds the same 500 length-64 records fixed and reads out the answer at every prefix. RNN accuracies at steps 15, 16, and 17 are 0%, 100%, and 0%. Replacing all distractors after the opening item with zeros preserves those three results and the repeated changes at longer prefixes. This locates the behavior more precisely: the trained state and readout dynamics depend on the stopping position, rather than following a simple gradual loss of memory. Training requires a correct answer at step 16 without supervising every intermediate readout. Examining prefixes of the same records separates this position dependence from changes in the test examples.

![Gates and cell state of the trained LSTM: unit 1 has the greatest absolute final cell value for the length-16 example generated with seed 999. Gates share a 0–1 color scale; cell state uses its own axis. Values are reconstructed stepwise from saved parameters.](https://ml-biomat.com/static/tutorials/machine-learning/figures/69538b6d14f1a2614cbdac12.svg?v=69538b6d14f1)

Figure 5Gates and cell state of the trained LSTM: unit 1 has the greatest absolute final cell value for the length-16 example generated with seed 999. Gates share a 0–1 color scale; cell state uses its own axis. Values are reconstructed stepwise from saved parameters.

The gate plot selects the unit with the largest absolute final cell state in this example, using the rule stated in the caption. All three gates share a zero-to-one color scale. The cell state has a separate curve because its range is not restricted to that interval. The largest discrepancy between our stepwise reconstruction and `nn.LSTM` is approximately 5.96 × 10⁻⁸, consistent with the numerical precision of this float32 computation. Inspecting one coordinate helps explain the mechanism, while inspecting the full state and readout addresses information distributed across several coordinates.

## From one answer to a sequence of outputs

Classification produces one answer after reading a record. Translation, summarization, and speech transcription produce another sequence, often with a different length. An encoder–decoder connects two processes: the encoder reads the input and forms context, and the decoder predicts successive outputs using that context and preceding output items. Early fixed-vector contexts compressed an entire source into a finite state, increasing the pressure on memory for long inputs. Attention later enabled a decoder to consult multiple source positions as needed. Understanding this bottleneck gives a concrete reason for the architecture introduced in the next chapter.

$$
p(y_{1:T}\mid x)=\prod_{t=1}^{T}p(y_t\mid y_{<t},c(x))
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/fcc5df999e3b49fae1685ee0.svg) | Complete source sequence, whose length may differ from the output length. |
| ![Formula](https://ml-biomat.com/static/agent-math/9969bc836ef1d3ea36f836a1.svg) | Complete output sequence, current item, and preceding prefix; discrete symbols. |
| ![Formula](https://ml-biomat.com/static/agent-math/db8506bdb7f13a6e716f3e71.svg) | Output length and current position, integers. |
| ![Formula](https://ml-biomat.com/static/agent-math/9a51c780ea99335cf8cbecb3.svg) | Context supplied by the encoder, a vector or a sequence of states. |
| ![Formula](https://ml-biomat.com/static/agent-math/8c93668eb0c4447eecb479c8.svg) | Probability, conditioning, and multiplication across steps; probabilities are dimensionless. |

The chain rule of probability factors a joint event into successive conditional events. Conditional probabilities 0.8, 0.7, and 0.9 give a sequence probability of 0.504. Teacher forcing evaluates training probabilities with the true preceding items; free generation uses the items already generated by the model.

During training, correct targets are already available. Feeding the previous correct item to the decoder is called teacher forcing. If the target is “red blue end,” decoder inputs are “start red blue,” while the corresponding labels are “red blue end.” The one-position shift is essential: the current label must not be supplied to the same step that predicts it. During inference, correct future items are unavailable, and the decoder feeds back its own predictions. An early error changes subsequent conditioning inputs. Training loss and the quality of freely generated sequences should therefore both be inspected, since they evaluate the decoder under different preceding contexts.

The organization also applies to continuous values. Forecasting can produce several future real-valued observations and train with regression losses. Speech transcription maps acoustic frames to symbols whose timing differs from the input frames. Text generation begins with a start marker or prompt and repeatedly predicts another token. The output type determines the readout layer, loss, and evaluation measure. Regression error, per-token accuracy, and whole-sequence quality answer different questions. A useful model specification states how much input is available, what output must be produced, and when the decision is required.

## Take control of three gates

This scalar experiment fixes the gates, starts from cell state 0.8, and writes candidate content −0.5 only at the chosen step. Change the forget gate to control retention, the input gate to control the write, and the output gate to zero: the blue memory can remain while the orange readout disappears. The graph follows the cell equations step by step.

[Figure: Cell state and hidden readout through time](https://ml-biomat.com/tutorials/machine-learning/m15/en/#M15-plot)

Blue: cell state c. Orange: hidden state h. Dashed line: writing time. Time is a discrete index and states are dimensionless. Direct retention isolates the fixed forget gate’s effect on the initial content.

## Inspect a new task along its time axis

Begin a new sequence problem by drawing a time axis and marking when observations arrive, when targets become known, and when predictions must be delivered. Establish valid lengths and sampling intervals. Check whether neighboring segments from the same object appear on opposite sides of the training–test split. Forecasting must use information available at prediction time, while analysis of an already recorded clip can legitimately use both directions. These choices give the data split and the architecture a common task definition.

Build an interpretable baseline such as the latest observation, a moving average, or a simple linear state model, then examine what a recurrent network changes. Length groups, error positions, and controlled distractors reveal more about memory than an overall score alone. Save vocabulary, normalization, padding rules, state initialization, and readout conventions with the trained parameters. Processing successive pieces of one continuous record may call for explicitly carrying the state forward. Starting an independent record calls for reinitialization according to the task, so information from the preceding sample does not silently enter the next one.

LSTM and GRU provide learned state management: how information is retained, revised, and exposed to the current output. Attention changes how earlier information is accessed, while state-space models offer another route to efficient sequence dynamics. All can be understood through the same questions developed here: what information is available, how does it travel across time, how does cost grow with sequence length, and which experiment demonstrates that the required dependency is actually used?

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M15.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Dive into Deep Learning — Long Short-Term Memory](https://d2l.ai/chapter_recurrent-modern/lstm.html)

   Architecture, history, and licensed original figure.

   CC BY-SA 4.0 text/figures; code Apache 2.0
2. [Dive into Deep Learning — Gated Recurrent Units](https://d2l.ai/chapter_recurrent-modern/gru.html)

   GRU mechanisms and notation conventions.

   CC BY-SA 4.0
3. [Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078)

   Cho et al., 2014; original gated encoder–decoder research.

   Linked as primary research; no figure copied
4. [PyTorch — LSTM](https://docs.pytorch.org/docs/2.15/generated/torch.nn.LSTM.html)

   Gate ordering, parameters, and state shapes.

   PyTorch documentation; technical reference
5. [PyTorch — GRU](https://docs.pytorch.org/docs/2.15/generated/torch.nn.GRU.html)

   Reset-gate placement used in this chapter.

   PyTorch documentation; technical reference
6. [Dive into Deep Learning — Sequence to Sequence Learning](https://d2l.ai/chapter_recurrent-modern/seq2seq.html)

   Encoder–decoder, padding masks, and teacher forcing.

   CC BY-SA 4.0
