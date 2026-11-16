# Read by content, remember selectively: Transformer and Mamba

Source: https://ml-biomat.com/tutorials/machine-learning/m32/en/
Language: en

From a hand-calculated query to trained attention, selective states, and long-context computation.

## How do you find the record relevant to a question?

Four cards lie on a desk, each containing a name and a number. Asked for the number associated with “Lin,” you first find the name and then read its number, rather than average all four numbers. Understanding a long sentence, connecting image patches, and searching a history of observations all involve related content-dependent reading. A recurrent network compresses the past into an evolving state. Attention lets the current position assign different weights to other positions and read information relevant to the present question.

We organize the chapter around what is read, what is retained, and where computation is spent. A two-key calculation introduces queries, keys, and values. Multiple heads, positions, masks, residuals, and normalization then form a Transformer. We next examine state-space models: how continuous dynamics become a recurrence, and why Mamba makes parts of the update depend on the current input. Two trained experiments expose the mechanisms. A Transformer learns key–value lookup; a selective-state model learns to remember marked values while intervening observations act as distractors.

Explicit task rules make it possible to inspect both answers and internal quantities, including reading weights, step sizes, and states. The models solve different tasks, each chosen to expose its own computational mechanism. Choosing an architecture also involves context length, incremental generation, whether the whole input is available, and the implementation’s memory organization. Connecting those conditions to the structure is more useful than inferring speed or capability from an architecture name alone.

## Queries, keys, and values have different jobs

A query describes what the current position is looking for. A key describes a candidate record for matching. A value contains the information to retrieve from that record. In a contact list, a name helps identify an entry while the telephone number is what you want to take away. Neural networks commonly construct these roles through different linear transformations. The same input vector can be projected into a query, a key, and a value, allowing training to determine which features support matching and which should be transmitted.

$$
Q=X_qW_Q,\qquad K=X_kW_K,\qquad V=X_kW_V
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0a9d9b45cd9e8a8dd4fd42b2.svg) | Query-side and record-side inputs; rows are positions and columns features, encoded or scaled to dimensionless values. |
| ![Formula](https://ml-biomat.com/static/agent-math/1f6c42b12b9575cb1af3a039.svg) | Query count, record count, and input feature width, integers. |
| ![Formula](https://ml-biomat.com/static/agent-math/d51101c07d06ef9d1ddeb5cb.svg) | Learned query/key/value projections; d_k is matching width and d_v is value width. |
| ![Formula](https://ml-biomat.com/static/agent-math/977b500e71ce6d69074802af.svg) | Projected query, key, and value matrices. |

Each input row is multiplied by the projection for its role. Input (1,2) with an identity query projection remains (1,2); a value projection with diagonal (2,0.5) produces (2,1). Self-attention uses the same input on both sides, while cross-attention uses separate sequences. Optional biases are omitted here to isolate the roles; library projections can include them.

A larger query–key dot product indicates greater alignment in the chosen feature coordinates. Dot products depend on feature dimension and scale, so scaled dot-product attention divides by the square root of key dimension. Softmax then converts the scores into nonnegative weights summing to one. The output is their weighted sum of value vectors. Similarity calculation, normalization, and information aggregation are three distinct stages, each reproducible with a few numbers.

$$
S=\frac{QK^\top}{\sqrt{d_k}}+M,\qquad \alpha_{ij}=\frac{e^{S_{ij}}}{\sum_{r=1}^{T_k}e^{S_{ir}}},\qquad O=\alpha V
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4121a43dfe038f5f051b9b6c.svg) | Matching scores and additive mask; allowed entries use zero and blocked entries negative infinity. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77898ba461afcb97a3e7f28.svg) | Transpose of the key matrix and key width; transposition forms all query–key dot products. |
| ![Formula](https://ml-biomat.com/static/agent-math/b80fa4f43252caaf216e9633.svg) | Query-row index, a key index, and the key index summed during normalization. |
| ![Formula](https://ml-biomat.com/static/agent-math/86745df553e3e78b7038595d.svg) | Nonnegative reading weights summing to one for each valid query row, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/91b7cd3dd14a1a81bca61eb0.svg) | Retrieved output and value matrix; output retains the value feature width. |
| ![Formula](https://ml-biomat.com/static/agent-math/abaa4fa6da9379e7ead98f05.svg) | Natural-exponential base and square-root dimension scaling; scores are dimensionless here. |

For approximately independent query/key coordinates of unit variance, dot-product variance grows with d_k; square-root scaling helps control score magnitude. Scores (1/√2,0) give weights (0.66976155,0.33023845); values (2,0),(0,4) then give (1.33952310,1.32095380). Subtracting each row’s largest score before exponentiation preserves the normalized result and improves numerical stability.

![Analytic two-key example: scaled scores, softmax weights, and the weighted sum of two-dimensional value vectors. The green arrow is the output; blue and orange arrows are values. Every quantity is computed from the stated inputs.](https://ml-biomat.com/static/tutorials/machine-learning/figures/307f3a6fa0cf9323b7992a51.svg?v=307f3a6fa0cf)

Figure 1Analytic two-key example: scaled scores, softmax weights, and the weighted sum of two-dimensional value vectors. The green arrow is the output; blue and orange arrows are values. Every quantity is computed from the stated inputs.

Take query (1,0), keys (1,0) and (0,1), and key dimension two. Scaled scores are approximately 0.7071 and zero, producing softmax weights 0.66976 and 0.33024. If the values are (2,0) and (0,4), the weighted output is approximately (1.33952,1.32095). The operation neither selects one value outright nor returns the similarity score. It translates matching strength into proportions for reading the stored content.

Self-attention constructs queries, keys, and values from the same sequence, supporting communication within that sequence. Cross-attention takes queries from one side and keys and values from another. During translation, for example, a target position can query representations supplied by the source encoder. The numbers of queries and keys can differ, giving a rectangular attention matrix. Identify where each piece of information comes from before interpreting shapes, and the difference between these arrangements becomes straightforward.

## Several reading views, with explicit information boundaries

One set of reading weights may not express all useful relationships. Multi-head attention learns several projections, performs matching and aggregation in their separate subspaces, then concatenates and projects the results back to the model width. Think of several ways of reading the same material: one might emphasize nearby relationships, another a content feature. The roles of trained heads emerge from learning; assigning grammatical or semantic labels to them before examining their behavior would skip the experiment needed to establish those roles.

$$
\operatorname{MHA}(X)=\operatorname{Concat}(O^{(1)},\ldots,O^{(H)})W_O
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9d6bf175b0b3d7c88137cd57.svg) | Number of attention heads and a head index, integers. |
| ![Formula](https://ml-biomat.com/static/agent-math/42d7a82f5a83ad83892f4fab.svg) | Retrieved result of head h from the preceding equation; superscript indexes the head. |
| ![Formula](https://ml-biomat.com/static/agent-math/be6eccd644d3a07b523f251f.svg) | Concatenation along features, producing shape T×(H d_v). |
| ![Formula](https://ml-biomat.com/static/agent-math/ff255aafe46114917e14e8ee.svg) | Output projection restoring model width d. |
| ![Formula](https://ml-biomat.com/static/agent-math/d9aafadb2337f86876fc8070.svg) | Input representation, length, model width, and multi-head attention operation; values are dimensionless. |

The example uses four heads at model width 32, with key and value width 8 per head. Four 8-dimensional outputs concatenate to 32 dimensions before a 32×32 output projection. Distinct learned projections allow different reading weights; concatenation retains their coordinates for the output projection to combine.

A mask specifies which connections are available for the task. An autoregressive model predicting early items has not yet observed later ones, so a causal mask blocks future positions. A padding mask excludes artificial positions added to equalize batch lengths. A common implementation assigns negative infinity to blocked scores before softmax, making their weights zero. Blocking every candidate in a row leaves normalization without a valid object to read. Data and masks should therefore provide at least one usable candidate for every position whose output is required.

Boolean-mask conventions vary by interface. The `nn.MultiheadAttention` used here treats True as blocked. Our program creates six input positions, changes the last three, and checks the first three outputs under a causal mask: their maximum change is zero. This intervention directly tests the intended information restriction. In next-token training, inputs and targets must also be shifted correctly. The mask and the label alignment jointly define the prediction problem.

Attention computes relationships among vectors without automatically knowing their order. Positional representations supply that information. They can be learned vectors or predetermined sine and cosine functions spanning different positional scales. Rotary positional encoding rotates feature pairs by position so query–key dot products carry relative-position information. Our small model simply adds five learned position vectors to its projected inputs, making the point where position enters the computation explicit. Swapping two records then changes which content is combined with each position vector.

## Combine reading, local processing, and direct paths

A Transformer layer contains more than attention. Attention exchanges information among positions. A positionwise feed-forward network applies a nonlinear feature transformation at each position, sharing its parameters across the sequence. Residual connections add the input back to a sublayer’s output, while LayerNorm controls feature scale within each position. The sublayers therefore have different jobs: retrieve information from other locations, process the resulting local representation, then repeat.

$$
U=X+\operatorname{MHA}(\operatorname{LN}_1(X)),\qquad Y=U+\operatorname{FFN}(\operatorname{LN}_2(U))
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/38f8e1d574419bbd047a3717.svg) | Layer input, intermediate representation, and output, all shape T×d; a batch adds an outer dimension. |
| ![Formula](https://ml-biomat.com/static/agent-math/ff86c7f353952f4d5c710806.svg) | LayerNorm across features at each position, with separately learned parameters. |
| ![Formula](https://ml-biomat.com/static/agent-math/917a676254468d25a9d8aefc.svg) | Multi-head reading across positions. |
| ![Formula](https://ml-biomat.com/static/agent-math/7c72d18fd01e238477b7cb66.svg) | Positionwise shared feed-forward network;32→64→32 with GELU in this example. |

Both residual additions require matching widths. At one position, input(0.2,0.4) plus first-sublayer output(0.1,−0.2) gives U=(0.3,0.2). Adding second-sublayer output(0.02,0.03) gives Y=(0.32,0.23). This is pre-normalization; the reproduced architecture diagram uses normalization after addition. Follow the order of each design.

![Encoder–decoder Transformer organization. Follow source and target pathways, including causal self-attention and cross-attention in the decoder. Figure: Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola, Dive into Deep Learning, Fig.11.7.1, CC BY-SA4.0, unchanged. Diagram: post-normalization; example code: pre-normalization.](https://ml-biomat.com/static/tutorials/machine-learning/figures/c1a346517b50a336116af6b5.svg?v=c1a346517b50)

Figure 2Encoder–decoder Transformer organization. Follow source and target pathways, including causal self-attention and cross-attention in the decoder. Figure: Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola, Dive into Deep Learning, Fig.11.7.1, CC BY-SA4.0, unchanged. Diagram: post-normalization; example code: pre-normalization.

The diagram presents the encoder–decoder arrangement associated with the original 2017 Transformer. An encoder can read across a complete source sequence and form its representations. The decoder uses causal self-attention and cross-attention to those encoder outputs. Encoder-only models suit tasks requiring representations or classification of a complete input; causal decoder-only models support successive generation. These names describe information flow and sublayer organization rather than assigning each architecture to only one application.

Normalization placement has several conventions. The reproduced diagram normalizes after residual addition. Our code normalizes before passing a representation into each sublayer, then applies a final normalization at the end. Follow the actual operation order when reading an implementation. In the small two-layer Transformer, every layer has four heads, model width 32, and feed-forward hidden width 64. Attention and feed-forward outputs both return to width 32, making addition with their residual inputs shape-consistent.

A token need not be a natural-language word. Text may use subword identifiers and an embedding table. Images can be split into flattened, projected patches. A continuous sensor record can project the features at one time point into the model width. All provide a sequence of vectors, but their sampling intervals, position meanings, and available context differ. Each card in our experiment becomes a nine-dimensional vector: four key indicators, four value indicators, and one query flag. Five cards make one short sequence.

## Another route: maintain a state that evolves with input

Revisiting the entire history whenever a new observation arrives gives an increasingly large set of objects to read. A state-space model instead summarizes the past in a state, updates it with the new input, and reads an output from that state. The idea has long been used to describe dynamic systems. The temperature of a container, for example, reflects current heating and previously accumulated heat. Separating internal evolution from observed output makes the state an intermediary between past and present.

$$
\frac{dh(\tau)}{d\tau}=Ah(\tau)+Bx(\tau),\qquad y(\tau)=Ch(\tau)+Dx(\tau)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3c5718e2fe3ba865d1d37f34.svg) | Continuous time and N-dimensional internal state; time uses model-defined units and states are dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/0a00dcb6659783089cd167c8.svg) | Scalar input and output of this simplified system, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/bb28ee8729a7fb3a1da437ba.svg) | State-evolution and input-drive coefficients, with inverse-time dimensions. |
| ![Formula](https://ml-biomat.com/static/agent-math/c37fb19f512eb0eb645bd7a8.svg) | State-readout coefficients and direct input coefficient, dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/dc6e3fa635830d5dca115967.svg) | State rate of change with continuous time. |

B drives the state with input, A governs its own evolution, C reads the state, and D permits a direct input contribution. For scalar A=−1,B=1,C=1,D=0, state 0.8 and input −0.5 produce instantaneous rate −1.3 per time unit. A rate is not the next state; integrate over the chosen interval.

A continuous equation must become a discrete update for computation. Consider a scalar state that decays in proportion to its current value while input drives it. If input stays constant over one interval, the retained fraction and the input contribution can be integrated exactly. With decay rate −1, input coefficient one, and interval ln2, half the old state remains and half the current input is added. Previous state 0.8 and input −0.5 then give 0.15. This calculation connects continuous dynamics, sampling interval, and recurrence coefficients.

$$
h_t=e^{a\Delta}h_{t-1}+\frac{e^{a\Delta}-1}{a}\,b x_t\quad(a\ne0)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6d3079853305e3d7d1266f42.svg) | Scalar states at the end and start of a discrete interval. |
| ![Formula](https://ml-biomat.com/static/agent-math/689da198c2dfc062dc6a4362.svg) | Scalar state rate and input coefficient, with inverse-time dimensions. |
| ![Formula](https://ml-biomat.com/static/agent-math/101bc29506fa7eee5de512cf.svg) | Positive interval duration and discrete step index. |
| ![Formula](https://ml-biomat.com/static/agent-math/f8abeca1e21f2ff4458a26ea.svg) | Scalar input held constant over the interval, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/9a6477ba1148f635d5b79627.svg) | Dimensionless old-state multiplier and integrated input coefficient. |

Solving the linear differential equation with constant input gives this exact update. For a=−1,b=1,Δ=ln2, both coefficients are0.5, so state 0.8 and input −0.5 give 0.15. As a approaches zero, the input coefficient approaches bΔ, providing the zero-rate limit.

When transition, writing, and reading rules do not change over time, the system is linear and time invariant. Expanding its recurrence shows earlier inputs adding to the current output with different decay weights; the input–output mapping can also be expressed as a sequence convolution. Such structure naturally represents a fixed dynamic response. Remembering selected content while skipping distractors calls for an update rule that can respond to what arrives. This returns us to the content-selection problem at the beginning of the chapter.

State dimension supplies internal storage coordinates, and decay rates provide different retention timescales. Structured transition matrices make larger states computationally manageable. A diagonal transition lets coordinates decay at separate rates, while input and output projections combine them. This shares the recurrence idea of a scalar moving average, but multiple timescales and learned projections create a richer representation. The distinction between state dimension and the number of visible input features matters when reading an implementation.

## Selective states let content shape the update

Mamba, introduced by Gu and Dao in 2023, makes some state-space parameters functions of the current input. The state pathway can consequently use different retention and writing behavior for different content: a marked observation can trigger an update, while a distractor can leave more previous information intact. Input-dependent step size, writing coefficients, and reading coefficients provide this selectivity. Once those quantities depend on content, the overall computation is no longer a fixed-kernel linear convolution.

$$
\begin{aligned}\Delta_t&=\operatorname{softplus}(W_\Delta u_t+b_\Delta),\quad B_t=W_Bu_t,\quad C_t=W_Cu_t\\h_{t,d,n}&=e^{\Delta_{t,d}A_{d,n}}h_{t-1,d,n}+\Delta_{t,d}B_{t,n}u_{t,d}\\r_{t,d}&=\sum_{n=1}^{N}C_{t,n}h_{t,d,n}+D_du_{t,d}\\\widehat y_t&=w^\top\bigl(r_t\odot\operatorname{SiLU}(z_t)\bigr)+b\end{aligned}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a5625d1805920ff4c88bdfe6.svg) | Internal input and output-gating branch, computed from current and causal local inputs; D_c=24. |
| ![Formula](https://ml-biomat.com/static/agent-math/81b6682fe1ae279c3c2db014.svg) | Positive channelwise steps; softplus is log(1+exp(v)), implemented stably. |
| ![Formula](https://ml-biomat.com/static/agent-math/097f23240656e0a867b67f4a.svg) | Learned input-to-step projection and bias. |
| ![Formula](https://ml-biomat.com/static/agent-math/9f0713f1222e82c96ccfea98.svg) | Input-dependent write/read projections; N=4, with these N-dimensional coefficients shared across internal channels at each time. |
| ![Formula](https://ml-biomat.com/static/agent-math/39ac8b0cf04d2c77169a6e71.svg) | Negative transition rates and state; code parameterizes rates as negative exponentials and initializes state to zero. |
| ![Formula](https://ml-biomat.com/static/agent-math/76a6dc77e0a5431e539a549a.svg) | Time, internal-channel, and state-coordinate indices; D_d is a direct coefficient and r_t the readout channel vector. |
| ![Formula](https://ml-biomat.com/static/agent-math/a62ffa9a018e73196692c19b.svg) | Final linear readout weights, bias, scalar prediction, and elementwise multiplication. |
| ![Formula](https://ml-biomat.com/static/agent-math/2650f19e6d80d3aec856bd07.svg) | Smooth gating activation with sigmoid σ; inputs, states, and model time use normalized numerical units here. |

For one coordinate A=−1,Δ=0.2,old h=0.8,B=0.5,u=−1, the next state is exp(−0.2)×0.8−0.1≈0.554985. The state transition is exponential while the input term is ΔBu, different from the preceding exact integrated input coefficient. Input-dependent B,C,andΔ support content-dependent updates. The scan state has shape batch size×24×4.

Our CPU model retains that central computation. An input projection splits into two branches. One passes through a short causal depthwise convolution and SiLU; the other gates the eventual output. The current representation generates positive step sizes and input-dependent write and read coefficients. Each internal channel has four state coordinates. Negative transition rates ensure that positive steps produce old-state multipliers between zero and one. The program uses exponential state transitions and a step-size-times-input writing term, with every time step visible in the ordinary Python loop.

Distinguish the exact continuous-system discretization from the writing approximation used by this implementation. The preceding scalar calculation integrates a constant input’s contribution over the whole interval. The selective scan here uses step size multiplied by the writing coefficient. Both preserve the organization of transmitted old state plus new information, while their input terms follow different numerical rules. Matching the formula to the code explains why changing step size affects both forgetting and writing.

Mamba also addresses how scanning executes on hardware. Once per-step coefficients are available, two affine state updates can be combined into one, and this composition is associative. That property permits parallel scan algorithms. Optimized implementations additionally organize memory access and fuse operations. Our explicit CPU loop makes the numerical mechanism inspectable and retains states needed for backpropagation. For a new observation at inference time, the recurrence can update an existing state without keeping a full historical attention matrix.

## Train content-based retrieval and selective memory

The first task contains four key–value records followed by a query. Each of four keys appears exactly once; values are independently selected from four categories. The query identifies one key, and the target is its value. Training, validation, and testing contain 1,000, 300, and 400 independently generated sequences. A two-layer Transformer trains for fifty epochs and selects parameters by validation cross entropy. A query-blind rule that returns the most frequent stored value provides a reference for solving the task without using the requested key.

The second task supplies sixteen values and their markers. Values are uniform between −1 and one. The first position is always marked; later positions are independently marked with probability 0.2. At every step, the target is the value at the most recent marked position. The selective model uses 800 training, 240 validation, and 320 test sequences, training for seventy epochs with a positionwise squared-error objective. The two experiments use different targets and losses, with their sample counts and generation seeds kept explicit.

### Complete Python: content retrieval and selective-state scanning

Requires NumPy, Matplotlib, and PyTorch. Run python main.py --output results --language en to train two small models and generate five SVG figures, parameters, summary.json, and raw traces. Uses two CPU threads and no large weight download. The selective core explicitly implements causal convolution, input-dependent steps/write/read coefficients, and output gating.

```
"""Attention retrieval and a CPU selective state-space teaching model.

The selective recurrence follows the mathematical form documented by Gu & Dao
and the state-spaces/mamba reference implementation. This compact implementation
uses ordinary PyTorch operations so each state is inspectable on CPU.
"""
from pathlib import Path
import argparse,copy,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch
from torch import nn

def retrieval_data(n,seed):
    rng=np.random.default_rng(seed);x=np.zeros((n,5,9),dtype=np.float32);target=np.zeros(n,dtype=np.int64);slots=[]
    for b in range(n):
        keys=rng.permutation(4);values=rng.integers(0,4,4);chosen=int(rng.integers(4))
        for t,(key,value) in enumerate(zip(keys,values)):x[b,t,key]=1;x[b,t,4+value]=1
        x[b,4,keys[chosen]]=1;x[b,4,8]=1;target[b]=values[chosen];slots.append(chosen)
    return torch.tensor(x),torch.tensor(target),np.array(slots)

class AttentionBlock(nn.Module):
    def __init__(self):
        super().__init__();self.norm1=nn.LayerNorm(32);self.attention=nn.MultiheadAttention(32,4,batch_first=True,dropout=0)
        self.norm2=nn.LayerNorm(32);self.ff=nn.Sequential(nn.Linear(32,64),nn.GELU(),nn.Linear(64,32))
    def forward(self,x,mask=None,weights=False):
        z=self.norm1(x);a,w=self.attention(z,z,z,attn_mask=mask,need_weights=weights,average_attn_weights=False)
        x=x+a;return x+self.ff(self.norm2(x)),w

class TinyTransformer(nn.Module):
    def __init__(self):
        super().__init__();self.embed=nn.Linear(9,32);self.position=nn.Parameter(torch.randn(1,5,32)*.02)
        self.blocks=nn.ModuleList([AttentionBlock(),AttentionBlock()]);self.norm=nn.LayerNorm(32);self.head=nn.Linear(32,4)
    def forward(self,x,weights=False):
        x=self.embed(x)+self.position;all_weights=[]
        for block in self.blocks:x,w=block(x,weights=weights);all_weights.append(w)
        logits=self.head(self.norm(x[:,-1]));return (logits,all_weights) if weights else logits

def memory_data(n,seed,length=16):
    rng=np.random.default_rng(seed);values=rng.uniform(-1,1,(n,length));marks=rng.random((n,length))<.2;marks[:,0]=True
    targets=np.zeros_like(values);last=np.zeros(n)
    for t in range(length):last=np.where(marks[:,t],values[:,t],last);targets[:,t]=last
    x=np.stack([values,marks],-1).astype('float32');return torch.tensor(x),torch.tensor(targets,dtype=torch.float32)

class SelectiveMemory(nn.Module):
    def __init__(self,width=24,state_size=4):
        super().__init__();self.width=width;self.state_size=state_size
        self.input=nn.Linear(2,2*width);self.local=nn.Conv1d(width,width,3,padding=2,groups=width)
        self.delta=nn.Linear(width,width);nn.init.constant_(self.delta.bias,-2)
        self.B=nn.Linear(width,state_size,bias=False);self.C=nn.Linear(width,state_size,bias=False)
        self.log_rates=nn.Parameter(torch.log(torch.arange(1,state_size+1,dtype=torch.float32)).repeat(width,1))
        self.direct=nn.Parameter(torch.ones(width));self.readout=nn.Linear(width,1)
    def forward(self,x,trace=False):
        u,z=self.input(x).chunk(2,-1);length=x.shape[1]
        u=nn.functional.silu(self.local(u.transpose(1,2))[...,:length].transpose(1,2))
        dt=nn.functional.softplus(self.delta(u));B=self.B(u);C=self.C(u);A=-torch.exp(self.log_rates)
        h=x.new_zeros(x.shape[0],self.width,self.state_size);outputs=[];states=[]
        for t in range(length):
            decay=torch.exp(dt[:,t,:,None]*A[None])
            write=dt[:,t,:,None]*B[:,t,None,:]*u[:,t,:,None]
            h=decay*h+write
            y=(h*C[:,t,None,:]).sum(-1)+self.direct*u[:,t]
            outputs.append(self.readout(y*nn.functional.silu(z[:,t])).squeeze(-1))
            if trace:states.append(h)
        result=torch.stack(outputs,1)
        return (result,dt,torch.stack(states,1)) if trace else result

def fit(model,train_x,train_y,val_x,val_y,classification,epochs,seed):
    optimizer=torch.optim.Adam(model.parameters(),lr=.003);generator=torch.Generator().manual_seed(seed)
    criterion=nn.CrossEntropyLoss() if classification else nn.MSELoss();history=[];best=float('inf');saved=None;best_epoch=0
    for epoch in range(1,epochs+1):
        model.train()
        for ix in torch.randperm(len(train_x),generator=generator).split(64):
            optimizer.zero_grad(set_to_none=True);loss=criterion(model(train_x[ix]),train_y[ix]);loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(),1.0);optimizer.step()
        model.eval()
        with torch.no_grad():tl=float(criterion(model(train_x),train_y));vl=float(criterion(model(val_x),val_y))
        history.append([epoch,tl,vl])
        if vl<best:best=vl;best_epoch=epoch;saved=copy.deepcopy(model.state_dict())
    model.load_state_dict(saved);model.eval();return np.array(history),best_epoch

def run(output,language):
    output.mkdir(parents=True,exist_ok=True);torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    zh=language=='zh';tr=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    tx,ty,_=retrieval_data(1000,320);vx,vy,_=retrieval_data(300,321);ex,ey,slots=retrieval_data(400,322)
    torch.manual_seed(323);transformer=TinyTransformer();attention_history,attention_best=fit(transformer,tx,ty,vx,vy,True,50,324)
    with torch.no_grad():logits,weights=transformer(ex,weights=True);accuracy=float((logits.argmax(-1)==ey).float().mean())
    query_blind=ex[:,:4,4:8].sum(1).argmax(-1);baseline=float((query_blind==ey).float().mean())
    mx,my=memory_data(800,325);mv,mvy=memory_data(240,326);me,mey=memory_data(320,327)
    torch.manual_seed(328);selective=SelectiveMemory();memory_history,memory_best=fit(selective,mx,my,mv,mvy,False,70,329)
    with torch.no_grad():memory_pred,dt,states=selective(me,trace=True)
    memory_mse=float(nn.functional.mse_loss(memory_pred,mey));last_mse=float(nn.functional.mse_loss(memory_pred[:,-1],mey[:,-1]))
    torch.save(transformer.state_dict(),output/'transformer.pt');torch.save(selective.state_dict(),output/'selective-memory.pt')
    # Exact QKV example; compare direct calculation with the library operation.
    q=torch.tensor([[1.,0.]],dtype=torch.float64);k=torch.eye(2,dtype=torch.float64);v=torch.tensor([[2.,0.],[0.,4.]],dtype=torch.float64)
    scores=q@k.T/math.sqrt(2);alpha=torch.softmax(scores,dim=-1);manual=alpha@v
    official=nn.functional.scaled_dot_product_attention(q[None,None],k[None,None],v[None,None])[0,0]
    qkv_error=float((manual-official).abs().max());assert qkv_error<1e-12
    # Changing future tokens cannot change earlier outputs under a causal mask.
    torch.manual_seed(330);block=AttentionBlock().eval();sequence=torch.randn(1,6,32);changed=sequence.clone();changed[:,3:]+=10*torch.randn(1,3,32)
    mask=torch.triu(torch.ones(6,6,dtype=torch.bool),diagonal=1)
    with torch.no_grad():a,_=block(sequence,mask);b,_=block(changed,mask);causal_error=float((a[:,:3]-b[:,:3]).abs().max())
    assert causal_error<1e-6
    # A diagonal scan independently evaluated in two equivalent arrangements.
    A=np.array([-.5,-1.]);deltas=np.array([.1,.2,.05]);inputs=np.array([1.,-2.,.3]);B=np.array([.6,-.4]);h=np.zeros(2);trace=[]
    for delta,value in zip(deltas,inputs):h=np.exp(delta*A)*h+delta*B*value;trace.append(h.copy())
    # Expanded closed form: each earlier write is multiplied by later decays.
    expanded=sum(deltas[t]*B*inputs[t]*np.exp(A*deltas[t+1:].sum()) for t in range(3))
    scan_error=float(np.abs(h-expanded).max());assert scan_error<1e-12

    fig=plt.figure(figsize=(12,4.3),layout='constrained');gs=fig.add_gridspec(1,3,width_ratios=[1,1,1.3])
    ax=fig.add_subplot(gs[0,0]);ax.bar([0,1],scores.numpy().ravel(),color=['#0072B2','#D58500']);ax.set(xticks=[0,1],xticklabels=['K1','K2'],ylabel=tr('缩放点积分数','Scaled dot-product score'))
    ax=fig.add_subplot(gs[0,1]);ax.bar([0,1],alpha.numpy().ravel(),color=['#0072B2','#D58500']);ax.set(xticks=[0,1],xticklabels=['K1','K2'],ylim=(0,1),ylabel=tr('归一化读取权重','Normalized reading weight'))
    ax=fig.add_subplot(gs[0,2]);ax.arrow(0,0,2,0,color='#0072B2',width=.025,length_includes_head=True);ax.arrow(0,0,0,4,color='#D58500',width=.025,length_includes_head=True);ax.arrow(0,0,float(manual[0,0]),float(manual[0,1]),color='#008675',width=.035,length_includes_head=True)
    ax.text(2,.2,'V1');ax.text(.1,3.8,'V2');ax.text(float(manual[0,0]),float(manual[0,1])+.15,tr('加权输出','Weighted output'));ax.set(xlim=(-.2,2.8),ylim=(-.2,4.3),xlabel=tr('特征维1','Feature dimension1'),ylabel=tr('特征维2','Feature dimension2'))
    fig.savefig(output/f'qkv-{language}.svg');plt.close(fig)
    # Actual second-layer head maps for the first held-out retrieval example.
    retrieval_sample=next(i for i in range(len(ex)) if len(set(ex[i,:4,4:8].argmax(1).tolist()))==4)
    head_maps=weights[-1][retrieval_sample].numpy();key_ids=ex[retrieval_sample,:4,:4].argmax(1).numpy();value_ids=ex[retrieval_sample,:4,4:8].argmax(1).numpy();query=int(ex[retrieval_sample,4,:4].argmax())
    labels=[f'K{k}:V{v}' for k,v in zip(key_ids,value_ids)]+[f'Q:K{query}']
    fig,axes=plt.subplots(1,4,figsize=(13,3.8),layout='constrained')
    for j,ax in enumerate(axes):
        im=ax.imshow(head_maps[j],vmin=0,vmax=1,cmap='viridis');ax.set(xticks=range(5),xticklabels=labels,yticks=range(5),yticklabels=labels,title=tr(f'头{j}',f'Head{j}'))
        ax.tick_params(axis='x',labelrotation=55);ax.add_patch(plt.Rectangle((-.5,3.5),5,1,fill=False,edgecolor='#D58500',lw=2))
    fig.colorbar(im,ax=list(axes),shrink=.6,label=tr('注意力权重','Attention weight'));fig.savefig(output/f'attention-{language}.svg');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11.5,4.3),layout='constrained')
    for ax,history,title in [(axes[0],attention_history,tr('键值检索：Transformer','Key-value retrieval: Transformer')),(axes[1],memory_history,tr('最近标记值：选择性状态','Last marked value: selective state'))]:
        ax.semilogy(history[:,0],history[:,1],label=tr('训练','Training'),color='#0072B2');ax.semilogy(history[:,0],history[:,2],label=tr('验证','Validation'),color='#D58500');ax.set(title=title,xlabel=tr('训练轮数','Epoch'),ylabel=tr('交叉熵' if ax is axes[0] else '均方误差','Cross entropy' if ax is axes[0] else 'MSE'));ax.legend()
    fig.savefig(output/f'learning-{language}.svg');plt.close(fig)
    # Inspect a learned memory trajectory, not a manually prescribed gate plot.
    sample=0;time=np.arange(1,17);marked=np.flatnonzero(me[sample,:,1].numpy())
    fig=plt.figure(figsize=(12,6.3),layout='constrained');gs=fig.add_gridspec(2,2,width_ratios=[1.6,1])
    ax=fig.add_subplot(gs[0,:]);ax.plot(time,me[sample,:,0],'.-',color='#9aa5ab',label=tr('当前输入值','Current input value'));ax.step(time,mey[sample],where='post',color='#273e47',lw=2,label=tr('最近标记值目标','Last-marked-value target'));ax.plot(time,memory_pred[sample],'o-',color='#0072B2',ms=4,label=tr('模型读出','Model readout'));ax.scatter(time[marked],me[sample,marked,0],s=90,facecolors='none',edgecolors='#D58500',linewidths=2,label=tr('有标记的输入','Marked inputs'));ax.set(xlabel=tr('时间步','Time step'),ylabel=tr('数值（无量纲）','Value (dimensionless)'));ax.legend(ncol=2,fontsize=9)
    ax=fig.add_subplot(gs[1,0]);im=ax.imshow(dt[sample].T,aspect='auto',origin='lower',cmap='magma');ax.set(xlabel=tr('时间索引0–15','Time index0–15'),ylabel=tr('内部通道0–23','Internal channel0–23'));fig.colorbar(im,ax=ax,label=tr('学习得到的步长Δ','Learned step sizeΔ'))
    ax=fig.add_subplot(gs[1,1]);ax.plot(time,states[sample,:,0,:].numpy());ax.set(xlabel=tr('时间步','Time step'),ylabel=tr('通道0的四维状态','Four state coordinates, channel0'));ax.legend([f'n={i}' for i in range(4)],fontsize=8,ncol=2)
    fig.savefig(output/f'memory-{language}.svg');plt.close(fig)
    lengths=np.array([16,32,64,128,256,512,1024,2048]);attention_entries=4*lengths**2;kv_entries=2*32*lengths;state_entries=np.full_like(lengths,24*4)
    fig,axes=plt.subplots(1,2,figsize=(11.5,4.3),layout='constrained')
    axes[0].loglog(lengths,attention_entries,'o-',label=tr('4头注意力分数','Four-head attention scores'),color='#0072B2');axes[0].loglog(lengths,24*4*lengths,'o-',label=tr('选择性状态逐步展开','Unrolled selective states'),color='#D58500');axes[0].set(xlabel=tr('序列长度T','Sequence lengthT'),ylabel=tr('指定数组的标量数','Scalars in the specified array'));axes[0].legend(fontsize=9)
    axes[1].loglog(lengths,kv_entries*4/1024,'o-',label=tr('单层KV缓存，d=32','One-layer KV cache,d=32'),color='#0072B2');axes[1].loglog(lengths,state_entries*4/1024,'o-',label=tr('24×4递推状态','24×4 recurrent state'),color='#D58500');axes[1].set(xlabel=tr('已读长度T','Observed lengthT'),ylabel=tr('float32状态存储（KiB）','float32 state storage(KiB)'));axes[1].legend(fontsize=9)
    fig.savefig(output/f'complexity-{language}.svg');plt.close(fig)
    summary={'retrieval':{'train':1000,'validation':300,'test':400,'accuracy':accuracy,'query_blind_majority_accuracy':baseline,'best_epoch':attention_best,'parameter_count':sum(p.numel() for p in transformer.parameters()),'sample_index':retrieval_sample,'sample_query_key':query,'sample_correct_slot':int(slots[retrieval_sample]),'sample_values':value_ids.tolist(),'sample_prediction':int(logits[retrieval_sample].argmax()),'sample_target':int(ey[retrieval_sample])},'memory':{'train':800,'validation':240,'test':320,'length':16,'test_mse_all_steps':memory_mse,'test_mse_last_step':last_mse,'best_epoch':memory_best,'parameter_count':sum(p.numel() for p in selective.parameters())},'hand_attention':{'weights':alpha.numpy().tolist(),'output':manual.numpy().tolist(),'library_max_error':qkv_error},'causal_prefix_max_error':causal_error,'scan_expansion_max_error':scan_error,'scan_final_state':h.tolist(),'torch_version':torch.__version__}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');np.savez(output/'experiment.npz',attention_history=attention_history,memory_history=memory_history,head_maps=head_maps,memory_input=me.numpy(),memory_target=mey.numpy(),memory_prediction=memory_pred.numpy(),delta=dt.numpy(),states=states.numpy(),retrieval_test=ex.numpy(),retrieval_target=ey.numpy());print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();run(a.output,a.language)
```

![Measured training and validation curves for two separate tasks: retrieval cross entropy on the left, positionwise last-marked-value MSE on the right. Both vertical axes are logarithmic; sample counts and budgets are stated in the text.](https://ml-biomat.com/static/tutorials/machine-learning/figures/103c6182d5077ec31ae91238.svg?v=103c6182d507)

Figure 3Measured training and validation curves for two separate tasks: retrieval cross entropy on the left, positionwise last-marked-value MSE on the right. Both vertical axes are logarithmic; sample counts and budgets are stated in the text.

The retrieval model reaches 100% accuracy on four hundred test sequences, compared with 53.5% for the query-blind majority rule. It has 17,764 parameters. For its attention display, we select a test sequence whose four values are distinct, so repeated answers cannot obscure the reading location. The panels show actual second-layer weights for all four heads, with the final query row outlined. Heads may allocate reading differently; residual connections, feed-forward processing, and the classification head jointly determine the answer.

![Four actual attention heads in the trained Transformer’s second layer. The first test example with four distinct values is selected. Columns are records being read; rows are query positions, with the final query outlined. Heads share a 0–1 color scale.](https://ml-biomat.com/static/tutorials/machine-learning/figures/2cbf6245d30aa3c1ebd55542.svg?v=2cbf6245d30a)

Figure 4Four actual attention heads in the trained Transformer’s second layer. The first test example with four distinct values is selected. Columns are records being read; rows are query positions, with the final query outlined. Heads share a 0–1 color scale.

The selective model has 1,177 parameters. Its test MSE is approximately 0.000552 across all positions and 0.001074 at the final position. The trajectory places current input, last-marked-value target, and model readout on the same time axis. Circles mark observations that should be written, while gray distractors continue to arrive. The prediction follows the target’s piecewise changes. Lower panels display learned step sizes and four state coordinates from one internal channel, connecting output behavior to the actual update dynamics.

The final stretch of this example contains no new marker, so the target stays level while the prediction shows visible drift near the end. This local behavior coexists with a small overall MSE, showing why a time-resolved view adds information. A further experiment could group errors by steps since the last marker, then vary distractor values to separate retention behavior from current-readout effects. The measured trajectory therefore supplies both a result and a specific question for the next investigation.

![A held-out trajectory from the trained selective model: current values, markers, targets, and predictions share a time axis. Lower panels show learned step sizes for 24 channels and four state coordinates in channel 0. Markers define when the task requires updating; the model learns its control parameters.](https://ml-biomat.com/static/tutorials/machine-learning/figures/ec6674f4681c20176b03f7cf.svg?v=ec6674f4681c)

Figure 5A held-out trajectory from the trained selective model: current values, markers, targets, and predictions share a time axis. Lower panels show learned step sizes for 24 channels and four state coordinates in channel 0. Markers define when the task requires updating; the model learns its control parameters.

Three independent numerical checks accompany training. The hand-calculated two-key weighted sum agrees with the library operation. Changing future inputs leaves the protected causal prefix unchanged. A two-coordinate recurrence agrees with the expanded weighted sum of its individual writes to approximately 2.78×10⁻¹⁷. That last check directly verifies why an earlier write receives every subsequent retention multiplier. Small numerical checks and trained behavior answer complementary questions about implementation rules and learning.

## Move the query and watch where information comes from

Four keys point in four directions. Their values are (2,0),(0,4),(−2,0),(0,−4). Drag the query in the left plane or use the sliders; weights and output update together. With the causal mask enabled, the query is at position 1 and can read only positions 0 and 1; the later two records receive zero weight.

[Figure: Query direction, four attention weights, and weighted-value output](https://ml-biomat.com/tutorials/machine-learning/m32/en/#M32-plot)

Key order: K1=(1,0),K2=(0,1),K3=(−1,0),K4=(0,−1). Dot-product scores are divided by √2. All features are dimensionless. The green arrow is the weighted output; gray bars mark blocked records.

## Long-context cost follows what must be stored and compared

Ordinary full self-attention considers pairs of positions, so doubling sequence length quadruples the number of pairs. During generation, a KV cache retains previous keys and values to avoid recomputing them for every new item. The new query still reads those cached records. A state-space recurrence compresses the past into a fixed-shape state, whose core size does not grow with the observed prefix. The methods retain history differently and therefore have different computation and storage structures.

$$
N_{\mathrm{score}}=H T^2,\qquad N_{\mathrm{KV}}=2Td,\qquad N_{\mathrm{state}}=D_cN
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1d35c4e2939f2a170dba0b27.svg) | Sequence length, attention-head count, and total model width across heads; counts are for one layer and one example. |
| ![Formula](https://ml-biomat.com/static/agent-math/92daac7d5ea84ad4363336d6.svg) | Scalar count in an explicit full self-attention score array. |
| ![Formula](https://ml-biomat.com/static/agent-math/568d04f23698088cf4fe07e0.svg) | Scalar count in ordinary multi-head key/value caches; factor2 accounts for both. |
| ![Formula](https://ml-biomat.com/static/agent-math/3af6a2de19c1f1d50afa0ea7.svg) | Internal channel count, state width per channel, and current core-state scalar count. |

For H=4,T=512, the score array has 1,048,576 scalars. At d=32, KV caches contain32,768 scalars, or 128KiB in float32. D_c=24,N=4 gives 96 current-state values, or 0.375KiB. Counts concern the named arrays; weights, convolution buffers, and other intermediates are separate. Retaining T states for training adds a factor of T.

![Analytic array sizes, not runtime measurements. Left: full attention scores and unrolled training-state counts. Right: float32 storage for ordinary one-layer KV caches and the example’s current recurrent core. Convolution buffers, weights, and other intermediates are separate.](https://ml-biomat.com/static/tutorials/machine-learning/figures/c587057fa9f6953c3b9746c2.svg?v=c587057fa9f6)

Figure 6Analytic array sizes, not runtime measurements. Left: full attention scores and unrolled training-state counts. Right: float32 storage for ordinary one-layer KV caches and the example’s current recurrent core. Convolution buffers, weights, and other intermediates are separate.

The left panel counts scalars in specified arrays; the right converts counts using four bytes per float32 number. With four heads and length 512, a full attention-score array contains 1,048,576 scalars. A one-layer KV cache at model width 32 contains 32,768 scalars, or 128KiB. Our 24-channel, four-coordinate recurrent core retains 96 state values, alongside separate short-convolution buffers and model weights. The figure distinguishes unrolled training states from inference that retains only the current state.

Implementation changes memory use. Fused attention can calculate blocks without storing a full score matrix for long periods. Sparse or local attention changes which position pairs participate. Grouped-query attention reduces KV head count and therefore the cache constant. An explicit diagonal-state Python loop is easy to inspect, while an optimized scan kernel has different runtime efficiency. Record sequence length, batch size, precision, caching, and measurements on the actual hardware when comparing deployment choices; this connects mathematical scale to observed speed.

Content matching in a complete input, repeated access to distant details during generation, and continuous-state tracking impose different requirements. Attention supplies content-dependent reading weights. Selective-state models supply input-dependent updates to a compressed record. Hybrid designs can combine them. New architecture names can then be unpacked using the same questions: how inputs are represented, how history is retained, how the current output reads it, and which experiment shows that these mechanisms suit the task.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M32.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

   Original Transformer research and history.

   Primary research link; no paper figure copied
2. [Dive into Deep Learning — The Transformer Architecture](https://d2l.ai/chapter_attention-mechanisms-and-transformers/transformer.html)

   Original tutorial figure, encoder/decoder, and masks.

   CC BY-SA4.0 text/figures
3. [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752)

   Input-dependent state parameters and scan design.

   Primary research link; no paper figure copied
4. [state-spaces/mamba — reference implementation](https://github.com/state-spaces/mamba)

   Official selective recurrence, causal convolution, and gating.

   Apache2.0 repository code; no GPU extension bundled
5. [PyTorch — MultiheadAttention](https://docs.pytorch.org/docs/2.15/generated/torch.nn.MultiheadAttention.html)

   Shapes, per-head weights, and boolean-mask convention used here.
