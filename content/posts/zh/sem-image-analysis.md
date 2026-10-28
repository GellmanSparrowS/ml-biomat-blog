---
title: "SEM图像分析实战：纤维形态的自动化测量"
date: "2026-06-26"
updated: "2026-10-28"
category: "wet-lab-data"
tags: ["SEM", "图像分析", "纤维形态", "python", "skimage"]
lang: "zh"
slug: "sem-image-analysis-zh"
description: "通过预处理、阈值分割、掩膜清理和骨架分析，将纤维显微图像转化为经过标尺校准的测量结果。构造几何解释局部直径和取向提取，Python 示例支持重复执行与批量处理。"
---

## 为什么自动化SEM分析

手动从SEM图像测量纤维直径和取向费时、主观、不可重复。Python脚本能在几秒内一致地处理每张图像。本指南使用scikit-image，专为科学图像分析设计的库。

```python
import numpy as np
from skimage import io, filters, measure, morphology
```

## 分析流程
### 第一步：加载和预处理

```python
img = io.imread("sem_fiber_network.tif", as_gray=True)
img_norm = (img - img.min()) / (img.max() - img.min())

# 高斯去噪
from scipy.ndimage import gaussian_filter
img_denoised = gaussian_filter(img_norm, sigma=1.0)
```

### 第二步：阈值分割

```python
methods = {"Otsu": filters.threshold_otsu(img_denoised),
           "Li": filters.threshold_li(img_denoised),
           "Yen": filters.threshold_yen(img_denoised)}
thresh = methods["Otsu"]  # Otsu通常最适合双峰纤维/背景图
binary = img_denoised > thresh
print(f"纤维覆盖率: {binary.mean()*100:.1f}%")
```

### 第三步：清理二值掩膜

```python
cleaned = morphology.remove_small_objects(binary, min_size=50)
closed = morphology.binary_closing(cleaned, morphology.disk(2))
skeleton = morphology.skeletonize(closed)  # 用于取向分析
```

![同一几何的三种图像表示](/static/images/article-guides/mech-sem-masks-zh.svg)

同一构造纤维几何分别显示为灰度图、前景掩膜和中心线叠加图。阈值选择决定掩膜，骨架则提供采样局部距离变换宽度的位置。

### 第四步：测量纤维属性

```python
labels = measure.label(closed)
props = measure.regionprops_table(labels, properties=[
    "area", "eccentricity", "orientation",
    "major_axis_length", "minor_axis_length"
])
import pandas as pd
df_fibers = pd.DataFrame(props)
df_fibers["等效椭圆短轴_px"] = df_fibers["minor_axis_length"]
df_fibers["长径比"] = df_fibers["major_axis_length"] / df_fibers["minor_axis_length"]
print(f"发现 {len(df_fibers)} 个纤维片段")
print(f"平均等效椭圆短轴: {df_fibers['等效椭圆短轴_px'].mean():.1f} +/- {df_fibers['等效椭圆短轴_px'].std():.1f} px")
```

`regionprops` 返回的 `minor_axis_length` 是与连通区域具有相同归一化二阶矩的等效椭圆短轴，描述整个对象的形状。若要估计孤立纤维沿中心线的局部宽度，可在骨架上读取距离变换；像素网格与分割边界决定了这一估计的分辨率。[scikit-image 区域属性](https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.regionprops)、[SciPy 距离变换](https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.distance_transform_edt.html)。

```python
from scipy.ndimage import distance_transform_edt

# 示例标尺：替换为当前 SEM 图像的标尺值
scale_nm_per_px = 2.5
radius_nm = distance_transform_edt(closed, sampling=scale_nm_per_px)
local_width_nm = 2 * radius_nm[skeleton]
```

![把像素距离转换为局部纤维宽度](/static/images/article-guides/mech-sem-width-zh.svg)

对孤立直条带，局部宽度为 d = 2rpxs，其中 rpx 是骨架点到最近背景的像素距离，s 是每像素对应的物理长度。交叉、分叉和被图像边缘截断的对象需单独检查。

### 第五步：取向分析

![纤维取向分布的极坐标直方图，优势取向约 90 度](/static/images/posts/sem-image-analysis/orientation-zh.webp)

```python
from skimage.transform import radon
theta = np.linspace(0., 180., max(img.shape), endpoint=False)
sinogram = radon(skeleton, theta=theta)
dominant_angle = theta[np.argmax(sinogram.sum(axis=0))]
print(f"主取向: {dominant_angle:.1f} 度")
```

### 第六步：批量处理

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
            "mean_ellipse_minor_axis_nm": df["minor_axis_length"].mean()*scale_nm_per_px})
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
- Ronneberger, O. et al. (2015). U-Net: Convolutional Networks for Biomedical Image Segmentation. *MICCAI*, 234-241.

## 深入探讨：图像分割算法的选择

阈值分割是SEM图像分析最关键的一步，直接影响后续所有量化结果的准确性。Otsu方法假设图像直方图是双峰的——纤维（前景）和背景形成两个明显分离的灰度峰。对于高对比度、光照均匀的SEM图像，Otsu通常是最佳选择。但对于光照不均或背景复杂的图像，局部自适应阈值方法更为合适。

分水岭算法是处理粘连纤维时的有效工具。当纤维在SEM图像中紧密接触时，简单的全局阈值无法将粘连的纤维分开。分水岭算法通过将图像视为地形图——像素值为高度——然后模拟"注水"过程来找到不同纤维之间的分界线。结合距离变换，分水岭算法可以准确分离紧密相邻的纤维。

机器学习方法正在改变SEM图像分析的范式。传统的滤波与阈值方法需要手动调整参数，而训练好的深度学习模型可以在各种成像条件下自动识别纤维特征。U-Net是图像分割的常用架构，仅需少量标注图像就能取得很好的效果。对于有大量重复性SEM分析需求的研究组，考虑训练一个专门的纤维分割模型是值得的投资。
