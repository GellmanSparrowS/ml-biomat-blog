# How Language Models Learn to Continue and Respond

Source: https://ml-biomat.com/tutorials/machine-learning/m16/en/
Language: en

From causal prediction on a small corpus to LoRA, preferences, quantization, and inspectable evaluation.

## 1. From completing a sentence to performing a language task

A keyboard predicting the next word, a search engine rewriting a query, and an assistant completing a function all use existing text to predict what should follow. A language model expresses this as a conditional distribution over the next token and combines successive predictions into a sequence. A token is a discrete processing unit: it may be a character, a word fragment, or bytes. The model receives identifiers for these units rather than directly receiving the meaning of the paragraph on a screen. Its layers learn relationships among those identifiers and their contexts.

Training a model to continue text and training it to answer a request are related but distinct jobs. Pretraining learns patterns from text, supervised instruction tuning adjusts behavior through task demonstrations, and preference optimization uses comparisons between responses. Quantization and distillation address the resources needed to preserve useful capabilities. Retrieval and tools can provide additional information or operations. This chapter follows the training chain and uses a small model built from scratch to make causal prediction and low-rank adaptation concrete.

The example has eighteen tokens and declarative sentences such as “the red dog runs .”. Complete sentences are assigned to separate training, validation, and test partitions. We then freeze the learned backbone and train a small set of LoRA parameters to answer prompts such as “color of the red dog ? :”. The task makes every step inspectable: input tokens, scored output positions, parameter updates, and agreement after merging the adapter. Questions about larger-scale data, budgets, and evaluation build on those visible calculations.

## 2. Corpus preparation and tokenization determine what is read

A useful pretraining corpus is more than a large collection of files. Reposted pages, duplicated code, and templates change sample weighting. Poor optical character recognition can introduce systematic errors, while language and domain proportions determine where computation is spent. Deduplication can operate on documents, near-duplicate passages, and the boundaries between partitions, with explicit retention rules. Evaluation contamination includes explanations, paraphrases, and mirrors of test questions, not just exact strings. Group documents or sources before constructing windows to reduce leakage between neighboring excerpts.

Byte-pair encoding begins with smaller units and repeatedly merges frequent adjacent token pairs into common subwords. Byte-level approaches use bytes as the coverage units. A larger vocabulary can shorten sequences while increasing embedding and output layers; a smaller vocabulary may require longer sequences. Chinese text, uncommon technical terms, and code can have different tokenization efficiencies, so equal character counts need not imply equal computation. Normalization, special tokens, and conversation templates must match the model. Identical-looking text can otherwise produce different identifiers or boundaries.

A small example explains merging. Suppose “ab” occurs three times and “ac” once. Starting with a, b, and c, the adjacent pair a–b is most frequent, so it becomes the token “ab”. The first word now uses one token while the second still uses two. A trained BPE tokenizer preserves the merge order and applies those rules to new text. It allocates representation units; merging “ab” does not establish understanding of its meaning. Our fixed eighteen-token vocabulary lets the reader inspect the identifier mapping directly while focusing the experiment on language modeling and adaptation.

Data versions are part of the experiment. Changed cleaning, a different tokenizer, or altered domain sampling changes the training distribution. Window boundaries, end-of-document markers, and whether padding contributes to the loss also need definitions. Each declarative sentence here begins and ends with a special token. Twenty-seven distinct sentences are partitioned into sixteen training, six validation, and five test sentences before training, with no identical complete sentence shared by training and test. This deliberately small grammar makes the split and each prediction easy to audit.

## 3. Make next-token prediction trainable

Statistical language models estimated the next word from a limited word history, such as counts of a third word following the previous two. Neural language models introduced learned word vectors that share parameters across related contexts. Recurrent networks compressed longer histories into states, while Transformers used attention to connect positions directly. The recurring question is which information in earlier text helps predict the next unit. Larger training has enabled broader transfer across tasks, but the objective can still be understood through token probabilities.

$$
p_\theta(x_{1:L})=\prod_{t=1}^{L}p_\theta(x_t\mid x_{<t}),\qquad \mathcal L=-\frac1{N_{\rm scored}}\sum_{t=1}^{L}m_t\log p_\theta(x_t\mid x_{<t}),\quad N_{\rm scored}=\sum_t m_t
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/cbb686effe661c228e62f064.svg) | Token at position t and its preceding prefix; tokens are discrete identifiers. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc947ed58e2957c8badfe9da.svg) | Sequence length and integer position index. |
| ![Formula](https://ml-biomat.com/static/agent-math/a564121e37890a2a9e2674a1.svg) | Model parameters and associated conditional probabilities, which are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/ab8ec7e384ca94386628a21f.svg) | Loss mask: one for scored positions and zero for excluded prompt or padding positions. |
| ![Formula](https://ml-biomat.com/static/agent-math/808a7af514d2203e40910dce.svg) | Positive number of scored tokens. |
| ![Formula](https://ml-biomat.com/static/agent-math/6a37d71725f7b516cbb9cf38.svg) | Mean negative natural-log probability, in nats per token. |

The chain rule factors sequence probability into conditional terms, while training accumulates negative logs of correct-token probabilities. Two scored tokens with probabilities 0.8 and 0.5 give sequence probability 0.4 and mean loss approximately 0.4581. A prompt can have mask zero while still influencing answer probabilities through attention. The code shifts inputs and targets by one position and ignores adaptation-prompt targets; the answer is not available at the position predicting that answer.

A causal mask allows a position to read only itself and earlier positions, preventing it from seeing the target next token during training. Many positions can be trained in parallel because their reference prefixes are already supplied. During generation, however, the next input depends on the token just selected. For a prefix such as “the red dog,” the output is a distribution across the vocabulary rather than a single answer. Greedy decoding takes its largest entry; sampling draws according to probabilities. Temperature and top-k choices modify randomness, so evaluation should record them alongside answer quality and cost.

$$
\mathrm{PPL}=\exp(\mathcal L)=\left(\prod_{t\in\mathcal S}\frac1{p_\theta(x_t\mid x_{<t})}\right)^{1/|\mathcal S|}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9e4e868f2fc2500459ddfb40.svg) | Mean negative natural-log loss over scored tokens, in nats per token. |
| ![Formula](https://ml-biomat.com/static/agent-math/70e8b5284e565dcc725b6ae7.svg) | Set of evaluated positions and its cardinality. |
| ![Formula](https://ml-biomat.com/static/agent-math/5ee0d293718f519d772b8cea.svg) | Dimensionless conditional probability assigned to the correct token. |
| ![Formula](https://ml-biomat.com/static/agent-math/f08cb97629674a8500700c57.svg) | Perplexity and natural exponential; perplexity is dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/092ff4a34fc8a0e4ab5d52f2.svg) | Position, current token, prefix, and model parameters. |

Averaging logs accumulates probabilities stably. Exponentiating gives the geometric mean of inverse probabilities. Correct-token probability 0.25 everywhere yields loss ln4 and perplexity four. For two probabilities 0.8 and 0.5, perplexity is sqrt(1/0.4), about 1.581. Comparisons require the same tokenizer, scored positions, and corpus, since otherwise a token is not a shared evaluation unit.

Perplexity is the exponential of average negative log likelihood. If the correct token always receives probability one quarter, perplexity is four: an effective number of choices under this logarithmic scoring rule, not a claim that every sentence has four correct answers. Different tokenizers divide the same text into different numbers of units, making per-token perplexities unsuitable for direct comparison without a common basis. Low perplexity also does not establish instruction following, factual accuracy, or mathematical reasoning. The example reports test perplexity, generated sentences, and adapted responses separately to inspect distribution learning and task behavior.

## 4. Allocate a budget across parameters, data, and computation

With a fixed compute budget, a larger model competes with processing more training tokens. Scaling studies fit relationships between model size, data quantity, and validation loss using controlled training runs, helping plan subsequent experiments. The original Chinchilla study emphasized considering parameters and training data together under a fixed budget. Its conclusions belong to the models, data, and compute range studied. A practical project additionally considers data quality, repeated exposure, context length, and downstream inference cost rather than adopting a single parameter-to-token ratio as a universal constant.

A data mixture is a learning schedule. General prose, code, mathematics, languages, and domain text expose the model to different errors and update directions. Repeating a small high-quality dataset is different from acquiring independent samples; additional repetition can reduce training loss while validation loss rises. Controlled runs should record processed tokens, measured throughput, validation loss, and task results before scaling the model. This describes where the budget goes more usefully than comparing parameter counts alone. Sequence length also affects attention work and activation storage, so token counts need the context configuration to be interpretable.

A mixture-of-experts layer prepares several feed-forward networks and uses a router to select a small subset for each token. Total parameter count can be large while each token activates fewer parameters. Switch Transformer provides a clear example in the development of sparse routing. An expert is not inherently assigned a human category such as physics or English; specialization emerges during training and can mix several factors. Uneven load, capacity limits, and communication between devices affect execution. Total parameters, activated parameters, and measured latency therefore describe different properties of the system.

$$
y=\sum_{e\in\mathcal E_k(x)}g_e(x)F_e(x),\qquad \sum_{e\in\mathcal E_k(x)}g_e(x)=1
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e4974840e693fae46f1e9926.svg) | Input and output hidden vectors for one token, usually dimension d with no assigned physical units. |
| ![Formula](https://ml-biomat.com/static/agent-math/81766128040a367a6c93adfc.svg) | Expert network e mapping the input to an output vector. |
| ![Formula](https://ml-biomat.com/static/agent-math/bab1cdf2de84a62048077249.svg) | Set of k experts selected by the router, selected count, and expert index. |
| ![Formula](https://ml-biomat.com/static/agent-math/83c51e1af9178eecb57722fc.svg) | Nonnegative dimensionless weights normalized over selected experts. |

This expression uses gates renormalized after top-k selection; particular MoE implementations can choose other gating conventions. Expert outputs (2,0) and (0,4) with weights 0.75 and 0.25 combine into (1.5,1). Unselected experts do not perform this token’s expert feed-forward computation, but their parameters still require storage. Routing and communication also cost resources, so active expert count alone is not a complete runtime estimate.

Training memory and inference memory also have different components. Training stores parameters, gradients, optimizer states, and activations needed for backward computation. Autoregressive inference can cache attention keys and values from earlier tokens, avoiding repeated calculation while using memory that grows with the retained context and batch size. Processing the initial prompt, often called prefill, differs from emitting successive tokens, or decoding. A throughput measurement should specify whether it includes both stages and how long the inputs and outputs are. This explains why a model that fits in memory can still have poor interactive latency, and why batching improves one measurement while increasing another user's waiting time.

## 5. Instruction tuning and LoRA restrict the learned update

Supervised fine-tuning uses task inputs paired with desired responses to adapt an existing language distribution. If only the answer should be trained, prompt and padding positions are masked from the loss. The model still reads the prompt; those positions simply do not directly contribute target terms. Conversation templates identify roles, turns, and end markers. Demonstration quality and coverage determine what behavior is taught: consistent formatting supports predictable output, while missing exceptional cases, corrections, or complex inputs leaves corresponding gaps. Organize examples around intended use rather than optimizing the number of records alone.

$$
y=W_0x+\frac\alpha r BAx+b,\qquad W_{\rm merged}=W_0+\frac\alpha r BA,\qquad N_{\rm LoRA}=r(d_{\rm in}+d_{\rm out})
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e69c4f8619ee3c1461e894d3.svg) | Input vector of dimension d_in, output of dimension d_out, and output bias; neural values have no assigned physical units. |
| ![Formula](https://ml-biomat.com/static/agent-math/605abc76c378afdf9024a75f.svg) | Frozen base weight matrix of shape d_out×d_in. |
| ![Formula](https://ml-biomat.com/static/agent-math/f12c13576bb625453e573142.svg) | Trainable factors of shapes r×d_in and d_out×r. |
| ![Formula](https://ml-biomat.com/static/agent-math/2e532aa640b07a3f05077121.svg) | Positive integer rank and scaling hyperparameter; alpha/r is dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/1deeadf66ae71d7cb0226d5a.svg) | Merged ordinary weight matrix with the same shape as the base weight. |
| ![Formula](https://ml-biomat.com/static/agent-math/ce72a13d053499294034e6ef.svg) | Number of factor parameters, input dimension, and output dimension; integers. |

A maps the input into r dimensions, and B maps it back to the output dimension, making the update rank at most r. With a 2×2 identity base, x=(1,2), A=(1,1), B=(0.5,−0.25) transposed, alpha=r=1, and zero bias, Ax=3 and BAx=(1.5,−0.75), giving output (2.5,1.25). Rank four uses 256 parameters for a 32×32 layer and 200 for an 18×32 output layer. Two former layers plus the latter train 712 values.

LoRA freezes an existing weight matrix and represents its update as the product of two smaller matrices. Imagine retaining a mixing desk while adding a few linked controls: each can affect many outputs, but the independent directions of change are restricted. A 32×32 matrix contains 1024 values. Rank-four factors contain 4×32+32×4=256. The restriction applies to the update, not to the rank of the original matrix. Increasing rank expands the available changes and parameter cost; validation on the target task determines whether the extra capacity helps.

The example places rank-four LoRA modules on attention query and value projections and on the output vocabulary layer, with scale alpha/r equal to two. One factor is randomly initialized and the other is zero, making the initial update exactly zero and preserving the backbone output. After training, the factor product can be added to the base weights to create ordinary linear layers. We verify that operation by comparing logits before and after merging. Several task adapters can also share one backbone, storing different lightweight changes rather than independent copies of all backbone weights.

## Compute the same output through an adapter or merged weights

This two-dimensional example uses an identity matrix as the frozen backbone. Choose one or two update directions and adjust input and scale alpha. Inspect A, B, the update, and both computation paths. Two dimensions support hand calculations; the actual 32-dimensional model demonstrates parameter savings.

[Figure: Low-rank factors, merged matrix, and numerical outputs](https://ml-biomat.com/tutorials/machine-learning/m16/en/#M16-svg)

## 6. Quantization and distillation reduce different resources

Quantization represents values with fewer bits, usually using scales and sometimes zero points to map floating-point numbers into finite codes. Range and outliers affect error, so tensor-wise, channel-wise, and block-wise scales make different tradeoffs. Fewer stored bytes do not automatically imply faster execution. Speed depends on supported kernels, dequantization, and hardware. Compare storage, memory, latency, throughput, and task error, and identify whether weights, activations, or caches are quantized. A computation that immediately reconstructs floating-point weights demonstrates numerical error but not an optimized low-bit inference kernel.

$$
s_i=\frac{\max_j|W_{ij}|}{127},\quad Q_{ij}=\operatorname{clip}\!\left(\operatorname{round}\frac{W_{ij}}{s_i},-127,127\right),\quad \hat W_{ij}=s_iQ_{ij}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33a5218183f1f6f9bd612ba0.svg) | Floating-point output-head weight at row i and column j. |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | Integer output- and input-dimension indices. |
| ![Formula](https://ml-biomat.com/static/agent-math/367eee464c8451e0f3beb03c.svg) | Positive row scale with the same units as weights; zero rows use a numerical floor. |
| ![Formula](https://ml-biomat.com/static/agent-math/5e116ac59f0a50d2fdd88270.svg) | Integer code stored as int8, between −127 and 127, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/a31f2474b0940d633856d1bb.svg) | Dequantized floating-point approximation. |
| ![Formula](https://ml-biomat.com/static/agent-math/ef7f27c02f7a407ee9a0fbeb.svg) | Rounding to the nearest integer and clipping to the specified range. |

The maximum absolute row value maps to integer 127, and other values are rounded to nearby grid points. Row (−1,0,0.5,1) uses scale 1/127 and codes (−127,0,64,127), reconstructing the third value as about 0.50394 with error 0.00394. Each code uses one byte, but row scales also require storage. Eighteen rows of 32 codes use 576 bytes; eighteen float32 scales add 72 bytes, totaling 648.

QLoRA combines low-bit storage of a frozen backbone with trainable low-rank adapters, propagating gradients through backbone computation into those adapters. The original work discusses NF4, quantization of scale information, and optimizer strategies for memory spikes. Four-bit backbone storage does not mean that all arithmetic, activations, and optimizer states use four bits. Our script separately demonstrates row-wise int8 quantization of the merged output-head weights and checks dequantization error. The actual adaptation run uses floating-point LoRA. The code and results keep those two operations distinct.

Distillation instead trains a smaller student from teacher distributions, responses, or intermediate representations. Soft targets can describe which incorrect candidates are still similar, rather than supplying only a correct class identifier. Generative distillation can use teacher-produced demonstrations. Temperature, teacher quality, and example coverage affect the result, and systematic teacher errors may transfer as well. Quantization changes numerical representation, distillation changes a model or its training target, and LoRA changes the parameterization of adaptation. They can be combined while retaining separate comparisons of the benefit and error introduced by each operation.

A three-class numerical example makes soft supervision concrete. Suppose a teacher assigns probabilities 0.7, 0.2, and 0.1, while a student assigns 0.4, 0.35, and 0.25. Matching the teacher distribution encourages more weight on the first class while preserving a difference between the two alternatives. A one-hot label for the first class does not communicate that second-versus-third distinction. Temperature can reveal less dominant alternatives, but it can also amplify unhelpful teacher relationships. A distilled student should therefore be evaluated on the actual task and on examples outside the teacher-generated training set, with model size and inference cost reported alongside accuracy.

## 7. Learn from comparisons between two responses

Writing a unique reference answer can be difficult when comparing two responses is easier. One explanation may describe an experimental procedure clearly while another omits an important condition. A conventional RLHF pipeline first trains a reward model on such comparisons, then updates a language model using generated responses, rewards, and a penalty for departing from a reference policy. The reward model approximates the collected preferences; aggressive optimization can exploit imperfections in that approximation. Track independent task behavior as well as reward. PPO is one possible policy-update method, with its mechanics developed in the deep reinforcement learning chapter.

$$
\mathcal L_{\rm DPO}=-\log\sigma\!\left[\beta\left(\log\frac{\pi_\theta(y_w\mid x)}{\pi_{\rm ref}(y_w\mid x)}-\log\frac{\pi_\theta(y_l\mid x)}{\pi_{\rm ref}(y_l\mid x)}\right)\right],\qquad \sigma(z)=\frac1{1+e^{-z}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/dba9bd8d1a5e5f99648a8f0a.svg) | Shared prompt, preferred response, and rejected response, all token sequences. |
| ![Formula](https://ml-biomat.com/static/agent-math/a30d99dab0379f2f58aac9b9.svg) | Current and fixed-reference probabilities of complete responses, dimensionless; computed by summing answer-token log probabilities. |
| ![Formula](https://ml-biomat.com/static/agent-math/1cc8c189acd9786d014e26f9.svg) | Trainable policy parameters and positive dimensionless preference-objective coefficient. |
| ![Formula](https://ml-biomat.com/static/agent-math/ff377425645f91fe4ca4ec1d.svg) | Sigmoid function and its dimensionless input. |
| ![Formula](https://ml-biomat.com/static/agent-math/2cefac4625b95ed29e1d4d22.svg) | Negative natural-log loss for one preference pair, in nats. |

Each log ratio measures how the current policy changes a response relative to the reference, then the difference compares those changes. Current log probabilities −1 and −2 with reference values both −1.5 give difference one. Beta 0.2 produces −ln sigmoid(0.2), approximately 0.59814. An unchanged policy gives zero difference and loss ln2, approximately 0.6931. Training averages across preference pairs. Sequence log probabilities vary with length, so data construction and evaluation should account for length-related preferences.

Direct preference optimization expresses paired comparisons through log-probability ratios relative to a reference model. In this training form, a separately fitted reward model and an online reinforcement-learning sampling loop are unnecessary. Both responses must address the same prompt, and reference probabilities remain fixed. Raising the preferred response probability alone, without the other response and reference distribution, changes the objective. Annotation criteria, response length, and data origin influence the learned direction. Longer responses may sometimes be judged better for reasons unrelated to their content, so evaluation should distinguish content quality, completeness, and format.

The script includes a numerical DPO example. Current log probabilities for preferred and rejected responses are −1 and −2; both reference log probabilities are −1.5. With beta equal to 0.2, the loss is approximately 0.5981. This verifies the objective calculation rather than running large-scale preference training. A subsequent preference experiment should preserve paired examples, judgment criteria, and independent evaluations, then inspect changes by task and language. One aggregate win rate can conceal which behaviors improved and which changed in an unwanted direction.

Preference batches require careful token accounting. Each preferred and rejected completion is joined to the same prompt, but only completion tokens contribute to its response log probability. Padding positions are excluded, and the reference model uses the same tokenizer and response boundaries. Summing log probabilities evaluates a complete sequence; averaging them by length defines a different objective unless the method explicitly calls for that change. A label reversal also reverses the learning signal, so a few readable paired examples are valuable checks before a long run. These checks make the mathematical quantities correspond to the responses that annotators actually compared.

## 8. Learn sentences, then update only 712 parameters

The backbone has one causal Transformer block, hidden dimension 32, four attention heads of dimension eight, and a feed-forward hidden dimension of 64, totaling 10290 parameters. Each declarative sentence contributes six prediction positions. Each training batch samples 24 sentences with replacement from the sixteen training sentences, so a sentence may occur more than once in a batch. Training runs for at most 400 updates, evaluating held-out validation sentences every ten steps and retaining the best checkpoint. Adaptation trains on six color–animal prompt combinations and evaluates three others. Prompt tokens are masked from the loss; only the response color and end token are scored.

### Pretraining, low-rank adaptation, and weight merging

Implements a one-block causal Transformer and LoRA without downloading large models. Saves training curves, complete generations, quantization and preference calculations, plus frozen-weight, causal, and merge checks.

```
"""A tiny causal language model, genuine low-rank adaptation, and exact checks."""
import argparse,copy,json,math,time
from pathlib import Path
import numpy as np
import torch
from torch import nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)
WORDS=['<pad>','<bos>','<eos>','the','red','green','blue','fox','dog','cat','runs','sleeps','jumps','.','color','of','?',':']
VOCAB={w:i for i,w in enumerate(WORDS)};D=32
def ids(words):return [VOCAB[w]for w in words]

class Attention(nn.Module):
    def __init__(self):
        super().__init__();self.q=nn.Linear(D,D);self.k=nn.Linear(D,D);self.v=nn.Linear(D,D);self.out=nn.Linear(D,D)
    def forward(self,x):
        b,t,d=x.shape
        q,k,v=[layer(x).reshape(b,t,4,8).transpose(1,2)for layer in [self.q,self.k,self.v]]
        scores=q@k.transpose(-2,-1)/math.sqrt(8);mask=torch.triu(torch.ones(t,t,dtype=torch.bool),diagonal=1);scores=scores.masked_fill(mask,float('-inf'))
        return self.out((scores.softmax(-1)@v).transpose(1,2).reshape(b,t,d))

class TinyLM(nn.Module):
    def __init__(self):
        super().__init__();self.token=nn.Embedding(len(WORDS),D);self.position=nn.Embedding(16,D);self.norm1=nn.LayerNorm(D);self.attn=Attention();self.norm2=nn.LayerNorm(D);self.ff=nn.Sequential(nn.Linear(D,64),nn.GELU(),nn.Linear(64,D));self.final=nn.LayerNorm(D);self.head=nn.Linear(D,len(WORDS))
    def forward(self,tokens):
        x=self.token(tokens)+self.position(torch.arange(tokens.shape[1]))[None];x=x+self.attn(self.norm1(x));x=x+self.ff(self.norm2(x));return self.head(self.final(x))

class LoRALinear(nn.Module):
    def __init__(self,base,rank=4,alpha=8):
        super().__init__();self.base=base;self.A=nn.Parameter(torch.randn(rank,base.in_features)*.02);self.B=nn.Parameter(torch.zeros(base.out_features,rank));self.scale=alpha/rank
        for p in self.base.parameters():p.requires_grad=False
    def forward(self,x):return self.base(x)+(x@self.A.T@self.B.T)*self.scale
    def merged(self):
        layer=copy.deepcopy(self.base)
        with torch.no_grad():layer.weight.add_(self.scale*self.B@self.A)
        return layer

def corpus():
    parts=[[],[],[]];sentences=[[],[],[]]
    for c,color in enumerate(['red','green','blue']):
        for a,animal in enumerate(['fox','dog','cat']):
            for v,verb in enumerate(['runs','sleeps','jumps']):
                residue=(c+2*a+v)%5;split=2 if residue==0 else 1 if residue==1 else 0
                words=['<bos>','the',color,animal,verb,'.','<eos>'];parts[split].append(ids(words));sentences[split].append(' '.join(words))
    return [torch.tensor(p)for p in parts],sentences

def prompts():
    allrows=[];istrain=[]
    for c,color in enumerate(['red','green','blue']):
        for a,animal in enumerate(['fox','dog','cat']):
            allrows.append(ids(['<bos>','color','of','the',color,animal,'?',':',color,'<eos>']));istrain.append(c!=a)
    return torch.tensor(allrows),np.array(istrain)

def lm_loss(model,rows):
    out=model(rows[:,:-1]);return nn.functional.cross_entropy(out.reshape(-1,len(WORDS)),rows[:,1:].reshape(-1))

def generate(model,prompt,steps=8):
    tokens=list(prompt)
    for _ in range(steps):
        with torch.no_grad():n=int(model(torch.tensor([tokens]))[0,-1].argmax())
        tokens.append(n)
        if n==VOCAB['<eos>']:break
    return ' '.join(WORDS[n]for n in tokens)

def run(out,language):
    out.mkdir(parents=True,exist_ok=True);torch.manual_seed(16);rng=np.random.default_rng(16);text=lambda z,e:z if language=='zh' else e
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','axes.unicode_minus':False})
    save=lambda fig,n:(fig.savefig(out/f'{n}-{language}.svg',bbox_inches='tight'),fig.savefig(out/f'{n}-{language}.png',dpi=140,bbox_inches='tight'),plt.close(fig))
    (train,valid,test),sentences=corpus();base=TinyLM();optimizer=torch.optim.Adam(base.parameters(),lr=.003);trace=[];best=float('inf');selected=0;start=time.perf_counter()
    for step in range(1,401):
        batch=train[torch.randint(len(train),(24,))];optimizer.zero_grad();loss=lm_loss(base,batch);loss.backward();optimizer.step()
        if step%10==0:
            with torch.no_grad():vl=lm_loss(base,valid).item()
            trace.append([step,loss.item(),vl])
            if vl<best:best=vl;weights=copy.deepcopy(base.state_dict());selected=step
    elapsed=time.perf_counter()-start;base.load_state_dict(weights);base.eval()
    with torch.no_grad():test_loss=lm_loss(base,test).item()
    rows,adapttrain=prompts();labels=rows[:,1:].clone();labels[:,:7]=-100
    with torch.no_grad():before=base(rows[:,:8])[:,-1].softmax(1).numpy()
    adapted=copy.deepcopy(base)
    for p in adapted.parameters():p.requires_grad=False
    adapted.attn.q=LoRALinear(adapted.attn.q);adapted.attn.v=LoRALinear(adapted.attn.v);adapted.head=LoRALinear(adapted.head)
    with torch.no_grad():initial_error=float((base(rows[:,:8])-adapted(rows[:,:8])).abs().max())
    frozen={n:p.detach().clone()for n,p in adapted.named_parameters()if not p.requires_grad};opt=torch.optim.Adam([p for p in adapted.parameters()if p.requires_grad],lr=.015);atrace=[]
    for step in range(1,401):
        opt.zero_grad();logits=adapted(rows[adapttrain,:-1]);loss=nn.functional.cross_entropy(logits.reshape(-1,len(WORDS)),labels[adapttrain].reshape(-1),ignore_index=-100);loss.backward();opt.step()
        if step%10==0:atrace.append([step,loss.item()])
    with torch.no_grad():after=adapted(rows[:,:8])[:,-1].softmax(1).numpy();adapt_test_loss=nn.functional.cross_entropy(adapted(rows[~adapttrain,:-1]).reshape(-1,len(WORDS)),labels[~adapttrain].reshape(-1),ignore_index=-100).item()
    frozen_error=max(float((p-frozen[n]).abs().max())for n,p in adapted.named_parameters()if n in frozen)
    merged=copy.deepcopy(adapted);merged.attn.q=merged.attn.q.merged();merged.attn.v=merged.attn.v.merged();merged.head=merged.head.merged()
    with torch.no_grad():merge_error=float((merged(rows[:,:8])-adapted(rows[:,:8])).abs().max())
    torch.save(base.state_dict(),out/'base.pt');torch.save(merged.state_dict(),out/'merged.pt')
    metadata={'vocabulary':WORDS,'architecture':{'hidden_dimension':32,'heads':4,'blocks':1,'feedforward_dimension':64,'max_positions':16},'adaptation':{'targets':['attn.q','attn.v','head'],'rank':4,'alpha':8},'selected_pretrain_step':selected}
    (out/'model.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    reloaded=load_model(out/'merged.pt')
    with torch.no_grad():reload_error=float((reloaded(rows[:,:8])-merged(rows[:,:8])).abs().max())
    true=rows[:,8].numpy();pred=after.argmax(1);bpred=before.argmax(1);delta=(adapted.head.scale*adapted.head.B@adapted.head.A).detach().numpy();singular=np.linalg.svd(delta,compute_uv=False)
    w=merged.head.weight.detach();scale=w.abs().amax(1,keepdim=True).clamp_min(1e-8)/127;quant=(w/scale).round().clamp(-127,127).to(torch.int8);recovered=quant.float()*scale;quant_error=float((w-recovered).abs().max())
    # Causal attention should leave a prefix unchanged when only its suffix changes.
    modified=test[:1,:-1].clone();modified[0,-1]=VOCAB['?']
    with torch.no_grad():causal_error=float((base(test[:1,:-1])[:,:-1]-base(modified)[:,:-1]).abs().max())
    dpo_loss=float(nn.functional.softplus(torch.tensor(-.2)));params=sum(p.numel()for p in base.parameters());trainable=sum(p.numel()for p in adapted.parameters()if p.requires_grad)
    summary={'vocabulary_size':len(WORDS),'unique_sentence_splits':[len(train),len(valid),len(test)],'unique_split_overlap':len(set(sentences[0])&set(sentences[2])),'base_parameters':params,'lora_trainable_parameters':trainable,'pretrain_selected_step':selected,'pretrain_test_loss':test_loss,'pretrain_test_perplexity':math.exp(test_loss),'pretrain_seconds':elapsed,'pretrain_tokens_per_second':400*24*6/elapsed,'base_color_accuracy':float(np.mean(bpred==true)),'lora_seen_pair_accuracy':float(np.mean(pred[adapttrain]==true[adapttrain])),'lora_unseen_pair_accuracy':float(np.mean(pred[~adapttrain]==true[~adapttrain])),'adapt_test_response_loss':adapt_test_loss,'lora_initial_output_error':initial_error,'frozen_parameter_max_change':frozen_error,'merged_logits_max_error':merge_error,'causal_prefix_error':causal_error,'lora_head_numerical_rank':int(np.sum(singular>1e-5)),'quant_head_max_weight_error':quant_error,'quant_head_storage_bytes':quant.numel()+scale.numel()*4,'float_head_storage_bytes':w.numel()*4,'dpo_hand_loss':dpo_loss,'base_generated':generate(base,ids(['<bos>'])),'adapted_outputs':[generate(adapted,row[:8].tolist(),3)for row in rows]}
    summary.update({'reloaded_logits_max_error':reload_error,'reloaded_example':generate(reloaded,ids(['<bos>','color','of','the','red','fox','?',':']),3)})
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');np.savez_compressed(out/'data.npz',pretrain_trace=trace,adapt_trace=atrace,before=before,after=after,targets=true,train_mask=adapttrain,head_delta=delta,singular_values=singular)
    (out/'corpus.json').write_text(json.dumps({'train':sentences[0],'validation':sentences[1],'test':sentences[2]},indent=2),encoding='utf-8')
    assert initial_error==0 and frozen_error==0 and causal_error<1e-6 and merge_error<1e-4 and reload_error==0
    fig,axs=plt.subplots(1,2,figsize=(11,4),layout='constrained');tr=np.array(trace);at=np.array(atrace)
    axs[0].plot(tr[:,0],tr[:,1],label=text('训练','Train'),color='#176b91');axs[0].plot(tr[:,0],tr[:,2],label=text('验证：独立句子','Validation: held-out sentences'),color='#bc584d');axs[0].axvline(selected,color='#9a9a9a',ls='--');axs[0].set(xlabel=text('预训练步数','Pretraining step'),ylabel=text('每token交叉熵','Cross entropy per token'));axs[0].legend()
    axs[1].plot(at[:,0],at[:,1],color='#267c6a');axs[1].set(xlabel=text('LoRA步数','LoRA step'),ylabel=text('仅回答token的交叉熵','Cross entropy on answer tokens'));save(fig,'training')
    fig,axs=plt.subplots(1,2,figsize=(11,5),layout='constrained');promptnames=[f'{WORDS[row[4]]} {WORDS[row[5]]}'for row in rows]
    for ax,probs,title in zip(axs,[before,after],[text('适配前','Before adaptation'),text('LoRA之后','After LoRA')]):
        im=ax.imshow(probs[:,4:7],vmin=0,vmax=1,cmap='Blues',aspect='auto');ax.set(xticks=range(3),xticklabels=['red','green','blue'],yticks=range(9),yticklabels=[s+(' *'if not adapttrain[i]else'')for i,s in enumerate(promptnames)],title=title,xlabel=text('颜色token','Color token'))
        for i in range(9):
            for j in range(3):ax.text(j,i,f'{probs[i,4+j]:.2f}',ha='center',va='center',color='white'if probs[i,4+j]>.5 else '#193b50',fontsize=9)
    fig.colorbar(im,ax=axs,label=text('在完整18词表中的概率','Probability in the full 18-token vocabulary'));save(fig,'answers')
    fig,axs=plt.subplots(1,3,figsize=(12,3.5),layout='constrained');lim=max(abs(delta).max(),1e-9);im=axs[0].imshow(delta,cmap='RdBu_r',vmin=-lim,vmax=lim,aspect='auto');axs[0].set(xlabel=text('输入维度','Input dimension'),ylabel=text('输出token','Output token'),title=text('输出层低秩增量','Low-rank output-head update'));fig.colorbar(im,ax=axs[0])
    axs[1].semilogy(np.arange(1,len(singular)+1),np.maximum(singular,1e-9),'o-',color='#176b91');axs[1].axvline(4.5,color='#aaa',ls='--');axs[1].set(xlabel=text('奇异值编号','Singular value index'),ylabel=text('奇异值','Singular value'),title=text('秩4的结构','Rank-four structure'))
    axs[2].bar([text('全模型','Base model'),'LoRA'],[params,trainable],color=['#9babb5','#267c6a']);axs[2].set(ylabel=text('参数个数','Parameter count'),title=text('冻结与训练','Frozen and trainable'));save(fig,'adapters')
    print(json.dumps(summary,indent=2))

def load_model(checkpoint):
    metadata=json.loads(checkpoint.with_name('model.json').read_text(encoding='utf-8'))
    expected={'hidden_dimension':32,'heads':4,'blocks':1,'feedforward_dimension':64,'max_positions':16}
    if metadata['vocabulary']!=WORDS or metadata['architecture']!=expected:raise ValueError('Checkpoint vocabulary or architecture does not match TinyLM.')
    model=TinyLM();model.load_state_dict(torch.load(checkpoint,map_location='cpu',weights_only=True));return model.eval()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('output'));p.add_argument('--language',choices=['zh','en'],default='en');p.add_argument('--load',type=Path);p.add_argument('--prompt',default='<bos> color of the red fox ? :');args=p.parse_args()
    if args.load:print(generate(load_model(args.load),ids(args.prompt.split()),3))
    else:run(args.output,args.language)
```

The run saves base.pt for the backbone, merged.pt for the adapted and merged model, and model.json for the eighteen-token vocabulary, architecture, target layers, rank, and scaling. A fresh TinyLM loads merged.pt and reproduces the saved model’s logits on the same raw token inputs with maximum difference zero. After training, run `python main.py --load output/merged.pt --prompt "<bos> color of the red fox ? :"` to reload the model and obtain `red <eos>`. Replace output with the directory selected during training. This command performs inference from saved weights without another training run.

The seeded run selects backbone step 50. Its five distinct test sentences have mean token loss 0.72775 and perplexity 2.0704. Greedy generation produces “the red dog runs .”. Continuing backbone training to the final step does not improve validation behavior; the plotted training and validation curves separate. Even this small corpus can overfit, making independent validation more useful for checkpoint selection than either the final update or the lowest training loss. The script also reports elapsed CPU training time and tokens per second for the current run; timing depends on the machine and concurrent workload.

![Measured pretraining and LoRA curves. The backbone selects step50 by validation loss, marked by a dashed line. Adaptation loss scores only the color answer and end token.](https://ml-biomat.com/static/tutorials/machine-learning/figures/96a53a66aee5de8343058e57.svg?v=96a53a66aee5)

Figure 1Measured pretraining and LoRA curves. The backbone selects step50 by validation loss, marked by a dashed line. Adaptation loss scores only the color answer and end token.

The unadapted backbone does not answer the color prompts correctly. Training 712 LoRA parameters gives correct color answers for all six training prompt combinations and all three adaptation-held-out combinations. These combinations are held out at the adaptation stage; the backbone may have encountered the same color and animal together in declarative pretraining sentences. The evaluation therefore measures reading a color from this small prompt format and answering in the required form. Probability plots display the three color entries but retain their normalization over the full eighteen-token vocabulary.

![Three color-token probabilities for nine prompts, normalized over all eighteen vocabulary tokens. Stars identify three prompt combinations held out during adaptation. Prompts match before and after.](https://ml-biomat.com/static/tutorials/machine-learning/figures/05c68f55aca96501c7d16086.svg?v=05c68f55aca9)

Figure 2Three color-token probabilities for nine prompts, normalized over all eighteen vocabulary tokens. Stars identify three prompt combinations held out during adaptation. Prompts match before and after.

The initial adapter output differs from the backbone by zero, frozen parameters change by zero, and modifying a sentence suffix leaves earlier outputs unchanged. Merging LoRA gives a maximum logit difference of about 7.63×10⁻⁶, consistent with floating-point operation ordering. The output-head update has numerical rank four, visible in its singular values. Row-wise int8 output weights plus scales occupy 648 bytes compared with 2304 bytes for the floating-point weights, with maximum weight error approximately 0.00635. Those byte counts concern this layer's weights and scales, not other model states or an entire inference process.

![Actual output-head LoRA update, singular values, and parameter counts. Rank is four; remaining singular values reach numerical rounding scale. The right panel compares base and trainable adapter counts.](https://ml-biomat.com/static/tutorials/machine-learning/figures/6e1d75d89f83b23a3260c819.svg?v=6e1d75d89f83)

Figure 3Actual output-head LoRA update, singular values, and parameter counts. Rank is four; remaining singular values reach numerical rounding scale. The right panel compares base and trainable adapter counts.

## 9. Allocate inference computation and preserve a reusable model

Generating several candidates introduces two separate scores: whether any candidate is correct and whether the system selects a correct final answer. The first describes the generator's coverage under a sampling budget; the second includes the selector's ability. In programming, executable tests can help select candidates, but tests used for selection should be separated from independent final tests. In other tasks, a verifier may share the generator's blind spots. Reporting candidate count and selector behavior prevents improvements from being attributed to a stronger generator when they actually arise from a larger search budget or a better checking procedure.

Inference still offers choices after training ends. A direct response, several sampled candidates followed by selection, iterative revisions, verifier calls, and executable checks consume different token and time budgets. Test-time compute research asks how to allocate those resources across problems of different difficulty. Additional samples help only when the model can produce a useful candidate and the selection procedure can recognize it. Doubling the candidate count does not automatically improve the final answer. Comparisons should fix total generation cost or report quality as a function of budget.

Reasoning evaluation should distinguish correct answers, checkable steps, and fluent expression. Mathematics can be checked through final values and key derivations; code can run against independent tests; document answers can be compared with their evidence. Candidate order, prompt templates, few-shot examples, decoding, and answer extraction can all change benchmark scores. Record them before performing repeated or subgroup evaluations. Longer reasoning text is not itself a capability metric. The relevant behavior is obtaining reliable answers under the new conditions specified by the task.

Reusing open weights requires reading the release conditions for the particular weights, code, tokenizer, and data. A model card describes architecture, languages, training scope, intended inputs, evaluation protocols, and results. An adapter additionally needs its exact base-model version, target layers, rank, and scale. A weight file alone does not ensure that another reader uses the same conversation template or numerical precision. Keeping these configurations with data partitions, environment details, and inference examples turns a successful run into a model that others can continue to study.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M16.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Language Modeling from Scratch](https://cs336.stanford.edu/)

   Open curriculum connecting tokenization, corpora, and training budgets.
2. [Hugging Face — BPE tokenization](https://huggingface.co/learn/llm-course/chapter6/5)

   Subword merging and byte-level coverage.
3. [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)

   Original low-rank adaptation paper; source diagram is linked for reading.
4. [Hugging Face PEFT — LoRA](https://huggingface.co/docs/peft/main/conceptual_guides/lora)

   Freezing, factor dimensions, and merging.
5. [QLoRA](https://arxiv.org/abs/2305.14314)

   Low-bit frozen backbones and low-rank adapters.
6. [Direct Preference Optimization](https://arxiv.org/abs/2305.18290)

   Paired preferences relative to a reference policy.
7. [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556)

   Parameter and data allocation under a compute budget.
8. [Switch Transformers](https://arxiv.org/abs/2101.03961)

   Sparse expert routing, capacity, and communication.
9. [Scaling LLM Test-Time Compute Optimally](https://arxiv.org/abs/2408.03314)

   Allocating inference computation across difficulty.
10. [Hugging Face — Model Cards](https://huggingface.co/docs/hub/model-cards)

    Organizing model, data, evaluation, and version information.
