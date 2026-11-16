# 从显微图像测量结构

Source: https://ml-biomat.com/tutorials/python-scientific/s01/
Language: zh-CN

把一幅真实细胞相位图变成有单位、有边界定义、能追问参数影响的面积测量。

## 显微镜里的大小，怎样变成可以比较的数字

观察水凝胶中的细胞、聚合物薄膜的孔洞或金属中的晶粒时，我们很容易说出“这个更大”“边界更粗糙”。要比较不同处理条件，就需要把这些观察变成测量。图像分析承担的正是这一步：先明确要测哪个对象，再把它从图像中找出来，最后用标定尺度把像素换算成实际长度或面积。本章围绕一幅真实的细胞定量相位图展开，使用 scikit-image 找到其中最大的明亮连通区域，计算投影面积和等效圆直径，同时查看这些结果怎样随边界选择改变。图、代码和交互使用同一张原图，因此可以沿着每一步核对测量的来由。

这幅公开图像来自 scikit-image 的 `cell` 数据，记录盐水中的一个细胞，空间采样间隔为每像素 0.107 μm。图像共有 660 行、550 列，细胞位于画面右侧。按照本章定义的处理流程，Otsu 阈值为 122，填充内部孔洞后选中的区域包含 11746 个像素，投影面积约为 134.48 μm²，等效圆直径约为 13.09 μm。这里的“约”对应结果的呈现精度；完整数值和计算条件都保存在示例输出中。先知道最终会得到什么，后面再逐步解释每个数值为何成立，会比一开始记住一串图像处理函数更容易理解。

测量对象需要说得具体。本章测的是这张二维图中按灰度规则选出的投影区域，并把面积换算成一个便于比较的圆直径。细胞的三维体积、膜表面的真实起伏和内部组分浓度，都需要另外的观测或模型。这样的区分与拿尺子量叶片很相似：沿桌面看到的轮廓可以给出投影面积，叶片卷曲时，投影面积和整个表面积就有不同含义。先把对象定义清楚，随后每一次阈值、填孔或标定选择才有判断依据。

![原始细胞相位图、局部边界和一条水平灰度剖面。所有空间坐标均使用 0.107 μm/像素标定；黄色线为阈值 122 下最大区域的外边界。](https://ml-biomat.com/static/tutorials/python-scientific/figures/b06b9d460d3b3ed43af5d353.svg?v=b06b9d460d3b)

图 1原始细胞相位图、局部边界和一条水平灰度剖面。所有空间坐标均使用 0.107 μm/像素标定；黄色线为阈值 122 下最大区域的外边界。

## 先把图像读成一张有位置的数表

一幅灰度数字图像可以看成铺满小方格的地图。每个格子称为像素，格子中的数字决定它在显示时有多亮。调用 `io.imread` 后，本章图片成为一个二维 NumPy 数组，`image.shape` 返回 `(660, 550)`。前一个数字表示行数，后一个表示列数。读取 `image[370, 400]` 时，先沿竖直方向找到第 370 行，再沿水平方向找到第 400 列；Python 的索引从 0 开始。绘图中的横坐标通常对应列，纵坐标对应行，这个顺序差异在绘制边界时尤其需要明确。

数组类型是 `uint8`，意思是每个值用 8 位无符号整数保存，可取 0 到 255。本章直接使用文件保存的灰度范围，阈值 122 因而也处于同一范围。将图像转换成浮点类型，和把数值缩放到 0 到 1，是两件不同的操作；前者可能只是把 122 写成 122.0，后者则会改变阈值的数值尺度。许多图像处理错误正是从这两步混淆开始的。先查看形状、类型、最小值和最大值，再选择处理参数，能够让代码与实际数据保持一致。

这张图来自定量相位成像。这样的成像关注光穿过样品后发生的相位变化，图中的灰度是所提供图像对这些信息的编码。这里读取的是公开的 8 位图像，不把灰度值直接当作具有弧度单位的原始相位，更不把它直接换算成某种分子的浓度。对于当前任务，我们利用的是细胞区域与背景在灰度上的差异。图中的水平剖面把第 370 行依次经过的像素画成曲线，显示背景、较暗边缘和明亮内部怎样沿着空间位置变化，从而把“看上去有个细胞”与“数组中哪些数字发生了变化”连接起来。

图像坐标还应与空间采样一致。示例把像素外边界从 0 开始排列，每个像素中心位于其格子的中点，所以绘制剖面和轮廓时使用半个像素的中心偏移。纵坐标向下增加，和图像的行编号一致。这个约定使原图、局部放大图和剖面之间能够准确对齐。当你换用显微镜软件导出的图像时，应先核对尺度、坐标方向与是否经过缩放，再沿用同样的表示方法。

## 从人工划线到 Otsu：怎样选择一个灰度界限

想把明亮区域从背景中分出来，可以先规定一个阈值：灰度严格大于这个值的像素记为真，其余记为假。代码 `image > threshold` 一次比较整张数组，返回同样形状的布尔数组。这张真假地图称为掩膜，它回答“当前规则把哪些像素算进对象”。阈值降低，更多像素进入掩膜；阈值提高，边缘和较暗内部会逐渐退出。阈值分割适用于目标与背景能够凭灰度区分的场景，而选择怎样的阈值，则需要查看图像的灰度分布。

直方图把所有像素按灰度分组，横轴是灰度值，纵轴是落入各组的像素数。它抹去了位置，却保留了明暗分布。本例有大量背景像素集中在较暗的一侧，较少的细胞像素分布在较亮的一侧。由于两类数量相差较大，图中像素数采用对数坐标，便于同时看清背景峰和亮侧分布。对数显示改变的是观察尺度，计算阈值时仍使用原始计数。把这个区别说明白，能够避免读者把画图方式误认成算法对图像做过的变换。

1979 年，Nobuyuki Otsu 发表了一种根据灰度直方图自动选择阈值的方法。它把“挑一个看起来合适的界限”变成一个可以计算、比较和重复的问题：对每个候选阈值，将像素分成暗侧和亮侧，计算两组的比例与平均灰度，再评价两组分离得有多清楚。下面的图直接用本章原图画出这个评价随候选阈值的变化。把选择规则写成数学目标后，同一输入就能得到可复查的阈值。

$$
B(T)=w_0(T)w_1(T)\big[\mu_0(T)-\mu_1(T)\big]^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c15eeb9e7a3ff525fbdcd2f1.svg) | 候选灰度阈值，本图为 0–255 的灰度编码 |
| ![Formula](https://ml-biomat.com/static/agent-math/fb2227ed627c5314ec2dc3cc.svg) | 阈值 T 的类间方差，灰度单位的平方 |
| ![Formula](https://ml-biomat.com/static/agent-math/abf19469b88ec6828af62099.svg) | 暗侧（≤T）与亮侧（>T）像素占总像素的比例，无量纲，两者和为 1 |
| ![Formula](https://ml-biomat.com/static/agent-math/f937e16c6768b39074edb1b7.svg) | 两类像素各自的平均灰度，灰度单位 |

先把两类平均灰度相减，再平方，使明暗差异转成非负的分离量；乘两类比例，兼顾分离程度与每类实际包含的像素。Otsu 选择 B 最大的候选阈值；空类不参与比较。一个教学算例中，暗侧占 0.9、平均灰度 60，亮侧占 0.1、平均灰度 180，B=0.9×0.1×(60−180)²=1296 灰度²。这组数用于解释公式，图中的曲线使用真实图像的直方图逐个阈值计算。

![用真实图像重现 Otsu（1979）的选择规则：灰度直方图、类间方差和类别比例共同解释阈值 122。像素计数用对数显示，算法使用原始计数。](https://ml-biomat.com/static/tutorials/python-scientific/figures/64b8e4fddb1b658f32365dff.svg?v=64b8e4fddb1b)

图 2用真实图像重现 Otsu（1979）的选择规则：灰度直方图、类间方差和类别比例共同解释阈值 122。像素计数用对数显示，算法使用原始计数。

本例的评价曲线在阈值 122 处达到最大，`filters.threshold_otsu(image)` 给出同样的结果。代码还独立地从直方图累计像素比例和灰度总和，再计算整条评价曲线，用于检查库函数结果与公式是否一致。两组平均灰度越远，分离项越大；两组比例的乘积又会压低把极少数异常亮点单独切出的方案。这个目标依赖灰度统计，并没有读懂细胞的生物学身份，所以接下来仍要把得到的边界叠加回原图，确认它选中了本章要测的区域。

## 哪些像素属于同一个对象，孔洞又该怎样处理

阈值掩膜可能同时包含细胞、小亮点和离散噪声。要测一个对象，必须进一步说明怎样判断像素彼此相连。四邻域只把上下左右相邻的像素连接起来，八邻域还允许通过对角线连接。示例使用 `measure.label(..., connectivity=2)`，在二维图像中对应八邻域，并给每个连通区域一个整数标签。标签 0 留给背景，其他标签分别对应不同区域。`np.bincount` 数出各标签出现多少次，再选择像素最多的非背景区域。这里选择最大区域，是因为当前图像与任务聚焦于一个占主导的明亮细胞；当画面包含许多细胞时，应保留各个标签并建立逐对象表。

填充孔洞是另一项有实际含义的选择。某个被选中区域内部可能存在灰度低于阈值的小岛。保留这些小岛时，测到的是满足阈值的区域面积；把被外边界包围的小岛填满时，测到的更接近这条外边界围成的面积。示例用 `ndimage.binary_fill_holes` 实现后一种定义。它填的是与外部背景不连通的内部空区，不会把所有凹陷都抹平。在阈值 122 下，两种定义得到相同像素数；阈值升到 140 时，填孔增加 8 个像素。交互中的开关让这项选择直接对应到轮廓和面积。

这些操作的顺序也属于测量定义。程序先阈值分割，再给连通区域编号，选择最大的区域，最后按选项填孔。若先大范围平滑图像，或先把分散区域连接起来，结果可能发生变化，因为输入给标签算法的真假地图已经不同。初学时把步骤保持少而明确，有助于看清每一步的作用。遇到照明不均、对象相互接触等新问题时，再引入背景校正、局部阈值或分水岭，并用对应图像检查它们解决了哪个具体问题。

## 从像素计数走到面积与等效直径

有了掩膜，面积计算可以从铺地砖的想象出发。每个像素在样品平面中对应一个小方格，边长由空间标定给出；数清选中多少个方格，再乘以一个方格的面积，就得到整个区域的面积。数字 0.107 μm 表示每个像素边长对应的实际距离，并不是一个像素的面积。长度乘以长度之后，单位变成 μm²，这也说明为什么缩放系数需要平方。只乘一次尺度会得到错误的单位和数值，即使程序完全能够运行。

$$
A=N s^2
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 选中投影区域的面积，μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/256531b7f0ddb14dd11a59a3.svg) | 掩膜中为真的像素个数，无量纲计数 |
| ![Formula](https://ml-biomat.com/static/agent-math/b8208c8407bd0942fcaa88f9.svg) | 正方形像素边长对应的实际距离，μm/像素 |

每个像素占据边长为 s 的小方格，面积为 s²；N 个选中方格的面积相加得到 A。平方表示一个数乘以自身。本例 s=0.107 μm，N=11746，因此 A=11746×0.107×0.107=134.479954 μm²。公式采用两个方向间隔相同的像素；若两个方向标定不同，应分别相乘。

图像中的区域并不完全是圆，但我们可以问：如果一个圆具有相同面积，它的直径是多少？这个问题定义了等效圆直径。它把面积变成更容易与细胞直观大小联系的长度，同时保留“等面积”的明确含义。细长区域与圆形区域可能拥有相同的等效直径，因此研究形状时还需要长短轴、周长或方向等指标。本章先把面积与等效直径讲清，再把形状测量作为后续可扩展的对象属性。

$$
d_{\mathrm{eq}}=2\sqrt{\frac{A}{\pi}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/636f64febcd4b6a8b2831455.svg) | 与区域等面积的圆的直径，μm；eq 表示等效 |
| ![Formula](https://ml-biomat.com/static/agent-math/3207697e43e4f88223ad85c1.svg) | 选中区域面积，μm² |
| ![Formula](https://ml-biomat.com/static/agent-math/8662109ab709179527b5d176.svg) | 圆周率，约 3.14159，无量纲 |

圆面积等于圆周率乘半径的平方，因此面积除以圆周率再开平方得到半径，乘 2 得到直径。根号取非负平方根。本例 A=134.479954 μm²，A/π≈42.8063 μm²，平方根约 6.54265 μm，直径约 13.0853 μm。等效圆直径描述面积尺度，并不要求对象真的是圆。

标定误差会成系统地影响这些结果。若把像素边长写大约 1%，每个方格面积就会增大约 2%，等效直径则增大约 1%。增加图像数量并不会自动消除这种统一的尺度偏差，因此空间标定值得与原图一起保存。示例还创建了一个半径 8 μm 的解析圆盘作为教学校验对象：按相同像素间隔采样后，数像素得到约 200.976 μm²，几何公式给出约 201.062 μm²，相对差异约为 −0.043%。这个圆盘是计算生成的校验对象，与真实细胞图像分开标识，用来检查单位换算与离散采样，而不是增加一个生物实验样本。

## 完整 Python 程序与能够逐项核对的输出

下面的程序从随示例提供的原图开始运行，默认不需要联网。输入读取、Otsu 阈值、连通区域、面积换算、阈值扫描和绘图都在同一份文件中。`region_mask` 返回按指定规则选出的布尔区域，`metrics` 将区域变成计数和物理量，`otsu_curve` 则把直方图变成可检查的评价曲线。把图像、掩膜和测量结果分开传递，有助于判断某个变化来自图像处理还是单位换算。

### 从原图计算区域、敏感性曲线与校验圆盘

以随包原图为输入，生成测量摘要、逐阈值表和三张科学图。完整网格用于数值计算，简化轮廓用于交互显示。

```
"""Measure the largest bright region in a public quantitative-phase cell image.

Data: skimage.data.cell, CC0, Mueller et al. (2018),
https://doi.org/10.1364/OE.26.010729 . Pixel spacing: 0.107 micrometres.
The calibrated disk is an analytic teaching object, separate from the image.
"""
from pathlib import Path
import argparse
import base64
import hashlib
import json
import math

import numpy as np
from scipy import ndimage
from skimage import io, filters, measure
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent
SPACING = 0.107
THRESHOLDS = np.arange(80, 201, 2)



def available_plot_fonts():
    """Choose installed fonts; keep a Latin fallback on every platform."""
    choices = ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]



def region_mask(image, threshold, fill):
    """Select the largest 8-connected region strictly brighter than threshold."""
    labels = measure.label(image > threshold, connectivity=2)
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    mask = labels == int(sizes.argmax()) if sizes.max() else np.zeros_like(image, bool)
    return ndimage.binary_fill_holes(mask) if fill else mask


def metrics(mask):
    pixels = int(np.count_nonzero(mask))
    area = pixels * SPACING ** 2
    return {"pixels": pixels, "area_um2": area,
            "equivalent_diameter_um": 2 * math.sqrt(area / math.pi)}


def otsu_curve(image):
    """Between-class variance for every integer uint8 threshold."""
    counts = np.bincount(image.ravel(), minlength=256)
    p = counts / counts.sum()
    weights = np.cumsum(p)
    first_moment = np.cumsum(p * np.arange(256))
    total_mean = first_moment[-1]
    score = np.zeros(256)
    valid = (weights > 0) & (weights < 1)
    score[valid] = (total_mean * weights[valid] - first_moment[valid]) ** 2 / (
        weights[valid] * (1 - weights[valid]))
    return counts, weights, score


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--language", choices=("zh", "en"), default="en")
    args = parser.parse_args()
    out = args.output; out.mkdir(parents=True, exist_ok=True)
    zh = args.language == "zh"
    text = lambda a, b: a if zh else b
    path = HERE / "data/cell.png"
    image = io.imread(path)
    assert image.shape == (660, 550) and image.dtype == np.uint8
    threshold = int(filters.threshold_otsu(image))
    mask = region_mask(image, threshold, True)
    base = metrics(mask)
    counts, weights, score = otsu_curve(image)
    assert int(score.argmax()) == threshold
    states = []
    for t in THRESHOLDS:
        for fill in (False, True):
            current = region_mask(image, int(t), fill)
            contours = measure.find_contours(current.astype(float), .5)
            # Simplification affects display geometry, never the measured area.
            outlines = [np.round(measure.approximate_polygon(c, tolerance=1.0)[:, ::-1], 1).tolist()
                        for c in contours if len(c) > 8]
            states.append({"threshold": int(t), "fill": fill, **metrics(current), "contours": outlines})
    # An independent analytic area check at known spatial sampling.
    yy, xx = np.mgrid[-15:15:SPACING, -15:15:SPACING]
    radius = 8.0
    disk = xx ** 2 + yy ** 2 <= radius ** 2
    disk_area = float(disk.sum() * SPACING ** 2)
    analytic_area = math.pi * radius ** 2
    assert abs(disk_area / analytic_area - 1) < .01
    summary = {"dataset": "skimage.data.cell", "data_license": "CC0", "shape": list(image.shape),
               "spacing_um": SPACING, "threshold_otsu": threshold, "fill_holes": True,
               "connectivity": 8, "comparison": "image > threshold", **base,
               "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
               "disk_check": {"radius_um": radius, "pixel_area_um2": disk_area,
                              "analytic_area_um2": analytic_area,
                              "relative_error": disk_area / analytic_area - 1}}
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out / "lab-data.json").write_text(json.dumps({"width": 550, "height": 660, "spacing": SPACING,
        "otsu": threshold, "states": states, "histogram": counts.tolist(),
        "image": "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()}, separators=(",", ":")), encoding="utf-8")
    np.savetxt(out / "threshold-sensitivity.csv", np.array([[s['threshold'],int(s['fill']),s['pixels'],s['area_um2'],s['equivalent_diameter_um']] for s in states]), delimiter=",", header="threshold,fill_holes,pixels,area_um2,equivalent_diameter_um", comments="")
    plt.rcParams.update({"font.family": available_plot_fonts(), "font.size": 12,
                         "axes.spines.top": False, "axes.spines.right": False, "svg.fonttype": "none",
                         "axes.labelcolor": "#172534", "text.color": "#172534", "axes.edgecolor": "#81939d",
                         "figure.facecolor": "#faf9f5", "axes.facecolor": "#faf9f5"})
    blue, orange = "#205b8c", "#ba5231"
    def save(fig, name):
        fig.savefig(out / f"{name}-{args.language}.svg", metadata={"Date": None})
        fig.savefig(out / f"{name}-{args.language}.png", dpi=150)
        plt.close(fig)
    # Spatial views share physical coordinates, including the zoomed boundary.
    fig = plt.figure(figsize=(12.4, 7.2), layout="constrained")
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.2], height_ratios=[1, .7])
    ax = fig.add_subplot(gs[:, 0]); zoom = fig.add_subplot(gs[0, 1]); profile = fig.add_subplot(gs[1, 1])
    for a in (ax, zoom):
        a.imshow(image, cmap="gray", vmin=0, vmax=255, extent=(0, 550*SPACING,660*SPACING,0))
        for c in measure.find_contours(mask.astype(float), .5):
            a.plot((c[:,1]+.5)*SPACING,(c[:,0]+.5)*SPACING,color="#ffcb66",lw=1.5)
        a.set(xlabel=text("水平位置 / μm", "Horizontal position / μm"),ylabel=text("垂直位置 / μm", "Vertical position / μm"))
    ax.set_title(text("A  原始相位图与测量边界", "A  Phase image and measured boundary"),loc="left")
    zoom.set(xlim=(34,55),ylim=(49,29));zoom.set_title(text("B  边界附近的真实灰度", "B  Original intensities near the boundary"),loc="left")
    row=370; ax.axhline((row+.5)*SPACING,color="#74d9db",ls="--",lw=1)
    profile.plot((np.arange(550)+.5)*SPACING,image[row],color=blue,lw=1.3)
    profile.axhline(threshold,color=orange,ls="--",label=f"T = {threshold}")
    profile.set(xlabel=text("水平位置 / μm", "Horizontal position / μm"),ylabel=text("灰度值", "Intensity"),ylim=(0,270))
    profile.set_title(text("C  水平剖面（第 370 行）", "C  Horizontal profile (row 370)"),loc="left");profile.legend(frameon=False)
    save(fig,"measured-cell")
    fig, axs=plt.subplots(1,2,figsize=(12.4,4.8),layout="constrained")
    for fill,color,ls in [(False,blue,"-"),(True,orange,"--")]:
        ss=[s for s in states if s['fill']==fill]
        for a,key in zip(axs,['area_um2','equivalent_diameter_um']):
            a.plot([s['threshold'] for s in ss],[s[key] for s in ss],color=color,ls=ls,lw=2,label=text("填充孔洞" if fill else "保留孔洞","Holes filled" if fill else "Holes retained"))
    for a,key in zip(axs,['area_um2','equivalent_diameter_um']):
        a.axvline(threshold,color="#7a8a94",ls=":");a.scatter([threshold],[base[key]],color=orange,zorder=3)
        a.set_xlabel(text("灰度阈值 T", "Intensity threshold T"));a.grid(axis='y',alpha=.18)
    axs[0].set_ylabel(text("投影区域面积 / μm²", "Projected region area / μm²"));axs[1].set_ylabel(text("等效圆直径 / μm", "Equivalent-circle diameter / μm"))
    axs[0].set_title(text("A  边界选择改变测量面积", "A  Boundary choice changes measured area"),loc="left")
    axs[1].set_title(text("B  相同面积换算成直径", "B  The same area expressed as a diameter"),loc="left");axs[0].legend(frameon=False)
    save(fig,"threshold-sensitivity")
    fig=plt.figure(figsize=(12.4,6.2),layout="constrained");gs=fig.add_gridspec(2,2,width_ratios=[1.25,1])
    hist=fig.add_subplot(gs[:,0]);criterion=fig.add_subplot(gs[0,1]);weight=fig.add_subplot(gs[1,1])
    hist.bar(np.arange(256),counts,width=1,color=np.where(np.arange(256)>threshold,orange,blue),rasterized=True)
    hist.axvline(threshold,color="#172534",ls="--");hist.set_yscale('log')
    hist.set(xlabel=text("灰度值", "Intensity"),ylabel=text("像素数（对数坐标）", "Pixel count (log scale)"),xlim=(0,255),ylim=(1,counts.max()*2))
    hist.set_title(text("A  按灰度把像素分成两类", "A  Split pixels into two intensity classes"),loc="left")
    criterion.plot(np.arange(256),score,color=blue);criterion.axvline(threshold,color=orange,ls="--")
    criterion.set(xlabel=text("候选阈值", "Candidate threshold"),ylabel=text("类间方差 / 灰度²", "Between-class variance / intensity²"));criterion.set_title(text("B  Otsu（1979）：比较所有分割", "B  Otsu (1979): compare all splits"),loc="left")
    weight.plot(np.arange(256),weights,color=blue,label=text("暗侧比例", "Dark-class fraction"));weight.plot(np.arange(256),1-weights,color=orange,label=text("亮侧比例", "Bright-class fraction"))
    weight.set(xlabel=text("候选阈值", "Candidate threshold"),ylabel=text("像素比例", "Pixel fraction"),ylim=(0,1));weight.legend(frameon=False,fontsize=10)
    save(fig,"otsu-separation")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
```

程序输出的 `summary.json` 保存图像形状、像素间隔、阈值、连通规则、填孔状态和最终测量。`threshold-sensitivity.csv` 保存阈值从 80 到 200、每次增加 2 时的两种填孔结果。三张主图分别回答“边界在哪里”“结果对阈值有多敏感”和“Otsu 为什么选择这个阈值”。查看这些输出时，可以先核对像素数，再手算面积，最后查看面积怎样换成直径；如果某一步不一致，就沿着对应函数回查，而不用在整份程序中盲目寻找。

交互使用的轮廓在导出时做了最多约一个像素容差的折线简化，以减少页面中的坐标数量。面积和直径始终从 660×550 的完整掩膜计算，既不来自缩略图，也不来自简化轮廓的几何面积。这种安排区分了“用于屏幕显示的形状”和“用于测量的原始网格”。开发科学可视化时经常需要同样的区分：可以为显示降低几何复杂度，但要保留计算结果所依据的分辨率和定义。

## 把参数影响画出来，判断一个结果稳不稳定

只给出一条边界和一个面积，很难判断这个数字对处理选择是否敏感。阈值扫描提供了更直接的信息：固定同一张图，每次只改变阈值，重复完整区域选择和测量。阈值 100 时，填孔后的面积约为 140.96 μm²；阈值 122 时约为 134.48 μm²；阈值 160 时约为 100.20 μm²。后一种设置已把一部分较暗内部排除，因此面积变化需要和轮廓变化一起看。曲线上的每个点都有同一套明确操作，比较才有共同基础。

![固定原图，改变阈值并比较填孔选择。面积与等效直径分别使用物理单位；竖线标记 Otsu 阈值 122。](https://ml-biomat.com/static/tutorials/python-scientific/figures/37eb47a5c859ff6646c48833.svg?v=37eb47a5c859)

图 3固定原图，改变阈值并比较填孔选择。面积与等效直径分别使用物理单位；竖线标记 Otsu 阈值 122。

交互中调整阈值时，左侧原图边界、灰度直方图上的分界线、面积敏感性曲线上的位置和测量数字会一起更新。填孔开关改变的是同一阈值下区域内部空区的处理。页面展示的是示例 Python 程序对全分辨率原图预先计算的 122 组状态，因此离线也能完整使用。当前阈值、填孔状态、像素数和物理量会同时显示；记录当前阈值和填孔状态后，就能按同样条件重现这次面积测量。

### 边界与测量实验台

调整阈值与孔洞处理，观察原图边界、灰度分布和测量面积怎样同步变化。

[Figure: 原始图像、空间坐标与选中区域边界](https://ml-biomat.com/tutorials/python-scientific/s01/#S01-image)

[Figure: 灰度直方图与当前阈值](https://ml-biomat.com/tutorials/python-scientific/s01/#S01-hist)

[Figure: 阈值面积敏感性曲线与当前状态](https://ml-biomat.com/tutorials/python-scientific/s01/#S01-curve)

可以按三个问题观察：首先，边界是否仍然围绕同一个主要对象；其次，小幅调整阈值时面积变化是否平缓；最后，某个变化较快的区间在图像上对应什么结构。这里的阈值敏感性描述同一幅图的处理选择，并不是多个细胞之间的生物差异，也不是重复实验误差。真正比较不同处理组时，应对每幅图采用同样的预先确定流程，再区分细胞、视野和独立实验批次，避免把同一视野中的许多像素当成许多独立样本。

## 把单个区域的测量扩展到自己的图像

换成自己的图像时，先把问题写成一个可测量的对象描述，例如“每个分离孔洞的投影面积”或“每个细胞核的长轴长度”。随后核对图像维度和尺度：彩色图多一个通道维度，三维堆栈多一个切片维度，层间距也可能与平面像素间隔不同。对彩色图直接调用本章的二维逻辑，或把三维体素当作等边小立方体，都会改变测量含义。确认输入结构后，再选取代表性的原图查看掩膜与边界，建立与研究对象对应的区域选择规则。

画面中有多个对象时，`measure.regionprops_table` 可以把各标签的面积、质心和形状属性汇成表格。此时保留对象编号、图像编号和实验条件，让表中的一行能重新定位到原图。接触图像边缘的对象通常只被拍到一部分，需要根据研究问题制定统一处理规则。过小区域、相互接触的对象和不均匀背景也应通过具体图像来处理，而不是为了让直方图好看就随意删除某些结果。把规则应用到所有图，再用可视化查看结果分布，才便于开展有意义的组间比较。

本章的工作链可以迁移到许多材料问题：图像数组提供位置和信号，分割规则定义对象，空间标定把网格变成物理量，参数扫描说明处理选择如何影响结果。scikit-image 提供了这些操作的通用工具，而科学问题决定工具之间怎样连接。最终值得保存的成果不止一个面积数字，还包括原图、边界、测量定义以及能够重新生成结果的程序；它们共同把肉眼观察变成可以继续追问的定量证据。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/S01.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [scikit-image tutorials: Images are arrays](https://scikit-image.org/skimage-tutorials/lectures/00_images_are_arrays.html)

   数组、图像类型、像素索引与范围的开源教学基础。

   Tutorial materials CC0, per repository README.
2. [scikit-image tutorials: Image segmentation](https://scikit-image.org/skimage-tutorials/lectures/4_segmentation.html)

   直方图、阈值和区域分割工作流；本章增加实际标定、单位推导和参数敏感性。

   Tutorial materials CC0, per repository README.
3. [scikit-image: cell image](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.cell)

   真实图像、0.107 μm 像素间隔和原始研究身份。

   Image: CC0, as documented by scikit-image.
4. [Mueller et al. (2018), Optics Express 26, 10729](https://doi.org/10.1364/OE.26.010729)

   公开细胞相位图对应的原始科学研究。

   Scientific citation; supplied image separately released under CC0.
5. [Otsu (1979), A Threshold Selection Method from Gray-Level Histograms](https://doi.org/10.1109/TSMC.1979.4310076)

   类间方差阈值选择的原始方法。
6. [scikit-image: Measure region properties](https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_regionprops.html)

   多对象属性与表格扩展的官方示例。
