# Generating one step at a time: autoregression and decoding

Source: https://ml-biomat.com/tutorials/machine-learning/m36/en/
Language: en

Connect next-character probabilities to text, pixels, and audio; train an LSTM and compare sampling, truncation, and beam search.

## 1 From the next character to the probability of an entire object

After typing “tomorrow morning,” a phone might suggest “we,” “leave,” or “meet.” The suggestions depend on the existing text, and several continuations may be reasonable. An autoregressive model organizes these local choices into a complete generative process: read what already exists, assign probabilities to the next item, choose one, append it, and repeat. An item can be a character, a word fragment, an image pixel, or an audio sample. This probability structure supports text completion, speech synthesis, and image generation, while the representation, network architecture, and computational cost differ across applications.

Imagine a branching route map. The probability of choosing the second road depends on which first road you took. To obtain the probability of a complete route, multiply the conditional probabilities encountered along it. Three successive choices with probabilities 0.6, 0.5, and 0.8 give a complete-route probability of 0.24. Because each later probability already conditions on earlier choices, this calculation does not require the choices to be independent. Dropping those conditions would turn a connected sentence into unrelated draws. The chain rule keeps the relationship between the pieces.

$$
p_\theta(x_1,\ldots,x_T\mid c)=\prod_{t=1}^{T}p_\theta(x_t\mid x_{<t},c)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2b4909437d46ae5fc3f3652f.svg) | Discrete symbol t, all preceding symbols, and complete sequence length; the last symbol may be EOS. Symbol indices are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/16508da7a38cadb954c4d62f.svg) | Probability distribution parameterized by network weights θ, and optional condition c such as a known prompt; BOS supplies the start convention. Probabilities are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/6a9f0a3025c11269dd3099d4.svg) | Product and step index from one to T; each factor is a next-item probability conditional on its prefix. |

Repeatedly apply p(a,b)=p(a)p(b|a), without assuming independence across positions. Conditional probabilities 0.6,0.5,0.8 give 0.24. Normalization over finite completed strings additionally requires eventual termination with probability one. Practical sampling uses a maximum length and records whether EOS was reached.

The model also needs a convention for beginning and ending. Our code adds two special symbols to every sentence: BOS starts prediction, and EOS marks completion. Without an ending event, the model can score fixed-length prefixes but lacks an explicit distinction between a finished sentence and one that continues. A third symbol, PAD, fills unused positions when sentences of different lengths share a rectangular batch. PAD is neither ordinary text nor a training target. We will use a miniature language whose entire grammar is specified, allowing every generated string to be checked character by character.

## 2 Why predicting the next character can learn whole sentences

Products of probabilities become tiny quickly: even a probability of 0.5 at every step produces approximately ten to the power minus thirty after one hundred steps. Logarithms turn multiplication into addition, and a minus sign turns higher probability for the correct answer into lower loss. This connects maximum-likelihood training with cross-entropy. When the model reads “the b,” the target might be “l.” The loss selects the probability assigned to that target, while the normalization inside softmax links the update to the scores of all competing characters.

$$
L=-\frac1N\sum_{i,t}m_{it}\log p_\theta(x_{it}\mid x_{i,<t}),\qquad N=\sum_{i,t}m_{it},\qquad \mathrm{PPL}=e^L
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3383ca973814618c495083d9.svg) | Sentence index, position, correct target, and prefix. Batched logits have shape B×S×V and labels B×S. |
| ![Formula](https://ml-biomat.com/static/agent-math/3c22fe2a0468f908781365f1.svg) | Mask equal to one for a valid target and zero for PAD, and total valid-target count; EOS is included. |
| ![Formula](https://ml-biomat.com/static/agent-math/a97c359088981a5c26ed4302.svg) | Mean negative log-likelihood in nats per valid symbol, natural logarithm and exponential base, and dimensionless perplexity. |

Taking the logarithm of a probability product yields a sum; dividing by valid positions gives a per-symbol mean. A three-step path of probability 0.24 has total NLL 1.427116, mean 0.475705, and perplexity 1.609149. Four equally probable choices give loss ln4 and perplexity four. Padding must not alter the denominator.

The shift between inputs and targets deserves careful attention. An input row begins BOS, t, h, e, and so on; the corresponding targets begin t, h, e, space, and eventually EOS. At each position, the network reads that input position and its predecessors to predict the shifted target. All correct histories are available during training, a procedure commonly called teacher forcing. A sentence with more than forty characters therefore supplies more than forty supervised next-character decisions. Training does not need to wait for a freely generated sentence and assign it a single overall score.

Perplexity exponentiates mean negative log-likelihood and can be interpreted as an effective number of choices. A model equally uncertain among four options at every position has perplexity four. Character perplexity becomes much lower when spelling is almost deterministic and genuine choices occur mainly at word boundaries. Our held-out test gives 0.159137 nats per character and perplexity 1.172499. These values describe predictability in this particular miniature language. Comparisons require the same tokenization, evaluation text, treatment of EOS, and averaging denominator; character and subword perplexities use different units of prediction.

## 3 Different networks can implement the same probability chain

Finite-order language models estimated conditional probabilities from counts of recent word combinations. Longer contexts rapidly create more combinations, many absent from the available corpus. Neural models map discrete symbols into vectors and share parameters across contexts. A recurrent network goes further by maintaining a hidden summary: every new character updates the previous state, and that state produces the next-item prediction. In the original diagram below, horizontal connections carry the summary forward and upward connections turn it into an output. Autoregression describes the factorization of a probability distribution; recurrence describes a mechanism for calculating its factors.

![Original D2L diagram: a hidden state summarizes observed history and produces successive predictions. Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola; unchanged, CC BY-SA 4.0. Its time-index convention is shifted by one relative to our consume-then-predict convention.](https://ml-biomat.com/static/tutorials/machine-learning/figures/e2f6da6b0d7ca8881d88b52b.svg?v=e2f6da6b0d7c)

Figure 1Original D2L diagram: a hidden state summarizes observed history and produces successive predictions. Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola; unchanged, CC BY-SA 4.0. Its time-index convention is shifted by one relative to our consume-then-predict convention.

An ordinary RNN repeatedly applies a nonlinear state transformation, through which information from distant positions may weaken. LSTM, introduced in 1997, adds gated information pathways that learn what to write, retain, and expose. Our single-layer LSTM maps each character to a 24-dimensional embedding, updates a 64-dimensional hidden state and a 64-dimensional cell state, and outputs 28 candidate scores. After reading “the blue robot,” the stored state can help place the next prediction in the verb slot. During generation, caching these two states allows the model to process just the newly appended character.

$$
(h_t,c_t)=\operatorname{LSTM}(e(x_t),h_{t-1},c_{t-1}),\qquad a_t=W_oh_t+b_o,\quad p(x_{t+1}=j\mid x_{\le t})=\operatorname{softmax}(a_t)_j
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a0f31d9accd033224b859ce5.svg) | 24-dimensional embedding, 64-dimensional hidden state, and 64-dimensional cell state, all dimensionless learned vectors; c_t denotes state, distinct from external conditioning c in E1. |
| ![Formula](https://ml-biomat.com/static/agent-math/fd8f947de5568504529202fd.svg) | Output matrix of shape 28×64, bias of length 28, and logit vector of length 28; j indexes a candidate symbol. |
| ![Formula](https://ml-biomat.com/static/agent-math/efda7fd2544be4b97cf94699.svg) | Index of the last consumed input, all inputs through that position, and exponentiation normalized across candidates. |

The current character updates state before the state predicts the following character, so the target has not been read. Two logits (ln3,0) yield probabilities (3/4,1/4). Parameter count is 28×24+4×64×(24+64+2)+28×64+28=25,532, including both LSTM bias vectors.

A causal Transformer organizes history differently. Each position creates queries, keys, and values. Its query may compare with keys at the same position and to its left; a mask excludes positions to the right. Since all actual input tokens are known during training, attention calculations at different positions can proceed in parallel. RNNs and LSTMs retain a time-direction dependency through their states, even when a library accepts the complete sequence in one call. During ordinary generation, all three architectures must know the newly selected symbol before determining the next conditional distribution. A Transformer key-value cache saves repeated work without removing this probability dependency.

$$
A=\operatorname{softmax}_{\mathrm{row}}\!\left(\frac{QK^\top}{\sqrt d}+M\right),\qquad M_{ij}=\begin{cases}0&j\le i\\-\infty&j>i\end{cases},\qquad H=AV
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d62be4b9e5e1132c2311be54.svg) | Per-position queries, keys, and values; Q and K have shape S×d and V has shape S×d_v, with dimensionless learned features. |
| ![Formula](https://ml-biomat.com/static/agent-math/7f6c855c878161720ea2bf9f.svg) | S×S causal mask, S×S attention weights, and S×d_v mixed output; each row of A sums to one. |
| ![Formula](https://ml-biomat.com/static/agent-math/33b315fab1d16e258b12531b.svg) | Query index, key index, sequence length, query-key dimension, value dimension, and transpose. |

Adding negative infinity makes the exponential of a forbidden score zero. At the second input position, allowed scores (ln3,0) yield weights (0.75,0.25), while the third position receives zero regardless of its score. Because inputs are shifted relative to targets, attending to the current input still predicts the following symbol.

Our script checks the connection between complete-sequence evaluation and cached single-character evaluation. The maximum difference across their logits is about 3.8×10⁻⁶, reflecting floating-point execution paths. Forgetting to pass the recurrent state onward would leave each step seeing only its current character. Directly using a bidirectional LSTM for next-character prediction creates the opposite problem: the backward path can read information beyond the allowed prefix. Both mistakes can produce tensors of the expected shape while changing the meaning of the calculation. Data access must match the conditional probability being modeled.

## 4 Pixels and sound can also take turns

An image is usually presented all at once, but a model can impose an order: begin at the top-left and read each row from left to right. PixelRNN and PixelCNN, developed in 2016, used such factorizations for pixel generation. When predicting grayscale pixel 25, the preceding 24 pixels are available history; pixel 25 and subsequent raw pixels must remain hidden. Multiplying convolution weights by a fixed mask prevents access to the target through neighboring input positions. Color images additionally require an ordering or another suitable joint distribution for the R, G, and B channels.

![Left: raster ordering of a 7×7 image; 24 blue positions are available and orange pixel 25 is the target. Right: dependency graph for width-three layers with dilations 1/2/4, reaching 15 inputs; the horizontal axis gives relative input offsets.](https://ml-biomat.com/static/tutorials/machine-learning/figures/cd991f6bf2a04e0a2ac1f810.svg?v=cd991f6bf2a0)

Figure 2Left: raster ordering of a 7×7 image; 24 blue positions are available and orange pixel 25 is the target. Right: dependency graph for width-three layers with dilations 1/2/4, reaching 15 inputs; the horizontal axis gives relative input offsets.

A first-layer type-A mask excludes the center raw pixel. Later type-B masks can read center-position hidden features because those features already depend only on allowed history. Causality must survive every layer. Simple stacks of masked convolutions can also leave a blind region within the preceding image area; gated PixelCNN uses separate vertical and horizontal information streams to improve coverage. Our numerical example constructs a 5×5 type-A mask, adds one hundred to the current and all later pixels, and verifies that the selected convolution output remains exactly unchanged.

WaveNet, also introduced in 2016, makes the next item an audio sample. With thousands of samples per second, an audio model needs a substantial history while respecting temporal order. Causal convolution reads only to the left, and dilation enlarges the spacing between sampled positions. Our diagram uses three kernel-width-three layers with dilations one, two, and four; the final output reaches fifteen consecutive input positions. These deliberately small dimensions support hand calculation. The original WaveNet used deeper stacks and represented quantized waveform amplitudes with categorical predictions. Additional conditioning supplied information such as speaker identity or text.

$$
R=1+\sum_{\ell=1}^{L}(k_\ell-1)d_\ell
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/626b40094bfad3228e2e2b06.svg) | Input-position span of the receptive field and number of convolution layers; every stride is one, with left-only causal padding. |
| ![Formula](https://ml-biomat.com/static/agent-math/58668167964505b55812b3b7.svg) | Kernel width, dilation spacing, and layer index; counted in discrete positions without physical units. |

A width-k layer extends the leftmost dependency by (k−1)d positions. Add these spans and include the current position. Width three with dilations one,two,four gives R=1+2+4+8=15. These particular offsets reach every position from zero through fourteen; arbitrary dilation choices need not fill their entire span.

During training, causal convolution can compute losses throughout a known waveform in parallel. Ordinary generation still produces samples sequentially, explaining why parallel training can coexist with slow synthesis. Our code checks the dependency pattern directly: changing input positions sixteen onward leaves the first sixteen outputs unchanged. For a real-time speech application, the same architectural reasoning leads to concrete measurements: generated samples per second, required cache memory, and delay before playback. Those measurements answer different questions from the likelihood of held-out audio.

## 5 How temperature and truncation change the available choices

After training, network weights determine candidate scores, and a decoding rule determines how a choice is made from them. Greedy decoding selects the highest-probability candidate at every step, so the same prefix repeatedly produces the same continuation. Sampling retains uncertainty. Temperature acts before softmax: lowering it magnifies score differences, while raising it gives lower-scoring candidates more opportunity. This operation changes relative preferences among existing candidates. It neither retrains the model nor adds knowledge absent from its training data.

$$
q_j(\tau)=\frac{e^{a_j/\tau}}{\sum_{r\in\mathcal V}e^{a_r/\tau}},\qquad \widetilde q_j=\frac{q_j\,\mathbf1[j\in S]}{\sum_{r\in S}q_r}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/22cadef85af9a199f278e8e7.svg) | Candidate logit, positive temperature, and allowed candidate vocabulary; generation excludes PAD/BOS and retains EOS. All quantities are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/105a65b28864b4c6dc4b2901.svg) | Temperature-adjusted probability, subset retained by top-k or top-p, and renormalized sampling probability. |
| ![Formula](https://ml-biomat.com/static/agent-math/788d26357b24a3227edc7280.svg) | Candidate and summation indices and indicator equal to one for retained candidates and zero otherwise. |

Logits ln(0.6),ln(0.25),ln(0.1),ln(0.05) recover those probabilities at temperature one. Temperature two makes probabilities proportional to their square roots. Top-p=0.8 retains 0.6 and 0.25 and divides by 0.85. Subtracting the maximum logit for numerical stability cancels a common numerator-denominator factor.

Top-k keeps a fixed number of highest-probability candidates. Top-p keeps a variable-size set whose cumulative mass first reaches a chosen threshold. For probabilities 0.60, 0.25, 0.10, and 0.05, top-k with k=2 retains the first two and renormalizes them to approximately 0.705882 and 0.294118. A top-p threshold of 0.8 retains the same pair: the first item has insufficient mass, while adding the second reaches 0.85. The item that crosses the threshold must remain included. Removing it would leave less probability mass than requested. A confident spelling position may retain one character while a word-choice position retains several.

Nucleus sampling, introduced in work released in 2019, uses this adaptable candidate set to examine the relationship between likelihood-based decoding and textual diversity. A miniature language makes the distinction visible: the model is highly confident that “robo” continues with “t,” while “the ” offers several possible colors. Fixed k preserves the same number of candidates at both positions; cumulative-mass selection responds to how concentrated each distribution is. The interactive explorer below uses scores from our trained model at five actual prefixes. Selecting a character branch reveals the next distribution after appending it.

## Explore the branches after an actual prefix

Compare candidate mass with the final sampling distribution. Prefixes and five next-level branches come from the trained LSTM. Select a character button to inspect the distribution after appending it. Single draws use a fixed seed and do not automatically change the prefix.

[Figure: Actual next-character probabilities and cumulative mass](https://ml-biomat.com/tutorials/machine-learning/m36/en/#M36-board)

Blue shows temperature-adjusted probability before truncation; orange shows the retained, renormalized distribution. The right panel accumulates blue probabilities in descending order; the vertical line marks retained count. The twelve largest candidates are displayed, while calculations always use all twenty-six allowed candidates.

The probability originally assigned by the model and the probability used after truncation can differ substantially. Evaluate the original model with its original softmax, and explain a sampled choice using the distribution after temperature, truncation, and renormalization. Our test cross-entropy retains the complete 28-class distribution. Generation excludes PAD and BOS before sampling because neither is an ordinary continuation. The explorer displays this generation-time distribution. Keeping these quantities separate makes it possible to reproduce a sample without accidentally reporting a transformed sampling probability as model likelihood.

## 6 Searching for a sentence and sampling one are different operations

Greedy decoding may commit too early to a locally attractive branch. Suppose the first choice gives A probability 0.6 and B probability 0.4. The best continuation after A has probability 0.5, while the best after B has probability 0.9. Their complete-route probabilities are 0.30 and 0.36. Keeping the initially weaker B branch makes the better ending accessible. Beam search retains several candidate prefixes, expands them, and selects a new set using accumulated scores. Beam width determines how many routes survive and affects both model evaluations and stored states.

$$
s(y)=\sum_{t=1}^{n}\log p(y_t\mid y_{<t},c),\qquad s_\alpha(y)=\frac{s(y)}{((5+n)/6)^\alpha}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/f10d7d17cd9a5f667bc1a22d.svg) | Generated continuation, its item t, preceding generated items, and fixed prefix condition. |
| ![Formula](https://ml-biomat.com/static/agent-math/00fa1a2d18f9f99092a11597.svg) | Generated length including EOS but excluding the supplied prefix, and accumulated model log probability in nats. |
| ![Formula](https://ml-biomat.com/static/agent-math/3a8b88596ffec78c08c189d1.svg) | Length-normalization exponent, 0.7 here; transformed ranking score; five and six are constants defining this particular rule. |

At n=1 the denominator is one; at n=7 and α=1 it is two, changing raw score −4 into −2 and relatively favoring longer candidates. Setting α=0 restores raw log probability. Width four retains four candidates per round; it is a finite search rather than exhaustive optimization.

Complete sentences also differ in length. Adding more negative log probabilities lowers a longer sequence’s raw score. Our code supplies an explicit length normalization and counts EOS in the length; all candidates use the same comparison rule. Finished candidates remain in the beam without further extension. With beam width four and length exponent 0.7, the search returns “the green robot finds the key near the river.” Its accumulated log probability is approximately −6.446799 and its normalized score approximately −1.441288. The latter ranks candidates under this search rule and is no longer a sentence log probability.

Beam search is useful when seeking high-scoring candidates under an existing model, as in constrained transcription or translation. Sampling serves a different purpose when multiple alternatives are wanted. A larger beam explores more routes, although a finite beam can still discard an ultimately better path early. Length normalization also changes preferences, so task-level evaluation remains necessary. Repeating deterministic beam search on the same prefix produces the same result; a collection of varied designs or stories requires an additional diversity or sampling mechanism.

## 7 Actual training: choices and errors behind low perplexity

The corpus follows an explicit combinatorial grammar: six colors, four agents, three actions, five objects, and four places produce 1,440 sentences of the form “the … near the ….” Complete strings are unique. A fixed random permutation allocates 1,008 sentences to training, 216 to validation, and 216 to testing. The test set uses familiar words in complete combinations that were absent from training. Because this is a synthetic miniature language, we can check spelling and syntax against its complete rule set and determine exactly whether a generated string overlaps the training corpus.

The LSTM contains 25,532 parameters and trains for eighty epochs using Adam, learning rate 0.004, batches of at most sixty-four sentences, and gradient-norm clipping at one. Validation loss selects the final epoch. The left panel shows training and validation loss; the middle checks grammatical validity among one hundred generations per strategy; the right counts distinct complete strings. Held-out next-character accuracy is about 91.60%. Some positions genuinely allow several colors, agents, or other choices, so a sensible probability distribution need not make the same single choice as every particular test sentence.

![Training and validation losses for one LSTM, followed by grammatical validity and distinct strings among 100 complete generations per strategy, seeds 363–462. Distinct strings include malformed outputs. The dotted line marks validation-selected epoch 80.](https://ml-biomat.com/static/tutorials/machine-learning/figures/9e02b812858702688652b541.svg?v=9e02b8128587)

Figure 3Training and validation losses for one LSTM, followed by grammatical validity and distinct strings among 100 complete generations per strategy, seeds 363–462. Distinct strings include malformed outputs. The dotted line marks validation-selected epoch 80.

Temperature 0.7 produces one hundred valid sentences and ninety-six distinct strings. Temperature 1.0 produces ninety-nine valid sentences and ninety-five distinct strings. At temperature 1.3, validity falls to eighty-six while the number of distinct strings reaches ninety-seven. Greedy decoding produces one distinct string across all one hundred runs. Top-p with threshold 0.9 produces one hundred valid sentences and ninety-five distinct strings. Distinct-string counts include misspellings, so they must be read together with validity. Two additional strings might represent two additional errors rather than two additional useful ideas.

![First two outputs for each strategy in fixed seed order. Spelling errors and repetition are retained; the second temperature-1.3 string shows an actual continuation after leaving the grammar.](https://ml-biomat.com/static/tutorials/machine-learning/figures/efc8107614113722a5a2db37.svg?v=efc810761411)

Figure 4First two outputs for each strategy in fixed seed order. Spelling errors and repetition are retained; the second temperature-1.3 string shows an actual continuation after leaving the grammar.

The gallery preserves the first two outputs from each strategy. The second temperature-1.3 example begins “the cube narrie fox …”: an object appears where the grammar expects a color, followed by malformed spelling. During generation, that error becomes part of the next conditional input. Training generally supplied a valid prefix at the corresponding position. This makes error accumulation concrete. A character-probability heatmap helps distinguish legitimately uncertain word boundaries from within-word spelling positions that should concentrate on one character, guiding a choice among changing data, architecture, or decoding.

![Actual next-character probabilities while reading a specified complete sentence. Columns sum approximately to one; PAD/BOS rows are omitted. The space candidate is labeled space and input spaces use underscores. Colors share the 0–1 scale.](https://ml-biomat.com/static/tutorials/machine-learning/figures/2018a8bc30cd7db5d194dd45.svg?v=2018a8bc30cd)

Figure 5Actual next-character probabilities while reading a specified complete sentence. Columns sum approximately to one; PAD/BOS rows are omitted. The space candidate is labeled space and input spaces use underscores. Colors share the 0–1 scale.

The generated strings also make an important distinction between learning a rule and enumerating a fixed answer. The greedy sentence was not one of the training strings, yet it follows the same combinatorial grammar. That observation is consistent with reuse of learned word and slot patterns. The test likelihood examines a larger collection of held-out combinations, while the generation statistics examine behavior under the model’s own choices. Taken together, these views tell us more than either an appealing example or a single averaged accuracy.

## 8 Conditional continuation and a reproducible complete experiment

Conditional generation can begin with a known prefix. The script first reads “the blue robot ” and then predicts actions, objects, and places. Twenty top-p=0.9 samples all preserve that prefix and satisfy the grammar. More general conditions include a source sentence for translation, a speaker identity, or an image to describe. Such information must enter the conditional prediction at each relevant step. How the architecture reads it, and which relationships appeared during training, determine which attributes it can control. A written instruction becomes effective through learned conditioning relationships.

Sequence evaluation starts with the intended task. Density estimation uses held-out negative log-likelihood; transcription uses word or character error; structured output can be checked against field and format constraints. Open-ended generation additionally requires attention to content, repetition, and diversity. Our experiment saves sampled character probabilities, complete strings, ending status, and training-corpus overlap. Roughly seventy percent of several sampling sets coincide with training strings, while the training set itself covers seventy percent of this finite language. Such overlap has a specific context here and should be interpreted alongside held-out probabilities and generated behavior.

### Complete Python: character LSTM, six decoding settings, and beam search

Run python main.py --output results --language en with NumPy, Matplotlib, and PyTorch. The program creates its complete corpus and downloads no weights. Training, generation, probability plots, causality checks, and outputs are contained in one file.

```
"""A character-level LSTM language model trained on a fully specified grammar.
All sequences, split indices, weights, generated strings, and figures are saved.
"""
from pathlib import Path
import argparse, json, math, itertools, copy, platform
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('results'));p.add_argument('--language',choices=['en','zh'],default='en');args=p.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True);zh=args.language=='zh'
def tr(z,e):return z if zh else e
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','svg.fonttype':'none'})
def save(fig,name):fig.savefig(out/f'{name}-{args.language}.svg',bbox_inches='tight');plt.close(fig)
colors=['blue','red','gold','green','pink','white'];agents=['robot','pilot','otter','fox'];verbs=['carries','finds','moves'];objects=['cube','book','ball','key','bag'];places=['river','tower','garden','bridge']
sentences=[f'the {c} {a} {v} the {o} near the {r}.' for c,a,v,o,r in itertools.product(colors,agents,verbs,objects,places)]
vocab=['<pad>','<bos>','<eos>']+sorted(set(''.join(sentences)));stoi={s:i for i,s in enumerate(vocab)};V=len(vocab)
encoded=[[1]+[stoi[c] for c in s]+[2] for s in sentences];length=max(map(len,encoded));data=torch.zeros(len(encoded),length,dtype=torch.long)
for i,row in enumerate(encoded):data[i,:len(row)]=torch.tensor(row)
perm=np.random.default_rng(360).permutation(len(data));train_ids,val_ids,test_ids=perm[:1008],perm[1008:1224],perm[1224:]
class CharacterLSTM(nn.Module):
 def __init__(self):
  super().__init__();self.embedding=nn.Embedding(V,24,padding_idx=0);self.lstm=nn.LSTM(24,64,batch_first=True);self.head=nn.Linear(64,V)
 def forward(self,x,state=None):
  h,state=self.lstm(self.embedding(x),state);return self.head(h),state
torch.manual_seed(361);model=CharacterLSTM();optimizer=torch.optim.Adam(model.parameters(),lr=.004);order_rng=torch.Generator().manual_seed(362)
def evaluation(indices):
 model.eval();total=0.;tokens=0;correct=0
 with torch.no_grad():
  for idx in np.array_split(indices,max(1,math.ceil(len(indices)/128))):
   x=data[idx,:-1];y=data[idx,1:];logits,_=model(x);mask=y!=0;total+=F.cross_entropy(logits.reshape(-1,V),y.reshape(-1),ignore_index=0,reduction='sum').item();tokens+=mask.sum().item();correct+=((logits.argmax(-1)==y)&mask).sum().item()
 return dict(nll=total/tokens,perplexity=math.exp(total/tokens),accuracy=correct/tokens,tokens=tokens)
history=[];best=float('inf');best_epoch=0;best_state=None
for epoch in range(1,81):
 model.train();order=torch.randperm(len(train_ids),generator=order_rng);total=0.;count=0
 for part in order.split(64):
  idx=train_ids[part];x=data[idx,:-1];y=data[idx,1:];logits,_=model(x);loss=F.cross_entropy(logits.reshape(-1,V),y.reshape(-1),ignore_index=0);optimizer.zero_grad();loss.backward();nn.utils.clip_grad_norm_(model.parameters(),1);optimizer.step();n=(y!=0).sum().item();total+=loss.item()*n;count+=n
 valid=evaluation(val_ids);history.append([epoch,total/count,valid['nll']])
 if valid['nll']<best:best=valid['nll'];best_epoch=epoch;best_state=copy.deepcopy(model.state_dict())
model.load_state_dict(best_state);model.eval();test_metrics=evaluation(test_ids)
torch.save(dict(model=model.state_dict(),vocab=vocab,epoch=best_epoch),out/'character-lstm.pt')
def distribution(logits,temperature=1.,top_k=0,top_p=1.):
 logits=logits.astype('float64').copy()/temperature;logits[:2]=-np.inf;logits-=np.max(logits);probs=np.exp(logits);probs/=probs.sum();order=np.argsort(-probs,kind='stable');keep=np.ones(len(probs),dtype=bool)
 if top_k>0:keep[:]=False;keep[order[:top_k]]=True
 if top_p<1:
  # Keep the token that first reaches or crosses the requested cumulative mass.
  n=np.searchsorted(np.cumsum(probs[order]),top_p,side='left')+1;nucleus=np.zeros(len(probs),dtype=bool);nucleus[order[:n]]=True;keep&=nucleus
 probs*=keep;return probs/probs.sum()
@torch.no_grad()
def prefix_state(prefix):return model(torch.tensor([[1]+[stoi[c] for c in prefix]]))
@torch.no_grad()
def sample(prefix='',mode='sample',temperature=1.,top_k=0,top_p=1.,seed=0,max_new=80):
 logits,state=prefix_state(prefix);rng=np.random.default_rng(seed);text=prefix;trace=[];ended=False
 for _ in range(max_new):
  raw=logits[0,-1].numpy();prob=distribution(raw,temperature,top_k,top_p);token=int(prob.argmax()) if mode=='greedy' else int(rng.choice(V,p=prob));trace.append(dict(token=vocab[token],probability=float(prob[token])))
  if token==2:ended=True;break
  text+=vocab[token];logits,state=model(torch.tensor([[token]]),state)
 return dict(text=text,ended=ended,trace=trace)
@torch.no_grad()
def beam_search(prefix='',width=4,alpha=.7,max_new=80):
 logits,state=prefix_state(prefix);beams=[dict(text=prefix,score=0.,length=0,ended=False,logits=logits,state=state)]
 def rank(b):return b['score']/(((5+b['length'])/6)**alpha)
 for _ in range(max_new):
  candidates=[]
  for b in beams:
   if b['ended']:candidates.append(b);continue
   # Raw log probabilities retain the model's normalization, including special tokens.
   lp=F.log_softmax(b['logits'][0,-1],dim=-1);lp[:2]=-torch.inf
   for token in torch.topk(lp,width).indices.tolist():
    ended=token==2;new_logits,new_state=(b['logits'],b['state']) if ended else model(torch.tensor([[token]]),b['state'])
    candidates.append(dict(text=b['text']+('' if ended else vocab[token]),score=b['score']+lp[token].item(),length=b['length']+1,ended=ended,logits=new_logits,state=new_state))
  beams=sorted(candidates,key=rank,reverse=True)[:width]
  if all(b['ended'] for b in beams):break
 best=sorted(beams,key=rank,reverse=True)[0];return {k:best[k] for k in ['text','score','length','ended']}|dict(normalized_score=rank(best))
settings={'greedy':dict(mode='greedy'),'T0.7':dict(temperature=.7),'T1.0':dict(temperature=1.),'T1.3':dict(temperature=1.3),'top-k5':dict(top_k=5),'top-p0.9':dict(top_p=.9)}
generation={};metrics={};valid_set=set(sentences);training_set={sentences[i] for i in train_ids}
for name,options in settings.items():
 rows=[sample(seed=363+i,**options) for i in range(100)];generation[name]=rows;strings=[r['text'] for r in rows]
 metrics[name]=dict(valid=sum(s in valid_set for s in strings)/100,unique=len(set(strings)),ended=sum(r['ended'] for r in rows)/100,training_overlap=sum(s in training_set for s in strings)/100)
beam=beam_search();conditioned=[sample(prefix='the blue robot ',seed=463+i,top_p=.9) for i in range(20)]
# A small tree of actual next-character distributions for the browser explorer.
prefixes=['the ','the blue ','the blue robot ','the blue robot carries the ','the blue robot carries the book near the ']
lab_nodes=[]
for prefix in prefixes:
 logits,_=prefix_state(prefix);raw=logits[0,-1].numpy();options=[]
 for token in np.argsort(-distribution(raw))[:5]:
  if token<3:continue
  child,_=prefix_state(prefix+vocab[token]);options.append(dict(token=int(token),prefix=prefix+vocab[token],logits=child[0,-1].numpy().tolist()))
 lab_nodes.append(dict(prefix=prefix,logits=raw.tolist(),children=options))
(out/'decoding.json').write_text(json.dumps(dict(vocab=vocab,nodes=lab_nodes),ensure_ascii=False,separators=(',',':')),encoding='utf-8')
# Compare teacher-forced and cached sequential evaluation of identical known tokens.
with torch.no_grad():
 seq=data[test_ids[:1],:-1];whole,_=model(seq);parts=[];state=None
 for t in range(seq.shape[1]):
  pred,state=model(seq[:,t:t+1],state);parts.append(pred)
 sequential_error=float((whole-torch.cat(parts,1)).abs().max())
 # A causal dilated convolution reads only positions at or before its input index.
 torch.manual_seed(364);signal=torch.randn(1,1,32);altered=signal.clone();altered[:,:,16:]+=10
 def causal(x):
  for dilation in [1,2,4]:x=F.conv1d(F.pad(x,(2*dilation,0)),torch.tensor([[[.2,.3,.5]]]),dilation=dilation)
  return x
 causal_error=float((causal(signal)[:,:,:16]-causal(altered)[:,:,:16]).abs().max())
 mask=torch.ones(1,1,5,5);mask[:,:,3:]=0;mask[:,:,2,2:]=0
 img=torch.arange(49,dtype=torch.float32).reshape(1,1,7,7);changed=img.clone();changed.flatten()[24:]+=100
 pixel_error=float((F.conv2d(img,mask,padding=2)[0,0,3,3]-F.conv2d(changed,mask,padding=2)[0,0,3,3]).abs())
hand_p=np.array([.6,.25,.1,.05]);hand_k=hand_p.copy();hand_k[2:]=0;hand_k/=hand_k.sum();chain=.6*.5*.8
summary=dict(versions=dict(python=platform.python_version(),torch=torch.__version__,numpy=np.__version__),data=dict(sentences=len(sentences),train=len(train_ids),validation=len(val_ids),test=len(test_ids),vocabulary=V,max_padded_length=length,seed=360),training=dict(epochs=80,best_epoch=best_epoch,parameters=sum(p.numel() for p in model.parameters()),embedding=24,hidden=64,lr=.004,batch=64),test=test_metrics,generation=metrics,beam=beam,conditioned=dict(count=20,valid=sum(r['text'] in valid_set for r in conditioned)/20,prefix_preserved=all(r['text'].startswith('the blue robot ') for r in conditioned)),hand=dict(chain_probability=chain,chain_nll=-math.log(chain),chain_perplexity=chain**(-1/3),top_k_first=float(hand_k[0]),top_p_count=int(np.searchsorted(np.cumsum(hand_p),.8)+1),receptive_field=1+2*(1+2+4),sequential_logit_max_error=sequential_error,causal_future_error=causal_error,pixel_future_error=pixel_error))
(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(out/'generations.json').write_text(json.dumps(dict(unconditional=generation,beam=beam,conditioned=conditioned),ensure_ascii=False,indent=2),encoding='utf-8');(out/'corpus.json').write_text(json.dumps(dict(sentences=sentences,vocab=vocab,train_indices=train_ids.tolist(),validation_indices=val_ids.tolist(),test_indices=test_ids.tolist()),indent=2),encoding='utf-8')
np.savez_compressed(out/'experiment.npz',encoded=data.numpy(),train_indices=train_ids,validation_indices=val_ids,test_indices=test_ids,history=history,mask=mask.numpy())
fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained');h=np.array(history);axs[0].plot(h[:,0],h[:,1],label=tr('训练','Train'),color='#125f82');axs[0].plot(h[:,0],h[:,2],label=tr('验证','Validation'),color='#bf7139');axs[0].axvline(best_epoch,color='#555',ls=':',lw=1);axs[0].set(xlabel=tr('训练轮数','Epoch'),ylabel=tr('每字符负对数似然 / nats','NLL per character / nats'),title=tr('A  从字符规则到新组合','A  Learning unseen combinations'));axs[0].legend()
names=list(metrics);xs=np.arange(len(names));axs[1].bar(xs,[metrics[n]['valid'] for n in names],color='#125f82');axs[1].set_xticks(xs,names,rotation=35,ha='right');axs[1].set(ylim=(0,1.07),ylabel=tr('合乎语法的生成比例','Grammar-valid fraction'),title=tr('B  每种策略100次生成','B  100 generations per strategy'))
axs[2].bar(xs,[metrics[n]['unique'] for n in names],color='#bf7139');axs[2].set_xticks(xs,names,rotation=35,ha='right');axs[2].set(ylim=(0,105),ylabel=tr('不同完整字符串数','Distinct complete strings'),title=tr('C  同一模型的不同选择','C  Choices from the same model'));save(fig,'learning')
# A teacher-forced probability strip makes uncertain boundaries and certain spelling visible.
chosen='the blue robot carries the book near the river.';ids=torch.tensor([[1]+[stoi[c] for c in chosen]])
with torch.no_grad():prob=model(ids)[0].softmax(-1)[0].numpy().T
fig,ax=plt.subplots(figsize=(14,6),layout='constrained');im=ax.imshow(prob[2:,:],aspect='auto',vmin=0,vmax=1,cmap='YlGnBu');ax.set_yticks(range(V-2),[('EOS' if v=='<eos>' else 'space' if v==' ' else v) for v in vocab[2:]]);ax.set_xticks(np.arange(0,len(chosen)+1,2),['BOS' if i==0 else ('_' if chosen[i-1]==' ' else chosen[i-1]) for i in range(0,len(chosen)+1,2)]);ax.set(xlabel=tr('读入的当前字符（预测下一字符）','Current input character (predicting the following character)'),ylabel=tr('候选下一字符','Candidate next character'),title=tr('真实模型的条件概率：词内集中，选择词语时分散','Actual conditional probabilities: concentrated spelling, uncertain word choices'));fig.colorbar(im,ax=ax,label=tr('预测概率','Predicted probability'));save(fig,'probabilities')
fig,axs=plt.subplots(1,2,figsize=(12,5),layout='constrained');raster=np.arange(49).reshape(7,7);ax=axs[0];state=np.where(raster<24,1,np.where(raster==24,2,0));ax.imshow(state,cmap=matplotlib.colors.ListedColormap(['#e9e4d9','#71a6b8','#bd713f']),vmin=0,vmax=2)
for row in range(7):
 for col in range(7):ax.text(col,row,str(raster[row,col]+1),ha='center',va='center',fontsize=10)
ax.set(title=tr('A  预测第25个像素：只读蓝色历史','A  Predict pixel 25 using only blue history'),xlabel=tr('图像列：从左到右','Column: left to right'),ylabel=tr('图像行：从上到下','Row: top to bottom'))
ax=axs[1];offsets={0}
for row,d in enumerate([4,2,1]):
 new={i-j*d for i in offsets for j in range(3)}
 for i in offsets:
  for j in range(3):ax.plot([i,i-j*d],[3-row,2-row],color='#8ca8b4',lw=1)
 for i in new:ax.scatter(i,2-row,s=30,color='#125f82')
 offsets=new
ax.scatter(0,3,c='#bd713f',s=65);ax.set(xticks=range(-14,1,2),yticks=range(4),yticklabels=[tr('输入','Input'),'d=1','d=2','d=4'],xlabel=tr('相对当前输入的位置','Position relative to current input'),title=tr('B  核3、膨胀1/2/4覆盖15个位置','B  Kernel 3, dilation 1/2/4 spans 15 positions'));save(fig,'causality')
fig,ax=plt.subplots(figsize=(13,7.4));ax.axis('off');lines=[]
for name in ['greedy','T0.7','T1.0','T1.3','top-k5','top-p0.9']:
 lines.append((name,generation[name][0]['text'],generation[name][1]['text']))
for i,(name,a,b) in enumerate(lines):
 y=.96-i*.15;ax.text(0,y,name,color='#125f82',weight='bold',fontsize=13,transform=ax.transAxes);ax.text(.13,y,a,fontsize=11,transform=ax.transAxes);ax.text(.13,y-.05,b,fontsize=11,transform=ax.transAxes)
ax.set_title(tr('每种策略最先生成的两个字符串：保留实际拼写','The first two generated strings per strategy: actual spelling retained'),loc='left',pad=18);save(fig,'samples')
print(json.dumps(summary,indent=2))
```

The outputs support several levels of inspection. corpus.json contains every sentence and split assignment. generations.json contains all generated strings and their token traces. experiment.npz stores encoded inputs and training history. character-lstm.pt stores weights, vocabulary, and selected epoch, while decoding.json stores the actual prefix scores used by the explorer. An informative extension keeps the model and one hundred sampling seeds fixed, changes temperature or cumulative-mass threshold, and compares validity, distinct valid sentences, termination length, and word frequencies. Each observed difference then corresponds to a clear intervention in the generation procedure.

That workflow also connects the model families studied elsewhere. An LSTM and a causal Transformer can both implement an autoregressive distribution; a VAE can use an autoregressive decoder; an image model can generate discrete codes instead of raw pixels. These choices address separate questions about probability factorization, representation, and computation. Keeping them separate helps explain why “generative model” names a broad objective, while autoregression names a particular way of constructing and sampling a joint distribution.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M36.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Dive into Deep Learning: Working with Sequences](https://d2l.ai/chapter_recurrent-neural-networks/sequence.html)

   Conditional factorization and the original recurrent-state figure.

   CC BY-SA 4.0; original image retained unchanged
2. [Long Short-Term Memory](https://doi.org/10.1162/neco.1997.9.8.1735)

   Original 1997 gated-memory paper.

   Primary paper; no figure copied
3. [Long Short-Term Memory — author-hosted full text](https://people.idsia.ch/~juergen/lstm1997-2024head.pdf)

   Author-hosted free full text of the original 1997 paper.

   Primary paper; no figure copied
4. [PyTorch LSTM](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html)

   State shapes, weights, and two bias sets.

   Official API reference; independent code
5. [Pixel Recurrent Neural Networks](https://arxiv.org/abs/1601.06759)

   Pixel autoregression and PixelRNN/PixelCNN.

   Primary paper; no figure copied
6. [Conditional Image Generation with PixelCNN Decoders](https://arxiv.org/html/1606.05328v2)

   Masking, blind spots, conditioning, and two information streams.

   Primary paper; no figure copied
7. [WaveNet: A Generative Model for Raw Audio](https://arxiv.org/html/1609.03499v2)

   Dilated causal convolution and training/generation dependencies.

   Primary paper; independently constructed dependency diagram
8. [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751)

   Nucleus sampling through candidate probability mass.

   Primary paper; no figure copied
9. [Dive into Deep Learning: Beam Search](https://d2l.ai/chapter_recurrent-modern/beam-search.html)

   Candidate expansion and computational meaning of beam width.

   CC BY-SA 4.0 reference; independent worked example
10. [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

    Causal attention and position-parallel computation.

    Primary paper; no figure copied
11. [Google Neural Machine Translation](https://arxiv.org/abs/1609.08144)

    Length-normalized search scoring form.

    Primary paper; no figure copied
