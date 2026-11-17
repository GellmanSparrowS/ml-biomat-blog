# Gel fraction: How much material belongs to the network

Source: https://ml-biomat.com/tutorials/experimental-methods/e02/en/
Language: en

Use connectivity, extraction and mass conservation to separate network fraction from filler, trapped soluble material and mechanical behavior.

## It looks like a gel, but how many chains joined the network?

A transparent liquid becomes a small disc after illumination. If the disc will support cells, the next questions concern its stability in culture medium, the amount of soluble material it releases and the consistency of its network between batches. Seeing that the liquid has gelled establishes a change in overall behavior, but does not reveal how much polymer remains in the connected structure. A gel-fraction experiment exposes the material to a liquid that removes soluble components, then compares dry mass before and after a defined extraction. It replaces a visual impression with a quantitative question about material retained.

Imagine loose yarn spread across a table. Some strands become connected into a large net, some form small clusters, and others remain separate. Lifting the net carries along the strands connected to it, while a suitable liquid can remove mobile clusters and free chains. Real extraction is slower than this simple picture because the soluble chains must travel through the network and surrounding liquid. Long chains, small mesh spacing and thick specimens can delay their departure. A large remaining mass may therefore reflect a high network fraction, incomplete extraction, or contributions from other components that also remain insoluble.

This experiment complements swelling measurements. Swelling asks how much liquid a network retains; gel fraction asks how much original dry material remains after extraction. Both processes can occur in the same specimen. Its wet mass may increase through water uptake while its mass after drying decreases because soluble material has left. Using wet mass in the gel-fraction numerator would mix hydration with the measurement of retained solids. Separate water from dry material first, then distinguish network polymer, filler and extracted substances. That sequence gives every subsequent calculation a clearly identified object.

The chapter moves from connectivity to mass accounting, extraction endpoints, filler correction and research interpretation. A worked composite-gel example can be checked by hand. The complete program also redraws published gel-fraction and mechanical data from an openly licensed study. These measurements show that nearly all polymer can remain in the network while stiffness differs substantially between formulations. The observations fit together once network mass, connection arrangement and load-bearing chains are recognized as different properties. Measuring them together helps decide how to modify a formulation for its intended biological or materials application.

## From a strand to a network: why connectivity can emerge suddenly

A polymer chain contains many connected repeat units, but a long chain alone is not a three-dimensional network. Network formation requires connections between chains or branches, eventually producing a connected structure that extends across the specimen. Think of nodes as molecular segments and links as chemical bonds or stable physical associations. With few links, there are many small clusters. A few strategically placed additional links can join several large clusters into one structure. The onset of gel-like behavior therefore differs from the point at which every reactive group has been consumed. Connectivity concerns the arrangement of bonds as well as their number.

Flory studied gel formation in three-dimensional polymers using molecular statistics in 1941. Stockmayer subsequently developed theories of branched-polymer size distributions and gel formation in work published in 1943 and 1944. This history changes the mental picture: gelation is not every chain simultaneously becoming hard, but a change in connections that produces structure over larger distances. The finite-grid illustration increases the probability of including the same candidate links and highlights the largest connected cluster. It shows how connecting existing pieces can change the scale of the structure without requiring every possible connection to be present.

![Finite-grid connectivity simulation with a fixed set of candidate links; blue marks the largest cluster. Equal-mass nodes illustrate connectivity rather than an experimental gel-fraction measurement. The historical note connects to Flory and Stockmayer’s gelation work.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9c77d44d5be9bbf8d667ade8.svg?v=9c77d44d5be9)

Figure 1Finite-grid connectivity simulation with a fixed set of candidate links; blue marks the largest cluster. Equal-mass nodes illustrate connectivity rather than an experimental gel-fraction measurement. The historical note connects to Flory and Stockmayer’s gelation work.

All nodes in this illustration have equal mass, so the fraction of nodes in the largest cluster is a useful exercise in connectivity. Real polymer chains differ in length and mass, while gravimetric experiments measure a mass fraction. A finite grid can also contain several large clusters; its largest cluster is not a universal experimental definition of gel fraction. The diagram explains a structural idea, whereas extraction separates removable and retained material under specified conditions. Connecting those ideas requires attention to solubility, diffusion, entanglement and the stability of the junctions that hold the material together.

A chain can belong to the retained network without carrying the same elastic load as another chain. A dangling strand attached at only one end adds mass but differs mechanically from a strand linking two load-bearing parts of the network. A local loop can consume reactive groups without improving long-range connectivity. Think of cables on a bridge: a cable spanning two supports and one hanging from a single support may weigh the same while contributing differently to load transfer. Gel fraction, chemical conversion and mechanical modulus consequently deserve separate measurements, followed by an explanation of how their trends relate.

Physical gels make the role of conditions particularly clear. Gelatin associations can dissociate when temperature changes, while ionically cross-linked polysaccharides respond to the surrounding ions. If extraction conditions dismantle the junctions, the remaining fraction includes network disassembly as part of the observation. For a stable covalent network, one usually seeks conditions that dissolve soluble chains while preserving the network of interest. For reversible networks, temperature, ionic environment and observation time belong directly in the scientific question. The measurement then describes the structure retained under those conditions rather than an environment-independent inventory of permanent bonds.

## Account for dry material before choosing the denominator

The simplest case contains one polymer and reliable dry masses before and after extraction. Dividing final dry mass by initial dry mass gives the gel fraction relative to the initial dry polymer. If 100 mg becomes 80 mg after sufficient extraction, the gel fraction is 80%; the remaining 20% was removed under the chosen conditions. This elementary example explains the percentage: for every hundred initial parts of dry material, how many parts remain after extraction? It also shows why both masses must refer to compatible dry states. Residual water in either weighing changes the quantity being compared.

$$
G=\frac{m_r}{m_0},\qquad S=\frac{m_0-m_r}{m_0}=1-G
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/86e66d54c5de5fb86d1da06d.svg) | Gel mass fraction relative to initial dry polymer, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | Extractable mass fraction on the same basis, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/2fae4459b565e480de0d463f.svg) | Dry polymer mass before extraction, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/81e93b3da5f9b0f6c20fbf5a.svg) | Dry polymer retained after sufficient extraction, mg. |

Both fractions use the initial mass. For m0=100 mg and mr=80 mg, G=0.80 and S=0.20, or 80% and 20%. The network remains stable under the experimental definition and other mass contributions are corrected.

The sol fraction commonly denotes the complementary extractable fraction, but complementarity requires the same mass reference. Subtracting 80 mg from 100 mg and dividing by the final 80 mg gives 25%, whereas dividing by the initial 100 mg gives 20%. Those are different ratios and cannot both be added to the same 80% gel fraction. Begin with the material balance: initial polymer equals retained network polymer plus extracted polymer, provided other losses are accounted for. Divide every term by the same initial mass. The equations then follow from conservation rather than memorizing which mass belongs underneath a fraction.

Biomaterials often contain inorganic particles, fibers, pigments or payloads. Consider a 100 mg composite containing 20 mg insoluble filler and 80 mg polymer, of which 80% belongs to the network. Network polymer accounts for 64 mg, soluble polymer for 16 mg and the final dry residue for 84 mg. Reporting 84% describes total composite residue. To estimate the polymer network fraction, remove the appropriate filler contribution from both numerator and denominator: 64 mg divided by 80 mg gives 80%. The two results are both meaningful when named correctly, but they answer different questions about the composite.

$$
G_p=\frac{m_r-m_{f,r}}{m_0-m_{f,0}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9c807c118e583214a0e1035b.svg) | Polymer gel mass fraction after filler correction, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/2fae4459b565e480de0d463f.svg) | Total dry composite mass before extraction, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/81e93b3da5f9b0f6c20fbf5a.svg) | Total dry composite residue after extraction, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/e7f3258e9a04f243f0185368.svg) | Dry filler mass before extraction, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/761a14a6eca3d939d07aa69e.svg) | Dry filler mass retained after extraction, mg. |

The numerator retains network polymer and the denominator initial polymer. Initial total mass 100 mg, residue 84 mg and 20 mg filler at each stage give Gp=(84−20)/(100−20)=0.80. If filler is lost, measure the two contributions separately.

![Constructed mass balance: a 100 mg composite contains 64 mg network polymer, 16 mg soluble polymer and 20 mg insoluble filler. Complete extraction leaves 84% total residue and an 80% polymer gel fraction.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/55688d76f1fd438c349d9c67.svg?v=55688d76f1fd)

Figure 2Constructed mass balance: a 100 mg composite contains 64 mg network polymer, 16 mg soluble polymer and 20 mg insoluble filler. Complete extraction leaves 84% total residue and an 80% polymer gel fraction.

Distinguish filler before extraction from filler after extraction. If particles detach, dissolve or react, subtracting the same assumed mass from both stages becomes incorrect. Formulation records, ash measurements, thermogravimetry or elemental analysis may help identify the filler contribution, with attention to other nonvolatile residues included by each method. A mesh bag, filter or support used during extraction also has its own mass. Subtract its contribution through a suitable blank or tare procedure. Every correction should correspond to a particular substance or object; adding symbols to an equation without measuring their physical counterparts does not improve the accounting.

The initial denominator deserves equal attention. Some precursor mixtures contain salts, initiators and small-molecule additives that were never intended to become polymer network. Using total formulation solids as the denominator yields a total-solids residue fraction. A study of polymer utilization may instead use the dry polymer introduced into the reaction, with transfer losses checked independently. Keep this definition consistent when comparing formulations. A comparison becomes distorted if one material is corrected for additives while another uses every solid in the starting mixture. Retaining the component masses makes it possible to present both useful definitions without confusing them.

## Extraction conditions determine what can leave

Choose a solvent by asking whether it dissolves the intended soluble components. Water works for many hydrophilic polymers, but it does not automatically remove all unconnected hydrophobic chains. A solvent that dissolves the starting polymer may also penetrate the finished gel slowly at the chosen temperature. Test an uncross-linked polymer control for solubility and an appropriate stable network for unwanted damage under the extraction conditions. These controls identify what the washing step does. They help distinguish removal of soluble chains from chemical cleavage, erosion or another process that changes the network during the assay.

Thickness controls the distance soluble chains must travel to reach the bath. A thin film, ground particles and an intact block can require different extraction times despite matching chemistry. Cutting reduces transport distance but may generate network fragments that are difficult to recover. A retaining mesh can preserve fragments while allowing smaller particles to escape, so its opening size participates in the measurement. Gentle mixing reduces a stagnant liquid layer around the specimen; vigorous mixing can break a soft network mechanically. Specimen dimensions, support and agitation should be chosen to remove soluble material while retaining the defined network residue.

Replacing solvent lowers the concentration of extracted material outside the specimen and encourages further migration. Continuous extraction devices repeatedly expose material to relatively fresh solvent, while scheduled batch replacement provides a simpler way of refreshing the concentration environment. The appropriate choice depends on solvent, stability and scale. Heating can accelerate transport but may also dissociate physical junctions or promote chemical reactions. Stronger conditions are therefore not automatically a better extraction. The useful operating window removes the target soluble components while preserving the network state that the experiment is meant to characterize, with evidence that an endpoint has been approached.

An endpoint requires a sequence of observations. Compare dry residues after additional extraction cycles, examine whether polymer signals in later extracts approach the blank, or combine both approaches. Repeated drying of the same specimen can alter structure; independently assigned specimens can instead represent different extraction durations. If residue continues to decrease, investigate degradation, particle loss and solvent incompatibility. The lowest value obtained after the longest treatment is not automatically the best estimate of initial network fraction. Establishing an endpoint together with material stability gives the final weighing a defined experimental meaning rather than a duration chosen by habit.

Blanks and recovery checks separate handling losses from material differences. Empty vessels or mesh bags taken through the same solvent and drying steps reveal changes in the support or residues left by the procedure. A known amount of soluble polymer processed through collection and analysis can estimate losses during transfer, evaporation and recovery. Chromatography can identify residual monomers or initiators when their chemistry matters. Total mass tells how much material left; composition analysis tells what left. Combining those measurements is particularly useful when the extracts will later be related to a cellular response.

## Why one wash and six washes can give different results

A simple model makes extraction arithmetic visible. Start with the same 100 mg composite: 64 mg network polymer, 20 mg filler and 16 mg soluble polymer. Suppose each cycle removes 70% of the soluble material currently remaining, while network and filler stay unchanged. After the first wash, 4.8 mg soluble material remains; after the second, 1.44 mg; after the third, 0.432 mg. Each cycle removes a fixed proportion of the current amount, so the remainder follows a geometric progression. It does not decrease by the same number of milligrams every time.

$$
m_{s,n}=m_{s,0}(1-f)^n,\qquad m_{r,n}=m_g+m_f+m_{s,n}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/ed6a8b77d464f557e04c458b.svg) | Soluble mass still trapped after cycle n, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/4485401618153fae76741122.svg) | Initial soluble mass, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/bc562d54615dad55d095db2a.svg) | Fraction of current soluble material removed per cycle, dimensionless, 0≤f≤1. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2a8560bbc7122a4dd4f1a0.svg) | Extraction-cycle count, nonnegative integer, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/1c08b19480f6f40dc311e3c0.svg) | Total dry residue after cycle n, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/821fabcbaa0d572d6a4846c5.svg) | Unchanged network-polymer mass, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/554f701c791c97b491f4dfff.svg) | Unchanged filler mass, mg. |

The teaching model retains the same fraction of soluble material each cycle. Starting from 16 mg with f=0.7 leaves 4.8 mg after one cycle and 0.432 mg after three; adding 64 mg network and 20 mg filler gives a three-cycle residue of 84.432 mg.

The total residue after one cycle is 88.8 mg, corresponding to an uncorrected residue fraction of 88.8%. Removing the 20 mg filler contribution and dividing by 80 mg initial polymer gives 86%, still above the true network fraction of 80%. After three cycles, the corrected result becomes 80.54%. Two distinct biases are present: filler contributes to total residue, and incompletely extracted soluble polymer contributes to apparent polymer residue. Correcting one does not remove the other. The diagnostic plots separate these effects so that the next improvement can target the actual reason for a high result.

![Constructed extraction diagnostics: total versus filler-corrected residue, material removed each wash, removal-fraction sensitivity and independent specimen results. The three specimen points show calculated values and the horizontal line their mean.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/e840dda76f27949a1673cdf6.svg?v=e840dda76f27)

Figure 3Constructed extraction diagnostics: total versus filler-corrected residue, material removed each wash, removal-fraction sensitivity and independent specimen results. The three specimen points show calculated values and the horizontal line their mean.

The mass removed in each cycle declines, showing that late washes serve a different purpose from the first wash. The first captures readily removable material; later washes help establish whether extraction is nearing completion. A fixed removal fraction is a teaching assumption. Actual extraction depends on solvent quality, chain dimensions, network resistance and duration. If a later wash suddenly removes much more material, revisit temperature, solvent replacement, physical damage and chemical change. Keeping extracts separately identified allows an unexpected mass or analytical signal to be associated with a particular experimental stage.

The interactive experiment changes removal per wash, cycle number and filler content while keeping the true polymer network fraction at 80%. First hold filler constant and increase cycles to see the corrected residue approach 80%. Next use nearly complete extraction and change filler content to see the total residue shift. The two curves distinguish composition from extraction efficiency. This distinction is especially helpful when comparing composites because filler loading may itself be the intended formulation variable. A rise in total insoluble residue should then be examined alongside polymer-normalized values before interpreting it as improved network formation.

## Separate extraction efficiency from filler content

Initial composite mass is 100 mg and true polymer gel fraction is 80%. Change cycle count, removal per cycle and filler content to compare total and polymer-corrected residue.

[Figure: Residue fraction versus extraction cycle](https://ml-biomat.com/tutorials/experimental-methods/e02/en/#E02-plot)

A mass-closure check connects residue and collected extracts. If the initial sample is 100 mg, the final residue is 84 mg and recovered extracts contain 15.2 mg, the accounted mass is 99.2 mg, or 99.2% of the starting value. The remaining 0.8 mg directs attention to transfer, recovery and measurement differences. A sum exceeding the initial mass points toward retained solvent, deposited salts or tare errors. Closure is most useful when the accounted categories are chemically compatible: collecting a salt-containing bath and calling every dried solid extracted polymer would close the wrong material balance.

$$
R_m=\frac{m_r+\sum_{i=1}^{N}m_{e,i}}{m_0}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e11a2e26f9ec9e2808fc57d6.svg) | Mass recovery, dimensionless; multiply by 100 for percent. |
| ![Formula](https://ml-biomat.com/static/agent-math/81e93b3da5f9b0f6c20fbf5a.svg) | Final total dry residue, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/fb04031f2872bf6b1f089faf.svg) | Target dry material recovered from extract i, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/2fae4459b565e480de0d463f.svg) | Initial total dry mass matching the accounted material categories, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Extract index, dimensionless integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Number of extracts, dimensionless integer; the sum adds all extracts. |

Add material retained in the specimen and recovered in all extracts, then compare with the initial mass. Residue of 84 mg plus 15.2 mg recovered extract from 100 mg gives 99.2% recovery.

## The same gel fraction can accompany different stiffness

A whole-specimen average can also hide spatial differences. In a photocross-linked material, light attenuation through thickness, surface oxygen or uneven component distribution can produce regions with different connectivity. A high overall gel fraction can coexist with different mechanical states at the surface and in the interior. Comparing thicknesses, illumination directions or sampled regions, together with spatially resolved spectroscopy or mechanical measurements, can reveal this pattern. The resulting improvement may concern preparation uniformity rather than raising an already high average residue fraction. A specimen's location and orientation can therefore be useful metadata even in an experiment based on total mass.

A gel fraction near 100% means almost all initial polymer remains in the residue under the stated extraction definition. It does not specify the chain length between junctions or the amount of polymer per unit hydrated volume. Two nets may include all their strands while having different spacing between knots and different load-bearing paths. Swelling also changes volume and chain spacing. Mechanical interpretation therefore needs polymer concentration, network structure, hydration and loading timescale alongside gel fraction. The mass fraction identifies one aspect of the network; the modulus describes its response under a particular deformation and measurement condition.

Open experimental data make this distinction concrete. Velasco-Rodriguez and colleagues compared modified gelatin, modified hyaluronic acid and mixed networks, reporting gel fraction alongside elastic modulus. The figure redraws the paired quantities from their table. Horizontal error bars retain the error values reported with gel fraction, and the right panel pairs each formulation's fraction and modulus. Points with similar fractions occupy different modulus values. Each point represents a formulation, so the cloud should be read as a comparison across compositions rather than a single material following one continuous path as cross-linking increases.

![Actual published data redrawn from Velasco-Rodriguez et al. (2021), Table 1, International Journal of Molecular Sciences 22:6758, DOI 10.3390/ijms22136758, CC BY 4.0. Gel fractions, moduli and reported error values are retained; the table does not explicitly label the error statistic, so no new label is assigned.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/72e6413b6c8502e13fb0512a.svg?v=72e6413b6c85)

Figure 4Actual published data redrawn from Velasco-Rodriguez et al. (2021), Table 1, International Journal of Molecular Sciences 22:6758, DOI 10.3390/ijms22136758, CC BY 4.0. Gel fractions, moduli and reported error values are retained; the table does not explicitly label the error statistic, so no new label is assigned.

The published table's error values are retained without assigning an uncertainty label that the table does not explicitly provide. In your own experiment, identify whether error bars represent standard deviation, standard error or a specified confidence interval, and state the number of independent specimens. Three independent gel fractions can be shown as individual points with their mean and between-specimen standard deviation. Three repeated weighings of one specimen instead describe weighing repeatability. Keeping these levels separate shows whether the dominant variation arises from measurement, specimen preparation or independent batches, which determines what should be improved next.

The connection to biological compatibility also passes through intermediate measurements. Extractable material may include unconnected polymer, additives or reaction products; its effect on cells depends on identity, concentration and exposure. Chromatography, spectroscopy or a suitable targeted assay can establish composition, followed by cellular experiments with defined controls and exposure conditions. This forms an explanatory chain from preparation to extract to response. Maximizing gel fraction alone may overlook an overly dense network, restricted transport or an unsuitable mechanical environment. A formulation is selected for the combination of properties required by its application, rather than a single percentage.

High chemical conversion can coexist with local loops or dangling structures and need not produce a proportional gain in effective connectivity. Spectroscopy can follow reactive-group consumption, extraction can measure insoluble network mass, swelling can characterize hydration, and rheology or mechanical testing can quantify load response. Agreement among these measurements strengthens a structural explanation; differing trends can reveal changes in network organization. The next experiment should address the layer of information that is missing. This approach lets a discrepancy guide a useful measurement instead of forcing every observation to follow a single assumed relationship.

## Use mass accounting to improve the next material batch

When returning to swelling, update the dry-mass reference after extraction. Suppose 100 mg of initial dry polymer leaves 80 mg of network, which subsequently reaches a wet mass of 800 mg. Dividing by the original 100 mg gives a ratio of eight; dividing by the remaining 80 mg network gives ten. The first describes wet mass relative to the original polymer input, while the second describes hydration of the network actually present. Retaining both dry masses lets those quantities answer separate questions. It also prevents extraction loss from being mistaken for a difference in the water-holding behavior of otherwise comparable networks.

The complete program begins with an explicit composition and tracks network, filler and soluble material through successive extraction cycles. It exports raw residue fractions and polymer-corrected fractions separately. Three specimen records with different initial masses demonstrate correction before averaging. Another bundled table contains the published experimental values and is read directly for plotting. Constructed data explain the calculation, while published measurements reveal relationships across real formulations. Their identities remain explicit in data files and captions. Keeping these roles separate makes the example useful both for learning arithmetic and for practicing the interpretation of scientific evidence.

### Complete Python: Extraction endpoints, filler correction and published data

The program exports cycle-by-cycle balances, specimen corrections, four figures and a numerical summary. The published table and CC BY notice are bundled.

```
"""Gel fraction: extraction mass balance, filler correction, and published network properties."""
from pathlib import Path
import argparse,json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def extraction(cycles,removal=.7,initial=100.,filler=20.,gel_fraction=.8):
    polymer=initial-filler;network=polymer*gel_fraction;sol=polymer-network
    trapped=sol*(1-removal)**np.asarray(cycles)
    residual=network+filler+trapped
    return residual,100*residual/initial,100*(residual-filler)/polymer,trapped

def connected_components(n,edges):
    parent=list(range(n))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for i,j in edges:parent[find(i)]=find(j)
    groups={}
    for i in range(n):groups.setdefault(find(i),[]).append(i)
    return sorted(groups.values(),key=len,reverse=True)

def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={x.name for x in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    rng=np.random.default_rng(202);coords=np.array([(i%6,i//6) for i in range(36)]);edges=[(i,j) for i in range(36) for j in range(i+1,36) if np.abs(coords[i]-coords[j]).sum()==1];scores=rng.random(len(edges));sizes=[]
    fig,ax=plt.subplots(1,3,figsize=(12,4.5))
    for a,p in zip(ax,[.2,.5,.85]):
        active=[e for e,s in zip(edges,scores) if s<p];groups=connected_components(36,active);largest=set(groups[0]);sizes.append(len(largest))
        for i,j in active:a.plot(coords[[i,j],0],coords[[i,j],1],color='#186e83' if i in largest else '#c4cbd0',lw=2)
        a.scatter(*coords.T,c=['#186e83' if i in largest else '#cd803f' for i in range(36)],s=36,zorder=4);a.set_aspect('equal');a.axis('off');a.set_title(tr(f'连接概率 {p:.2f}\n最大连通簇 {len(largest)}/36',f'Bond probability {p:.2f}\nLargest connected cluster {len(largest)}/36'))
    fig.text(.5,.02,tr('1941–1943：Flory 与 Stockmayer 将成胶理解为分支连接的统计问题。','1941–1943: Flory and Stockmayer treated gelation as a statistical connectivity problem.'),ha='center',fontsize=10);save(fig,'connectivity')
    fig,ax=plt.subplots(1,2,figsize=(11,4.8));names=tr(['提取前','充分提取后'],['Before extraction','After complete extraction'])
    ax[0].bar(names,[64,64],label=tr('网络聚合物','Network polymer'),color='#186e83');ax[0].bar(names,[16,0],bottom=[64,64],label=tr('可溶聚合物','Soluble polymer'),color='#cd803f');ax[0].bar(names,[20,20],bottom=[80,64],label=tr('不溶填料','Insoluble filler'),color='#8160a1');ax[0].set(ylabel=tr('干质量 / mg','Dry mass / mg'),title=tr('A  100 mg 复合材料的质量去向','A  Mass accounting for a 100 mg composite'));ax[0].legend(fontsize=9)
    ax[1].barh(tr(['原始残留比','聚合物凝胶分数'],['Raw residue fraction','Polymer gel fraction']),[84,80],color=['#8160a1','#186e83']);ax[1].set(xlim=(0,105),xlabel=tr('质量分数 / %','Mass fraction / %'),title=tr('B  分子和分母同时扣除填料','B  Remove filler from numerator and denominator'))
    for i,v in enumerate([84,80]):ax[1].text(v+1,i,str(v),va='center')
    fig.tight_layout();save(fig,'accounting')
    cycles=np.arange(7);residual,raw,corrected,trapped=extraction(cycles);removed=np.r_[0,-np.diff(trapped)];np.savetxt(output/'extraction.csv',np.column_stack([cycles,residual,raw,corrected,trapped,removed]),delimiter=',',header='cycle,residual_mg,raw_percent,polymer_corrected_percent,trapped_sol_mg,removed_this_cycle_mg',comments='')
    specimen_initial=np.array([100.,120.,90.]);specimen_filler=.2*specimen_initial;specimen_final=.8*(specimen_initial-specimen_filler)+specimen_filler+np.array([.3,-.2,.1]);measured=100*(specimen_final-specimen_filler)/(specimen_initial-specimen_filler)
    np.savetxt(output/'specimens.csv',np.column_stack([specimen_initial,specimen_filler,specimen_final,measured]),delimiter=',',header='initial_mg,filler_mg,extracted_dry_mg,polymer_gel_percent',comments='')
    fig,ax=plt.subplots(2,2,figsize=(11,7));ax=ax.ravel();ax[0].plot(cycles,raw,'o-',label=tr('未扣填料','Filler uncorrected'));ax[0].plot(cycles,corrected,'s-',label=tr('扣除填料','Filler corrected'));ax[0].axhline(80,color='#707c82',ls='--');ax[0].set(ylabel=tr('残留分数 / %','Remaining fraction / %'),title=tr('A  提取不足与填料是两个偏差','A  Incomplete extraction and filler are distinct biases'));ax[0].legend(fontsize=9)
    ax[1].bar(cycles[1:],removed[1:],color='#cd803f');ax[1].set(ylabel=tr('本次提取物 / mg','Mass extracted in this wash / mg'),title=tr('B  每一次换液带走多少','B  Material removed by each wash'))
    for f in [.3,.5,.7,.9]:ax[2].plot(cycles,extraction(cycles,f)[2],'.-',label=f'{f:.1f}')
    ax[2].axhline(80,color='#707c82',ls='--');ax[2].set(ylabel=tr('校正后残留分数 / %','Corrected remaining fraction / %'),title=tr('C  每次去除比例改变终点接近速度','C  Removal fraction controls endpoint approach'));ax[2].legend(title=tr('每次去除比例','Removal per wash'),fontsize=9)
    ax[3].plot(np.arange(1,4),measured,'o',ms=8);ax[3].axhline(measured.mean(),color='#cd803f');ax[3].set(xticks=[1,2,3],ylim=(78,82),xlabel=tr('独立样品编号','Independent specimen'),ylabel=tr('聚合物凝胶分数 / %','Polymer gel fraction / %'),title=tr('D  先逐样品校正，再汇总','D  Correct individual specimens before averaging'))
    for a in ax[:3]:a.set_xlabel(tr('提取循环次数','Extraction cycle'))
    fig.tight_layout();save(fig,'extraction')
    with Path(__file__).with_name('published_table.csv').open(encoding='utf8') as f:rows=list(csv.DictReader(f))
    g=np.array([float(r['gel_percent']) for r in rows]);ge=np.array([float(r['gel_error']) for r in rows]);m=np.array([float(r['modulus_kPa']) for r in rows]);me=np.array([float(r['modulus_error']) for r in rows]);labels=[r['formulation'] for r in rows]
    fig,ax=plt.subplots(1,2,figsize=(12,6.8),gridspec_kw={'width_ratios':[1.3,1]});y=np.arange(len(rows));ax[0].errorbar(g,y,xerr=ge,fmt='o',capsize=3,color='#186e83');ax[0].set(yticks=y,yticklabels=labels,xlim=(55,109),xlabel=tr('凝胶分数 / %','Gel fraction / %'),title=tr('A  公开表格中的凝胶分数','A  Gel fractions from a published table'));ax[0].invert_yaxis()
    colors=['#186e83']*3+['#cd803f']*3+['#8160a1']*6
    for i in range(len(rows)):ax[1].errorbar(g[i],m[i],xerr=ge[i],yerr=me[i],fmt='o',color=colors[i],alpha=.8,capsize=2)
    ax[1].set(xlabel=tr('凝胶分数 / %','Gel fraction / %'),ylabel=tr('弹性模量 / kPa','Elastic modulus / kPa'),title=tr('B  质量连入网络与刚度并非一一对应','B  Network mass and stiffness are not one-to-one'))
    ax[1].text(.04,.96,tr('蓝：HAMA\n橙：GelMA\n紫：混合网络','Blue: HAMA\nOrange: GelMA\nPurple: mixed networks'),transform=ax[1].transAxes,va='top',fontsize=10)
    fig.suptitle('Velasco-Rodriguez et al. (2021), Table 1 · CC BY 4.0',fontsize=11);fig.tight_layout();save(fig,'published')
    summary={'worked_example':{'network_mg':64.,'raw_fraction_percent':84.,'polymer_fraction_percent':80.,'sol_fraction_percent':20.,'closure_percent':99.2},'extraction':{'cycle1_corrected_percent':float(corrected[1]),'cycle3_corrected_percent':float(corrected[3]),'cycle6_trapped_mg':float(trapped[6])},'specimens':{'mean_percent':float(measured.mean()),'sd_percent':float(measured.std(ddof=1))},'published':{'rows':len(rows),'hama_modulus_ratio':m[2]/m[0]},'connectivity':{'largest_cluster_sizes':sizes}}
    assert abs(corrected[1]-86)<1e-12;assert abs(corrected[3]-80.54)<1e-12;assert abs(residual[-1]+sum(removed)-100)<1e-12
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--language',choices=['zh','en'],default='zh');args=parser.parse_args();main(args.output,args.language)
```

After execution, check the corrected values of 86% after one cycle and 80.54% after three cycles. Then confirm that all material removed plus the final residue returns the original 100 mg in the ideal model. Change removal per wash from 0.7 to 0.3 and compare the number of cycles needed to reach a chosen endpoint tolerance. Alternatively, increase filler loading and inspect the gap between corrected and uncorrected results. These exercises identify different information needs in a real experiment: more extraction, better filler measurement, improved mass recovery or additional independent specimens.

Connect specimen identifiers, initial dry mass, final dry residue, extraction conditions and composition corrections in one data record. Photographs can document whether a soft gel remains intact after extraction. Turbidity or sediment in the extract of a composite deserves examination for escaped particles. For degradable networks, continuing mass loss should be compared with a separate degradation experiment. These observations explain why one mass difference represents removal of soluble chains while another includes fragmentation or changing chemistry. They make the gravimetric result easier to interpret without replacing the quantitative measurements that establish its magnitude.

The next chapter turns time-dependent material change into the main question. Gel-fraction measurements distinguish the starting network and extractable material through a defined separation. Degradation experiments follow changes in chains or junctions and relate them to mass, molecular size, structure and function. Establishing the initial network fraction makes that later interpretation clearer. Early mass loss may reflect soluble material already present at the start, whereas subsequent loss can arise from newly generated fragments. A well-characterized starting state provides the basis for separating those possibilities as the material evolves in its environment.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/E02.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [IUPAC Gold Book: gel fraction](https://goldbook.iupac.org/terms/view/GT07551)

   Terminology for the mass fraction of network material.

   Definition reference; no assets reproduced.
2. [Stockmayer (1943). Theory of Molecular Size Distribution and Gel Formation in Branched-Chain Polymers](https://doi.org/10.1063/1.1723803)

   Historical original paper on gelation and branched-chain distributions.
3. [Kovac and Fixman (2017). Walter H. Stockmayer, National Academy of Sciences Biographical Memoir](https://www.nasonline.org/wp-content/uploads/2024/10/Stockmayer_Walter.pdf)

   Documents the relationship between Flory’s 1941 work and Stockmayer’s 1943–1944 studies.

   Historical reference; no photographs or text reproduced.
4. [Hiroki et al. (2011). Biodegradability of Blend Hydrogels Based on Carboxymethyl Cellulose and Carboxymethyl Starch](https://www.jstage.jst.go.jp/article/tmrsj/36/3/36_397/_pdf)

   Extraction, dry-mass and swelling definitions in an original experiment.
5. [Velasco-Rodriguez et al. (2021). Hybrid Methacrylated Gelatin and Hyaluronic Acid Hydrogel Scaffolds](https://www.mdpi.com/1422-0067/22/13/6758)

   Actual gel-fraction and modulus data, with the extraction procedure.

   CC BY 4.0; Table 1 data transcribed and plotted with attribution.
