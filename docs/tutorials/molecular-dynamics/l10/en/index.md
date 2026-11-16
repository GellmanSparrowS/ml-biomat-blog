# Stretching and Relaxation: Reading Mechanics from Molecules

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l10/en/
Language: en

Connect prescribed cell deformation with network stress, strand orientation and adjustment at fixed strain.

## What continues after stretching stops?

Stretch an elastic band, hold your hands at a fixed separation, and consider the force needed to maintain that length. Even after the separation is fixed, the material can continue to adjust internally. A hydrogel dressing attached to a moving joint, an elastic seal under prolonged compression and a stretched piece of soft tissue all raise related questions. Once the external shape has been prescribed, do internal strands continue moving, and how does the transmitted force change with time? This lesson turns that question into an observable molecular simulation. We change the shape of a periodic cell, then hold it fixed while recording chain conformations and mechanical statistics.

The previous lesson prepared three connection levels in the same bead–spring model. Each system contains 1,600 equal-mass beads and eighty original chains of twenty beads, with zero, eighty or 160 added permanent links. Three independently prepared configurations are available for each condition. We continue from those actual systems, keeping their connectivity, local structure and mechanical records linked to one another. The zero-added-link systems undergo the same loading. They show how densely packed chains can respond over a finite loading interval through their motion and interactions even when permanent interchain bonds are absent. The comparison thus retains both the network cases and their unlinked counterparts.

Force and stress are also easy to confuse. Force describes the overall pull on a specimen, while stress distributes that action over an area. The same force applied to a thin thread and a thick cord gives different loads per unit area. Material comparison therefore needs to separate specimen dimensions from the response being studied. The global simulation pressure tensor is already normalized by cell volume and differs from the force on one bead. We begin with the geometry and average mechanical action of the whole material, then return to strands to explain their origin. This connects with experimental measurements while distinguishing a large instantaneous microscopic force from a property of the entire network.

Stretching first specifies an operation, rather than a material law. We must choose the loading direction, rate, transverse response and temperature control. A long experimental specimen with free side surfaces can become thinner naturally. A periodic cell has no surrounding free surface, so its transverse dimensions must be controlled explicitly. Here the x length increases to 1.2 times its initial value, while the y and z lengths shrink by the same factor to preserve volume. This separates shape change from density change and provides a useful exercise for an approximately incompressible network. A study of volume change during extension would instead choose transverse conditions appropriate to that question.

The measured quantities also need definitions before we interpret them. A trajectory describes bead arrangements, cell lengths specify deformation, and the pressure tensor provides directional mechanical information. Placing them on a common time axis separates loading from the subsequent hold. We begin with a length ratio that can be checked by hand, then introduce strain, transverse contraction, the tensile normal-stress difference, chain orientation and time averaging. Stress fluctuates appreciably in these small systems, so all three configurations remain visible. Understanding those fluctuations together with the structural signal is part of turning a stretching command into an interpretable comparison of materials.

## From force and length to thermal motion and chain shape

A spring is an intuitive picture of elasticity: separating its ends requires a restoring force. That picture helps explain local bond extension, but a polymer network contains another structural level. A coiled strand can change its bends and orientation, increasing its end separation without greatly lengthening every chemical bond. Slowly extending a loosely arranged string of beads makes this distinction visible. Overall network deformation is shared among changes in strand direction, conformation and local distances. We therefore record both local bond alignment and the size of each original chain in the three coordinate directions. Looking only at the longest bond would miss much of the adjustment occurring on larger scales.

A second historical route into elasticity connects deformation with heat. John Gough published a study of natural rubber in 1805, and Joule’s 1859 paper, On Some Thermo-Dynamic Properties of Solids, placed mechanical change and thermal effects within one investigation. Early experiments worked with materials that could be held, loaded and measured thermally. Molecular simulation now adds a view of the internal chains. The diagram connects these levels of observation: length, force and temperature on one side, and the range of strand conformations on the other. This relationship brings temperature and conformational statistics into the discussion of recovery in rubber and gels.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/en/#en-s2)

Figure 1 · Elasticity studies connect external loading, dimensions and temperature; the molecular view additionally follows internal chain conformations. Left: a conceptual arrangement of these observables.

In a modern molecular picture, a flexible strand with nearby endpoints usually has many possible coiled conformations. Separating the endpoints restricts that set. Thermal motion continually explores the available shapes, so their statistical abundance contributes to the average restoring tendency. This provides an entry point to conformational entropy: here entropy concerns the number of microscopic arrangements compatible with constraints, rather than whether a picture looks tidy. A real network also involves repulsion, fluctuating junctions and finite extensibility. The FENE bead–spring model retains spring energy, bead repulsion and thermal motion together, allowing us to examine how an overall dimensional change is distributed between local bonds and chain conformations.

Temperature control must consequently be stated together with the loading protocol. During constant-temperature extension, a bath exchanges energy with the system so that chains move in a specified thermal environment. Studying heating during rapid deformation requires a corresponding energy-exchange protocol and temperature measurement. We maintain a Langevin bath at T*=1 with a damping time of 1τ and study the structural and mechanical response in that environment. The temperature record checks whether the motion statistics fluctuate around the target, while chain-shape records describe the evolving internal structure. These observations answer complementary questions: a settled temperature does not by itself describe the progress of structural adjustment.

Timescale determines how much opportunity these internal changes have to occur. Local bond vibrations are usually faster than whole-chain shape changes, and longer strands between junctions can require still more time to rearrange. Imagine extending a loose collection of cords rapidly and then slowly; the slower operation gives the cords more opportunity to adjust their positions. In a molecular system, thermal motion continually supplies microscopic movement for such rearrangement. The same final length can consequently be reached at different rates and leave different structures and stresses. Reporting the loading duration beside the stretch ratio makes this available adjustment time part of the experimental description.

## Calculating strain from recorded cell lengths

Choose the length at the start of loading as a reference. If the x dimension grows from ten length units to twelve, its stretch ratio is twelve divided by ten, or 1.2. Engineering strain is the increase of two units divided by the original ten, giving 0.2. Strain has no length unit because numerator and denominator use the same unit. This makes specimens of different sizes comparable: a change from two to 2.4 millimetres has the same engineering strain as a change from two to 2.4 centimetres. Their absolute elongations differ, but the relative geometrical change can be discussed on a common scale.

Stretch, engineering strain and Hencky strainEq. 1

![Stretch, engineering strain and Hencky strain](https://ml-biomat.com/static/agent-math/fffc4df63ffaf3521633a239.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| λ | Stretch ratio along x | 1 |
| Lₓ | Current x cell length | σ |
| Lₓ₀ | Reference x length at the start of loading | σ |
| e | Engineering strain relative to the initial length | 1 |
| h | Logarithmic or Hencky strain | 1 |
| ln | Natural logarithm of the positive dimensionless stretch | 1 |
| =, /, −, 1 | Equality, division, subtraction and the constant one; subscript 0 denotes the reference state | 1 |

Reading the relationshipThe length ratio gives relative size, subtracting one gives extension relative to the original length, and its logarithm accumulates infinitesimal changes relative to the current length.

A worked exampleFor a reference length 10σ and current length 12σ, λ=1.2, e=0.2 and h=ln1.2≈0.182322.

ConditionsLengths are positive. This example loads along fixed x and uses the cell length at loading onset as its reference.

Another common measure is logarithmic, or Hencky, strain. It accumulates small extensions relative to the current length and gives the natural logarithm of the stretch ratio. At a stretch of 1.2, engineering strain is 0.2 and Hencky strain is about 0.1823. They are close at small deformation and diverge increasingly at larger deformation. Simulation inputs likewise distinguish constant engineering strain rate from constant logarithmic strain rate. The former makes length grow linearly with time; the latter continually multiplies the current length. Our scale setting specifies a final box length reached through a linear x-length ramp, so it corresponds to a constant engineering strain rate.

Transverse contraction follows directly from volume conservation. The volume of an orthogonal cell is the product of its three lengths. If x grows by a factor λ and both y and z change by a factor a, the volume ratio is λ times a squared. Preserving volume sets that product to one, giving a=λ to the power −1/2. At λ=1.2, each transverse length becomes about 0.9129 of its initial value, and the transverse area becomes five-sixths of its original value. This contraction is an imposed geometrical condition. Allowing transverse pressure to relax to a target value defines a different experiment, selected according to the material’s lateral constraints.

Constant volume with symmetric transverse contractionEq. 2

![Constant volume with symmetric transverse contraction](https://ml-biomat.com/static/agent-math/402c2fd71657a1d7748c5376.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Lᵧ, L𝓏 | Current transverse cell lengths | σ |
| Lᵧ₀, L𝓏₀ | Reference transverse cell lengths | σ |
| λ | Axial stretch ratio | 1 |
| V, V₀ | Current and reference cell volumes | σ³ |
| J | Volume ratio | 1 |
| −1/2 | Reciprocal square root | 1 |
| =, /, 1 | Equality, division and the constant one; adjacent quantities multiply | 1 |

Reading the relationshipThe volume of an orthogonal cell is the product of its lengths. With equal transverse scaling, axial stretch times the square of that scaling must equal one.

A worked exampleAt λ=1.2, each transverse ratio is 1/√1.2≈0.912871, giving volume ratio 1.2×0.912871²≈1.

ConditionsThis is the imposed constant-volume protocol with equal relative transverse scaling and a preserved y/z aspect ratio.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/en/#en-s3)

Figure 2 · For constant-volume loading, the axial stretch is λ and each transverse ratio is λ to the power −1/2.

[Figure: Changing cell geometry](https://ml-biomat.com/tutorials/molecular-dynamics/l10/en/#en-s3)

Geometrical mapping: all three initial lengths are 10σ; points retain their fractional positions.

Compare two transverse constraints at one axial stretch and inspect area, volume and strain definitions.

The simulation holds the original box for 100τ, increases the x length from a factor of one to 1.2 over the next 100τ, and then holds the deformed box for another 100τ. Its engineering strain rate during loading is therefore 0.2 divided by 100τ, or 0.002 per τ. Actual outputs record the box lengths, from which the analysis calculates stretches and checks their product. This goes beyond reading the input alone: the input specifies the target, while the output records the geometry used at each observation. Times 100τ and 200τ mark the beginning and end of loading throughout the structural and mechanical comparisons.

A simple comparison helps make strain rate concrete. Keep the final increase at twenty percent but extend the loading duration from 100τ to 200τ, and the engineering strain rate is halved. Final geometry is unchanged, while the time available for strand adjustment during loading doubles. This comparison targets rate dependence. Changing final extension, chain length and temperature together would require further comparisons to distinguish their contributions. A useful study can first fix material structure and thermal conditions, then vary a specified loading condition. The horizontal axis follows the question as well: strain compares different loading rates at matched deformation, while elapsed time after loading describes a hold.

## Loading a periodic cell and moving its particles

The central command is fix deform. Its x scale 1.2 setting specifies the final x length, while y volume and z volume jointly preserve volume through transverse contraction. The remap x option maps particle positions to the changing box geometry whenever the cell updates. Here x names the coordinate-remapping option; positions are transformed in every direction changed by the box, rather than merely translated along x. The box changes about its centre, and fractional particle positions follow the geometrical mapping at that instant. Forces and thermal motion then continue to move beads relative to that uniform transformation, producing local rearrangement.

Applying the same linear geometrical transformation to all positions is called affine deformation. Imagine drawing points on flexible graph paper and stretching the paper: the points move with its grid. A molecular system additionally has forces between those points, allowing further rearrangement after each mapping. This solid-style loading differs from establishing a continuous flow velocity field. The remap x option changes positions without directly adding the box-motion velocity to each particle velocity. A fluid-viscosity calculation under sustained shear requires compatible velocity treatment, a definition of thermal motion and a suitable nonequilibrium integration scheme. The next lesson discusses those requirements in the context of flow.

Periodic loading also changes the meaning of specimen ends. There are no laboratory grips inside the cell and no nearly immobilized clamped regions; deformation is imposed by changing the geometry of the repeating unit. This is useful for examining chain alignment, stress and rearrangement in a homogeneous bulk environment. Questions about stress concentrations near grips, thinning at a free surface or a crack tip require those geometries and boundaries to be built into the system. With these cases distinguished, the purpose of the periodic cell becomes clear: a finite number of beads represents a portion of continuous material, focusing the calculation on prescribed bulk deformation and molecular structure.

### Complete preparation–extension–hold input

```
units lj
atom_style bond
boundary p p p
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
bond_style fene
pair_style lj/cut 1.122462048309373
pair_modify shift yes
read_data network.data
bond_coeff * 30.0 1.5 1.0 1.0
pair_coeff * * 1 1 1.122462048309373
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 20263501 zero yes
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cP all pressure cTemp
compute bl all bond/local dist
compute maxbl all reduce max c_bl inputs local
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE/atoms
variable K equal c_cKE/atoms
variable E equal (c_cPE+c_cKE)/atoms
variable pxx equal c_cP[1]
variable pyy equal c_cP[2]
variable pzz equal c_cP[3]
variable bx equal lx
variable by equal ly
variable bz equal lz
variable bmax equal c_maxbl
thermo_style custom step time c_cTemp pe ke etotal c_cP[1] c_cP[2] c_cP[3] lx ly lz c_maxbl
thermo_modify norm no
thermo 1000
fix record all ave/time 100 1 100 v_clock v_T v_U v_K v_E v_pxx v_pyy v_pzz v_bx v_by v_bz v_bmax file thermo.dat format " %.15g"
dump trajectory all custom 500 trajectory.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
compute chunks all chunk/atom molecule
compute chainRg all gyration/chunk chunks
fix rg all ave/time 100 1 100 c_chainRg file chain-rg.dat mode vector format " %.15g"
run 20000
write_data relaxed.data
write_restart relaxed.restart
fix stretch all deform 1 x scale 1.2 y volume z volume remap x units box
run 20000
unfix stretch
write_data stretched.data
run 20000
write_data final.data
write_restart final.restart
```

Example for configuration 1 with 80 added links; other branches use their own data and random seeds.

The input retains an NVE integrator together with the Langevin thermostat and a time step of 0.005τ. In this combination, the NVE command supplies the position and velocity integration operation. The bath continues exchanging energy, and loading changes the box and particle positions, so the physical process follows from all commands together. Data files saved after the three run stages connect the original, relaxed and extended network states. Before the final stage, fix deform is removed and integration continues with the deformed cell held fixed. Beads still experience forces and exchange energy with the bath; the imposed overall deformation simply stops increasing.

The complete generator derives the zero-, eighty- and 160-link cases from each prepared melt and runs preparation, loading and holding continuously. Readers who completed the previous exercise can analyse those outputs directly; the program and shell script below also provide the complete workflow from the beginning. Each configuration retains its own selected-edge list. Thus eighty links in different replicates define different networks generated by the same rule. Keeping both link count and configuration ID makes it possible to inspect variation at a fixed link count and to compare increasing connectivity within one prepared melt. These two kinds of variation can then be examined separately.

### Generate and run the three connection patterns

```
"""Prepare, connect, relax and stretch a FENE bead-spring network.

python run_network.py --beads 1600 --replica 1 --out-dir network-runs
The LAMMPS executable is selected by --lmp or the LAMMPS environment variable.
Each independent preparation is followed by zero, one or two links per
original chain in total. The linked cases share nested selected-edge lists.
The output retains the exact selected endpoints, inputs and simulation logs.
"""
from pathlib import Path
import argparse,json,hashlib,subprocess,time,re,math
import numpy as np
import os,shutil
p=argparse.ArgumentParser();p.add_argument('--beads',type=int,default=1600);p.add_argument('--replica',type=int,default=1);p.add_argument('--out-dir',type=Path,default=Path('network-runs'));p.add_argument('--lmp',default=os.environ.get('LAMMPS','lmp'));a=p.parse_args()
N=a.beads;M=N//20;assert N%20==0
base=a.out_dir.resolve();d=base/f'n{N}-rep{a.replica}'
if d.exists():raise SystemExit('Choose a new output directory for this configuration.')
d.mkdir(parents=True)
seed=20263000+a.replica;generator=np.random.default_rng(seed);L=(N/.85)**(1/3);coords=[];bonds=[]
# Pack open chains while retaining the seeded sequence of random draws.
for chain in range(M):
 current=generator.uniform(0,L,3)
 for local in range(20):
  for attempt in range(100000):
   candidate=generator.uniform(0,L,3) if local==0 else current+.97*(v:=generator.normal(size=3))/np.linalg.norm(v)
   if coords:
    dr=np.array(coords)-candidate;dr-=L*np.round(dr/L)
    if np.min(np.sum(dr*dr,axis=1))<.65**2:continue
   break
  else:raise RuntimeError('Chain packing did not find a valid location')
  coords.append(candidate.copy());current=candidate
  if local:bonds.append((len(coords)-1,len(coords)))
lines=['Generated FENE chain starting configuration','',f'{N} atoms',f'{len(bonds)} bonds','','1 atom types','2 bond types','',f'0 {L:.15g} xlo xhi',f'0 {L:.15g} ylo yhi',f'0 {L:.15g} zlo zhi','','Masses','','1 1.0','','Atoms # bond','']
for i,xyz in enumerate(coords):
 image=np.floor(xyz/L).astype(int);wrapped=xyz-L*image;lines.append(f'{i+1} {i//20+1} 1 '+' '.join(f'{x:.15g}' for x in wrapped)+' '+' '.join(str(x) for x in image))
lines+=['','Bonds','']+[f'{j+1} 1 {i} {k}' for j,(i,k) in enumerate(bonds)]
(d/'initial.data').write_text('\n'.join(lines)+'\n')
# Shared reduced-unit, neighbour and special-pair definitions.
header='''units lj
atom_style bond
boundary p p p
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
'''
# Instantaneous records: time, T, U/N, K/N, E/N, pressure, box and longest bond.
record='''compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cP all pressure cTemp
compute bl all bond/local dist
compute maxbl all reduce max c_bl inputs local
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE/atoms
variable K equal c_cKE/atoms
variable E equal (c_cPE+c_cKE)/atoms
variable pxx equal c_cP[1]
variable pyy equal c_cP[2]
variable pzz equal c_cP[3]
variable bx equal lx
variable by equal ly
variable bz equal lz
variable bmax equal c_maxbl
thermo_style custom step time c_cTemp pe ke etotal c_cP[1] c_cP[2] c_cP[3] lx ly lz c_maxbl
thermo_modify norm no
thermo 1000
fix record all ave/time 100 1 100 v_clock v_T v_U v_K v_E v_pxx v_pyy v_pzz v_bx v_by v_bz v_bmax file thermo.dat format " %.15g"
dump trajectory all custom 500 trajectory.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
compute chunks all chunk/atom molecule
compute chainRg all gyration/chunk chunks
fix rg all ave/time 100 1 100 c_chainRg file chain-rg.dat mode vector format " %.15g"
'''
# Soft separation, FENE switch, minimization and 100 tau melt preparation.
prepare=header+f'''read_data initial.data
bond_style harmonic
bond_coeff * 100.0 0.97
pair_style soft 1.122462048309373
pair_coeff * * 0
velocity all create 1.0 {seed+100} mom yes rot no dist gaussian
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+200} zero yes
variable softA equal ramp(0,100)
fix soften all adapt 1 pair soft a * * v_softA
timestep 0.002
thermo 1000
thermo_style custom step temp pe ke etotal
run 20000
unfix soften
unfix dyn
unfix bath
write_data after-soft.data
pair_style lj/cut 1.122462048309373
pair_modify shift yes
pair_coeff * * 1 1 1.122462048309373
bond_style fene
bond_coeff * 30.0 1.5 1.0 1.0
min_style cg
min_modify dmax 0.01
minimize 1e-8 0.01 10000 100000
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+300} zero yes
'''+record+'''run 20000
write_restart melt.restart
write_data melt.data
'''
(d/'prepare.lmp').write_text(prepare,encoding='utf-8',newline='\n')
found=shutil.which(a.lmp);assert found, f'LAMMPS executable not found: {a.lmp}';binary=Path(found).resolve();logs=[]
def run(where,script):
 cmd=[str(binary),'-in',script,'-log','simulation.log']
 r=dict(command=cmd,directory=where.relative_to(base).as_posix(),input_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in where.iterdir() if f.is_file()});t=time.perf_counter()
 with (where/'stdout.log').open('wb') as f:q=subprocess.run(cmd,cwd=where,env={**os.environ,'OMP_NUM_THREADS':'1'},stdout=f,stderr=subprocess.STDOUT)
 r.update(exit_code=q.returncode,wall_seconds=time.perf_counter()-t,output_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in where.iterdir() if f.is_file()});logs.append(r)
 (d/'progress.json').write_text(json.dumps(logs,indent=2));print(json.dumps({'directory':str(where),'exit_code':q.returncode,'wall_seconds':r['wall_seconds']}),flush=True)
 if q.returncode:raise SystemExit(q.returncode)
run(d,'prepare.lmp')
data=(d/'melt.data').read_text();atompart=re.search(r'\nAtoms[^\n]*\n(.*?)(?=\n[A-Z][A-Za-z ]*(?:#.*)?\n|\Z)',data,re.S)[1]
atoms=np.array([[float(x) for x in line.split()] for line in atompart.splitlines() if line.strip()]);atoms=atoms[np.argsort(atoms[:,0])];xyz=atoms[:,3:6];mol=atoms[:,1].astype(int)
# Candidate edges connect nearby beads with different original chain IDs.
candidate=[]
for i in range(N-1):
 dr=xyz[i+1:]-xyz[i];dr-=L*np.round(dr/L);r2=np.sum(dr*dr,1)
 for j in np.flatnonzero((r2<=1.15**2)&(mol[i+1:]!=mol[i])):candidate.append((i,int(i+1+j),float(np.sqrt(r2[j]))))
# Greedy matching uses each bead once; prefixes of one list give nested cases.
edgegen=np.random.default_rng(seed+400);edgegen.shuffle(candidate);edges=[];used=set()
for i,j,dist in candidate:
 if i not in used and j not in used:edges.append((i+1,j+1,dist));used.update((i,j))
target=M*2
if len(edges)<target:raise RuntimeError(f'Only {len(edges)} available edges for {target} target')
# Each branch: 100 tau relaxation, 100 tau extension, 100 tau fixed strain.
choices=[0,M,2*M]
for nc in choices:
 sub=d/f'links-{nc}';sub.mkdir();selected=edges[:nc];text=data
 text=re.sub(r'^\d+ bonds$',f'{len(bonds)+nc} bonds',text,flags=re.M)
 match=re.search(r'\nBonds\s*\n(.*?)(?=\n[A-Z][A-Za-z ]*(?:#.*)?\n|\Z)',text,re.S)
 original=match[1].strip();addition='\n'.join(f'{len(bonds)+j+1} 2 {i} {k}' for j,(i,k,_) in enumerate(selected))
 text=text[:match.start(1)]+original+'\n'+addition+'\n'+text[match.end(1):]
 (sub/'network.data').write_text(text)
 (sub/'selected-crosslinks.json').write_text(json.dumps(dict(seed=seed+400,candidates=len(candidate),selected=selected,definition='Different original chain IDs, minimum-image distance<=1.15, at most one added edge per bead; common ordered candidate list gives nested link sets.'),indent=2))
 protocol=header+f'''bond_style fene
pair_style lj/cut 1.122462048309373
pair_modify shift yes
read_data network.data
bond_coeff * 30.0 1.5 1.0 1.0
pair_coeff * * 1 1 1.122462048309373
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 {seed+500} zero yes
'''+record+'''run 20000
write_data relaxed.data
write_restart relaxed.restart
fix stretch all deform 1 x scale 1.2 y volume z volume remap x units box
run 20000
unfix stretch
write_data stretched.data
run 20000
write_data final.data
write_restart final.restart
'''
 (sub/'network.lmp').write_text(protocol,encoding='utf-8',newline='\n');run(sub,'network.lmp')
receipt=dict(case='lammps-network',N=N,chains=M,replica=a.replica,seed=seed,rho=.85,chain_length=20,links=choices,binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),source='Official LAMMPS30Sep2026Update1 bench/in.chain interaction model; independently generated coordinates and explicitly added crosslink/deformation protocols',runs=logs,exit_code=0)
(d/'receipt.json').write_text(json.dumps(receipt,indent=2));print('Network comparison complete',flush=True)
```

Save connectivity and all three stages, beginning with melt preparation.

### Run three independent configurations from the beginning

```
#!/usr/bin/env bash
set -euo pipefail
for replica in 1 2 3; do
  python run_network.py --beads 1600 --replica "$replica" --out-dir network-runs
done
python analyze_mechanics.py network-runs --out mechanics/en --language en
python analyze_mechanics.py network-runs --out mechanics/zh --language zh
```

With network-runs output from the previous lesson, execute the final two analysis commands directly.

### Recorded deformation and temperature

Top: recorded length ratios for configuration 1 with 160 links. Bottom: 5τ temperature-block means, followed by the mean and sample SD across three configurations. Shading marks loading from 100–200τ.

LAMMPS 30 Sep 2026 Update 1; official bead–spring interaction model, with 1600 beads in 80 chains of 20, ρ*=0.85 and T*=1, using three initial configurations. The FENE/WCA dynamics time step is 0.005τ.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/en/#en-s4)

Loading and holding records for the original nine conditions. The cell stretches from 1 to 1.2 along x while y and z contract to conserve volume. Temperature and volume records check the implemented physical conditions.

## Reading tensile response from the pressure tensor

A single pressure value is often sufficient for a cup of water because an equilibrium liquid has approximately equal average mechanical action in every direction. A stretching material can transmit different forces along different directions, so directional information must be retained. The pressure tensor is a collection of directional quantities: Pxx, Pyy and Pzz are its normal components, with further components describing tangential action. LAMMPS includes contributions from particle motion and interactions in its global pressure calculation. For this bead–spring model, repulsive pair interactions and bonds both contribute. Observing the extension of one class of bonds therefore cannot replace the calculation of the complete mechanical quantity.

Pressure conventionally takes compression as positive, whereas tensile stress is usually positive in solid mechanics, so their tensors have opposite signs. We further subtract the mean transverse tensile stress from the x tensile stress to obtain a normal-stress difference S. An equal hydrostatic contribution in all directions then cancels, leaving the directional difference. If all three pressure components equal five, S is zero. If Pxx decreases to four while the transverse components remain five, S is one. A positive tensile normal-stress difference can therefore occur even while the individual pressure components remain positive.

Tension-positive normal-stress differenceEq. 3

![Tension-positive normal-stress difference](https://ml-biomat.com/static/agent-math/b95c88cf7dd466c999a902e1.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| S | Axial tensile stress minus the mean transverse tensile stress | ε/σ³ |
| Pₓₓ, Pᵧᵧ, P𝓏𝓏 | Normal components of the global LAMMPS pressure tensor | ε/σ³ |
| ε | Energy unit of the bead–spring model | energy |
| σ | Length unit of the bead–spring model | length |
| =, −, +, /, 2 | Equality, negation, addition, division; two averages the transverse pair | 1 |

Reading the relationshipTension-positive stress has the opposite sign to compression-positive pressure. Subtracting the transverse mean cancels an equal hydrostatic contribution.

A worked exampleIf Pxx=4 and Pyy=Pzz=5 in ε/σ³, S=−4+(5+5)/2=1ε/σ³. Equal components of 5 give S=0.

ConditionsFor this periodic constant-volume loading, including kinetic and interaction contributions in the recorded pressure. The quantity measures the normal directional difference.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/en/#en-s5)

Figure 3 · Two worked pressure-tensor examples. Equal normal pressures give zero normal-stress difference; a lower axial pressure gives a positive tensile difference relative to the transverse directions.

The relation between S and an experimental tensile force depends on the boundary conditions. A specimen with free side surfaces is often close to zero transverse stress, making axial stress close to the axial-minus-transverse difference. Here transverse contraction is imposed to preserve volume, and transverse pressure develops from the interactions. We therefore label the plotted quantity explicitly as a normal-stress difference. True stress also differs from nominal stress calculated using the initial area: as a specimen narrows, dividing one force by the current area or the original area gives different values. For this periodic system, the pressure components and geometrical constraints provide the starting point for interpreting the measured response.

Instantaneous stress fluctuates with collisions, bond vibrations and local rearrangement. Averaging saved values over a time interval reduces fast variation while retaining slower loading trends. We divide the 100τ loading interval into twenty blocks of 5τ, calculate each configuration’s block means, and then display the mean and sample standard deviation across the three configurations. Shading describes their between-configuration spread, and thin lines retain each replicate. This shows whether a trend appears across the set and prevents one temporarily high interval from defining the comparison. Block duration also controls temporal resolution: longer blocks combine more of the fast dynamics into one observation.

### Loading stresses for the original nine networks

Each thin line contains 5τ block means for one configuration; the dark line is their mean and shading is their sample SD. Strain is calculated from box lengths in the same thermodynamic records.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/en/#en-s5)

Normal-stress difference S is averaged in 5τ loading blocks. Each link count retains three configurations; dark lines and shading show their mean and sample standard deviation. The horizontal axis is engineering strain.

The stress unit ε/σ³ can be understood through energy and volume. Deformation involves work, and work accumulates force over displacement, so energy divided by volume has the same dimensions as force divided by area. The reduced model leaves ε and σ as chosen scales and reports stress through this combination. Conversion to pascals requires a consistent physical mapping for energy and length. If an energy scale is quoted per mole, it must first be converted to the energy associated with a simulated interaction. Checking these dimensions is useful for finding missing volume factors or confusion between total and per-particle energy, before numerical values are compared with a material experiment.

## Which directions change? Bonds and whole chains

One way to inspect the internal response is to measure the angle between each original-chain bond and the x axis. A bond aligned with x has a large x component in its unit direction vector, while a transverse bond has a small one. Combining the squared cosine of that angle gives the second-order orientation measure P₂. It equals one when every bond is parallel to x, minus one-half when every bond is perpendicular to x, and averages to zero for an isotropic distribution of directions in three dimensions. Squaring treats bonds pointing toward positive and negative x as aligned with the same axis, which suits the study of stretching-induced orientation.

Original-chain bond orientation along the loading axisEq. 4

![Original-chain bond orientation along the loading axis](https://ml-biomat.com/static/agent-math/d10a6bc5ac632f32cbfc72a8.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| P₂ | Second-order original-bond orientation relative to x | 1 |
| B₀ | Number of original-chain bonds, 80×19=1520 here | 1 |
| j | Original-bond index | 1 |
| bⱼ, bⱼₓ | Displacement vector of original bond j and its x component | σ |
| \|bⱼ\| | Magnitude of that bond vector | σ |
| uⱼₓ | x component of the unit bond direction, also the angle cosine | 1 |
| Σ, ² | Sum over original bonds; square | 1 |
| =, /, −, 1, 2, 3 | Equality, division, subtraction and constants one, two, three; adjacent quantities multiply | 1 |

Reading the relationshipSquaring treats positive and negative x as one axis. An isotropic three-dimensional distribution has mean uₓ²=1/3, producing a zero baseline in this combination.

A worked exampleFor bonds parallel to x, uₓ²=1 and P₂=(3−1)/2=1. Perpendicular bonds have uₓ²=0 and P₂=−0.5.

ConditionsThe 1520 original-chain bonds are equally weighted; added links form a separate set. Directions come from actual unwrapped bond vectors.

Local bond directions and whole-chain shape describe different scales. Many bonds may each acquire only a small directional preference, yet their collective arrangement can visibly extend a coiled chain along x. We separate every bead’s displacement from its original-chain centre into x, y and z components, square each component and average. These are the three directional gyration components, whose sum is the squared radius of gyration. Dividing the x component by their sum gives the fraction of the chain’s squared size associated with x. For a statistically isotropic chain population this fraction is close to one-third; extension along x generally increases it.

Directional chain dimensions and axial fractionEq. 5

![Directional chain dimensions and axial fraction](https://ml-biomat.com/static/agent-math/f4ff8fb7c831934b5e95dc63.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| M, n | Number of original chains and beads per chain | 1 |
| m, i | Original-chain and within-chain bead indices | 1 |
| a | Coordinate-direction index x, y or z | 1 |
| rₘᵢₐ | Unwrapped coordinate of bead i of chain m in direction a | σ |
| Rₘₐ | Centre of equal-mass original chain m in direction a | σ |
| Gₐₐ, Gₓₓ, Gᵧᵧ, G𝓏𝓏 | Population-averaged directional gyration components | σ² |
| fₓ | Fraction of total squared chain size along x | 1 |
| Σ, ² | Sum over specified chains or beads; square | 1 |
| =, /, −, +, 1, (, ) | Equality, division, subtraction, addition, one and grouping; adjacent quantities multiply | 1 |

Reading the relationshipSubtract each chain’s own centre to remove translation and average squared displacement by direction. The sum is the mean squared radius of gyration; dividing the x contribution by it gives the axial fraction.

A worked exampleFor three beads at x=−1,0,1σ with y=z=0, the centre is 0 and Gxx=(1+0+1)/3=2/3σ². Gyy=Gzz=0 and fx=1.

ConditionsBeads have equal mass; original chains are unwrapped using current box lengths and image flags. fx is a ratio of population-averaged components, distinct from averaging per-chain ratios.

These calculations first unwrap each original chain using the trajectory image flags and the actual box lengths of that frame. Cell lengths change during loading, so unwrapping later coordinates with the initial box would misplace boundary-crossing strands. Every original chain still contains twenty equal-mass beads, allowing its centre to be calculated as their mean position. The retained original-chain IDs follow the dimensions of those same finite strands. The complete crosslinked network can instead extend through periodic replicas and requires a different whole-network size definition. The program also checks original-chain bond lengths to confirm that adjacent unwrapped beads remain at physically consistent distances.

The actual curves place these two scales together. During loading, original-chain bond orientation becomes more positive and the x fraction of whole-chain size rises. Both continue adjusting after the cell dimensions are fixed. The latter observation is particularly intuitive: external dimensions have stopped changing, yet internal strands can rotate and redistribute their bends. Curves for different link counts overlap and starting configurations differ, so the figure shows three-configuration means and their spread. These structural records complement the stress curves, connecting continued material relaxation to measurable internal motion rather than treating relaxation as an abstract label.

### Orientation and directional size of the actual chains

Original chains are unwrapped with each frame’s box lengths and images. Top: P₂ of 1520 original bonds. Bottom: population-averaged Gxx divided by the sum of directional components. Shading is the sample SD across three configurations.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/en/#en-s6)

The upper panel measures the second-order orientation parameter of consecutive original-chain bonds relative to the stretching axis; the lower shows the x share of the original-chain gyration tensor. Image flags reconstruct each chain before local orientation and whole-chain shape are compared over the same loading history.

Uniform geometrical mapping also provides a useful reference picture. If a chain simply followed the deforming grid and underwent no subsequent internal adjustment, its x extent would increase with the imposed extension and its transverse extents would decrease with contraction. In the actual trajectory, forces and thermal motion continue between remapping operations, so chain shape can depart from that reference. Comparing the two helps distinguish geometrically imposed change from rearrangement by the strands themselves. Showing both local bond alignment and directional whole-chain dimensions makes these multiple scales visible. A material distributes deformation among them, and their evolution need not proceed at the same rate.

## Interpreting stress after deformation is held fixed

Holding the cell after loading does not freeze its particles. Strands continue fluctuating, local forces change and directional preferences may slowly adjust. This is the process studied in stress-relaxation experiments on viscoelastic materials: maintain deformation and observe the corresponding stress over time. Creep asks the complementary question, maintaining an applied load while observing deformation. The two experiments require different controls. Our fixed cell shape makes stress the evolving response to internal motion. Separating the controlled variable from the measured variable clarifies the experimental question and identifies which part of a simulation protocol should change when asking a different question.

Before loading, a finite system can already have a nonzero normal-stress difference because of its conformation and finite averaging interval. To compare changes relative to each branch’s own starting condition, the holding plot subtracts that branch’s mean stress from the resting window 50≤t<100τ. This defines a change from a specified reference state while retaining the raw stress values in the numerical output. A reference window should precede loading, use consistent physical conditions and follow the same rule across systems. Moving the window after loading or selecting it according to the resulting stress would define a different comparison. Both the window and each branch’s baseline are therefore saved.

Stress change from the branch-specific resting baselineEq. 6

![Stress change from the branch-specific resting baseline](https://ml-biomat.com/static/agent-math/8913bd3f4a29e7121d0e91fa.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Sⱼ | Normal-stress-difference record j in the resting window | ε/σ³ |
| n₀ | Number of baseline records, 100 here | 1 |
| j | Baseline-record index | 1 |
| S̄₀ | Mean over that branch’s reference window | ε/σ³ |
| S(t), ΔS(t) | Raw stress difference and its baseline-relative change at t | ε/σ³ |
| t | Record time | τ |
| Σ, =, /, −, Δ | Summation, equality, division, subtraction and change marker | 1 |

Reading the relationshipUse the preloading mean of the same branch as the reference, separately recording its finite-configuration offset and subsequent change.

A worked exampleThe first 160-link network has baseline approximately −0.009295ε/σ³. A holding-block S=0.18ε/σ³ gives ΔS=0.18−(−0.009295)=0.189295ε/σ³.

ConditionsThe baseline is 50≤t<100τ with a record every 0.5τ, calculated separately for each network; raw S is retained.

### Adjustment at fixed 1.2 stretch

Subtract each branch’s resting baseline 50≤t<100τ. Holding uses 10τ blocks with left-open/right-closed intervals. Thin lines show configurations, the dark line their mean and shading their sample SD.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/en/#en-s7)

The 100τ holding record uses 10τ blocks. Each branch is first referenced to its own resting stress over 50≤t<100τ, then the mean and sample standard deviation across three configurations are compared. Thermal fluctuations over this window remain visible.

In these short records at twenty-percent extension, the linked systems have positive mean normal-stress differences near the end of loading, with appreciable variation across configurations during holding. For 160 added links, the three-configuration mean over 190

To observe the hold more clearly, the same three 160-link networks undergo an additional protocol. Each starts from its original relaxed endpoint, reaches a stretch of 1.5 over 300τ, and then holds for 500τ. This branch starts a new Langevin random history while retaining temperature, damping time, bond parameters and volume conservation. It increases both final deformation and observation duration, providing holding records with a clearer load signal. The original nine twenty-percent-extension results remain part of the comparison, describing smaller-deformation structural changes and fluctuations. Each protocol is interpreted with its complete conditions, so the combined changes are not assigned to a single variable.

### Complete input for 1.5 stretch and a longer hold

```
units lj
atom_style bond
boundary p p p
read_restart initial.restart
special_bonds fene
neighbor 0.4 bin
neigh_modify every 1 delay 0 check yes
pair_modify shift yes
reset_timestep 0
timestep 0.005
fix dyn all nve
fix bath all langevin 1.0 1.0 1.0 20263501 zero yes
compute cTemp all temp
compute cPE all pe
compute cKE all ke
compute cP all pressure cTemp
compute bl all bond/local dist
compute maxbl all reduce max c_bl inputs local
variable clock equal time
variable T equal c_cTemp
variable U equal c_cPE/atoms
variable K equal c_cKE/atoms
variable E equal (c_cPE+c_cKE)/atoms
variable pxx equal c_cP[1]
variable pyy equal c_cP[2]
variable pzz equal c_cP[3]
variable bx equal lx
variable by equal ly
variable bz equal lz
variable bmax equal c_maxbl
thermo_style custom step time c_cTemp pe ke etotal c_cP[1] c_cP[2] c_cP[3] lx ly lz c_maxbl
thermo_modify norm no
thermo 1000
fix record all ave/time 100 1 100 v_clock v_T v_U v_K v_E v_pxx v_pyy v_pzz v_bx v_by v_bz v_bmax file thermo.dat format " %.15g"
dump trajectory all custom 500 trajectory.lammpstrj id mol type x y z vx vy vz ix iy iz
dump_modify trajectory sort id
compute chunks all chunk/atom molecule
compute chainRg all gyration/chunk chunks
fix rg all ave/time 100 1 100 c_chainRg file chain-rg.dat mode vector format " %.15g"
run 0
fix stretch all deform 1 x scale 1.5 y volume z volume remap x units box
run 60000
unfix stretch
write_data stretched.data
write_restart stretched.restart
run 100000
write_data final.data
write_restart final.restart
```

Start from the original 160-link relaxed.restart, reset time and begin a new Langevin random history.

### Apply the same protocol to the three original networks

```
"""Run three 1.5-stretch branches from the prepared 160-link networks.

python run_extension.py --base-runs network-runs --out-runs network-extension
Use the same LAMMPS build that produced the binary restart files.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("--base-runs", type=Path, default=Path("network-runs"))
parser.add_argument("--out-runs", type=Path, default=Path("network-extension"))
parser.add_argument("--lmp", default=os.environ.get("LAMMPS", "lmp"))
args = parser.parse_args()
binary = shutil.which(args.lmp)
if binary is None:
    raise SystemExit(f"LAMMPS executable not found: {args.lmp}")
template = Path(__file__).with_name("extension.lmp").read_text(encoding="utf-8")
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
for replica in (1, 2, 3):
    source = args.base_runs/f"n1600-rep{replica}"/"links-160"/"relaxed.restart"
    target = args.out_runs/f"n1600-rep{replica}-links160"
    if target.exists():
        raise SystemExit(f"Choose a new output directory: {target}")
    if not source.is_file():
        raise SystemExit(f"Prepare the source network first: {source}")
    target.mkdir(parents=True)
    shutil.copy2(source, target/"initial.restart")
    text = template.replace("20263501", str(20263500+replica))
    (target/"extension.lmp").write_text(text, encoding="utf-8", newline="\n")
    command = [str(Path(binary).resolve()), "-in", "extension.lmp", "-log", "simulation.log"]
    started = time.perf_counter()
    with (target/"stdout.log").open("wb") as stream:
        result = subprocess.run(command, cwd=target, env={**os.environ, "OMP_NUM_THREADS": "1"},
                                stdout=stream, stderr=subprocess.STDOUT)
    receipt = {"replica": replica, "exit_code": result.returncode,
               "wall_seconds": time.perf_counter()-started,
               "source_restart_sha256": digest(source),
               "input_sha256": digest(target/"extension.lmp"),
               "new_Langevin_history_after_restart": True,
               "Langevin_seed": 20263500+replica,
               "protocol": "300tau to lambda1.5, constant volume;500tau hold;T1,damping1,dt0.005"}
    (target/"receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps(receipt), flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
```

Copy the corresponding restart state and write each input. Use the same LAMMPS version that generated the restart files.

### Run the additional protocol and generate bilingual plots

```
#!/usr/bin/env bash
set -euo pipefail
python run_extension.py --base-runs network-runs --out-runs network-extension
python analyze_extension.py network-extension --base-runs network-runs --out extension-analysis/en --language en
python analyze_extension.py network-extension --base-runs network-runs --out extension-analysis/zh --language zh
```

Run after preparing network-runs and its three 160-link relaxed restart files.

The longer holding record is divided into ten blocks of 50τ per configuration. Over the final 250τ, the three networks have mean normal-stress differences of about 0.1752, 0.1088 and 0.1144ε/σ³. Their mean is 0.1328ε/σ³ and the sample standard deviation across configurations is about 0.0368ε/σ³. Variation between configurations is saved separately from variation between time blocks within one trajectory. Each network has its own link locations and conformation, so equal link counts need not give identical holding loads. The figure retains individual curves and their shared mean, displaying both aspects of the measurement rather than concealing network differences within one averaged line.

### Larger extension and a longer hold for the same three networks

Restart the same three 160-link networks from their original relaxed endpoints: 300τ to 1.5 stretch, then 500τ holding. Left: 20τ blocks; right: 50τ blocks, both left-inclusive/right-exclusive. Shading is the sample SD across three configurations.

Three 1600-bead FENE networks with 160 added interchain bonds restart from their respective original 100τ prepared states. T*=1 at constant volume; x stretches to 1.5 over 300τ, followed by a 500τ hold, using a 0.005τ time step.

[Download reference data and complete inputs (ZIP) 47.14 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-network-extended-mechanics-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l10/en/#en-s7)

The same three networks with 160 added links restart from their respective prepared states, stretch to 1.5 over 300τ and hold for another 500τ. Both panels show normal-stress difference S without baseline subtraction, retaining individual configurations, their mean and sample standard deviation. This protocol changes both extension and observation duration.

### Complete longer-hold analysis

```
"""Analyse the independently restarted 1.5-stretch, 500tau-hold networks.

python analyze_extension.py network-extension --base-runs network-runs \
    --out extension-analysis --language en
Input: thermo.dat in three n1600-repN-links160 extension directories and the
original n1600-repN/links-160 directories used for preloading baselines.
"""
from pathlib import Path
import argparse
import json
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def stress(table):
    return -table[:, 6]+(table[:, 7]+table[:, 8])/2


def blocks(time, value, left, right, width):
    rows = []
    for lo in np.arange(left, right, width):
        mask = (time >= lo) & (time < lo+width)
        assert np.any(mask)
        rows.append([lo+width/2, np.mean(value[mask])])
    return np.asarray(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--base-runs", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("extension-analysis"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    records, raw = [], []
    for rep in (1, 2, 3):
        table = np.loadtxt(args.directory/f"n1600-rep{rep}-links160"/"thermo.dat")
        base = np.loadtxt(args.base_runs/f"n1600-rep{rep}"/"links-160"/"thermo.dat")
        time = table[:, 1]
        assert table.shape == (1601, 13) and np.allclose(time, np.arange(1601)*.5)
        S = stress(table)
        base_window = (base[:, 1] >= 50) & (base[:, 1] < 100)
        baseline = float(stress(base)[base_window].mean())
        ratios = table[:, 9:12]/table[0, 9:12]
        assert np.max(abs(np.prod(ratios, axis=1)-1)) < 1e-12
        assert np.allclose(ratios[-1], [1.5, 1.5**(-.5), 1.5**(-.5)], atol=1e-12)
        hold = blocks(time, S, 300, 800, 50)
        loading = blocks(time, S, 0, 300, 20)
        strains = blocks(time, ratios[:, 0]-1, 0, 300, 20)[:, 1]
        late = hold[-5:, 1]
        records.append({"replica": rep, "temperature_mean": float(table[:, 2].mean()),
                        "temperature_sd": float(table[:, 2].std(ddof=1)),
                        "max_bond_sigma": float(table[:, 12].max()),
                        "final_stretches": ratios[-1].tolist(),
                        "old_baseline_50_le_t_lt_100": baseline,
                        "late_hold_stress_550_le_t_lt_800": float(late.mean()),
                        "late_hold_timeblock_sd": float(late.std(ddof=1)),
                        "late_change_from_baseline": float(late.mean()-baseline),
                        "holding_50tau_block_means": hold.tolist()})
        raw.append((loading, strains, hold))
        np.savetxt(args.out/f"hold-blocks-rep{rep}.csv", hold, delimiter=",",
                   header="time_from_restart_tau,normal_stress_difference_epsilon_per_sigma3", comments="")
    late = np.array([r["late_hold_stress_550_le_t_lt_800"] for r in records])
    changes = np.array([r["late_change_from_baseline"] for r in records])
    result = {"definition": "Tension-positive normal difference S=-Pxx+(Pyy+Pzz)/2, epsilon/sigma3",
              "protocol": "Restart each original160-link relaxed state, new Langevin history; lambda1 to1.5 in300tau, hold500tau",
              "blocks": "20tau loading,50tau holding; intervals[left,right). Late window550<=t<800 is the final250tau of holding.",
              "records": records,
              "late_hold_mean_across_three": float(late.mean()),
              "late_hold_sample_sd_across_three": float(late.std(ddof=1)),
              "late_change_mean_across_three": float(changes.mean()),
              "late_change_sample_sd_across_three": float(changes.std(ddof=1))}
    (args.out/"extension_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    zh = args.language == "zh"
    tr = lambda c,e: c if zh else e
    installed = {f.name for f in font_manager.fontManager.ttflist}
    font_candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"]
    plt.rcParams.update({"font.family": [x for x in font_candidates if x in installed] if zh else ["DejaVu Sans"],
                         "font.size": 14, "svg.fonttype": "path", "axes.spines.top": False,
                         "axes.spines.right": False, "figure.facecolor": "#faf9f5", "axes.facecolor": "#faf9f5",
                         "text.color": "#193d43", "axes.labelcolor": "#193d43"})
    fig, axes = plt.subplots(1, 2, figsize=(13, 6), constrained_layout=True)
    fig.get_layout_engine().set(wspace=.12)
    for ax, stage in zip(axes, (0, 2)):
        values = np.stack([r[stage][:, 1] for r in raw])
        x = raw[0][1] if stage == 0 else raw[0][2][:, 0]-300
        for i, (color, ls) in enumerate(zip(("#167d84", "#c16b3d", "#466eaa"), ("-", "--", ":"))):
            ax.plot(x, values[i], color=color, ls=ls, lw=1.3, label=tr(f"构型 {i+1}", f"Config. {i+1}"))
        mean, sd = values.mean(0), values.std(0, ddof=1)
        ax.fill_between(x, mean-sd, mean+sd, color="#557b80", alpha=.13)
        ax.plot(x, mean, color="#193d43", lw=2.5, label=tr("三组平均", "Mean of three"))
        ax.axhline(0, color="#777777", lw=.8); ax.grid(alpha=.15)
    axes[0].set(title=tr("300τ 加载；20τ 分段", "300τ loading; 20τ blocks"),
                xlabel=tr("工程应变 e", "Engineering strain e"), ylabel=tr("法向应力差 S / (ε σ⁻³)", "Normal-stress difference S / (ε σ⁻³)"))
    axes[1].set(title=tr("500τ 保持；50τ 分段", "500τ holding; 50τ blocks"), xlabel=tr("保持时间 / τ", "Hold time / τ"))
    axes[0].legend(frameon=False, fontsize=11)
    fig.suptitle(tr("同三组160边网络：伸长到1.5倍并延长保持", "The same three 160-link networks: stretch to 1.5 and hold longer"), fontsize=18)
    for ext in ("svg", "png"):
        fig.savefig(args.out/f"network-extended-hold-{args.language}.{ext}", dpi=180)
    plt.close(fig)
    print(json.dumps({k:v for k,v in result.items() if k.startswith("late_")}, indent=2))


if __name__ == "__main__":
    main()
```

Loading uses 20τ blocks and holding 50τ blocks, with left-inclusive/right-exclusive intervals. The final 250τ statistics include the sample SD across three configurations.

In this longer observation, all three networks retain a positive late-window mean normal-stress difference at the imposed deformation. This connects with the continuing constraints supplied by permanent links and provides a starting point for investigating a long-time plateau. Separating final extension from loading-rate effects calls for additional controlled comparisons: retain the 300τ loading duration and add a branch ending at 1.2, or retain a final stretch of 1.5 and change the time taken to reach it. Each comparison addresses a specified question, progressively resolving the relationship between material structure, loading rate and observation time seen in the current records.

Extracting a relaxation time requires a record that resolves continuing change and a sufficiently stable later interval. A single exponential can describe one dominant timescale, while a polymer network may contain local rotations, strand rearrangement and longer-scale motion that need several timescales. Comparing observation windows, independent configurations and loading rates helps determine whether fitted parameters remain consistent before selecting a functional form. For a permanent network, a residual elastic contribution should also be distinguished from components that decay with time. The temporal structure of the measured response therefore guides the model used to describe it.

## Connecting loading, statistics and material conditions

The complete analysis reads recorded box lengths, pressure components and all original-chain coordinates. It checks the three-stage geometrical protocol, calculates the normal-stress difference, forms non-overlapping loading and holding blocks, and measures bond orientation and directional chain sizes. Numerical tables retain every replicate, while shading uses the sample standard deviation across the three configurations. The integration step, saved trajectory steps and thermodynamic times are explicitly related so that different outputs can be checked against the same stages. This organization also supports changes to loading duration or link count: modify the physical protocol first, then update the checks and labels to match it.

### Complete geometry, stress and chain-orientation analysis

```
"""Read network deformation, stress and original-chain orientation.

python analyze_mechanics.py network-runs --out mechanics --language en
Requires NumPy and Matplotlib. Each n1600-rep1/2/3 directory contains
links-0/80/160 with thermo.dat and trajectory.lammpstrj.
Stress uses the tension-positive normal difference -Pxx+(Pyy+Pzz)/2.
Shading is the sample SD across three independently prepared configurations.
"""
from pathlib import Path
import argparse
import csv
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def frames(path):
    """Read orthogonal LAMMPS custom dumps and preserve atom identity."""
    with path.open(encoding="utf-8") as stream:
        while line := stream.readline():
            if not line.strip():
                continue
            assert line.strip() == "ITEM: TIMESTEP"
            step = int(stream.readline())
            assert stream.readline().strip() == "ITEM: NUMBER OF ATOMS"
            n = int(stream.readline())
            assert stream.readline().strip() == "ITEM: BOX BOUNDS pp pp pp"
            bounds = np.array([[float(x) for x in stream.readline().split()] for _ in range(3)])
            columns = stream.readline().split()[2:]
            atoms = np.array([[float(x) for x in stream.readline().split()] for _ in range(n)])
            index = {name: i for i, name in enumerate(columns)}
            atoms = atoms[np.argsort(atoms[:, index["id"]])]
            assert np.array_equal(atoms[:, index["id"]], np.arange(1, n+1))
            xyz = atoms[:, [index[k] for k in ("x", "y", "z")]]
            image = atoms[:, [index[k] for k in ("ix", "iy", "iz")]]
            box = bounds[:, 1]-bounds[:, 0]
            yield step*.005, xyz+image*box, atoms[:, index["mol"]].astype(int), box


def chain_shape(path):
    """Equal-mass original chains: gyration components and bond alignment."""
    rows = []
    for time, xyz, mol, box in frames(path):
        assert len(xyz) == 1600
        assert np.array_equal(mol, np.repeat(np.arange(1, 81), 20))
        chains = xyz.reshape(80, 20, 3)
        relative = chains-chains.mean(axis=1, keepdims=True)
        gyration = np.mean(relative**2, axis=(0, 1))
        vectors = np.diff(chains, axis=1)
        distances = np.linalg.norm(vectors, axis=2)
        assert distances.max() < 1.5
        orientation = np.mean((3*(vectors[:, :, 0]/distances)**2-1)/2)
        rows.append([time, *gyration, orientation, distances.mean(), distances.max()])
    rows = np.asarray(rows)
    assert len(rows) == 121 and np.isclose(rows[-1, 0], 300)
    return rows


def block_means(time, values, start, stop, width):
    """Non-overlapping blocks (left, right], with one mean per block."""
    out = []
    for left in np.arange(start, stop, width):
        mask = (time > left+1e-9) & (time <= left+width+1e-9)
        assert mask.any()
        out.append([left+width/2, np.mean(values[mask])])
    return np.asarray(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, default=Path("mechanics"))
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    records, raw = [], {}
    for replica in (1, 2, 3):
        for links in (0, 80, 160):
            base = args.directory/f"n1600-rep{replica}"/f"links-{links}"
            thermo = np.loadtxt(base/"thermo.dat", comments="#")
            assert thermo.shape == (601, 13)
            time = thermo[:, 1]
            assert np.allclose(time, np.arange(601)*.5)
            box = thermo[:, 9:12]
            stretches = box/box[0]
            volume_ratio = np.prod(stretches, axis=1)
            # ave/time precedes fix deform in the end-of-step fix order.
            # During loading its recorded box is one integration step behind
            # the post-remap box saved in trajectory/data output.
            recorded_elapsed = np.clip(time-100, 0, 100)
            loading_record = (time > 100) & (time <= 200)
            recorded_elapsed[loading_record] -= .005
            expected_x = 1+.002*recorded_elapsed
            expected_yz = expected_x**(-.5)
            assert np.max(np.abs(stretches[:, 0]-expected_x)) < 1e-12
            assert np.max(np.abs(stretches[:, 1:]-expected_yz[:, None])) < 1e-12
            stress = -thermo[:, 6]+.5*(thermo[:, 7]+thermo[:, 8])
            baseline_mask = (time >= 50) & (time < 100)
            baseline = float(stress[baseline_mask].mean())
            shape = chain_shape(base/"trajectory.lammpstrj")
            start_shape = shape[np.isclose(shape[:, 0], 100)][0]
            end_shape = shape[np.isclose(shape[:, 0], 200)][0]
            final_shape = shape[-1]
            summary = {
                "replica": replica, "added_links": links,
                "initial_box_sigma": box[0].tolist(), "final_box_sigma": box[-1].tolist(),
                "final_stretches": stretches[-1].tolist(),
                "final_engineering_strain": float(stretches[-1, 0]-1),
                "final_hencky_strain": float(np.log(stretches[-1, 0])),
                "engineering_strain_rate_per_tau": .002,
                "max_volume_ratio_error": float(np.max(np.abs(volume_ratio-1))),
                "baseline_stress_50_le_t_lt_100": baseline,
                "loading_end_stress_190_lt_t_le_200": float(stress[(time > 190) & (time <= 200)].mean()),
                "early_hold_stress_200_lt_t_le_220": float(stress[(time > 200) & (time <= 220)].mean()),
                "late_hold_stress_280_lt_t_le_300": float(stress[(time > 280) & (time <= 300)].mean()),
                "loading_temperature_mean": float(thermo[(time > 100) & (time <= 200), 2].mean()),
                "holding_temperature_mean": float(thermo[(time > 200) & (time <= 300), 2].mean()),
                "max_bond_sigma": float(thermo[:, 12].max()),
                "gyration_components_t100": start_shape[1:4].tolist(),
                "gyration_components_t200": end_shape[1:4].tolist(),
                "gyration_components_t300": final_shape[1:4].tolist(),
                "bond_P2_t100": float(start_shape[4]), "bond_P2_t200": float(end_shape[4]),
                "bond_P2_t300": float(final_shape[4]),
                "shape_frames": len(shape), "thermo_records": len(time),
            }
            summary["late_hold_change_from_baseline"] = summary["late_hold_stress_280_lt_t_le_300"]-baseline
            records.append(summary)
            raw[(replica, links)] = {"time": time, "thermo": thermo, "stretches": stretches,
                                     "stress": stress, "baseline": baseline, "shape": shape}
            np.savetxt(args.out/f"shape-rep{replica}-links{links}.csv", shape, delimiter=",",
                       header="time_tau,Gxx_sigma2,Gyy_sigma2,Gzz_sigma2,original_bond_P2,mean_bond_sigma,max_bond_sigma", comments="")
    aggregate = []
    for links in (0, 80, 160):
        group = [row for row in records if row["added_links"] == links]
        row = {"added_links": links, "independent_configurations": 3}
        for key in ("baseline_stress_50_le_t_lt_100", "loading_end_stress_190_lt_t_le_200",
                    "early_hold_stress_200_lt_t_le_220", "late_hold_stress_280_lt_t_le_300",
                    "late_hold_change_from_baseline"):
            values = np.array([g[key] for g in group])
            row[key] = {"mean": float(values.mean()), "sample_sd": float(values.std(ddof=1)), "values": values.tolist()}
        aggregate.append(row)
    result = {"protocol": "100tau fixed volume preparation; 100tau linear Lx ramp to1.2 with constant volume;100tau hold",
              "stress_definition": "S=-Pxx+(Pyy+Pzz)/2, epsilon/sigma^3; tension-positive normal difference",
              "block_definition": "Loading5tau and holding10tau blocks with intervals(left,right]; shading sample SD across3 configurations, not confidence interval",
              "baseline_definition": "50<=t<100, subtracted separately from each branch for holding-change plot",
              "records": records, "aggregate": aggregate}
    (args.out/"mechanics_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    scalar_keys = [k for k, v in records[0].items() if not isinstance(v, list)]
    with (args.out/"mechanics_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=scalar_keys, extrasaction="ignore")
        writer.writeheader(); writer.writerows(records)
    zh = args.language == "zh"
    tr = lambda c, e: c if zh else e
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    fonts = [f for f in candidates if f in installed] if zh else ["DejaVu Sans"]
    plt.rcParams.update({"font.family": fonts, "font.size": 14, "axes.spines.top": False,
                         "axes.spines.right": False, "svg.fonttype": "path", "text.color": "#193d43",
                         "axes.labelcolor": "#193d43", "figure.facecolor": "#faf9f5", "axes.facecolor": "#faf9f5"})
    colors = ["#167d84", "#c16b3d", "#466eaa"]
    def save(fig, name):
        fig.savefig(args.out/f"{name}-{args.language}.svg")
        fig.savefig(args.out/f"{name}-{args.language}.png", dpi=180)
        plt.close(fig)
    fig, axes = plt.subplots(2, 1, figsize=(12, 7.8), sharex=True, constrained_layout=True)
    first = raw[(1, 160)]
    for i, (label, color, ls) in enumerate(zip(("x", "y", "z"), colors, ("-", "-", "--"))):
        axes[0].plot(first["time"], first["stretches"][:, i], label=label, color=color, ls=ls, lw=2)
    for links, color in zip((0, 80, 160), colors):
        blocks = [block_means(raw[(rep, links)]["time"], raw[(rep, links)]["thermo"][:, 2], 0, 300, 5) for rep in (1, 2, 3)]
        values = np.stack([b[:, 1] for b in blocks]); avg, sd = values.mean(0), values.std(0, ddof=1)
        axes[1].plot(blocks[0][:, 0], avg, color=color, label=tr(f"{links} 条新边", f"{links} links"))
        axes[1].fill_between(blocks[0][:, 0], avg-sd, avg+sd, color=color, alpha=.13)
    for ax in axes:
        ax.axvspan(100, 200, color="#ece4d5", alpha=.5, zorder=0)
        ax.axvline(100, color="#777777", lw=.7, ls=":"); ax.axvline(200, color="#777777", lw=.7, ls=":")
        ax.legend(frameon=False, ncol=3); ax.grid(alpha=.18)
    axes[0].set_ylabel(tr("盒长 / 初始盒长", "Box length / initial length"))
    axes[1].set(xlabel=tr("时间 / τ", "Time / τ"), ylabel=tr("温度 T*", "Temperature T*"))
    axes[1].axhline(1, color="#687574", lw=1, ls="--")
    fig.suptitle(tr("先规定形变，再核对温度和体积", "Specify deformation, then check thermal and geometric conditions"), fontsize=18)
    save(fig, "network-deformation")
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.7), sharey=True, constrained_layout=True)
    fig.get_layout_engine().set(wspace=.12)
    for ax, links, color in zip(axes, (0, 80, 160), colors):
        blocks = [block_means(raw[(rep, links)]["time"], raw[(rep, links)]["stress"], 100, 200, 5) for rep in (1, 2, 3)]
        strain = block_means(raw[(1, links)]["time"], raw[(1, links)]["stretches"][:, 0]-1, 100, 200, 5)[:, 1]
        values = np.stack([b[:, 1] for b in blocks]); avg, sd = values.mean(0), values.std(0, ddof=1)
        for rep, ls in enumerate(("-", "--", ":")):
            ax.plot(strain, values[rep], color=color, ls=ls, alpha=.5, lw=1, label=tr(f"构型{rep+1}", f"Config. {rep+1}"))
        ax.fill_between(strain, avg-sd, avg+sd, color=color, alpha=.13)
        ax.plot(strain, avg, color="#213b40", lw=2.3, label=tr("三组平均", "Mean of three"))
        ax.axhline(0, color="#7c8788", lw=.8); ax.grid(alpha=.15)
        ax.set(title=tr(f"{links} 条新增边", f"{links} added edges"), xlabel=tr("工程应变 e", "Engineering strain e"))
    axes[0].set_ylabel(tr("法向应力差 S / (ε σ⁻³)", "Normal-stress difference S / (ε σ⁻³)"))
    axes[0].legend(frameon=False, fontsize=11)
    fig.suptitle(tr("加载段：5τ 分段平均与三组构型的离散", "Loading: 5τ block means and variation across configurations"), fontsize=18)
    save(fig, "network-stress-strain")
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.7), sharey=True, constrained_layout=True)
    fig.get_layout_engine().set(wspace=.12)
    for ax, links, color in zip(axes, (0, 80, 160), colors):
        blocks = [block_means(raw[(rep, links)]["time"], raw[(rep, links)]["stress"]-raw[(rep, links)]["baseline"], 200, 300, 10) for rep in (1, 2, 3)]
        values = np.stack([b[:, 1] for b in blocks]); avg, sd = values.mean(0), values.std(0, ddof=1)
        for rep, ls in enumerate(("-", "--", ":")):
            ax.plot(blocks[0][:, 0]-200, values[rep], ls=ls, color=color, alpha=.5, lw=1)
        ax.fill_between(blocks[0][:, 0]-200, avg-sd, avg+sd, color=color, alpha=.13)
        ax.plot(blocks[0][:, 0]-200, avg, color="#213b40", lw=2.3)
        ax.axhline(0, color="#7c8788", lw=.8); ax.grid(alpha=.15)
        ax.set(title=tr(f"{links} 条新增边", f"{links} added edges"), xlabel=tr("保持时间 / τ", "Hold time / τ"))
    axes[0].set_ylabel(tr("相对各自静置基线的 ΔS / (ε σ⁻³)", "ΔS from each resting baseline / (ε σ⁻³)"))
    fig.suptitle(tr("固定形变后：10τ 分段平均，阴影为三组间标准差", "Fixed deformation: 10τ blocks; shading is the SD across three configurations"), fontsize=17)
    save(fig, "network-stress-relaxation")
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    for links, color in zip((0, 80, 160), colors):
        shapes = np.stack([raw[(rep, links)]["shape"] for rep in (1, 2, 3)])
        time = shapes[0, :, 0]
        for ax, vals in zip(axes, (shapes[:, :, 4], shapes[:, :, 1]/np.sum(shapes[:, :, 1:4], axis=2))):
            avg, sd = vals.mean(0), vals.std(0, ddof=1)
            ax.plot(time, avg, color=color, label=tr(f"{links} 条新边", f"{links} links"))
            ax.fill_between(time, avg-sd, avg+sd, color=color, alpha=.13)
    for ax in axes:
        ax.axvspan(100, 200, color="#ece4d5", alpha=.5, zorder=0); ax.grid(alpha=.18)
        ax.axvline(100, color="#777777", lw=.7, ls=":"); ax.axvline(200, color="#777777", lw=.7, ls=":")
    axes[0].axhline(0, color="#777777", lw=.8, ls="--")
    axes[1].axhline(1/3, color="#777777", lw=.8, ls="--")
    axes[0].set_ylabel(tr("原链键取向 P₂", "Original-chain bond P₂")); axes[0].legend(frameon=False, ncol=3)
    axes[1].set(xlabel=tr("时间 / τ", "Time / τ"), ylabel=tr("链尺寸的 x 方向占比 Gxx / tr(G)", "Chain-shape x fraction Gxx / tr(G)"))
    fig.suptitle(tr("从局部键取向到整条原链的形状", "From local bond orientation to whole original-chain shape"), fontsize=18)
    save(fig, "network-chain-orientation")
    print(json.dumps(aggregate, indent=2))


if __name__ == "__main__":
    main()
```

Read thermo.dat and trajectory.lammpstrj for each branch, retaining per-configuration statistics and bilingual plots.

One detail concerns observation timing. The recording fix is defined before the deformation fix, so during loading the thermodynamic record contains the box before that step’s remapping, whereas trajectory and stage-end data output use the updated box. The difference is one 0.005τ integration step, corresponding here to a stretch-ratio difference of 0.00001. The analysis pairs stress with the actual box lengths on its own record and unwraps trajectories using their own saved boundaries. The effect on the overall figure is small, but it illustrates why precise analysis follows the actual outputs and their ordering.

For a material study, first identify the experiment being compared. The present example supplies a complete route through geometry, stress and structure for a network stretched at controlled temperature and nearly constant volume. A swollen-hydrogel study first specifies water content and equilibrated volume. Rapid impact introduces questions about heat exchange and loading duration. Crack growth or chemical fracture requires a model that permits the corresponding damage mechanisms. Equal stretch ratios do not make these physical processes equivalent. Relating preparation state, connection lifetime, volume constraints and timescale turns a runnable example into a model directed at a particular material question.

Three questions help connect an interpretation to its data. What was imposed: can direction, stretch, duration and transverse conditions be recovered from the actual cell lengths? What was measured: are stress signs, pressure components, reference windows and averaging rules defined? How did the interior respond: do bond directions, chain dimensions and temperature connect with the mechanical changes? Considering these levels together provides a concrete route for explaining differences between curves. Further studies can add independent configurations, vary loading rate or extend the holding interval, changing conditions to address a specified question while retaining the previous results for comparison.

Mechanical questions in biomaterials often span several scales. Macroscopic relaxation in a tissue or hydrated network can involve both strand rearrangement and redistribution of water, with fluid-transport times depending on specimen dimensions. The fixed-density bead–spring network without explicit solvent concentrates on chains and their connections. An extension to a hydrated model can retain the geometric checks, stress definitions and independent-replicate strategy developed here, then add measurements of solvent distribution, flow and chemical interactions. The additional physical processes acquire corresponding observables while the chain-network analysis remains useful. This provides a route toward a more complete explanation of a specific material without losing the definitions that made the initial comparison interpretable.

## Further Reading and Open Materials

- [LAMMPS 30 September 2026 Update1 — bench/in.chain](https://download.lammps.org/tars/lammps-30Sep2026_update1.tar.gz) · LAMMPS developers · GPL-2.0 software source

  FENE bead–spring foundation and the same actual networks used in L08–09.

  Add constant-volume extension, fixed-deformation holding, three independent configurations and structural/mechanical analysis, with complete protocol parameters in the lesson.
- [fix deform command](https://docs.lammps.org/fix_deform.html) · LAMMPS developers · Official documentation; cited for command semantics

  Linear length ramps, volume-preserving transverse dimensions and remap x coordinate mapping.

  Original geometry diagrams, interactive mapping and actual simulation protocols.
- [compute pressure command](https://docs.lammps.org/compute_pressure.html) · LAMMPS developers · Official documentation; cited for physical definitions

  Pressure-tensor ordering and kinetic/interaction contributions.

  Develop the normal-stress difference and analyse actual records.
- [NEMD simulations](https://docs.lammps.org/Howto_nemd.html) · LAMMPS developers · Official documentation; citation

  Distinguish solid-style coordinate mapping from fluid-flow/SLLOD arrangements.

  Explain the control conditions linking extension and rheology.
- [A Description of a Property of Caoutchouc or Indian Rubber (1805)](https://www.biodiversitylibrary.org/part/304904) · John Gough · Original historical article; BHL catalogue lists public domain; citation, no scan reproduced

  Historical subject and publication year of the natural-rubber study.

  Original diagram connecting external observations with molecular conformations.
- [On Some Thermo-Dynamic Properties of Solids (1859)](https://doi.org/10.1098/rstl.1859.0005) · James Prescott Joule · Historical research article; citation, no original text or image reproduced

  Historical study of mechanical and thermal effects together.

  Connect macroscopic measurements with modern chain models through an original conceptual diagram.
- [On Some Thermo-Dynamic Properties of Solids: original 1858 abstract, p.254](https://darwin-online.org.uk/converted/pdf/1858_Lyell_tabular_masses_A4980.pdf) · James Prescott Joule; Proceedings of the Royal Society of London · Historical primary text scan; citation and paraphrase

  Primary abstract linking mechanical action, temperature and material dimensions.

  Historical information supports the original teaching narrative; no text or image is reproduced.
