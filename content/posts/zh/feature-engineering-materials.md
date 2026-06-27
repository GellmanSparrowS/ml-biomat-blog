---
title: "材料科学中的特征工程：从实验记录到机器学习就绪数据"
date: "2026-06-27"
category: "machine-learning"
tags: ["特征工程", "机器学习", "材料科学", "数据预处理"]
lang: "zh"
slug: "feature-engineering-materials-zh"
description: "将实验室实验数据转化为机器学习特征：分类编码、交互特征、缺失值处理和小样本特征选择。"

大多数材料科学的机器学习教程从一个完美的CSV文件开始，直接跳到模型训练。但在真实的实验室环境中，数据分散在实验记录本、仪器导出文件和格式不统一的Excel表格中。特征工程——将原始实验观测转化为结构化数值特征矩阵的过程——占实际机器学习工作量的百分之八十以上，也是决定模型性能的最关键步骤。

## 一、从实验台到数据表

典型的纤维生物材料实验记录包含纤维直径、取向分布、交联密度、处理溶剂类型和测试温度作为特征，杨氏模量作为预测目标。直接将这些信息输入机器学习模型存在明显问题：处理溶剂是文本而非数字、不同特征的数量级差异巨大、缺失值普遍存在、某些特征之间存在物理意义的交互关系。特征工程就是系统性地解决这些问题。

## 二、分类变量的数值编码

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
df = pd.DataFrame({"diameter_nm": [45, 52, 48], "solvent": ["methanol", "ethanol", "water"], "modulus_GPa": [2.8, 1.9, 2.3]})
encoder = OneHotEncoder(sparse_output=False, drop="first")
encoded = encoder.fit_transform(df[["solvent"]])
```

OneHot编码为每个类别创建二进制列，drop="first"参数避免完全共线性。对于有序分类变量如处理强度等级，使用OrdinalEncoder保留顺序信息。

## 三、物理知识驱动的交互特征

这是材料科学家区别于纯数据科学家的关键优势：利用物理知识构造有意义的特征。交联密度与纤维直径的乘积反映了交联点对纤维网络刚度的协同贡献。构造交互特征时应基于明确的物理依据，而非盲目进行多项式扩展。

## 四、缺失值处理策略

小样本情况下，简单的均值填充可能引入显著偏差。分组中位数填充利用相似样品的信息更合理。缺失比率超过百分之三十的特征建议直接丢弃。

## 五、小样本特征选择

样品数量少于一百时，自动化特征选择容易过拟合。推荐使用领域知识辅助的手动筛选：首先去除方差接近零的特征，然后计算特征间相关系数去除冗余，最后基于物理合理性手工选择保留的特征集。

## 六、完整处理管道

将编码、交互特征构造、缺失值处理和标准化整合为可复用的管道函数。当新实验数据到达时，只需修改文件路径并重新运行脚本，所有分析自动完成。

## 参考文献
- Kuhn, M. & Johnson, K. (2019). *Feature Engineering and Selection*. CRC Press.
- Ramprasad, R. et al. (2017). Machine learning in materials informatics. *npj Computational Materials*, 3, 54.
