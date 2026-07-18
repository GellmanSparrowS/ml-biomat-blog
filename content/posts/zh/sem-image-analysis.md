---
title: "SEM图像分析实战：纤维形态的自动化测量"
date: "2026-06-26"
category: "wet-lab-data"
tags: ["SEM", "图像分析", "纤维形态", "python", "skimage"]
lang: "zh"
slug: "sem-image-analysis-zh"
description: "SEM图像分析实战：纤维形态的自动化测量。面向生物与材料科学研究生的实用教程，含完整可运行代码示例与详细原理解析，适合零基础入门与进阶参考。"
---

## 为什么自动化SEM分析

手动从SEM图像测量纤维直径和取向费时、主观、不可重复。Python脚本能在几秒内一致地处理每张图像。本指南使用scikit-image，专为科学图像分析设计的库。

```python
import numpy as np
from skimage import io, filters, measure, morphology
```

## 第一步：加载和预处理

```python
img = io.imread("sem_fiber_network.tif", as_gray=True)
img_norm = (img - img.min()) / (img.max() - img.min())

# 高斯去噪
from scipy.ndimage import gaussian_filter
img_denoised = gaussian_filter(img_norm, sigma=1.0)
```

## 第二步：阈值分割

```python
methods = {"Otsu": filters.threshold_otsu(img_denoised),
           "Li": filters.threshold_li(img_denoised),
           "Yen": filters.threshold_yen(img_denoised)}
thresh = methods["Otsu"]  # Otsu通常最适合双峰纤维/背景图
binary = img_denoised > thresh
print(f"纤维覆盖率: {binary.mean()*100:.1f}%")
```

## 第三步：清理二值掩膜

```python
cleaned = morphology.remove_small_objects(binary, min_size=50)
closed = morphology.binary_closing(cleaned, morphology.disk(2))
skeleton = morphology.skeletonize(closed)  # 用于取向分析
```

## 第四步：测量纤维属性

```python
labels = measure.label(closed)
props = measure.regionprops_table(labels, properties=[
    "area", "eccentricity", "orientation",
    "major_axis_length", "minor_axis_length"
])
import pandas as pd
df_fibers = pd.DataFrame(props)
df_fibers["直径_px"] = df_fibers["minor_axis_length"]
df_fibers["长径比"] = df_fibers["major_axis_length"] / df_fibers["minor_axis_length"]
print(f"发现 {len(df_fibers)} 个纤维片段")
print(f"平均直径: {df_fibers['直径_px'].mean():.1f} +/- {df_fibers['直径_px'].std():.1f} px")
```

## 第五步：取向分析

```python
from skimage.transform import radon
theta = np.linspace(0., 180., max(img.shape), endpoint=False)
sinogram = radon(skeleton, theta=theta)
dominant_angle = theta[np.argmax(sinogram.sum(axis=0))]
print(f"主取向: {dominant_angle:.1f} 度")
```

## 第六步：批量处理

```python
import glob
def batch_analyze_sem(image_dir, scale_nm_per_px=10.0):
    results = []
    for filepath in glob.glob(f"{image_dir}/*.tif"):
        img = io.imread(filepath, as_gray=True)
        binary = (img-img.min())/(img.max()-img.min()) > filters.threshold_otsu(img)
        cleaned = morphology.remove_small_objects(binary, 50)
        props = measure.regionprops_table(measure.label(cleaned),
            properties=["minor_axis_length", "area"])
        df = pd.DataFrame(props)
        results.append({"file": filepath, "n_fibers": len(df),
            "mean_diameter_nm": df["minor_axis_length"].mean()*scale_nm_per_px})
    return pd.DataFrame(results)
```

## 常见坑

| 问题 | 解决 |
|------|------|
| 光照不均 | 用滚动球背景扣除 |
| 纤维粘连 | 用分水岭分割 |
| 过分割 | 增大min_size |
| 标尺错误 | 始终验证像素-纳米标定 |

## 参考资料

- van der Walt, S. et al. (2014). scikit-image. *PeerJ*, 2, e453.
- GitHub: [scikit-image/scikit-image](https://github.com/scikit-image/scikit-image)


## 深入探讨：图像分割算法的选择

阈值分割是SEM图像分析最关键的一步，直接影响后续所有量化结果的准确性。Otsu方法假设图像直方图是双峰的——纤维（前景）和背景形成两个明显分离的灰度峰。对于高对比度、光照均匀的SEM图像，Otsu通常是最佳选择。但对于光照不均或背景复杂的图像，局部自适应阈值方法更为合适。

分水岭算法是处理粘连纤维时的有效工具。当纤维在SEM图像中紧密接触时，简单的全局阈值无法将粘连的纤维分开。分水岭算法通过将图像视为地形图——像素值为高度——然后模拟"注水"过程来找到不同纤维之间的分界线。结合距离变换，分水岭算法可以准确分离紧密相邻的纤维。

机器学习方法正在改变SEM图像分析的范式。传统的滤波与阈值方法需要手动调整参数，而训练好的深度学习模型可以在各种成像条件下自动识别纤维特征。U-Net是图像分割的常用架构，仅需少量标注图像就能取得很好的效果。对于有大量重复性SEM分析需求的研究组，考虑训练一个专门的纤维分割模型是值得的投资。

## 参考文献
- Ronneberger, O. et al. (2015). U-Net: Convolutional Networks for Biomedical Image Segmentation. *MICCAI*, 234-241.
