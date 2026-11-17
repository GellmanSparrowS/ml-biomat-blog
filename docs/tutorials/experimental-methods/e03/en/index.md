# Degradation: How materials change with time

Source: https://ml-biomat.com/tutorials/experimental-methods/e03/en/
Language: en

Follow molecular scission, mass loss and carbon destinations to understand structural change and functional lifetime.

## When does a material lose its function, and when does it leave?

An absorbable suture must hold tension while tissue heals and then be processed by the body. A tissue-engineering scaffold provides initial support while making space for new tissue. A degradable package encounters a different set of environments, such as compost, soil or water. All involve degradation, but the relevant clocks differ. A suture can lose substantial strength before its mass decreases appreciably, while a film can fragment into small pieces that remain polymeric. Designing a degradation experiment begins by deciding whether the question concerns chemical connections, structural integrity, retained function or the eventual destination of material.

Cutting a long necklace into two pieces provides a useful starting point. The number of beads stays the same, but the number of chains doubles and the average chain becomes shorter. If both pieces remain in the original specimen, a balance sees little change. Mass decreases when fragments become able to dissolve and move away. Chain scission, formation of soluble fragments and escape from the specimen can therefore follow different time courses. Measuring molecular size alongside mass often reveals internal change earlier than weighing alone. The two measurements describe linked stages of a process rather than interchangeable definitions of degradation.

Several terms are useful when kept distinct. Degradation concerns changes in chemical structure or macromolecular connections. Erosion describes material leaving the specimen, often observed as loss of mass or dimensions. Fragmentation divides an object into smaller pieces. Mineralization tracks conversion of organic carbon into inorganic products such as carbon dioxide. These processes can promote one another without occurring simultaneously. Mass loss in an enzyme solution and biological conversion in compost involve different environments and evidence. Assigning each term to an actual measurement makes the study's question and its interpretation more precise.

A connected study usually follows three kinds of evidence: mass, morphology and function of the specimen; molecular size or chemical change within it; and products entering liquid or gas. Select the measurements that matter to the application and arrange sampling around their likely sequence. This chapter uses a constructed random-scission model to explain why shorter molecules can precede mass loss, published gel images to examine changes under enzyme exposure, and carbon accounting to define a mineralization denominator. The complete example plots these processes separately so that each can guide an appropriate experimental choice.

## Water, enzymes and diffusion work together

Many polyesters contain ester bonds along their backbone. Hydrolysis breaks a connection through a reaction involving water, generating new chain ends and progressively shorter molecules. Its rate depends on temperature, acid–base conditions, chemical structure and the local environment. Proteins and some polysaccharide networks can also be cleaved by suitable enzymes. An enzyme is a biological macromolecule that catalyzes particular reactions after accessing compatible structures. The presence of a cleavable bond establishes a possible reaction route; whether water or enzyme reaches that bond also contributes to the rate observed in a specimen.

Think of the material as a building. Water or enzyme must enter, reactions take place in accessible rooms, and generated fragments must find a route out. When water enters rapidly relative to bond cleavage, reactions can occur throughout the interior, giving bulk degradation. When the active species mainly accesses the outer region, or reacts quickly before penetrating farther, change can concentrate near the surface. These modes are not permanent labels attached to a polymer name. Dimensions, porosity and environment alter the balance between access, reaction and escape, sometimes changing the dominant behavior for the same chemistry.

In 1995, Grizzi and colleagues compared devices of different dimensions made from the same batch of poly(DL-lactic acid). Their study examined the coupling of reaction and diffusion during hydrolysis. Larger specimens can retain acidic degradation products internally, accelerating reactions there, whereas smaller structures provide shorter escape paths. The example shows why a larger surface-to-volume ratio does not establish a universal ranking of degradation speed. The historical diagram emphasizes two roles of geometry: controlling entry distances and controlling product accumulation. Their combined effect must be examined rather than inferred from exposed area alone.

![Original mechanism and history diagram: a backbone cut increases molecule count, while specimen size changes product diffusion distance. Grizzi and colleagues’ 1995 size comparisons connected PLA degradation with reaction–diffusion coupling. Arrows illustrate processes rather than measured fluxes.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/7ba778392616f5008a0fa627.svg?v=7ba778392616)

Figure 1Original mechanism and history diagram: a backbone cut increases molecule count, while specimen size changes product diffusion distance. Grizzi and colleagues’ 1995 size comparisons connected PLA degradation with reaction–diffusion coupling. Arrows illustrate processes rather than measured fluxes.

Enzymatic degradation adds enzyme size, adsorption and activity to the transport problem. An open porous gel can make internal sites more accessible, while a dense network may be attacked mainly near its exterior. Enzyme amount may be reported as mass concentration or activity units, which describe different quantities. Equal milligrams from different preparations need not provide equal catalytic activity. Record enzyme identity, activity definition, storage and replacement conditions. A matching buffer control without enzyme helps separate hydrolysis, dissolution and the additional changes associated with enzyme exposure. The control should experience the same temperature, handling and sampling schedule.

Material history also matters. Crystalline regions contain more ordered chains than amorphous regions, with consequences for water access and chain mobility. Processing changes crystallinity, orientation and residual stress; sterilization can change initial molecular size. A chemical name alone therefore provides an incomplete starting description. Record grade, molecular-size distribution, crystallinity, dimensions and preparation conditions relevant to the comparison. For a biomaterial, begin from the state in which the material would actually enter its intended experiment or use. That reference makes the subsequent timing of functional and structural changes easier to interpret.

## Mass, chain length and function provide complementary readings

Weighing is intuitive but combines several possible changes. To measure dry-polymer mass loss, clean and dry each time-point specimen consistently before comparison with initial dry mass. Wet-gel mass also depends on hydration and should be named separately. Filler escape, salt deposition, protein adsorption and vessel residues can affect the balance reading. List the substances that may enter or leave, then choose blanks and composition corrections appropriate to them. This preparation ties the mass difference to the research question. Otherwise a highly repeatable weighing may still mix polymer erosion with water uptake or a change in nonpolymer components.

$$
L_m(t)=1-\frac{m_d(t)}{m_d(0)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/99da358d7cf8b7d2ecc3cb0b.svg) | Dry-mass loss fraction at time t, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/083a973ce5ea6d3e3795e784.svg) | Remaining dry mass at t under the same washing and drying conditions, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/ce9c3374598b0bc90f891f70.svg) | Initial dry mass on the same basis, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Immersion or exposure time, d in this example. |

Subtract remaining mass from initial mass and divide by initial mass. An initial 100 mg and remaining 80 mg give Lm=0.20, or 20%. Account for salts, filler and residual liquid according to the material being measured.

A specimen starting at 100 mg dry mass and retaining 80 mg has lost 20% of its dry mass. If 10 mg of salt remains on it, an uncorrected result would suggest only 10% loss. If washing discards an insoluble fragment, the measured loss also includes handling of solid material. For easily fragmented specimens, collect visible pieces and filter-retained particles where appropriate and document their destinations. This distinguishes conversion to dissolved products from conversion to smaller solids. Those categories can have different significance for an implant, a release carrier and a material exposed to the environment.

Molecular-size measurements examine the chains themselves. Number-average molar mass averages molecular mass over the number of molecules. Dividing the same total number of repeat units among more molecules lowers that average. For an accessible calculation, use number-average degree of polymerization: the average number of repeat units per chain. One hundred chains, each containing one hundred units, contain ten thousand units altogether. Cutting each chain exactly once produces two hundred chains and an average length of fifty, while the total repeat-unit count remains ten thousand. The arithmetic explains why substantial chain change can precede erosion.

$$
\overline{N}_n=\frac{N_{\rm units}}{N_{\rm chains}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/e1867b609e4ab077116615bd.svg) | Number-average degree of polymerization, repeat units per chain, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/bf2c4bb71bb69b11da8c031e.svg) | Total repeat-unit count in the population being considered, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/67fcf314cf72502074519d11.svg) | Chain count in the same molecular population, dimensionless. |

Distribute all repeat units among all chains. One thousand chains of 100 units contain 100000 units. Cutting each once while retaining every fragment increases the count to 2000 and decreases mean length to 50 without reducing polymer mass.

Size-exclusion chromatography can reveal the molecular-size distribution of soluble polymer, but the population sent into the instrument defines the result. Dissolving and analyzing the remaining solid excludes small fragments that already entered the bath. Analyzing only the bath emphasizes species able to escape. Cross-linked networks may be difficult to dissolve at all and require another chemical or structural measurement. State the analyzed fraction explicitly. “Mean chain length in the remaining material” and “mean chain length of all generated fragments” are different quantities, and selective removal can make them evolve differently even under the same bond-cleavage mechanism.

Functional measurements return to the reason the material exists. A suture may be followed by breaking force, a supporting scaffold by compression or fatigue, and a barrier by integrity or permeability. Keep hydration, temperature and loading conditions comparable because they directly affect response. Early chain shortening with little mass loss can accompany a mechanical change. Other materials soften through hydration and later change through crystallization or structural rearrangement. Placing functional, mass and molecular-size measurements on the same time axis reveals the useful operating interval more clearly than any single endpoint described as complete degradation.

## Make time points, controls and environment one experiment

A pretreatment comparison can identify early washout of material already soluble at the start. Compare specimens that have been extracted and re-equilibrated with specimens in the actual post-preparation state, following early bath composition and dry mass. A difference concentrated in the first interval directs attention to residual additives or unconnected polymer. Pretreatment can also change structure, so characterize both starting states rather than assuming that washing removes only one component. This comparison separates an initial inventory difference from fragments newly generated during the subsequent exposure and helps position the first informative degradation time points.

Choose the environment in relation to the application. A hydrolysis study may use an aqueous medium with specified pH and ions. An enzyme study needs enzyme identity and activity. A composting study requires its corresponding inoculum, temperature, moisture and gas exchange. Each arrangement answers a particular question. Directly converting a high-temperature hydrolysis time into an in-body residence time would skip changes in chemistry, enzymes, transport and tissue interactions. A useful progression first establishes comparisons under defined conditions, checks whether the mechanism remains relevant, and then tests the critical interval in the target environment.

Sampling is often destructive. Drying changes a hydrogel, chromatography requires dissolving material, and tensile testing may break the specimen. Allocate independent samples to time points and distribute preparation batches across those groups. Assigning one batch only to early times and another only to late times confounds batch with aging. Measure the actual initial state after preparation and pretreatment as well. For continuous observation, imaging or dimensional measurements may follow a specimen without strongly changing it, while independent specimens supply destructive measurements. This combination preserves a time narrative without assuming every assay leaves the material unaffected.

Place time points around the expected sequence. Early changes may reflect soluble-component washout or hydration, intermediate changes may appear in molecular size, and major mass loss may arrive later. Measuring only the beginning and end compresses these stages into one percentage. A small exploratory series can identify intervals of changing morphology, chain size or mechanics, followed by denser sampling in those intervals during a formal comparison. Slow systems need a sufficiently long observation window. Fast enzymatic systems also require recording the time needed to collect a specimen and stop or substantially slow its ongoing reaction.

Medium replacement changes the experiment. Retaining one bath accumulates products and supports material accounting, but can also accumulate acids, lose enzyme activity or deplete biological resources. Replacing the medium maintains some external conditions while removing products and changing feedback. Both designs can answer useful questions when replacement time, volume and sampling fraction are recorded. For an autocatalytic polyester, the bath pH may also differ from the internal pH. A stable external reading therefore does not by itself establish an unchanged internal environment. The relevant transport distances and buffering behavior help determine that relationship.

Accelerated testing benefits from a mechanism check. Heating shortens waiting times, but crossing a glass transition, changing crystallinity or deactivating an enzyme can change the controlling process. Compare morphology, products and molecular-size changes across temperatures before interpreting a temperature dependence as a lifetime transformation. A smooth high-temperature curve alone does not determine behavior elsewhere. Acceleration is useful for ranking formulations within a defined test regime. Estimating an application-specific lifetime additionally needs observations under the target conditions and a connection between those observations and the proposed acceleration model.

## Shorter chains can appear before substantial mass loss

Chain length is a distribution as well as an average. Two materials with the same number-average length may differ because one combines many short chains with a few very long chains while another has a narrow distribution. Their soluble fractions, entanglements and mechanical responses can consequently differ. The program retains expected counts for every fragment length and converts those counts into mass associated with each length class. This reveals both the mean and the accumulation of short fragments. A distribution plot therefore supplies information that would be hidden if the entire molecular population were reduced to one average.

The teaching model starts with many identical linear chains, each containing one hundred repeat units. Each bond is cut independently at the same constant rate. With time, the probability that a particular bond has been cut increases. Repeat units are treated as equal-mass beads, leaving aside the small end-group mass changes of actual hydrolysis so that attention stays on molecule count and material escape. Expected counts of fragments of each length can be calculated directly. This produces a reproducible distribution without requiring random fluctuations to stand in for an explanation of the underlying process.

$$
p(t)=1-e^{-kt},\qquad \overline{N}_n(t)=\frac{N_0}{1+(N_0-1)p(t)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/9b836c2bf1155191ac0f8ab3.svg) | Probability that an initial backbone bond has been cut by t, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/8dc6f7e80ecaac9fa07890ce.svg) | Rate constant for independent identical bond scission, d^{-1}. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Exposure time, d. |
| ![Formula](https://ml-biomat.com/static/agent-math/358eaab52fd29057e6b95399.svg) | Repeat units per initial linear chain, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/9197ac85a3550d73ddda69d0.svg) | Population number-average degree of polymerization including all fragments, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/0be950b3e59846bc80f7e4ca.svg) | Base of the natural exponential function, dimensionless. |

A chain of N0 units has N0−1 bonds and each cut adds a fragment. Across many identical starting chains, expected fragment count is 1+(N0−1)p. With N0=100 and p=0.1, 10.9 fragments give a number-average degree of 100/10.9=9.174. Autocatalysis and spatial variation are absent from this model.

A second rule states that fragments of eight units or fewer immediately enter the bath, while longer fragments remain. Eight units is a teaching threshold, rather than a universal solubility limit for polymers. Real solubility depends on chemistry, temperature and interactions, and escape takes time. A defined threshold nevertheless makes the stages visible: scission generates smaller molecules, while only some satisfy the removal rule. Changing the threshold shows why an unchanged chemical scission rate can produce a different mass-loss curve. It separates the chemistry that creates fragments from the physical selection that removes them.

![Constructed independent-scission model and a separate spherical surface-erosion model. Mean lengths in A are normalized to their initial value of 100; B shows mass by fragment-length class; C changes only the maximum soluble length; D changes only initial radius. The panels distinguish molecular, mass, solubility and geometry effects.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/6a35f816c2402e0b29cc662b.svg?v=6a35f816c240)

Figure 2Constructed independent-scission model and a separate spherical surface-erosion model. Mean lengths in A are normalized to their initial value of 100; B shows mass by fragment-length class; C changes only the maximum soluble length; D changes only initial radius. The panels distinguish molecular, mass, solubility and geometry effects.

At a cut probability of 0.10 per bond, an initial one-hundred-unit chain produces an expected 10.9 fragments. The number-average length across all fragments is about 9.174 units, or 9.174% of its initial value. Yet the eight-unit removal threshold leaves approximately 74.38% of the initial repeat-unit mass in the specimen. These very different changes arise within the same mass-conserving model. Molecular-size and gravimetric measurements capture different stages, so limited early mass loss can coexist with extensive molecular change. The calculation makes that distinction quantitative without requiring either measurement to be incorrect.

The plots also separate the mean length of all fragments from that of retained fragments. Once short fragments leave, the remaining population has been selected and its mean length exceeds the value for the complete population. This matters when only solid material that can still be recovered is analyzed at successive times. The interactive experiment changes scission rate, observation time and solubility threshold while displaying mass retention and mean lengths. Keep the scission rate fixed and vary only the threshold: the all-fragment mean stays tied to the same bond history, while mass retention responds to the changed removal rule.

## Separate chain scission from dissolution

Initial chain length is 100. Bonds break independently and fragments at or below the chosen threshold immediately enter solution. Compare the mean length of all fragments with retained polymer mass.

[Figure: Fragment mass distribution](https://ml-biomat.com/tutorials/experimental-methods/e03/en/#E03-plot)

The lower-right panel shows a separate idealized surface-erosion model for a sphere. Its surface recedes at constant speed and density stays constant, making mass proportional to radius cubed. Starting from a radius of 1 mm and a recession speed of 0.005 mm/day, after 100 days the radius is halved and one eighth of the mass remains. Its assumptions differ from the random bulk-scission model. The comparison illustrates how geometry can shape an erosion curve. Cross-sectional morphology, internal chemical change and size dependence help determine which description is useful for an actual material.

$$
\frac{m(t)}{m(0)}=\left[\max\left(1-\frac{vt}{R_0},0\right)\right]^3
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1c845ebfe8aa7560445baa5c.svg) | Sphere mass after erosion time t, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/4357fcfe49d6a8dd7d2c3424.svg) | Initial sphere mass, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/6ea26af94b3e02fd7aa1d744.svg) | Constant inward surface recession speed, mm d^{-1}. |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | Erosion time, d. |
| ![Formula](https://ml-biomat.com/static/agent-math/31e316fb976f1ca84f57e4cb.svg) | Initial sphere radius, mm. |
| ![Formula](https://ml-biomat.com/static/agent-math/8228983b74c5db73c259fc11.svg) | Maximum operator, preventing a negative radius. |

For a constant-density sphere that retains its shape, mass scales with radius cubed. Starting with R0=1 mm and v=0.005 mm/d, after 100 d the radius is halved and remaining mass is 0.5 cubed, or 12.5%.

## Images and carbon destinations make degradation more specific

Yin and colleagues compared gelatin-derived gels with different pore architectures under collagenase exposure. The reproduced figure combines mass change, macroscopic photographs and microscopic views, allowing morphology to be followed over time. An important definition comes from the methods: specimens were weighed in their swollen state after external liquid was removed. The graph therefore describes wet-mass change. The original image is retained with that definition made explicit, linking the visual evidence to the actual weighing procedure rather than renaming the result as dry-polymer mass loss.

![Actual microscopy and curves reproduced in full from Yin et al. (2023), Figure 4, Frontiers in Soft Matter, DOI 10.3389/frsfm.2022.1101680, CC BY 4.0. Original figure contents are unchanged; an external title and credit are added. The source uses wet mass, so its decrease is interpreted alongside morphology and water-content changes.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/859c0aa96c29f66acd17b2d8.svg?v=859c0aa96c29)

Figure 3Actual microscopy and curves reproduced in full from Yin et al. (2023), Figure 4, Frontiers in Soft Matter, DOI 10.3389/frsfm.2022.1101680, CC BY 4.0. Original figure contents are unchanged; an external title and credit are added. The source uses wet mass, so its decrease is interpreted alongside morphology and water-content changes.

Macroscopic photographs show whether the object remains intact; microscopy examines local walls and surfaces; the mass curve supplies an overall quantity. Together they explain more than a selected photograph showing the largest change. Compare scale bars, field locations and preparation conditions across time points. Enlarged cavities may accompany erosion but can also reflect swelling, collapse or preparation. Wet-state imaging, dry-mass measurements and composition analysis can help distinguish these possibilities. A useful figure sequence keeps acquisition conditions comparable and relates local observations to independent specimens and the larger quantitative record.

Environmental biological conversion adds the destination of carbon. Microorganisms may convert some material carbon to carbon dioxide, incorporate some into biomass, and leave some as dissolved organics or solid residue. Disappearance of the original object does not establish complete mineralization. Respirometry tracks biological activity through carbon dioxide evolution or oxygen uptake. A parallel inoculum blank without the test material measures background activity from the organisms and medium. A reference substance helps establish that the experimental system functions as intended. These controls tie the measured gas signal to the test substance and the chosen biological environment.

For a carbon-dioxide example, consider 100 mg of material containing 50% carbon by mass. It starts with 50 mg carbon. Each carbon atom entering carbon dioxide is joined by two oxygen atoms, so approximate molar masses of 12 and 44 give a theoretical complete-conversion amount of 183.33 mg carbon dioxide. If the total measured amount is 80 mg and the inoculum blank contributes 14 mg, the specimen-associated net amount is 66 mg. That corresponds to 36% carbon mineralization. The denominator comes from the initial carbon inventory, rather than the original total mass of the material.

$$
B=\frac{m_{\mathrm{CO_2,test}}-m_{\mathrm{CO_2,blank}}}{m_0w_C(44/12)}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/7533ad047439b7d799dd7afe.svg) | Fraction of specimen carbon converted to carbon dioxide, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/1ea936ecb6fb60952e0e8269.svg) | Cumulative carbon dioxide mass collected from the test system, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/827ffe18301532ffcc19ff8f.svg) | Carbon dioxide mass from the matched inoculum blank, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/2fae4459b565e480de0d463f.svg) | Initial dry test-material mass, mg. |
| ![Formula](https://ml-biomat.com/static/agent-math/76b6ff745138a626e7b2b375.svg) | Initial carbon mass fraction of the material, dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/bd59755da4d9bf50091317ae.svg) | Ratio of carbon dioxide to carbon molar masses; units cancel. |

Complete oxidation of 12 mg carbon produces approximately 44 mg carbon dioxide. A 100 mg material with 50% carbon has theoretical CO₂ of 183.333 mg. A test value of 80 mg minus a 14 mg blank gives 66 mg and B=36%. The apparatus must collect the relevant carbon destination.

![Constructed carbon-balance example. The left panel distributes 50 mg initial carbon among solids, dissolved material, biomass and carbon dioxide; the right axis measures the mass of CO₂ itself. Subtracting the inoculum blank leaves 66 mg CO₂, equivalent to 18 mg carbon and 36% mineralization.](https://ml-biomat.com/static/tutorials/experimental-methods/figures/d30308362c9aae4fc709a03b.svg?v=d30308362c9a)

Figure 4Constructed carbon-balance example. The left panel distributes 50 mg initial carbon among solids, dissolved material, biomass and carbon dioxide; the right axis measures the mass of CO₂ itself. Subtracting the inoculum blank leaves 66 mg CO₂, equivalent to 18 mg carbon and 36% mineralization.

The constructed carbon balance divides the initial 50 mg carbon among remaining solid, dissolved organics, biomass and carbon dioxide. Actual mineralization experiments require an environment-appropriate setup, blanks, recovery checks and a defined time course. OECD aerobic aqueous screening methods illustrate this measurement logic, while compost or other media need the corresponding methods. Describe the environment in the result, such as a carbon-conversion curve under specified temperature and inoculum conditions. This gives degradation rate an experimentally reproducible meaning and connects it to the destination of material rather than only its visible disappearance.

## From a falling curve to a useful material lifetime

When a specimen fragments so extensively that it cannot be gripped, record that the chosen mechanical measurement could no longer be performed rather than inserting a measured strength of zero. Residue below the weighing detection range likewise needs an appropriate detection statement. Additional methods suitable for small fragments or low masses can extend the observation, while the time at which the intact form was lost remains useful evidence. This records a functional endpoint without inventing a numerical measurement. It also helps explain gaps in a time series when the material itself changes which assays remain applicable.

The program exports mass retention, number-average length of all fragments and number-average length of retained fragments at every time point. It also plots fragment-size distributions, threshold sensitivity and the separate spherical surface-erosion example. Calculation checks first verify repeat-unit conservation and then a fragment-count relationship that can be checked independently. The published gel image and license notice are bundled for offline execution. The model, actual images and carbon calculation each serve a distinct explanatory purpose. Their labels preserve that distinction so that readers can inspect the calculations without treating the figures as measurements from one material batch.

### Complete Python: Scission distributions, mass loss and carbon destinations

The example exports mean lengths for different molecular populations, retained mass, four figures and a numerical summary. The actual published image and license notice are bundled.

```
"""Constructed random-chain scission, dry-mass retention, and carbon accounting."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,FancyArrowPatch

def _label(text):
    """Readable English labels without changing numbers or scientific identifiers."""
    import re
    if not isinstance(text, str):
        return [_label(x) for x in text] if isinstance(text, list) else text
    return re.sub(r'(?<=[a-z])(?=\d)|(?<=\d)(?=[a-zμµ])|(?<=%)(?=[A-Za-z])', ' ', text)


def fragment_distribution(probability,length=100):
    """Expected fragment counts per initial linear chain; independent identical bond cuts."""
    p=float(probability);l=np.arange(1,length+1);counts=np.empty(length)
    counts[:-1]=((length-l[:-1]-1)*p*p+2*p)*(1-p)**(l[:-1]-1)
    counts[-1]=(1-p)**(length-1)
    return l,counts

def response(time,rate=.003,cutoff=8,length=100):
    probability=1-np.exp(-rate*time);l,c=fragment_distribution(probability,length)
    keep=l>cutoff;mass=np.sum(l[keep]*c[keep]);number=np.sum(c[keep])
    return {'cut_probability':float(probability),'remaining_mass_percent':float(100*mass/length),'all_DP':float(length/c.sum()),'retained_DP':float(mass/number) if number>0 else 0.}

def main(output,language):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    from matplotlib import font_manager
    fonts={x.name for x in font_manager.fontManager.ttflist};font=next((f for f in ['Microsoft YaHei','Noto Sans CJK SC','SimHei'] if f in fonts),'DejaVu Sans')
    plt.rcParams.update({'font.family':[font,'DejaVu Sans'] if language=='zh' else ['DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'#faf9f5','axes.facecolor':'#faf9f5','savefig.facecolor':'#faf9f5','axes.prop_cycle':plt.cycler(color=['#186e83','#cd803f','#8160a1','#3c8a6a'])})
    tr=lambda z,e:z if language=='zh' else _label(e)
    def save(fig,name):fig.savefig(output/f'{name}-{language}.svg',bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(1,3,figsize=(12,4.6))
    for a in ax:a.set(xlim=(0,10),ylim=(0,8));a.axis('off')
    for row,(cut,title) in enumerate([(False,tr('链尚未切断','Uncut chain')),(True,tr('切一次：链数加一','One cut adds one chain'))]):
        xx=np.linspace(1,9,12);yy=np.full(12,6-row*3,dtype=float)
        for i in range(11):
            if cut and i==5:continue
            ax[0].plot(xx[i:i+2],yy[i:i+2],color='#186e83',lw=3)
        ax[0].scatter(xx,yy,color='#186e83',s=30);ax[0].text(5,4.8-row*3,title,ha='center',fontsize=10)
    ax[0].set_title(tr('A  断链先改变分子数量','A  Scission first changes molecule count'))
    for a,r,label in [(ax[1],2.2,tr('内部产物较难排出','Products retained in the interior')),(ax[2],.9,tr('较短的扩散路径','Shorter diffusion paths'))]:
        a.add_patch(Circle((5,4.4),r,color='#a2cdd9'));a.add_patch(Circle((5,4.4),r*.48,color='#cd803f',alpha=.75))
        for ang in [0,np.pi/2,np.pi,3*np.pi/2]:
            start=(5+r*.65*np.cos(ang),4.4+r*.65*np.sin(ang));end=(5+(r+1.1)*np.cos(ang),4.4+(r+1.1)*np.sin(ang));a.add_patch(FancyArrowPatch(start,end,arrowstyle='->',mutation_scale=12,color='#186e83'))
        a.text(5,1.1,label,ha='center',fontsize=9)
    ax[1].set_title(tr('B  大尺度样品','B  Larger specimen'));ax[2].set_title(tr('C  小尺度样品','C  Smaller specimen'))
    fig.text(.5,.02,tr('1995：Grizzi 等通过不同尺寸的聚乳酸器件研究反应与扩散的耦合。','1995: Grizzi and colleagues investigated reaction–diffusion coupling across PLA device sizes.'),ha='center',fontsize=10);save(fig,'mechanism')
    time=np.linspace(0,120,241);records=[response(t) for t in time];remaining=np.array([r['remaining_mass_percent'] for r in records]);all_dp=np.array([r['all_DP'] for r in records]);ret_dp=np.array([r['retained_DP'] for r in records]);np.savetxt(output/'degradation.csv',np.column_stack([time,remaining,all_dp,ret_dp]),delimiter=',',header='time_day,remaining_mass_percent,all_fragments_number_average_DP,retained_fragments_number_average_DP',comments='')
    fig,ax=plt.subplots(2,2,figsize=(11.6,7.3));ax=ax.ravel();ax[0].plot(time,remaining,label=tr('剩余聚合物质量','Remaining polymer mass'));ax[0].plot(time,all_dp,label=tr('全部片段的平均链长','Mean length of all fragments'));ax[0].plot(time,ret_dp,label=tr('仅残留片段的平均链长','Mean length of retained fragments'));ax[0].set(xlabel=tr('时间 / d','Time / d'),ylabel=tr('相对初始值 / %','Relative to initial value / %'),title=tr('A  质量与平均链长分开变化','A  Mass and mean chain length change differently'));ax[0].legend(fontsize=8)
    for t in [10,30,90]:
        l,c=fragment_distribution(1-np.exp(-.003*t));ax[1].plot(l,l*c/100,label=f'{t} d')
    ax[1].axvspan(1,8,color='#cd803f',alpha=.12);ax[1].set(xscale='log',xlabel=tr('片段长度 / 重复单元数','Fragment length / repeat units'),ylabel=tr('初始质量的比例 / 每种长度','Initial mass fraction / length class'),title=tr('B  短片段到达可溶范围','B  Short fragments enter the soluble range'));ax[1].legend(fontsize=9)
    for threshold in [4,8,12]:ax[2].plot(time,[response(t,cutoff=threshold)['remaining_mass_percent'] for t in time],label=f'{threshold}')
    ax[2].set(xlabel=tr('时间 / d','Time / d'),ylabel=tr('剩余聚合物质量 / %','Remaining polymer mass / %'),title=tr('C  改变溶解阈值，不改变断链速率','C  Change solubility threshold, keep scission rate'));ax[2].legend(title=tr('最大可溶长度','Maximum soluble length'),fontsize=9)
    for radius in [.5,1,2]:ax[3].plot(time,100*np.maximum(1-.005*time/radius,0)**3,label=f'{radius:g} mm')
    ax[3].set(xlabel=tr('时间 / d','Time / d'),ylabel=tr('剩余质量 / %','Remaining mass / %'),title=tr('D  独立的球体表面侵蚀模型','D  Separate spherical surface-erosion model'));ax[3].legend(title=tr('初始半径','Initial radius'),fontsize=9)
    fig.tight_layout();save(fig,'kinetics')
    fig,ax=plt.subplots(1,2,figsize=(11,4.8));labels=tr(['剩余固体','溶解有机物','生物量','二氧化碳中的碳'],['Remaining solid','Dissolved organics','Biomass','Carbon in CO₂']);values=[10,15,7,18]
    left=0
    for label,value,color in zip(labels,values,['#186e83','#cd803f','#8160a1','#3c8a6a']):ax[0].barh([0],value,left=left,label=label,color=color);left+=value
    ax[0].set(xlabel=tr('碳质量 / mg','Carbon mass / mg'),yticks=[],xlim=(0,50),title=tr('A  50 mg 初始碳的四条去向','A  Four destinations for 50 mg initial carbon'));ax[0].legend(loc='upper center',bbox_to_anchor=(.5,-.15),fontsize=9,ncol=2)
    ax[1].bar(tr(['测得总量','接种物空白','样品净贡献','理论完全转化'],['Measured total','Inoculum blank','Net specimen','Theoretical total']),[80,14,66,50*44/12],color=['#8160a1','#a8b4b9','#3c8a6a','#186e83']);ax[1].tick_params(axis='x',labelrotation=20);ax[1].set(ylabel=tr('CO₂ 质量 / mg','CO₂ mass / mg'),title=tr('B  扣空白后矿化比例为 36%','B  Blank-corrected mineralization is 36%'));fig.tight_layout();save(fig,'carbon')
    from PIL import Image
    img=np.asarray(Image.open(Path(__file__).with_name('yin2023-figure4.webp')));fig,ax=plt.subplots(figsize=(11,8));ax.imshow(img);ax.axis('off');ax.set_title(tr('真实研究：酶作用下的凝胶形态与湿质量变化','Published study: gel morphology and wet-mass change under enzyme exposure'),fontsize=12,pad=12);fig.text(.5,.015,'Yin et al. (2023), Figure 4 · Frontiers in Soft Matter · CC BY 4.0',ha='center',fontsize=9);save(fig,'published')
    l,c=fragment_distribution(.1);r30=response(30);summary={'worked_example':{'initial_dry_mg':100,'remaining_dry_mg':80,'mass_loss_percent':20,'one_cut_DP_ratio':.5,'one_cut_retained_mass_percent':100},'distribution':{'mass_conserved_units':float(np.sum(l*c)),'expected_fragment_count':float(c.sum()),'mean_DP_at_p_point1':float(100/c.sum()),'retained_mass_at_p_point1_percent':float(np.sum(l[8:]*c[8:]))},'at_day30':r30,'carbon':{'theoretical_CO2_mg':50*44/12,'net_CO2_mg':66,'mineralized_percent':36},'surface':{'radius1_day100_percent':100*(1-.005*100)**3}}
    assert abs(sum(l*c)-100)<1e-10;assert abs(sum(c)-10.9)<1e-10;assert abs(summary['surface']['radius1_day100_percent']-12.5)<1e-12
    (output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--language',choices=['zh','en'],default='zh');args=parser.parse_args();main(args.output,args.language)
```

Change the model scission rate first and observe the shift in timescale. Then change only the soluble-length threshold and compare mass loss while the all-fragment mean length remains unchanged. Finally compare surface-erosion curves for different radii. Changing one condition at a time identifies whether it controls chemistry, separation or geometry. Fitting actual data starts by identifying which molecular population, mass definition and boundary condition were measured. A model should be chosen around those definitions before adding adjustable parameters. Otherwise a visually close curve can combine several processes without distinguishing what the experiment actually observed.

The practical result often lies between two times: when the material begins to lose required function and when its desired structural or chemical transformation has occurred. A scaffold also needs comparison with tissue formation, a release carrier with payload transport, and an environmental material with fragmentation, dissolution and carbon destinations. Organizing results around these questions connects mass, structure and function. A statement about the change observed on a particular day then supports material selection and the next experiment, rather than serving as an isolated percentage detached from the reason the material was designed.

The next chapter considers release experiments. A molecule may leave a carrier through diffusion, through pathways enlarged by swelling, or after degradation removes the structure that retained it. The mass references, sampling records and awareness of medium replacement developed here directly support release calculations. Measuring carrier change and payload destination separately, then connecting their time courses, helps explain why apparently similar release curves can arise from different material processes. That comparison also identifies which additional measurement would most effectively distinguish the competing explanations.

[Download complete code and data](https://ml-biomat.com/static/tutorials/experimental-methods/downloads/E03.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Grizzi et al. (1995). Hydrolytic degradation of devices based on poly(DL-lactic acid) size-dependence](https://pubmed.ncbi.nlm.nih.gov/7772670/)

   Historical experiments on size, autocatalysis and reaction–diffusion coupling.

   Abstract reference; no figures reproduced.
2. [Höglund et al. (2012). Crucial Differences in the Hydrolytic Degradation between Industrial Polylactide and Laboratory-Scale Poly(L-lactide)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3359772/)

   Separation of molecular-weight change from mass loss, and effects of temperature, morphology and medium.
3. [Tsuji et al. (2011). Synthesis and Hydrolytic Degradation of Substituted Poly(DL-Lactic Acid)s](https://www.mdpi.com/1996-1944/4/8/1384)

   Molecular-weight measurements and specimen definitions in hydrolysis experiments.
4. [Yin et al. (2023). Physical properties and cellular responses of gelatin methacryloyl bulk hydrogels and highly ordered porous hydrogels](https://www.frontiersin.org/journals/soft-matter/articles/10.3389/frsfm.2022.1101680/full)

   Enzyme exposure, pore structure, actual microscopy and wet-mass definitions.

   CC BY 4.0; Figure 4 reproduced with attribution.
5. [OECD (1992). Test No. 301: Ready Biodegradability](https://www.oecd.org/en/publications/test-no-301-ready-biodegradability_9789264070349-en.html)

   Blanks, reference compounds, carbon dioxide, oxygen demand and dissolved carbon in aerobic screening.

   Official method reference; no assets reproduced.
