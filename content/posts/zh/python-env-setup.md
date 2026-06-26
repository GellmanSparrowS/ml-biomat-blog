---
title: "Python科学计算环境搭建指南：从零开始到顺利跑代码"
date: "2026-06-26"
category: "python-tutorials"
tags: ["python", "conda", "jupyter", "环境配置", "科学计算"]
lang: "zh"
slug: "python-env-setup-zh"
description: "面向生物/材料研究生的Python环境搭建完整指南：Miniconda、Jupyter、VS Code、包管理和常见问题解决。"
---

## 你需要这篇指南

你是生物、化学或材料科学的研究生。你听说Python可以帮你处理数据，但从来没有搭建过编程环境。这篇指南带你从零开始——不假设任何先验知识。

## 第一步：安装Miniconda

为什么选Miniconda而不是Anaconda？Miniconda体积小（约50MB vs 500MB），安装快，只装你需要的包。打开docs.conda.io下载对应操作系统的安装包，运行安装程序。重要：勾选"Add Miniconda to PATH"。验证：`conda --version`

## 第二步：创建环境

```bash
conda create -n matsci python=3.10 -y
conda activate matsci
```

## 第三步：安装科学计算包

```bash
conda install numpy scipy pandas matplotlib jupyter -y
conda install -c conda-forge seaborn scikit-learn scikit-image -y
# 国内用户设置清华镜像加速
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
```

验证安装：`python -c "import numpy as np; import scipy; print('成功！')"`

## 第四步：Jupyter Notebook

```bash
cd 你的项目文件夹; jupyter lab  # 推荐lab
```

## 第五步：VS Code

下载code.visualstudio.com，安装Python扩展（Microsoft）。Ctrl+Shift+P > "Python: Select Interpreter" > 选择matsci。推荐扩展：Python, Jupyter, Rainbow CSV, GitLens。

## 常见问题

| 问题 | 解决 |
|------|------|
| conda不被识别 | 重启终端或重装勾选"Add to PATH" |
| 下载慢 | 清华镜像或安装mamba |
| Jupyter找不到内核 | `python -m ipykernel install --user --name matsci` |
| DLL加载失败(Windows) | 安装VC++ Redist |

## 参考文献
- Conda文档: docs.conda.io
- Jupyter文档: docs.jupyter.org
