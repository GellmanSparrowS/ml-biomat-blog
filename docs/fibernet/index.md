# FiberNet

Source: https://ml-biomat.com/fibernet/
Language: zh-CN

4.41.0 · Python 3.9+ · MIT

纤维网络结构生成、分析与力学建模

用 Python 连接结构生成、网络分析与力学计算，并通过 FiberScope 桌面界面查看、配置和导出网络。

## Python 工具库

FiberNet 以节点和连边组织结构数据，将结构生成、分析、模拟和导出连接到可复用的 Python 工作流。

- 二维与三维结构生成，节点、连边及纤维半径管理。
- 平面结构快照、孔隙分布与给定轨迹上的拉伸招募分析。
- 梁框架 FEM，以及按需安装的其他计算后端。
- 原生图与结果保存，配合示例开展后续分析。

## FiberScope 桌面界面

FiberScope 3.1.0 支持几何配置、结构查看、轨迹回放与导出。Windows 下载包自带运行环境。

## 纤维网络动态演示

![结构变形](https://ml-biomat.com/static/images/fibernet/homepage/network-morph.webp)

结构变形

![编织网络的拉伸断裂](https://ml-biomat.com/static/images/fibernet/homepage/woven-fracture.webp)

编织网络的拉伸断裂

![从取向场到三维纤维束](https://ml-biomat.com/static/images/fibernet/homepage/orientation-to-bundle.webp)

从取向场到三维纤维束

![从叶脉到图神经网络](https://ml-biomat.com/static/images/fibernet/homepage/leaf-venation-gnn.webp)

从叶脉到图神经网络

![三维纤维网络中的流动](https://ml-biomat.com/static/images/fibernet/homepage/porous-fiber-flow.webp)

三维纤维网络中的流动

![压缩接触改变电流路径](https://ml-biomat.com/static/images/fibernet/homepage/woven-contact-current.webp)

压缩接触改变电流路径

![用强化学习选择桥梁支撑位置](https://ml-biomat.com/static/images/fibernet/homepage/reinforcement-bridge.webp)

用强化学习选择桥梁支撑位置

![扭转中依次承载的螺旋路径](https://ml-biomat.com/static/images/fibernet/homepage/helical-recruitment.webp)

扭转中依次承载的螺旋路径

![断电后纤维网络的冷却](https://ml-biomat.com/static/images/fibernet/homepage/electrothermal-switch.webp)

断电后纤维网络的冷却

## 安装 FiberNet

在终端运行以下命令。基础安装包含 NumPy、SciPy、NetworkX 和 Matplotlib，可直接运行下面的蜂窝网络示例。

```bash
python -m pip install "fibernet==4.41.0"
```

可选依赖

```bash
python -m pip install "fibernet[ml]==4.41.0"  # 机器学习
python -m pip install "fibernet[viz]==4.41.0"  # 三维显示
python -m pip install "fibernet[manufacturing]==4.41.0"  # 几何与实体导出
```

三维显示使用 PyVista。使用 Taichi 后端时，安装 `accel` 扩展。

## 示例：蜂窝网络拉伸

这段 Python 代码生成并显示二维蜂窝网络，计算拉伸后的最大位移（米），再将网络和计算结果分别保存为 JSON 文件。

```python
import fibernet as fn

# 生成二维蜂窝网络，长度单位为米
graph = fn.pattern_2d(
    unit="honeycomb", box=(0.01, 0.01), grid=(2, 2),
    radius=0.00005, seed=23,
)
fn.show(graph)

# 用线性梁模型计算 1% 拉伸，弹性模量单位为 Pa
result = fn.simulate(
    graph, backend="fem", mode="stretch", stretch_ratio=1.01,
    nonlinear=False, E=1e9, nu=0.3,
)
print(result.max_displacement)

graph.save_json("network.json")
result.save("fem_result.json")
```

运行结果：18 个节点、22 条边，最大位移为 0.20 mm（终端输出单位为米）。

## 更多工作流

### 结构分析与学习

从平面结构快照提取特征，或从边应变轨迹分析纤维何时参与承载。示例还涵盖物理标签生成、回归与目标曲线搜索。

[快照分析示例](https://github.com/GellmanSparrowS/fibernet/blob/main/examples/snapshot_features_workflow.py)[物理学习示例](https://github.com/GellmanSparrowS/fibernet/blob/main/examples/physical_learning_workflow.py)[目标曲线搜索](https://github.com/GellmanSparrowS/fibernet/blob/main/examples/curve_inverse_workflow.py)

### 几何路径与导出

用自定义基元在平面或曲面上生成连续路径，再导出路径或实体几何。

[路径生成示例](https://github.com/GellmanSparrowS/fibernet/blob/main/examples/manufacturing_workflow.py)[实体导出示例](https://github.com/GellmanSparrowS/fibernet/blob/main/examples/solid_export_workflow.py)

## 文档与教程

[PyPI 4.41.0](https://pypi.org/project/fibernet/4.41.0/)[4.41.0 发行说明](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/RELEASE_4_41_0.md)[快速开始](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/quickstart.rst)[梁 FEM 模型与单位](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/METHODS_BEAM_FEM_CONTRACT.md)[示例目录](https://github.com/GellmanSparrowS/fibernet/tree/main/examples)[完整 Notebook 教程](https://github.com/GellmanSparrowS/fibernet/blob/main/tutorials/complete_tutorial_v4.ipynb)

结构与计算图集（6 张）

![12 种二维结构 · v3 图集。](https://ml-biomat.com/static/images/fibernet/01_2d_gallery.webp?v=fce8466dc2ec)

12 种二维结构 · v3 图集。 [源图](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/images/01_2d_gallery.png)

![蜂窝网络的 8 个保存帧；颜色表示边的伸长比。](https://ml-biomat.com/static/images/fibernet/05_trajectory_dark.webp?v=49bfe332bfbb)

蜂窝网络的 8 个保存帧；颜色表示边的伸长比。 [源图](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/images/05_trajectory_dark.png)

![梁框架 FEM 示例；颜色表示 sigma_total（轴向应力绝对值与弯曲应力之和）。](https://ml-biomat.com/static/images/fibernet/fem_showcase_dark.webp?v=9528bb432d96)

梁框架 FEM 示例；颜色表示 sigma_total（轴向应力绝对值与弯曲应力之和）。 [源图](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/images/fem_showcase_dark.png)

![Voronoi 网络计算示例 · 目标伸长比 1.5。](https://ml-biomat.com/static/images/fibernet/voronoi_1.5x_auto.webp?v=e8a06dbbbab0)

Voronoi 网络计算示例 · 目标伸长比 1.5。 [源图](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/images/voronoi_1.5x_auto.png)

![分类示例：混淆矩阵、ROC、特征重要性与学习曲线。](https://ml-biomat.com/static/images/fibernet/09_ml_analysis_dark.webp?v=1d577a2906f4)

分类示例：混淆矩阵、ROC、特征重要性与学习曲线。 [源图](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/images/09_ml_analysis_dark.png)

![CEM 搜索示例：每轮目标值与当前最优值。](https://ml-biomat.com/static/images/fibernet/11_rl_reward_dark.webp?v=6f458966f86e)

CEM 搜索示例：每轮目标值与当前最优值。 [源图](https://github.com/GellmanSparrowS/fibernet/blob/main/docs/images/11_rl_reward_dark.png)

[素材许可](https://ml-biomat.com/static/images/fibernet/homepage/credits.html)
