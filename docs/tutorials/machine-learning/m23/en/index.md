# Find useful candidates, then rank them: retrieval and recommendation

Source: https://ml-biomat.com/tutorials/machine-learning/m23/en/
Language: en

Inspect term scores, search approximations, interaction feedback and temporal evaluation in a complete two-stage recommendation experiment.

## Finding a repair guide and recommending the next film

Your bicycle brake needs attention, so you search for “bike repair” and hope to see a repair guide before a city cycling map. A video service faces a related problem without an explicit query: it must infer what you might want to watch next from previous activity and current context. Information retrieval and recommendation both select a small useful set from many candidates. Their available evidence differs, and their evaluation targets should reflect that difference. One system primarily responds to a stated information need; the other must also infer interests and the purpose of the current visit.

Large catalogs commonly lead to two stages. Retrieval quickly finds a manageable candidate set; ranking compares those candidates more carefully. Think of locating a promising library shelf before inspecting individual tables of contents. A book omitted from the shelf cannot be selected by the second stage, however sophisticated that stage becomes. We therefore track candidate recall, final top-ten quality and computational work separately. These measurements describe whether a system finds relevant options, orders them well and can perform the required search at an acceptable cost.

The chapter begins with eight short documents whose words can all be inspected, proceeds to approximate search over 5,000 vectors, and then trains recommendation models for 80 users and 140 items. The latter datasets follow disclosed synthetic mechanisms. Interaction logs are divided chronologically into initial training, second-stage training and final testing. This scale supports complete CPU execution while exposing item availability, negative sampling and metric denominators. Many consequential errors in larger systems arise from precisely these definitions, rather than from the choice of a more elaborate network.

## Why should one word contribute more than another?

An inverted index reverses the relationship between documents and words. Instead of listing the words in each document, it lists the documents containing each word. In our corpus, bike points to D1 and D5, while repair points to D1 and D2; the postings also retain within-document counts. A query can merge these lists without rereading every document. As with an index at the back of a book, locating entries is separate from deciding which entry is most useful. Tokenization, case normalization, stemming and segmentation determine the searchable units, and the query must follow the same processing rules as the index.

TF-IDF combines two intuitions. A term repeated within a document may describe its subject, while a term present throughout the collection distinguishes documents poorly. Our implementation multiplies term frequency by a smoothed inverse document frequency, normalizes the whole vector, and compares query and document directions using cosine similarity. Normalization helps compare documents of different lengths. A rare model number may be highly informative; a widespread word such as guide contributes less. A rare typo can also receive substantial weight, which connects the scoring rule to practical decisions about text cleaning.

$$
w_{td}=f_{td}\left[\log\frac{N+1}{n_t+1}+1\right],\quad \widehat{\mathbf w}_d=\frac{\mathbf w_d}{\|\mathbf w_d\|_2},\quad s(q,d)=\widehat{\mathbf w}_q^\mathsf T\widehat{\mathbf w}_d
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2d2478f98dd73335a812d415.svg) | Term, document, query, document count and document frequency of term t; dimensionless counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/ec687a03bb96151ed8bf0df0.svg) | Term count, TF-IDF component and vocabulary-wide vector; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/61d920a4595219981b16f6e7.svg) | Normalized vector, Euclidean norm, transpose and cosine score; dimensionless. Zero vectors receive score zero. |

This is the code’s smoothed IDF. A term in one of four documents has IDF=log(5/2)+1≈1.916; frequency two gives component 3.833 before vector normalization. Queries use the same fitted vocabulary and IDF.

BM25 makes additional repetitions progressively less valuable and introduces a separate document-length adjustment. Writing bike ten times should not automatically produce ten times the score, and a long directory has more opportunities to mention a query word by chance. The Okapi team's 1994 TREC-3 report discusses term frequency, length and comparative retrieval evaluation: the methodological changes respond to these concrete problems. We use a common BM25 form with a positive smoothed IDF and display individual term contributions. Implementation variants in IDF, tokenization and query processing belong alongside the parameter settings when comparing results.

$$
s(q,d)=\sum_{t\in q}\log\left(1+\frac{N-n_t+0.5}{n_t+0.5}\right)\frac{f_{td}(k_1+1)}{f_{td}+k_1(1-b+bL_d/\overline L)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/33640683d4255f503365a392.svg) | Query, document, unique query term, document count, document frequency and term count; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/f1ad2a4a6689818aacf5aeda.svg) | Document length and collection-average length, in token counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/067d6b2017776921657ed11d.svg) | Frequency-saturation parameter, length-normalization strength and score; dimensionless, k1>0 and 0≤b≤1. |

Both numerator and denominator grow with frequency, producing saturation. N=8, df=2, tf=1 and b=0 give log(3.6)≈1.281 per term, or 2.562 for two such terms. Length increases the denominator when b>0.

![Left: bike and repair BM25 contributions in eight documents. Right: lexical, four-dimensional LSA and RRF ranks; 1 is best, with stable document-ID ties.](https://ml-biomat.com/static/tutorials/machine-learning/figures/603c9d7224f905668d8b6c6f.svg?v=603c9d7224f9)

Figure 1Left: bike and repair BM25 contributions in eight documents. Right: lexical, four-dimensional LSA and RRF ranks; 1 is best, with stable document-ID ties.

| ID | Contents |
| --- | --- |
| D1 | bike repair wheel brake guide |
| D2 | bicycle maintenance tire repair workshop |
| D3 | bread baking flour yeast oven |
| D4 | sourdough bread starter fermentation guide |
| D5 | city bicycle route bike travel map |
| D6 | train travel ticket station guide |
| D7 | python data matrix vector tutorial |
| D8 | search vector index ranking retrieval |

## Inspect each term contribution

Keep the query bike repair and eight documents fixed, while changing repetition and length in D1. Postings and term scores update with the parameters.

[Figure: BM25 term contributions and document scores](https://ml-biomat.com/tutorials/machine-learning/m23/en/#M23-plot)

For the default query bike repair, D1 contains both terms and scores approximately 2.588. D2 contains repair alone and scores 1.294. D5 contains bike alone and is one word longer, giving 1.197. The interaction lets you repeat bike in D1, append unrelated words, and change the saturation and length parameters. Repetition gains and length penalties then become visible separately. Setting the length parameter to zero removes the effect of unrelated padding on that document's score. Understanding the controlled behavior makes parameter selection more meaningful than memorizing a conventional default.

## Add vector evidence, then choose a fusion rule

Lexical retrieval handles exact names, identifiers and explicit terminology well, but can miss a useful document phrased differently. Vector retrieval maps queries and documents into a shared space and searches by inner product, cosine or distance. We first apply a four-dimensional singular-value decomposition to the TF-IDF matrix, producing an inspectable latent semantic analysis representation. Co-occurrence structure supports the compression from word coordinates to a smaller space. Its semantic usefulness depends on that structure and the corpus; reducing dimensionality by itself does not supply an understanding of every synonym or intended meaning.

$$
A=U\Sigma V^\mathsf T,\quad z_d=\mathbf w_d^\mathsf T V_r,\quad s(q,d)=\frac{z_qz_d^\mathsf T}{\|z_q\|_2\|z_d\|_2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9dfb718bce8fbf73a38d014f.svg) | Document-by-term TF-IDF matrix and singular-value factors; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/be148765b8f86fb526625511.svg) | Retained dimension, term-by-r right singular-vector matrix, document term vector and 1×r projected document/query vectors. |
| ![Formula](https://ml-biomat.com/static/agent-math/13c6cae25092da1039650016.svg) | Cosine score, Euclidean norm and transpose; dimensionless. |

Projection uses co-occurrence directions as coordinates. For zq=(1,0), zd=(1,1), cosine is 1/√2≈0.707. The code retains r=4 and treats zero projections as zero scores.

D1, D2 and D5 all concern bicycles and receive high similarities for the current query after the four-dimensional projection. A travel guide can also become closer through shared vocabulary, illustrating information that the compression mixes or loses. Modern dense retrievers commonly train encoders on relevant and irrelevant pairs so useful query–document relationships become nearby representations. Their performance depends on task-representative pairs and suitable negatives. Updating the query encoder also requires a compatible document index: keeping old document vectors while changing the query coordinate system creates a version mismatch that a faster search algorithm cannot resolve.

Hybrid retrieval combines lexical and dense channels. Adding raw scores requires attention to their different scales and distributions. Reciprocal rank fusion, RRF, instead adds functions of each channel's rank, using a constant to moderate the advantage of the highest positions. The experiment fuses BM25 and LSA with constant 60 and resolves ties consistently by document ID. This provides a transparent starting point. Channel weights and candidate counts should be selected on held-out queries, because exact identifier searches and broad natural-language questions may benefit from different mixtures of evidence.

$$
\operatorname{RRF}(d)=\sum_{j=1}^{J}\frac1{c+r_j(d)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d0fb244cdbf42016f7472d53.svg) | Document, channel index and channel count; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0c246eec0bb985ee8582cbba.svg) | One-based rank in channel j, positive smoothing constant and fused score; dimensionless. |

Use ranks rather than incompatible raw-score scales. First in both channels with c=60 gives 2/61≈0.032787; second in both gives 2/62≈0.032258. Ties here follow stable IDs.

A retrieval score is not automatically a probability. An inner product of 0.8 does not mean 80% relevance; a zero cosine means orthogonality under the current representation and inner product. With unit-normalized vectors, cosine and inner product give the same ordering. Without normalization, vector magnitude also contributes. Recording normalization, distance type and training objective in the index configuration helps explain ranking changes when a search component is replaced. These choices specify the comparison being performed, rather than serving as interchangeable implementation details.

## How much recall does scanning less data cost?

Exact search evaluates every database vector and provides a clear reference answer. Approximate nearest-neighbor methods reduce the work as catalogs grow. Our transparent inverted-file implementation, IVF, uses k-means to partition the database into 64 regions. A query selects the closest regions and computes exact distances only to vectors inside them. The inverted relationship is now region to vector IDs, echoing the organizational idea behind a term index. Neighbors in unopened regions can be missed, making the number of probed regions a direct control over approximation and scanning work.

![Candidate-distance work versus exact-neighbor recall for 64-cell IVF; labels give probe counts. Right: cell sizes. Each query additionally compares 64 centroids, outside the horizontal count.](https://ml-biomat.com/static/tutorials/machine-learning/figures/f5bc4700257f87d076b977d1.svg?v=f5bc4700257f)

Figure 2Candidate-distance work versus exact-neighbor recall for 64-cell IVF; labels give probe counts. Right: cell sizes. Each query additionally compares 64 centroids, outside the horizontal count.

The experiment compares 5,000 sixteen-dimensional vectors with 100 queries. Probing one region scans an average of 80.54 candidate vectors and retrieves 0.253 of the exact top-ten neighbors. Eight probes scan approximately 626.76 candidates with recall 0.753. Thirty-two probes scan 2,507.13 with recall 0.992. Searching all 64 regions scans 5,000 vectors and restores recall one. The horizontal axis counts candidate-distance evaluations; selecting regions also requires 64 centroid comparisons. This is a direct work measure, while wall-clock latency additionally depends on implementation, hardware, batching and memory access.

Regions do not contain equal numbers of vectors. The second panel shows their sizes, explaining why a fixed probe count can still produce variable work across queries. Production measurements should therefore include tail latency and difficult queries. HNSW navigates a multilayer neighbor graph, trading search breadth against recall. Product quantization, PQ, stores short codes for subvectors to reduce storage and distance-computation costs, introducing another approximation. Partitioning, graph navigation and quantization can be combined. Every new approximation calls for renewed comparison with exact neighbors and separate accounting of recall, memory and query work.

The Faiss getting-started tutorial introduces database vectors, query vectors, returned IDs and distances using an exact flat index before more complicated structures. That order is useful: fix the representation first and ask whether approximate search finds its neighbors faithfully. Then use relevance judgments to ask whether those neighbors are useful. ANN Recall@10 compares approximate results with exact vector neighbors. Recommendation Recall@10 compares a list with relevant items or future interactions. Keeping these denominators distinct locates problems in the index approximation or in the relationship between representation and task.

## What does a blank in the user–item matrix mean?

A rating is explicit feedback, while clicking, watching, saving and purchasing are often treated as implicit feedback. A missing click might reflect dislike, lack of exposure, limited time or a purchase elsewhere. A blank therefore has a different meaning from an expressed negative preference. Collaborative filtering uses shared interaction patterns: items selected by similar users may be useful neighbors. Our item-neighborhood baseline computes cosine similarity between interaction columns, retains the ten nearest neighbors for each candidate, and sums the evidence supplied by the user's historical items.

Matrix factorization learns a low-dimensional vector for each user and item, with an inner product producing a match score. Shared parameters distribute information across the sparse table. If several items in a user's history have large coordinates in one latent direction, training may move the user toward that direction as well. Such directions need not correspond individually to named concepts such as comedy or sport; jointly rotating the vectors can preserve all inner products. Neighbor relationships and changes in predictions provide firmer interpretation than assigning an untested semantic name to each coordinate.

![User–item matrix and its two low-rank factor matrices.](https://ml-biomat.com/static/tutorials/machine-learning/figures/f291c526f57824c2230065e8.svg?v=f291c526f578)

Figure 3Original matrix-factorization illustration: user and item factors reconstruct scores. Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola, Dive into Deep Learning, Fig. 21.3.1, CC BY-SA 4.0. Unmodified, retained under CC BY-SA 4.0; original page in references.

$$
\widehat R_{ui}=\mathbf p_u^\mathsf T\mathbf q_i,\qquad\widehat R=PQ^\mathsf T
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d572cf609be8ae51ebaa6bac.svg) | User and item indices, and latent dimension; dimensionless counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/5c59c6d3c83a1823c744de5b.svg) | User-by-k and item-by-k factor matrices and their k-dimensional vectors; learned coordinates. |
| ![Formula](https://ml-biomat.com/static/agent-math/b0822334e5c350d432390490.svg) | Match score, full score matrix and transpose. Scores here are dimensionless, not star ratings. |

Multiply corresponding coordinates and add. p=(1,2), q=(3,1) give 5; q=(0,1) gives 2. The code uses 12 factors trained with ranking loss.

Explicit rating prediction and implicit ranking use different training targets. To predict a star rating, fit squared error on observed entries and optionally include user and item biases, describing differences in rating generosity and broad item appeal. To select the next likely interaction, relative candidate order matters more. A model can improve rating mean-squared error while ordering the most useful few items poorly. Deciding how the page will use a model's output therefore comes before choosing its loss. The factorization structure can remain similar while the learning objective changes to match that decision.

The 2009 BPR paper formulated implicit recommendation as pairwise ranking: an observed item i should tend to rank above an unobserved comparison item j for user u. The training object is a triple rather than an isolated like/dislike label. For every positive training interaction, our code samples a comparison from the 120 items available during that period, excluding that user's training positives. A logistic loss favors the positive score over the comparison score. The sampled item can become a positive in the future; sampling uses only the history available at training time.

$$
\mathcal L=\frac1{|\mathcal D|}\sum_{(u,i,j)\in\mathcal D}\log\left[1+\exp\bigl(-(s_{ui}-s_{uj})\bigr)\right]
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7648b83134fd7aeb0e573c5d.svg) | Sampled triple set, its size, user, observed item and sampled comparison item. |
| ![Formula](https://ml-biomat.com/static/agent-math/dfee1a8dc0a4351aaa28654d.svg) | Dimensionless match scores and mean pairwise logistic loss. |
| ![Formula](https://ml-biomat.com/static/agent-math/e3f3d7dde4cc9b7b4cb6c489.svg) | Natural logarithm and exponential; implemented with stable softplus. |

A positive-minus-comparison margin 2 gives log(1+e^-2)≈0.127; margin −2 gives 2.127. Comparisons are resampled each epoch, excluding training positives; Adam separately uses weight decay 0.001.

Uniform negatives cover a broad catalog, popularity-based negatives more often resemble items users encounter, and hard negatives focus on candidates the model finds confusing. Harder examples can strengthen the learning signal while also increasing the chance of treating a potentially desirable item as negative. In-batch negatives reuse other examples' positive items, with special handling needed for duplicates and shared positives. Approximating a full-catalog softmax with sampled candidates also changes the normalization through the sampling distribution and may require correction. Negative sampling is consequently part of the statistical objective, not merely a way to accelerate otherwise identical arithmetic.

## Connect content through two towers, then rerank candidates

An ID-only factorization has little evidence for a newly introduced item. A two-tower model preserves an efficiently searchable inner-product structure while encoding user features and item features separately. Item features may contain categories, text or images; user features may summarize history and context. Both networks return vectors of the same dimension. Item vectors can be computed in advance, leaving a user-tower computation and index search at request time. A larger joint model can express richer pairwise interactions, but applying it to every user–item combination removes much of that reusable precomputation.

Each synthetic item has an eight-dimensional normalized content vector, and user preferences are generated in the same feature space. Interaction probabilities depend on preference match and item exposure weight. Each user selects one previously unseen item per day. The first 16 days supply 1,280 interactions for BPR matrix factorization and the two towers; the user tower receives the mean content vector of those 16 historical items. Days 17–20 supply 320 interactions for training the second-stage ranker. Days 21–24 provide 320 final test interactions, including 65 involving the 20 items introduced on day 21.

![Left: training interactions for the first 24 users; later items lie right of the orange line. Middle: actual BPR and tower training losses. Right: full-catalog top-ten evaluation over the final four days.](https://ml-biomat.com/static/tutorials/machine-learning/figures/42e7b39b96bdc0423b3cbe0b.svg?v=42e7b39b96bd)

Figure 4Left: training interactions for the first 24 users; later items lie right of the orange line. Middle: actual BPR and tower training losses. Right: full-catalog top-ten evaluation over the final four days.

Both neural models train for 160 epochs using pairwise loss. On the complete eligible test catalog, the two towers achieve Recall@10 around 0.359 and NDCG@10 around 0.307; BPR factorization achieves approximately 0.225 and 0.171. A simple content baseline, the inner product between mean historical content and item content, reaches recall 0.369, slightly above the two towers. The generating preferences already use a content inner product, making this baseline well matched to the mechanism. Extra network capacity provides no additional benefit in this sample. Training-loss improvement and test-ranking improvement are separate observations.

The second-stage learning-to-rank experiment uses a real XGBoost LambdaMART model. Candidate records are grouped by user as query groups; features contain tower score, factorization score, content similarity and training popularity. The ranker learns from the middle-period interactions and reranks only the tower's top 30 candidates at test time. Those candidates retrieve about 0.703 of future interactions, defining the range within which reranking can operate. The reranked top ten achieve recall approximately 0.350 and NDCG 0.293, slightly below the direct tower results. This concrete outcome motivates improvements to second-stage features, data and objectives.

## Cold starts and exposure change what a model learns

New items have no training interactions. ID-based factorization and the neighborhood model both have zero cold-item Recall@10 in this experiment. The content-based towers reach approximately 0.600, the direct content baseline 0.631, and reranking 0.446. The denominator is the 65 cold-item test interactions, while ranking still uses the whole eligible catalog. Cold starts can also involve new users, categories or regions. Content features supply similarities for some new objects; a genuinely new category outside the existing feature range calls for additional measurements, exploration and feedback.

![Left: cold-item recall within full-catalog ranking, with 65 test interactions as denominator. Right: generating exposure weight and training interaction count for 120 existing items.](https://ml-biomat.com/static/tutorials/machine-learning/figures/4193b60b587b554fd1a2cd93.svg?v=4193b60b587b)

Figure 5Left: cold-item recall within full-catalog ranking, with 65 test interactions as denominator. Right: generating exposure weight and training interaction count for 120 existing items.

Exposure bias combines the chance to see an item with the chance to choose it after seeing it. A homepage placement can increase interactions. A model trained only on clicks may learn placement advantage as apparent preference and then allocate even more exposure to the same item. The simulation makes exposure weights explicit, and its plot shows exposure alongside interaction counts with variation due to user preferences. Applied logs should retain impressions, positions, candidate sets, timestamps and subsequent behavior, so unshown, shown-but-unclicked and clicked-but-unsatisfactory outcomes remain distinguishable.

Randomized exploration creates comparable opportunities for less-exposed candidates. When logged assignment probabilities are known and support the target policy, inverse-propensity weighting can help evaluate another policy. Small probabilities create high-variance weights, making overlap and effective sample size useful diagnostics. Filling unexposed entries with arbitrary negative labels changes the question being learned. A practical starting point is to define whether the target is a click, completed viewing, satisfaction or longer-term retention, then collect the measurements and design the experiment that can evaluate that target.

## Make the metric match the page people will see

Recall@K measures how many relevant items appear in the first K positions. NDCG additionally values earlier positions and can represent graded relevance. Each test user here has four future interactions. The code excludes items seen in either training period, then ranks all remaining eligible items. Binary relevance assigns gain one to each hit, discounted more heavily at lower ranks. Replacing the full catalog with a small sample of negatives makes the ranking problem easier and changes the evaluation protocol. Metrics from these different candidate protocols should retain their own definitions and denominators.

$$
\operatorname{Recall@K}=\frac{|L_K\cap G|}{|G|},\quad\operatorname{DCG@K}=\sum_{r=1}^K\frac{2^{g_r}-1}{\log_2(r+1)},\quad\operatorname{NDCG@K}=\frac{\operatorname{DCG@K}}{\operatorname{IDCG@K}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ab6865610db5ec65193b681b.svg) | Displayed count, top-K set, relevant set, set size and intersection; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/6b3a844b884853058429fba8.svg) | One-based rank and relevance grade; code uses binary future interactions. |
| ![Formula](https://ml-biomat.com/static/agent-math/e0bc5c9a3a33a40b20fdb7f5.svg) | Discounted gain, ideal gain for the same relevance set, normalized gain and base-2 logarithm; dimensionless. |

With two relevant items at ranks 1 and 3, Recall@3=1, DCG=1+1/2=1.5, ideal DCG=1+1/log2(3)≈1.631 and NDCG≈0.920. Our four future interactions per user are evaluated then averaged across users.

Relevance judgments should reflect the actual task expressed by a query. For a brake-repair request, a direct adjustment guide might receive a high grade, a general maintenance guide a medium grade, and a cycling route a low grade despite containing bike. Annotators need shared judgment instructions, and ambiguous queries can retain multiple plausible intents. Purchases, completed viewing and accidental clicks likewise provide different evidence in recommendation. Defining relevance before discussing metrics reveals what a better ranking is expected to accomplish for the person using the system.

A temporal split keeps training information before the test period, while offline replay still reflects the logging policy's exposure. If a different system would show an item that was never displayed in a historical context, the log generally lacks that item's outcome in that context. Assigning every unobserved event a zero evaluates a specific observational protocol. An online randomized experiment compares behavior after actual display, using users or another stable assignment unit and considering outcome windows, weekly cycles and interference. Catalog coverage, repetition, new-item performance and retention can accompany average clicks to connect ranking quality with the broader experience.

Catalog operations also affect evaluation and serving. An unavailable item should leave the eligible set, changed content may require a new vector, and a newly introduced item must enter the index. Filtering stock only after retrieving ten neighbors can leave too few items to display; retrieving more candidates or using an index with filtering support addresses that interaction. Retain the encoder version, catalog snapshot, eligibility rules and index construction time. These records make a past result reconstructible and keep offline evaluation aligned with the candidates that were actually available for display.

### Complete experiment: BM25, IVF, BPR, two towers and LambdaMART

Run python main.py --output results --language en. No dataset download is required; the eight original documents and synthetic log are preserved. Outputs include four original figure groups, weights, time splits and metric summaries.

```
"""Inspectable lexical retrieval, IVF, BPR, two towers and chronological reranking."""
from pathlib import Path
import argparse,json,re
from collections import Counter,defaultdict
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from threadpoolctl import threadpool_limits
from xgboost import XGBRanker
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
DOCS=['bike repair wheel brake guide','bicycle maintenance tire repair workshop','bread baking flour yeast oven','sourdough bread starter fermentation guide','city bicycle route bike travel map','train travel ticket station guide','python data matrix vector tutorial','search vector index ranking retrieval']
def tokens(s):return re.findall('[a-z]+',s.lower())
def bm25(docs,query,k1=1.2,b=.75):
 cs=[Counter(tokens(d)) for d in docs];length=np.array([sum(c.values()) for c in cs]);N=len(docs);score=np.zeros(N);parts={}
 for t in sorted(set(tokens(query))):
  tf=np.array([c[t] for c in cs]);df=np.count_nonzero(tf);idf=np.log(1+(N-df+.5)/(df+.5));v=idf*tf*(k1+1)/(tf+k1*(1-b+b*length/length.mean()));score+=v;parts[t]=v
 return score,parts
def metrics(scores,truth,k=10):
 order=np.argsort(-scores,axis=1,kind='stable')[:,:k];hit=np.take_along_axis(truth,order,axis=1);den=truth.sum(1);rec=hit.sum(1)/np.maximum(den,1);discount=1/np.log2(np.arange(k)+2);ideal=np.array([discount[:min(int(n),k)].sum() for n in den]);ndcg=(hit*discount).sum(1)/np.maximum(ideal,1e-12);return {'recall':float(rec[den>0].mean()),'ndcg':float(ndcg[den>0].mean()),'coverage':float(len(np.unique(order))/scores.shape[1])},order
class MF(nn.Module):
 def __init__(self,nuser,nitem):
  super().__init__();self.u=nn.Embedding(nuser,12);self.v=nn.Embedding(nitem,12);nn.init.normal_(self.u.weight,std=.1);nn.init.normal_(self.v.weight,std=.1)
 def all_scores(self,uf,it):return self.u.weight@self.v.weight.T
class Towers(nn.Module):
 def __init__(self):
  super().__init__();self.u=nn.Sequential(nn.Linear(8,24),nn.Tanh(),nn.Linear(24,12));self.v=nn.Sequential(nn.Linear(8,24),nn.Tanh(),nn.Linear(24,12))
 def all_scores(self,uf,it):return self.u(uf)@self.v(it).T
def main(output,language):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh';L=lambda a,b:a if zh else b;rng=np.random.default_rng(23);torch.manual_seed(23);torch.set_num_threads(1)
 plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'DejaVu Sans','font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
 def save(fig,name):fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
 postings=defaultdict(list)
 for i,doc in enumerate(DOCS):
  for term,tf in Counter(tokens(doc)).items():postings[term].append([i,tf])
 lexical,parts=bm25(DOCS,'bike repair');vec=TfidfVectorizer();A=vec.fit_transform(DOCS).toarray();q=vec.transform(['bike repair']).toarray()[0];cos=A@q;U,S,Vt=np.linalg.svd(A,full_matrices=False);latent=A@Vt[:4].T;ql=q@Vt[:4].T;dense=latent@ql/np.maximum(np.linalg.norm(latent,axis=1)*np.linalg.norm(ql),1e-12)
 ranks1=np.argsort(np.argsort(-lexical,kind='stable'),kind='stable')+1;ranks2=np.argsort(np.argsort(-dense,kind='stable'),kind='stable')+1;rrf=1/(60+ranks1)+1/(60+ranks2)
 fig,axs=plt.subplots(1,2,figsize=(12,5),layout='constrained');terms=list(parts);base=np.zeros(8)
 for t in terms:axs[0].barh(np.arange(8),parts[t],left=base,label=t);base+=parts[t]
 axs[0].set(yticks=range(8),yticklabels=[f'D{i+1}' for i in range(8)],xlabel='BM25',title=L('查询 bike repair：逐词贡献','Query bike repair: term contributions'));axs[0].invert_yaxis();axs[0].legend();im=axs[1].imshow(np.c_[ranks1,np.argsort(np.argsort(-cos))+1,ranks2,np.argsort(np.argsort(-rrf))+1],cmap='Blues_r',vmin=1,vmax=8);axs[1].set(yticks=range(8),yticklabels=[f'D{i+1}' for i in range(8)],xticks=range(4),xticklabels=['BM25','TF-IDF','LSA','RRF'],title=L('同一语料的排名（1最好）','Ranks on the same corpus (1 is best)'))
 for i in range(8):
  for j,v in enumerate([ranks1[i],(np.argsort(np.argsort(-cos))+1)[i],ranks2[i],(np.argsort(np.argsort(-rrf))+1)[i]]):axs[1].text(j,i,str(v),ha='center',va='center',color='white' if v<=3 else '#20394a')
 save(fig,'lexical')
 # IVF uses Euclidean partitions; exact top10 provides retrieval ground truth.
 xb=rng.normal(size=(5000,16));xq=rng.normal(size=(100,16));km=KMeans(64,n_init=3,random_state=23).fit(xb);exact=np.argsort(((xq[:,None]-xb[None])**2).sum(2),axis=1)[:,:10];centers=np.argsort(((xq[:,None]-km.cluster_centers_[None])**2).sum(2),axis=1);trade=[]
 for probe in [1,2,4,8,16,32,64]:
  recalls=[];cost=[]
  for qi in range(100):
   ids=np.flatnonzero(np.isin(km.labels_,centers[qi,:probe]));chosen=ids[np.argsort(((xb[ids]-xq[qi])**2).sum(1))[:10]];recalls.append(len(set(chosen)&set(exact[qi]))/10);cost.append(len(ids))
  trade.append({'nprobe':probe,'recall10':float(np.mean(recalls)),'distance_evaluations':float(np.mean(cost))})
 fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained');axs[0].plot([d['distance_evaluations'] for d in trade],[d['recall10'] for d in trade],'o-',color='#247b94')
 for d in trade:axs[0].annotate(str(d['nprobe']),(d['distance_evaluations'],d['recall10']),xytext=(4,5),textcoords='offset points')
 axs[0].set(xlabel=L('每查询候选向量距离计算数','Candidate-vector distances per query'),ylabel='Recall@10',ylim=(0,1.06),title=L('5000向量，100查询，64分区','5,000 vectors, 100 queries, 64 cells'));axs[1].hist(np.bincount(km.labels_),bins=15,color='#d97b36');axs[1].set(xlabel=L('每分区向量数','Vectors per cell'),ylabel=L('分区数','Number of cells'),title=L('相同nprobe也会扫描不同数量','The same nprobe can scan different counts'));save(fig,'ivf')
 # Known synthetic preference plus exposure generates chronological unique interactions.
 nu,ni,warm=80,140,120;item=rng.normal(size=(ni,8));item/=np.linalg.norm(item,axis=1,keepdims=True);preference=rng.normal(size=(nu,8));preference/=np.linalg.norm(preference,axis=1,keepdims=True);utility=preference@item.T;exposure=np.linspace(1.5,.5,ni);log=[];seen=np.zeros((nu,ni),bool)
 for day in range(24):
  available=warm if day<20 else ni
  for u in range(nu):
   prob=np.exp(5*utility[u,:available])*exposure[:available];prob[seen[u,:available]]=0;prob/=prob.sum();i=int(rng.choice(available,p=prob));seen[u,i]=True;log.append((u,i,day))
 log=np.array(log);train=np.zeros((nu,ni),bool);stage2=train.copy();test=train.copy()
 for u,i,t in log:(train if t<16 else stage2 if t<20 else test)[u,i]=True
 uf=train@item/16;uft=torch.tensor(uf,dtype=torch.float32);it=torch.tensor(item,dtype=torch.float32);users,pos=np.where(train);users_t=torch.tensor(users);pos_t=torch.tensor(pos);available_neg=[np.flatnonzero(~train[u,:warm]) for u in range(nu)];models={};traces={};rawscores={}
 for name,model in [('BPR-MF',MF(nu,ni)),('Two-tower',Towers())]:
  opt=torch.optim.Adam(model.parameters(),lr=.025,weight_decay=.001);losses=[]
  for epoch in range(160):
   neg=torch.tensor([rng.choice(available_neg[u]) for u in users]);scores=model.all_scores(uft,it);loss=F.softplus(-(scores[users_t,pos_t]-scores[users_t,neg])).mean();opt.zero_grad();loss.backward();opt.step();losses.append(float(loss.detach()))
  models[name]=model;traces[name]=losses;rawscores[name]=model.all_scores(uft,it).detach().numpy();torch.save(model.state_dict(),out/(name.lower().replace('-','_')+'.pt'))
 popularity=train.sum(0);norm=train/np.maximum(np.sqrt(train.sum(0)),1);sim=norm.T@norm;np.fill_diagonal(sim,0);keep=np.zeros_like(sim,bool);top=np.argsort(-sim,axis=0,kind='stable')[:10];np.put_along_axis(keep,top,True,axis=0);sim*=keep;rawscores['Item-kNN']=train@sim;rawscores['Popularity']=np.tile(popularity,(nu,1));rawscores['Content']=uf@item.T
 def features(u,ids):return np.c_[rawscores['Two-tower'][u,ids],rawscores['BPR-MF'][u,ids],rawscores['Content'][u,ids],np.log1p(popularity[ids])]
 xx=[];yy=[];qid=[]
 for u in range(nu):
  ids=np.flatnonzero(~train[u,:warm]);xx.append(features(u,ids));yy.extend(stage2[u,ids].astype(int));qid.extend([u]*len(ids))
 ranker=XGBRanker(n_estimators=100,max_depth=3,learning_rate=.05,objective='rank:ndcg',tree_method='hist',n_jobs=1,random_state=23,lambdarank_num_pair_per_sample=10);ranker.fit(np.vstack(xx),np.array(yy),qid=np.array(qid));ranker.save_model(out/'reranker.json')
 history=train|stage2;results={};rankings={};candidate_recall=[];rerank=np.full((nu,ni),-1e12)
 for name,s in rawscores.items():
  masked=s.copy();masked[history]=-1e12;results[name],rankings[name]=metrics(masked,test)
 for u in range(nu):
  s=rawscores['Two-tower'][u].copy();s[history[u]]=-1e12;ids=np.argsort(-s,kind='stable')[:30];candidate_recall.append(test[u,ids].sum()/4);rerank[u,ids]=ranker.predict(features(u,ids))
 results['Tower+rerank'],rankings['Tower+rerank']=metrics(rerank,test);cold={}
 for name,ranking in rankings.items():cold[name]=float(sum(test[u,ranking[u][ranking[u]>=warm]].sum() for u in range(nu))/test[:,warm:].sum())
 fig,axs=plt.subplots(1,3,figsize=(15,4.8),layout='constrained');axs[0].imshow(train[:24],aspect='auto',cmap='Blues',interpolation='nearest');axs[0].axvline(warm-.5,color='#d97b36');axs[0].set(xlabel=L('物品ID','Item ID'),ylabel=L('用户ID（前24人）','User ID (first 24)'),title=L('前16天的交互矩阵','First 16 days: interaction matrix'))
 for name,loss in traces.items():axs[1].plot(loss,label=name)
 axs[1].set(xlabel=L('训练轮数','Training epoch'),ylabel=L('成对softplus损失','Pairwise softplus loss'));axs[1].legend(fontsize=9);names=list(results);ix=np.arange(len(names));axs[2].barh(ix-.16,[results[n]['recall'] for n in names],height=.3,label='Recall@10');axs[2].barh(ix+.16,[results[n]['ndcg'] for n in names],height=.3,label='NDCG@10');axs[2].set(yticks=ix,yticklabels=names,xlabel=L('后四天，全候选评价','Last four days, full eligible catalog'));axs[2].legend(fontsize=8);save(fig,'recommendation')
 fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained');axs[0].barh(names,[cold[n] for n in names],color='#247b94');axs[0].set(xlabel=L('冷启动交互Recall@10','Cold-item interaction Recall@10'),title=L('20件物品从第21天才可见','20 items become available on day 21'));axs[1].scatter(exposure[:warm],popularity[:warm],color='#d97b36',s=28,alpha=.7);axs[1].set(xlabel=L('生成曝光权重','Generating exposure weight'),ylabel=L('训练交互次数','Training interaction count'),title=L('点击同时受偏好与曝光影响','Interactions mix preference and exposure'));save(fig,'cold_exposure')
 summary={'documents':DOCS,'query':'bike repair','bm25_scores':lexical.tolist(),'tfidf_scores':cos.tolist(),'lsa_scores':dense.tolist(),'rrf_scores':rrf.tolist(),'lexical_order':np.argsort(-lexical,kind='stable').tolist(),'ivf':trade,'users':nu,'items':ni,'warm_items':warm,'log_count':len(log),'train_count':int(train.sum()),'stage2_count':int(stage2.sum()),'test_count':int(test.sum()),'cold_test_count':int(test[:,warm:].sum()),'train_test_overlap':int((train&test).sum()),'results':results,'cold_recall':cold,'candidate_recall30':float(np.mean(candidate_recall)),'loss_initial':{k:v[0] for k,v in traces.items()},'loss_final':{k:v[-1] for k,v in traces.items()},'train_last_day':int(log[log[:,2]<16,2].max()),'test_first_day':int(log[log[:,2]>=20,2].min())}
 summary.update({'postings':dict(postings),'item_neighbors':10,'ivf_full_recall':trade[-1]['recall10'],'ivf_full_distance_count':trade[-1]['distance_evaluations']})
 np.savez_compressed(out/'experiment_data.npz',log=log,item_features=item,user_preferences=preference,exposure=exposure,train=train,stage2=stage2,test=test,user_features=uf,ivf_database=xb,ivf_queries=xq,ivf_labels=km.labels_,ivf_centers=km.cluster_centers_,exact_neighbors=exact,**{k.replace('-','_').replace('+','_'):v for k,v in rawscores.items()});(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args()
 with threadpool_limits(limits=1):main(a.output,a.language)
```

The complete code saves documents, postings, timestamps, interaction matrices, content features, model weights, ranking metrics and plotting arrays. First change a query and inspect term scores. Then vary IVF probes and inspect neighbor recall. Finally change exposure or new-item availability and retrain to examine cold-start results. Changing one mechanism at a time lets you trace an effect through indexing, representation, sampling, retrieval and ranking. A useful retrieval or recommendation system emerges from these connected, inspectable decisions.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M23.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Robertson et al., Okapi at TREC-3 (1994)](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/okapi_trec3.pdf)

   Original term-frequency, length and retrieval-evaluation problem.

   Primary paper; no figure copied
2. [Introduction to Information Retrieval](https://nlp.stanford.edu/IR-book/)

   Inverted indexes, weighting, vector spaces and retrieval evaluation.

   Authors’ public text; reference
3. [Faiss — Getting started](https://github.com/facebookresearch/faiss/wiki/Getting-started)

   Exact vector-search interface and baseline for approximate indexing.

   MIT project
4. [Dive into Deep Learning — Matrix Factorization](https://d2l.ai/chapter_recommender-systems/mf.html)

   Original factor-model illustration and observed-rating fitting.

   Figure CC BY-SA 4.0, unmodified
5. [Rendle et al. (2009), Bayesian Personalized Ranking](https://proceedings.mlr.press/r7/rendle09a.html)

   Implicit-feedback triples and pairwise ranking.

   Primary reference
6. [TensorFlow Recommenders — Basic retrieval](https://www.tensorflow.org/recommenders/examples/basic_retrieval)

   Query and item towers, retrieval and ranking stages.

   Official tutorial; independent PyTorch experiment
7. [XGBoost — Learning to rank](https://xgboost.readthedocs.io/en/stable/tutorials/learning_to_rank.html)

   Query groups, LambdaMART and position bias.

   Apache-2.0 project
