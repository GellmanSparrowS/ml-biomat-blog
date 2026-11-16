# 开始实践：准备运行环境与文件

Source: https://ml-biomat.com/tutorials/molecular-dynamics/s00/
Language: zh-CN

把一份输入变成可以观察和分析的分子轨迹，需要哪些程序？从终端和文件夹开始，准备两套课程共用的运行环境。

## 先认识计算中的三个角色

看一段水分子绕着蛋白质运动的动画，容易让人觉得模拟软件像一个分子世界的播放器。真正的计算从更早的地方开始：它先读入原子的位置、相互连接的关系和力场参数，再按选定的时间步推进运动，把若干时刻的位置、能量和温度保存下来。浏览器里的轨迹播放器负责展示这些坐标；GROMACS或LAMMPS负责产生坐标；Python分析程序则负责计算距离、分布、平均值和误差。把这几个角色分开理解，后面看到不同文件扩展名时，就知道应该把文件交给谁。

这两套课程可以从阅读和运行两个方向进入。直接打开HTML，就能阅读双语正文、查看公式、调整科学交互，并播放已经嵌入的参考轨迹；这些内容随页面保存在一起。准备亲自实践时，先下载某章的参考数据包，用分析程序重新生成图，再运行输入文件产生自己的数据。这样每增加一种工具，都有一个明确目标：先认识数据，再学习计算怎样得到它。

[Figure: diagram](https://ml-biomat.com/tutorials/molecular-dynamics/s00/#zh-roles)

图 1 · 模拟引擎推进分子的运动，分析程序从保存的记录中提取测量量。轨迹文件把这两个步骤连接起来；同一条轨迹可以回答多个结构和运动问题。

本页采用一套固定的CPU环境：GROMACS 2026.4、LAMMPS 30 Sep 2026 Update 1，以及Python分析工具。CPU是计算机处理通用任务的处理器，课程中的小体系可以用它完成。GPU适合加速部分计算，后续需要较大体系时，可以依据GROMACS安装指南建立单独的GPU版本。首先把CPU流程跑通，文件、命令和分析方法就有了共同的起点。

## 打开正确的终端，选好工作目录

终端是通过文字向程序发出指令的窗口。窗口里的“命令解释器”负责读懂这句话；在本课程中，大部分运行脚本使用Bash解释器。Linux和Windows里的PowerShell采用不同语法，因此同样一行文字放进不同窗口，结果可能不同。Windows读者可以通过WSL使用Linux环境：在Windows中打开已安装的Ubuntu，随后执行本页标为Bash的命令。下面两行PowerShell用于了解机器上有哪些Linux环境；需要新建环境时，按文末微软官方安装说明完成安装与首次启动。

### 在Windows中查看Linux环境

```
wsl --list --verbose
wsl --list --online
```

在PowerShell中执行。第一行查看已有环境，第二行查看可安装的发行版；实际安装步骤见微软官方说明。

进入Linux终端后，先选择一个方便管理且空间充足的课程文件夹。把它理解成实验台：引擎、分析环境和各次实验都有自己的位置。`pwd`显示当前所在目录，`ls`列出里面的文件，`cd`切换目录；例如，已经位于希望存放课程的位置时，可以执行`mkdir -p md-course`，然后执行`cd md-course`。此后本页的相对路径都从这个目录开始计算。`runtime`存程序与环境，具体实验可以另建`water-run`或`protein-run`等目录。

这里的“相对路径”类似从当前房间出发寻找隔壁房间。`runtime/analysis`表示当前目录里的runtime文件夹中的analysis文件夹；`.`代表当前目录，`..`代表上一级目录。命令中的`$PWD`会被Bash替换成当前目录的完整位置。路径两侧的双引号把可能含空格的路径作为一个整体交给程序。把输入和输出放进清楚命名的文件夹，既方便复查，也能避免第二次运行覆盖第一次的记录。

下面准备编译器、下载工具和绘图字体。编译器把人能阅读的源代码变成计算机执行的程序，CMake负责组织编译步骤，Ninja负责按依赖关系安排任务，FFTW提供傅里叶变换所需的计算库。这些名称此时可以先按用途认识；后续解释长程静电时，会再遇到傅里叶变换。命令对应Ubuntu 24.04，其中`sudo`会请求操作系统安装权限，输入的是自己Linux账户的密码。已有这些工具的环境可以直接核对下面输出的版本。

### 在Ubuntu 24.04中准备编译与绘图工具

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

在选定的课程工作目录执行。sudo负责安装操作系统软件包；之后引擎和Python环境均放进当前目录。Noto字体供中文图使用。

## 把源代码变成可运行的引擎

开放源码使我们能够检查程序如何实现模型，也可以选择一份明确的版本来重复计算。下面下载课程使用的两个源码包，然后核对SHA-256。这个长字符串可以看作文件内容的指纹：文件中的任意字节发生变化，通常就会得到不同的指纹。核对的是下载文件与本课程固定发行包是否一致。下载命令中的`-fL`让curl跟随下载地址的跳转，并在服务器报告错误时结束；`-o`指定保存文件的名称。

### 下载固定版本并核对文件

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

两行长字符串是完整源码包的SHA-256。检查通过后才解压，两个OK分别对应两个源码包。

解压以后，`runtime/src`保存原始源码，`runtime/build`保存编译过程中产生的文件，`runtime/install`保存最终使用的程序。三个位置各有用途：重新调整编译选项时可以建立新的build目录；运行模拟时只需要安装后的程序。下面的CMake命令使用`-S`指定源码位置，`-B`指定构建位置，`-D`给出配置选项。行尾的反斜杠表示同一条命令在下一行继续，复制时应保留整个代码块。

LAMMPS的许多能力按功能包组织。例如，MOLECULE处理分子中的连接关系，KSPACE提供长程相互作用算法，RIGID提供刚性约束相关方法，MC包含后续吸附课使用的交换操作。把课程所需功能在安装时准备好，后面遇到某个命令就能直接使用。本版本安装脚本还包含刷新系统动态库缓存的步骤；这里使用项目目录内的运行时库路径，代码只移除生成的安装脚本中的该步骤，计算源码保持原有内容。

### 编译并安装两套模拟引擎

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

从同一个工作目录执行。--parallel 4使用四个编译任务；软件安装到runtime/install。末尾的版本输出用于检查可执行文件。

编译结束后，版本命令应分别给出`GROMACS version: 2026.4`与`LAMMPS (30 Sep 2026 - Update 1)`。LAMMPS帮助输出还列出已启用的功能包和命令。`--parallel 4`中的4是同时执行的编译任务数，影响安装阶段的资源使用；模拟使用多少线程，要由运行命令另行设置。此时可以把版本输出保存进自己的实验记录，以后对比结果时，就知道使用了哪套计算程序。

## 给数据分析准备自己的工具箱

轨迹里可能有成千上万个坐标，肉眼适合发现整体形状，计算程序适合准确地重复同一种测量。Python分析环境中的NumPy处理数组，SciPy提供科学计算方法，Matplotlib把数值画成图，MDAnalysis读取分子结构和轨迹。它们共同构成一个工具箱。虚拟环境把这套工具放进专用目录，使课程使用的版本清楚可见；另一项研究需要不同版本时，可以另建环境。

### 建立独立的Python分析环境

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

Python环境保存在runtime/analysis。最后的检查同时显示解释器位置与四个库的版本，并确认当前使用的是独立环境。

本页的分析命令使用Python 3.12或兼容的更新版本，四个主要库固定为代码中的版本。`python -m pip`中的`-m`表示让这个Python运行pip模块，从而把库安装到同一个解释器所属的环境。最后显示的解释器位置应位于刚建立的`runtime/analysis`内。图中选择中文时，还需要系统能够找到中文字体；上一步安装的Noto CJK提供相应字形。每章的分析程序都提供语言选项，英文图使用`en`，中文图使用`zh`。

新开一个终端时，需要再次告诉它课程程序在哪里。下面把两个引擎所在目录加入当前终端的`PATH`，然后激活Python环境。PATH是一串按顺序查找程序的位置；输入`gmx`时，终端会沿着它找到对应的可执行文件。将下面文件保存在课程工作目录，并使用`source activate-course.sh`执行。source让这些设置在当前终端中生效，此后进入任意案例子目录，仍然可以直接输入gmx、lmp和python。

### 让当前终端找到课程程序

```
# Run with: source activate-course.sh
# First change to the workspace containing the runtime directory.
export PATH="$PWD/runtime/install/gromacs-2026.4/bin:$PWD/runtime/install/lammps-30Sep2026_update1/bin:$PATH"
source runtime/analysis/bin/activate
command -v gmx
command -v lmp
command -v python
```

在工作目录使用source activate-course.sh。source使路径设置留在当前终端；随后进入具体案例目录，gmx、lmp和python仍可使用。

## 从参考数据走到自己的一次运行

第一次实践可以先选G01的水盒。下载页面中的参考数据ZIP，解压到一个新的文件夹，进入该文件夹，然后运行下面的分析命令。这里的XVG文件已经包含模拟记录，程序会读取时间、温度、体积和密度，生成图与统计结果。这个步骤把文件、数值和图联系起来：打开XVG可以看到数据行，打开生成的SVG或PNG可以看到同一组数字怎样组成曲线。SVG放大后仍然清晰，PNG适合放进普通文档或图片查看器。

### 先用参考数据生成第一张图

```
#!/usr/bin/env bash
set -euo pipefail
# Run from the extracted water reference-data directory.
python analyze_water.py npt-density-volume-temperature.xvg --output figures --language en
```

解压G01的水盒参考数据，在解压目录执行；英文图使用en，中文图使用zh。完整分析程序在G01中逐行展示。

熟悉参考结果以后，再把完整输入包解压到另一目录，从课程工作目录激活环境，然后进入这个新目录执行`bash run.sh`。该脚本按顺序调用模拟引擎，前一步生成的结构或检查点会成为后一步的输入。运行结束后，使用同一个分析程序处理自己的输出，再对照章节中的数值、时间范围和曲线形态。温度这样的瞬时量会波动；观察条件相同的时间窗口和统计量，比要求某一个时刻的数字完全相同更有意义。

LAMMPS的入口采用同样的学习顺序：先在L01认识粒子和能量，随后在L02阅读完整输入、运行脚本和轨迹记录。不同引擎使用不同文件格式，但“建立模型—推进运动—保存观测—分析结果”的关系相同。后续章节会逐渐增加分子的连接关系、溶剂、约束与新的测量方法；每次新增的命令都对应一个可以解释的物理或分析操作。

## 顺着报错找到需要补齐的一步

遇到`command not found`，先检查当前终端是否已经激活环境，再用`command -v gmx`或`command -v lmp`查看实际找到的程序。若提示找不到输入文件，执行`pwd`和`ls`，核对自己所在目录与命令中写的文件名，包括大小写。若Python提示`ModuleNotFoundError`，先查看`python -c "import sys; print(sys.executable)"`的输出，确认使用的是课程环境中的解释器，再给该解释器安装缺少的库。

模拟引擎报告的错误往往包含具体文件、行号或原子编号，可以从这些线索回到相应章节：缺少相互作用参数时检查拓扑和力场，原子距离过近时检查建模与最小化，约束出现异常时检查初始几何、时间步和准备过程。读日志时先找到第一次出现的错误，再回看它前面的输入与输出；后续报错有时只是前一步没有生成文件造成的连锁结果。把问题定位到一个明确步骤，修改和重新运行就有了清楚的起点。

## 为配体和聚合物准备建模工具

学习到蛋白质与小分子、聚合物和修饰膜时，建模的起点会有所变化。蛋白质通常能按照已有残基模板建立拓扑；一个新的小分子需要根据化学结构分配原子类型和电荷，长链则需要把重复单元与端基连接起来，并生成可放进盒子的初始构象。这一步发生在动力学模拟之前：它决定计算机中有哪些原子、它们怎样连接、使用什么相互作用参数。模拟引擎随后按这些规则推进运动。

几种开源工具各有分工。Open Babel读取和转换化学结构；ACPYPE衔接AmberTools的参数化工具与模拟文件格式；Polyply从单元序列、连接和力场库建立聚合物模型；INSANE用于安排粗粒化膜、溶剂与其他组分的位置。比如，在小分子例题中，GAFF指定参数体系，AM1-BCC指定电荷处理方法，零净电荷指定整个分子的电荷状态。三个选择共同进入模型。具体化学结构怎样检查、为什么选择这些设置，将在相应章节中结合分子逐项解释。

下面的安装对应Ubuntu 24.04、x86_64处理器环境和Python 3.12。这里固定到Python的小版本，是因为下载的Open Babel轮子已经针对这一解释器和平台编译。一个轮子可以理解为装配好的程序包：文件名中的`cp312`表示CPython 3.12，平台字段说明它面向哪类Linux环境。先用`python3 --version`确认解释器，再把下方五个文件放在同一文件夹；也可以直接下载完整工具包后解压到课程工作目录。

[下载建模环境的完整脚本与版本约束（ZIP）](https://github.com/GellmanSparrowS/ml-biomat-blog/releases/download/md-courses-2026-11/setup-modeling-tools.zip)

在含有`runtime`目录的课程工作目录执行`bash setup_modeling.sh`。安装程序使用文件自身的位置寻找辅助脚本，使用当前工作目录存放环境。完成后，`runtime/modeling`容纳建模程序，`runtime/analysis`继续容纳前面的轨迹分析工具。把`runtime/modeling/bin`加入当前终端的PATH后，就能调用polyply、insane、obabel和acpype；需要切回分析解释器时，使用`source runtime/analysis/bin/activate`，或直接写出相应解释器的相对路径。

### 安装分子建模工具

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

在课程工作目录执行bash setup_modeling.sh。脚本检查平台，建立独立环境，再安装并检查四个建模入口。

固定版本还要固定下载内容。网络地址告诉程序从哪里取文件，SHA-256告诉程序期望得到哪一份字节内容。下面的下载器先写入临时文件，计算校验值，匹配后再采用正式文件名。下载中断时可以重新运行；若同名文件的内容与预期不同，提示会指出需要重新核对的文件。Polyply的提交编号同时固定源码和自带力场库，后续改变链长时仍使用同一套建模规则。

### 下载后核对完整文件

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

SHA-256由文件的全部字节计算。只有匹配固定值，下载文件才进入正式文件名；已有文件也会重新检查。

### 选择匹配平台的程序包

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

程序从官方PyPI版本记录中查找精确文件名，再同时核对公开校验值与实际下载内容。

配体电荷计算还调用编译好的数值程序。它们依赖线性代数库以及Fortran运行库，就像一个测量程序还需要相应的计算部件。下面从Ubuntu官方发行包取得BLAS、LAPACK、GNU Fortran和四倍精度运行库，核对完整校验值后解压到项目目录。主安装脚本再让ACPYPE的AmberTools找到这些文件。这样，建模程序、数值库、临时文件和下载缓存都有明确的位置，下一次检查版本时可以顺着同一目录查看。

### 准备半经验计算需要的数值库

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

四个Ubuntu软件包解压到runtime/amber-libraries。主安装脚本把对应库连接到ACPYPE的专用库目录。

最后一份文件记录配套的Python依赖。约束文件中的`==`表示选用这个版本；它让环境解析时有一组明确的组合。这里保留的setuptools版本提供INSANE使用的pkg_resources接口，Polyply所需的分子图、数值和构型生成依赖也相应固定。安装末尾的`pip check`检查这些依赖声明是否相容，各程序的帮助入口则确认命令可以启动。接着回到具体章节，从化学结构、序列或膜组成开始建立例题模型。

### 让依赖版本相互配合

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

约束文件固定依赖版本。pip按实际需要安装相应包，并用这些版本解析依赖关系。

## 延伸阅读与开放资料

- [GROMACS 2026.4 installation guide](https://manual.gromacs.org/2026.4/install-guide/index.html)
- [LAMMPS: Build with CMake](https://docs.lammps.org/Build_cmake.html)
- [Microsoft: Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
- [Python 3.12: Virtual environments](https://docs.python.org/3.12/library/venv.html)
- [MDAnalysis installation guide](https://userguide.mdanalysis.org/stable/installation.html)
- [Polyply — polymer topology and coordinate generation](https://github.com/marrink-lab/polyply_1.0)
- [INSANE — coarse-grained membrane construction](https://github.com/Tsjerk/Insane)
- [ACPYPE — AnteChamber Python Parser Interface](https://github.com/alanwilter/acpype)
- [Open Babel — chemical file conversion](https://openbabel.org/docs/)
