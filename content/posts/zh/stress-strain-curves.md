---
title: "应力-应变曲线解读：材料力学入门"
date: "2026-06-26"
category: "biomaterials"
tags: ["应力-应变", "力学", "生物材料", "弹性模量", "教程"]
lang: "zh"
slug: "stress-strain-curves-zh"
description: "面向生物/材料研究生的应力-应变曲线入门指南：弹性模量、屈服强度、极限强度、韧性，以及生物材料的特殊性。"
---

## 为什么每个材料人都要懂这个

应力-应变曲线是材料科学最重要的图。它告诉你材料有多硬、能拉多长、吸收多少能量。无论你研究丝素蛋白、水凝胶还是骨头，这都是基础。

**应力 = 力 / 截面积。应变 = 长度变化量 / 原始长度。**

## 曲线的五个关键区域

| 区域 | 发生什么 | 关键参数 |
|------|------|------|
| 弹性区 | 变形可逆 | 杨氏模量 E |
| 屈服点 | 永久变形开始 | 屈服强度 |
| 塑性区 | 永久变形累积 | 加工硬化 |
| 极限点 | 最大应力 | 抗拉强度 UTS |
| 断裂点 | 材料破坏 | 断裂伸长率 |

## Python计算力学参数

```python
import numpy as np
def compute_properties(strain, stress):
    elastic = strain < 0.02
    E, _ = np.polyfit(strain[elastic], stress[elastic], 1)
    UTS = np.max(stress)
    toughness = np.trapz(stress, strain)
    return {"E_MPa": E, "UTS_MPa": UTS, "elongation_pct": strain[-1]*100, "toughness_MJ_m3": toughness}
```

## 生物材料的特殊性

软生物材料与金属行为不同：没有明显屈服点（用0.2%偏移法）、应变率依赖（报告速率）、含水量影响巨大（始终在水合态下测试）、J形曲线常见（趾区+线性区）、滞回是能量耗散而非塑性。

## 常见错误

混淆工程应力与真实应力（大应变>10%时差异显著）、不报告样品尺寸、夹具滑移被误认为额外应变。

## 参考文献
- Callister, W.D. (2018). *Materials Science and Engineering*. Wiley.
- Meyers, M.A. (2009). *Mechanical Behavior of Materials*. Cambridge.
