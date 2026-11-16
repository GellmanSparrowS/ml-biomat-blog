# Getting Started: Your Environment and Files

Source: https://ml-biomat.com/tutorials/molecular-dynamics/s00/en/
Language: en

What turns an input file into a molecular trajectory you can inspect and analyse? Start with terminals and folders, then prepare the environment shared by both courses.

## Three roles in a simulation

A movie of water moving around a protein can make simulation software look like a player for a miniature molecular world. The calculation begins earlier. An engine reads atomic coordinates, connectivity and force-field parameters, advances motion through successive time steps, and saves positions, energies and temperatures at selected intervals. The trajectory player in the browser displays those coordinates; GROMACS or LAMMPS generates them; a Python analysis program measures distances, distributions, averages and uncertainties. Keeping these roles distinct makes unfamiliar file extensions easier to understand: each file has a place in the calculation.

You can enter these courses through reading or through practical work. Opening the HTML gives access to both complete language versions, formulas, scientific controls and embedded reference trajectories. These resources travel with the page. When you are ready to practise, download a chapter's reference bundle and regenerate its figures before running the inputs to create your own data. Each new tool then has a clear purpose: first learn to recognise the data, and then learn how a calculation produces them.

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/s00/en/#en-roles)

Figure 1 · The engine advances molecular motion; an analysis program measures properties from saved records. A trajectory connects the two stages and can support several structural and dynamical questions.

This guide uses a fixed CPU environment: GROMACS 2026.4, LAMMPS 30 Sep 2026 Update 1 and a Python analysis environment. A CPU is the processor that handles general computational tasks, including the small systems in the introductory lessons. A GPU can accelerate parts of larger calculations. When that becomes useful, the GROMACS installation guide explains how to make a separate GPU build. A working CPU installation provides a common starting point for learning the files, commands and analysis methods.

## Choose a terminal and workspace

A terminal is a window in which you give programs instructions as text. A shell interprets that text; most running scripts in these courses use the Bash shell. Bash and Windows PowerShell have different syntax, so a line pasted into the wrong shell can have a different meaning. On Windows, WSL provides a Linux environment. Open an installed Ubuntu environment, then use the commands labelled Bash. The two PowerShell commands below inspect available Linux environments. If you need to install one, follow Microsoft's linked installation guide through installation and first launch.

### Inspect Linux environments from Windows

```
wsl --list --verbose
wsl --list --online
```

Run in PowerShell. The first command lists installed environments; the second lists available distributions. Microsoft documents the installation procedure.

Inside the Linux terminal, choose a course directory with enough free space and a location you can find easily. Think of it as a laboratory bench with separate places for instruments and experiments. `pwd` reports the current directory, `ls` lists its files, and `cd` changes directories. Once you are where you want the course workspace to live, for example, run `mkdir -p md-course`, then `cd md-course`. The relative paths below begin in this directory. The `runtime` directory holds programs and environments; individual experiments can have separate directories such as `water-run` or `protein-run`.

A relative path is like a set of directions starting from your current room. `runtime/analysis` identifies the analysis directory inside runtime, starting from the current directory. A single dot, `.`, means the current directory; two dots, `..`, mean its parent. Bash replaces `$PWD` with the full location of the current directory. Double quotation marks keep a path containing spaces together as one argument. Giving inputs and outputs clearly named directories makes comparisons easier and helps preserve records from earlier runs.

The next commands prepare compilers, download tools and plotting fonts. A compiler turns readable source code into an executable program. CMake organises the build, Ninja schedules its tasks, and FFTW supplies Fourier-transform routines. For now, identify these tools by their jobs; the discussion of long-range electrostatics will return to Fourier transforms. The package commands apply to Ubuntu 24.04. `sudo` requests permission to install operating-system packages and uses your own Linux account password. If the tools are already installed, check their versions with the commands below.

### Prepare build and plotting tools on Ubuntu 24.04

```
#!/usr/bin/env bash
set -euo pipefail
sudo apt update
sudo apt install build-essential cmake ninja-build python3 python3-venv curl libfftw3-dev unzip fonts-noto-cjk
cmake --version
c++ --version
python3 --version
mkdir -p runtime/downloads runtime/src runtime/build runtime/install
```

Run in your chosen course workspace. sudo installs operating-system packages; the engines and Python environment are then installed inside this directory. Noto provides Chinese plot glyphs.

## Build the simulation engines

Open source lets us inspect how a program implements a model and choose an explicit software version for a reproducible calculation. The commands below download the two course releases and check their SHA-256 values. This long string acts as a fingerprint of a file's contents: changing a byte will generally change the fingerprint. The check compares the download with the fixed source archive used here. In the download command, `-fL` tells curl to follow redirects and stop when the server reports an error; `-o` names the saved file.

### Download and verify the pinned releases

```
#!/usr/bin/env bash
set -euo pipefail
curl -fL https://ftp.gromacs.org/gromacs/gromacs-2026.4.tar.gz \
  -o runtime/downloads/gromacs-2026.4.tar.gz
curl -fL https://download.lammps.org/tars/lammps-30Sep2026_update1.tar.gz \
  -o runtime/downloads/lammps-30Sep2026_update1.tar.gz
printf '%s\n' \
  '58eda60979b124fcf9dff8b1b63cedfbc72fdb36d99e921dc1bdc310571098b6  runtime/downloads/gromacs-2026.4.tar.gz' \
  '60e648992f6edf3c47e2093a1c0a0bcce42fb89b7ac4370f15ab56abc0b0eea6  runtime/downloads/lammps-30Sep2026_update1.tar.gz' \
  | sha256sum -c -
tar -xzf runtime/downloads/gromacs-2026.4.tar.gz -C runtime/src
tar -xzf runtime/downloads/lammps-30Sep2026_update1.tar.gz -C runtime/src
```

The two long strings are SHA-256 checksums of the source archives. Extraction follows verification; each OK identifies one matching archive.

After extraction, `runtime/src` contains source code, `runtime/build` contains files produced while compiling, and `runtime/install` contains the programs you will run. Each location has a separate job. A new build directory can hold a different set of compilation options, while simulations use the installed executable. In the CMake commands, `-S` selects the source directory, `-B` selects the build directory, and `-D` sets an option. A backslash at the end of a line continues the same command onto the next line, so copy the whole block.

LAMMPS organises many capabilities into packages. MOLECULE handles molecular connectivity, KSPACE supplies long-range interaction algorithms, RIGID supplies methods involving rigid constraints, and MC includes the exchange operations used in the adsorption lesson. Enabling the required capabilities now makes their commands available later. This release's generated installer also includes a command to refresh the system library cache. The project installation uses its own runtime library path, so the code removes that step from the generated installation script while keeping the simulation source unchanged.

### Build and install both simulation engines

```
#!/usr/bin/env bash
set -euo pipefail
cmake -S runtime/src/gromacs-2026.4 -B runtime/build/gromacs -G Ninja \
  -DCMAKE_INSTALL_PREFIX="$PWD/runtime/install/gromacs-2026.4" \
  -DCMAKE_BUILD_TYPE=Release -DGMX_GPU=OFF -DGMX_MPI=OFF \
  -DGMX_OPENMP=ON -DGMX_FFT_LIBRARY=fftw3 -DGMX_BUILD_OWN_FFTW=OFF \
  -DBUILD_TESTING=OFF -DGMX_BUILD_UNITTESTS=OFF
cmake --build runtime/build/gromacs --parallel 4
cmake --install runtime/build/gromacs

cmake -S runtime/src/lammps-30Sep2026/cmake -B runtime/build/lammps -G Ninja \
  -DCMAKE_INSTALL_PREFIX="$PWD/runtime/install/lammps-30Sep2026_update1" \
  -DCMAKE_BUILD_TYPE=Release -DBUILD_MPI=OFF -DBUILD_OMP=ON \
  -DBUILD_SHARED_LIBS=ON -DLAMMPS_INSTALL_RPATH=ON \
  -DPKG_MOLECULE=ON -DPKG_KSPACE=ON -DPKG_RIGID=ON -DPKG_CLASS2=ON \
  -DPKG_MISC=ON -DPKG_EXTRA-MOLECULE=ON -DPKG_EXTRA-FIX=ON \
  -DPKG_EXTRA-COMPUTE=ON -DPKG_DPD-BASIC=ON -DPKG_MANYBODY=ON \
  -DPKG_BPM=ON -DPKG_REACTION=ON -DPKG_REAXFF=ON -DPKG_OPENMP=ON \
  -DPKG_FEP=ON -DPKG_ASPHERE=ON -DPKG_COLLOID=ON -DPKG_MC=ON
cmake --build runtime/build/lammps --parallel 4
python3 - <<'PY'
from pathlib import Path
p = Path('runtime/build/lammps/cmake_install.cmake')
s = p.read_text()
line = 'execute_process(COMMAND ldconfig || exit 0)'
if s.count(line) == 1:
    p.write_text(s.replace(line, '# Project-local runtime library path is used.'))
PY
cmake --install runtime/build/lammps

export PATH="$PWD/runtime/install/gromacs-2026.4/bin:$PWD/runtime/install/lammps-30Sep2026_update1/bin:$PATH"
gmx --version
lmp -help
```

Run from the same workspace. --parallel 4 starts four compilation tasks, and runtime/install receives the programs. The final commands report their versions.

The version commands should report `GROMACS version: 2026.4` and `LAMMPS (30 Sep 2026 - Update 1)`. LAMMPS help also lists enabled packages and commands. The 4 in `--parallel 4` is the number of simultaneous compilation tasks; it controls resources during installation. The number of threads used by a simulation is set separately when launching that calculation. Save the version information with your experiment records so future comparisons identify the program that produced each result.

## Prepare the analysis environment

A trajectory may contain many thousands of coordinates. Looking at them is useful for recognising overall shape, while a program is useful for repeating the same measurement accurately. In the Python environment, NumPy handles arrays, SciPy supplies scientific routines, Matplotlib turns numbers into figures, and MDAnalysis reads molecular structures and trajectories. Together they form an analysis toolbox. A virtual environment puts that toolbox in a dedicated directory with identifiable versions. A different project can use another environment when it needs other versions.

### Create an isolated Python analysis environment

```
#!/usr/bin/env bash
set -euo pipefail
python3 -m venv runtime/analysis
runtime/analysis/bin/python -m pip install MDAnalysis==2.11.0 numpy==2.5.4 scipy==1.18.1 matplotlib==3.11.2
runtime/analysis/bin/python - <<'PY'
import sys
import MDAnalysis, numpy, scipy, matplotlib
print(sys.executable)
print('MDAnalysis', MDAnalysis.__version__)
print('NumPy', numpy.__version__)
print('SciPy', scipy.__version__)
print('Matplotlib', matplotlib.__version__)
assert sys.prefix != sys.base_prefix
PY
```

The Python environment lives in runtime/analysis. The final check reports the interpreter and four package versions and confirms that the interpreter belongs to a virtual environment.

The analysis commands here use Python 3.12 or a compatible newer version, with the four main libraries pinned to the versions in the code. In `python -m pip`, `-m` asks this Python interpreter to run the pip module, connecting package installation to the same interpreter. The final interpreter location should be inside the newly created `runtime/analysis` environment. Chinese figure labels also need a font containing Chinese glyphs; the Noto CJK package installed earlier provides them. Chapter analyses offer a language option: `en` selects English figures and `zh` selects Chinese.

A newly opened terminal needs to be told where the course programs are. The following script adds both engine directories to its `PATH`, then activates the Python environment. PATH is an ordered list of places to look for programs. When you type `gmx`, the shell follows that list to find an executable. Save the script in the course workspace and run `source activate-course.sh`. source applies the settings to the current terminal. You can then move into an example subdirectory and still invoke gmx, lmp and python directly.

### Make the course programs available in this terminal

```
# Run with: source activate-course.sh
# First change to the workspace containing the runtime directory.
export PATH="$PWD/runtime/install/gromacs-2026.4/bin:$PWD/runtime/install/lammps-30Sep2026_update1/bin:$PATH"
source runtime/analysis/bin/activate
command -v gmx
command -v lmp
command -v python
```

Use source activate-course.sh from the workspace. source applies the path settings to the current terminal. The commands remain available when you move into an example directory.

## From reference data to your own run

The water box in G01 is a convenient first exercise. Download its reference-data ZIP, extract it into a new directory, enter that directory and run the analysis command below. The XVG file already contains simulation records. The program reads time, temperature, volume and density, then produces figures and numerical summaries. This links the file, its numbers and the picture: the XVG shows the rows of data, while the resulting SVG or PNG shows how the same numbers form a curve. An SVG remains sharp when enlarged; a PNG works well in ordinary documents and image viewers.

### Make a first figure from reference data

```
#!/usr/bin/env bash
set -euo pipefail
# Run from the extracted water reference-data directory.
python analyze_water.py npt-density-volume-temperature.xvg --output figures --language en
```

Extract the G01 water reference bundle and run this command inside it. en selects English figures and zh selects Chinese. G01 displays the complete analysis program.

After exploring the reference results, extract the complete input bundle into another directory. Activate the environment from the course workspace, move into the new directory and run `bash run.sh`. The script calls the engine in sequence, passing structures or checkpoints from one stage into the next. When it finishes, analyse your own output with the same program and compare the reported quantities, time intervals and curve shapes with the lesson. Instantaneous quantities such as temperature fluctuate. Comparing the same time window and statistic is more informative than requiring one instantaneous value to match exactly.

The LAMMPS course follows the same learning sequence. L01 introduces particles and energy; L02 follows the full input, running script and trajectory records. The engines have different file formats, but both connect model construction, motion, saved observations and analysis. Later chapters add molecular connectivity, solvent, constraints and new measurements. Each additional command is tied to a physical or analytical operation that can be explained.

## Use an error message to find the next step

For `command not found`, check whether this terminal has activated the course environment, then use `command -v gmx` or `command -v lmp` to see which program it finds. If an input file is missing, use `pwd` and `ls` to compare the current directory with the filename in the command, including letter case. For Python's `ModuleNotFoundError`, first inspect `python -c "import sys; print(sys.executable)"`. Confirm that this is the course interpreter, then install the missing package into that interpreter's environment.

An engine error often names a file, line or atom. Follow that detail back to the relevant lesson: missing interaction parameters lead to topology and force-field definitions; close contacts lead to structure preparation and minimisation; constraint failures lead to initial geometry, time steps and preparation conditions. Find the first error in the log, then inspect the inputs and outputs immediately before it. Later errors can follow simply because an earlier stage did not create a needed file. Locating one specific step gives a clear starting point for correction and another run.

## Prepare tools for ligands and polymers

The starting point changes when the courses reach protein–ligand systems, polymers and modified membranes. A protein can usually be assigned a topology using established residue templates. A new small molecule needs atom types and charges based on its chemical structure, while a long chain needs connected repeat units, terminal groups and an initial conformation that can be placed in a simulation cell. This preparation precedes dynamics: it defines the atoms, their connections and interaction parameters. The simulation engine then advances motion under those rules.

The open-source tools have complementary roles. Open Babel reads and converts chemical structures. ACPYPE connects AmberTools parameterization programs to simulation file formats. Polyply builds polymer models from unit sequences, connections and force-field libraries. INSANE arranges coarse-grained membranes, solvent and other components. For the ligand example, GAFF selects the parameter family, AM1-BCC selects the charge treatment, and zero net charge specifies the molecule’s overall charge state. These choices jointly enter the model. The relevant chapters examine the chemical structure and explain the settings molecule by molecule.

This installation targets Ubuntu 24.04 on x86_64 with Python 3.12. The Python minor version is pinned because the downloaded Open Babel wheel was compiled for that interpreter and platform. A wheel is a preassembled program package: `cp312` in its filename identifies CPython 3.12, while the platform field identifies the Linux environment it supports. Check the interpreter with `python3 --version`, then place the five files below in one folder. You can also download the complete tool bundle and extract it into the course workspace.

[Download complete modeling setup scripts and constraints (ZIP)](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/setup-modeling-tools.zip)

Run `bash setup_modeling.sh` from the course workspace containing `runtime`. The installer locates helper scripts beside itself and stores the environment relative to the current working directory. After installation, `runtime/modeling` contains preparation programs, while `runtime/analysis` continues to hold the trajectory-analysis tools. Adding `runtime/modeling/bin` to this terminal’s PATH makes polyply, insane, obabel and acpype available. To return to the analysis interpreter, use `source runtime/analysis/bin/activate` or invoke the desired interpreter by its relative path.

### Install molecular-preparation tools

```
#!/usr/bin/env bash
# Run from the course workspace; all installed files remain under ./runtime.
# Platform: Ubuntu 24.04 x86_64, Python 3.12 with venv, curl, unzip, dpkg-deb.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
project=$(pwd)
runtime="$project/runtime"
python=${PYTHON:-python3}
"$python" -c 'import sys; assert sys.version_info[:2] == (3,12), "Use Python 3.12 for the pinned Linux wheel"'
test "$(uname -m)" = x86_64
. /etc/os-release
test "$ID" = ubuntu
test "$VERSION_ID" = 24.04
for tool in unzip dpkg-deb; do command -v "$tool" >/dev/null; done
mkdir -p "$runtime/downloads" "$runtime/src" "$runtime/tmp" "$runtime/cache/pip" "$runtime/cache/numba"
export TMPDIR="$runtime/tmp" PIP_CACHE_DIR="$runtime/cache/pip" NUMBA_CACHE_DIR="$runtime/cache/numba"
venv="$runtime/modeling"
if test ! -e "$venv/pyvenv.cfg"; then "$python" -m venv "$venv"; fi
"$venv/bin/python" -m pip install -c "$here/modeling-constraints.txt" \
  numpy==2.5.4 scipy==1.18.1 setuptools==80.9.0 wheel==0.48.0 pbr==7.1.3 \
  networkx==3.7 vermouth==0.15.0 decorator==4.4.2 tqdm==4.70.1 \
  pysmiles==2.1.1 cgsmiles==1.0.2 insane==1.2.0 simopt==0.4.0 \
  numba==0.68.1 llvmlite==0.50.0 rich==15.0.0 typer==0.28.0
"$venv/bin/python" "$here/fetch_verified.py" \
  'https://github.com/marrink-lab/polyply_1.0/archive/38d4d5424e1ef35c86e7cb8532fbd86ecf997221.zip' \
  cd5cd656ef9b819988780009e9b5a2798f03b895539765fd5b92f15a8bacb316 \
  "$runtime/downloads/polyply.zip"
src="$runtime/src/polyply_1.0-38d4d5424e1ef35c86e7cb8532fbd86ecf997221"
if test ! -d "$src"; then unzip -q "$runtime/downloads/polyply.zip" -d "$runtime/src"; fi
PBR_VERSION=0.0.0+g38d4d5424e1e "$venv/bin/python" -m pip install --no-build-isolation --no-deps "$src"
"$venv/bin/python" "$here/fetch_pypi_wheels.py" "$runtime/downloads"
"$venv/bin/python" -m pip install --no-deps \
  "$runtime/downloads/acpype-2026.10.15-py3-none-manylinux_2_35_x86_64.whl" \
  "$runtime/downloads/openbabel_wheel-3.1.1.23-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl"
PYTHON="$venv/bin/python" bash "$here/install_amber_libraries.sh"
"$venv/bin/python" - "$runtime" <<'PY'
from pathlib import Path
import sys, acpype
root=Path(sys.argv[1]).resolve()
amber=Path(acpype.__file__).resolve().parent/'amber_linux/lib'
assert root in amber.parents
libs=root/'amber-libraries/usr/lib/x86_64-linux-gnu'
for filename,relative in {
    'libblas.so.3':'blas/libblas.so.3',
    'liblapack.so.3':'lapack/liblapack.so.3',
    'libgfortran.so.5':'libgfortran.so.5',
    'libquadmath.so.0':'libquadmath.so.0',
}.items():
    target=(libs/relative).resolve();assert target.is_file()
    link=amber/filename
    if link.is_symlink() and link.resolve()==target:continue
    if link.exists() or link.is_symlink():raise RuntimeError(f'Existing library needs review: {filename}')
    link.symlink_to(target)
PY
"$venv/bin/python" -m pip check
"$venv/bin/python" -m pip freeze > "$runtime/modeling-requirements.lock.txt"
"$venv/bin/polyply" -h > "$runtime/polyply-help.txt"
"$venv/bin/insane" -h > "$runtime/insane-help.txt" 2>&1
"$venv/bin/obabel" -V
"$venv/bin/acpype" -h > "$runtime/acpype-help.txt"
printf '%s\n' 'Modeling programs are ready. For this terminal, run:'
printf 'export PATH="%s/bin:$PATH"\n' "$venv"
```

Run bash setup_modeling.sh from the course workspace. It checks the platform, creates a dedicated environment, then installs and checks the four preparation programs.

Pinning a release also involves pinning its downloaded content. The network address tells the program where to obtain a file; SHA-256 identifies the expected bytes. The downloader below first writes a temporary file, calculates its digest and gives it the final filename after a match. An interrupted download can be retried. If an existing file differs from the expected content, the message identifies the file to check again. The Polyply commit fixes both the source and bundled force-field library, so changing chain length later retains one set of construction rules.

### Verify each complete download

```
"""Download one pinned source or wheel and verify its SHA256 before use."""
from pathlib import Path
import argparse, hashlib, urllib.request
p=argparse.ArgumentParser()
p.add_argument('url');p.add_argument('sha256');p.add_argument('destination',type=Path)
a=p.parse_args();a.destination.parent.mkdir(parents=True,exist_ok=True)
def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
if not a.destination.exists():
    partial=a.destination.with_name(a.destination.name+'.partial')
    with urllib.request.urlopen(a.url,timeout=120) as response,partial.open('wb') as output:
        while block:=response.read(1024*1024):output.write(block)
    if digest(partial)!=a.sha256:raise SystemExit(f'{a.destination.name}: downloaded file SHA256 differs from the pinned value.')
    partial.replace(a.destination)
if digest(a.destination)!=a.sha256:raise SystemExit(f'{a.destination.name}: existing file SHA256 differs from the pinned value.')
print(a.destination.name+': SHA256 verified')
```

SHA-256 is calculated from all bytes. A download receives its final name only after matching the pinned value; existing files are checked again.

### Select the platform-specific packages

```
"""Resolve exact official PyPI wheels and verify their fixed SHA256 values."""
from pathlib import Path
import json,sys,subprocess,urllib.request
target=Path(sys.argv[1]);helper=Path(__file__).with_name('fetch_verified.py')
packages=[
('acpype','2026.10.15','acpype-2026.10.15-py3-none-manylinux_2_35_x86_64.whl','c07111fba6601c9680db2bf32d9bbf1c980955fbb97d2f40b2670ca61df378f9'),
('openbabel-wheel','3.1.1.23','openbabel_wheel-3.1.1.23-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl','39340af4da11cafabb95542fd110e7ff120e3af085e4e48aa2b8e69cc49b807b')]
for name,version,filename,expected in packages:
    with urllib.request.urlopen(f'https://pypi.org/pypi/{name}/{version}/json',timeout=60) as response:data=json.load(response)
    rows=[r for r in data['urls'] if r['filename']==filename]
    assert len(rows)==1 and rows[0]['digests']['sha256']==expected
    subprocess.run([sys.executable,str(helper),rows[0]['url'],expected,str(target/filename)],check=True)
```

The program selects exact filenames from official PyPI version records and checks both the published digest and downloaded content.

Ligand charge calculation also calls compiled numerical programs. They depend on linear-algebra libraries and a Fortran runtime, much as a measurement program needs its computational components. The next script obtains BLAS, LAPACK, GNU Fortran and quad-precision runtime libraries from official Ubuntu distribution packages, verifies their complete digests and extracts them into the project. The main installer then makes these files available to ACPYPE’s AmberTools. Preparation programs, numerical libraries, temporary files and download caches consequently have explicit locations for later inspection.

### Prepare the numerical libraries used by SQM

```
#!/usr/bin/env bash
# Ubuntu 24.04, x86_64. Extract libraries inside the current project.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
project=$(pwd)
runtime="$project/runtime"
downloads="$runtime/downloads/amber-libraries"
prefix="$runtime/amber-libraries"
python=${PYTHON:-python3}
test "$(uname -m)" = x86_64
. /etc/os-release
test "$ID" = ubuntu
test "$VERSION_ID" = 24.04
command -v dpkg-deb >/dev/null
mkdir -p "$downloads" "$prefix"
while read -r archive hash; do
  "$python" "$here/fetch_verified.py" "https://archive.ubuntu.com/ubuntu/$archive" "$hash" "$downloads/${archive##*/}"
  dpkg-deb --extract "$downloads/${archive##*/}" "$prefix"
done <<'PACKAGES'
pool/main/l/lapack/libblas3_3.12.0-3build1.1_amd64.deb 1b0ef0ad0893ff77bf7d5ab75723771788e16137ea1efde557dbac7b7b83a758
pool/main/l/lapack/liblapack3_3.12.0-3build1.1_amd64.deb 05ced5049d4fd393e0ae6dc71211e7c07ed0c85e8099649d679cf4b5a1aed59b
pool/main/g/gcc-14/libgfortran5_14.2.0-4ubuntu2~24.04.1_amd64.deb 2b05896c477275ad3473bb63a5ac5a5b8a7e4a6ad6ed7cb23c442ccd1abc28f5
pool/main/g/gcc-14/libquadmath0_14.2.0-4ubuntu2~24.04.1_amd64.deb dc8f0ca542e09d662f29370c8393c016440dd4bc5c996c5fcc19f632b63ce3b0
PACKAGES
printf '%s\n' 'Project-local BLAS, LAPACK, GNU Fortran and quad-precision libraries are ready.'
```

Four Ubuntu packages are extracted under runtime/amber-libraries. The main installer links the corresponding libraries into ACPYPE’s dedicated library directory.

The last file records the accompanying Python dependencies. A `==` entry selects one version, giving environment resolution a defined combination. The retained setuptools version supplies the pkg_resources interface used by INSANE. Molecular-graph, numerical and conformation-generation dependencies needed by Polyply are pinned as well. At the end of installation, `pip check` checks compatibility between declared dependencies, and each program’s help command checks its entry point. Return to the relevant chapter next and build its example from a chemical structure, a sequence or a membrane composition.

### Keep dependency versions consistent

```
annotated-doc==0.0.5
cgsmiles==1.0.2
cloudpickle==3.1.2
contourpy==1.4.0
cycler==0.12.1
decorator==4.4.2
filelock==4.2.10
fonttools==4.68.0
GridDataFormats==1.2.0
insane==1.2.0
joblib==1.6.0
kiwisolver==1.5.1
llvmlite==0.50.0
markdown-it-py==4.2.0
matplotlib==3.11.2
mda-xdrlib==0.2.0
MDAnalysis==2.11.0
mdurl==0.1.2
mmtf-python==1.1.3
mrcfile==1.5.4
msgpack==1.2.4
networkx==3.7
numba==0.68.1
numpy==2.5.4
packaging==26.3
pbr==7.1.3
pillow==13.0.0
Pygments==2.21.0
pyparsing==3.3.3
pysmiles==2.1.1
python-dateutil==4.0.0
rich==15.0.0
scipy==1.18.1
setuptools==80.9.0
shellingham==1.5.4
simopt==0.4.0
threadpoolctl==3.8.0
tqdm==4.70.1
typer==0.28.0
tzdata==2026.6
vermouth==0.15.0
wheel==0.48.0
```

The constraints file pins dependency versions. pip installs the packages actually required and resolves their dependencies using these versions.

## Further Reading and Open Materials

- [GROMACS 2026.4 installation guide](https://manual.gromacs.org/2026.4/install-guide/index.html)
- [LAMMPS: Build with CMake](https://docs.lammps.org/Build_cmake.html)
- [Microsoft: Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
- [Python 3.12: Virtual environments](https://docs.python.org/3.12/library/venv.html)
- [MDAnalysis installation guide](https://userguide.mdanalysis.org/stable/installation.html)
- [Polyply — polymer topology and coordinate generation](https://github.com/marrink-lab/polyply_1.0)
- [INSANE — coarse-grained membrane construction](https://github.com/Tsjerk/Insane)
- [ACPYPE — AnteChamber Python Parser Interface](https://github.com/alanwilter/acpype)
- [Open Babel — chemical file conversion](https://openbabel.org/docs/)
