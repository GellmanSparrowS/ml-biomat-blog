# How a Double Helix Moves in Solution

Source: https://ml-biomat.com/tutorials/molecular-dynamics/g11/en/
Language: en

Start with base pairing, water, and ions; run a periodic DNA model and measure the local motion within its double helix.

## From genetic molecule to designed material

Textbook DNA often appears as a perfectly regular double helix, like a spiral staircase that keeps the same shape forever. In water, its steps rock, its handrails deform, and nearby water molecules and ions continually exchange positions. Genetic information lies in the order of the bases, while molecular shape changes with thermal motion and the surrounding environment. Separating sequence from conformation is the first step in reading a nucleic-acid simulation. One sequence supports many conformations, and those conformations affect how proteins approach DNA and which atoms encounter solvent.

This distinction also matters in materials design. Complementary DNA sequences provide selective pairing and can serve as recognition elements or connections within assembled structures. A designer may need to know both whether two sequences pair and how the resulting connection bends or fluctuates. As with a connector in a mechanical model, its length and flexibility influence the larger arrangement. This lesson begins with a well-defined double-helical segment so that local motion can be connected to measurable geometry before being applied to a larger assembly.

We will run a periodic model containing 20 base pairs: two backbones of 20 nucleotides each, 2688 water molecules, and 40 sodium ions. The production record covers 1 ns near 300 K. It is unbiased in the specific sense that no additional force is applied to pull a selected base pair apart. Motion follows the chosen force field and temperature and pressure controls. The supplied starting state is paired, and the short trajectory examines local fluctuations around that state. Covalent backbone connections continue through the axial periodic boundary, a feature that we will examine before running.

By the end, you will be able to identify DNA backbones, bases, water, and counterions; inspect the periodic connections; execute the complete input; and extract three distinct local measurements. These are atomic separation, donor–hydrogen–acceptor direction, and relative tilt between two base-ring planes. Time series, distributions, and a map along the duplex will make the measurements visible. Atom selections, time windows, and units remain attached to each plot, turning a molecular animation into a result that can be examined and recalculated.

The required biology and geometry are introduced where they are used. You can initially regard DNA as two molecular chains with specified connections, then learn the chemistry of their repeating units. Likewise, a trajectory can begin as a sequence of coordinate tables before we calculate distances and angles. Molecular simulation joins these descriptions: chemistry defines connectivity and interactions, while geometry and statistics translate the resulting motion into quantities that can be compared.

### The periodic duplex in solution

Saved frames from the actual 1 ns trajectory, interpreted with the model’s periodic backbone connections.

Official periodic DNA model: 20 base pairs, 40 nucleotides, 1261 DNA atoms, 2688 SPC/E waters and 40 Na, totaling 9365 atoms. Parmbsc1 parameters, 300 K, 1 bar and a triclinic periodic cell; 20 ps pilot followed by a 1 ns unbiased trajectory.

[Download reference data and complete inputs (ZIP) 33.27 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/gromacs-dna-reference-data.zip)

## How diffraction changed the picture of DNA

Understanding DNA did not begin with a sharp molecular photograph that could simply be copied into a model. X-ray diffraction was one of the essential tools of the early 1950s. X-rays passed through oriented DNA fibres, and the resulting scattering pattern was recorded. Franklin and Gosling examined specimens under different hydration conditions: the more hydrated B form and the less hydrated A form produced different patterns. Their diffraction work and the structural studies published in 1953 connected molecular repetition with a double-helical model while making hydration part of the structural question.

Diffraction can be understood through the addition of waves. When two water waves meet, their displacements reinforce each other at some positions and cancel at others. X-rays scattered by different atoms also interfere. Repeating atomic arrangements therefore leave characteristic patterns in the scattered intensity. Interpreting those patterns requires geometry and chemistry; the molecule is not printed directly onto the detector. A proposed structure must accommodate several kinds of information, including molecular composition, plausible bonds, contacts between bases, and the spatial repetition inferred from scattering.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/en/#en-s2)

Figure 1 · Diffraction and structural modelling: repeating arrangements affect diffraction, while a structural model must also satisfy molecular chemistry. The spots are explanatory schematics.

Watson and Crick proposed their double-helical model in 1953, alongside diffraction papers by Franklin and Gosling and by Wilkins and colleagues. Considering these contributions together makes the reasoning process easier to understand. Measurements constrain possible arrangements, a model organizes those constraints into a spatial explanation, and further observations test that explanation. A related distinction is useful in simulation: a coordinate file supplies a starting arrangement, a force field supplies rules for motion, and a trajectory shows what those rules and conditions produce. These descriptions need to refer to the same physical object.

The historical role of hydration leads directly to this lesson. Water occupies the environment of DNA and interacts directionally with exposed chemical groups. Ions modify the electrostatic environment around its charged backbone. Changing experimental humidity and changing the salt content of an aqueous simulation are different operations, but both ask how molecular structure depends on its surroundings. Explicit water and ions let us observe some of that surrounding motion rather than treating the helix as an isolated drawing with empty space around it.

Diffraction and a saved molecular frame also describe structure at different levels. A diffraction signal collects information from many molecules over the measurement, whereas a trajectory frame records one small model at one time. Comparing them requires a corresponding average or scattering observable calculated from the simulation. Here we begin with local geometry that can be measured directly from coordinates. These simpler quantities clarify what the model is doing and prepare us to construct observables that match a particular experiment.

## Reading the model through one base pair

The repeating unit of DNA is a nucleotide, which contains phosphate, deoxyribose sugar, and a base. Sugar and phosphate alternate along the backbone, while each base extends from its sugar. The familiar letters A, T, G, and C denote adenine, thymine, guanine, and cytosine. Sugar carbons use primed labels, such as 1′, 3′, and 5′, to distinguish them from atoms in the base. The direction called 5′ to 3′ follows this chemical connectivity. It is therefore a molecular property, not an arbitrary name for the upward or downward direction in a picture.

In the usual complementary duplex, the two strands run in opposite chemical directions. A pairs with T, and G with C. A local ladder sketch is useful: sugar–phosphate backbones form the two sides, and paired bases occupy the intervening steps. The real structure also twists, stacks neighbouring bases, and forms grooves. Interactions along the stack, contacts across a pair, and solvent all contribute to its organization. Thinking of the entire duplex as two chains held together only by a few drawn hydrogen bonds would omit much of this molecular environment.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/en/#en-s3)

Figure 2 · A local ladder representation separates backbone connectivity from base pairing. Direction labels show the opposite chemical directions when reading down the two backbones.

The first strand in this example has sequence CGCGCGCGCGTGCGCGCGCG. The second, read in its own chemical direction, is CGCGCGCGCACGCGCGCGCG. Reverse the second sequence when checking complementarity across the duplex. The thymine at position 11 of the first strand pairs with an adenine on the second. In the continuous residue numbering of the coordinate file, these are DT11 and DA30. The D denotes a deoxynucleotide and the final letter identifies the base. The analysis uses actual strand and residue identities rather than inferring partners from their apparent proximity in a rendered view.

A hydrogen-bond measurement requires a donor, its bonded hydrogen, and an acceptor. Thymine N3 is covalently connected to H3; adenine N1 is the acceptor selected here. The donor–acceptor distance measures proximity, while the N3–H3–N1 angle describes the direction in which the hydrogen points. Together these provide a more informative geometric contact rule than nitrogen separation alone. A hydrogen-bond contact and a backbone covalent bond also play different roles in this model: nonbonded interactions produce contacts that vary with conformation, while the fixed topology retains the covalent molecular framework.

The supplied amber99bsc1 implementation is used with SPC/E water. It represents DNA atoms explicitly, with bonded and nonbonded interactions describing conformational motion. Bonds involving hydrogen are constrained, supporting the chosen 2 fs timestep. Electronic motion, chemical reactions, and intermolecular proton transfer are separate modelling ingredients. In this calculation, base contacts may weaken and recover as geometry changes while the covalent backbone remains connected according to its topology. Studying chemical damage or enzymatic cleavage calls for a model that includes the corresponding reaction process.

The phosphate-bearing periodic nucleotides give the two strands a combined charge close to −40 elementary charges. Forty Na⁺ counterions make the cell electrically neutral. These ions balance DNA charge; the system does not also contain 40 chloride ions representing an added neutral salt population. Counterions remain mobile, and global neutrality does not eliminate local electric fields. Water orientation, ionic positions, and backbone conformation interact with one another. Later, a precisely defined neighbour count will provide one way of observing this ionic environment.

## What periodic connectivity means for a helix

Periodic boundaries can be pictured as a repeated wallpaper pattern: what leaves one tile continues in its neighbour. In a water box, this mainly specifies the environment encountered across a boundary. This DNA model adds covalent continuity. The end of each displayed backbone is bonded to the beginning of its image in the neighbouring axial cell. The 20 base pairs therefore form one repeating section of a continuous duplex, with no free 5′ or 3′ ends in the represented chain.

This construction focuses attention on the interior of a continuous helix. Free ends of a short duplex can fluctuate differently from interior positions; the periodic model removes those ends from its geometry. The repetition also defines an axial condition. Backbone extension and twist must remain compatible with continuation into the next cell. Bases can still rock and the backbone can still deform, but they do so within the conformations permitted by that connection. End fraying in a finite oligonucleotide or bending over much longer distances requires a model containing the relevant ends and length scales.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/en/#en-s4)

Figure 3 · Left: the 60° xy cell requires full-vector distance calculations. Right: the 20-base-pair unit repeats along z with covalent backbone connections across its boundaries.

The xy cell is tilted, with an angle of 60° between its in-plane edges. Three vectors define periodic translations, and the axial vector is perpendicular to the xy plane. In the first saved frame, they are approximately (4.005,0,0), (2.002,3.468,0), and (0,0,6.540) nm. The second vector has a length near 4.005 nm but a y component near 3.468 nm. Those numbers describe different quantities. Distinguishing vector lengths from Cartesian components prevents a tilted periodic cell from being silently treated as an orthogonal box.

Volume of the tilted cellEq. 5

![Volume of the tilted cell](https://ml-biomat.com/static/agent-math/20e51513b824d8b84ca0c0b9.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| V | Periodic cell volume | nm³ |
| a、b、c | Lengths of the three cell vectors | nm |
| γ | Angle between a and b; c is perpendicular to both | ° |
| sin | Sine, which gives the parallelogram height relative to its side length | operator |
| =、+、−、/、× | Equality, addition, subtraction, division, and multiplication; a fraction bar also means division. | operators |

Reading the relationshipThe xy base is a parallelogram with area a times perpendicular height b sinγ; multiplying by c gives its volume.

A worked exampleFor a=b=4 nm, c=6.5 nm, and γ=60°, V≈90.0666 nm³. Treating the same edge lengths as orthogonal would give 104 nm³.

ConditionsApplies to this cell with its axial edge perpendicular to xy. The code evaluates the determinant of the full cell-vector matrix in each frame.

Distance calculations must use the same geometry. Two neighbouring atoms may appear far apart in the coordinate table because one is stored in a different periodic image. Direct subtraction can then turn a short contact into a distance approaching the cell length. The minimum-image distance finds the shortest separation after allowed cell translations. The analysis passes the complete current box geometry to a distance routine that supports tilted cells. Pressure coupling changes the cell during the trajectory, so each frame uses its own dimensions.

Finding the nearest periodic imageEq. 1

![Finding the nearest periodic image](https://ml-biomat.com/static/agent-math/0a85b50b17c9129522654a18.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| dᵢⱼ | Minimum-image distance between atoms i and j | nm |
| rᵢ、rⱼ | Three-dimensional position vectors of the two atoms | nm |
| a、b、c | Three cell vectors defining one periodic cell | nm |
| n₁、n₂、n₃ | Integer translations along the three cell vectors | dimensionless |
| i、j | Atom indices | dimensionless |
| min、‖ ‖、∈、ℤ | Minimum; vector length; membership; set of integers | operators and set |
| =、+、−、/、× | Equality, addition, subtraction, division, and multiplication; a fraction bar also means division. | operators |

Reading the relationshipPeriodic copies give an atom equivalent coordinates. Selecting the shortest translated separation identifies the distance relevant to a local contact.

A worked exampleIn a one-dimensional 4 nm cell, positions 0.2 and 3.8 nm differ by 3.6 nm. Translating the second by −4 nm gives −0.2 nm, only 0.4 nm from the first.

ConditionsThe actual xy cell angle is 60°. The analysis uses the full cell geometry; component-wise orthogonal wrapping describes a different cell.

Periodic covalent connectivity also changes trajectory processing. Trying to turn an infinitely continued strand into one finite, globally whole molecule creates a conflict: following the covalent path through a repeat leads to a displacement by a cell vector. For local contacts, we instead calculate minimum-image distances directly. For a base-ring plane, we reconstruct only the small ring in a consistent local image. This preserves local geometry while respecting the global topology. The setting `periodic-molecules = yes` tells GROMACS to evaluate the self-connected periodic model accordingly.

Pressure coupling is semiisotropic: xy scales together while z responds separately, with both target pressures set to 1 bar. The term describes box adjustment here; the model contains no membrane. Because the DNA continues along z, its axial repeat and cell volume are useful records alongside local geometry. Instantaneous pressure in a small system can fluctuate widely, while temperature, volume, and base-contact distances vary on different timescales. Each curve therefore needs to be read as its own observable, rather than treated as a universal indicator of structural sampling.

## Running a DNA trajectory from a defined state

The complete example consists of a preparation program, two MD parameter files, a runner, and an analysis program. Place them in one directory and execute `python prepare_dna.py` to obtain the periodic coordinates, topology, atom index, and force field. If the matching source archive is already available, use `--archive dna-awh.zip`. The program verifies the archive before writing the model files. Atomic order and stored velocities remain consistent, and the expected numbers of base pairs, waters, and counterions are reported after preparation.

### Prepare the complete periodic DNA model

```
"""Prepare the official periodic DNA model in the current directory.

python prepare_dna.py --archive dna-awh.zip
Without --archive, the verified upstream archive is downloaded first.
The molecular data and force-field parameters retain the upstream CC BY 4.0 notice.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
from urllib.request import Request, urlopen
from zipfile import ZipFile

URL = 'https://gitlab.com/gromacs/online-tutorials/awh-tutorial/-/archive/main/awh-tutorial-main.zip'
SHA256 = '67dedf235b40959e0b58239a18ade6f2f92beac1cd4fb7756b1bad9c05b15e6c'
PREFIX = 'awh-tutorial-main/awh-simple/'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', type=Path, default=Path('dna-awh.zip'))
    ap.add_argument('--out', type=Path, default=Path('.'))
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    if not args.archive.exists():
        with urlopen(Request(URL, headers={'User-Agent': 'MD-course'}), timeout=60) as response:
            with args.archive.open('wb') as target:
                while block := response.read(1024 * 1024):
                    target.write(block)
    with args.archive.open('rb') as source:
        digest = hashlib.file_digest(source, 'sha256').hexdigest()
    if digest != SHA256:
        raise ValueError(f'SHA256 mismatch for {args.archive.name}; obtain the matching reference archive.')
    written = {}
    with ZipFile(args.archive) as z:
        for member in z.namelist():
            if not member.startswith(PREFIX) or member.endswith('/'):
                continue
            name = member[len(PREFIX):]
            if name not in ['conf.gro', 'topol.top', 'index.ndx'] and not name.startswith('amber99bsc1.ff/'):
                continue
            destination = (args.out / name).resolve()
            if not destination.is_relative_to(args.out.resolve()):
                raise ValueError('Invalid archive path.')
            data = z.read(member)
            if name == 'conf.gro':
                lines = data.decode().splitlines()
                lines[0] = 'Periodic 20-base-pair DNA in SPC/E water'
                data = ('\n'.join(lines) + '\n').encode()
            elif name == 'topol.top':
                # Remove generated workstation metadata, preserving molecular records.
                lines = data.decode().splitlines()
                metadata = re.compile(r'^\s*;.*(?:/data/|/home/|By user:|On host:|At date:|Executable:|Data prefix:|Working dir:|Command line:|gmx pdb2gmx)')
                data = ('\n'.join(line for line in lines if not metadata.search(line)) + '\n').encode()
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            written[name] = hashlib.sha256(data).hexdigest()
        (args.out / 'LICENSE-source.txt').write_bytes(z.read('awh-tutorial-main/LICENSE'))
    lines = (args.out / 'conf.gro').read_text().splitlines()
    if int(lines[1]) != 9365 or not all(len(s) >= 68 for s in lines[2:9367]):
        raise ValueError('Expected 9365 atoms with retained velocities.')
    (args.out / 'model-files.json').write_text(json.dumps(written, indent=2))
    print('Prepared 20 periodic base pairs, 2688 SPC/E waters, and 40 sodium ions.')


if __name__ == '__main__':
    main()
```

After preparation, run bash run.sh in the example directory. Analyze with python analyze_dna.py --run . --out figures --language en.

The starting point is an already prepared periodic duplex, rather than a sequence beginning to fold or an experimental structure identified by a PDB entry. Its coordinate file contains both positions and velocities, and its topology supplies matching masses, charges, and connectivity. Continuing this state lets the lesson concentrate on nucleic-acid motion and analysis. A different sequence would require its own compatible structure and topology, appropriate ends or periodic connections, solvation, and preparation. Those operations change the molecular model and should be treated as part of designing a new calculation.

The first stage lasts 20 ps. At 0.002 ps per step, equivalent to 2 fs, it requires 10000 steps. The v-rescale thermostat targets 300 K with a coupling time of 0.5 ps. Parrinello–Rahman pressure coupling uses a time of 5 ps. Existing velocities are retained through `gen-vel = no`, so another initial velocity distribution is not generated. This preparation stage checks continuous evolution from the supplied state under the stated settings and saves its final state for the subsequent observation.

### Parameters for the 20 ps preparation

```
title                    = Amber NPT equilibration 
integrator               = md
dt                       = 0.002
nsteps = 10000

nstlog = 1000
nstenergy = 100
nstxout-compressed = 500

; Settings that make sure we run with parameters in harmony with the selected force-field
coulombtype              = pme
rcoulomb                 = 1.0
fourierspacing           = 0.121 ; grid spacing for FFT
;
vdwtype                  = cut-off
vdw-modifier             = potential-shift-verlet
rvdw                     = 1.0
dispCorr                 = enerpres
constraints              = h-bonds

; Pressure coupling is on
pcoupl                   = parrinello-rahman  
pcoupl-type              = semiisotropic  ; isotropic in the x and y direction, but different in the z direction  
tau_p                    = 5.0 
ref_p                    = 1.0 1.0
compressibility          = 4.5e-5 4.5e-5 
nstpcouple               = 10

; Keep system temperature fluctuating physically correct
tcoupl                   = v-rescale 
tc-grps                  = system
tau_t                    = 0.5 
ref_t                    = 300 

gen-vel                  = no
gen-temp                 = 300
gen-seed                 = -1


periodic-molecules       = yes              ; for systems with molecules that couple to themselves through the periodic boundary conditions, this requires a slower PBC algorithm and molecules are not made whole in the output.

ld-seed = 20263111
```

After preparation, run bash run.sh in the example directory. Analyze with python analyze_dna.py --run . --out figures --language en.

The second stage continues from the preparation coordinates and checkpoint for 500000 steps, giving 1 ns. A checkpoint carries state needed for continuing integration and coupling, while the coordinate file supplies the corresponding structural record. Both stages retain the same force field, water, nonbonded settings, and temperature and pressure targets. PME handles long-range electrostatics. Coulomb and van der Waals real-space cutoffs are 1.0 nm, with a dispersion correction for energy and pressure. The distinction between stages concerns preparation and observation rather than a change of molecular interactions.

### Parameters for the 1 ns unbiased record

```
title                    = Amber NPT equilibration 
integrator               = md
dt                       = 0.002
nsteps = 500000

nstlog = 1000
nstenergy = 100
nstxout-compressed = 500

; Settings that make sure we run with parameters in harmony with the selected force-field
coulombtype              = pme
rcoulomb                 = 1.0
fourierspacing           = 0.121 ; grid spacing for FFT
;
vdwtype                  = cut-off
vdw-modifier             = potential-shift-verlet
rvdw                     = 1.0
dispCorr                 = enerpres
constraints              = h-bonds

; Pressure coupling is on
pcoupl                   = parrinello-rahman  
pcoupl-type              = semiisotropic  ; isotropic in the x and y direction, but different in the z direction  
tau_p                    = 5.0 
ref_p                    = 1.0 1.0
compressibility          = 4.5e-5 4.5e-5 
nstpcouple               = 10

; Keep system temperature fluctuating physically correct
tcoupl                   = v-rescale 
tc-grps                  = system
tau_t                    = 0.5 
ref_t                    = 300 

gen-vel                  = no
gen-temp                 = 300
gen-seed                 = -1


periodic-molecules       = yes              ; for systems with molecules that couple to themselves through the periodic boundary conditions, this requires a slower PBC algorithm and molecules are not made whole in the output.

ld-seed = 20263111
continuation = yes
```

After preparation, run bash run.sh in the example directory. Analyze with python analyze_dna.py --run . --out figures --language en.

### Run the stages and export thermodynamic records

```
#!/usr/bin/env bash
set -euo pipefail
gmx=${GMX:-gmx}
"$gmx" grompp -f pilot.mdp -c conf.gro -p topol.top -n index.ndx -o pilot.tpr > pilot.grompp.log 2>&1
"$gmx" mdrun -deffnm pilot -ntmpi 1 -ntomp 2 -pin off > pilot.stdout.log 2>&1
"$gmx" grompp -f md.mdp -c pilot.gro -t pilot.cpt -p topol.top -n index.ndx -o md.tpr > md.grompp.log 2>&1
"$gmx" mdrun -deffnm md -ntmpi 1 -ntomp 2 -pin off > md.stdout.log 2>&1
printf 'Temperature
Potential
Pressure
Volume
Density
Box-X
Box-Y
Box-Z
0
' | "$gmx" energy -f md.edr -o md-properties.xvg > energy.log 2>&1
"$gmx" check -f md.xtc > trajectory-check.log 2>&1
```

After preparation, run bash run.sh in the example directory. Analyze with python analyze_dna.py --run . --out figures --language en.

After `bash run.sh`, `grompp` combines parameters, topology, coordinates, and index into a runnable TPR file, and `mdrun` advances the dynamics. The script then exports temperature, pressure, volume, and box quantities to a readable table. Coordinates are saved every 1 ps, yielding 1001 frames from 0 to 1000 ps. Energy values are saved every 0.2 ps, yielding 5001 records. These outputs have different temporal densities, and each analysis uses the time column belonging to its input.

In the actual production record, second-half temperature averages approximately 299.992 K, with a saved-record standard deviation of 3.043 K. This describes the temperature series, not the independence of every saved conformation. Other checks include atom count, increasing times, finite coordinates, and plausible lengths of the covalent connections crossing the periodic boundary. The analysis verifies the two closure bonds, between one-based atoms 1 and 632 and between atoms 633 and 1261. Their minimum-image lengths range from approximately 0.148 to 0.171 nm across the trajectory.

Atom numbers and array indices differ by one in a way worth checking explicitly. GROMACS index files start numbering at one; Python arrays start at zero. The target nitrogens are numbered 338 and 936 in the supplied index, corresponding to Python positions 337 and 935. Before calculating, the program checks that these positions really are N3 in DT11 and N1 in DA30. Verifying identity first is more informative than accepting a distance curve merely because its magnitude looks plausible.

## Resolving local motion into distance, direction, and tilt

Begin with the target N3–N1 distance. Its mean over the 1 ns record is approximately 0.29605 nm, with a saved-frame standard deviation of 0.01119 nm and a range of roughly 0.2707 to 0.3592 nm. The mean supplies a typical scale, while the time series shows how excursions develop around it. A larger value can be inspected alongside neighbouring frames, hydrogen direction, and base-ring motion. Together these reveal more than assigning a whole base pair an opening label from a single distance threshold.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/en/#en-s6)

Figure 4 · The left angle is defined at hydrogen; near 180°, donor, H, and acceptor approach collinearity. The right plane angle uses two normals and describes a different geometric relationship.

### Local motion of one base pair

N–N separation, contact direction, and ring-plane tilt use the same 1001 frames.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/en/#en-s6)

Distance, D–H–A angle and local base-plane angle for the selected DT11–DA30 contact, using minimum-image geometry in the triclinic cell.

The second curve measures the N3–H3–N1 angle. Its vertex is H3, with vectors directed from H3 toward the donor N3 and acceptor N1. An angle near 180° places the three atoms close to a straight line. The recorded angle averages approximately 165.92°, with a standard deviation of 7.29°. Similar nitrogen separations can occur with different hydrogen directions, which is why both measurements are useful. Each point in the distance–angle scatter plot retains the paired observations from one actual frame.

Using a donor–acceptor distance no greater than 0.35 nm and a donor–H–acceptor angle no smaller than 150°, 974 of the 1001 frames pass both conditions. The resulting geometric contact fraction is 97.3027%. It refers to the selected atoms and the observed trajectory. An A–T pair contains other contacts, and base opening also involves stacking, solvent exposure, and broader conformational changes. A single-contact fraction and a base-pair opening probability are consequently different observables. A precise definition lets us add further contacts or solvent measurements when the research question requires them.

A contact fraction from an explicit geometric ruleEq. 2

![A contact fraction from an explicit geometric rule](https://ml-biomat.com/static/agent-math/89e25a33e369aa65f080c794.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| f | Fraction of saved frames satisfying both conditions | dimensionless |
| M、k | Total saved frames and frame index | dimensionless |
| dₖ、dc | Donor–acceptor distance in frame k and its cutoff | nm |
| θₖ、θc | Donor–H–acceptor angle and its lower threshold | ° |
| 1[ ]、∑、≤、≥、and | Indicator: one if all conditions hold, zero otherwise; sum; no greater than; no less than; logical conjunction | operators |
| =、+、−、/、× | Equality, addition, subtraction, division, and multiplication; a fraction bar also means division. | operators |

Reading the relationshipCheck distance and direction for the same atoms in every frame, then divide the passing count by the number of frames.

A worked exampleAt dc=0.35 nm and θc=150°, 974/1001=0.973027, or 97.3027%. A 0.30 nm separation at 165° passes; the same separation at 135° does not.

ConditionsThis measures the geometry of the DT11:N3–H3 to DA30:N1 contact over the stated trajectory. Saved frames are temporally correlated.

### Distribution of a local contact

The half-trajectories share bin edges; the scatter plot retains paired distance and angle observations.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/en/#en-s6)

Joint distance and directional distribution across the same 1001 frames; the geometrical rule defines this specific contact.

A frequently observed contact and a long-lived contact answer different questions. Two records may both satisfy a criterion in ninety percent of their frames, yet one may contain many brief departures and the other one prolonged departure. Their fractions agree while their temporal organization differs. A lifetime analysis retains consecutive intervals of contact and loss and specifies how to handle events shorter than the 1 ps saving interval. The fraction reported here directly answers how many saved observations satisfy the chosen geometry.

The third curve compares two base-ring planes. Fit a plane to the atoms of each six-membered ring and find a unit vector perpendicular to it, called its normal. The dot product of two unit normals gives the cosine of their angle. A fitted plane has two equally valid, opposite normal directions, so the absolute dot product removes this arbitrary sign. The resulting plane angle averages approximately 11.32° in the reference trajectory. It shows continuing relative tilt of the two rings alongside fluctuations in their central contact.

Comparing the tilt of two base-ring planesEq. 3

![Comparing the tilt of two base-ring planes](https://ml-biomat.com/static/agent-math/a397f68bcc9f396532fcba61.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| β | Angle between unoriented planes, from 0 to 90° | ° |
| n̂₁、n̂₂ | Unit vectors normal to the fitted ring planes | dimensionless |
| ·、\| \|、arccos | Dot product; absolute value; inverse cosine, converted to degrees | operators |
| 1、2 | Labels of the two base-ring planes | dimensionless |
| =、+、−、/、× | Equality, addition, subtraction, division, and multiplication; a fraction bar also means division. | operators |

Reading the relationshipA plane admits two opposite normal directions. The absolute dot product removes that arbitrary sign before converting the cosine into an angle.

A worked exampleNormals (0,0,1) and (0.6,0,0.8) have dot product 0.8, giving β≈36.87°. Reversing the second normal leaves the plane angle unchanged.

ConditionsThe program fits the two six-membered rings in the supplied index. This plane angle is distinct from convention-specific DNA opening, twist, or helical parameters.

This plane angle should be distinguished from specialized DNA helical parameters. It compares orientations of two planes over a range from 0 to 90°. It does not specify whether a base rotates toward the major or minor groove, nor does it measure the twist between neighbouring base pairs. A full decomposition into opening, shear, stretch, and twist requires defined local coordinate systems. Starting with transparent geometric quantities helps explain which additional directional information those more specialized parameters provide.

The interaction below uses the same 1001 actual observations while changing the classification rule. Tightening the distance cutoff or raising the minimum angle reduces the selected region; relaxing them includes more points. The underlying coordinates remain fixed. For comparisons between physical systems, apply the same rule so that contact fractions share a meaning. When examining sensitivity to the rule itself, display the threshold and result together, as the interaction does here. This separates the choice of measurement from a change in molecular behaviour.

Compare contact definitions using the same 1001 saved frames.

Static interaction based on the actual 1001 frames. Changing thresholds reclassifies the same observations; arrow keys operate the sliders.

GROMACS can also read the same atomic distance independently. The command below explicitly disables whole-molecule reconstruction while retaining periodic distance handling, which suits the continuously connected backbone. Its values agree with the Python minimum-image calculation within the numerical precision written to the output file. The comparison works because both methods use the same atoms and cell geometry. Comparing an atomic distance with a base-centre distance would first compare different measurement definitions, even if both curves appeared physically reasonable.

### Read the same distance with GROMACS

```
gmx distance -s md.tpr -f md.xtc -select "atomnr 338 plus atomnr 936" -normpbc -pbc -oall target-distance.xvg
```

Disable whole-molecule reconstruction while retaining periodic minimum-image distances for this self-connected backbone.

## Reading distributions and environmental changes

A time series retains temporal order. A histogram asks a different question: which distances occur more often? Divide the distance axis into intervals, count the frames in each, and normalize by both total frames and interval width to obtain probability density. Its unit is nm⁻¹. A histogram height can exceed one because interval probability is height multiplied by width. Checking the units is a useful way to distinguish a plot of counts, fractions, and probability density before interpreting its peaks.

Reading probability from a distance histogramEq. 4

![Reading probability from a distance histogram](https://ml-biomat.com/static/agent-math/0c697a54b2064d3c9e2b3da0.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| pj | Probability density in distance bin j | nm⁻¹ |
| Nj | Number of frames in bin j | dimensionless |
| M | Total frames used for that histogram | dimensionless |
| Δd | Distance-bin width | nm |
| Pj | Fraction of frames in the bin | dimensionless |
| j、Δ | Bin index; interval width | dimensionless; operator |
| =、+、−、/、× | Equality, addition, subtraction, division, and multiplication; a fraction bar also means division. | operators |

Reading the relationshipDivide the count by total frames to obtain an interval fraction, then divide by bin width for density. Height times width recovers interval probability.

A worked exampleIf 50 of 500 frames lie in a 0.01 nm bin, density is 10 nm⁻¹ and interval probability is 0.10. A density exceeding one is compatible with probability no greater than one.

ConditionsBoth half-trajectories use identical bin edges and normalize separately by 500 or 501 frames. The comparison concerns sampled local-distance distributions.

Here the two intervals are 0≤t<500 ps and 500≤t≤1000 ps, containing 500 and 501 frames. They use identical distance-bin edges and have means of approximately 0.29484 and 0.29725 nm. Their main regions are similar while tail and shape differences remain visible. These adjacent intervals belong to one continuous history, so their comparison measures sensitivity to the observation window. Independent repeats require separate velocity and random histories under the same physical protocol, allowing variation between repeated calculations to be examined.

The same central-distance measurement can be extended along the 20 base pairs. The program orders residues on the first strand and matches them to the reverse order of the second, selecting the relevant N1 or N3 for every pair. The resulting position–time map retains time horizontally, pair position vertically, and minimum-image distance as colour. It locates the target A–T pair within the surrounding G–C pairs. The colour scale ends at the pooled 99.5th percentile to reveal the main fluctuations. Values above it use the upper colour, while all distances remain available in the CSV.

### Inspecting 20 positions along the duplex

Colour denotes central N–N minimum-image distance. The upper triangle marks values beyond the display scale; the full data are retained.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/en/#en-s7)

Framewise central N–N minimum-image distances for all 20 base pairs; the upper colour-bar triangle marks values beyond the display range.

The ionic environment also changes. For each Na⁺, calculate its shortest distance to all nonbridging phosphate oxygens named O1P and O2P. Count that ion as a neighbour when this distance is at most 0.35 nm. Even if a sodium is close to two oxygens, it contributes only once in a frame. Across the actual record, the neighbour count averages approximately 3.216, with a standard deviation of 1.825 and a range from zero to nine. All 40 counterions remain in the periodic system; a lower neighbour count places more of them outside this particular region.

This spatial count neither fixes an ion to a site nor introduces a new covalent bond. A residence-time question needs ion identities and a record of entry, exit, and return, together with a rule for brief threshold crossings. A salt-concentration question needs matched populations of cations and anions in addition to the ions required for charge neutrality. The present sodium population primarily defines the counterion environment of negatively charged DNA. Keeping that distinction explicit guides the choice of a meaningful comparison system.

### Axial repeat and neighbouring ions

A sodium is counted once per frame when within 0.35 nm of any nonbridging phosphate oxygen.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/g11/en/#en-s7)

Native cell vectors determine axial repeat and volume; each Na⁺ is counted once per frame when within 0.35 nm of any nonbridging phosphate oxygen.

The axial repeat is shown alongside the ionic record. Its mean is approximately 6.579 nm, and mean cell volume is approximately 90.379 nm³. Both vary with molecular motion and pressure coupling. Dividing axial length by 20 gives an average axial length per repeating pair position; the rise at a particular base step requires local structural analysis. Shared time axes help identify changes worth investigating together. Establishing a causal explanation then calls for controlled variations, repeated calculations, and measurements that address the proposed molecular mechanism.

### Complete Python: pairing, directions, ions, and cell geometry

```
"""Analyze the periodic duplex with full triclinic minimum-image geometry.

Run: python analyze_dna.py --run . --out figures --language en
Dependencies: MDAnalysis 2.11, NumPy 2.5, Matplotlib 3.11.
Atom numbers in the index file are one-based; Python indices are zero-based.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import MDAnalysis as mda
from MDAnalysis.lib.distances import calc_bonds, calc_angles, distance_array, minimize_vectors
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


def index_groups(path):
    groups = {}; current = None
    for raw in path.read_text().splitlines():
        line = raw.split(';', 1)[0].strip()
        if line.startswith('['):
            current = line.strip('[] ').strip(); groups[current] = []
        elif line and current:
            groups[current].extend(int(x) - 1 for x in line.split())
    return {k: np.array(v, dtype=int) for k, v in groups.items()}


def one_atom(residue, name):
    atoms = residue.atoms.select_atoms('name ' + name)
    if len(atoms) != 1:
        raise ValueError(f'Expected one {name} in residue {residue.resid}')
    return atoms[0].index


def ring_normal(points, box):
    # Each ring is smaller than the cell. Reconstruct this local object only.
    local = minimize_vectors(points - points[0], box)
    _, _, vh = np.linalg.svd(local - local.mean(axis=0))
    return vh[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', type=Path, default=Path('.'))
    ap.add_argument('--out', type=Path, default=Path('figures'))
    ap.add_argument('--language', choices=['zh', 'en'], default='en')
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    tr = lambda zh, en: zh if args.language == 'zh' else en
    available = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in ['Microsoft YaHei', 'Noto Sans CJK SC', 'Source Han Sans SC', 'WenQuanYi Zen Hei', 'DejaVu Sans'] if f in available]
    plt.rcParams.update({'font.family': fonts if args.language == 'zh' else ['DejaVu Sans'],
                         'font.size': 12, 'axes.spines.top': False, 'axes.spines.right': False,
                         'figure.facecolor': '#f8f7f2', 'axes.facecolor': '#f8f7f2',
                         'svg.fonttype': 'path'})
    u = mda.Universe(str(args.run / 'md.tpr'), str(args.run / 'md.xtc'))
    groups = index_groups(args.run / 'index.ndx')
    target = np.concatenate([groups['base_N1orN3'], groups['partner_N1orN3']])
    identities = [(a.resname, int(a.resid), a.name, int(a.index)) for a in u.atoms[target]]
    if identities != [('DT', 11, 'N3', 337), ('DA', 30, 'N1', 935)]:
        raise ValueError('Target must be the supplied thymine N3 and adenine N1.')
    dna = u.select_atoms('nucleic'); segments = dna.segments
    if len(segments) != 2 or [len(s.residues) for s in segments] != [20, 20]:
        raise ValueError('Expected two 20-residue periodic strands.')
    pair_residues = list(zip(segments[0].residues, segments[1].residues[::-1]))
    pairs = np.array([[one_atom(a, 'N1' if a.resname in ['DA', 'DG'] else 'N3'),
                       one_atom(b, 'N1' if b.resname in ['DA', 'DG'] else 'N3')]
                      for a, b in pair_residues])
    hydrogen = one_atom(u.atoms[target[0]].residue, 'H3')
    phosphorus_oxygen = dna.select_atoms('name O1P O2P')
    ions = u.select_atoms('resname NA')
    closure = []
    for strand in segments:
        first = one_atom(strand.residues[0], 'P')
        last = one_atom(strand.residues[-1], "O3'")
        if not any(set(b.indices) == {first, last} for b in strand.atoms.bonds):
            raise ValueError('Missing cross-boundary covalent closure.')
        closure.append([first, last])
    closure = np.array(closure)
    times = []; distances = []; angles = []; tilt = []; cells = []; counts = []; bonds = []
    for ts in u.trajectory:
        if not np.isfinite(ts.positions).all():
            raise ValueError('Non-finite trajectory coordinate.')
        box = ts.dimensions
        if not np.allclose(box[3:5], 90, atol=.01) or not np.isclose(box[5], 60, atol=.01):
            raise ValueError('This reference model uses a 60-degree cell in xy.')
        times.append(float(ts.time))
        distances.append(calc_bonds(u.atoms[pairs[:, 0]].positions,
                                    u.atoms[pairs[:, 1]].positions, box=box) / 10)
        angles.append(float(np.degrees(calc_angles(u.atoms[target[0]].position,
                      u.atoms[hydrogen].position, u.atoms[target[1]].position, box=box))))
        n1 = ring_normal(u.atoms[groups['base_6ring']].positions, box)
        n2 = ring_normal(u.atoms[groups['partner_6ring']].positions, box)
        tilt.append(float(np.degrees(np.arccos(np.clip(abs(np.dot(n1, n2)), 0, 1)))))
        cells.append(ts.triclinic_dimensions.copy() / 10)
        d = distance_array(ions.positions, phosphorus_oxygen.positions, box=box) / 10
        counts.append(int(np.sum(np.min(d, axis=1) <= .35)))
        bonds.append(calc_bonds(u.atoms[closure[:, 0]].positions,
                               u.atoms[closure[:, 1]].positions, box=box) / 10)
    t = np.array(times); d = np.array(distances); theta = np.array(angles)
    beta = np.array(tilt); h = np.array(cells); nc = np.array(counts); bc = np.array(bonds)
    if np.any(np.diff(t) <= 0) or bc.max() > .2:
        raise ValueError('Invalid time order or closure-bond geometry.')
    target_column = int(np.where(np.all(pairs == target, axis=1))[0][0])
    dt = d[:, target_column]
    hb = (dt <= .35) & (theta >= 150)
    halves = [t < 500, t >= 500]
    volume = np.linalg.det(h)
    summary = {
        'atoms': len(u.atoms), 'dna_atoms': len(dna), 'nucleotides': len(dna.residues),
        'base_pairs': len(pairs), 'waters': len(u.select_atoms('resname SOL').residues),
        'sodium_ions': len(ions), 'frames': len(t), 'time_ps': [float(t[0]), float(t[-1])],
        'target_one_based_atom_numbers': (target + 1).tolist(),
        'target_residues': ['DT11:N3', 'DA30:N1'],
        'target_distance_nm': {'mean': float(dt.mean()), 'sd': float(dt.std()),
                               'min': float(dt.min()), 'max': float(dt.max())},
        'target_angle_deg': {'mean': float(theta.mean()), 'sd': float(theta.std())},
        'ring_plane_tilt_deg': {'mean': float(beta.mean()), 'sd': float(beta.std())},
        'central_hbond_geometry_fraction': float(hb.mean()),
        'criterion': 'T:N3-to-A:N1 <=0.35nm and T:N3-H3-A:N1 angle>=150deg',
        'halves': [{'time_ps': [0, 500] if j == 0 else [500, 1000],
                    'frame_count': int(mask.sum()), 'distance_mean_nm': float(dt[mask].mean()),
                    'hbond_geometry_fraction': float(hb[mask].mean())}
                   for j, mask in enumerate(halves)],
        'na_within_035nm_phosphate_oxygen': {'mean': float(nc.mean()), 'sd': float(nc.std()),
                                            'min': int(nc.min()), 'max': int(nc.max())},
        'closure_bonds_one_based': (closure + 1).tolist(),
        'closure_bond_range_nm': [float(bc.min()), float(bc.max())],
        'cell_first_nm': h[0].tolist(), 'volume_mean_nm3': float(volume.mean()),
        'axial_repeat_mean_nm': float(h[:, 2, 2].mean()),
        'mean_central_distance_by_pair_nm': d.mean(axis=0).tolist(),
        'sequence_strand_A': ''.join(r.resname[-1] for r in segments[0].residues),
        'sequence_strand_B': ''.join(r.resname[-1] for r in segments[1].residues),
        'definitions': 'Full triclinic minimum images; ring-plane angle ignores normal sign. '
                       'Hydrogen-bond fraction is one stated geometric contact, not opening probability. '
                       'Neighbour counts count each sodium once. Adjacent frames are correlated.'}
    (args.out / 'dna_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    np.savetxt(args.out / 'dna_timeseries.csv', np.column_stack([t, dt, theta, beta, hb, h[:, 2, 2], volume, nc, bc]),
               delimiter=',', header='time_ps,target_distance_nm,DHA_angle_deg,plane_tilt_deg,hbond_geometry,axial_repeat_nm,volume_nm3,Na_near_phosphate,closure_A_nm,closure_B_nm', comments='')
    np.savetxt(args.out / 'dna_pair_distances.csv', np.column_stack([t, d]), delimiter=',',
               header='time_ps,' + ','.join('pair_' + str(i + 1) + '_nm' for i in range(20)), comments='')
    def save(fig, name):
        for ext in ['svg', 'png']:
            fig.savefig(args.out / f'{name}.{ext}', dpi=170, bbox_inches='tight')
        plt.close(fig)
    colors = ['#147d85', '#c46938', '#4c78b5']
    fig, ax = plt.subplots(3, 1, figsize=(11, 9), sharex=True, layout='constrained')
    for axis, values, label, col in zip(ax, [dt, theta, beta],
                [tr('N3—N1距离 / nm', 'N3–N1 distance / nm'),
                 tr('N3—H3—N1角 / °', 'N3–H3–N1 angle / °'),
                 tr('两碱基环平面夹角 / °', 'Angle between base-ring planes / °')], colors):
        axis.plot(t, values, lw=.75, color=col); axis.set_ylabel(label)
    ax[0].set_title(tr('同一A—T碱基对的三种局部测量', 'Three local measurements of the same A–T pair'))
    ax[-1].set_xlabel(tr('时间 / ps', 'Time / ps')); save(fig, 'dna-local-motion')
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5), layout='constrained')
    edges = np.linspace(dt.min() - .0001, dt.max() + .0001, 30)
    for i, mask in enumerate(halves):
        ax[0].hist(dt[mask], bins=edges, density=True, histtype='step', lw=2, color=colors[i],
                   label=['0 ≤ t < 500 ps', '500 ≤ t ≤ 1000 ps'][i])
    ax[0].legend(fontsize=10,loc='upper center',bbox_to_anchor=(.5,-.19),ncol=2); ax[0].set(xlabel=tr('N3—N1距离 / nm', 'N3–N1 distance / nm'),
             ylabel=tr('概率密度 / nm⁻¹', 'Probability density / nm⁻¹'),
             title=tr('相邻半段采用同一组距离箱', 'Common bins for adjacent half-trajectories'))
    ax[1].scatter(dt, theta, s=8, alpha=.4, color=colors[0]); ax[1].axhline(150, ls='--', c=colors[1])
    ax[1].set(xlabel=tr('N3—N1距离 / nm', 'N3–N1 distance / nm'), ylabel=tr('供体—氢—受体角 / °', 'Donor–H–acceptor angle / °'),
             title=tr('距离与方向共同描述接触', 'Distance and direction describe a contact'))
    save(fig, 'dna-contact-distribution')
    fig, ax = plt.subplots(figsize=(11, 6), layout='constrained')
    im = ax.pcolormesh(t, np.arange(1, 21), d.T, shading='nearest', cmap='viridis',
                      vmin=float(d.min()), vmax=float(np.quantile(d, .995)))
    ax.set_yticks(np.arange(1, 21)); ax.set(xlabel=tr('时间 / ps', 'Time / ps'),
                   ylabel=tr('第一条链的配对位置', 'Pair position on strand A'),
                   title=tr('20对碱基的中心N—N距离', 'Central N–N distances across 20 base pairs'))
    fig.colorbar(im, ax=ax, label=tr('最小镜像距离 / nm', 'Minimum-image distance / nm'), extend='max')
    save(fig, 'dna-pair-map')
    fig, ax = plt.subplots(3, 1, figsize=(11, 8), sharex=True, layout='constrained')
    ax[0].plot(t, h[:, 2, 2], color=colors[0], lw=1); ax[0].set_ylabel(tr('轴向周期长度 / nm', 'Axial repeat / nm'))
    ax[1].plot(t, volume, color=colors[1], lw=1); ax[1].set_ylabel(tr('盒体积 / nm³', 'Cell volume / nm³'))
    ax[2].plot(t, nc, color=colors[2], lw=.8); ax[2].set_ylabel(tr('磷酸氧近邻Na⁺数', 'Na⁺ near phosphate O')); ax[2].set_ylim(0, max(10,int(nc.max())+1))
    ax[2].set_xlabel(tr('时间 / ps', 'Time / ps')); ax[0].set_title(tr('轴向约束与离子环境随轨迹一同记录', 'Axial geometry and ionic environment along the trajectory'))
    save(fig, 'dna-cell-ions')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
```

After preparation, run bash run.sh in the example directory. Analyze with python analyze_dna.py --run . --out figures --language en.

## Matching the model to the biological question

The calculation now supports a precise question: how does the local geometry of one A–T pair fluctuate within a continuous, periodically connected duplex in water and a counterion environment? That question matches the starting coordinates, connectivity, and 1 ns observation. End stability of a short DNA recognition element instead calls for a finite duplex with defined terminal chemistry. Bending of a connector in a DNA material needs enough length and appropriate junctions for the intended deformation to occur. Choosing the object and its boundaries comes before choosing a convenient analysis command.

A base-opening free-energy calculation requires sampling that connects closed and opened configurations. One can select a physically meaningful coordinate, use enhanced sampling to promote exploration, and then inspect coverage, time dependence, and independent repeats. The present unbiased record develops familiarity with local motion in the paired state and helps identify useful coordinates. These activities form a coherent sequence: understand the coordinate and its molecular meaning, design sampling across relevant regions, then calculate the distribution or free energy required by the question.

Biological recognition also combines sequence and environment. Similar central distances do not guarantee that two sequences present the same interaction surface to a protein. Groove shape, charge distribution, neighbouring bases, and solvent exposure can all matter. A controlled starting design can hold temperature, water, ions, and boundaries fixed while changing one sequence position, then compare the same local and environmental observables. Adding a protein or ligand later can build on this defined structural reference rather than mixing several changes at once.

One exercise can be completed with the existing data: vary both the distance and angle cutoffs, record the contact fraction, and compare the response of the two half-trajectories. A second exercise selects a nearby G–C pair, identifies the correct donor hydrogen and acceptor from its chemistry, and then reuses the measurement approach. The exercises emphasize different decisions. The first changes a classification rule; the second changes the object being measured. Each therefore requires its own checks before the resulting numbers are compared.

The familiar double helix can now be read as a moving molecular structure. Covalent connectivity maintains the backbone, base contacts and stacking organize local conformations, solvent and counterions form the environment, and periodic geometry defines the permitted global continuation. Distances, directions, plane angles, and distributions make parts of that motion understandable. When studying glycans, protein recognition, or nucleic-acid materials, the same sequence of reasoning remains useful: define the molecular object and its connections, then choose observables, spatial scales, and sampling appropriate to it.

## Further Reading and Open Materials

- [Calculating PMFs with AWH in GROMACS](https://tutorials.gromacs.org/docs/awh-tutorial.html) · Viveca Lindahl; reviewed and updated by Alessandra Villa and Christian Blau · CC BY 4.0

  Periodic DNA model, unbiased MD settings, and target-base atom indices.

  Retains the model with 20 ps preparation and a 1 ns unbiased record; expands foundational explanations, local geometry, and ionic analysis.
- [Sequence dependency of canonical base pair opening in the DNA double helix](https://doi.org/10.1371/journal.pcbi.1005463) · Viveca Lindahl, Alessandra Villa, Berk Hess · CC BY

  Parmbsc1 implementation and the research context for local base contacts.
- [The story behind Photograph 51](https://www.kcl.ac.uk/the-story-behind-photograph-51) · Brian Sutton, King’s College London

  History of Franklin and Gosling’s diffraction and hydration work; the historical principle diagram is newly drawn.
- [GROMACS periodic-molecules and pressure coupling](https://manual.gromacs.org/documentation/2026.4/user-guide/mdp-options.html#mdp-periodic-molecules)
- [gmx distance](https://manual.gromacs.org/documentation/current/onlinehelp/gmx-distance.html)
- [MDAnalysis distance functions](https://docs.mdanalysis.org/stable/documentation_pages/lib/distances.html)
