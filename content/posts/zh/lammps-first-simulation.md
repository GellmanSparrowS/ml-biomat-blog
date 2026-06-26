---
title: "分子动力学入门：你的第一个LAMMPS模拟"
date: "2026-06-27"
category: "multiscale-modeling"
tags: ["分子动力学", "LAMMPS", "模拟", "教程", "力场"]
lang: "zh"
slug: "lammps-first-simulation-zh"
description: "手把手教你跑第一个分子动力学模拟：LAMMPS安装、输入脚本结构、力场选择、水盒子模拟和轨迹分析。"
---

## 什么是分子动力学

MD通过在每个时间步求解牛顿运动方程(F=ma)来模拟原子运动。给定了初始位置、速度和力场(势能函数)，MD预测系统如何随时间演化。

对于生物材料研究，MD可以回答：
- 胶原微纤维的杨氏模量是多少？
- 水分子如何与丝素蛋白表面相互作用？
- 蛋白质在拉伸载荷下会发生什么？

## 安装LAMMPS

LAMMPS来自Sandia国家实验室，是最广泛应用的开源MD代码。

**方法一：预编译二进制（推荐新手）**
```bash
sudo apt install lammps        # Linux (Ubuntu/Debian)
brew install lammps             # macOS
# Windows: https://packages.lammps.org/windows.html
```

**方法二：Conda（跨平台）**
```bash
conda create -n lammps -c conda-forge lammps -y
conda activate lammps
```

验证安装：
```bash
lmp_serial -h
```

## LAMMPS输入脚本结构

一个LAMMPS输入文件有四个基本部分：

```bash
# 1. 初始化
units           real        # 能量: kcal/mol, 距离: 埃
atom_style      full        # 原子带电荷、分子ID
boundary        p p p       # 所有方向周期性边界

# 2. 系统设置
region          box block 0 30 0 30 0 30
create_box      2 box       # 2种原子类型
create_atoms    1 random 500 12345 box

# 3. 力场
pair_style      lj/cut 10.0
pair_coeff      1 1 0.155 3.166  # O-O LJ参数

# 4. 运行
velocity        all create 300.0 12345
fix             nvt all nvt temp 300.0 300.0 100.0
thermo          100
dump            traj all custom 100 dump.lammpstrj id type x y z
run             10000
```

## 第一个模拟：水盒子

用TIP3P模型模拟500个水分子在室温下：

```bash
# water.lammps
units           real; atom_style      full
bond_style      harmonic; angle_style     harmonic

read_data       water_box.data
pair_style      lj/cut/coul/long 10.0 10.0
kspace_style    pppm 1e-5

minimize        1e-4 1e-6 1000 10000     # 能量最小化
velocity        all create 300.0 12345
fix             nvt all nvt temp 300.0 300.0 100.0
run             50000                     # NVT平衡
fix             npt all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0
run             100000                    # NPT生产
```

## 关键参数

| 参数 | 含义 | 典型值 |
|------|------|--------|
| timestep | 积分步长 | 1.0-2.0 fs |
| cutoff | 非键作用截断距离 | 10-12 埃 |
| temperature | 系统温度 | 300 K(室温) |
| NVT | 恒粒子数/体积/温度 | 平衡阶段 |
| NPT | 恒粒子数/压力/温度 | 生产阶段 |

## 常用力场

| 力场 | 适用 | 参考文献 |
|------|------|---------|
| OPLS-AA | 蛋白质、有机分子 | Jorgensen (1996) |
| CHARMM36 | 蛋白质、核酸 | Best (2012) |
| AMBER ff19SB | 蛋白质 | Tian (2020) |
| ReaxFF | 反应体系、断键 | van Duin (2001) |
| Martini | 粗粒化生物分子 | Marrink (2007) |

## 轨迹分析

```python
import MDAnalysis as mda
from MDAnalysis.analysis import rdf

u = mda.Universe("water_box.data", "dump.lammpstrj")
oxygen = u.select_atoms("type O")
rdf_oo = rdf.InterRDF(oxygen, oxygen, nbins=200, range=(0, 10.0))
rdf_oo.run()
```

## 常见问题

| 问题 | 解决 |
|------|------|
| "Lost atoms"错误 | 减小timestep或增大neighbor list skin |
| 能量不收敛 | 更长最小化或用更软的初始条件 |
| 模拟太慢 | 用GPU(Kokkos)或更粗的力场 |

## 参考资料

- LAMMPS文档: [docs.lammps.org](https://docs.lammps.org)
- MDAnalysis: [mdanalysis.org](https://www.mdanalysis.org)
- Allen & Tildesley (2017). *Computer Simulation of Liquids*. Oxford.
- GitHub: [lammps/lammps](https://github.com/lammps/lammps)
