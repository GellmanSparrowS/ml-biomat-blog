# Connecting Chains into a Network

Source: https://ml-biomat.com/tutorials/molecular-dynamics/l09/en/
Language: en

Build bead–spring networks and connect link counts with clusters, periodic winding and structural relaxation.

## Why does joining chains change a material?

A bowl of cooked noodles can be separated with chopsticks, whereas a fishing net transfers a pull at one place to other parts of the net. Both contain long, flexible pieces; the difference lies in how those pieces are joined. Polymer materials raise a similar question. Some chains are close together and hinder one another through crowding and interpenetration. Others also have stable connections between chains. The recovery of rubber, the shape of many hydrogels and the load carried by an adhesive layer all depend on these connections. A dense collection of chains and a connected network therefore deserve separate descriptions. Crowding restricts motion through the surrounding material, while a permanent link continually constrains the relative separation of two selected positions.

We begin with the bead–spring melt from the previous lesson, join selected neighbouring beads on its eighty short chains, and examine what changes. A bead is a coarse structural unit, and a spring assigns an energy cost to a connection. Mapping one bead onto a particular portion of a real molecule requires material-specific parameterization. Here all beads share a common mass, length scale and energy scale, so geometry and connectivity are the central variables. The construction is useful for learning how to build a network, identify isolated clusters and inspect structural adjustment after links are introduced. For a hydrated gel, a subsequent material model would also specify interactions with water, swelling and the relevant ionic conditions.

Imagine each chain as a cord assembled from small rings. Connections along the cord already exist; additional clips join rings belonging to different original cords. A clip at an end may simply extend a route through two cords. A clip at an internal ring creates a local branch. Adding a clip between two previously separate clusters reduces the cluster count, whereas adding one inside a cluster provides an additional closed route. Each operation increases the number of links by one, but their structural consequences differ. When reading a reported crosslink density, it is therefore useful to ask exactly what is counted: links, occupied sites, or strands that participate in transmitting a load through the network.

By the end of the lesson, you will be able to reconstruct a bead-and-bond graph from a LAMMPS data file, count connected components and independent closed routes, and measure the fraction of beads in the largest component. You will also learn why periodic boundaries require an additional check. Three connection patterns derived from the same melt provide a controlled comparison of bond lengths, temperature and potential energy. The workflow first defines the molecular relationships, then places those relationships in the energy and equations of motion, and finally examines the resulting structure. The next lesson stretches these prepared systems. Separating construction from loading makes the contribution of connectivity and the influence of preparation stresses easier to interpret.

## How gelation became a connectivity problem

Step-growth polymerization presents a natural puzzle: as many smaller molecules join together, why can a single, inseparable structure eventually appear? Molecules with only two available connection sites tend to extend linear paths. Molecules with three or more potential neighbours introduce branches, which bring previously separate pieces into the same growing molecule. One newly formed chemical bond gives little information about that collective change. Considering all connections together makes it possible to discuss the largest molecule and the distribution of molecular sizes. Gelation theory therefore connects two levels of description: an individual local reaction and the connectivity of the entire population. That change of viewpoint is also useful when building a simulation network.

In 1941, Paul Flory investigated molecular-size distributions and gelation in three-dimensional polymers. Walter Stockmayer subsequently studied size distributions and gel formation in branched-chain polymers using statistical methods in 1943. Their questions linked connection probabilities and branching to the behaviour of a whole molecular population. The useful historical idea is the organization of the problem: specify the connections that can occur, then determine the structures produced when many such events accumulate. The diagram follows this idea through growing clusters. Small clusters can coexist with a large connected structure. A dominant connected component can therefore appear while some original chains remain outside it, a feature that we will measure directly in the present simulations.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/en/#en-s2)

Figure 1 · Gelation theory connects local bonding with size distributions across a molecular population. The conceptual clusters retain a small separate component beside the large one.

For computation, we describe a structure using vertices and edges. Each bead is a vertex, and each permanent bond is an edge. If one vertex can be reached from another by following edges, the two belong to the same connected component. Following a path here is a mathematical search; it does not require a bead to travel along a chain. A transit map offers a useful analogy. Whether two stations are connected by a route is a different question from where a train happens to be. Similarly, a bond graph records which beads are joined, while coordinates record their positions. Chains can bend, turn or cross periodic boundaries while retaining exactly the same graph.

In historical gelation theories, a connection probability is often related to chemical conversion. Here connections are assigned by an explicit geometrical rule: search the prepared melt for nearby beads with different original chain IDs, then select edges from that candidate list. Preserving spatial proximity makes the rule useful for studying how existing chains become joined, while the resulting structure also depends on the melt conformation, selection order and site restrictions. A model of a particular crosslinking reaction would additionally specify reactive sites, reaction conditions and the relationship between its bond-formation rule and experimental conversion. Our immediate task is to connect geometry, graph structure and spring energy, establishing an analysis that can support those more specific material models.

## Three comparable connection patterns from one melt

All three patterns start from the same prepared melt snapshot: 1,600 equal-mass beads arranged into eighty original chains, with twenty beads per chain and a reduced number density of 0.85. An open chain of twenty beads contains nineteen bonds, giving 1,520 original bonds before additional connections are introduced. We add zero, eighty or 160 connections between original chains. The word “original” matters. After joining, several original chains can belong to one connected molecule, while their molecule IDs still identify their starting chains. Retaining those IDs is useful for comparing chain dimensions before and after linking. Finding the connected molecules in the final structure requires a fresh traversal of all bonds.

Counting beads and bondsEq. 1

![Counting beads and bonds](https://ml-biomat.com/static/agent-math/34c0761ccdd5cccad86e3378.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| N | Total number of beads | 1 |
| M | Number of original open linear chains | 1 |
| n | Beads per original chain | 1 |
| B | Total number of permanent bonds | 1 |
| Bₓ | Number of added interchain bonds | 1 |
| 1 | One fewer edge than vertices in an open chain | 1 |
| =, +, − | Equality, addition and subtraction; adjacent symbols denote multiplication | 1 |

Reading the relationshipAn open chain with n vertices has n−1 edges; sum over M chains and add Bₓ new edges.

A worked exampleFor M=80 and n=20, N=1600. With Bₓ=80, B=80×19+80=1600.

ConditionsOriginal chains are equally long and open, and construction adds the specified interchain bonds.

The endpoints of a candidate edge must belong to different original chains and have a minimum-image distance no greater than 1.15σ, where σ is the bead length unit. The minimum-image calculation includes neighbours across a box boundary: beads close to opposite faces may be adjacent in periodic space. The candidate edges are then shuffled with a fixed random seed and selected in order, allowing each bead to participate in at most one added edge. This restricts the local connectivity and prevents a few beads from becoming highly connected hubs. An internal bead can acquire a third bond, while a terminal bead can acquire a second. These changes have different structural consequences, which we will examine separately.

To make the eighty-link and 160-link cases easier to compare, both use the same ordered candidate list. Its first eighty edges define the less connected case, and its first 160 define the more connected case. Every new bond in the former is therefore retained in the latter, rather than drawing two unrelated sets of edges. For each prepared melt, we save the selected bead IDs and their distances at the moment of connection. This allows a difference in the results to be traced back to actual connections instead of retaining only a single crosslink percentage. Two further independently prepared melts undergo the same procedure, exposing variation associated with starting conformations and link selection.

The common starting state and nested edge sets also illustrate controlled comparison. Within one prepared melt, the three cases share bead coordinates, velocities, box size and temperature settings; the added-edge set is the changed variable. Once links are introduced, forces change and the trajectories gradually separate. The comparison concerns statistical differences in structure and response under matched conditions, rather than requiring each bead to follow the same path in every case. The three independent melts provide a second level of comparison: how much does the outcome vary when one connection rule acts on different conformations? Separating these levels helps identify variation associated with a particular structure instead of treating it as an inevitable consequence of the rule.

An occupied-site fraction also needs a clearly stated denominator. Each added edge uses two distinct beads, and each bead is used by at most one added edge. Eighty edges therefore occupy 160 beads, or ten percent of all beads; 160 edges occupy twenty percent. This fraction describes beads selected as endpoints in the present model. Chemical conversion in a real material usually counts a specified type of reactive group and may involve side reactions or multifunctional groups. Relating the two requires a definition of how many reactive sites each bead carries. Keeping molecules, sites and edges as distinct counting levels gives a percentage a precise and useful meaning.

Occupied-site fraction and mean degreeEq. 2

![Occupied-site fraction and mean degree](https://ml-biomat.com/static/agent-math/3c99deb197ed01c1f4e0c097.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| p | Fraction of beads used by added edges | 1 |
| Bₓ | Number of added edges | 1 |
| N | Total bead count | 1 |
| d̄ | Mean number of bonds incident on a bead | 1 |
| B | Total edges, including original and added bonds | 1 |
| 2 | Two endpoints per edge | 1 |
| =, / | Equality and division; a fraction bar denotes division, adjacent symbols multiplication | 1 |

Reading the relationshipCount both endpoints of every edge. Each bead is used by at most one added edge, so the number of added endpoints equals the number of occupied beads. The total degree counts every bond twice.

A worked exampleWith Bₓ=80 and N=1600, p=160/1600=0.10. With B=1600 total bonds, d̄=3200/1600=2.

ConditionsThe expression for p uses the one-added-edge-per-bead rule; the mean-degree expression applies to the undirected bond graph.

## Writing new connections and updating neighbour relationships

In the Bonds section of a LAMMPS data file, each row records one bond: its identifier, its bond type and the atom IDs of its two endpoints. IDs support lookup and tracking; the type selects an interaction parameter set. Original chain bonds are type 1, and newly added connections are type 2. Both use identical FENE parameters, so the type label distinguishes their origin rather than their stiffness. A FENE spring resists extension increasingly strongly as its length approaches a limiting value. Here that value is 1.5σ, a boundary of the potential function. Investigating chemical rupture or reversible binding would require a connection model and parameters that include those processes.

Adding a bond introduces a spring energy and changes which beads count as directly bonded neighbours. In the present model, the FENE bond already includes short-range bead repulsion. The setting special_bonds fene therefore assigns zero weight to the ordinary nonbonded interaction of directly bonded beads, while pairs separated by two or three bonds retain unit weight. Directly bonded beads receive their repulsion through the bond potential, and ordinary neighbours receive it through the pair potential. Reading the updated data file lets LAMMPS construct these relationships from the new topology. Other force fields may scale two-bond and three-bond neighbours differently, so their corresponding rules need to be checked whenever connectivity changes.

We construct each complete topology before reading it into LAMMPS. The generator prepares the melt, builds and orders candidate edges, writes three network.data files, and generates a complete simulation input for each case. It saves the configuration seed, selected links and result directory together so that the comparison can be reproduced. Each case then proceeds through fixed-volume relaxation, volume-preserving uniaxial extension and a hold at fixed deformation. This lesson analyses the first stage; the next lesson uses the latter two. Keeping the stages in one executable workflow ensures that the mechanical comparison continues from the same prepared network states, while separate data and restart files preserve the individual stages.

### Complete construction and simulation program

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

Generate three nested connection cases, retain every added edge, and run relaxation, extension and holding stages. One replicate defaults to 1,600 beads; --replica changes the independently prepared configuration.

### Complete LAMMPS input for configuration 1 with 80 links

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

The construction program writes this input; run it beside its network.data. This lesson uses the first 100τ, while the following extension and holding records serve the next lesson.

Execute run.sh in the folder containing the two Python files and the shell script. It prepares three independent melts, produces three connection patterns from each melt, and generates the figures and numerical tables for this lesson. The example uses reduced units: lengths are expressed in σ, energies in ε, times in τ and the temperature target is T*=1. Conversion to nanometres, picoseconds or a physical temperature requires a chosen mapping for these scales. Directory names record bead counts and replicate numbers, while the analysis checks chain counts, link counts and file contents. For an initial construction exercise, a single generator command can use 640 beads. The statistics and figures discussed here use three 1,600-bead configurations.

### Run three configurations and generate bilingual figures

```
#!/usr/bin/env bash
set -euo pipefail
for replica in 1 2 3; do
  python run_network.py --beads 1600 --replica "$replica" --out-dir network-runs
done
python analyze_network.py network-runs --out network-analysis/en --language en
python analyze_network.py network-runs --out network-analysis/zh --language zh
```

Run in the directory containing run_network.py, analyze_network.py and run.sh. Select the LAMMPS executable through --lmp or the LAMMPS environment variable.

## Large clusters, closed routes and dangling portions

To identify connectivity, start at any bead that has not yet been visited, find all of its bonded neighbours, then find their neighbours, continuing until no new bead can be added. The collected beads form one connected component. Start again from another unvisited bead and repeat until every bead has been assigned. This procedure, a graph traversal, can be implemented with a list of pending vertices. Before links are added, each original chain forms its own component, giving eighty components of twenty beads each. Added links may merge components while bead positions continue to fluctuate thermally. Determining membership from the bond list and then examining shape through coordinates keeps these two questions organized.

Largest-component fractionEq. 3

![Largest-component fraction](https://ml-biomat.com/static/agent-math/4ebb9e2b58f74ffad9f5fb1b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| Pₘₐₓ | Fraction of beads in the largest connected component | 1 |
| Nₘₐₓ | Number of beads in the largest component | 1 |
| N | Total system bead count | 1 |
| max | Subscript selecting the largest of all components | 1 |
| =, / | Equality; the fraction bar denotes division | 1 |

Reading the relationshipDividing the component bead count by the system count gives the fraction of all beads that belong to that component.

A worked exampleFor the first 80-link case, Nₘₐₓ=63×20=1260 and Pₘₐₓ=1260/1600=0.7875.

ConditionsBeads have equal masses here, so bead and mass fractions coincide. Unequal masses require summing masses for a mass fraction.

After eighty edges are added to the first configuration, thirteen components remain. The largest contains sixty-three original chains, or 1,260 beads, giving a largest-component fraction of 0.7875. With 160 added edges, two components remain and the largest contains seventy-nine original chains, a fraction of 0.9875. Doubling the link count still leaves one original chain outside the largest component. At eighty links, the second and third configurations contain thirteen and eighteen components respectively; their largest components each contain sixty-two original chains. The differences arise from their spatial conformations and specific selected edges. Showing all three results reveals the structures produced by the construction rule more clearly than a dense-looking network picture alone.

### Connectivity of three actual network configurations

Points are measured from each configuration’s actual bond list; lines guide comparison across added-edge counts. Largest-component fractions, component counts and independent-cycle counts describe different features.

LAMMPS 30 Sep 2026 Update 1; official bead–spring interaction model, with 1600 beads in 80 chains of 20, ρ*=0.85 and T*=1, using three initial configurations. The FENE/WCA dynamics time step is 0.005τ.

[Download reference data and complete inputs (ZIP) 2.33 MB](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/lammps-network-connectivity-data.zip)

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/en/#en-s5)

Adding 0, 80 or 160 permanent links to each of three initial melts gives nine topologies. Largest-component fraction, independent-cycle count and periodic winding rank are computed from the actual bond tables and initial coordinates, then checked against the structures after 100τ of relaxation. Link count and network structure are measured separately.

Consider what one additional edge does. If it joins two previously separate components, the component count decreases by one and the edge count increases by one. If its endpoints were already connected by a path, the edge creates an additional independent closed route. Independence means that the route adds a cycle beyond those obtainable from the earlier cycle basis. Graph theory counts these cycles as the number of edges minus the number of vertices plus the number of components. Initially every chain is a tree, with no closed route. In the first eighty-link case, sixty-seven links merge eighty components into thirteen; the remaining thirteen supply independent cycles. This count also helps detect missing connections in an analysis.

Counting independent cyclesEq. 4

![Counting independent cycles](https://ml-biomat.com/static/agent-math/13f6200a36cd44df7485535b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| μ | Number of independent cycles, or graph cycle rank | 1 |
| B | Total edge count; multiple edges between original chains are counted separately | 1 |
| N | Number of vertices in the bead graph | 1 |
| C | Number of connected components | 1 |
| =, −, + | Equality, subtraction and addition | 1 |

Reading the relationshipA forest with C components needs N−C edges; each additional edge contributes an independent cycle.

A worked exampleAfter 80 links in configuration 1, B=1600, N=1600 and C=13, giving μ=13. With 160 links, μ=1680−1600+2=82.

ConditionsThis is a topological count for the finite undirected graph; periodic winding directions are checked separately through closure displacements.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/en/#en-s5)

Figure 2 · One added edge merges two separate components or creates an independent cycle within an existing component.

Local degrees provide another calculation that can be checked by hand. Before linking, the eighty chains have 160 terminal beads of degree one and 1,440 internal beads of degree two. In the first eighty-link case, the new links use twenty-one terminal beads and 139 internal beads. The final counts are therefore 139 beads of degree one, 1,322 of degree two and 139 of degree three. These counts sum to 1,600; their degree sum is twice the total bond count because every bond has two endpoints. A mean degree of two can consequently coexist with branches and dangling ends. Inspecting the full distribution reveals structural features hidden by that average.

Contracting each original chain into one vertex makes the added connections easier to inspect. The figure places eighty vertices around a circle to arrange their identifiers clearly; its lines come from the actual selected interchain links. Several links may join the same pair of original chains, and the calculation retains them as separate edges. This graph emphasizes who is connected to whom, while a molecular trajectory emphasizes spatial conformation. Dangling portions also deserve attention. A terminal strand can fluctuate without constraining two network junctions in the same way as a strand joining them. Interpreting elastic response requires considering junctions, dangling branches, cycles and the loading direction together.

### Contracting the 80 original chains of configuration 1

Vertices are arranged by original chain ID around a circle, with lines representing actual added links. Teal identifies the largest component and orange the others. All zero-link components are equally large and shown in orange. Multiple links between two original chains overlap visually and remain separate in calculations.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/en/#en-s5)

Each node represents one original 20-bead chain, placed around a circle in chain-index order. Edges are the actual added interchain links. The circular layout displays connectivity clearly; three-dimensional geometry is stored separately in the simulation coordinates.

[Figure: Connection graph for eight original chains](https://ml-biomat.com/tutorials/molecular-dynamics/l09/en/#en-s5)

Each vertex represents one original chain; edges are added links. Positions arrange the labels and colours distinguish connected components.

A graph exercise with eight original chains: compare cluster and cycle counts at equal edge counts but different connection orders.

## Crossing a boundary and winding through a periodic network

Periodic boundaries repeat a small box in three directions. A bead leaving the right face continues at the corresponding position on the left. For a finite chain, neighbouring periodic images can be chosen along its bonds so that the whole chain appears continuous in an unwrapped space. Additional connections introduce an interesting possibility: following a closed bond route can return to a different periodic image of the starting bead. These positions share one bead ID in the primary box but differ by one or more box lengths in the repeated space. Such a closed route shows that the connected network extends through periodic replicas rather than remaining a finite cluster inside a single box.

Seeing a bond cross a boundary is insufficient to distinguish the two cases. A short finite chain may happen to straddle the left and right faces and can be displayed as an ordinary continuous chain after choosing suitable images. A stronger test adds the minimum-image bond displacements around a closed route. A route that returns to its starting position in a finite region has zero total displacement. A route that ends at another periodic image has a displacement equal to box lengths multiplied by a nonzero integer vector. Its three components count net box crossings in the three directions. The analysis uses this test to distinguish local closed loops from routes connecting different periodic images.

Accumulating periodic displacements around a closed routeEq. 5

![Accumulating periodic displacements around a closed route](https://ml-biomat.com/static/agent-math/87916823504495865d28552b.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| 𝒞 | A closed bond route with a chosen traversal direction | 1 |
| k | An individual bond segment on the route | 1 |
| Δrₖ | Minimum-image bond displacement in the traversal direction | σ |
| Σ, ∈ | Sum over the segments of the specified route; membership in a set | 1 |
| Lₓ, Lᵧ, L𝓏 | Three lengths of the orthogonal box | σ |
| w, wₓ, wᵧ, w𝓏 | Integer winding vector and its three components | 1 |
| ℤ³ | Set of vectors with three integer components | 1 |
| =, (, ), , | Equality; parentheses and commas arrange x, y and z vector components; adjacent symbols multiply | 1 |

Reading the relationshipOne bead ID in the primary box has multiple images in unwrapped space. A closed route therefore accumulates integer multiples of the box lengths.

A worked exampleFor box lengths of 10σ, an accumulated displacement (10σ,0,0) gives w=(1,0,0), one winding in x. Zero accumulated displacement gives w=(0,0,0).

ConditionsFor an orthogonal periodic box, each bond uses a minimum image shorter than half a box length, as satisfied here.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/en/#en-s6)

Figure 3 · Left: a finite chain crosses a boundary. Right: a closed bead-ID route reaches a neighbouring image of its start, winding once in x.

If all nonzero winding vectors lie along the same direction, they provide one independent direction of periodic extension. A second or third direction increases this count when it cannot be formed from combinations of the previous directions. The rank of the winding-vector set measures that independence: ranks one, two and three indicate one, two and three independent directions. This concerns directional independence rather than how long a route appears. For example, vectors (1,0,0) and (2,0,0) still span only one direction. Adding (0,1,0) creates a second. The analysis saves the underlying integer vectors, allowing the rank calculation to be traced back to the closed routes that produced them.

For all six linked systems, the largest component has winding rank three both immediately after construction and after 100τ of relaxation. The unlinked systems contain eighty finite original chains. The linked cases have therefore established periodic connectivity in three independent directions. Together with the largest-component fraction, this describes network topology; an elastic modulus also depends on strand conformations, temperature, relaxation and the loading protocol. There is a practical geometrical consequence as well. A periodically connected network generally cannot be assigned one image for every bead that makes all closed routes close in a finite unwrapped space. Whole-network dimensions consequently require a careful definition, while the retained original-chain IDs still support size measurements for the individual finite chains.

Box size is another scale to control. Periodic repetition makes a local structure recur throughout space, and changing the box size or chain count can change the probability of obtaining winding routes. A study of the gelation threshold would therefore construct multiple system sizes at several connection fractions and measure how large clusters and periodic winding change across them. The three link counts here provide concrete networks for learning structural analysis and mechanical loading. Extending such observations into a system-size series addresses the broader question of when a macroscopic connected network emerges, while helping separate effects associated with periodic repetition from those of bulk connectivity.

## Why a newly connected network needs to relax

The candidate-distance limit keeps a new bond away from the FENE extension limit at construction, but it does not place every new bond near its preferred length. Two neighbouring beads in a melt originally balance nonbonded repulsion and surrounding packing. Adding a spring introduces an additional elastic force. In the first eighty-link configuration, the mean added-bond length decreases from 1.0791σ initially to 0.9665σ after 100τ. Original chain bonds have a mean length of about 0.9651σ before connection. This comparison shows how geometrical proximity evolves into a distance distribution shaped by the spring. Shortening a bond also moves neighbouring strands, so local stress redistribution involves coordinated motion throughout the surrounding material.

### Added bonds adjust from geometrical proximity to spring constraints

Left: the three configurations are pooled separately for 80 and 160 links; dashed curves show construction and solid curves show 100τ. Right: the six linked systems retain their individual largest-bond-length records. The FENE maximum-extension parameter is 1.5σ.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/en/#en-s7)

Added links are compared by identity before and after 100τ of relaxation. Distances use the minimum periodic displacement, in units of σ. Original backbone bonds and added links are counted separately; the FENE model sets the maximum extension parameter R₀=1.5σ.

At the instant of linking, bead positions and velocities can remain unchanged while the potential energy changes, because the energy function now contains additional connections. For this model, repulsion for each newly bonded pair moves from the nonbonded WCA term to the identical repulsive term inside the FENE bond. At fixed coordinates, these contributions match exactly. The difference between the old and new potential energies therefore consists of the added FENE elastic terms. The first eighty-link case gains 1.24037ε per bead, matching an independent sum evaluated from the saved new-bond lengths. This is a useful check that the bonds were added, their parameters are correct and repulsion has been counted once.

Energy added by links at fixed coordinatesEq. 6

![Energy added by links at fixed coordinates](https://ml-biomat.com/static/agent-math/e54c6ec00f905aa9880a1fd1.svg)

| Symbol | Meaning | Unit |
| --- | --- | --- |
| ΔU | Increase in total potential energy after adding the specified links | ε |
| N | Total number of beads | 1 |
| K | FENE elastic coefficient, 30ε/σ² here | ε/σ² |
| R₀ | Maximum-extension parameter, 1.5σ here | σ |
| Bₓ, j | Added-bond count and one bond index | 1 |
| rⱼ | Initial minimum-image length of added bond j | σ |
| Σ | Sum over j from 1 to Bₓ | 1 |
| ln | Natural logarithm of a positive dimensionless quantity | 1 |
| ² | Square, multiplication by itself | 1 |
| Δ, =, −, / | Change marker, equality, negation or subtraction, division; adjacent quantities multiply | 1 |
| 1, 2, [, ], (, ) | Constants one and two; brackets group operations | 1 |

Reading the relationshipThe WCA repulsion inside each new bond replaces the identical previous nonbonded WCA term. The remaining difference is the FENE elastic energy, summed over links and divided by N.

A worked exampleFor one new bond with r=1σ, the elastic increment is −(30×1.5²/2)ln(1−1/1.5²)=19.8378ε. At N=1600, this contributes 0.0123986ε per bead. Summing the 80 actual bond lengths gives 1.24037191ε per bead.

ConditionsCompare identical coordinates with matching WCA parameters and special_bonds fene, with 0<rⱼ<R₀ for every bond. This is the potential-energy change caused by the linking operation.

Once integration begins, stretched new bonds contract and potential energy can become kinetic energy. The thermostat exchanges energy with the system so that temperature fluctuates around T*=1. We retain a Langevin thermostat with a damping time of 1τ and a time step of 0.005τ. Showing potential-energy adjustment beside temperature connects these processes: the thermostat regulates motion statistics, while structural relaxation appears in bond lengths, strand shapes and energy changes over time. Each potential-energy curve is measured from its own branch starting value to show that branch’s adjustment. The three topologies contain different numbers of interaction terms, so an absolute-energy comparison also needs the link count and the energy definition.

### Temperature and energy adjustment for three topologies from one starting state

Actual records from 0–100τ for configuration 1. The dashed temperature line is T*=1; potential energies are differences from each branch’s own start, in ε per bead.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/l09/en/#en-s7)

Fixed-volume relaxation records over 0–100τ for all nine systems. Temperature uses the model’s reduced units and potential energy is normalized by 1600 beads. Curves retain the energy changes associated with each initial link set, preceding structural and mechanical comparison under a common preparation protocol.

Monitoring the largest bond length reveals whether any local connection approaches the extension boundary. Rechecking component counts, cycle counts and winding ranks confirms that relaxation retains the intended connectivity. With permanent bonds, the changes over these 100τ arise mainly from rearrangement of bead positions. If temperature has settled while strand shapes or stresses continue to evolve slowly, a longer preparation interval can measure that continuing adjustment. We save both data and restart files at the end of relaxation so that subsequent extension begins from the same state. The network construction, preparation duration and remaining structural features can then be kept explicit when interpreting the mechanical comparison.

Fixed-volume preparation preserves a specific material condition: the network cannot remove linking stresses by changing its overall volume. A real hydrogel may take up or release water, with its dimensions determined jointly by elastic constraints and solvent interactions. A material confined by a mould or substrate may instead be prepared under fixed-volume or partly fixed-dimension conditions. Choosing a preparation protocol should therefore follow the experiment being interpreted. Here the box retains its original density while beads rearrange inside it. Subsequent loading measures the response of that fixed-density network under the stated thermal and loading conditions. A variable-volume comparison could then investigate how preparation constraints affect the initial stress.

## From connectivity statistics to an interpretable material comparison

The complete analysis program connects these checks into one workflow. It reads the initial and relaxed networks for all nine cases, reconstructs bonds by bead ID, verifies edge endpoints, distance limits and nested link sets, and calculates components, cycles and periodic winding. It then reads temperature and energy records, selects the preparation interval from zero to 100τ, and plots comparisons using consistent definitions. Numerical results are also written to JSON and CSV for further analysis. The connectivity plots retain the three starting configurations separately, while bond-length histograms pool equal-link-count cases across the three configurations to compare construction with relaxation. Reading the statistical object and pooling rule alongside each figure clarifies what its curves answer.

### Complete graph, periodic-winding and relaxation analysis

```
"""Measure the actual fixed-topology networks and their initial relaxation.

python analyze_network.py network-runs --out network-analysis --language en
Requires NumPy and Matplotlib. The input directory contains n1600-rep1/2/3.
Each replica contains links-0/80/160 with network.data, relaxed.data,
selected-crosslinks.json and thermo.dat. 
"""
from pathlib import Path
import argparse
import csv
import json
import re

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.collections import LineCollection


def read_data(path):
    """Read the orthogonal atom_style bond files used in this example."""
    text = path.read_text(encoding="utf-8")
    sections, section = {}, None
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if re.fullmatch(r"[A-Za-z][A-Za-z ]*", line):
            section = line
            sections[section] = []
        elif section:
            sections[section].append(line.split())
    atoms = np.asarray(sections["Atoms"], float)
    atoms = atoms[np.argsort(atoms[:, 0])]
    assert np.array_equal(atoms[:, 0], np.arange(1, len(atoms) + 1))
    bonds = np.asarray(sections["Bonds"], int)
    bounds = []
    for direction in "xyz":
        found = re.search(rf"^([\d.eE+\-]+)\s+([\d.eE+\-]+)\s+{direction}lo {direction}hi", text, re.M)
        bounds.append([float(found[1]), float(found[2])])
    bounds = np.asarray(bounds)
    return {"xyz": atoms[:, 3:6], "mol": atoms[:, 1].astype(int),
            "box": bounds[:, 1]-bounds[:, 0], "bonds": bonds}


def bond_geometry(data):
    ends = data["bonds"][:, 2:4] - 1
    delta = data["xyz"][ends[:, 1]] - data["xyz"][ends[:, 0]]
    shift = -np.rint(delta / data["box"]).astype(int)
    minimum_image = delta + shift * data["box"]
    return ends, shift, np.linalg.norm(minimum_image, axis=1)


def connectivity(data):
    """Graph components, cycle counts and independent periodic directions.

    Integer image offsets are propagated along a spanning tree. A cycle that
    closes at a different periodic image leaves a nonzero integer vector.
    The rank of these vectors counts independent periodic winding directions.
    """
    n = len(data["xyz"])
    ends, shifts, lengths = bond_geometry(data)
    graph = [[] for _ in range(n)]
    for edge_id, ((i, j), shift) in enumerate(zip(ends, shifts)):
        graph[i].append((j, shift, edge_id))
        graph[j].append((i, -shift, edge_id))
    labels = np.full(n, -1, int)
    offsets = np.zeros((n, 3), int)
    components = []
    for root in range(n):
        if labels[root] >= 0:
            continue
        label = len(components)
        labels[root] = label
        stack, vertices, edge_ids, closures = [root], [], set(), []
        while stack:
            i = stack.pop()
            vertices.append(i)
            for j, shift, edge_id in graph[i]:
                edge_ids.add(edge_id)
                trial = offsets[i] + shift
                if labels[j] < 0:
                    labels[j] = label
                    offsets[j] = trial
                    stack.append(j)
                else:
                    assert labels[j] == label
                    closure = trial - offsets[j]
                    if np.any(closure):
                        closures.append(closure.tolist())
        unique_closures = np.unique(closures, axis=0) if closures else np.empty((0, 3), int)
        rank = int(np.linalg.matrix_rank(unique_closures.astype(float), tol=1e-10)) if len(unique_closures) else 0
        components.append({"beads": len(vertices), "edges": len(edge_ids),
                           "original_chains": len(np.unique(data["mol"][vertices])),
                           "independent_cycles": len(edge_ids)-len(vertices)+1,
                           "winding_rank": rank,
                           "integer_closure_vectors": unique_closures.tolist()})
    largest_id = int(np.argmax([c["beads"] for c in components]))
    largest = components[largest_id]
    degree = np.array([len(x) for x in graph])
    return {"components": components, "component_count": len(components),
            "largest": largest, "largest_id": largest_id, "labels": labels,
            "total_cycles": len(ends)-n+len(components), "degree": degree,
            "lengths": lengths, "ends": ends}


def numeric_rows(path):
    return np.loadtxt(path, comments="#")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path, default=Path("network-analysis"))
    parser.add_argument("--language", choices=("en", "zh"), default="en")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    records, raw = [], {}
    for replica in (1, 2, 3):
        base = args.directory / f"n1600-rep{replica}"
        previous_edges = set()
        for count in (0, 80, 160):
            folder = base / f"links-{count}"
            before = read_data(folder / "network.data")
            after = read_data(folder / "relaxed.data")
            graph = connectivity(before)
            later = connectivity(after)
            n = len(before["xyz"])
            assert n == 1600 and len(np.unique(before["mol"])) == 80
            selected = json.loads((folder / "selected-crosslinks.json").read_text(encoding="utf-8"))["selected"]
            chosen = {tuple(sorted((int(x[0]), int(x[1])))) for x in selected}
            assert len(chosen) == count and previous_edges <= chosen
            previous_edges = chosen
            added = before["bonds"][:, 1] == 2
            endpoints = graph["ends"][added]
            assert len(endpoints) == count
            assert len(np.unique(endpoints)) == 2*count
            assert np.all(before["mol"][endpoints[:, 0]] != before["mol"][endpoints[:, 1]])
            assert np.all(graph["lengths"][added] <= 1.15 + 1e-10)
            assert graph["component_count"] == later["component_count"]
            assert graph["largest"]["winding_rank"] == later["largest"]["winding_rank"]
            # Equal masses make the largest bead fraction a mass fraction too.
            largest_fraction = graph["largest"]["beads"] / n
            t = numeric_rows(folder / "thermo.dat")
            t = t[(t[:, 1] >= 0) & (t[:, 1] <= 100)]
            assert len(t) == 201
            elastic_added = float(np.sum(-.5*30*1.5**2*np.log1p(-(graph["lengths"][added]/1.5)**2)))
            if count == 0:
                reference_energy = t[0, 3]
            observed_change = float(t[0, 3]-reference_energy)
            assert abs(observed_change-elastic_added/n) < 1e-9
            assert np.max(graph["degree"]) <= 3
            old_lengths = graph["lengths"][~added]
            new_lengths = graph["lengths"][added]
            relaxed_new = later["lengths"][after["bonds"][:, 1] == 2]
            rec = {"replica": replica, "added_links": count,
                   "beads": n, "total_bonds": len(before["bonds"]),
                   "component_count": graph["component_count"],
                   "largest_component_beads": graph["largest"]["beads"],
                   "largest_component_chains": graph["largest"]["original_chains"],
                   "largest_mass_fraction": largest_fraction,
                   "total_independent_cycles": graph["total_cycles"],
                   "largest_winding_rank": graph["largest"]["winding_rank"],
                   "modified_bead_fraction": 2*count/n,
                   "mean_degree": float(graph["degree"].mean()),
                   "degree_counts": {str(k): int(np.sum(graph["degree"] == k)) for k in (1, 2, 3)},
                   "initial_U_change_per_bead": observed_change,
                   "sum_added_FENE_elastic_per_bead": elastic_added/n,
                   "original_bond_initial_mean": float(old_lengths.mean()),
                   "added_bond_initial_mean": float(new_lengths.mean()) if count else None,
                   "added_bond_after_100tau_mean": float(relaxed_new.mean()) if count else None,
                   "max_bond_before": float(graph["lengths"].max()),
                   "max_bond_after_100tau": float(later["lengths"].max()),
                   "late_50_100tau_temperature_mean": float(t[t[:, 1] >= 50, 2].mean()),
                   "components": graph["components"]}
            records.append(rec)
            raw[(replica, count)] = (before, after, graph, later, t)
    summary = {"case": "fixed FENE networks", "records": records,
               "topology": "All edges retained, including parallel connections between original chains.",
               "winding": "Rank of integer closure vectors; connectivity is distinct from mechanical response.",
               "time_scope": "Topology at insertion; before/after100tau fixed-volume relaxation. All statistics are finite-window descriptors."}
    (args.out / "network_summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    table = [{k: v for k, v in rec.items() if k not in ("components", "degree_counts")} for rec in records]
    with (args.out / "network_metrics.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(table[0]))
        writer.writeheader()
        writer.writerows(table)
    zh = args.language == "zh"
    def tr(cn, en):
        return cn if zh else en
    candidates = ["Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Zen Hei", "DejaVu Sans"] if zh else ["DejaVu Sans"]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams.update({"font.family": [f for f in candidates if f in installed],
                         "font.size": 14, "svg.fonttype": "path", "axes.spines.top": False,
                         "axes.spines.right": False, "axes.unicode_minus": False})
    colors = ["#187e89", "#ca713f", "#7663a0"]
    def save(fig, name):
        fig.savefig(args.out / f"{name}.svg")
        fig.savefig(args.out / f"{name}.png", dpi=150)
        plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    for replica, color in enumerate(colors, 1):
        rr = [x for x in records if x["replica"] == replica]
        for ax, key in zip(axes, ["largest_mass_fraction", "component_count", "total_independent_cycles"]):
            ax.plot([x["added_links"] for x in rr], [x[key] for x in rr], "o-", color=color,
                    label=tr(f"构型 {replica}", f"Configuration {replica}"), alpha=.8)
    axes[0].set_ylabel(tr("最大连通分量质量分数", "Largest-component mass fraction"))
    axes[0].set_ylim(0, 1.05)
    axes[1].set_ylabel(tr("连通分量数", "Connected components"))
    axes[2].set_ylabel(tr("独立环数 E − V + C", "Independent cycles E − V + C"))
    for ax in axes:
        ax.set_xlabel(tr("新增连接数", "Added connections")); ax.set_xticks([0, 80, 160]); ax.grid(alpha=.2)
    axes[0].legend(frameon=False, fontsize=11)
    fig.suptitle(tr("同一熔体逐步加边：哪些链已经连在一起", "Adding edges to each melt: which chains are connected"), fontsize=19)
    save(fig, "network-connectivity")
    # A chain-level circular graph is a connectivity drawing, not a spatial projection.
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.6), constrained_layout=True)
    theta = np.linspace(0, 2*np.pi, 80, endpoint=False)
    positions = np.column_stack([np.cos(theta), np.sin(theta)])
    for ax, count in zip(axes, (0, 80, 160)):
        data, _, graph, _, _ = raw[(1, count)]
        selected = data["bonds"][:, 1] == 2
        chain_ends = data["mol"][graph["ends"][selected]]-1
        segments = positions[chain_ends]
        if len(segments):
            ax.add_collection(LineCollection(segments, colors="#6c9c99", linewidths=.7, alpha=.5))
        chain_labels = graph["labels"][np.arange(80)*20]
        in_largest = chain_labels == graph["largest_id"]
        # At zero links all components are tied; use the same color for all chains.
        node_colors = np.where(in_largest, "#177d88", "#d59564") if count else ["#d59564"]*80
        ax.scatter(positions[:, 0], positions[:, 1], c=node_colors, s=26, zorder=3)
        rr = next(x for x in records if x["replica"] == 1 and x["added_links"] == count)
        ax.set_title(tr(f"{count} 条新增边", f"{count} added edges"))
        ax.text(0, -1.3, tr(f"最大分量：{rr['largest_component_chains']}/80 条链", f"Largest component: {rr['largest_component_chains']}/80 chains"), ha="center", fontsize=12)
        ax.set_aspect("equal"); ax.set_xlim(-1.12, 1.12); ax.set_ylim(-1.46, 1.15); ax.axis("off")
    fig.suptitle(tr("构型 1 的连接图：每个圆点代表一条原始链", "Configuration 1 connectivity: one node per original chain"), fontsize=18)
    save(fig, "network-chain-graph")
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2), constrained_layout=True)
    bins = np.linspace(.85, 1.20, 36)
    for count, color in zip((80, 160), colors[:2]):
        for stage, linestyle in [(0, "--"), (1, "-")]:
            vals = []
            for replica in (1, 2, 3):
                before, after, graph, later, t = raw[(replica, count)]
                dat, gg = (before, graph) if stage == 0 else (after, later)
                vals.extend(gg["lengths"][dat["bonds"][:, 1] == 2])
            axes[0].hist(vals, bins=bins, density=True, histtype="step", lw=2, color=color, linestyle=linestyle,
                         label=f"{count}: " + (tr("刚加边", "Just connected") if stage == 0 else tr("100τ 后", "After 100τ")))
    for replica, color in enumerate(colors, 1):
        for count, linestyle in [(80, "--"), (160, "-")]:
            t = raw[(replica, count)][4]
            axes[1].plot(t[:, 1], t[:, 12], color=color, ls=linestyle, lw=1.1, alpha=.7,
                         label=tr(f"构型{replica} · {count}边", f"Config. {replica} · {count} links"))
    axes[0].set(xlabel=tr("新增键长 / σ", "Added-bond length / σ"), ylabel=tr("概率密度 / σ⁻¹", "Probability density / σ⁻¹"))
    axes[1].set(xlabel=tr("加边后的时间 / τ", "Time after adding edges / τ"), ylabel=tr("全体系最大键长 / σ", "Largest bond length / σ"))
    for ax in axes:
        ax.legend(frameon=False, fontsize=10, loc="lower center", bbox_to_anchor=(.5, 1.02), ncol=2); ax.grid(alpha=.2)
    fig.suptitle(tr("连接后的局部几何松弛", "Local geometrical relaxation after adding connections"), fontsize=19)
    save(fig, "network-bond-relaxation")
    fig, axes = plt.subplots(2, 1, figsize=(12, 7.4), sharex=True, constrained_layout=True)
    for count, color in zip((0, 80, 160), colors):
        t = raw[(1, count)][4]
        axes[0].plot(t[:, 1], t[:, 2], color=color, lw=1.1, label=tr(f"{count} 条新增边", f"{count} added edges"))
        axes[1].plot(t[:, 1], t[:, 3]-t[0, 3], color=color, lw=1.3)
    axes[0].axhline(1, color="#6d7779", ls="--", lw=1)
    axes[0].set_ylabel(tr("温度 T*", "Temperature T*")); axes[0].legend(frameon=False, loc="lower center", bbox_to_anchor=(.5, 1.02), ncol=3, fontsize=11)
    axes[1].set(xlabel=tr("加边后的时间 / τ", "Time after adding edges / τ"), ylabel=tr("相对各分支起点的 Δ(U/N) / ε", "Δ(U/N) from each branch's start / ε"))
    for ax in axes:
        ax.grid(alpha=.2)
    fig.suptitle(tr("构型 1：固定连接后的温度与势能调整", "Configuration 1: temperature and energy after fixing the connections"), fontsize=18)
    save(fig, "network-preparation")
    print(json.dumps(table, indent=2))


if __name__ == "__main__":
    main()
```

Analyse the three n1600-rep directories under network-runs, each containing links-0, links-80 and links-160. Outputs include four figure groups and per-condition JSON and CSV records.

Returning to the material question, added links clearly change these structures: the largest component generally incorporates more original chains, the number of independent cycles increases, and the distribution of local degrees changes. After eighty links are added to the first configuration, the average bead degree is exactly two, yet beads of degree one, two and three coexist. Their average conceals where branches are located. Likewise, a largest-component fraction near one can coexist with dangling portions, local loops and routes extending through periodic space. Describing a network through several complementary measurements therefore gives a more informative structural picture than expecting a single crosslink-density number to explain every feature.

For a biomaterial application, first identify the connections that matter physically. A chemically crosslinked hydrogel can represent stable covalent connections as permanent edges while treating the solvent separately. Reversible associations in a physical gel require a model for binding probabilities or lifetimes. Protein-based networks may add directional interactions, specific binding sites and changing conformations. Each choice affects the retained motions, the connections that can change and the mapping between simulation time and experiment. The equal-mass bead–spring system provides a clear starting point: establish topology and spatial constraints, then add the molecular features required by the material so that each increase in complexity addresses a specific question.

Before the next comparison, retain a compact structural record for each system: original chain count and length, the added-edge list, largest-component fraction, independent cycle count, periodic winding directions and the relaxed endpoint. A mechanical comparison then adds loading rate, temperature, volume change and the stress definition. If one network responds more softly than another during extension, its connection locations and starting conformation can be examined alongside the measured response. The next lesson follows this sequence using the same network set: calculate extension from the actual box lengths, obtain tensile stress from the pressure tensor, and observe how stress evolves after deformation is held fixed while the strands continue to adjust.

## Further Reading and Open Materials

- [LAMMPS 30 September 2026 Update 1 — bench/in.chain](https://download.lammps.org/tars/lammps-30Sep2026_update1.tar.gz) · LAMMPS developers · GPL-2.0 software source

  FENE bead–spring interactions, reduced units and Langevin/integrator combination.

  Retain the L08 teaching melt: 1,600 beads, 80 chains of 20 beads, density 0.85, exact WCA cutoff, time step 0.005τ and thermostat damping 1τ. Add permanent-link selection, three configurations, relaxation/extension protocols and complete graph analysis.
- [bond_style fene; special_bonds; read_data](https://docs.lammps.org/bond_fene.html) · LAMMPS developers · Official documentation; cited for definitions

  FENE energy terms, directly bonded repulsion and data topology.

  Explanations, worked examples and diagrams are newly written.
- [special_bonds command](https://docs.lammps.org/special_bonds.html) · LAMMPS developers · Official documentation; cited for command semantics

  The fene weights 0, 1, 1 and bond-topology definitions of special neighbours.

  Explain interaction counting when adding connections.
- [read_data command](https://docs.lammps.org/read_data.html) · LAMMPS developers · Official documentation; cited for command semantics

  Bonds data format and image relationships in periodic connected systems.

  Original route diagrams and periodic-winding analysis.
- [Molecular Size Distribution in Three Dimensional Polymers. I. Gelation (1941)](https://doi.org/10.1021/ja01856a061) · Paul J. Flory · Research article citation; no original text or image reproduced

  Historical connection between gelation and molecular-size distributions.

  Explain the scientific question through original cluster diagrams.
- [Theory of Molecular Size Distribution and Gel Formation in Branched-Chain Polymers (1943)](https://doi.org/10.1063/1.1723803) · Walter H. Stockmayer · Research article citation; no original text or image reproduced

  Statistical treatment of branching and gel formation.

  Historical account checked against a public scholarly memoir.
- [Walter Hugo Stockmayer: A Biographical Memoir (2017)](https://www.nasonline.org/wp-content/uploads/2024/10/Stockmayer_Walter.pdf) · Jeffrey Kovac and Marshall Fixman · National Academy of Sciences memoir; citation and paraphrase, no image reproduced

  Check the context and connections of the 1941–1943 gelation studies.

  Historical information supports the original conceptual explanation.
