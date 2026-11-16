# Finding unlabeled structure: PCA, clustering and anomalies

Source: https://ml-biomat.com/tutorials/machine-learning/m06/en/
Language: en

Use real digit images, shape comparisons and false alarms to examine what compression, clustering and maps preserve.

## Clear questions are possible without answer labels

Organizing a phone's photo collection seems natural: put photographs of the same person together, separate trips by location, then find blurry or duplicate pictures. Yet similarity has several meanings. A seaside group photograph can belong near an indoor portrait because it shows the same person, or near photographs of the sky because both contain a blue background. Unsupervised learning begins in this situation. Objects are available, but no answer column specifies how they should be organized. An algorithm needs a computable objective, and the reader first needs to decide which relationships matter.

This chapter connects four objectives. Dimension reduction describes objects with fewer numbers; clustering organizes them into groups; density estimation describes where observations concentrate; anomaly detection prioritizes records for inspection. These operations can form a workflow, but their outputs differ. A two-dimensional map supplies coordinates, clustering supplies group identifiers, density describes probability concentration per unit volume, and an anomaly score measures unusualness under a particular definition. Deciding whether the end use is browsing, compression or an alert establishes a basis for choosing distances, parameters and evaluation criteria.

The main experiment uses the 1,797 eight-by-eight digit images bundled with scikit-learn, originating from UCI's Optical Recognition of Handwritten Digits and the work of E. Alpaydin and C. Kaynak, under CC BY 4.0. Each image becomes 64 values, divided by 16 to lie between zero and one. Additional moon-shaped, elliptical, normal and anomalous observations are generated explicitly so their mechanisms can be compared with algorithm outputs. Digit labels are used for stratified splitting and coloring completed maps; PCA, t-SNE and UMAP fitting never reads those labels.

## Similarity begins with the measuring scale

Imagine organizing products by price and weight. Two products differ by 100 currency units and 0.1 kilograms. Squaring and adding these raw differences makes price dominate the distance. Expressing price in units of ten thousand changes the geometry again, although the products remain identical. Standardization subtracts a training mean and divides by a training standard deviation, expressing a difference in units of typical variation. This reduces domination by numerical scale, while also deciding that typical variation in different features deserves comparable weight. It remains a modeling choice rather than an automatic definition of relevance.

$$
z_j=\frac{x_j-\mu_j}{s_j},\quad d(z,v)=\sqrt{\sum_{j=1}^{d_f}(z_j-v_j)^2},\quad \operatorname{cos}(a,b)=\frac{a^\mathsf Tb}{\|a\|_2\|b\|_2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/212957f061a4837e3688ae41.svg) | Original feature, training mean, positive training standard deviation and feature index; the first three share feature units, and zero-variance features need separate handling. |
| ![Formula](https://ml-biomat.com/static/agent-math/f0a4b57a130481b83378460b.svg) | Standardized vector, another standardized vector, feature count and Euclidean distance; standardized coordinates and distance are unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/de4a4793c577391ef6bbe08e.svg) | Nonzero vectors of equal dimension, Euclidean norm, transpose and cosine similarity; similarity is unitless, with consistent coordinate units across vectors. |

A price of 120 and weight of 12 kg, with training means 100 and 10 kg and standard deviations 20 and 2 kg, standardize to (1,1), at distance √2 from the mean. Vectors (1,0) and (2,0) have Euclidean distance one and cosine one: different lengths, identical direction.

Euclidean distance treats coordinate differences as geometric displacements that accumulate through squared length. Cosine similarity focuses on direction: word-frequency vectors for two documents can point in similar directions even when one document is longer. Manhattan distance adds absolute coordinate differences, while Mahalanobis distance uses covariance to account for correlated variation. Translate these choices back into the question. Does total purchasing volume matter, or the proportions purchased? Do two strongly correlated measurements repeatedly describe one underlying event? A zero vector has no cosine direction, so its handling must be defined before applying that similarity.

All 64 coordinates in the digit experiment use the same grayscale unit. Dividing every value by 16 preserves relative pixel differences. Standardizing each pixel separately would amplify small fluctuations at border pixels that are usually almost black, thereby changing image distances. Shifting a digit by one pixel can also produce a large pixel distance although a person recognizes the same digit. Raw pixels are therefore one particular representation. If neural-network features replace them later, investigate which transformations the new representation preserves and which it ignores. Representation and distance always work together.

As dimensions increase, many unrelated noise coordinates can accumulate into distance and obscure informative differences. Responses include removing uninformative features, choosing task-relevant weights or learning a lower-dimensional representation. The order of these operations matters for evaluation. When processing future objects, learn means, scales and projection directions from training observations and apply them to new objects. When browsing one fixed collection, the entire collection can instead be the declared descriptive population. Both tasks have sensible workflows, provided that the analysis population corresponds to the intended use.

## PCA preserves variation, and its compression loss is measurable

A direct way to represent a point cloud with a line is to minimize perpendicular distances from the points to that line. Pearson's 1901 study of lines and planes of closest fit brought this geometric question into statistical investigation. PCA follows the same idea: center the point cloud and find mutually perpendicular directions that retain as much variation as possible. The first direction follows its greatest extension; the second retains as much remaining variation as possible while staying perpendicular to the first. Here importance means variance, before considering which differences matter for classification or another research objective.

$$
z_i=V_k^\mathsf T(x_i-\mu),\quad\widehat x_i=\mu+V_kz_i,\quad E_k=\frac1n\sum_{i=1}^n\|x_i-\widehat x_i\|_2^2,\quad V_k^\mathsf TV_k=I_k
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/10d2411af09e9ba80eb7f88b.svg) | Observation count, index, original feature dimension and retained rank, no greater than the feature dimension. |
| ![Formula](https://ml-biomat.com/static/agent-math/e00cb86ad595f6fecb8e7e9d.svg) | Original vector, training mean and reconstructed vector, each of dimension d_f; dimensionless rescaled pixels here. |
| ![Formula](https://ml-biomat.com/static/agent-math/c271bce45296621ac9590a40.svg) | d_f-by-k matrix of orthonormal directions, k-dimensional projected coordinates and k-by-k identity; directions are unitless and coordinates share input units. |
| ![Formula](https://ml-biomat.com/static/agent-math/cc49eec661d93602ca36b4ac.svg) | Mean total squared reconstruction error per observation and Euclidean norm; E has squared-input units. Reported per-pixel image MSE divides this quantity by 64. |

With zero mean, projecting (2,1) onto the horizontal unit vector gives coordinate two, reconstruction (2,0) and squared error one. Original squared length five separates into retained four and residual one. Orthogonality cancels the cross term, connecting maximum retained variance with minimum squared reconstruction error.

A projection resembles a shadow. Changing the viewing direction can preserve an object's long axis or compress it almost to a point. Under orthogonal projection, a centered vector separates into a retained component and a perpendicular residual. Their squared lengths add to the original squared length. With total variation fixed, maximizing retained variance therefore minimizes squared reconstruction error. The interactive example uses five points whose total mean squared length is 2.56. Horizontal projection retains 2 and discards 0.56; rotating the direction shows these two quantities trading against each other.

## Project a point cloud onto one line

Blue points are five centered observations, orange points their orthogonal projections, and connectors the reconstruction residuals. Change angle or select an observation to compare retained variance, discarded variance and its residual. Coordinates are dimensionless.

[Figure: Orthogonal projection and variance decomposition](https://ml-biomat.com/tutorials/machine-learning/m06/en/#M06-plot)

The digit experiment learns PCA directions from 1,347 images and reserves 450 images for reconstruction assessment. With two components, test pixel mean squared error is about 0.05277. Ten components reduce it to 0.01954, twenty to 0.00837, and forty to 0.000919. Each figure column contains the same held-out image as the retained rank increases from top to bottom. This lets the reader identify which strokes return first. Every image uses the same grayscale range, so apparent visual improvement and numerical error share a comparable measurement scale.

![Six held-out digits remain in their columns as PCA rank increases. Right: pixel MSE on 450 held-out images and training cumulative variance. Grayscale is fixed from zero to one. Data: UCI Optical Recognition of Handwritten Digits, CC BY 4.0; original computed figure.](https://ml-biomat.com/static/tutorials/machine-learning/figures/18ecc23b061d2af0de5678f0.svg?v=18ecc23b061d)

Figure 1Six held-out digits remain in their columns as PCA rank increases. Right: pixel MSE on 450 held-out images and training cumulative variance. Grayscale is fixed from zero to one. Data: UCI Optical Recognition of Handwritten Digits, CC BY 4.0; original computed figure.

At all 64 components, reconstruction error approaches floating-point rounding levels because a complete orthogonal basis spans the original space. Twenty components already retain approximately 89.6% of training variance, yet may still lose a short stroke distinguishing similar digits. Compression should be assessed through reconstruction, while classification requires an additional predictive evaluation. Cumulative explained variance helps read the trade-off but supplies no universal adequacy threshold. Large-variance noise can receive priority under PCA; low-variance but discriminative directions may require a supervised objective or domain knowledge to recognize their value.

## The clustering rule defines what a group means

K-means assigns each point to its nearest center, then moves each center to the mean of its assigned points. With centers fixed, nearest-center assignment minimizes each squared distance. With assignments fixed, the arithmetic mean minimizes the within-group squared-error sum. These alternating improvements explain why the objective generally decreases and why the method favors compact groups around centers. Different initial centers can lead to different local solutions, so the code uses multiple initializations. Increasing the group count also decreases training distortion, making stability, intended use or another criterion necessary when choosing the count.

$$
J=\sum_{i=1}^n\|x_i-c_{g_i}\|_2^2,\qquad c_k=\frac1{|A_k|}\sum_{i\in A_k}x_i
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/43f2ec92374b1c86b9b64c3e.svg) | Observation count, index and d_f-dimensional feature vector under a consistent scale convention. |
| ![Formula](https://ml-biomat.com/static/agent-math/14399b8dddaeab27160ff5ed.svg) | Group count, group index, assigned group, center, membership set and its nonzero size. |
| ![Formula](https://ml-biomat.com/static/agent-math/614eb99191286bb013cad6c9.svg) | Total squared-distance objective and Euclidean norm; squared feature units, or unitless after standardization. |

Grouping one-dimensional points (0,2) and (8,10) gives centers one and nine and total squared distance four. One group has center five and total distance 68. More groups can lower training distortion, requiring an additional basis for complexity selection.

Moon-shaped data make the preference visible. Each curved moon is connected, but its ends lie far from its own mean, encouraging k-means to carve compact geometric regions across the shapes. Hierarchical clustering instead starts with individual objects and repeatedly merges groups, recording the sequence in a dendrogram. Single linkage compares the nearest pair across groups and can follow thin chains. Complete linkage compares the farthest pair and emphasizes group diameter. Ward linkage chooses the merge with the smallest increase in within-group squared error. Each linkage defines a different relationship between groups rather than one universal meaning of nearest.

DBSCAN asks which points have enough neighbors and whether dense regions connect. A point with enough neighbors inside a specified radius is a core point. A nearby point without enough neighbors of its own can become a border point, while points outside these connected regions receive a noise label. The implementation's minimum sample count includes the point itself. Connections propagate between core points, permitting curved clusters without specifying their number beforehand. When densities differ strongly, one radius can fragment a sparse group while joining regions around a dense group; radius selection then reflects a substantive scale assumption.

![The same 500 moon and 500 ellipse observations pass through three algorithms. Colors indicate fitted groups and gray denotes DBSCAN noise. ARI compares grouping with generating labels; noise counts appear alongside it.](https://ml-biomat.com/static/tutorials/machine-learning/figures/1c479d9b288f8b05dc8ae385.svg?v=1c479d9b288f)

Figure 2The same 500 moon and 500 ellipse observations pass through three algorithms. Colors indicate fitted groups and gray denotes DBSCAN noise. ARI compares grouping with generating labels; noise counts appear alongside it.

For the 500 generated moon observations, the chosen DBSCAN parameters recover the two generating shapes with adjusted Rand index, or ARI, equal to one. K-means and the two-component GMM give about 0.257 and 0.523. On elliptical data, GMM gives approximately 0.921 and k-means 0.906, while DBSCAN labels 31 observations as noise. These scores use saved generating labels: ARI compares whether pairs belong together and corrects for chance agreement, so exchanging group numbers leaves the score unchanged. Without labels, investigate resampling stability and boundary objects instead of treating an internal score as evidence of natural categories.

![Clustering algorithms compared across different dataset shapes](https://ml-biomat.com/static/tutorials/machine-learning/figures/f9722ff1d6f26abfb41607ed.png?v=f9722ff1d6f2)

Figure 3Original algorithm-by-shape comparison by the scikit-learn developers, BSD-3-Clause, unmodified. Read rows for the same dataset and columns for the same algorithm; timings belong to the original example.

The official comparison figure places more shapes side by side. Read along a row to ask how the same observations are organized, then down a column to ask which shapes one rule favors. Its additional algorithms provide a broader map of available approaches. The actual experiments here focus on k-means, GMM and DBSCAN, with a separate six-observation hierarchical example showing every merge. Use the original figure to generate questions, then return to saved inputs and explicit parameters to distinguish a method's structural preference from the effects of one parameter choice.

Silhouette is another internal diagnostic: it compares a point's mean distance to its own group with its mean distance to the nearest other group. If these distances are two and five, their difference three divided by the larger distance five gives 0.6, placing the point closer to its own group under the chosen metric. The criterion favors compact, separated geometry, so a connected curved moon may receive a less favorable score. Interpret the geometry preferred by the metric alongside the algorithm. Resampling comparisons must also account for arbitrary group-number exchanges; pairwise co-membership provides a more meaningful target than numerical label equality.

## A Gaussian mixture supplies soft membership and density

When two populations overlap in measurement space, assigning every boundary object to one group discards information. A Gaussian mixture describes the population as a weighted sum of elliptical probability distributions. Each component has a center, covariance and mixture proportion. The center describes a typical location, covariance describes scale and orientation, and the proportion describes the chance of drawing an observation from that component. An object can have different probabilities of membership in the components. These responsibilities are conditional probabilities of latent component membership after observing that object's feature values.

$$
p(x)=\sum_{k=1}^K\pi_k\mathcal N(x\mid\mu_k,\Sigma_k),\qquad r_{ik}=\frac{\pi_k\mathcal N(x_i\mid\mu_k,\Sigma_k)}{\sum_{h=1}^K\pi_h\mathcal N(x_i\mid\mu_h,\Sigma_h)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/27509148373c8c6129efab02.svg) | Component count, two component indices, observation index, arbitrary d_f-dimensional vector and observation vector. |
| ![Formula](https://ml-biomat.com/static/agent-math/324d4eda86e7dc8a4081a48b.svg) | Nonnegative mixture weights summing to one, d_f-dimensional means and positive-definite d_f-by-d_f covariances; means share input units and covariance entries have corresponding product units. |
| ![Formula](https://ml-biomat.com/static/agent-math/42db73e94c2e691a2004355e.svg) | Gaussian density, mixture density and component responsibility; density has inverse-feature-volume units, while responsibility is a unitless conditional probability. |

Weights 0.4 and 0.6 and component densities 0.2 and 0.1 give weighted densities 0.08 and 0.06, total 0.14 and responsibilities 4/7 and 3/7. Dividing both densities by one thousand divides total density by one thousand while leaving responsibilities unchanged.

The responsibility denominator adds all weighted component densities, normalizing their individual contributions to sum to one. Two quantities deserve separate attention. Overall density describes how common a location is, whereas responsibility divides membership among the candidate components. A point far from every component can still have responsibility near one for the relatively closest component while having extremely low overall density. Anomaly assessment should therefore examine density or a separately designed anomaly score. The largest responsibility answers a component-membership question; it does not measure the probability that the observation is normal.

Expectation maximization alternates between responsibilities under current parameters and weighted updates of proportions, means and covariances. Covariance constraints change the model family: spherical covariance retains one scale, diagonal covariance omits coordinate correlations, and full covariance permits rotated ellipses. Too many components can chase individual observations, and covariance can become extremely small. Multiple initializations and covariance regularization support computation, while choosing complexity requires a separate criterion. This experiment fits 375 elliptical observations, reserves 125 for assessment, and compares one through five components using BIC and held-out mean log density.

![Left: density contours of a two-component Gaussian mixture. Middle: BIC on 375 training points and mean log density on 125 test points. Right: complete-link dendrogram for six observations, with farthest-pair distance on the vertical axis.](https://ml-biomat.com/static/tutorials/machine-learning/figures/0b2c345631b8f60005f345a4.svg?v=0b2c345631b8)

Figure 4Left: density contours of a two-component Gaussian mixture. Middle: BIC on 375 training points and mean log density on 125 test points. Right: complete-link dendrogram for six observations, with farthest-pair distance on the vertical axis.

BIC combines training log likelihood with a penalty for the number of fitted parameters; smaller values are preferred. Here two components minimize BIC, agreeing with the generating process, and held-out mean log density is also favorable nearby. The criterion chooses approximation complexity within the Gaussian-mixture family. A single population with a complicated shape may require several Gaussian components. In the six-point dendrogram, the vertical axis instead measures complete-link distance, with the final two large groups merging at distance 2.4. Juxtaposing these panels separates a probability-density model from a distance-based merging record.

## Check neighbors in a two-dimensional map, not only islands

After rolling up a sheet of paper, neighbors along the surface remain neighbors, but points close through the surrounding air can lie on different layers. Manifold learning uses a related intuition: high-dimensional observations may be controlled by a few continuous factors, and local neighborhoods offer clues to that lower-dimensional structure. Viewing angle, posture and illumination can move photographs of one object along continuous paths. Finite sampling, noise, missing observations and an unsuitable distance can distort those paths. Understanding the input representation before embedding often contributes more than repeatedly adjusting a map's colors.

Van der Maaten and Hinton's 2008 t-SNE paper addressed crowding when arranging high-dimensional neighborhoods in two dimensions. The method converts high-dimensional proximity into probabilities and adjusts low-dimensional coordinates to align their neighborhood probabilities. A heavy-tailed distribution in the low-dimensional space gives non-neighbors room to separate. Perplexity controls an effective neighborhood scale, rather than fixing an exact final neighbor count. Optimization particularly emphasizes arranging high-dimensional neighbors. Empty distances between islands, their areas and their orientations therefore lack a universal interpretation in the original feature-space metric.

UMAP constructs a weighted neighbor graph using locally adapted distance scales, then optimizes a low-dimensional graph representation. The n_neighbors parameter changes the neighborhood range considered during construction, while min_dist affects how tightly points can pack in the embedding. The same observations may consequently appear as loose clouds or compact islands without changing their underlying identities. UMAP provides a transform path for new observations; the standard scikit-learn t-SNE used here principally embeds its current sample set jointly. Systems that continually add objects should consider new-object mapping and map stability when selecting a method.

![Four unsupervised maps of the same 900 digits, colored by labels added after fitting. T denotes ten-neighbor trustworthiness and overlap the mean ten-neighbor overlap. Coordinate scale and orientation belong to each embedding. Data: UCI, CC BY 4.0.](https://ml-biomat.com/static/tutorials/machine-learning/figures/cfc1ab7ebef5ca839102f525.svg?v=cfc1ab7ebef5)

Figure 5Four unsupervised maps of the same 900 digits, colored by labels added after fitting. T denotes ten-neighbor trustworthiness and overlap the mean ten-neighbor overlap. Coordinate scale and orientation belong to each embedding. Data: UCI, CC BY 4.0.

The four maps use the same 900 digit images: two-dimensional PCA, t-SNE with perplexities 10 and 50, and UMAP with 15 neighbors. Mean overlap between ten nearest neighbors in the original and embedded spaces is about 0.182, 0.616, 0.628 and 0.555 respectively. Trustworthiness asks how distant newly introduced embedded neighbors actually rank in the original space, giving approximately 0.825, 0.988, 0.989 and 0.987. High trustworthiness and exact ten-neighbor overlap are different demands. Promoting an original eleventh neighbor into tenth position should receive a smaller penalty than promoting an extremely distant object.

$$
O_k=\frac1n\sum_{i=1}^n\frac{|N_i^{\rm original}\cap N_i^{\rm map}|}{k},\quad T_k=1-\frac{2}{nk(2n-3k-1)}\sum_{i=1}^n\sum_{j\in U_i}(r_i(j)-k)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0dc800785ec2d81e6ae9f15e.svg) | Point count, two point indices and neighbor count, excluding the point itself; trustworthiness uses k<n/2. |
| ![Formula](https://ml-biomat.com/static/agent-math/a08c10878c94c7d88df99a60.svg) | Original-space and map k-neighbor sets, and map neighbors absent from the original k-neighbor set. |
| ![Formula](https://ml-biomat.com/static/agent-math/d6f0c06dc4fba168d372c430.svg) | Rank of j among original-space neighbors of i, starting at one; mean neighbor overlap and trustworthiness, all unitless. |

Six shared members among two ten-neighbor sets give overlap 0.6 for that point; average across points for O. With six points and one neighbor each, suppose the only new map neighbor ranks third originally. The penalty is two, normalization factor 1/24, and T=11/12. More distant false neighbors incur larger penalties.

The measurements support a specific conclusion: for these pixel distances, observations and parameters, the nonlinear maps preserve more local-neighborhood membership than two-dimensional PCA. Further investigation can select one point, inspect its image and neighbors in both spaces, and change seeds, neighborhood scales or sample subsets. If a grouping appears only in one attractive view, examine the corresponding differences in the original features. For compression followed by reconstruction, the earlier PCA error remains the more direct measurement. Visual appearance, neighborhood preservation and reconstruction accuracy answer separate questions.

## An anomaly score becomes a number of inspections

A normally operating device may occupy a stable region of measurement space. A future record outside that region can trigger an inspection. This is novelty detection: training observations principally represent normal operation, and evaluation concerns future records. Outlier detection instead allows some anomalous observations within the current collection and seeks departures from its main structure. The assumptions about training data differ. A whole new anomalous group may be dense internally; comparing local densities after combining it with normal observations can produce a different result from judging it against historical normal observations alone.

Isolation Forest repeatedly chooses random features and cut positions to isolate observations. Objects isolated after fewer splits receive greater unusualness. Local Outlier Factor, or LOF, compares an observation's local reachability density with those of its neighbors, emphasizing how sparse it is relative to its surroundings. Here LOF uses novelty mode and fits 400 normal observations. Another 200 normal calibration records determine the threshold, followed by 200 normal and 40 anomalous test records. Scores are oriented so higher means more unusual. The two numerical scales differ, so each threshold comes from its own calibration scores.

![Both models fit 400 normal records and choose thresholds using another 200 normal records. Blue points are 200 normal test records, green crosses 40 generated anomalies, and black contours are thresholds. Right: changing calibration quantiles changes false alarms and detection together.](https://ml-biomat.com/static/tutorials/machine-learning/figures/2ba32d3d7a451d42cfe5aeac.svg?v=2ba32d3d7a45)

Figure 6Both models fit 400 normal records and choose thresholds using another 200 normal records. Blue points are 200 normal test records, green crosses 40 generated anomalies, and black contours are thresholds. Right: changing calibration quantiles changes false alarms and detection together.

The threshold is the 95th percentile of normal calibration scores. On the actual test observations, Isolation Forest detects all 40 anomalies and raises 13 false alarms; LOF also detects all 40 and raises 12 false alarms. With false-alarm inspection cost one and missed-anomaly cost twenty, the observed costs are 13 and 12. Selecting a five-percent calibration tail does not force every future population to have exactly five-percent false alarms: the new normal test rates are 6.5% and 6%. The figure varies thresholds to show how inspection workload and detected fraction move together.

Generated anomalies come from a Gaussian distribution near (3.3,−3.3), well separated from the normal region. Moving that group inward, changing normal noise or adding another normal operating mode changes both detection and false alarms. Record anomaly types, normal-state coverage and human review outcomes alongside an overall alert rate. Rarity can also identify a valuable new phenomenon. An anomaly score can send an observation into an inspection queue; determining whether it is an error, a fault or a discovery requires its original context and follow-up evidence.

## Return from the map to the original objects

The complete script retains original arrays, training and test indices, all four embeddings and numerical summaries. Start with the PCA reconstruction gallery: choose an image, identify the stroke missing from a low-rank reconstruction and relate that observation to its error. Then compare original-space and embedded neighbors for an object, asking whether visually similar digits with shifted pixels become separated. In clustering experiments, hold generated observations fixed while changing radius or group count and inspect which assignments change first. This sequence keeps visual observations, numerical summaries and algorithmic operations connected to the same records.

### Complete experiment: digit compression, neighborhoods, clusters and anomalies

Requires NumPy, SciPy, Matplotlib, scikit-learn and umap-learn. Run python main.py --output results --language en. Digits are bundled with scikit-learn without another download; outputs are five scientific figure groups, experiment_data.npz and summary.json.

```
"""Unsupervised structure: actual compression, neighborhoods, density and novelty."""
from pathlib import Path
import argparse,json,os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.cluster.hierarchy import linkage,dendrogram
from sklearn.datasets import load_digits,make_moons
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans,DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.manifold import TSNE,trustworthiness
from sklearn.neighbors import NearestNeighbors,LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from sklearn.metrics import adjusted_rand_score,confusion_matrix
from umap import UMAP

COL=['#237b94','#d87430','#609b6d','#a268a6','#c7a22b','#465db0','#b95159','#7f8e37','#6e8290','#d38aab']
def main(out,lang):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);zh=lang=='zh';T=lambda z,e:z if zh else e
 plt.rcParams.update({'font.family':'Microsoft YaHei' if zh else 'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','figure.facecolor':'white','axes.titleweight':'bold','axes.unicode_minus':False})
 rng=np.random.default_rng(6)
 def save(fig,name):fig.savefig(out/f'{name}-{lang}.svg',bbox_inches='tight');plt.close(fig)
 d=load_digits();X=d.data/16;y=d.target;it,ie=train_test_split(np.arange(len(X)),test_size=.25,stratify=y,random_state=6)
 ranks=[2,5,10,20,40,64];errors=[];ratios=[];recons={}
 for k in ranks:
  p=PCA(n_components=k,svd_solver='full').fit(X[it]);rec=p.inverse_transform(p.transform(X[ie]));errors.append(float(np.mean((rec-X[ie])**2)));ratios.append(float(p.explained_variance_ratio_.sum()));recons[k]=rec
 # Every image is reconstructed from a training-only basis; common grayscale limits.
 fig=plt.figure(figsize=(14.2,9.2),layout='constrained')
 outer=fig.add_gridspec(1,2,width_ratios=[1.85,1],wspace=.17)
 gs=outer[0].subgridspec(6,6,hspace=.08,wspace=.06)
 curves=outer[1].subgridspec(2,1,hspace=.20)
 for row,k in enumerate([None,2,5,10,20,40]):
  for c in range(6):
   ax=fig.add_subplot(gs[row,c]);ax.imshow(X[ie[c]].reshape(8,8) if k is None else recons[k][c].reshape(8,8),cmap='gray',vmin=0,vmax=1);ax.set_xticks([]);ax.set_yticks([])
   if c==0:ax.set_ylabel(T('原图','Original') if k is None else f'k={k}',rotation=0,labelpad=27,va='center')
   if row==0:ax.set_title(str(y[ie[c]]))
 ax=fig.add_subplot(curves[0]);ax.plot(ranks,errors,'o-',color=COL[0]);ax.set(xlabel=T('保留分量数','Retained components'),ylabel=T('测试像素均方误差','Test pixel MSE'),title=T('450幅留出图像','450 held-out images'));ax.grid(alpha=.18)
 ax=fig.add_subplot(curves[1]);ax.plot(ranks,ratios,'s-',color=COL[1]);ax.set(xlabel=T('保留分量数','Retained components'),ylabel=T('训练累计方差比例','Training cumulative variance'),ylim=(0,1.05));ax.grid(alpha=.18);save(fig,'compression')
 # Labels are used for display after the unsupervised embeddings are fitted.
 subset=it[:900];A=X[subset];p2=PCA(2,svd_solver='full').fit_transform(A)
 embeddings={'PCA':p2,'t-SNE p=10':TSNE(perplexity=10,random_state=6,max_iter=800,init='pca',learning_rate='auto').fit_transform(A),'t-SNE p=50':TSNE(perplexity=50,random_state=6,max_iter=800,init='pca',learning_rate='auto').fit_transform(A),'UMAP n=15':UMAP(n_neighbors=15,min_dist=.15,random_state=6,n_jobs=1,n_epochs=300).fit_transform(A)}
 def neighbors(data):
  raw=NearestNeighbors(n_neighbors=11).fit(data).kneighbors(data,return_distance=False)
  return np.array([row[row!=i][:10] for i,row in enumerate(raw)])
 nbr=neighbors(A);quality={}
 fig,axs=plt.subplots(2,2,figsize=(12,10),layout='constrained')
 for ax,(name,Z) in zip(axs.flat,embeddings.items()):
  en=neighbors(Z);overlap=float(np.mean([len(set(a)&set(b))/10 for a,b in zip(nbr,en)]));tr=float(trustworthiness(A,Z,n_neighbors=10));quality[name]={'trustworthiness10':tr,'neighbor_overlap10':overlap}
  sc=ax.scatter(Z[:,0],Z[:,1],c=y[subset],s=10,cmap=ListedColormap(COL),vmin=-.5,vmax=9.5,alpha=.8);ax.set(title=f'{name} | T={tr:.3f}, overlap={overlap:.3f}',xlabel=T('嵌入坐标1（任意单位）','Embedding coordinate 1 (arbitrary units)'),ylabel=T('嵌入坐标2','Embedding coordinate 2'));ax.set_xticks([]);ax.set_yticks([])
 cb=fig.colorbar(sc,ax=axs,ticks=range(10),shrink=.75);cb.set_label(T('真实数字标签（拟合未使用）','Digit label (unused during fitting)'));save(fig,'neighborhoods')
 moon,ym=make_moons(500,noise=.07,random_state=6)
 e0=rng.multivariate_normal([-2,0],[[1.2,.7],[.7,.6]],250);e1=rng.multivariate_normal([2,0],[[.6,-.45],[-.45,1.2]],250);ell=np.vstack([e0,e1]);ye=np.repeat([0,1],250);cluster_scores={};fig,axs=plt.subplots(2,3,figsize=(13,8),layout='constrained')
 for row,(name,D,Y) in enumerate([('moons',moon,ym),('ellipses',ell,ye)]):
  for col,(n,model) in enumerate([('k-means',KMeans(2,n_init=20,random_state=6)),('GMM',GaussianMixture(2,n_init=5,random_state=6)),('DBSCAN',DBSCAN(eps=.19 if row==0 else .4,min_samples=8))]):
   labels=model.fit_predict(D);ari=float(adjusted_rand_score(Y,labels));noise=int((labels==-1).sum());cluster_scores[f'{name}/{n}']={'ari':ari,'noise':noise,'clusters':len(set(labels)-{-1})};ax=axs[row,col];colors=[('#acb5bc' if a==-1 else COL[a%len(COL)]) for a in labels];ax.scatter(*D.T,c=colors,s=13,alpha=.8);ax.set(title=f'{n} | ARI={ari:.3f}, noise={noise}',xlabel=T('特征1','Feature 1'),ylabel=T('特征2','Feature 2'));ax.set_aspect('equal',adjustable='datalim')
 save(fig,'cluster_shapes')
 gt,ge=train_test_split(np.arange(500),test_size=.25,random_state=6);gm=GaussianMixture(2,n_init=10,random_state=6).fit(ell[gt]);xx,yy=np.meshgrid(np.linspace(-6,6,180),np.linspace(-4,4,150));grid=np.c_[xx.ravel(),yy.ravel()];density=np.exp(gm.score_samples(grid)).reshape(xx.shape);bics=[];ll=[]
 for k in range(1,6):
  q=GaussianMixture(k,n_init=10,random_state=6).fit(ell[gt]);bics.append(float(q.bic(ell[gt])));ll.append(float(q.score(ell[ge])))
 fig,axs=plt.subplots(1,3,figsize=(15,4.6),layout='constrained');im=axs[0].contourf(xx,yy,density,levels=12,cmap='Blues');axs[0].scatter(*ell[gt].T,s=4,color='#293d4b',alpha=.35);fig.colorbar(im,ax=axs[0],label=T('概率密度','Probability density'));axs[0].set(title=T('GMM：密度不等于组分概率','GMM: density versus membership'),xlabel=T('特征1','Feature 1'),ylabel=T('特征2','Feature 2'))
 axs[1].plot(range(1,6),bics,'o-',color=COL[0]);axs[1].set(xlabel=T('组分数','Components'),ylabel='BIC',title=T('训练拟合与复杂度','Training fit and complexity'));ax2=axs[1].twinx();ax2.plot(range(1,6),ll,'s--',color=COL[1]);ax2.set_ylabel(T('测试平均对数密度','Test mean log density'),color=COL[1]);axs[1].set_xticks(range(1,6))
 small=np.array([[0,0],[.2,.1],[.5,0],[2,0],[2.1,.2],[2.4,0]]);Z=linkage(small,method='complete');dendrogram(Z,labels=list('ABCDEF'),ax=axs[2],color_threshold=1);axs[2].set(ylabel=T('完全连接距离','Complete-link distance'),title=T('六点的逐步合并','Six observations merge'));save(fig,'density_hierarchy')
 # Training and threshold selection see only normal observations.
 train=rng.multivariate_normal([0,0],[[1,.6],[.6,1]],400);cal=rng.multivariate_normal([0,0],[[1,.6],[.6,1]],200);normal=rng.multivariate_normal([0,0],[[1,.6],[.6,1]],200)
 anomaly=rng.normal(loc=[3.3,-3.3],scale=.6,size=(40,2));test=np.vstack([normal,anomaly]);truth=np.r_[np.zeros(200,dtype=int),np.ones(40,dtype=int)];novel={};models=[('Isolation Forest',IsolationForest(n_estimators=150,random_state=6,n_jobs=1)),('LOF novelty',LocalOutlierFactor(n_neighbors=20,novelty=True))]
 fig,axs=plt.subplots(1,3,figsize=(15,4.7),layout='constrained')
 for ax,(name,model) in zip(axs[:2],models):
  model.fit(train);cs=-model.score_samples(cal);score=-model.score_samples(test);threshold=float(np.quantile(cs,.95));pred=(score>threshold).astype(int);tn,fp,fn,tp=confusion_matrix(truth,pred).ravel();novel[name]={'threshold':threshold,'tn':int(tn),'fp':int(fp),'fn':int(fn),'tp':int(tp),'cost_fp1_fn20':int(fp+20*fn)};field=-model.score_samples(grid).reshape(xx.shape);im=ax.contourf(xx,yy,field,levels=16,cmap='YlOrRd');ax.contour(xx,yy,field,levels=[threshold],colors=['#263744'],linewidths=1.5);ax.scatter(*normal.T,s=8,c=COL[0],alpha=.7);ax.scatter(*anomaly.T,s=15,c=COL[2],marker='x');fig.colorbar(im,ax=ax,label=T('异常分数（越大越异常）','Anomaly score (higher is more unusual)'));ax.set(title=f'{name} | FP={fp}, FN={fn}',xlabel=T('特征1','Feature 1'),ylabel=T('特征2','Feature 2'))
  fr=[];rec=[]
  for quantile in np.linspace(.8,.995,40):
   p=score>np.quantile(cs,quantile);fr.append(float(p[:200].mean()));rec.append(float(p[200:].mean()))
  axs[2].plot(fr,rec,'o-',ms=3,label=name)
 axs[2].set(xlabel=T('正常测试样本误报比例','False-positive fraction on normal test data'),ylabel=T('异常测试样本检出比例','Detected fraction of anomalous test data'),ylim=(0,1.05),title=T('阈值改变检查工作量','Thresholds alter review workload'));axs[2].legend(fontsize=9);axs[2].grid(alpha=.2);save(fig,'novelty')
 summary={'digits_n':len(X),'train_n':len(it),'test_n':len(ie),'pixel_features':64,'map_n':len(subset),'pca_ranks':ranks,'pca_test_mse':errors,'pca_train_variance_fraction':ratios,'neighborhoods':quality,'clusters':cluster_scores,'gmm_bic':bics,'gmm_test_mean_log_density':ll,'gmm_best_bic_components':int(np.argmin(bics)+1),'gmm_responsibility_sum_max_error':float(abs(gm.predict_proba(ell[ge]).sum(1)-1).max()),'novelty_train_normal':len(train),'novelty_calibration_normal':len(cal),'novelty_test_normal':len(normal),'novelty_test_anomaly':len(anomaly),'novelty':novel,'hierarchy_final_complete_distance':float(Z[-1,2])}
 np.savez_compressed(out/'experiment_data.npz',digits=X,labels=y,train_indices=it,test_indices=ie,map_indices=subset,moons=moon,moon_labels=ym,ellipses=ell,ellipse_labels=ye,novelty_train=train,novelty_calibration=cal,novelty_test=test,novelty_truth=truth,**{f'map_{j}':v for j,v in enumerate(embeddings.values())});(out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();main(a.output,a.language)
```

For a new unsupervised analysis, first describe the objects, the coordinates defining similarity, the treatment of units and the intended use: browsing, compression, grouping or alerts. Select corresponding checks. Reconstruction error evaluates compression; neighborhood preservation evaluates a map; resampling consistency and domain review evaluate grouping; false-positive and missed-event costs evaluate alerts. Even without ready-made labels, small targeted human reviews or later observations can turn an exploration into testable research questions. Each added check gives a particular output a clearer role instead of asking one two-dimensional picture to establish the entire conclusion.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M06.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Pearson (1901), On Lines and Planes of Closest Fit](https://zenodo.org/records/1430636)

   Historical context for distances from points to fitted lines.
2. [UCI — Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)

   Digit data and license.

   CC BY 4.0
3. [scikit-learn — Decomposing signals in components](https://scikit-learn.org/stable/modules/decomposition.html)

   PCA, centering, SVD and reconstruction.

   BSD-3-Clause
4. [scikit-learn — Comparing clustering algorithms](https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_comparison.html)

   Original shape-comparison figure and open example.

   BSD-3-Clause
5. [scikit-learn — Gaussian mixture models](https://scikit-learn.org/stable/modules/mixture.html)

   Responsibilities, covariance, EM and BIC.

   BSD-3-Clause
6. [van der Maaten & Hinton (2008), Visualizing Data using t-SNE](https://www.jmlr.org/papers/v9/vandermaaten08a.html)

   Neighborhood probabilities and crowding.
7. [UMAP — How UMAP Works](https://umap-learn.readthedocs.io/en/latest/how_umap_works.html)

   Local scales, neighbor graphs and low-dimensional layout.

   BSD-3-Clause project
8. [UMAP — Basic Parameters](https://umap-learn.readthedocs.io/en/latest/parameters.html)

   Neighbor-count and minimum-distance parameters.

   BSD-3-Clause project
9. [scikit-learn — Novelty and Outlier Detection](https://scikit-learn.org/stable/modules/outlier_detection.html)

   LOF novelty mode and anomaly-detection objectives.

   BSD-3-Clause
