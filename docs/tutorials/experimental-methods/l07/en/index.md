# Western blotting: Band identity, intensity and comparison

Source: https://ml-biomat.com/tutorials/experimental-methods/l07/en/
Language: en

Follow separation, transfer, recognition and imaging to a protein measurement with a defined denominator.

## What does a dark protein band actually tell us?

Did a material increase a cellular protein, or cause that protein to be cleaved into smaller fragments? Did a signaling protein change its modification state while its total amount remained similar? These questions concern molecular form as well as quantity. Western blotting combines separation with recognition: gel electrophoresis distributes a complex protein mixture according to migration behavior, and antibodies identify a target within that distribution. Band position supplies apparent size information. Band signal supports quantitative comparison when the relevant part of the measurement chain operates in a suitable range.

Imagine objects moving through an obstacle-filled passage. If every object experiences a different driving force, their final positions are difficult to interpret. Common SDS polyacrylamide gel electrophoresis helps unfold proteins and establish a relatively consistent relationship between charge and mass, then uses the gel network to separate them. The analogy explains the direction of separation, but proteins are not rigid spheres and migration is not a perfect weighing process. A ladder measured on the same gel provides an apparent molecular-mass scale, which is interpreted alongside the expected forms of the target.

Band intensity has passed through another sequence: extraction, loading, separation, transfer, antibody binding, reporter generation, and imaging. Changes at any stage can alter the final signal. Comparing treatment and control therefore requires comparable conditions and a suitable reference for material entering each lane. Normalization addresses a specific question: did the target become more abundant relative to the sample, or did more sample enter this lane overall? The reference gives that division a meaning rather than simply making the bands look consistent.

The chapter follows a constructed blot with a known answer and a measured dilution series from a published study. In the constructed example, treatment doubles target abundance relative to total protein, while loading and transfer vary between lanes. The program integrates actual generated pixel arrays and asks whether normalization recovers the known change. The measured figure shows that different targets and detection methods have different quantitative ranges. Linking appearance, pixel measurement, and biological interpretation makes the familiar row of bands into a readable experiment.

## Preserve the separated pattern and make it accessible to antibodies

After electrophoresis, proteins occupy positions inside a gel, while antibodies need access to those positions. In 1979, Towbin, Staehelin, and Gordon described electrophoretic transfer from polyacrylamide gels to nitrocellulose sheets. Towbin later recalled the problem of characterizing antibodies against separated ribosomal proteins: the dense gel was an obstacle to antibody movement. Moving the separated pattern onto an accessible surface connected the strengths of electrophoresis and molecular recognition. The historical idea helps explain why transfer is a central part of the method.

A printing analogy is useful here. Preserve relative positions in the plane while moving protein out of the gel onto a membrane. In electrophoretic transfer, the field drives charged proteins across the gel thickness, with the membrane placed in their path. Gel, membrane, and buffer need good contact. A trapped bubble creates a local interruption and can leave a patch with poor transfer. Inspecting the overall transferred-protein pattern helps distinguish such a spatial defect from a target-specific biological change.

![Original illustration of 1979 electrophoretic transfer: separation in a gel becomes an antibody-accessible pattern on a membrane.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/45ec3241c57170b199af278c.svg?v=45ec3241c571)

Figure 1Original illustration of 1979 electrophoretic transfer: separation in a gel becomes an antibody-accessible pattern on a membrane.

Large and small proteins need not transfer equally under one condition. A large protein may leave the gel slowly, while a small protein can be poorly retained or pass through a membrane under some conditions. Gel composition, membrane type, pore size, buffer, and duration therefore relate to the target range. More transfer time is not a universal improvement. Inspecting protein on the membrane and protein remaining in the gel helps identify where the current procedure loses useful material. The goal is comparable transfer in the range being studied.

After transfer, blocking reduces unwanted antibody adsorption, primary antibody recognizes the target, and a labeled secondary or another reporter arrangement generates signal. Chemiluminescence uses an enzyme-driven light-producing reaction; fluorescence requires suitable excitation. Their time dependence, channels, and useful intensity ranges differ. The membrane supplies the spatial pattern, while detection converts it into numbers. Comparing methods or exposures should return to original measurements and validated ranges rather than only to how white the displayed background appears.

## Give the material entering a lane a clear definition

Lysis releases cellular material, but proteins differ in extractability. Membrane-associated, cytoskeletal, and readily soluble proteins can respond differently to buffers and handling. Collecting the supernatant after centrifugation defines the fraction recovered under those conditions. A target remaining in the pellet will be underrepresented if only the supernatant is examined. Choose preparation around target location and the research question, then check that the relevant fraction is retained. Cells attached to a material can also be recovered with different efficiencies between groups, making collection part of the comparison.

Proteases cleave proteins, while phosphatases remove certain phosphate modifications. Opening a cell allows enzymes and substrates that were previously separated to meet. Preparation time, temperature, and protective conditions can therefore change the forms later observed. Measuring total protein and measuring a phosphorylated form require preservation of related but distinct properties. Consistent collection timing and handling reduce changes introduced after sampling. When smaller bands appear, controls can investigate biological processing, preparation-associated degradation, and recognition of another protein.

In conventional denaturing electrophoresis, SDS helps unfold proteins and supplies negative charge. Reducing agents address disulfide bonds, separating chains connected by those bonds. These treatments perform different jobs, and the desired molecular form determines whether reducing conditions are appropriate. Heating is also specimen-dependent; unsuitable treatment can promote aggregation or impair recognition for some proteins. Record denaturation, reduction, and heating conditions so that migration patterns remain connected to preparation state. Samples in one comparison should share the relevant handling conditions.

Measuring lysate concentration converts a volume decision into a protein-amount decision. A lysate containing two micrograms per microliter requires ten microliters to load twenty micrograms. A second lysate at one microgram per microliter requires twenty microliters, with final buffer conditions and volume arranged consistently. The protein assay must be compatible with detergents, reducing agents, and other lysate components. If standards and lysates behave differently in that assay, nominally equal loading can inherit a matrix-dependent concentration error.

$$
V=m/C
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | Sample volume taken, μL |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Planned protein mass, μg |
| ![Formula](https://ml-biomat.com/static/agent-math/c0c348883f19c18a48444415.svg) | Sample total-protein mass concentration, μg/μL |

Mass equals concentration times volume. Loading 20 μg from 2 μg/μL requires 10 μL. Use a concentration assay compatible with the lysate and match final loading volume after buffer addition.

Equal total protein defines one denominator; it does not automatically mean equal cell numbers. A treatment changing cell size or total protein content can change how many cells are represented by twenty micrograms of lysate. Total-protein normalization directly addresses target abundance relative to the extracted protein mixture. A per-cell question additionally needs cell counts, extraction volume, and recovery information. Retaining several original quantities allows different questions to be examined while keeping the meaning of each final ratio explicit.

## Read the band position together with the rest of its lane

A molecular-mass ladder contains proteins of known sizes run alongside the samples. Within an appropriate range, the logarithm of molecular mass can be approximately related to migration distance. Greater migration usually corresponds to smaller apparent mass. On a logarithmic scale, the changes from one hundred to fifty and from fifty to twenty-five are equal halving steps. The constructed ladder uses distances of twenty, forty, and sixty millimeters for those masses in kilodaltons, making the local calibration easy to check.

$$
\log_{10}\!\left(\frac{M}{1\,\mathrm{kDa}}\right)=\alpha-\beta d
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/34058a2a5d1de088feed7d98.svg) | Ladder-estimated apparent molecular mass, kDa |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Migration distance from a shared origin, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | Fitted intercept, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/f27acf6959fc15846a7239da.svg) | Positive distance coefficient, inverse mm |

Fit within a ladder region approximately linear in log mass. Constructed distances 20, 40 and 60 mm correspond to 100, 50 and 25 kDa; beta=0.0150515/mm and alpha=2.30103 give 50 kDa at 40 mm. Division by 1 kDa makes the logarithm dimensionless. Use the calibrated region of an actual ladder.

A band near the expected mass supplies one clue about identity. Glycosylation, cleavage, isoforms, aggregation, and unusual migration can shift its position, and an antibody can recognize another protein of similar size. A target-reduced or target-absent sample, a positive sample, or an independent antibody recognizing another epitope can test the association between the selected band and target. For a phosphorylation-specific antibody, a modification-changing treatment and measurement of total target provide complementary information. Select controls according to the particular identity or molecular form being established.

The full membrane image preserves valuable context. Cropping immediately around an expected position removes higher aggregates, lower fragments, and other recognized bands from view. Inspect the lane before defining the peak for integration. The constructed image deliberately retains a weaker band below the designated target. It reminds us that every visible feature is not automatically part of one quantitative object. The example integrates only the preselected target region and leaves the second peak visible so that the choice can be examined.

Curvature, tails, and band width also report on the experiment. Excess loading, sample composition, and uneven separation can broaden peaks or distort lanes. Overlapping features make the integration boundary consequential. Selecting an appropriate gel range and load so that the target is resolved is more informative than trying to split badly overlapping peaks with an increasingly elaborate box. Prestained ladders make migration and transfer convenient to follow, but attached dyes can affect mobility, so apparent size should be interpreted with the ladder's stated calibration conditions.

The logarithmic calibration also explains why one constant conversion from pixels to kilodaltons is unsuitable across a broad gel. Equal distances correspond approximately to equal mass ratios, not equal mass differences. Interpolate between relevant nearby markers rather than extending a local fit far beyond its range. Keep migration distance and image coordinates distinct: resizing an exported image changes pixel distances, while the original physical separation is unchanged. The numerical example uses a deliberately defined millimeter scale to keep this distinction visible.

## From pixel addition to a normalized fold change

A membrane image is a two-dimensional numerical array. Integrated band signal adds the values in a selected region. Background occupies the same pixels, so subtraction must account for region size. If four hundred pixels sum to twelve thousand and background is twenty units per pixel, eight thousand units come from background and the corrected integral is four thousand. Subtracting twenty only once would leave most background in the result. Software mean intensity and integrated intensity describe different quantities, so establish which output is being used.

$$
S=\sum_{j=1}^{n}I_j-nB
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | Background-corrected region integral, signal units |
| ![Formula](https://ml-biomat.com/static/agent-math/2182e4a63941864596054a3f.svg) | Raw signal at pixel j, signal units |
| ![Formula](https://ml-biomat.com/static/agent-math/85c7a0c0a90e94bee07686fc.svg) | Pixel index, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Number of region pixels, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | Representative mean background signal per pixel |

The sum contains band plus background over every pixel. For 400 pixels summing to 12000 and background 20, the net integral is 4000. The example uses unclipped linear digital signals; spatially varying backgrounds require spatially matched estimates.

Background estimation depends on its spatial pattern. A nearby band-free region can estimate a uniform background. A slowly changing background can be estimated from suitable regions above and below the target or another checked local method. Do not treat a neighboring weak band as pure background or alter rules separately to force groups into agreement. The program uses symmetric local regions around the target peak. For total protein, it uses an adjacent strip and explicitly accounts for the known horizontal gradient in the constructed background. Saved arrays allow every step to be inspected.

An integration region should cover the selected peak completely under a consistent rule. A small box clips the tails of a broad band; a large box can include neighboring peaks and additional background variation. Similar bands can use common widths and boundary rules. Strongly different shapes require checking whether that same box still captures the same object. A longitudinal lane profile turns bands into peaks and background into a baseline. It can reveal clipping, shoulders, and tails that are difficult to judge in a small image thumbnail.

![Simulated blot pixels, selected regions, a lane profile and the resulting quantification. Lanes 1–3 are controls; lanes 4–6 have a true twofold target abundance. A second weak band remains visible in the full image.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9ebe6c74e36032697b1b93e1.svg?v=9ebe6c74e360)

Figure 2Simulated blot pixels, selected regions, a lane profile and the resulting quantification. Lanes 1–3 are controls; lanes 4–6 have a true twofold target abundance. A second weak band remains visible in the full image.

Normalization divides corrected target signal by a reference from the same lane, then compares that ratio with control. Suppose control target and total-protein signals are ten thousand and one hundred thousand, while treatment values are twenty-four thousand and one hundred twenty thousand. Target alone suggests a 2.4-fold change. Normalizing by total protein gives a twofold change. This division assumes that target and reference respond appropriately over their working ranges and that the reference reflects the shared variation being corrected. A mathematical ratio cannot remove differences that the reference does not track.

$$
R_i=T_i/P_i,\qquad F_i=R_i/\overline{R}_{\rm control}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/df8767aa6cc94e0af05ed184.svg) | Target-to-total-protein integral ratio for sample i, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Sample index, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/d337cf254934852ef394972a.svg) | Background-corrected target integral, signal units |
| ![Formula](https://ml-biomat.com/static/agent-math/0cabdc5951d269a0b202838f.svg) | Corrected total-protein lane integral on a consistent signal scale |
| ![Formula](https://ml-biomat.com/static/agent-math/9b2693d2330ea11c23fe03a6.svg) | Fold relative to mean control ratio, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/56cda88a0249301c9488c9fc.svg) | Arithmetic mean of individual control ratios, dimensionless |

Normalize each lane by its own total protein, then divide by the mean control ratio. Control 10000/100000=0.1 and treatment 24000/120000=0.2 give twofold; target alone gives 2.4. Both signals must be in established response ranges. This denominator expresses target per recovered total protein.

The six constructed lanes have target values of one in control and two in treatment, with additional loading and transfer variation. Target-only comparisons contain that extra fluctuation. Total-protein normalization moves the comparison closer to the known group difference. Individual lanes remain visible rather than being replaced by one representative band. In actual research, lanes from independently prepared samples support biological comparisons, while repeated loading of one lysate investigates technical repeatability. Preserve the map connecting sample, lane, and membrane so that later summaries retain those experimental levels.

The denominator also changes the biological interpretation. Dividing phosphorylated-target signal by total-target signal addresses relative modification of that target under the chosen antibody conditions. Dividing total target by total protein addresses target abundance within the extracted mixture. Neither ratio alone provides an absolute fraction of molecules carrying a modification unless the detection responses are appropriately calibrated. Keeping all component signals allows the two questions to be examined separately and makes an apparent change caused by a falling denominator easier to recognize.

## Why the darkest band can be harder to compare

The darkest band does not necessarily contain the most quantitative information. Signal can be proportional to target amount over one range and flatten beyond it. Flattening can arise from loading and membrane capacity, antibody access, reporter chemistry, or detector clipping. Clipping is especially easy to visualize: a detector records one maximum value even when two different inputs exceed it. Shorter exposure can investigate detector saturation. If a loading series still fails to scale proportionally after exposure is changed, earlier stages of the detection chain deserve examination.

A loading series from a representative pooled sample can test target and reference ranges together. An abundant housekeeping protein may approach a plateau at a load where a scarce target is only becoming visible. Housekeeping proteins are commonly selected as reference candidates because of their basic cellular roles, but the label does not guarantee stability under every treatment. Check both biological stability and measurement range. Total-protein staining offers another denominator, with its own requirements for background handling, proportional response, and interpretation of sample composition.

The measured dilution series from Taylor and colleagues shows these distinctions. The samples contain added ADH and endogenous GAPDH, corresponding to the upper and lower bands. The panels compare digital imaging and film detection. Follow successive halving steps in the load and inspect whether both targets halve in signal throughout the series. They do not. Curve error bars represent the standard error of the mean from four blots. The example teaches how to identify useful ranges, rather than prescribing its particular loads for another antibody or instrument.

![Taylor et al. (2013), Fig. 3, reproduced in full under the article’s Creative Commons Attribution license. ADH and GAPDH dilution series compare digital and film imaging; error bars show SEM across four blots.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/3b74bd7b6128e5c5d7c89e15.svg?v=3b74bd7b6128)

Figure 3Taylor et al. (2013), Fig. 3, reproduced in full under the article’s Creative Commons Attribution license. ADH and GAPDH dilution series compare digital and film imaging; error bars show SEM across four blots.

The interactive experiment isolates detector clipping. Two constructed peaks have identical shapes and a true twofold difference in target amount, with known background. At moderate exposure, their integrated ratio is two. Increasing exposure flattens the stronger peak first and lowers the measured fold change. Reduce both loads together and observe recovery of proportionality. Dashed curves retain the signals that would have been recorded without clipping, showing exactly which part is lost. The exercise compares exposure and loading changes within this stated mechanism; it does not model membrane or antibody saturation.

## Interactive experiment: Does exposure change the fold change?

Two constructed bands always differ twofold in true target amount. Adjust exposure and shared loading to see clipping at 255 counts, then compare background-corrected integrals. Background also scales with exposure; dashed curves show an unlimited detector response.

[Figure: Raw intensity profiles of two bands](https://ml-biomat.com/tutorials/experimental-methods/l07/en/#L07-lab)

![Constructed ladder, detector clipping, fold-change compression and background sensitivity. D compares weak and strong integrals in the same 400-pixel region.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/e8e741f0ef7aac529b7b658b.svg?v=e8e741f0ef7a)

Figure 4Constructed ladder, detector clipping, fold-change compression and background sensitivity. D compares weak and strong integrals in the same 400-pixel region.

Weak bands are also sensitive to background estimates. A fixed error per pixel produces the same integrated error for equal-sized regions, but that error occupies a greater fraction of a weak signal. In the diagnostic figure, both regions contain four hundred pixels. Overestimating background by one unit per pixel removes four hundred units: half of an eight-hundred-unit band but only five percent of an eight-thousand-unit band. This identifies a concrete reason why a very large fold change can depend strongly on a small denominator near background.

Image presentation and numerical processing should remain connected but distinct. A grayscale inversion can display high signals as dark bands without changing the underlying signal array. A common display range makes comparisons easier, while independent contrast adjustment can make unequal bands look similar. Preserve the native measurements and document the transformation used for display. For a scanned film, image darkness has passed through film chemistry and scanning, so its numeric response needs its own calibration. Directly treating every dark pixel value as proportional to emitted light skips that response relationship.

## Connect the complete image, lane values, and biological question

The complete program exports constructed target and total-protein images, corrected integrals and normalized values for every lane, and separate size, background, and saturation diagnostics. Original arrays preserve every pixel. Move an integration region up or down to test whether another peak enters it, or change a background region to see how weak signals respond. Constructed data and the measured publication image are labeled separately. The code does not infer original quantitative measurements from the compressed figure displayed in the paper.

### Complete Python: From band pixels to normalized fold change

Exports full constructed arrays, lane-level CSV, summary and figures; the measured publication image is bundled offline.

```
"""Offline western-blot pixels, lane normalization and dynamic-range exercise."""
from pathlib import Path
import argparse,csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
BLUE='#186e83';AMBER='#cd803f';GREEN='#3c8a6a';PURPLE='#8160a1'
def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def integrated(signal=80.,exposure=1.,ceiling=255.):
    y=np.arange(-20,21);profile=signal*np.exp(-.5*(y/4)**2)
    return float((np.minimum(ceiling,exposure*(profile+20))-exposure*20).sum())
def main(output,language='zh'):
    out=Path(output);out.mkdir(parents=True,exist_ok=True);zh=language=='zh'
    def T(a,b):return a if zh else _label(b)
    plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5'})
    def save(fig,n):fig.savefig(out/f'{n}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(707);yy,xx=np.mgrid[:240,:400];base=20+.025*yy+.01*xx
    target=base.copy();total=base.copy();loads=np.array([1,.8,1.2,1,.8,1.2]);transfers=np.array([1,.9,1.1,.85,1.05,.95]);amount=np.array([1,1,1,2,2,2]);centers=45+60*np.arange(6)
    for i,cx in enumerate(centers):
        shape_x=np.exp(-.5*((xx-cx)/8)**2);factor=loads[i]*transfers[i]
        target+=80*amount[i]*factor*shape_x*np.exp(-.5*((yy-95)/4)**2)
        target+=7*factor*shape_x*np.exp(-.5*((yy-165)/4)**2)
        for y0,a in zip([50,80,110,145,180,210],[18,30,20,26,16,22]):total+=a*factor*shape_x*np.exp(-.5*((yy-y0)/4)**2)
    target+=rng.normal(0,.4,target.shape);total+=rng.normal(0,.4,total.shape);rows=[]
    for i,cx in enumerate(centers):
        mask=(abs(xx-cx)<=16)&(abs(yy-95)<=15)
        bgmask=(abs(xx-cx)<=16)&(((yy>=65)&(yy<=75))|((yy>=115)&(yy<=125)))
        bg=target[bgmask].mean();signal=float(target[mask].sum()-mask.sum()*bg)
        lane=(abs(xx-cx)<=16)&(yy>=30)&(yy<=225)
        side=(abs(xx-(cx+26))<=2)&(yy>=30)&(yy<=225)
        # Correct the known linear x-gradient between adjacent background strip and lane center.
        total_bg=float(total[side].mean()-.01*26)
        total_signal=float(total[lane].sum()-lane.sum()*total_bg)
        rows.append([i+1,'control' if i<3 else 'treated',loads[i],transfers[i],amount[i],signal,total_signal,signal/total_signal])
    with (out/'lanes.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['lane','group','relative_load','relative_transfer','true_target_per_total','target_integral_au','total_protein_integral_au','target_over_total']);w.writerows(rows)
    np.savez_compressed(out/'blots.npz',target=target,total_protein=total,background_plane=base)
    ratio=np.array([r[-1] for r in rows]);normalized=ratio/ratio[:3].mean();rawratio=np.array([r[-3] for r in rows]);rawratio/=rawratio[:3].mean()
    fig,ax=plt.subplots(figsize=(11,5.1));ax.axis('off');ax.set(xlim=(0,12),ylim=(0,7))
    for x0,col,label in [(1.5,BLUE,T('分离后的凝胶','Separated gel')),(6,PURPLE,T('接收蛋白的膜','Receiving membrane'))]:
        ax.add_patch(Rectangle((x0,1.2),2.2,4.7,fc=col,alpha=.13,ec=col))
        for j in range(3):
            for y in [2+j*.3,3.2+j*.2,4.8-j*.3]:ax.plot([x0+.3+j*.55,x0+.7+j*.55],[y,y],color=col,lw=4)
        ax.text(x0+1.1,.6,label,ha='center')
    ax.annotate('',xy=(5.7,3.5),xytext=(4,3.5),arrowprops={'arrowstyle':'->','lw':2});ax.text(4.8,4.1,T('横向电场','Transverse field'),ha='center')
    ax.text(9.8,4.4,T('保留分离位置\n让抗体接近蛋白','Preserve separation\nMake proteins accessible'),ha='center',linespacing=1.7)
    ax.text(6,6.6,T('1979：Towbin、Staehelin、Gordon 的电转移方法','1979: electrophoretic transfer by Towbin, Staehelin and Gordon'),ha='center',fontsize=12)
    fig.text(.5,.02,T('原创示意：条带间的位置关系在转移后保留；不是历史仪器照片。','Original schematic: relative band positions survive transfer; not a historical apparatus photograph.'),ha='center',fontsize=9);save(fig,'history')
    fig,ax=plt.subplots(2,2,figsize=(11,8.4))
    for a,img,title in [(ax[0,0],target,T('A  构造靶标通道','A  Constructed target channel')),(ax[0,1],total,T('B  构造总蛋白通道','B  Constructed total-protein channel'))]:
        a.imshow(img,cmap='gray_r',vmin=15,vmax=200);a.set_title(title);a.set_xticks(centers,range(1,7));a.set_xlabel(T('泳道','Lane'));a.set_yticks([50,95,165,210]);a.set_ylabel(T('纵向位置 / 像素','Vertical position / pixel'))
    for cx in centers:ax[0,0].add_patch(Rectangle((cx-16,80),32,30,fill=False,ec=AMBER,lw=.8))
    profile=target[:,centers[0]-16:centers[0]+17].mean(axis=1);ax[1,0].plot(np.arange(240),profile,color=BLUE);ax[1,0].axvspan(80,110,color=AMBER,alpha=.25);ax[1,0].set(xlabel=T('纵向位置 / 像素','Vertical position / pixel'),ylabel=T('泳道横向平均读数 / a.u.','Lane-width mean signal / a.u.'),title=T('C  积分区域只覆盖指定的靶标峰','C  Integration isolates the selected target peak'))
    ax[1,1].bar(np.arange(6)-.18,rawratio,.35,color=BLUE,label=T('只比较靶标','Target only'));ax[1,1].bar(np.arange(6)+.18,normalized,.35,color=AMBER,label=T('总蛋白归一化','Total-protein normalized'));ax[1,1].set_xticks(range(6),range(1,7));ax[1,1].set(xlabel=T('泳道1–3对照，4–6处理','Lanes1–3control;4–6treated'),ylabel=T('相对各自对照均值','Relative to corresponding control mean'),title=T('D  相同真实倍数，不同加样与转移','D  Shared true fold change, variable loading'));ax[1,1].legend(fontsize=8);fig.tight_layout();save(fig,'pixels')
    fig,ax=plt.subplots(2,2,figsize=(11,8.2));masses=np.array([100,100/np.sqrt(2),50,50/np.sqrt(2),25]);dist=np.array([20,30,40,50,60]);coef=np.polyfit(dist,np.log10(masses),1)
    ax[0,0].plot(dist,masses,'o-',color=BLUE);ax[0,0].set_yscale('log');ax[0,0].set_yticks([25,50,100],[25,50,100]);ax[0,0].set(xlabel=T('迁移距离 / mm','Migration distance / mm'),ylabel=T('表观分子质量 / kDa','Apparent molecular mass / kDa'),title=T('A  构造标尺：对数质量与距离','A  Constructed ladder: log mass and distance'))
    load=np.geomspace(.05,6,100)
    for e,col in [(1,BLUE),(3,AMBER)]:ax[0,1].plot(load,[integrated(80*v,e) for v in load],color=col,label=T(f'曝光{e}倍',f'{e}× exposure'))
    ax[0,1].set(xlabel=T('相对目标量','Relative target amount'),ylabel=T('积分读数 / a.u.','Integrated signal / a.u.'),title=T('B  截顶后信号不再按量增长','B  Clipping breaks proportional response'));ax[0,1].legend(fontsize=8)
    exposures=np.linspace(.2,4,100);fold=[integrated(160,e)/integrated(80,e) for e in exposures]
    ax[1,0].plot(exposures,fold,color=PURPLE);ax[1,0].axhline(2,color=GREEN,ls='--');ax[1,0].set(xlabel=T('曝光倍数','Exposure multiplier'),ylabel=T('测得倍数变化','Measured fold change'),title=T('C  真值2倍在饱和时被压低','C  Saturation compresses a true twofold change'))
    errors=np.linspace(-2,2,50);ax[1,1].plot(errors,100*(800-400*errors)/800,color=BLUE,label=T('弱条带：总净信号800','Weak band: net integral800'));ax[1,1].plot(errors,100*(8000-400*errors)/8000,color=AMBER,label=T('强条带：总净信号8000','Strong band: net integral8000'));ax[1,1].set(xlabel=T('每像素背景高估值 / a.u.','Background overestimate per pixel / a.u.'),ylabel=T('保留下来的净信号 / %','Retained net signal / %'),title=T('D  同一400像素区域的背景敏感性','D  Background sensitivity in400pixels'));ax[1,1].legend(fontsize=8)
    for a in ax.flat:a.grid(alpha=.18)
    fig.tight_layout();save(fig,'diagnostics')
    fig,ax=plt.subplots(figsize=(10,9));ax.imshow(Image.open(Path(__file__).resolve().parent/'taylor2013-figure3.jpg').convert('RGB'));ax.axis('off');ax.set_title(T('真实稀释系列：目标与参照各有工作范围','Measured dilution series: target and reference have distinct ranges'),fontsize=12);fig.text(.5,.015,T('Taylor等，2013，图3；Creative Commons Attribution。\n上、下条带分别为ADH、GAPDH；曲线误差条为4张膜的SEM。','Taylor et al.,2013,Fig.3; Creative Commons Attribution.\nUpper/lower bands: ADH/GAPDH; curve error bars: SEM from4blots.'),ha='center',fontsize=9);fig.tight_layout(rect=[0,.08,1,1]);save(fig,'published')
    assert np.isclose(integrated(160)/integrated(80),2)
    summary={'mass':{'load_volume_ul':20/2,'ladder_midpoint_kDa':float(10**np.polyval(coef,40))},'background':{'corrected_integral':12000-400*20},'normalization':{'raw_ratio':24000/10000,'normalized_fold':(24000/120000)/(10000/100000)},'dynamic':{'linear_fold':integrated(160)/integrated(80),'exposure_three_fold':integrated(160,3)/integrated(80,3)},'pixels':{'mean_control':float(normalized[:3].mean()),'mean_treated':float(normalized[3:].mean()),'individual_normalized':normalized.tolist()}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

Start by checking whether normalization recovers a twofold target change when loading and transfer vary. Then compare the unnormalized fluctuation with the corrected result. A further exercise lets the reference itself change with treatment, revealing the consequence of an unstable denominator. For phosphorylation studies, retain both phosphorylated and total-target signals as well as total protein, so relative modification and overall target abundance can be discussed separately. Each ratio becomes interpretable when its numerator and denominator remain available.

For an experimental comparison, preserve the full membrane as a spatial record, the selected band and integration boundaries as an analysis record, and independent-sample values as the statistical record. A shared reference sample can connect different membranes while each membrane retains its own controls. Describe the specimen and target form, the evidence for band identity, the range used for comparison, and what the denominator represents. The resulting explanation keeps western blotting's distinctive size information while turning band intensity into a defined quantitative comparison.

A shared reference sample connects comparisons made on different membranes. Suppose aliquots of the same pooled lysate give target-to-total ratios of 0.10 on one membrane and 0.08 on another. A study sample with a ratio of 0.16 on the second membrane is twice its local shared reference. Comparing 0.16 directly with 0.10 from the first membrane would instead give 1.6, incorporating a shift in measurement scale. Prepare enough consistent aliquots, check storage stability, and distribute experimental groups across membranes in a balanced arrangement. The shared sample connects measurement scales while independent biological differences remain in the analysis. Its usefulness depends on the same target and reference signals remaining measurable on every membrane.

The direction of an image's gray values also needs attention. Original digital luminescence counts normally increase with detected light, but display software can map larger values to either white or black. Changing that display palette leaves the underlying array unchanged. A scanned film has passed through exposure, development and scanner response, and a darker band may have smaller pixel values. Simply inverting the image reverses numerical direction; it does not reconstruct linearity across every stage of film acquisition. When two programs seem to assign opposite intensity rankings, inspect the data definition before choosing a background correction. Keeping quantitative arrays separately from display images preserves both visual readability and numerical meaning.

Band shape supplies another kind of information. Strong edges with a weak middle suggest inspecting transfer contact and possible bubbles. A curved or diffuse entire lane shifts attention toward loading, salt composition and electrophoresis conditions. A narrow stain crossing all lanes at one height has a different interpretation from an extra coherent band appearing specifically after a biological treatment. Preserve the full membrane and nearby background, then connect the pattern to acquisition and preparation records. This leads to an identifiable experiment: repeat a lower loading amount, adjust transfer conditions, or check target identity with an antibody against another epitope. Cropping a band first removes much of the information needed to select that experiment.

Biological replication can be made concrete with three independently prepared cultures per condition. Their six lysates provide six biological observations. Loading each lysate twice provides technical information about gel and detection repeatability, but still leaves three independent cultures in each group. Average or model those technical repeats at the sample level before the biological comparison, retaining any preparation or membrane pairing in the analysis. By contrast, cutting one large culture into three tubes after lysis creates extraction aliquots of one biological preparation. The distinction matters because an intervention may vary between cultures through cell state, treatment response and growth history; repeated lanes cannot reproduce that variation.

Finally, show enough of the measurement chain to make a numerical comparison intelligible. A target-to-total ratio belongs beside the underlying target and total-protein signals, with the relevant molecular-mass region visible. If a treatment alters the distribution of several target forms, describe whether the analysis follows one form or their combined signal. A combined analysis can answer a total-abundance question, whereas separate bands can reveal processing or modification. Select the integration rule in relation to that biological question and apply it consistently across samples, keeping the full pattern available for further interpretation.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/L07.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Towbin, Staehelin & Gordon (1979): Electrophoretic transfer of proteins](https://doi.org/10.1073/pnas.76.9.4350)

   Original electrophoretic-transfer publication.
2. [Towbin (1988): Citation Classic retrospective](https://garfield.library.upenn.edu/classics1988/A1988M295200001.pdf)

   Author retrospective on protein accessibility and electrophoretic transfer.
3. [Taylor et al. (2013): A Defined Methodology for Reliable Quantification of Western Blot Data](https://pmc.ncbi.nlm.nih.gov/articles/PMC3840294/)

   Dilution series, digital/film imaging and total-protein normalization; measured Fig. 3.

   Creative Commons Attribution, version not stated by article; Fig. 3 reproduced
4. [Thermo Fisher: Western blot sample preparation](https://www.thermofisher.com/us/en/home/life-science/protein-biology/protein-biology-learning-center/protein-gel-electrophoresis-information/western-blot-protocols/western-blot-sample-preparation.html)

   Extraction, protein preservation and assay compatibility.
5. [Thermo Fisher: Total protein normalization](https://www.thermofisher.com/us/en/home/life-science/protein-biology/protein-gel-electrophoresis-western-blot/protein-gel-electrophoresis-western-blot-imaging-analysis/total-protein-normalization.html)

   Total-protein denominator and response-range checks.
6. [Uhlén et al. (2016): A proposal for validation of antibodies](https://pmc.ncbi.nlm.nih.gov/articles/PMC10335836/)

   Application-specific antibody validation.
7. [ImageJ: Analyze menu and gel analysis](https://imagej.net/ij/docs/menus/analyze.html#gels)

   Lane profiles, integrated pixels and retained regions.
