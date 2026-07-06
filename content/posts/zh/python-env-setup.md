---
title: "Python 科学计算环境完全搭建指南：从零到生产力"
date: "2026-07-06"
category: "python-tutorials"
tags: ["python", "conda", "jupyter", "环境配置", "科学计算", "Mamba"]
lang: "zh"
slug: "python-env-setup-zh"
description: "从虚拟环境原理到Conda/Mamba实战再到Jupyter与VS Code配置，三平台全覆盖的Python科学计算环境搭建指南，面向生物与材料科学研究生的从零到生产力完整教程。"
---
## 一、为什么需要管理 Python 环境——从版本冲突说起

很多研究生第一次接触 Python 的体验并不美好。你在网上找到一个处理 AFM 数据或者 XRD 衍射图谱的脚本，按照教程安装了所有依赖库，脚本能跑了。几周后，导师发来一个机器学习的分析代码，安装新的依赖之后，原来那个脚本忽然报错，提示某个模块的版本不兼容。你什么也没改，它就坏了。这种经历几乎是每个研究生的必经之路，而背后的根本原因是：当所有包都安装在同一个"全局"Python 环境里，不同项目对同一个底层库的版本需求一旦相互冲突，就必然两败俱伤。

问题的本质可以用一个实验室类比来说明。假设你只有一个培养箱，两种菌株的最适培养温度分别是 30°C 和 37°C——你无法让两者同时在最适条件下生长，必须妥协一方。Python 的包冲突也是同一逻辑：BioPython 的旧版脚本可能依赖 NumPy 1.x 的接口，而 TensorFlow 的新版本需要 NumPy 2.x 的特性；OVITO 的 Python 绑定依赖某一版本的 VTK 库，而你的有限元后处理脚本依赖另一版本——如果共享同一个环境，安装其中一个必然破坏另一个。对于同时在做材料表征分析、分子动力学仿真、以及尝试机器学习预测的研究生，这种冲突几乎是必然发生的。

解决方案是**虚拟环境（Virtual Environment）**。虚拟环境是操作系统中一个隔离的 Python 运行空间，有自己独立的 Python 解释器版本和完整的包集合，与其他环境、与系统自带的 Python 完全互不干扰。你可以把它理解为实验室里的一间间独立超净间：每个超净间维护自己的温度、气氛和污染控制标准，不同实验在各自的空间里进行，互不污染。创建一个新的虚拟环境，就是开辟一间新超净间；销毁一个环境，就是拆掉那间超净间，完全不影响其他正在运行的实验。

**Conda** 是目前 Python 科学计算社区管理虚拟环境的事实标准工具。相比 Python 内置的 `venv` 或 `virtualenv`，Conda 的核心优势在于它不仅管理 Python 包，还管理 Python 解释器本身以及各种非 Python 的底层依赖——包括 C/C++ 共享库、BLAS/LAPACK 线性代数库（NumPy 和 SciPy 的速度瓶颈最终取决于这一层）、CUDA 工具链（GPU 计算的基础）等。对于需要调用有限元求解器（如 FEniCSx）、分子动力学库（如 LAMMPS 的 Python 接口）、或者生物序列分析工具（如 BLAST 的本地调用）的研究场景，Conda 在这一层面的精确控制能力是 pip 组合无法替代的。

掌握 Conda 虚拟环境管理，是从"能跑 Python 脚本"升级到"能稳定复现科研计算结果"的关键一步，也是向导师或合作者分享代码时展示基本研究规范的前提。本文覆盖 Windows、macOS（含 Apple Silicon）和 Linux 三个平台，从安装到日常使用完整说明，力求让完全没有命令行经验的读者也能独立完成配置。

---

## 二、Anaconda 还是 Miniconda——按需选择，无需焦虑

在安装 Conda 之前，首先澄清一个常见混淆：Anaconda 和 Miniconda 是两个不同的安装包，但它们安装的核心工具 `conda` 完全相同，在环境管理功能上没有任何差异。区别仅在于安装时预置了多少内容。你用哪一个都可以，本文后续所有命令对两者完全通用。

**Anaconda** 是"全家桶"版本。安装完成后，你会得到 `conda` 本身、Python、以及超过两百五十个预装的科学计算包（涵盖 NumPy、SciPy、Pandas、Matplotlib、Jupyter、scikit-learn 等核心工具），外加 **Anaconda Navigator** 这个图形化管理界面。整个安装包约 800 MB 到 1 GB，在磁盘展开后占用 3 到 5 GB。优势是真正的开箱即用：安装完成后不需要运行任何安装命令，直接启动 JupyterLab 就可以开始数据分析。Anaconda Navigator 的图形界面允许你用鼠标点击完成环境创建、包搜索安装和应用启动，对于不习惯命令行的研究生而言友好度极高。如果你的第一目标是"尽快开始处理实验数据"而不是"深入理解环境管理"，Anaconda 是更合适的起点。

**Miniconda** 是精简版本，安装包仅约 60 到 100 MB，安装完成后只有 `conda`、Python 和几个基础工具，没有任何预装的科学计算库。一切都需要手动按需安装，初次配置时需要多运行几条安装命令，但换来的好处是环境从一开始就完全在你的掌控之下——你清楚地知道安装了什么，不存在大量"永远不会用到的包"默默占用磁盘空间。对于已经有一定 Python 使用经验、希望精确控制环境内容的用户，或者在磁盘空间有限的笔记本上工作、或者在远程服务器上无法使用图形界面的用户，Miniconda 更为合适。

如何选择？**一般推荐 Miniconda**——从零按需搭建让你清楚知道装了什么，磁盘占用仅数百 MB，在远程服务器上也能轻松部署。如果对命令行完全陌生且磁盘充裕，Anaconda 的开箱即用体验也不错。两者日后可自由切换，不存在选错的风险

还有一个值得单独介绍的选项：**Mamba**。Mamba 不是独立的安装包，而是在已安装 Conda 之后可以选择安装的高性能替代工具。它用 C++ 重写了 Conda 的依赖求解器（即计算"安装包 A 需要哪些版本的依赖包"这个问题的算法），在解决复杂依赖关系时速度比 Conda 快数倍。如果你安装过 PyTorch 并同时需要 CUDA 支持，就会体验过 `conda install` 长时间卡在"Solving environment..."的痛苦——这正是 Mamba 的适用场景。安装方式：在已有 Conda 安装的基础上运行 `conda install -n base -c conda-forge mamba -y`，之后将所有 `conda install` 和 `conda create` 命令替换为 `mamba install` 和 `mamba create` 即可，其余用法完全相同。

---

## 三、三平台完整安装流程：Windows、macOS 与 Linux

不同操作系统的安装步骤存在若干关键差异，尤其是 macOS 的 Apple Silicon 芯片需要特别注意版本选择。以下按平台逐一说明，请对照自己的系统操作。

**Windows 系统**

前往 Anaconda 官网（`https://www.anaconda.com/download`）下载对应 Windows 的安装程序（.exe 文件）。如果选择 Miniconda，则前往 `https://docs.conda.io/en/latest/miniconda.html` 下载。双击运行安装程序，在"Installation Type"步骤选择"Just Me"（只为当前用户安装，无需管理员权限，不影响其他用户）。在"Advanced Installation Options"页面，**务必勾选"Add Anaconda3/Miniconda3 to my PATH environment variable"** 这一选项——若不勾选，安装完成后系统找不到 `conda` 命令，所有后续操作都无法进行。

安装完成后，不要使用普通的命令提示符（CMD）或 PowerShell，而是从开始菜单找到并打开 **Anaconda Prompt**（或 Miniforge Prompt），以此作为后续所有 `conda` 操作的命令行入口。普通 CMD 和 PowerShell 在默认安全策略下可能无法正确识别 conda 的激活命令。在 Anaconda Prompt 中运行以下命令验证安装：

```bash
conda --version
python --version
```

两条命令都正常返回版本号（如 `conda 24.7.1`、`Python 3.12.4`）即表示安装成功。

**macOS 系统（重要：M 系列芯片与 Intel 的区别）**

2020 年底之后发布的 Mac 电脑大多搭载 Apple Silicon 芯片（M1/M2/M3/M4 系列），与 Intel 芯片在指令集架构上存在根本差异（ARM 对比 x86-64）。下载安装包时**必须选择正确的架构版本**，否则所有科学计算库的 Apple Silicon 原生加速（包括 NumPy 对 Apple Accelerate 框架的调用、PyTorch 的 MPS 后端等）将无法生效，性能损失可高达数倍。

查看自己芯片型号：点击左上角苹果图标 → 关于本机，查看"芯片"栏。如果显示"Apple M1/M2/M3/M4"，下载 **arm64** 版本；如果显示"Intel Core"，下载 **x86_64** 版本。

在终端（Terminal.app）中运行安装，以 Apple Silicon Miniconda 为例：

```bash
# 下载（arm64 版本）
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh

# 运行安装脚本
bash Miniconda3-latest-MacOSX-arm64.sh
```

安装过程中出现"Do you wish the installer to initialize Miniconda3 by running conda init?"时输入 `yes`，这会修改 `~/.zshrc` 配置文件（macOS 默认 shell 为 zsh）。安装完成后运行以下命令使配置立即生效（或直接关闭并重新打开终端）：

```bash
source ~/.zshrc
conda --version
```

**Linux 系统（本地及 HPC 集群）**

Linux 的安装方式与 macOS 命令行步骤基本相同：

```bash
# 下载（以 x86_64 为例，ARM 服务器替换为对应架构版本）
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 运行安装脚本（全程接受默认选项，conda init 时输入 yes）
bash Miniconda3-latest-Linux-x86_64.sh

# 使配置生效
source ~/.bashrc
conda --version
```

如果你在大学或研究院的高性能计算（HPC）集群上工作，优先检查集群是否已经通过 module 系统预装了 Conda：运行 `module avail anaconda` 或 `module avail miniconda` 查看可用模块。若已预装，通过 `module load anaconda3` 直接加载，避免在 home 目录下重复安装。若集群没有预装，将 Miniconda 安装在自己的 home 目录下（安装路径选择 `$HOME/miniconda3`）是标准做法，无需 root 权限，且不影响其他用户。

---

## 四、创建与管理虚拟环境——项目隔离的核心操作

理解了虚拟环境的必要性之后，具体的创建和管理操作其实非常直观。这一节完整介绍环境的全生命周期操作，以及最重要的"环境复现"（Reproducibility）工作流。

创建一个新环境时，最重要的参数是 Python 版本。建议始终明确指定版本，而不是让 Conda 自行决定：

```bash
conda create -n matsci python=3.11 -y
```

`-n matsci` 是环境名称，建议用与项目相关的描述性名字（例如 `afm_analysis`、`ml_fatigue`、`protein_dock`），避免使用过于宽泛的名字如 `myenv`。不同环境可以有不同的 Python 版本，互不干扰。`-y` 参数表示自动确认所有提示，跳过逐行输入 y 的步骤。

激活环境是开始工作前的必须步骤：

```bash
conda activate matsci
```

激活成功后，终端提示符前会出现 `(matsci)` 字样——这是环境已激活的视觉标志。此后在该终端窗口中安装的所有包、运行的所有 Python 脚本，都在 `matsci` 这个隔离空间里执行，不会影响其他环境或系统。退出当前环境用 `conda deactivate`。

列出所有已创建的环境（带 `*` 标记的是当前激活的）：

```bash
conda env list
```

列出当前环境中已安装的所有包及其版本：

```bash
conda list
```

**环境复现（Reproducibility）**是科研工作中最重要的一个实践。当你的材料表征分析或疲劳寿命预测代码达到可以写进论文附录的阶段，将当前环境的完整信息导出为配置文件：

```bash
conda env export > environment.yml
```

生成的 `environment.yml` 文件记录了该环境中所有包的名称和精确版本号。合作者或审稿人拿到这个文件后，运行一条命令即可在自己的计算机上复现完全相同的运行环境：

```bash
conda env create -f environment.yml
```

这个工作流确保你的代码在导师的电脑、投稿后审稿人要求验证数据时，以及三年后你自己回头复查时，都能产生完全相同的输出。这是现代计算科研的基本规范，也是开放科学（Open Science）要求的可重复性的技术保障。

| 操作 | 命令 |
|---|---|
| 创建新环境 | `conda create -n 名称 python=3.11 -y` |
| 激活环境 | `conda activate 名称` |
| 退出当前环境 | `conda deactivate` |
| 查看所有环境 | `conda env list` |
| 删除环境 | `conda env remove -n 名称` |
| 导出环境配置 | `conda env export > environment.yml` |
| 从配置文件重建 | `conda env create -f environment.yml` |
| 列出已安装包 | `conda list` |
| 更新单个包 | `conda update 包名` |

---

## 五、安装核心科学计算工具包——按需配置，理解每个工具的定位

激活目标环境后，就可以安装科学计算所需的核心包。以下从功能角度介绍各个主要包解决什么问题，而不只是列出安装命令——理解每个工具的定位，有助于你在遇到新的分析任务时知道该找哪个工具，而不是盲目 `pip install everything`。

安装基础科学计算套件：

```bash
conda install numpy scipy pandas matplotlib -y
conda install -c conda-forge jupyterlab seaborn scikit-learn scikit-image ipykernel -y
```

**NumPy** 是整个 Python 科学计算生态的数值计算地基。它提供多维数组（ndarray）数据结构和大量向量化数学函数，背后由高度优化的 BLAS/LAPACK 线性代数库驱动。如果你在做应力-应变数据的矩阵运算、CT 图像的体素阵列处理、或者蛋白质结构的坐标变换，NumPy 几乎是第一个会用到的工具。矩阵乘法在 NumPy 中只需 `A @ B` 一行代码，且速度是纯 Python 循环的数十到数百倍。

**SciPy** 建立在 NumPy 之上，提供更高层次的科学计算算法。`scipy.signal` 用于信号处理（疲劳试验载荷谱的滤波、电生理信号的频谱分析）；`scipy.stats` 用于统计检验（判断两组材料测试数据的均值差异是否显著）；`scipy.ndimage` 用于图像处理（CT 图像的形态学操作、骨小梁分割的后处理）；`scipy.optimize` 用于曲线拟合（拟合 Paris 裂纹扩展公式 `da/dN = C(ΔK)^m` 中的参数 C 和 m）；`scipy.sparse` 提供稀疏矩阵支持（有限元刚度矩阵的高效存储和求解）。

**Pandas** 是处理表格型数据的标准工具。在材料成分-性能数据库整理、生物实验的多样本批量数据管理、以及多通道传感器数据的合并和清洗方面，Pandas 几乎不可缺少。它的核心数据结构 DataFrame 可以理解为"有标签行列的 NumPy 矩阵"，支持 SQL 风格的分组聚合、时间序列重采样等操作。

**Matplotlib** 和 **Seaborn** 是绘图的主力工具。Matplotlib 提供精细的底层控制（可以精确调整坐标轴范围、字体大小、线型、颜色、图例位置等，满足期刊投稿对图像格式的严格要求）；Seaborn 在 Matplotlib 基础上提供更美观的统计图表（箱线图、热图、散点图矩阵等），适合快速的探索性可视化。论文中的 XRD 衍射图谱、S-N 疲劳寿命曲线、细胞活性的统计箱线图，都可以用这两个库制作出版级图形。

**scikit-learn** 是传统机器学习算法的标准库，覆盖随机森林、支持向量机、主成分分析（PCA）、Lasso/Ridge 回归、k 近邻等在科学数据分析中最常用的算法。深度学习章节反复强调"不是所有问题都需要深度学习"——scikit-learn 正是在样本量有限、特征有明确物理含义时的首选工具。

如果你的研究需要深度学习（图像分类、序列预测、物理信息神经网络等），安装 **PyTorch**：

```bash
# CPU 版本（无 NVIDIA 显卡时使用，macOS M 系列芯片也用此命令，PyTorch 通过 MPS 自动调用 GPU）
conda install pytorch torchvision torchaudio -c pytorch -y

# NVIDIA GPU 版本（需要先确认 CUDA 版本：nvidia-smi 查看；以 CUDA 12.1 为例）
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y
```

领域专用库同样值得关注。生物信息学方向：`conda install -c conda-forge biopython -y`（序列分析、PDB 蛋白质结构文件解析）。材料科学方向：`conda install -c conda-forge pymatgen -y`（Materials Project 数据库 API 接口、晶体结构分析和对称性操作）。计算力学方向：`conda install -c conda-forge fenics-dolfinx -y`（FEniCSx 有限元求解框架，适用于自定义 PDE 的数值求解）。通用仿真数据格式：`conda install -c conda-forge h5py netcdf4 -y`（读写 HDF5 和 NetCDF 格式文件，常见于有限元输出和大规模仿真数据存储）。

---

## 六、JupyterLab：交互式科研计算的核心工作环境

JupyterLab 是当代科学计算中最广泛使用的交互式编程环境。它在浏览器中运行，在同一个界面里集成了代码编辑与执行、图表内嵌显示、Markdown 格式文字记录、LaTeX 数学公式渲染、文件系统浏览，以及嵌入式终端。对于需要同时展示实验数据、计算逻辑、可视化结果和科学解释的科研工作，Notebook 这种"可计算文档"形式具有无可替代的价值——它不仅是一个编程工具，更是一种记录科学探索过程的媒介，使得"代码即是实验记录"成为可能。

激活 conda 环境后启动 JupyterLab：

```bash
conda activate matsci
jupyter lab
```

JupyterLab 会自动在默认浏览器中打开，地址通常是 `http://localhost:8888`。如果在远程服务器（HPC 集群或云主机）上工作，无法直接在浏览器访问，需要使用 SSH 端口转发：

```bash
# 在本地终端运行（将服务器的 8888 端口映射到本地 8888）
ssh -L 8888:localhost:8888 用户名@服务器IP
# 然后在服务器端启动 JupyterLab（不自动打开浏览器）
jupyter lab --no-browser --port=8888
# 复制服务器终端输出的 token URL，粘贴到本地浏览器即可访问
```

理解 **Kernel（内核）**的概念对于正确使用 JupyterLab 至关重要。Kernel 是 Notebook 后台实际执行代码的 Python 进程，与 JupyterLab 的界面层完全分离。每个 Notebook 有一个关联的 Kernel，Kernel 的 Python 环境决定了你能 `import` 哪些包。当你遇到 `ModuleNotFoundError: No module named 'torch'` 时，最常见的原因不是 PyTorch 没有安装，而是当前 Notebook 使用的 Kernel 对应的 conda 环境不是你安装 PyTorch 的那个环境。

将 conda 环境注册为 JupyterLab 可选 Kernel 的标准步骤：

```bash
conda activate matsci         # 激活要注册的环境
# ipykernel 若未安装则先安装
conda install -c conda-forge ipykernel -y
# 注册为 Kernel，--display-name 是在 JupyterLab 界面显示的名称
python -m ipykernel install --user --name matsci --display-name "Python (matsci)"
```

注册完成后，在 JupyterLab 的 Launcher 页面（新建 Notebook 时）或 Notebook 右上角的 Kernel 选择器中，会出现"Python (matsci)"选项。每个 conda 环境都可以单独注册为 Kernel，在同一个 JupyterLab 实例中可以运行关联不同环境的多个 Notebook，无需重新启动 JupyterLab。

几个高频使用的 JupyterLab 技巧值得记录：**魔法命令（Magic Commands）**是 Jupyter 独有的便捷功能，`%timeit func()` 自动多次运行并统计执行时间，适合评估不同算法的计算效率；`%matplotlib inline` 使图表直接嵌入 Notebook 单元格输出；`%%bash` 使整个单元格作为 shell 命令执行（可以在 Notebook 里直接运行 `conda list`）。**Tab 自动补全**和**内联文档查询**（在函数名后加 `?` 再按 Shift+Enter 显示完整文档字符串）是减少查文档时间的核心技巧。Notebook 文件本质上是 JSON 格式，可以用 git 进行版本控制，配合 **nbstripout** 工具（`conda install -c conda-forge nbstripout`）在提交前自动清除输出单元格，使 git diff 只显示代码变更而不是输出数据，大幅提升代码审查的可读性。

---

## 七、VS Code 集成——从探索到工程化开发

JupyterLab 适合探索性分析：你不确定数据的形态，需要一步一步尝试，每步的输出立即可见，非常适合"边做边想"的科研初期。当分析逻辑逐渐稳定，需要将代码整理成可重复运行的脚本、构建数据处理流水线、或者编写可供他人调用的分析模块时，**VS Code（Visual Studio Code）**是更合适的开发环境。两者并不互斥，实际工作流往往是：JupyterLab 中探索 → 确认逻辑后迁移到 VS Code 中重构为 .py 脚本。

从 `https://code.visualstudio.com` 下载安装 VS Code（Windows、macOS、Linux 均有对应版本）。安装后，在左侧扩展面板（快捷键 `Ctrl+Shift+X`，macOS 为 `Cmd+Shift+X`）搜索并安装以下扩展：

- **Python**（Microsoft 官方扩展）：提供语法高亮、代码补全（IntelliSense）、Linting（代码风格检查）、内联变量查看和断点调试
- **Jupyter**（Microsoft）：在 VS Code 内直接打开和编辑 .ipynb 文件，且支持将 .py 脚本以 `# %%` 注释划分为可单独运行的 Cell，无需 .ipynb 格式也能享受交互式执行

安装 Python 扩展后，按 `Ctrl+Shift+P`（macOS `Cmd+Shift+P`）打开命令面板，输入 `Python: Select Interpreter`，在列表中选择你的 conda 环境对应的 Python 路径（路径中通常包含 `envs/matsci` 字样，例如 `/home/用户名/miniconda3/envs/matsci/bin/python`）。选择正确的解释器后，代码补全、Linting 和调试都会使用该 conda 环境中安装的包。

VS Code 对科研工作者最具价值的特性之一是**远程开发（Remote Development）**。通过安装 **Remote - SSH** 扩展，可以在本地 Mac 或 Windows 电脑的 VS Code 界面上直接编辑和运行存储在远程服务器上的代码——本地享有高分辨率屏幕、熟悉的键盘布局和完整的 IDE 功能，计算实际在服务器的 GPU 或大内存上执行。对于需要在 HPC 集群运行有限元仿真后处理、或者在实验室服务器上训练深度学习模型的研究生，这种工作方式的效率远优于在服务器终端中用 `vim` 或 `nano` 编辑代码。配置方法：安装扩展后按 `F1` 打开命令面板，选择 `Remote-SSH: Connect to Host`，输入 `用户名@服务器IP`，VS Code 会自动完成连接，之后的操作与本地完全一致。

---

## 八、conda 与 pip 的关系与最佳实践

使用 conda 管理环境的过程中，迟早会遇到某些包在 conda 频道无法找到，只能用 pip 安装的情况。正确理解 conda 和 pip 的分工，是避免环境依赖混乱的关键。

**conda** 是一个**通用软件包管理器**，管理范围涵盖 Python 包、Python 解释器本身，以及各类非 Python 底层依赖（C/C++ 共享库、编译工具链、CUDA 运行时等）。conda 在安装一个包时，会完整地解析该包及其全部依赖的版本兼容关系，然后一次性将整个依赖树安装到位，确保所有组件版本相互兼容。这个依赖求解过程在科学计算包（往往有复杂的 C 扩展依赖）上表现尤为重要。

**pip** 是 **Python 专用的包管理器**，只处理 Python 层面的包，不管理底层二进制依赖。pip 的依赖求解能力相对较弱：它可能在安装包后才发现依赖冲突，而不是在安装前就提示。但 pip 覆盖的包数量远多于 conda，很多新发布的研究代码（尤其是 GitHub 上的实验性库）只发布在 PyPI（pip 的包仓库），没有对应的 conda 包。

在同一个 conda 环境中混用 conda 和 pip 是完全合理的，但必须遵守一个操作顺序原则：**先用 conda 安装所有能用 conda 安装的包，最后才用 pip 安装 conda 没有的包**。原因在于：conda 的依赖求解器遇到已经由 pip 安装的包时，无法准确识别其版本信息，可能做出错误的依赖判断——如果先大量用 pip 安装包，再用 conda 安装其他包，conda 可能会将 pip 安装的包覆盖或强制降级，破坏原有配置。

判断某个包应该用 conda 还是 pip 安装，建议按以下原则：纯 Python 包（如 NumPy、Pandas、Matplotlib）优先用 pip 安装，速度快且版本新；需要编译 C/Fortran 扩展或有复杂二进制依赖的包（如 PyTorch、FEniCSx）才用 conda 安装。具体操作时，在 conda-forge 频道搜索（`conda search -c conda-forge 包名`）；如果 conda-forge 有且版本足够新，用 conda 安装；如果没有或版本过旧，再用 pip 安装。conda-forge 是由开源社区维护的 conda 包仓库，覆盖极为广泛，包括 BioPython、pymatgen、FEniCSx、NGsolve 等专业科学计算包，大多数情况下 conda-forge 的版本更新速度并不慢于 PyPI。

```bash
# 推荐操作顺序示例
conda activate matsci

# 第一步：用 conda 安装所有能找到的包
conda install -c conda-forge numpy scipy pandas matplotlib scikit-learn -y
conda install -c conda-forge biopython pymatgen -y

# 最后一步：仅对 conda 找不到的包使用 pip
pip install some-niche-library-only-on-pypi
```

---

## 九、国内网络环境下的加速配置

国内用户在安装 conda 包时经常遇到下载缓慢甚至连接超时的问题，原因是 conda 的默认下载源服务器位于境外。将下载源替换为国内高校维护的镜像站，可以将安装速度提升数个数量级。以下以稳定性和更新频率均较高的**清华大学 TUNA 镜像**为例：

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
```

配置完成后，执行 `conda install` 时终端输出的下载地址会变更为 `tuna.tsinghua.edu.cn`，原本需要数分钟的下载通常在数十秒内完成。如果 TUNA 镜像某一时刻不稳定，北京外国语大学开源软件镜像（`mirrors.bfsu.edu.cn`）是同样可靠的备选。

pip 也可以配置国内镜像。临时使用（不修改配置文件）：

```bash
pip install 包名 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/
```

永久配置（修改 pip 配置文件）：

```ini
# Windows：%APPDATA%\pip\pip.ini
# macOS/Linux：~/.pip/pip.conf  或  ~/.config/pip/pip.conf
[global]
index-url = https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/
trusted-host = mirrors.tuna.tsinghua.edu.cn
```

如果配置镜像之后 `conda install` 仍然偶尔在"Solving environment"步骤卡很长时间，这通常是 conda 自带的 Python 依赖求解器的性能瓶颈（与网络无关）。此时安装 Mamba 是最有效的解决方案——Mamba 的 C++ 求解器在同样的依赖关系下往往在几秒内完成，而 conda 可能需要数分钟。

---

## 十、常见问题排查手册

即使按照上述步骤逐一操作，仍然可能遇到环境配置问题。以下整理了各平台最高频的故障现象和对应的排查思路，按"症状 → 根本原因 → 解决方案"的格式给出，方便直接对号入座。

**`conda` 命令不被识别（Windows CMD 或 PowerShell）**

症状：打开命令提示符（CMD）或 PowerShell，输入 `conda` 提示"'conda' 不是内部或外部命令"或"未找到命令"。根本原因：安装时未勾选"Add to PATH"，或者使用了普通 CMD 而非 Anaconda Prompt。解决方案：从开始菜单打开 **Anaconda Prompt** 代替普通 CMD；若坚持要在 PowerShell 中使用，以管理员身份运行 `Set-ExecutionPolicy RemoteSigned`，然后运行 `conda init powershell`，重启 PowerShell 后生效。

**`conda activate` 报错（macOS / Linux）**

症状：运行 `conda activate matsci` 提示 `CommandNotFoundError` 或"conda activate is not supported in non-interactive shells"。根本原因：conda 的 shell 初始化脚本未加载，通常是因为安装时 `conda init` 步骤未执行。解决方案：运行 `conda init zsh`（macOS 默认）或 `conda init bash`（Linux 默认），然后关闭并重新打开终端，使 `~/.zshrc` 或 `~/.bashrc` 中新写入的初始化代码生效。

**Jupyter Notebook 中 `import` 某个包报 `ModuleNotFoundError`**

症状：明明已经 `conda install` 了某个包，但在 Notebook 中 `import` 时提示找不到模块。根本原因：Notebook 使用的 Kernel 与安装包的 conda 环境不一致。排查方法：在 Notebook 第一个单元格运行 `import sys; print(sys.executable)`，查看当前 Kernel 实际使用的 Python 解释器路径，确认它是否包含你期望的 conda 环境名称。解决方案：按第六节的步骤重新注册 ipykernel，然后在 Notebook 右上角切换 Kernel 到正确的环境。

**Windows 上安装包后 `import` 出现 `DLL load failed`**

症状：安装某包后 `import` 时出现 `ImportError: DLL load failed while importing xxx`。根本原因：缺少 Microsoft Visual C++ Redistributable 运行时库。解决方案：在微软官网搜索"Visual C++ Redistributable"下载并安装最新版本（同时安装 x64 和 x86 版本），重启电脑后重试。

**macOS Apple Silicon 上某些包安装失败（架构不兼容）**

症状：在 M 系列芯片 Mac 上 `conda install` 某些包时提示找不到 arm64 架构版本，或安装后无法 `import`。根本原因：该包尚未提供 Apple Silicon 原生编译版本。临时方案：创建一个 Rosetta 2 兼容的 x86_64 环境专门运行不兼容包（`CONDA_SUBDIR=osx-64 conda create -n compat_env python=3.10 -y`），注意该环境的性能会受影响。更好的方案是优先在 conda-forge 检索——社区维护者通常会快速提供 arm64 编译版本，conda-forge 的版本往往比官方 conda 频道更新更快。

**`conda install` 长时间卡在"Solving environment..."**

根本原因：Conda 默认的依赖求解算法（SAT solver）在依赖关系复杂时效率低下，与网络速度无关。解决方案：安装 Mamba（`conda install -n base -c conda-forge mamba -y`），之后将 `conda install` 替换为 `mamba install`，解决速度通常从分钟级降至秒级。

遇到本文未覆盖的问题时，推荐在 Stack Overflow 上用**英文**搜索完整的错误信息（中文搜索结果通常更少且更旧），或在 conda-forge GitHub Issues（`github.com/conda-forge/conda-forge.github.io/issues`）中检索。几乎所有常见的环境配置问题都已经有人遇到并留下了解决记录。

---

## 参考文献

1. Anaconda, Inc. (2024). Anaconda Distribution Documentation. Anaconda, Inc. https://docs.anaconda.com

2. conda Contributors (2024). Conda User Guide (Version 24.x). conda.io. https://docs.conda.io/en/latest/

3. Project Jupyter (2024). JupyterLab Documentation. ReadTheDocs / GitHub. https://jupyterlab.readthedocs.io

4. Microsoft (2024). Python in Visual Studio Code — Getting Started Tutorial. Microsoft Docs. https://code.visualstudio.com/docs/python/python-tutorial

5. Pérez, F., & Granger, B. E. (2007). IPython: A System for Interactive Scientific Computing. *Computing in Science & Engineering*, 9(3), 21–29. https://doi.org/10.1109/MCSE.2007.53

6. Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. *Nature*, 585, 357–362. https://doi.org/10.1038/s41586-020-2649-2

7. Virtanen, P., Gommers, R., Oliphant, T. E., et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods*, 17, 261–272. https://doi.org/10.1038/s41592-019-0686-2

8. McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference (SciPy 2010)*, 56–61. https://doi.org/10.25080/Majora-92bf1922-00a