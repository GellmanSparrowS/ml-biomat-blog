# Support vector machines: margins, kernels and boundaries

Source: https://ml-biomat.com/tutorials/machine-learning/m05/en/
Language: en

From seven points to handwritten digits, tolerance tubes and normal regions: discover what determines a boundary.

## Separating two groups while leaving a corridor

A sorting machine receives a handwritten digit and must decide whether it is a 3 or an 8. A quality-control system receives sensor measurements and must decide whether a component is acceptable. Separating the examples already collected is only the beginning: handwriting shifts, and measurements fluctuate. If the decision boundary passes extremely close to an observation, a small change can reverse the decision. A support vector machine asks a geometric question: among boundaries that separate the classes, can we choose one that also stays relatively far from the nearest observations? The space it leaves is the margin. Like a buffer beside a road, it concerns the distance to a risky edge as well as whether the edge has already been crossed.

This viewpoint is useful for small and medium-sized classification problems with a meaningful feature representation. It also extends to regression and novelty detection. An SVM does not acquire an understanding of image structure simply because its inputs are pixels: it works with the geometry of the numerical representation supplied to it. If the inputs are spectra or summary measurements, the boundary concerns those features instead. Before choosing the method, identify the observation, decide whether distances between observations are meaningful, and establish which features will be available when predicting. We will first inspect every component in two dimensions, then test the choices on actual handwritten-digit data.

The 1995 support-vector networks paper by Corinna Cortes and Vladimir Vapnik brought together large-margin classification, nonlinear feature mappings and optimization that permits training errors. Permitting errors was a crucial practical step. Real classes often overlap, and demanding a perfect separation can make the boundary follow noise. The geometric argument converts “how many observations can be separated?” into “what cost should be paid to separate them?” A modern library hides the optimization behind a short call, but the trade-off between a broad margin and expensive violations remains central to interpreting the result.

## Scores, normal vectors and the observations that matter

Represent an observation as a column of numbers. For an introductory drawing, the first coordinate might be standardized stroke width and the second a measure of stroke inclination. A linear classifier multiplies each coordinate by a weight, adds the contributions and adds an intercept. Positive scores select one class; negative scores select the other. Points with zero score form the boundary. In higher dimensions the line becomes a hyperplane, but the computation is unchanged. The weight vector is perpendicular to this boundary, so it determines its orientation. The intercept changes its position.

$$
f(\mathbf x)=\mathbf w^\top\mathbf x+b,\qquad d=\frac{|f(\mathbf x)|}{\|\mathbf w\|_2},\qquad W=\frac{2}{\|\mathbf w\|_2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4fa2300af121b336bb0d7845.svg) | A p-dimensional feature vector, dimensionless after standardization here. |
| ![Formula](https://ml-biomat.com/static/agent-math/76309848742948f71178485f.svg) | A p-dimensional normal vector, dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Scalar intercept, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | Signed decision score, dimensionless; its sign gives the binary decision. |
| ![Formula](https://ml-biomat.com/static/agent-math/9221822a6402f4d6cb9d08be.svg) | Transpose, allowing the inner product of column vectors. |
| ![Formula](https://ml-biomat.com/static/agent-math/91c83adc25418ce23b813590.svg) | Euclidean length of the weight vector, required to be nonzero. |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Perpendicular distance to the zero-score plane in standardized-feature units. |
| ![Formula](https://ml-biomat.com/static/agent-math/b6053f2ba2b57f6638d0be7f.svg) | Distance between score −1 and +1 surfaces under the unit-margin convention. |

With w=(2,0), b=−1 and x=(1,3), the score is 1, weight length is 2, distance is 0.5 and corridor width is 1. The second coordinate does not affect distance to this vertical boundary.

A score is not itself a geometric distance. Multiplying every weight and the intercept by ten leaves the zero-score boundary unchanged while multiplying every score by ten. Dividing by the length of the weight vector removes that arbitrary rescaling. The SVM convention places the nearest ideal observations of the two classes on scores of minus one and plus one. The distance between those parallel surfaces is then two divided by the weight-vector length. Enlarging the margin becomes equivalent to shrinking that length, provided the observation constraints are retained. Setting all weights to zero does not satisfy the classification problem.

Which observations actually determine the boundary? Imagine two parallel boards placed between two groups of pins. The pins nearest the gap touch the boards first and prevent further movement. These are the geometric prototype of support vectors. A correctly classified point far from the boundary can often move slightly without changing the optimum; points touching or entering the margin can alter it. The plots mark support vectors with an extra ring so that the boundary, the margin and the particular observations constraining them can be read together. This is a useful diagnostic rather than simply a decorative way to display the fit.

![The same seven points with C=0.1 and C=10. Fitted margin widths are approximately 4.00 and 0.566. Solid lines denote zero score; dashed lines denote scores ±1; rings identify support vectors.](https://ml-biomat.com/static/tutorials/machine-learning/figures/30676d8a0abed0b23ff7c615.svg?v=30676d8a0abe)

Figure 1The same seven points with C=0.1 and C=10. Fitted margin widths are approximately 4.00 and 0.566. Solid lines denote zero score; dashed lines denote scores ±1; rings identify support vectors.

The two panels use the same seven observations and change only the violation penalty. One point carries a label unlike its nearby neighbors and pulls the boundary in a different direction. With a small penalty, the model accepts a violation and retains a broad corridor. With a larger penalty, the line rotates and the corridor narrows. The widths shown come from fitted coefficients, not manually selected illustrative lines. A wider margin does not guarantee a better test result; it is a way to control the geometry of the solution. Validation data determine whether that particular trade-off is useful.

## Putting a price on violations

A hard-margin formulation requires every training observation to lie beyond the appropriate margin surface. This is easy to picture for clearly separated groups, but a single contradictory label may make the constraints impossible to satisfy. A soft margin assigns each observation a slack variable measuring how far it falls short of the required signed score. Zero slack means the requirement is satisfied. Slack between zero and one means that classification is correct but the buffer is too small. Slack greater than one means the observation has crossed the decision boundary. Geometry has become a continuous penalty that can be traded against the weight-vector length.

$$
\min_{\mathbf w,b,\boldsymbol\xi}\ \frac12\|\mathbf w\|_2^2+C\sum_{i=1}^{n}\xi_i,\qquad y_i f(\mathbf x_i)\ge 1-\xi_i,\quad\xi_i\ge0
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/532fd9de01c5518cbb6ef73b.svg) | Training sample count and index, unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/a3cbcc3d75664bd27e243f85.svg) | Weights, intercept, score and observation i as defined above; dimensionless here. |
| ![Formula](https://ml-biomat.com/static/agent-math/a51d7c6c42d3bb0b61f865ba.svg) | Binary class label of observation i, −1 or +1, unitless. |
| ![Formula](https://ml-biomat.com/static/agent-math/09714133b942eafde68b756d.svg) | Nonnegative slack and its vector, unitless; for a fixed boundary its minimum is max(0,1−y_i f). |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | Positive penalty per unit slack, dependent on scaling and the sum-loss convention. |
| ![Formula](https://ml-biomat.com/static/agent-math/87e2d6f0b155ef8920bda496.svg) | Choose parameters minimizing the objective; sum slacks over training observations. |

For w=(1,0), b=0 and a positive point x=(0.4,1), the score is 0.4 and minimum slack is 0.6. With this single point and C=2, the objective is 0.5+2×0.6=1.7. A positive point with score −0.2 requires slack 1.2 and is misclassified.

The parameter C determines the price of a unit violation. A larger value encourages the optimizer to increase weight length when that reduces training violations; a smaller value gives more priority to a broad margin. Its numerical interpretation depends on feature scales, sample size and whether a software formulation sums or averages losses. Consequently, C=1 is not a universal regularization strength. If one feature is recorded in meters and another in millimeters, equal physical changes differ numerically by a thousandfold. Standardization subtracts each training-column mean and divides by its training standard deviation, reducing the influence of arbitrary units. Those statistics must be estimated separately inside each training fold.

The interactive experiment lets you choose a boundary orientation, intercept and weight length. It computes signed margins, hinge losses and both contributions to the objective. Here you play the role of the optimizer. First reduce classification errors, then inspect the weight penalty paid for doing so. Changing C does not automatically move this manually specified boundary: it changes the price against which candidate boundaries are compared. Move the boundary again after changing that price. Class colors and rings around margin violations connect the numerical objective to individual observations, while the displayed totals make the calculation inspectable.

## Compare the cost of a boundary

Both axes are dimensionless features. Sliders specify the boundary directly. Dashed lines mark unit margins; rings mark violations.

[Figure: Decision boundary and margin](https://ml-biomat.com/tutorials/machine-learning/m05/en/#M05-plot)

Class-specific penalties can also express an imbalanced objective. If missing a defect is costly, a violation on a defect observation can receive greater weight. Class weighting changes the learning objective, whereas changing a decision threshold changes how an already fitted score produces an action. Evaluate the resulting recall, false-alarm rate and practical cost together. The raw SVM decision score is not a probability. When probabilities are required, add calibration on the training side of the workflow and examine a reliability diagram rather than interpreting the score magnitude as confidence directly.

## Curved boundaries from pairwise comparisons

If a straight line cannot separate an inner ring from an outer ring, improving the optimizer will not repair an insufficient representation. Adding the squared distance to the origin as another coordinate may make the groups separable by a plane in the expanded space. Kernel methods take this idea further: we need not always write down every expanded coordinate. If a function computes the inner product that two observations would have in that feature space, many SVM calculations can use that value directly. A kernel takes two inputs and returns the corresponding inner-product value, allowing a linear separation in a transformed space to appear nonlinear in the original coordinates.

$$
K_{\rm lin}(\mathbf x,\mathbf z)=\mathbf x^\top\mathbf z,\quad K_{\rm poly}=(\gamma\mathbf x^\top\mathbf z+r)^q,\quad K_{\rm RBF}=e^{-\gamma\|\mathbf x-\mathbf z\|_2^2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c4d10fa08c540fadb62d6163.svg) | Linear, polynomial and radial-basis kernel values, dimensionless for the standardized inputs here. |
| ![Formula](https://ml-biomat.com/static/agent-math/af71bc998a10ca33d6d1ea71.svg) | Two equal-dimensional feature vectors on standardized scales. |
| ![Formula](https://ml-biomat.com/static/agent-math/7db9474e1e95a533a1714618.svg) | Positive scale parameter; inverse squared-feature-distance units for the RBF kernel. |
| ![Formula](https://ml-biomat.com/static/agent-math/a3862e85bcfb892a6e44bb39.svg) | Polynomial offset and positive integer degree; common valid settings use gamma>0 and r≥0. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Base of the natural exponential, approximately 2.71828. |

For x=(1,0) and z=(0,1), the inner product is zero and squared distance is two. At gamma=0.5, RBF similarity is exp(−1)≈0.3679; identical inputs have similarity one. With r=1 and q=2, the polynomial kernel equals one.

The linear kernel retains the original inner product. A polynomial kernel includes feature products and can therefore express interactions, with degree controlling an important part of its flexibility. The radial basis function, or RBF kernel, turns squared distance into similarity: coincident points have similarity one, and similarity decreases as distance grows. Its gamma parameter determines the scale of influence. Small gamma spreads influence broadly; large gamma concentrates it in small neighborhoods and can produce islands around individual training points. C and gamma must therefore be selected together. One controls the cost of violations; the other controls the geometry over which observations influence one another.

Not every plausible similarity function is a valid kernel for the usual SVM formulation. For any finite collection of inputs, its Gram matrix should be positive semidefinite: every real weighted quadratic form of that matrix is nonnegative. This property permits an inner-product interpretation and supports the standard convex optimization argument. Starting with established kernels is a practical way to learn before constructing domain-specific alternatives. Calling an edit distance, a correlation coefficient or an arbitrary neural score a kernel does not establish this property. The mathematical condition concerns all possible weighted combinations, not merely whether individual similarity values look sensible.

The dual optimization changes variables from feature weights to one coefficient per training observation. These coefficients act like prices associated with constraints. Introducing the prices and eliminating the original weights leaves features appearing only through pairwise inner products, which can then be replaced by kernel evaluations. The equality constraint below arises from the intercept; the coefficient upper bounds arise from the linear slack penalty. The primal is a convex minimization over weights and slacks, while the dual is a concave maximization with box constraints. They provide two optimization descriptions of the same classifier in this setting.

$$
\max_{\boldsymbol\alpha}\sum_{i=1}^n\alpha_i-\frac12\sum_{i=1}^n\sum_{j=1}^n\alpha_i\alpha_j y_i y_j K(\mathbf x_i,\mathbf x_j),\quad 0\le\alpha_i\le C,\quad\sum_i\alpha_i y_i=0
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a70831c35436479ca201ac33.svg) | An n-vector of dual variables and coefficient i, unitless; zero coefficients belong to nonsupport observations. |
| ![Formula](https://ml-biomat.com/static/agent-math/a6505df9c7be061c1a794c47.svg) | Training sample count and the two sample indices. |
| ![Formula](https://ml-biomat.com/static/agent-math/e39d2f647a056424e7dd5ef3.svg) | Labels, feature vectors, positive-semidefinite kernel and common penalty, with meanings and units defined above. |

For one-dimensional points −1 and +1 with corresponding labels −1 and +1 and a linear kernel, equal coefficients a satisfy the equality constraint. The objective becomes 2a−2a². If C≥0.5, it is maximized at a=0.5, recovering weight w=Σαyx=1.

$$
f(\mathbf x)=\sum_{i\in S}\alpha_i y_i K(\mathbf x_i,\mathbf x)+b,\qquad 0<\alpha_i\le C
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8a1afc03b89f0210dd0f13b5.svg) | Set of support-vector indices with nonzero coefficients, and an index in that set. |
| ![Formula](https://ml-biomat.com/static/agent-math/c1688c6743f4779a68a29b34.svg) | Nonzero optimized dual coefficient, unitless in this soft-margin binary formulation with common C. |
| ![Formula](https://ml-biomat.com/static/agent-math/1a7ca3fd714cc9789220d8f1.svg) | Support-vector label, kernel, training vector, new vector, intercept, penalty and score, as defined above. |

Two support vectors have coefficients 0.5 and labels +1 and −1. With kernel values 0.8 and 0.2 and zero intercept, the score is 0.3 and the prediction is positive. The full dual also requires the sum of alpha_i y_i to be zero, which this example satisfies.

The dual prediction expression explains why only support vectors are retained: observations with zero coefficients disappear from the sum. Nonzero coefficients, class signs and kernel evaluations against the new observation determine the score. It also reveals a resource constraint. A complete kernel matrix for n training observations contains n squared entries; increasing sample count tenfold increases that storage one hundredfold. Exact fitting time additionally depends on the data, kernel and optimizer. Linear solvers are consequently attractive for large sparse text problems, while an RBF kernel can be a useful candidate for moderate datasets with meaningful nonlinear feature geometry.

## Testing the geometry on handwritten digits

The experiment uses the handwritten-digit dataset bundled with scikit-learn: 1,797 grayscale images, each with eight by eight pixels. Flattening an image produces 64 features, whose intensities range from zero to sixteen. Targets are the ten digits. A stratified split with seed 17 places 1,347 images in training and 450 in testing, preserving representation of every class. Flattening does not explicitly preserve the image neighborhood structure, but it gives a clear reproducible starting point. A later convolutional-network chapter will exploit that neighborhood structure through the model architecture rather than leaving it implicit in a vector of pixel values.

All parameter selection occurs within the 1,347 training images. Each combination of C and gamma uses the same three stratified folds. Standardization is inside a Pipeline, so a validation fold never contributes to the mean or standard deviation used to transform its training fold. The heatmap displays the mean validation accuracy of sixteen configurations. It is not a display of whichever configurations looked best on the test set. This search selected C=100 and gamma=0.001, with mean validation accuracy around 98.07%. The selected pipeline is then fitted on all training observations and evaluated once on the 450 test images.

![Left: three-fold training-side validation for sixteen configurations. Right: the selected RBF model on 450 held-out images. The left panel uses color and cell labels for validation accuracy; the right uses color for counts by true and predicted class.](https://ml-biomat.com/static/tutorials/machine-learning/figures/06c7d29cdf47c699263c8cda.svg?v=06c7d29cdf47)

Figure 2Left: three-fold training-side validation for sixteen configurations. Right: the selected RBF model on 450 held-out images. The left panel uses color and cell labels for validation accuracy; the right uses color for counts by true and predicted class.

The RBF SVM correctly classifies 446 test images, giving 99.11% accuracy. The linear SVM correctly classifies 444, giving 98.67%; logistic regression obtains 97.11%; and a 150-feature Nyström approximation followed by LinearSVC obtains 96.22%. These are results for the fixed split in this experiment. The difference between four and six errors is small, so a claim of stable superiority would require repeated splits or a suitable paired evaluation. More informative observations are that the linear approach is already strong, the nonlinear improvement is modest, and a computational approximation introduces another accuracy-resource trade-off.

![Actual misclassified digits, supplemented with correct examples when fewer than six errors occur, and test accuracy of four configurations. Images come from the bundled scikit-learn digits dataset; metrics are computed by the chapter code.](https://ml-biomat.com/static/tutorials/machine-learning/figures/9a4d6ef7cda66fbb5c13de75.svg?v=9a4d6ef7cda6)

Figure 3Actual misclassified digits, supplemented with correct examples when fewer than six errors occur, and test accuracy of four configurations. Images come from the bundled scikit-learn digits dataset; metrics are computed by the chapter code.

The confusion matrix shows where observations of each true digit were assigned. The accompanying image panel connects those counts to actual strokes. An error may arise from similar handwriting, limited pixel resolution or a model that does not explicitly use spatial structure. Inspecting errors suggests concrete experiments, such as preserving image geometry or adding controlled translations. Once the 450 test examples guide such decisions, they have become development material; retain another evaluation set for the revised workflow. This keeps visual error analysis useful without repeatedly presenting the same adapted-to sample as independent evidence.

Ten-class SVC training does not produce a single separating hyperplane. The library uses one-versus-one training: ten classes give 45 binary problems whose decisions are combined. The two-dimensional margin drawing remains useful because it explains the building block of those comparisons. The complete code retains split indices, validation results, fitted-model metrics and plotting procedures. After changing the parameter grid, inspect how the validation surface and error types change rather than focusing only on the last decimal place. Prediction timings are also recorded, but a single short call is too sensitive to system scheduling to serve as a performance benchmark.

### Complete experiment: margins, digits, regression and novelty

Requires NumPy, Matplotlib and scikit-learn. Data come from bundled digits and seeded generators. Run python main.py --output results --language en to produce five SVG figures, summary.json and experiment_data.npz.

```
"""SVM margins, digit recognition, support-vector regression and novelty detection.
Run: python main.py --output results --language en
The digits data are bundled with scikit-learn (UCI optical handwritten digits).
"""
from pathlib import Path
import argparse,json,time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split,GridSearchCV,StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC,SVR,LinearSVC,OneClassSVM
from sklearn.kernel_approximation import Nystroem
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='results');p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args()
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True);zh=a.language=='zh';rng=np.random.default_rng(17)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
    def save(fig,name):fig.savefig(out/f'{name}-{a.language}.svg',bbox_inches='tight');plt.close(fig)
    X=np.array([[-2,-1],[-2,1],[-1,0],[1,0],[2,-1],[2,1],[-.8,.3]])
    y=np.array([-1,-1,-1,1,1,1,1])
    gx,gy=np.meshgrid(np.linspace(-3,3,180),np.linspace(-2,2,150));grid=np.c_[gx.ravel(),gy.ravel()]
    fig,axs=plt.subplots(1,2,figsize=(11.4,4.5),layout='constrained');margins=[]
    for ax,C in zip(axs,[.1,10.]):
        model=SVC(kernel='linear',C=C).fit(X,y);z=model.decision_function(grid).reshape(gx.shape)
        ax.contourf(gx,gy,z,levels=[-100,0,100],colors=['#d7e9ed','#f5e2cb'])
        ax.contour(gx,gy,z,levels=[-1,0,1],colors='#183845',linestyles=['--','-','--'])
        ax.scatter(X[:,0],X[:,1],c=np.where(y<0,'#167b82','#ca8446'),s=65,edgecolors='white')
        ax.scatter(model.support_vectors_[:,0],model.support_vectors_[:,1],s=165,facecolors='none',edgecolors='#183845',lw=1.4)
        norm=np.linalg.norm(model.coef_);margins.append({'C':C,'w':model.coef_[0].tolist(),'b':float(model.intercept_[0]),'width':float(2/norm),'support_indices':model.support_.tolist()})
        ax.set(title=f'C = {C:g}; '+('间隔宽度 ' if zh else 'margin width ')+f'{2/norm:.2f}',xlabel='x₁',ylabel='x₂',xlim=(-3,3),ylim=(-2,2),aspect='equal')
    save(fig,'margins')
    digits=load_digits();train_idx,test_idx=train_test_split(np.arange(len(digits.target)),test_size=.25,stratify=digits.target,random_state=17)
    Xt,Xs=digits.data[train_idx],digits.data[test_idx];yt,ys=digits.target[train_idx],digits.target[test_idx]
    grid_search=GridSearchCV(make_pipeline(StandardScaler(),SVC(kernel='rbf')),{'svc__C':[.1,1,10,100],'svc__gamma':[.001,.01,.1,1]},cv=StratifiedKFold(3,shuffle=True,random_state=17),n_jobs=1)
    grid_search.fit(Xt,yt)
    models={'Linear SVM':make_pipeline(StandardScaler(),SVC(kernel='linear',C=1)),
            'RBF SVM':grid_search.best_estimator_,
            'Logistic regression':make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=2000)),
            'Nystroem + LinearSVC':make_pipeline(StandardScaler(),Nystroem(gamma=.01,n_components=150,random_state=17),LinearSVC(C=1,dual=False,max_iter=5000))}
    scores={};predictions={}
    for name,model in models.items():
        start=time.perf_counter()
        if name!='RBF SVM':model.fit(Xt,yt)
        pred=model.predict(Xs);predictions[name]=pred
        scores[name]={'test_accuracy':float(accuracy_score(ys,pred)),'prediction_seconds':None,'support_vectors':int(model[-1].support_.size) if hasattr(model[-1],'support_') else None}
        t=time.perf_counter();model.predict(Xs);scores[name]['prediction_seconds']=time.perf_counter()-t
    cv=np.array(grid_search.cv_results_['mean_test_score']).reshape(4,4)
    fig,axs=plt.subplots(1,2,figsize=(11.5,4.8),gridspec_kw={'width_ratios':[1,1.2]},layout='constrained')
    im=axs[0].imshow(cv,vmin=.1,vmax=1,cmap='YlGnBu',aspect='auto');fig.colorbar(im,ax=axs[0],label='CV accuracy')
    axs[0].set(xticks=range(4),xticklabels=['.001','.01','.1','1'],yticks=range(4),yticklabels=['.1','1','10','100'],xlabel='γ',ylabel='C',title='训练集内3折验证' if zh else '3-fold validation inside training data')
    for i in range(4):
        for j in range(4):axs[0].text(j,i,f'{cv[i,j]:.3f}',ha='center',va='center',color='white' if cv[i,j]>.7 else '#183845',fontsize=10)
    cm=confusion_matrix(ys,predictions['RBF SVM']);im=axs[1].imshow(cm,cmap='Blues');fig.colorbar(im,ax=axs[1],label='样本数' if zh else 'Count')
    axs[1].set(xlabel='预测数字' if zh else 'Predicted digit',ylabel='真实数字' if zh else 'True digit',xticks=range(10),yticks=range(10),title='独立测试集：RBF SVM' if zh else 'Held-out test set: RBF SVM')
    save(fig,'validation')
    fig=plt.figure(figsize=(11.4,6.1),layout='constrained');gs=fig.add_gridspec(2,6,height_ratios=[1,1.5]);err=np.flatnonzero(ys!=predictions['RBF SVM']);show=np.r_[err[:6],np.flatnonzero(ys==predictions['RBF SVM'])[:6-len(err[:6])]]
    for j,idx in enumerate(show):
        ax=fig.add_subplot(gs[0,j]);ax.imshow(Xs[idx].reshape(8,8),cmap='gray_r',vmin=0,vmax=16);ax.set_title(f'{ys[idx]} → {predictions["RBF SVM"][idx]}',fontsize=11);ax.axis('off')
    ax=fig.add_subplot(gs[1,:]);names=list(scores);vals=[scores[n]['test_accuracy'] for n in names];ax.barh(names,vals,color=['#6f8191','#167b82','#ca8446','#8b7557']);ax.set(xlim=(0,1.08),xlabel='测试准确率' if zh else 'Test accuracy')
    for i,v in enumerate(vals):ax.text(v+.01,i,f'{v:.3f}',va='center')
    save(fig,'digits')
    x=np.sort(rng.uniform(0,6,80));target=np.sin(x)+rng.normal(0,.12,80);xx=np.linspace(0,6,300)
    fig,axs=plt.subplots(1,2,figsize=(11.5,4.4),layout='constrained');svr=[]
    for ax,eps in zip(axs,[.05,.25]):
        model=SVR(C=10,gamma=.5,epsilon=eps).fit(x[:,None],target);fit=model.predict(xx[:,None])
        ax.fill_between(xx,fit-eps,fit+eps,color='#cfe5e6',label='ε '+('容忍带' if zh else 'tube'));ax.plot(xx,fit,color='#167b82',lw=2);ax.plot(xx,np.sin(xx),'--',color='#6f8191',label='生成函数' if zh else 'Generating function');ax.scatter(x,target,s=20,color='#183845');ax.scatter(x[model.support_],target[model.support_],s=70,facecolors='none',edgecolors='#ca8446');ax.set(xlabel='x',ylabel='y',title=f'ε={eps}; '+('支持向量 ' if zh else 'support vectors ')+str(len(model.support_)));ax.legend(frameon=False,fontsize=9)
        svr.append({'epsilon':eps,'n_support':len(model.support_)})
    save(fig,'svr')
    normal=rng.normal(0,.6,(160,2));new=rng.normal(0,.6,(40,2));outliers=rng.uniform(-3,3,(40,2));novel=make_pipeline(StandardScaler(),OneClassSVM(nu=.1,gamma=.5)).fit(normal)
    xx2,yy2=np.meshgrid(np.linspace(-3,3,140),np.linspace(-3,3,140));zz=novel.decision_function(np.c_[xx2.ravel(),yy2.ravel()]).reshape(xx2.shape)
    fig,ax=plt.subplots(figsize=(7.6,5.8),layout='constrained');ax.contourf(xx2,yy2,zz,levels=[zz.min(),0,zz.max()],colors=['#f7e6d7','#d6e9eb']);ax.contour(xx2,yy2,zz,levels=[0],colors='#183845');ax.scatter(normal[:,0],normal[:,1],s=12,color='#167b82',alpha=.6,label='正常训练样本' if zh else 'Normal training samples');ax.scatter(new[:,0],new[:,1],s=38,facecolors='none',edgecolors='#183845',label='新正常样本' if zh else 'New normal samples');ax.scatter(outliers[:,0],outliers[:,1],s=30,marker='x',color='#b45d3b',label='广域测试样本' if zh else 'Broad-range test samples');ax.set(xlabel='x₁',ylabel='x₂',aspect='equal',title='One-Class SVM');ax.legend(frameon=False,fontsize=9)
    save(fig,'novelty')
    summary={'digits_samples':len(digits.target),'train_samples':len(yt),'test_samples':len(ys),'best_params':grid_search.best_params_,'best_cv_accuracy':float(grid_search.best_score_),'models':scores,'margin_models':margins,'svr':svr,'one_class_normal_acceptance':float((novel.predict(new)==1).mean()),'one_class_broad_rejection':float((novel.predict(outliers)==-1).mean())}
    np.savez_compressed(out/'experiment_data.npz',tiny_X=X,tiny_y=y,train_idx=train_idx,test_idx=test_idx,test_y=ys,rbf_prediction=predictions['RBF SVM'],cv_scores=cv,svr_x=x,svr_y=target)
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary))


if __name__=='__main__':main()
```

## A prediction curve with an explicit tolerance

When the target is a continuous response, support vector regression replaces the classification corridor with a tolerance tube around the fitted curve. Squared-error regression penalizes every discrepancy, including differences smaller than measurement resolution. Epsilon-insensitive loss assigns no penalty to discrepancies within a specified tolerance and grows with the amount exceeding that tolerance. This makes “how small a discrepancy is worth fitting?” an explicit modeling choice. The curve still balances fit against regularity, but individual observations inside the tolerance tube need not exert the same pressure as observations that lie outside it.

$$
\ell_\epsilon(y,f)=\max\bigl(0,|y-f|-\epsilon\bigr)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/db4e42af6785df82e7296e31.svg) | Epsilon-insensitive loss, in target units. |
| ![Formula](https://ml-biomat.com/static/agent-math/2eea885ee51e19ae4e16f003.svg) | Observed and predicted response in the same units. |
| ![Formula](https://ml-biomat.com/static/agent-math/f24aa8f3e071190248b55b03.svg) | Nonnegative tolerance half-width in response units. |
| ![Formula](https://ml-biomat.com/static/agent-math/4ab88af114f90ff87651b701.svg) | Absolute error and the maximum of zero and the excess over tolerance. |

With epsilon=0.2, an error of 0.15 has zero loss, while an error of 0.6 has loss 0.4. If the response is in degrees Celsius, epsilon and this loss are also in degrees Celsius.

![The same synthetic observations and fixed C and gamma, with different epsilon tolerances. Shading shows the loss tolerance, rings identify support vectors, and the dashed curve is the generating relationship.](https://ml-biomat.com/static/tutorials/machine-learning/figures/53204270758c88eda9e5dae7.svg?v=53204270758c)

Figure 4The same synthetic observations and fixed C and gamma, with different epsilon tolerances. Shading shows the loss tolerance, rings identify support vectors, and the dashed curve is the generating relationship.

The figure uses a sine relationship with independent Gaussian noise of standard deviation 0.12. Both coordinates use dimensionless teaching scales. Holding C=10 and gamma=0.5 fixed, we change epsilon from 0.05 to 0.25. The actual number of support vectors decreases from 47 to six. A wider tube allows more observations to stop constraining the fitted curve. Whether that is desirable depends on the measurement resolution and prediction objective. If small changes carry useful information, an excessively wide tube discards them. If measurements are noisy, fitting every tiny fluctuation can add complexity without improving the response estimated for new observations.

Epsilon has the same units as the regression target, while C and kernel parameters remain sensitive to scaling. Expressing a temperature target in millidegrees instead of degrees requires a corresponding change in epsilon to preserve the same tolerance. The displayed tube is part of the training-loss definition. It is not a confidence interval for the fitted mean or a coverage interval for future observations. To answer where a future measurement is likely to fall, add a predictive uncertainty model or construct a prediction interval with separate calibration data. Probability models and conformal prediction provide later routes to that question.

## Learning a normal region without fault examples

Some monitoring systems have many normal operating records and very few known faults. One-Class SVM addresses a novelty-detection formulation: learn a region from normal training observations, then evaluate whether a new observation lies substantially outside it. No catalogue of invented fault labels is required. The kernel again defines similarity, while nu controls aspects of the support-vector fraction and training violations. Under the usual theoretical conditions, nu bounds the training-error fraction from above and the support-vector fraction from below. Finite samples and numerical optimization introduce approximations, so inspect the actual boundary and actual counts alongside the parameter setting.

![A kernel boundary fitted on 160 normal points, with two groups of forty new observations. The broad generator overlaps the normal distribution in input space.](https://ml-biomat.com/static/tutorials/machine-learning/figures/67c611b09e7a78903eb97f8f.svg?v=67c611b09e7a)

Figure 5A kernel boundary fitted on 160 normal points, with two groups of forty new observations. The broad generator overlaps the normal distribution in input space.

The example generates 160 normal training observations from a two-dimensional Gaussian with coordinate standard deviation 0.6. It also generates forty new observations from the same distribution and forty from a broader uniform region. Training-side standardization precedes a model with nu=0.1 and gamma=0.5. The acceptance rate for new normal observations is 90%, and the rejection rate for broad-region observations is 80%. Some broad-region samples fall in the normal region, so membership in that generator is not equivalent to being an intrinsically abnormal point. The experiment illustrates a learned region and overlapping distributions rather than a validated diagnosis of real equipment faults.

Outlier detection and novelty detection require different training protocols. Outlier detection commonly starts with a contaminated dataset and searches for unusual observations within it. Novelty detection first learns from relatively clean normal records and then evaluates future cases. Establish which setting describes the application before fitting. If normal operating modes shift seasonally, a fixed region may reject a new but legitimate mode. Stratifying by operating condition, recalibrating a threshold or updating the normal reference set can address distinct versions of that problem. The decision boundary needs a definition of normal operation and a monitoring workflow, not only a kernel choice.

## Comparing exact kernels, approximate kernels and linear models

A kernel approximation constructs a finite explicit representation intended to preserve a useful part of the implicit feature-space geometry. A linear model can then operate on those features. Nyström methods select representative training observations and use their kernel relationships to build a low-rank approximation. Random Fourier features approximate certain translation-invariant kernels through randomly sampled frequencies. The former depends on landmark selection; the latter depends on the eligible kernel and the number of sampled features. Both make representation size a controllable resource parameter, allowing accuracy, memory and prediction speed to be investigated together.

The Nyström pipeline here uses 150 features and a fixed gamma of 0.01, different from the best exact-RBF setting. Its 96.22% accuracy therefore describes this configuration. A comparison of the best attainable approximate and exact models would give each a training-side parameter search under an explicit budget. Likewise, LinearSVC and SVC with a linear kernel both construct linear decision boundaries but differ in solvers, default losses and multiclass strategies. Record the actual implementation rather than treating a shared method name as a complete experimental specification. This is particularly relevant when an apparent speed improvement comes partly from a changed objective.

Three controlled experiments consolidate the chapter. First change only the scaling rule and inspect the validation heatmap and number of support vectors. Next hold preprocessing fixed, increase the number of Nyström features, and measure median prediction time over repeated calls. Finally group mistakes by digit class and stroke pattern. Each experiment changes one principal factor and records accuracy, resources and error structure together. The resulting evidence can tell you whether a method fits the task and which next change is most promising: a better representation, a parameter adjustment, a different approximation or a different model family.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M05.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Cortes & Vapnik (1995), Support-vector networks](https://homepages.math.uic.edu/~lreyzin/papers/cortes95.pdf)

   Original development of margins, soft constraints and kernel classification.
2. [scikit-learn — Support Vector Machines](https://scikit-learn.org/stable/modules/svm.html)

   Implementation details and parameters for SVC, SVR and OneClassSVM.

   BSD-3-Clause documentation/code; dataset terms separate.
3. [scikit-learn — SVM Margins Example](https://scikit-learn.org/stable/auto_examples/svm/plot_svm_margin.html)

   Further geometric comparison of C and margins.

   BSD-3-Clause
4. [scikit-learn — Kernel Approximation](https://scikit-learn.org/stable/modules/kernel_approximation.html)

   Conditions and implementations of Nyström and random Fourier features.

   BSD-3-Clause
5. [scikit-learn — load_digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html)

   Bundled handwritten-digit shapes, values and original data link.

   Dataset from UCI Optical Recognition of Handwritten Digits; see linked dataset terms.
