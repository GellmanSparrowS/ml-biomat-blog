# AFM: Touching a surface with a tiny probe

Source: https://ml-biomat.com/tutorials/experimental-methods/i05/en/
Language: en

Give probe shape, surface topography and small forces distinct physical meanings.

## Why might cells feel a difference between two smooth-looking surfaces?

Two transparent polymer films can look equally smooth to the eye while cells spread differently on them. Alongside chemical composition, small surface features, local stiffness and adsorbed molecules may contribute. An ordinary photograph cannot fully describe the depth of a nanoscale groove or the deformation of one small hydrogel region under gentle pressure. Atomic force microscopy, abbreviated AFM, places a tiny probe at the end of a flexible cantilever. Interactions between probe and surface bend that cantilever by a detectable amount. Scanning across the specimen produces a height map; approaching and withdrawing at a fixed location produces a force curve.

Running a finger over a tabletop can reveal particles and scratches that are hard to see. This is a useful introduction to AFM, including its complications. A finger has finite width, pushes into soft material and may miss small features when moved too quickly. An AFM probe likewise has a shape that influences lateral outlines, applies forces that can deform soft specimens, and relies on feedback to follow changing terrain. Once these relationships are understood, an AFM image becomes more than a colorful landscape: it is a set of height and force measurements connected to a probe, specimen and control conditions.

This chapter follows two paths. Surface imaging introduces nanoscale topography and roughness; force curves introduce local indentation and elastic modulus. Both use a cantilever but require different calibration and analysis. AFM can operate in suitable air or liquid environments, making specimen-state choices useful for protein films, cells, hydrogels and coatings. Decide first whether the target is dry morphology, hydrated height, or mechanical response on a particular timescale. Settings can then be organized around one research question rather than around whichever image mode happens to be available.

## From measuring current to measuring a tiny spring's bending

In 1986, Binnig, Quate and Gerber extended scanning-probe measurement from current to force with the atomic force microscope. Scanning tunneling microscopy uses the tunneling current between probe and surface and therefore requires suitable electrical conduction. AFM instead lets surface interactions bend a cantilever, making many nonconducting materials accessible. The original apparatus used a metal cantilever carrying a diamond tip and another tunneling probe to detect its displacement. This historical detail matters: the familiar laser readout was not the complete design of the first instrument. New measurement methods often begin by borrowing an existing technique to solve their hardest readout problem.

A common modern readout is the optical lever. A laser reflects from the cantilever's back onto a segmented photodetector. A slight bend changes the reflection angle and moves the spot at the detector. The instrument initially records a voltage related to spot position. A sensitivity calibration converts that voltage into cantilever displacement, and multiplying displacement by spring constant converts it into force. These are two separate conversions: how much displacement corresponds to a voltage change, and how much force corresponds to that displacement? Keeping them distinct prevents an uncalibrated voltage trace from being treated as an already quantitative force curve.

$$
d=S\Delta V,\qquad F=kd
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d47d91d61053a3c786f20a4b.svg) | Cantilever end deflection, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/4d93e1f4798eafa4154488df.svg) | Inverse optical-lever sensitivity, m/V; 50 nm/V here. |
| ![Formula](https://ml-biomat.com/static/agent-math/d734398b2cf2660032fdbf86.svg) | Baseline-corrected detector voltage change, V. |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | Force associated with elastic cantilever bending, N. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Calibrated cantilever spring constant, N/m. |

Convert voltage to displacement using sensitivity, then use the linear spring relation. 50 nm/V×0.10 V=5 nm; 0.20 N/m×5×10⁻⁹ m=10⁻⁹ N=1 nN. Signs follow the measurement convention; this example compares magnitudes.

For example, an optical sensitivity of 50 nm/V converts a baseline-corrected signal of 0.10 V into 5 nm of cantilever displacement. With a spring constant of 0.20 N/m, the corresponding force is 1.0 nN. This sensitivity is defined as displacement divided by voltage; some software instead reports its reciprocal in V/nm. Writing units at each multiplication immediately reveals whether an inversion is required. Contact against a sufficiently stiff reference can help calibrate optical sensitivity because much of the postcontact motion appears as cantilever bending. Probe geometry, contact stability and the assumptions of the calibration procedure still need attention.

Spring constants can be established through thermal-noise methods, reference cantilevers or other validated procedures. Thermal calibration uses the relationship between thermal motion and stiffness, with analysis accounting for vibration modes, detection bandwidth and readout. The useful principle is the physical correspondence being established rather than one instrument's menu sequence. After replacing a cantilever, moving the laser spot or changing the medium, check which calibration quantities have changed. The resulting force curve then has a traceable path from detector signal to physical units, and changes between experiments can be interpreted at the correct stage of that path.

![Original AFM readout schematic. Left: diamond probe, metal cantilever and tunneling readout associated with the 1986 apparatus. Right: a common optical lever and feedback concept. Gaps are enlarged for explanation; not to scale.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d3098db6332e9b530bd4670c.svg?v=d3098db6332e)

Figure 1Original AFM readout schematic. Left: diamond probe, metal cantilever and tunneling readout associated with the 1986 apparatus. Right: a common optical lever and feedback concept. Gaps are enlarged for explanation; not to scale.

The spring constant describes resistance to bending, in N/m. A softer cantilever bends farther under the same force and can be useful for detecting small interactions. A stiffer cantilever accommodates larger forces, while a very small force produces a smaller displacement. Selection also involves thermal noise, liquid damping, resonance frequency and measurement speed. Biological specimens often require a balance between gentle contact and stable readout; hard coatings may require another range. Nominal manufacturer values help select probes, but quantitative force work requires an appropriate calibration of the actual cantilever and measurement environment.

A piezoelectric scanner converts voltage changes into small position changes, moving either probe or specimen laterally and vertically. During imaging, feedback compares the measured interaction with its target and adjusts vertical position. Recording the motion required to maintain that target produces a topographic map. The idea resembles continually adjusting height while following a winding mountain road. If feedback responds too slowly, a sharp edge may leave a trailing error; overly aggressive control can oscillate. Inspecting height together with the error channel therefore reveals tracking quality more clearly than viewing the colored height map alone.

## The scanning mode determines how the probe encounters the specimen

Contact mode maintains close or continuous interaction with the surface, commonly using cantilever deflection as the controlled quantity. Its principle is direct and useful for many stable surfaces. Lateral dragging, however, generates friction that can displace weakly adsorbed molecules or deform soft structures. Dynamic modes oscillate the cantilever and use changes in amplitude, frequency or phase for control. Intermittent-contact operation, often called tapping, reduces continuous lateral dragging, but interaction strength still depends on amplitude, setpoint, probe and medium. Mode names classify operation; the actual interaction conditions determine what the specimen experiences.

For an adsorbed protein film, the substrate should be stable and the immobilization route should preserve the structure being studied. Drying in air can shrink a film, whereas liquid observation introduces buffer composition, temperature, drift and probe motion in fluid. A hydrogel may also continue swelling after a solution change, making equilibration relevant to both height and mechanical measurements. Interpreting time-dependent changes at one location as a material response requires separating them from scanner drift and probe-induced motion. Environmental conditions are part of the specimen state, not simply background information appended after analysis.

Choose scan range, pixel count and speed together. Sampling a 1 μm field at 512 positions gives a lateral interval of roughly 2 nm. A 2 nm sampling interval does not establish 2 nm lateral resolution because probe shape and tracking also limit visible detail. A wider field describes distribution and representativeness, while a smaller field reveals local geometry. Start with a stable overview and select smaller regions for an explicit reason. When comparing specimens, retain comparable scan scales and processing rules; otherwise a roughness difference may combine material variation with a change in the spatial scales sampled.

Forward and reverse scans provide a useful internal comparison. Real topography tracked consistently should produce compatible structures after appropriate registration. A trailing edge that reverses direction with the scan suggests checking feedback, speed and probe condition. An abrupt horizontal jump can arise from temporary loss of tracking, contamination pickup or a line offset. Repeated copies of the same shape across unrelated objects may indicate a double or contaminated tip. Rotating scan direction, slowing the scan and examining a reference surface help distinguish specimen features from the instrument's path and probe geometry.

## A probe has width, so a measured hill can become wider

A tip is not a dimensionless mathematical point. As it moves beside a small raised feature, its side can contact the feature before the apex reaches the feature's center. The probe must already rise, broadening the recorded lateral outline. This is often called tip convolution, although geometrically it is closer to morphological dilation: among possible contacts, the probe must reach a height that prevents intersection with the surface. That operation differs from the averaging associated with ordinary optical blur. Understanding the distinction explains why applying a simple smoothing filter cannot automatically reconstruct a particle's true shape.

The teaching model isolates this geometry with a rectangular feature 10 nm high and 20 nm wide, scanned by a probe with a parabolic cross-section. Increasing the curvature parameter R makes the probe blunter and extends the apparent edges farther to each side. In this rigid geometrical model, the top height remains unchanged. At half the feature height, R=20 nm gives a measured width of approximately 48.28 nm, substantially wider than the true 20 nm. This explains why nanoparticle lateral dimensions often require attention to probe shape, while vertical height can under suitable conditions remain closer to the object's actual vertical extent.

$$
w_{1/2}=w+2\sqrt{RH}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/facda8feca2f934f536e87e0.svg) | Measured profile width at half the step height, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/5f85a26e5089def254fee2b9.svg) | True width of the ideal rectangular feature, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Apex curvature-radius parameter of the parabolic probe, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/6d6950da29507eb4f6b78d53.svg) | Step height, nm. |

For the parabolic probe, height at lateral offset s is s²/(2R). At half height, s²/(2R)=H/2, hence s=√(RH). Add both sides to obtain the width. With w=20, R=20 and H=10 nm, the apparent half-height width is 48.284 nm. The model assumes rigid geometry, no adhesion and perfect tracking.

![Constructed teaching surface. A changes parabolic probe curvature over the same rectangular feature. B and C show tilted and plane-levelled heights, each with its stated color scale. D compares the same profile and Sq before and after processing.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/9538d57069fec219d47eea08.svg?v=9538d57069fe)

Figure 2Constructed teaching surface. A changes parabolic probe curvature over the same rectangular feature. B and C show tilted and plane-levelled heights, each with its stated color scale. D compares the same profile and Sq before and after processing.

Height is also influenced by physical interactions. A soft particle pressed flatter becomes shorter; a polymer brush or adsorbed layer may be penetrated to different depths at different forces. A narrow pit may prevent the tip from reaching its bottom, making it appear too shallow. Height therefore needs its own checks. Vary interaction conditions to test stability, and use reference specimens with known dimensions to examine scanner and probe performance. Where lateral geometry is central, probe characterization, shape reconstruction and comparison with other microscopy methods become valuable parts of the measurement.

The interactive experiment provides controls for probe curvature, feature height and true width. It shows both the true step and predicted measured outline, with the apparent width at half height. First keep height fixed and increase R to observe lateral expansion. Then hold R fixed and raise the step, watching the probe sides encounter it earlier. The model isolates geometry by omitting deformation, adhesion and tracking delay. Separating this geometrical contribution from the mechanical contribution developed later is an important step toward interpreting AFM images of soft materials.

## How much does a blunt probe broaden a step?

Geometrical model of a rigid rectangular feature and parabolic probe. Gray shows the true outline, green the predicted measurement; the dashed line marks half height.

[Figure: Probe-broadening model](https://ml-biomat.com/tutorials/experimental-methods/i05/en/#I05-plot)

## Roughness depends on the reference surface and spatial scale

An AFM height map is a numerical field. Color translates height into a visual representation, and different color ranges can make the same data appear dramatically different. Quantitative comparison requires height units, color limits, lateral scale and the leveling history. A slightly tilted specimen creates a gradual rise across the entire field. This slope increases height dispersion but may not be the roughness targeted by the experiment. The simplest plane-leveling operation fits a plane to the data and subtracts its height from each location. The reference surface is thereby made explicit.

The constructed surface in the figure contains two smooth periodic variations, with an added inclined plane. Raw height combines genuine structure and overall slope; leveling reveals the local variations more clearly. The operation is justified by known geometry rather than by a desire for a cleaner-looking picture. In an experimental specimen, long-wavelength variation may itself be meaningful structure. A high-degree polynomial or aggressive line-by-line correction can remove it. Large particles concentrated on one side can also bias a whole-image plane fit. Choose background regions or masks according to the question, and preserve before-and-after profiles to show what was removed.

$$
\bar z=\frac1N\sum_{i=1}^N z_i,\qquad S_q=\sqrt{\frac1N\sum_{i=1}^N(z_i-\bar z)^2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/51874f02b4c579417c89ce04.svg) | Height at sampled position i, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/33f73a318016d781b6ae1aa9.svg) | Sample index within the selected region; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | Number of valid sampled points in the region; dimensionless integer. |
| ![Formula](https://ml-biomat.com/static/agent-math/0c0542cabaa03a20baa1420d.svg) | Mean height of the selected region, nm. |
| ![Formula](https://ml-biomat.com/static/agent-math/d2cee8f616536ae9f81ee93c.svg) | Root-mean-square height variation relative to the region mean, nm. |

Average equally weighted, equal-area pixels. Heights −1, 1, −1 and 1 nm have zero mean and mean squared deviation 1 nm², giving Sq=1 nm. The denominator N defines an area statistic of the measured surface; leveling, masks and scan extent must be specified.

Root-mean-square roughness, Sq, subtracts the mean height from every value, squares the deviations, averages them and takes the square root. Squaring makes positive and negative deviations contribute positively and gives larger peaks or valleys greater influence. The final square root returns the unit from nm² to nm. For heights −1, 1, −1 and 1 nm, the mean is zero and Sq is 1 nm. Adding 100 nm to every value changes the height origin but leaves Sq unchanged. Adding a genuine slope changes deviations across the field and changes Sq. Roughness is independent of an overall offset, yet depends on the background removed.

Equal Sq does not imply equal surfaces. A landscape of fine, closely spaced bumps and one of broad waves can have the same height dispersion but different spatial organization for cells, droplets or adhesive contacts. Profiles, two-dimensional maps and correlation length complement Sq. Correlation length can initially be understood as the lateral distance over which surface heights remain related. Scan scale matters too: measurements over 100 nm and 100 μm cover different ranges of wavelength. Describing both height amplitude and lateral organization usually communicates material differences better than listing a single roughness number.

## Read indentation and adhesion from an approach-and-retract curve

A force-curve measurement pauses lateral scanning and moves the probe toward the sample, into contact and indentation, then away again. The instrument records scanner position and cantilever deflection. The precontact baseline helps establish zero and drift. The rising contact segment combines cantilever bending and specimen deformation. During withdrawal, adhesion can hold the probe to the surface, producing a negative force before release. Differences between approach and retract may reflect adhesion, viscoelasticity, fluid drag or molecular extension. Identify the physical stage before selecting a model, so that fitted parameters remain connected to a particular interaction.

Scanner travel is not all specimen indentation. Part of the movement bends the cantilever and part deforms the sample, with the onset of contact defining the reference. Treating scanner displacement as indentation, or placing the contact point too early or late, changes the fitted modulus. Probe radius, spring constant and optical sensitivity govern different conversions and must match the experiment. Compare several reasonable contact points and fitting intervals on the same curve to see how the parameter responds. This helps distinguish a stable description of material response from a result controlled mainly by processing choices.

A common introductory model is Hertzian contact with a spherical indenter. It describes a sphere pressing into a thick, homogeneous, isotropic, linearly elastic material under small-deformation conditions, with contact dimensions small compared with sphere radius and negligible adhesion. Deeper indentation increases both the contact region and the amount of material deformed, so force is not simply proportional to indentation. The model predicts force proportional to indentation raised to the power 3/2. Increasing indentation fourfold therefore increases force eightfold. This growth reflects contact geometry together with elasticity.

$$
F=\frac{4E}{3(1-\nu^2)}\sqrt{R}\,\delta^{3/2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8b97c6f147719ab8db0510f3.svg) | Indentation force, N. |
| ![Formula](https://ml-biomat.com/static/agent-math/2f88d982a5fd3728e7074ecd.svg) | Specimen Young modulus, Pa. |
| ![Formula](https://ml-biomat.com/static/agent-math/5064898bae7c73820eaab47c.svg) | Specimen Poisson ratio; dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/085f4d77675f3cb7323d94fe.svg) | Spherical indenter radius, m. |
| ![Formula](https://ml-biomat.com/static/agent-math/e5b7c4267da3b3fe02d6ae1a.svg) | Specimen indentation after accounting for cantilever bending and contact zero, m. |

Assumes a probe effectively rigid relative to a thick, homogeneous, isotropic, linearly elastic specimen, small contact deformation and negligible adhesion. With E=20000 Pa, ν=0.45, R=10⁻⁶ m and δ=50×10⁻⁹ m, F≈3.73846×10⁻¹⁰ N, or 0.374 nN.

The example uses a 1 μm spherical probe radius, an elastic modulus of 20 kPa and a Poisson ratio of 0.45, over indentations of 2–100 nm. Poisson ratio describes lateral expansion accompanying axial compression; values near 0.5 correspond to small volume changes. At 50 nm indentation, the model gives approximately 0.374 nN. The program adds reproducible small noise, fits the same model and plots residuals. A separate panel varies assumed probe radius: a larger radius requires a smaller fitted modulus to explain the same force curve. A visually close fit therefore still depends on geometrical calibration.

![Constructed Hertz contact data for a 1 μm sphere, 20 kPa specimen and Poisson ratio 0.45. A shows noisy observations and fit; B gives residuals; C holds the curve fixed while changing assumed probe radius, revealing the relationship between geometry calibration and modulus.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/4576f3b265efb92cb6e05eb9.svg?v=4576f3b265ef)

Figure 3Constructed Hertz contact data for a 1 μm sphere, 20 kPa specimen and Poisson ratio 0.45. A shows noisy observations and fit; B gives residuals; C holds the curve fixed while changing assumed probe radius, revealing the relationship between geometry calibration and modulus.

A thin coating can feel the underlying stiff substrate when indentation becomes sufficiently deep. In a cell, local thickness, cytoskeleton, fluid flow and measurement speed can all contribute. A viscoelastic gel may yield different apparent moduli at different loading rates. Changing indentation range, loading speed, probe size or location helps identify the controlling contribution. Reporting a local modulus fitted under specified probe, environment and loading conditions connects the number naturally to its measurement. Each colored pixel in a mechanical map comes from such curves and model choices; stiffness is not a color directly photographed from the specimen.

## Test geometry, leveling and contact mechanics separately

Adhesion in a force curve can itself be the research target. The most negative force during retraction is often used to describe pull-off, but its value depends on contact time, loading history, probe chemistry, humidity or liquid composition. Small liquid bridges in air can increase attraction; electrostatic screening or polymer connections in liquid produce different responses. To compare a protein-coated surface with bare substrate, keep probe conditions and contact time comparable, repeat across positions and check whether material accumulates on the probe. These comparisons connect an adhesion difference to a defined interface process rather than treating every negative force as the same molecular event.

The complete program treats three questions independently. First it changes tip curvature to examine lateral broadening. Second it adds a known tilt to a constructed surface, then uses plane fitting to recover its variations. Third it generates a force curve from specified elastic parameters, adds noise and refits the curve. Outputs include bilingual figures, raw and leveled height arrays, a point-by-point force table and a numerical summary. Known teaching values let the analysis be checked under its own assumptions before considering additional experimental complications such as contact uncertainty, adhesion, drift and heterogeneity.

### Complete Python: tip broadening, plane leveling and indentation fitting

Explicit teaching surfaces and contact parameters produce exported data, fit residuals, numerical summaries and three bilingual figures.

```
"""AFM teaching models: probe broadening, levelling and Hertz indentation.

All arrays are constructed teaching data. No experimental surface or cell is claimed.
"""
from pathlib import Path
import argparse,json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon

def hertz(delta,E,R,nu):return 4/3*E/(1-nu**2)*np.sqrt(R)*delta**1.5
def broadening(x,radius,height=10,width=20):
    distance=np.maximum(np.abs(x)-width/2,0)
    return np.maximum(height-distance**2/(2*radius),0)

def main(output,language):
    output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'svg.fonttype':'none','font.size':11,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','text.color':'#243b45','axes.labelcolor':'#243b45'})
    tr=lambda a,b:a if language=='zh' else b
    green,blue,red,gray='#168477','#3474a8','#bd624b','#788b90'
    def save(fig,name):
        fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');fig.savefig(output/f'{name}-{language}.png',dpi=140,bbox_inches='tight');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,5.5),layout='constrained')
    for ax in axes:ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
    ax=axes[0];ax.set_title(tr('A  1986：用悬臂弯曲读取微小力','A  1986: cantilever bending senses force'))
    ax.add_patch(Rectangle((1,3.8),6,.15,fc='#d6b664'));ax.add_patch(Rectangle((.8,3),.5,2,fc=gray));ax.add_patch(Polygon([[6.5,3.8],[7,3.8],[6.75,3]],fc=blue));ax.add_patch(Rectangle((1,1.5),8,.4,fc='#c8d6ca'))
    ax.add_patch(Polygon([[6.4,6.5],[7.1,6.5],[6.75,4.3]],fc=red));ax.text(6.75,7,tr('STM读取悬臂位移','STM reads cantilever displacement'),ha='center',fontsize=10)
    ax.text(3.5,4.4,tr('金属悬臂','Metal cantilever'),ha='center');ax.text(7.2,2.9,tr('金刚石探针','Diamond tip'),fontsize=10);ax.text(4.7,.8,tr('压电位置控制','Piezo position control'),ha='center');ax.annotate('',(6.75,3),(6.75,2),arrowprops={'arrowstyle':'<->','color':green})
    ax=axes[1];ax.set_title(tr('B  常用光杠杆读出与反馈','B  Common optical-lever readout and feedback'))
    ax.add_patch(Rectangle((1,3.8),6,.15,fc=gray));ax.add_patch(Polygon([[6.4,3.8],[7,3.8],[6.7,2.9]],fc=blue));ax.add_patch(Rectangle((1,1.7),8,.3,fc='#c8d6ca'))
    ax.plot([2,6.5,8.8],[7,3.95,6.8],color=red,lw=2);ax.text(1.6,7.4,tr('激光','Laser'));ax.add_patch(Rectangle((8.2,6.5),1.2,.6,fc='#d5e5eb',ec=blue));ax.text(7.1,7.5,tr('分区探测器','Split detector'),fontsize=10)
    ax.text(3,5,tr('悬臂弯曲 → 光斑移动','Bending → spot displacement'),ha='center',fontsize=10);ax.text(5,.6,tr('反馈调节z位置，使相互作用接近设定值','Feedback changes z to maintain the interaction setpoint'),ha='center',fontsize=10)
    save(fig,'principle')
    x=np.linspace(-80,80,801);truth=np.where(np.abs(x)<=10,10.,0.)
    grid=np.linspace(-250,250,129);X,Y=np.meshgrid(grid,grid);surface=2*np.cos(2*np.pi*X/500)+np.cos(4*np.pi*Y/500);plane=.025*X-.015*Y+7;raw=surface+plane
    design=np.column_stack([X.ravel(),Y.ravel(),np.ones(X.size)]);coef=np.linalg.lstsq(design,raw.ravel(),rcond=None)[0];level=raw-(design@coef).reshape(X.shape)
    sq=lambda a:float(np.sqrt(np.mean((a-a.mean())**2)))
    fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained');ax=axes[0,0];ax.fill_between(x,truth,color=gray,alpha=.3,label=tr('真实台阶','True step'))
    for radius,color in [(5,green),(20,red),(60,blue)]:ax.plot(x,broadening(x,radius),color=color,lw=2,label=f'R={radius} nm')
    ax.set(xlabel='x / nm',ylabel=tr('高度 / nm','Height / nm'),title=tr('A  更钝的针尖使横向轮廓更宽','A  Blunter probes broaden lateral outlines'));ax.legend(frameon=False,fontsize=9)
    for ax,a,title in [(axes[0,1],raw,tr('B  原始高度：表面加倾斜','B  Raw height: surface plus tilt')),(axes[1,0],level,tr('C  减去拟合平面','C  Subtract a fitted plane'))]:
        im=ax.imshow(a,extent=(-250,250,-250,250),origin='lower',cmap='cividis');ax.set(xlabel='x / nm',ylabel='y / nm',title=title);cb=fig.colorbar(im,ax=ax,shrink=.8);cb.set_label(tr('高度 / nm','Height / nm'))
    axes[1,1].plot(grid,raw[64],color=red,label=tr('原始剖面','Raw profile'));axes[1,1].plot(grid,level[64],color=green,label=tr('调平后剖面','Levelled profile'));axes[1,1].set(xlabel='x / nm',ylabel=tr('高度 / nm','Height / nm'),title=tr('D  倾斜改变粗糙度统计','D  Tilt changes roughness statistics'));axes[1,1].legend(frameon=False);axes[1,1].text(.04,.06,f'Sq: {sq(raw):.3f} → {sq(level):.3f} nm',transform=axes[1,1].transAxes)
    save(fig,'topography')
    delta_nm=np.linspace(2,100,100);delta=delta_nm*1e-9;E=20e3;R=1e-6;nu=.45;clean=hertz(delta,E,R,nu);rng=np.random.default_rng(1705);observed=clean+rng.normal(0,8e-12,len(delta));basis=hertz(delta,1,R,nu);Efit=np.dot(basis,observed)/np.dot(basis,basis);fit=basis*Efit
    fig,axes=plt.subplots(1,3,figsize=(13,4.5),layout='constrained')
    axes[0].scatter(delta_nm,observed*1e9,s=12,color=gray,label=tr('构造观测数据','Constructed observations'));axes[0].plot(delta_nm,fit*1e9,color=green,lw=2,label=tr('赫兹拟合','Hertz fit'));axes[0].set(xlabel=tr('压入深度 / nm','Indentation / nm'),ylabel=tr('力 / nN','Force / nN'),title=tr('A  球形探针弹性接触','A  Spherical elastic contact'));axes[0].legend(frameon=False,fontsize=9)
    axes[1].plot(delta_nm,(observed-fit)*1e12,color=blue);axes[1].axhline(0,color=gray);axes[1].set(xlabel=tr('压入深度 / nm','Indentation / nm'),ylabel=tr('残差 / pN','Residual / pN'),title=tr('B  检查拟合剩余结构','B  Inspect remaining structure'))
    assumed=np.linspace(.5,2,100);estimates=Efit*np.sqrt(1/assumed);axes[2].plot(assumed,estimates/1000,color=red,lw=2);axes[2].axvline(1,color=gray,ls='--');axes[2].set(xlabel=tr('假定探针半径 / μm','Assumed probe radius / μm'),ylabel=tr('拟合模量 / kPa','Fitted modulus / kPa'),title=tr('C  半径标定影响模量','C  Radius calibration changes modulus'))
    save(fig,'force')
    with (output/'data.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f);w.writerow(['indentation_nm','true_force_nN','constructed_observation_nN','fitted_force_nN','residual_pN']);w.writerows(zip(delta_nm,clean*1e9,observed*1e9,fit*1e9,(observed-fit)*1e12))
    np.savez_compressed(output/'topography.npz',x_nm=grid,raw_nm=raw,levelled_nm=level,true_nm=surface)
    exact=np.dot(basis,clean)/np.dot(basis,basis)
    summary={'force_02Npm_5nm_nN':1.,'width_halfheight_R20_H10_W20_nm':20+2*np.sqrt(20*10),'sq_raw_nm':sq(raw),'sq_levelled_nm':sq(level),'sq_true_nm':sq(surface),'hertz_force_50nm_nN':float(hertz(50e-9,E,R,nu)*1e9),'fitted_E_kPa':float(Efit/1000),'noiseless_E_kPa':float(exact/1000),'plane_slope_x':float(coef[0]),'plane_slope_y':float(coef[1]),'data_origin':'Constructed AFM geometry, surface and indentation teaching data.'}
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--language',choices=['zh','en'],default='zh');a=p.parse_args();main(a.output,a.language)
```

The executed example gives Sq=4.528 nm before leveling and Sq=1.587 nm afterward. The latter matches the known constructed surface because its added plane is recovered with slopes 0.025 and −0.015. The force fit returns approximately 20.003 kPa after adding the specified noise; fitting the noiseless curve recovers 20 kPa. These checks serve different purposes. Plane recovery tests background subtraction, whereas noiseless modulus recovery tests the contact-model calculation. Neither depends on making the displayed curves look attractive. In an experiment, analogous checks use calibration specimens, repeated observations and comparison of residual structure with the physical process being measured.

A complete surface study may begin with optical localization, use AFM to measure height in selected regions, and then add force curves or repeated measurements in another environment. A protein adsorption study can connect coverage, thickness and local interaction; a hydrogel study can compare topography with indentation at corresponding positions; a coating study can connect nanoscale morphology with wetting, adhesion or bulk mechanics. Retaining raw signals, calibration, specimen state and analysis definitions allows information from a tiny probe to contribute to a broader materials or biological question.

## Connect a hydrogel's surface map with its mechanical map

Measure a stable reference before and after the series when probe changes are plausible. A changed reference response can reveal contamination or calibration drift that would otherwise be assigned to the hydrogel.

Suppose the aim is to compare hydrogels with two crosslinking levels and determine whether increased crosslinking changes both surface variation and local resistance to indentation. Bring both groups to comparable equilibrium in the same solution and temperature, then record the measurement regions optically. Acquire height maps at the same spatial scale, with comparable interaction settings and an explicit leveling rule. Collect force curves using a calibrated spherical probe and the same loading program across several positions. Retain the raw data for each measurement type, then associate them by location. This connects structure and response without reading stiffness directly from a height-map color.

If the second group has larger Sq and a higher fitted modulus, inspect the level at which those changes occur. Every specimen may follow a consistent trend, or a small population of raised regions may be both rougher and stiffer. Overlaying indentation positions on topography helps separate matrix, raised features and boundaries, turning an overall comparison into a more specific structural question. A raised feature only tens of nanometers thick may be influenced by underlying material during deeper indentation. A mobile feature may move under the probe, becoming evident in before-and-after height images. Spatial correspondence and repeated observation make the mechanism more interpretable.

Measurement order deserves attention too. A scan may modify a weakly attached region before its force curve is collected, while repeated indentation may leave a depression visible in the next scan. Include nearby regions with a different order or revisit a minimally disturbed reference location when that distinction matters. This is particularly useful for soft, hydrated interfaces whose structure can evolve during the experiment. Record the elapsed time after a solution exchange and the timing of each map. Temporal information then complements spatial coordinates, helping separate equilibration, local loading and changes caused by repeated observation.

A useful final figure can combine height maps on matched spatial scales, representative force curves, specimen-level parameter distributions and a few informative profiles. Height and modulus color bars need different units, while scale bars remain explicit. State how many independent specimens and measurement positions contribute to each distribution. Representative curves should include the baseline, contact region and fitting interval so that the reader sees where the modulus comes from. Distributions reveal whether the material is uniform. Together, these views answer both what the surface looks like and how it responds under the stated conditions, linking crosslinking structure with material behavior.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/I05.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Binnig, Quate & Gerber — Atomic Force Microscope (1986)](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.56.930)

   Original AFM paper and early readout concept.

   Primary paper; original explanatory figure here.
2. [APS Physics — AFM landmark](https://physics.aps.org/articles/v5/106)

   1986 apparatus, metal cantilever, tunneling readout and subsequent optical detection.

   Publisher historical account; no image reused.
3. [Gwyddion — Tip Convolution Artefacts](https://gwyddion.net/documentation/user-guide-en/tip-convolution-artefacts.html)

   Probe geometry, morphological dilation and reconstruction.

   Guide GPL v2+ or GFDL v1.2+; linked reference, figures original.
4. [Gwyddion — Data Levelling and Background Subtraction](https://gwyddion.net/documentation/user-guide-en/leveling-and-background.html)

   Consequences of plane, polynomial and masked leveling.

   Guide GPL v2+ or GFDL v1.2+; linked reference.
5. [Gwyddion — Statistical Analysis](https://gwyddion.net/documentation/user-guide-en/statistical-analysis.html)

   Areal roughness, statistical quantities and scale interpretation.

   Guide GPL v2+ or GFDL v1.2+; linked reference.
6. [JPK / Bruker — A practical guide to AFM force spectroscopy](https://www.bruker.com/en/products-and-solutions/microscopes/bioafm/resource-library/a-practical-guide-to-afm-force-spectroscopy-and-data-analysis/_jcr_content/root/sections/section/sectionpar/twocolumns/contentpar-2/calltoaction.download-asset.pdf/primaryButton/jpk-tech-force-spectroscopy.14-2.pdf)

   Approach/retract, conversion to force, calibration and interactions.
