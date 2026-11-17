# HPLC: Separating mixtures in time

Source: https://ml-biomat.com/tutorials/experimental-methods/c01/en/
Language: en

Separate a mixture into distinguishable time signals, then turn peak area into concentration and mass with a clear experimental meaning.

## How do we count only the caffeine in coffee?

Coffee contains many dissolved substances as well as color and aroma. A direct ultraviolet measurement records their combined optical response, while the caffeine we want to measure is only one contributor. Materials research encounters the same difficulty: water exposed to a polymer may contain released drug, residual small molecules and degradation products. Cell-culture medium contains nutrients, metabolites and additives. Measuring one target reliably often begins by separating it from the surrounding mixture and then selecting an appropriate detector.

High-performance liquid chromatography, abbreviated HPLC, passes a liquid mixture through a column containing a stationary separation medium. Different molecules interact with that medium for different average lengths of time. Substances introduced together consequently arrive at the outlet at different times. A detector continuously records what passes it, producing a chromatogram with time on the horizontal axis and a response such as ultraviolet absorbance on the vertical axis. The column separates, and the detector translates passing material into a signal. Their combination creates an analytical measurement.

Imagine people crossing a shopping district from the same starting point. Some keep walking; others stop repeatedly, so their arrival times differ. Molecules have no intentions: thermal motion and interactions determine their exchanges between the moving liquid and stationary environment. Even molecules of the same compound follow somewhat different histories, producing a distribution of arrival times rather than a perfectly synchronized group. Good separation therefore requires both different average arrival times for different compounds and sufficiently narrow arrival distributions for each compound.

This chapter follows a complete quantitative experiment: understand the column, separate a target from its neighbors, convert peak area to concentration, and return that concentration to the original research question. Caffeine provides a familiar motivation, while explicitly constructed data make the calculations inspectable. The same reasoning applies to residual monomer, additives in material extracts and drug release. Suitability begins with whether the target remains stable in the chosen liquid, can be separated under useful conditions and gives a measurable detector response.

## Turning a molecular preference into minutes of separation

The moving liquid is the mobile phase. The environment retained within the column is the stationary phase, which may include chemical groups on particles or a retained liquid-like environment. Molecules move forward readily while carried by the mobile phase and advance more slowly on average while associated with the stationary phase. Repeated exchange along the column accumulates small differences into measurable time differences. The important question is how the two environments treat different molecules. An ordinary reversed-phase column is therefore not simply a filter that sorts everything by molecular size.

This repeated-distribution idea also illuminates the history. In his 1952 Nobel lecture, Archer Martin described partition chromatography as a connection between chromatography and countercurrent extraction. Martin and Richard Synge developed separation methods in a setting where understanding protein composition required distinguishable components from complex mixtures. The original column illustration shows two bands separating as differences accumulate. Modern pumps, refined packing and continuous detection make this process more reproducible and measurable. The scientific need encouraged a separation method, and improved separation enabled more demanding biochemical questions.

Common reversed-phase methods use relatively hydrophobic stationary surfaces, such as C18 groups, with mobile phases containing water and a miscible organic solvent. Many hydrophobic compounds remain longer under these conditions; increasing organic solvent often helps elute them. These comparisons apply within specified conditions. Charge, hydrogen bonding, aromatic interactions and details of the surface all influence retention, and two columns labeled C18 can have different selectivities. Very polar compounds, charged molecules and macromolecules may benefit from other mechanisms, including hydrophilic interaction, ion exchange or size exclusion.

Charge state deserves an early explanation. Some molecules accept or release protons, so pH changes the proportions of charged and neutral forms. Those forms interact differently with water and the stationary surface, changing retention. A buffer helps maintain the desired acidity, while its concentration and ion identity can also influence separation. Conditions must suit the analyte, the column and the detector. For example, nonvolatile salts have different practical consequences when the column is connected to mass spectrometry than when the detector simply measures ultraviolet absorbance.

![Original partition and flow-path diagrams. Two bands represent different average retention, illustrating the idea behind Martin and Synge’s partition chromatography. The right panel places pumping, injection, separation and detection in flow order; dimensions are schematic.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9177064aa8cf9073e3111225.svg?v=9177064aa8cf)

Figure 1Original partition and flow-path diagrams. Two bands represent different average retention, illustrating the idea behind Martin and Synge’s partition chromatography. The right panel places pumping, injection, separation and detection in flow order; dimensions are schematic.

Follow a modern instrument in the direction of flow. Solvents are degassed, mixed and pumped; an injection system introduces a defined sample volume; the column separates; a detector measures the effluent before it reaches collection or waste. Pressure drives liquid through a bed of fine particles, but pressure itself does not identify compounds. Smaller particles can shorten some transport paths while increasing resistance to flow. Understanding these distinct functions prevents a common misconception: a higher-pressure instrument does not automatically separate two molecules with nearly identical interactions.

## Peak width matters as much as arrival time

Retention time runs from injection to the target peak maximum. It includes transit with the mobile phase and the additional delay caused by retention. A suitably detectable marker that is essentially unretained under the selected conditions can estimate the hold-up time, t₀. Subtracting t₀ from retention time and dividing by t₀ gives the retention factor, k. This separates ordinary passage time from additional retention. The marker and measurement geometry must suit the column-volume question; the first small feature in a chromatogram is not automatically a trustworthy hold-up marker.

$$
k=\frac{t_R-t_0}{t_0},\qquad t_R=t_0(1+k)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Retention factor under isocratic conditions, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0dfa193aee7778fd0c1a71af.svg) | Target retention time, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/a15f4e949d9181049b209fc5.svg) | Hold-up time from an appropriate unretained marker, min. |

Normalize additional retention by unretained transit. tR=4 min and t₀=1 min give k=3. Changing gradient composition requires more than a single constant k.

If t₀ is 1 min and a compound arrives at 4 min, its retention factor is 3. Total passage takes four times the unretained transit time, with three times that interval added through retention. A second compound with k=3.36 arrives at 4.36 min. The ratio of the larger to smaller retention factor is 1.12, called the selectivity for this pair. Selectivity expresses how differently the phases treat the compounds. If their retention factors are equal, making both wait longer does not create a difference between their mean arrival times. A change in discriminating interactions is needed.

Molecules of one compound arrive over a range of times because they experience different flow paths, diffusion and exchange histories. Two peak centers separated by 0.3 min can be easy to distinguish when peaks are narrow, but strongly overlap when both are broad. Resolution compares the center separation with their widths. State whether widths are measured at the baseline or at half maximum, because the corresponding formula coefficients differ. A numerical resolution value is meaningful only with a defined width convention.

$$
R_s=\frac{2(t_{R,2}-t_{R,1})}{w_1+w_2},\qquad \alpha=\frac{k_2}{k_1}\quad(k_2\geq k_1>0)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c29ea71c312c1c2bf08acd27.svg) | Resolution of the two peaks, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/43bdb088cbae6d3907fc9e8b.svg) | Earlier and later retention times, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/8959dc68ce37371df41f244e.svg) | Baseline peak widths, min; 4σ in the Gaussian model here. |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | Selectivity, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/d62ad609310d0b90a08f3cae.svg) | Isocratic retention factors of the two compounds, dimensionless. |

Center separation relative to mean baseline width quantifies separation. Times 4 and 4.36 min and widths 0.32 and 0.3488 min give Rs≈1.07656. k values 3 and 3.36 give α=1.12. Tailing or unequal areas require inspection of the relevant integration interference.

The theoretical plate number, N, describes relative peak narrowness. It does not count physical shelves inside the column. For an approximately Gaussian peak, dividing retention time by its time standard deviation and squaring gives N. The standard deviation describes the spread of arrival times around their mean. If retention time stays fixed while width is halved, N increases fourfold. Under otherwise matched conditions, resolution then increases approximately twofold. Improving efficiency helps, but it acts differently from changing chemical selectivity.

$$
N=\left(\frac{t_R}{\sigma_t}\right)^2=16\left(\frac{t_R}{w}\right)^2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Theoretical plate count, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0dfa193aee7778fd0c1a71af.svg) | Retention time, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/87de164e10556b3dda44460d.svg) | Standard deviation of Gaussian arrival-time distribution, min. |
| ![Formula](https://ml-biomat.com/static/agent-math/5f85a26e5089def254fee2b9.svg) | Gaussian baseline width, taken as 4σt, min. |

For an approximately Gaussian peak under suitable isocratic conditions, relative width describes efficiency. tR=4 min and σt=0.08 min give N=2500; halving width at fixed retention gives N=10000. Extra-column dispersion also contributes to observed width.

![Constructed isocratic Gaussian peaks have unit area, t₀=1 min and k₁=3. A versus B changes only N; A versus C changes only selectivity. Resolution uses baseline widths of 4σ; the heatmap contour marks Rs=1.5.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/2f78881c5e500308f7f0648d.svg?v=2f78881c5e50)

Figure 2Constructed isocratic Gaussian peaks have unit area, t₀=1 min and k₁=3. A versus B changes only N; A versus C changes only selectivity. Resolution uses baseline widths of 4σ; the heatmap contour marks Rs=1.5.

The three chromatograms compare these routes. Initial conditions use N=2500 and selectivity 1.12. Increasing N to 10000 leaves centers unchanged but narrows the peaks. Keeping N=2500 while increasing selectivity to 1.30 moves the centers apart. The heatmap extends these combinations across a continuous range, with a white contour at model resolution 1.5. For similar-area, nearly symmetric Gaussian peaks, that is associated with good separation. A much smaller peak next to a large one, or a strongly tailing peak, calls for direct inspection of the interference relevant to its integration.

Flow also influences width. At slow flow, molecules have more time to diffuse along the column; at fast flow, exchange between environments may lag behind the moving liquid. Differences in paths contribute as well. These effects create a useful range of flow conditions. Doubling flow commonly shortens retention times, but also changes pressure, dispersion and detector sampling, so resolution need not improve. The interactive experiment first isolates efficiency and selectivity. Method development then connects those concepts to column length, particles, solvent, pH and temperature.

## Narrow the peaks or move them apart

Hold the first retention factor at 3 and compare efficiency, selectivity and time scale. Hold-up time only rescales this model; it does not predict how real flow affects efficiency.

[Figure: Interactive two-component chromatogram](https://ml-biomat.com/tutorials/experimental-methods/c01/en/#C01-plot)

## Introducing the specimen in a suitable state

The chromatogram begins at injection, but the quantitative story starts earlier. Sampling uniformity, complete dissolution, adsorption to containers or filters, and decomposition during storage all affect how much target reaches the instrument. Turbid specimens generally need appropriate clarification to keep particles out of narrow flow paths. Centrifugation, filtration and extraction must also suit the analyte. A hydrophobic molecule may be retained by a filter, while a drug can be lost with precipitated protein. Preparation should protect the separation system and bring the target into a solution whose history can be followed.

Sample solvent can alter the chromatogram. A large injection dissolved in a strong reversed-phase eluent may begin moving before the analyte focuses into a narrow band at the column head. Broadening, splitting or fronting can follow. Raising concentration while keeping injection volume small is therefore not always equivalent to injecting a large volume of dilute solution. Excess sample mass can also exceed the linear capacity of the stationary phase, changing retention and shape with concentration. Comparing several injection amounts helps establish whether position, shape and area behave as expected.

Isocratic elution keeps mobile-phase composition constant during a run. It suits mixtures with a manageable retention range and supports the simple k and N relationships used here. Gradient elution changes composition with time, often increasing organic solvent in reversed-phase work to release strongly retained components. The retention behavior of a molecule then changes during its passage, so the run is not equivalent to an isocratic experiment with one fixed k. After the gradient, the column must return to and equilibrate at its initial conditions before the next comparable injection.

A changed pump composition does not instantly reach the column. Mixer, tubing and injection-system volume must first be traversed. With a gradient delay volume of 0.75 mL and flow of 0.50 mL/min, the delay is 1.5 min. Two instruments running the same programmed gradient can consequently deliver different composition histories at their column entrances. Method transfer should compare actual gradient arrival and system volume. The figure shows two curves with the same slope but different arrival times, distinguishing this system effect from separation within the column.

The detector must respond appropriately to the analyte. Ultraviolet detection suits compounds absorbing at the selected wavelength; a diode-array detector records a range of wavelengths. Fluorescence detection suits intrinsically fluorescent or suitably labeled targets. Refractive-index and other detectors can help with compounds lacking strong ultraviolet absorption, but have their own mobile-phase requirements. Mass spectrometry adds mass and fragmentation information. Choosing a convenient wavelength is only one decision: solvent background, analyte response, neighboring components and the working concentration together determine whether detection is adequate.

Sampling speed also matters for narrow peaks. If the detector records too few points while a component passes, a peak may look angular and its measured height or area may depend on timing. Extra tubing and a large detector cell can broaden a band after it has left an efficient column. A short, fast separation therefore requires the whole flow path and detector configuration to preserve the resolution achieved inside the column. This explains why transferring a method involves more than copying the column name and solvent ratio.

## From one peak to the amount in the original specimen

Measure an authentic standard under matched conditions to compare retention time. Adding a small amount of the standard to the sample and observing the corresponding increase can further help locate the target. Different compounds can coelute, producing one visually tidy peak. Comparing spectra across the front, apex and tail, changing separation conditions or adding mass-spectral information provides additional evidence. Retention time is a condition-dependent identity clue, and coordinated observations strengthen the assignment.

Area measurement begins with the baseline, the signal expected when the target is absent. A slowly varying background can be estimated from nearby intervals free of other components, then subtracted before integration. A narrow window loses the peak wings; an excessively wide window can include neighboring components and baseline error. The window experiment demonstrates that enclosing the tallest part still misses considerable area. Tailing and overlapping peaks require a defined integration rule applied consistently and checked across the intended concentration range.

External calibration measures known concentrations of the same analyte with matched injection and detection conditions. The example uses six concentrations with three constructed repeats per level and fits a straight line. Its slope gives the mean area increase per concentration unit; its intercept represents the near-zero offset. Blank behavior, residuals and error structure guide whether to retain an intercept or use weighting. Forcing a line through zero simply because that looks convenient can change an unknown result. Samples should fall within the verified calibration range, with accurate dilution used when necessary.

$$
A=mc+b,\qquad c_{\mathrm{original}}=D\frac{A_{\mathrm{unknown}}-b}{m}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/88c650b4e9eb956a41e222a9.svg) | Target peak area for calibration or unknown, mAU min. |
| ![Formula](https://ml-biomat.com/static/agent-math/528857d51fe0ca9fb1f0a19e.svg) | Calibration slope, (mAU min)/(micrograms/mL). |
| ![Formula](https://ml-biomat.com/static/agent-math/b332ba26d1b8a3e4b8f817ed.svg) | Analyte concentration in the injected vial, micrograms/mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/a77a353782459b753313d802.svg) | Calibration intercept, mAU min. |
| ![Formula](https://ml-biomat.com/static/agent-math/5914524b1d3db63c66998b75.svg) | Total dilution factor from original solution to injected vial, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/994c7009d659d06ee37650ec.svg) | Original solution concentration, micrograms/mL. |

Invert the response within a verified linear range, then apply dilution. m=6, b=0.8, A=78.8 and D=4 give 13 micrograms/mL in the vial and 52 micrograms/mL originally. The program computes nearby results from noisy calibration and integration.

![Constructed quantitative experiment with a fixed seed. The true unknown concentration is 13 micrograms/mL; calibration uses three repeats per level. Shading marks the target integration interval. Residuals are measured calibration areas minus fitted areas. The final panel varies the integration window to show the contribution of peak wings.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d06234bc7b39e67a85b99ad8.svg?v=d06234bc7b39)

Figure 3Constructed quantitative experiment with a fixed seed. The true unknown concentration is 13 micrograms/mL; calibration uses three repeats per level. Shading marks the target integration interval. Residuals are measured calibration areas minus fitted areas. The final panel varies the integration window to show the contribution of peak wings.

The teaching relationship is approximately area equals six times concentration plus 0.8. Concentration is in micrograms per milliliter, and area is in mAU min, where mAU means one thousandth of an absorbance unit. The constructed unknown contains 13 micrograms per milliliter; integration and calibration recover a nearby value. If that solution came from a fourfold dilution, the original concentration is approximately 52 micrograms per milliliter. Fourfold means final volume divided by the volume of original solution taken, not added-solvent volume divided by original volume. Recording aliquots, final volumes and subsequent dilutions keeps the conversion connected to the specimen.

Reporting content within a material requires further accounting. Multiply extract concentration by total extract volume, then divide by extracted material mass. An original extract at 52 micrograms per milliliter in 10 mL contains 520 micrograms. If it came from 0.20 g of material, the content is 2600 micrograms per gram, or 2.6 milligrams per gram. Units cancel or remain in meaningful ways at each step, making dimensional checks part of the reasoning. A peak representing 90% of total detector area is a detector-area fraction; compounds with unequal responses prevent automatic interpretation as 90% mass purity.

Internal calibration adds a known amount of another suitable compound to standards and samples and uses the ratio of analyte to internal-standard areas. A globally larger or smaller injection changes both signals, so their ratio reduces that source of variation. The internal standard should be stable, absent from the specimen or distinguishable, and separated from target and matrix peaks. Tracking extraction loss additionally requires adding it before the relevant preparation step and demonstrating comparable recovery behavior. Adding it after extraction helps only with subsequent steps. A spike-recovery experiment adds the analyte itself to investigate measured recovery; it answers a different question.

## What should accompany a convincing calibration line?

A straight calibration line indicates that the selected model describes the measured standards over that range. Extraction loss, coelution and degradation while samples wait for injection require additional observations. Place checks where the relevant errors arise: solvent blanks examine system background, preparation blanks examine reagents and containers, blanks after concentrated samples examine carryover, and independently prepared check samples evaluate measurement after calibration. These controls have distinct purposes and make a changed result easier to diagnose.

Recovery provides an intuitive preparation check. Compare two equivalent specimens, adding a known amount of analyte to one before extraction. Subtract the unspiked result from the spiked result and divide by the added amount. If a 10 microgram addition produces an 8.5 microgram increase, the recovery is 85%. This characterizes how much of the added analyte becomes measurable under the tested concentration, matrix and processing conditions. Repeating the comparison after changing a container, extraction condition or filter turns an observed loss into an experimentally addressable step.

$$
\mathrm{Recovery}=\frac{q_{\mathrm{spiked}}-q_{\mathrm{unspiked}}}{q_{\mathrm{added}}}\times100\%
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/da2911810e849da2f484a127.svg) | Spike recovery percentage, %. |
| ![Formula](https://ml-biomat.com/static/agent-math/340607043a312e60188e2839.svg) | Measured analyte amount in the spiked specimen, micrograms. |
| ![Formula](https://ml-biomat.com/static/agent-math/17a361682607930130ab2ca5.svg) | Measured amount in the corresponding unspiked specimen, micrograms. |
| ![Formula](https://ml-biomat.com/static/agent-math/2ed64c2d28a6fe11e9f25433.svg) | Known amount added before the relevant processing step, micrograms. |

Subtract the original contribution and compare the increment with the added amount. An 8.5 microgram increase from a 10 microgram spike gives 85%. Specimens and final volumes must be comparable, with spike timing defined.

Precision and recovery answer related but different questions. Three values close to 85% describe a relatively stable loss; values of 60%, 85% and 105% point to variation or interference. A stable bias and a variable process affect research differently. Analyte originally embedded in a complex material may not behave exactly like a freely added spike. Different addition times, repeated extraction or suitable reference materials can bring validation closer to the behavior of the original specimen. A correction becomes useful when its physical basis matches the preparation being corrected.

The calibration residual plot preserves each repeat's deviation from the fitted line. Residuals on one side at low concentration and the other at high concentration can reveal an unsuitable linear range or model. Increasing error with concentration motivates examination of weighting. For a real sample sequence, retention time, check-sample concentration and pressure plotted against injection order can reveal trends or abrupt changes. Such plots help distinguish gradual column changes, solvent problems and isolated injection events.

Replicate structure should also match the claim. Reinjecting one vial measures injection and short-term instrument variation. Preparing several aliquots examines preparation variation. Sampling independent specimens addresses variation in the material or biological process. Keeping those levels separate helps explain whether a small difference between formulations reflects repeatable material behavior or simply a repeatable measurement on one prepared solution. The useful outcome is an uncertainty statement tied to the actual experimental unit.

Before an analytical sequence, a standard mixture can test whether the system still separates the important pair, gives the expected retention behavior and produces repeatable areas. Define those checks around the task. A method for a trace impurity beside a dominant main component places different demands on separation from a method measuring two similarly abundant compounds. If the check changes, examine solvent preparation, leaks, temperature, column condition and injection settings in a controlled order. Changing several settings at once can produce a better-looking chromatogram while obscuring the reason for improvement. A short sequence containing a blank, standards, a check sample, unknowns and periodic checks turns the run into a coherent comparison rather than a collection of unrelated traces.

### Complete separation, integration, calibration and sampling mass balance

A fixed seed generates labeled teaching data and saves all figures, calibration repeats, the unknown chromatogram and release-sampling table.

```
"""Reproducible constructed HPLC separation, calibration and sampling examples."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,FancyArrowPatch

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True);zh=a.language=='zh';T=lambda z,e:z if zh else e
 plt.rcParams.update({'font.family':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','text.color':'#243c49','axes.labelcolor':'#243c49','axes.edgecolor':'#8ea1a8','figure.facecolor':'#fbfaf6','axes.facecolor':'#fbfaf6','svg.fonttype':'path'})
 blue,green,red,gold='#286488','#008b7b','#dc604d','#c39227';rng=np.random.default_rng(610)
 def save(fig,n):
  fig.tight_layout(pad=1.6)
  for ext in ['svg','png']:fig.savefig(out/f'{n}-{a.language}.{ext}',dpi=155,bbox_inches='tight')
  plt.close(fig)
 def g(t,mu,s):return np.exp(-.5*((t-mu)/s)**2)/(s*np.sqrt(2*np.pi))
 fig,ax=plt.subplots(1,2,figsize=(13,5),gridspec_kw={'width_ratios':[1,1.55]});x=ax[0];x.set(xlim=(0,10),ylim=(0,10));x.axis('off')
 x.add_patch(Rectangle((3,1.1),3,7.7,fill=False,lw=2,color=blue))
 for yy in np.arange(1.6,8.6,.55):
  for xx in [3.45,4.25,5.05,5.65]:x.add_patch(Circle((xx,yy),.13,color='#b9c9cb'))
 for yy,c,label in [(6.5,gold,T('停留较久','More retained')),(3.1,green,T('前进较快','Faster migration'))]:x.add_patch(Rectangle((3.1,yy),2.8,.55,color=c,alpha=.65));x.text(6.4,yy+.27,label,va='center',fontsize=10)
 x.annotate('',xy=(4.5,9),xytext=(4.5,10),arrowprops={'arrowstyle':'->','color':blue,'lw':2});x.annotate('',xy=(4.5,.15),xytext=(4.5,1),arrowprops={'arrowstyle':'->','color':blue,'lw':2});x.text(.1,.15,T('流动相不断向下移动','Mobile phase keeps moving'),fontsize=10);x.set_title(T('A  分配差异累积为分离','A  Repeated partition creates separation'),loc='left')
 x=ax[1];x.set(xlim=(0,14),ylim=(0,10));x.axis('off');items=[(.3,6.5,2,1.4,T('溶剂瓶','Solvents')), (3.3,6.5,2,1.4,T('泵与混合','Pump / mix')), (6.3,6.5,2,1.4,T('定量进样','Injection')), (6.3,2.8,2,1.4,T('色谱柱','Column')), (10,2.8,2.7,1.4,T('检测器','Detector'))]
 for xx,yy,w,h,label in items:x.add_patch(Rectangle((xx,yy),w,h,facecolor='#e6eeee',edgecolor=blue,lw=1.7));x.text(xx+w/2,yy+h/2,label,ha='center',va='center')
 for start,end in [((2.3,7.2),(3.3,7.2)),((5.3,7.2),(6.3,7.2)),((7.3,6.5),(7.3,4.2)),((8.3,3.5),(10,3.5)),((12.7,3.5),(13.7,3.5))]:x.add_patch(FancyArrowPatch(start,end,arrowstyle='->',mutation_scale=14,color=green,lw=2))
 x.text(10,1.2,T('固定波长下的信号随时间记录','Signal recorded over time at a fixed wavelength'),fontsize=10,ha='center');x.text(1,2.2,T('分离发生在柱内\n检测发生在出口','Separation inside the column\nDetection after the column'),fontsize=12,color=green);x.set_title(T('B  用稳定流动读取时间顺序','B  Controlled flow reveals elution order'),loc='left');save(fig,'instrument')

 t=np.linspace(0,10,4001);t0=1.;k1=3.;alpha=1.12;N=2500.
 def peaks(N,alpha):
  tr=np.array([t0*(1+k1),t0*(1+alpha*k1)]);s=tr/np.sqrt(N);ys=np.array([g(t,m,w) for m,w in zip(tr,s)]);rs=(tr[1]-tr[0])/(2*sum(s));return tr,s,ys,rs
 fig,ax=plt.subplots(2,2,figsize=(12,7.6));records=[]
 for axis,(n,al,label) in zip(ax.flat[:3],[(2500,1.12,T('A  原条件','A  Initial conditions')),(10000,1.12,T('B  柱效提高四倍','B  Fourfold plate count')),(2500,1.30,T('C  改变选择性','C  Change selectivity'))]):
  tr,s,y,rs=peaks(n,al);axis.plot(t,y.sum(axis=0),color=blue,lw=2);axis.fill_between(t,0,y[0],alpha=.2,color=green);axis.fill_between(t,0,y[1],alpha=.2,color=gold);axis.set(xlim=(3.4,5.6),xlabel=T('时间 / min','Time / min'),ylabel=T('归一化信号 / 每 min','Normalized signal / per min'));axis.set_title(label+f' · Rs={rs:.2f}',loc='left');records.append([n,al,*tr,*s,rs])
 ns=np.linspace(1000,12000,100);als=np.linspace(1.01,1.4,100);nn,aa=np.meshgrid(ns,als);rsgrid=3*(aa-1)*np.sqrt(nn)/(2*(4+1+3*aa));im=ax[1,1].pcolormesh(ns,als,rsgrid,shading='auto',cmap='viridis');ax[1,1].contour(ns,als,rsgrid,levels=[1.5],colors=['white'],linewidths=1.5);ax[1,1].set(xlabel=T('理论塔板数 N','Theoretical plates N'),ylabel=T('选择性 α','Selectivity α'));ax[1,1].set_title(T('D  两种改进各有作用','D  Two distinct routes to separation'),loc='left');fig.colorbar(im,ax=ax[1,1],label='Rs');save(fig,'resolution');np.savetxt(out/'separation_cases.csv',records,delimiter=',',header='N,alpha,tR1_min,tR2_min,sigma1_min,sigma2_min,Rs',comments='')

 concentrations=np.repeat([0,2,5,10,20,40],3);calarea=6*concentrations+.8+rng.normal(0,.6,len(concentrations));slope,intercept=np.polyfit(concentrations,calarea,1)
 trace_t=np.linspace(4,7,1501);baseline=2+.3*(trace_t-4);truearea=6*13+.8;trace=baseline+truearea*g(trace_t,5.2,.12)+40*g(trace_t,6.25,.14)+rng.normal(0,.3,len(trace_t));baseline_mask=(trace_t<4.5)|(trace_t>6.85);bp=np.polyfit(trace_t[baseline_mask],trace[baseline_mask],1);estimated_base=np.polyval(bp,trace_t);region=(trace_t>=4.65)&(trace_t<=5.7);area=np.trapezoid((trace-estimated_base)[region],trace_t[region]);conc=(area-intercept)/slope;stock=conc*4
 fig,ax=plt.subplots(2,2,figsize=(12,7.5));ax[0,0].plot(trace_t,trace,color=blue,label=T('进样信号','Injected signal'));ax[0,0].plot(trace_t,estimated_base,color=gold,label=T('估计基线','Estimated baseline'));ax[0,0].fill_between(trace_t[region],estimated_base[region],trace[region],alpha=.25,color=green);ax[0,0].set(xlabel=T('时间 / min','Time / min'),ylabel='mAU');ax[0,0].legend(fontsize=9);ax[0,0].set_title(T('A  面积包括整个目标峰','A  Integrate the target peak'),loc='left')
 ax[0,1].scatter(concentrations,calarea,color=blue,s=22);xx=np.linspace(0,42,100);ax[0,1].plot(xx,slope*xx+intercept,color=green);ax[0,1].scatter([conc],[area],color=red,marker='D',s=55,label=T('未知样','Unknown'));ax[0,1].legend();ax[0,1].set(xlabel=T('浓度 / μg mL⁻¹','Concentration / micrograms per mL'),ylabel=T('峰面积 / mAU·min','Peak area / mAU min'));ax[0,1].set_title(T('B  同一目标物的校准','B  Analyte-specific calibration'),loc='left')
 ax[1,0].axhline(0,color='#8da0a8');ax[1,0].scatter(concentrations,calarea-(slope*concentrations+intercept),color=blue,s=25);ax[1,0].set(xlabel=T('浓度 / μg mL⁻¹','Concentration / micrograms per mL'),ylabel=T('面积残差 / mAU·min','Area residual / mAU min'));ax[1,0].set_title(T('C  校准残差保留误差信息','C  Calibration residuals reveal error'),loc='left')
 windows=[.12,.24,.36,.48,.6];captured=[]
 for half in windows:
  sel=np.abs(trace_t-5.2)<=half;captured.append(np.trapezoid((trace-estimated_base)[sel],trace_t[sel])/truearea*100)
 ax[1,1].plot(windows,captured,'o-',color=green);ax[1,1].axhline(100,color='#8da0a8',ls=':');ax[1,1].set(xlabel=T('积分窗口半宽 / min','Integration half-width / min'),ylabel=T('目标面积回收 / %','Target area recovered / %'),ylim=(60,105));ax[1,1].set_title(T('D  太窄的窗口遗漏峰翼','D  Narrow windows lose peak tails'),loc='left');save(fig,'quantification')
 np.savetxt(out/'calibration.csv',np.c_[concentrations,calarea,calarea-(slope*concentrations+intercept)],delimiter=',',header='concentration_ug_per_mL,area_mAU_min,residual_mAU_min',comments='');np.savetxt(out/'unknown_chromatogram.csv',np.c_[trace_t,trace,estimated_base],delimiter=',',header='time_min,signal_mAU,estimated_baseline_mAU',comments='')

 fig,ax=plt.subplots(1,3,figsize=(14,4.7));tt=np.linspace(0,16,500);program=np.clip(10+8*tt,10,90);arrival=np.clip(10+8*(tt-1.5),10,90);ax[0].plot(tt,program,color=blue,label=T('泵设定','Pump program'));ax[0].plot(tt,arrival,color=green,label=T('到达柱入口','At column inlet'));ax[0].set(xlabel=T('时间 / min','Time / min'),ylabel=T('有机相 B / %','Organic B / %'));ax[0].legend(fontsize=9);ax[0].set_title(T('A  梯度有到达延迟','A  Gradients have a delay'),loc='left')
 spikes=[0,5,10,20];recovered=np.array(spikes)*.85;ax[1].plot(spikes,spikes,ls=':',color='#8da0a8',label='100%');ax[1].plot(spikes,recovered,'o-',color=green,label='85%');ax[1].set(xlabel=T('提取前加入 / μg','Spike before extraction / micrograms'),ylabel=T('测得增加量 / μg','Measured increase / micrograms'));ax[1].legend();ax[1].set_title(T('B  加标追踪样品回收','B  Spikes track recovery'),loc='left')
 c=np.array([2.,5.,8.]);V=10.;v=1.;cumulative=V*c+v*np.r_[0,np.cumsum(c[:-1])];ax[2].plot([1,2,3],V*c,'o-',color=gold,label=T('当前容器内','Currently in vessel'));ax[2].plot([1,2,3],cumulative,'o-',color=green,label=T('累计释放','Cumulative released'));ax[2].set(xlabel=T('取样序号','Sampling event'),ylabel=T('目标物质量 / μg','Analyte mass / micrograms'));ax[2].set_xticks([1,2,3]);ax[2].legend(fontsize=9);ax[2].set_title(T('C  已取走的质量也要算','C  Include previously removed mass'),loc='left');save(fig,'method-decisions');np.savetxt(out/'release_sampling.csv',np.c_[c,V*c,cumulative],delimiter=',',header='concentration_ug_per_mL,current_mass_ug,cumulative_mass_ug',comments='')
 _,_,_,rs=peaks(2500,1.12)
 summary={'retention_factor_example':3.,'initial_resolution':float(rs),'fourfold_N_resolution':float(peaks(10000,1.12)[3]),'changed_selectivity_resolution':float(peaks(2500,1.3)[3]),'calibration_slope':float(slope),'calibration_intercept':float(intercept),'unknown_area_mAU_min':float(area),'unknown_diluted_ug_per_mL':float(conc),'unknown_original_ug_per_mL':float(stock),'dwell_delay_min':.75/.5,'spike_recovery_fraction':.85,'cumulative_release_final_ug':float(cumulative[-1]),'constructed_data':True}
 (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
```

## When concentration becomes a materials result

Drug-release measurements show why a reliable concentration still needs an experiment-specific mass balance. Suppose a material sits in 10 mL of liquid. At each sampling time, 1 mL is removed for analysis and replaced with 1 mL of drug-free liquid. Before the third withdrawal, the mass remaining in the vessel is the current concentration multiplied by 10 mL. Drug removed during the first two withdrawals has already left the vessel and must be added back when calculating cumulative release. Ignoring it particularly underestimates experiments with early release or frequent sampling.

$$
M_n=Vc_n+v\sum_{i=1}^{n-1}c_i
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/4f3c9d3ab8208b50c9e81e73.svg) | Cumulative released mass before sampling event n, micrograms. |
| ![Formula](https://ml-biomat.com/static/agent-math/bef27a67f1f86637c8224c0d.svg) | Total vessel volume restored after each replacement, mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/31eea81269f83b010cbeea2c.svg) | Concentrations in the mixed liquid before the corresponding withdrawals, micrograms/mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | Fixed withdrawn volume at each event, mL. |
| ![Formula](https://ml-biomat.com/static/agent-math/532fd9de01c5518cbb6ef73b.svg) | Sampling indices, dimensionless; the sum covers earlier withdrawals only. |

Cumulative mass equals current vessel mass plus previously removed mass. V=10 mL, v=1 mL and c₁/c₂/c₃=2/5/8 micrograms/mL give M₃=80+2+5=87 micrograms. Assumes mixing, equal analyte-free replacement and appropriate treatment of degradation or other losses.

If the first three concentrations are 2, 5 and 8 micrograms per milliliter, the vessel contains 80 micrograms just before the third sample. Earlier withdrawals removed 2+5=7 micrograms, giving 87 micrograms cumulative release. The arithmetic assumes thorough mixing, known withdrawal volume, analyte-free replacement liquid, restoration of the 10 mL total volume and no substantial degradation or other consumption of the counted analyte. If degradation occurs, measuring the parent compound and degradation products can establish a fuller account of material fate.

![Three defined teaching calculations. Gradient delay is 0.75 mL / 0.50 mL/min=1.5 min; spike recovery is modeled at 85%; a 10 mL release vessel is sampled by 1 mL withdrawals with analyte-free replacement, giving 87 micrograms cumulative release before the third withdrawal.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/4f484d06cdaecffd647bc61e.svg?v=4f484d06cdae)

Figure 4Three defined teaching calculations. Gradient delay is 0.75 mL / 0.50 mL/min=1.5 min; spike recovery is modeled at 85%; a 10 mL release vessel is sampled by 1 mL withdrawals with analyte-free replacement, giving 87 micrograms cumulative release before the third withdrawal.

Extraction experiments similarly distinguish the amount released into a defined medium from the total amount originally present in the material. Temperature, medium, exposure duration, surface area and liquid volume affect the result. Comparing formulations requires matching these conditions to the same research question. Residual-monomer content calls for sufficiently complete extraction with appropriate recovery validation. Migration during use calls for a contact experiment representing that use. The same chromatographic signal can serve different questions, and the reported quantity should follow the experimental definition.

Analytical measurement and preparative collection use the same separation idea with different priorities. An analytical injection uses a small amount to estimate composition or concentration. A preparative run collects a useful quantity of the desired material, so loading capacity, collection boundaries, recovery and solvent removal become central. Collecting only the middle of a peak can improve purity while reducing recovered amount; collecting the full band may recover more material together with neighboring impurities. If the purpose is to purify a peptide or additive for later experiments, examine the collected fraction again under an appropriate analytical method and relate recovered mass to the amount initially loaded. The chromatogram then guides a physical separation rather than merely reporting a number.

The final description connects preparation, separation, detection wavelength, calibration range, integration and quality checks into a reproducible account. Retain raw chromatograms alongside processed area tables so each concentration has an inspectable basis. When improving the experiment, locate the issue before injection, during separation, at detection or in conversion back to the original specimen. HPLC earns its place by turning a complicated mixture into temporally distinguishable components and reconnecting those components to a defined chemical, biological or materials question.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/C01.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Martin: The development of partition chromatography](https://www.nobelprize.org/uploads/2018/06/martin-lecture.pdf)

   Original historical account connecting partition chromatography and countercurrent extraction.
2. [Thermo Fisher: HPLC basics](https://www.thermofisher.com/dk/en/home/industrial/chromatography/chromatography-learning-center/liquid-chromatography-information/hplc-basics.html?erpType=Global_E1)

   Flow components, phases and chromatographic recording.
3. [Agilent: Essentials of good HPLC method development](https://www.agilent.com/cs/library/slidepresentation/public/essentials_of_good_hplc_method_development_july_27_2022.pdf)

   Resolution, efficiency, selectivity, flow and gradient delay.
4. [Agilent: A guide to HPLC column selection](https://www.agilent.com/cs/library/eseminars/public/how-do-i-choose-a-guide-to-hplc-column-selection.pdf)

   Stationary-phase choices, particle size and system volume.
5. [JASCO: Qualitative and quantitative HPLC analysis](https://www.jasco-global.com/principle/principles-of-hplc-5-qualitative-and-quantitative-analysis/)

   Retention, spiking for assignment, external and internal calibration.
6. [Shimadzu: Quantitation error factors in sample preparation](https://www.shimadzu.com/an/service-support/technical-support/liquid-chromatography/essential_knowledge/error.html)

   Container adsorption, stability, extraction and recovery experiments.
