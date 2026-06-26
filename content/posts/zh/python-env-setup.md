---
title: "Python科学计算环境搭建指南：从零开始到顺利跑代码"
date: "2026-06-26"
category: "python-tutorials"
tags: ["python", "conda", "jupyter", "环境配置", "科学计算"]
lang: "zh"
slug: "python-env-setup-zh"
description: "面向生物/材料研究生的Python环境搭建完整指南：Miniconda、Jupyter、VS Code、包管理和常见问题解决。"
---

## 谁需要这篇指南

你是生物、化学或材料科学的研究生。你听说Python可以帮你处理数据，但从来没有搭建过编程环境。这篇指南带你从零开始——不假设任何先验知识。

## 第一步：安装Miniconda

**为什么选Miniconda而不是Anaconda？** Miniconda体积小（~50 MB vs ~500 MB），安装快，只装你需要的包。

1. 打开 [docs.conda.io](https://docs.conda.io/en/latest/miniconda.html)
2. 下载对应操作系统的安装包
3. 运行安装程序。**重要：勾选"Add Miniconda to PATH"**
4. 验证安装：

```bash
conda --version
```

## 第二步：创建环境

```bash
conda create -n matsci python=3.10 -y
conda activate matsci
```

## 第三步：安装科学计算包

```bash
conda install numpy scipy pandas matplotlib jupyter -y
conda install -c conda-forge seaborn scikit-learn scikit-image -y
```

如果下载慢，可以用清华镜像（国内用户）：

```bash
# 设置清华镜像
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes
```

验证安装：

```python
import numpy as np; import scipy; import pandas as pd
import matplotlib.pyplot as plt; import sklearn
print(f"NumPy: {np.__version__}, Pandas: {pd.__version__}")
print("所有包安装成功！")
```

## 第四步：Jupyter Notebook

```bash
cd 你的项目文件夹
jupyter notebook   # 或 jupyter lab（推荐）
```

## 第五步：VS Code

1. 下载 [code.visualstudio.com](https://code.visualstudio.com)
2. 安装Python扩展（Microsoft）
3. `Ctrl+Shift+P` > "Python: Select Interpreter" > 选择`matsci`

推荐扩展：Python, Jupyter, Rainbow CSV, GitLens

## 第六步：包管理速查

```bash
conda list              # 查看已安装包
conda install numpy=1.24.3  # 安装特定版本
conda env export > environment.yml  # 导出环境
conda env create -f environment.yml  # 从文件重建
```

## 常见问题

| 问题 | 解决方案 |
|---------|---------|
| conda不被识别 | 重启终端或重装并勾选"Add to PATH" |
| 下载慢 | 用清华镜像(国内)或安装mamba |
| Jupyter找不到内核 | `python -m ipykernel install --user --name matsci` |
| DLL加载失败(Windows) | 安装[VC++ Redist](https://aka.ms/vs/17/release/vc_redist.x64.exe) |

## 参考资料

- Conda文档: [docs.conda.io](https://docs.conda.io)
- Jupyter文档: [docs.jupyter.org](https://docs.jupyter.org)
- 清华镜像: [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)
