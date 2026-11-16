# FiberNet

Source: https://ml-biomat.com/fibernet/
Language: zh-CN

4.2.0 · Python 3.9+ · MIT

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

## 安装 4.2.0

核心安装包含 NumPy、SciPy、NetworkX 和 Matplotlib。按工作流添加机器学习、三维显示或几何导出依赖。

```bash
python -m pip install "fibernet==4.2.0"
```

可选依赖

```bash
python -m pip install "fibernet[ml]==4.2.0"  # 机器学习
python -m pip install "fibernet[viz]==4.2.0"  # 三维显示
python -m pip install "fibernet[manufacturing]==4.2.0"  # 几何与实体导出
```

ml 对应机器学习工具；viz 对应 PyVista 三维显示；manufacturing 对应实体几何与导出工具。Taichi 后端可另装 accel 扩展。

## 生成并查看结构

```python
import fibernet as fn

# 坐标和半径：米
graph = fn.pattern_2d(
    unit="honeycomb", box=(0.01, 0.01), grid=(2, 2),
    radius=0.00005, seed=23,
)
fn.show(graph)
```

示例采用 SI 单位：坐标与半径为米，弹性模量为 Pa。

## 小变形计算与保存

沿用上面的 graph，以梁框架 FEM 进行线性求解，保存结构与结果。

```python
# 弹性模量：Pa；strain 为目标伸长比
result = fn.simulate(
    graph, backend="fem", mode="stretch", strain=1.01,
    nonlinear=False, E=1e9, nu=0.3,
)
print(result.max_displacement)

graph.save_json("network.json")
result.save("fem_result.json")
```

4.2.0 接口中的 strain 表示目标伸长比；1.01 对应 1% 伸长。nonlinear=False 选择线性求解，max_displacement 的单位为米。

## 继续使用

## 结构分析与学习

SnapshotFeatureExtractor 用于平面结构快照分析；analyze_tensile_recruitment 分析已给定的边应变轨迹。物理标签生成、回归建模和目标曲线搜索分别有独立示例。

[快照分析示例](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/examples/snapshot_features_workflow.py)[物理学习示例](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/examples/physical_learning_workflow.py)[目标曲线搜索](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/examples/curve_inverse_workflow.py)

## 几何路径与导出

制造几何接口用于构建平面或曲面上的连续路径，并支持自定义基元。实体与路径文件导出接入相应可选依赖；坐标单位和路径顺序随输入一起管理。

[路径生成示例](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/examples/manufacturing_workflow.py)[实体导出示例](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/examples/solid_export_workflow.py)

## 结构与计算图例

二维结构图集

![12 种二维结构 · v3 图集。](https://ml-biomat.com/static/images/fibernet/01_2d_gallery.webp?v=fce8466dc2ec)

12 种二维结构 · v3 图集。 [源图](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/docs/images/01_2d_gallery.png)

力学计算图例

![蜂窝网络的 8 个保存帧；颜色表示边的伸长比。](https://ml-biomat.com/static/images/fibernet/05_trajectory_dark.webp?v=49bfe332bfbb)

蜂窝网络的 8 个保存帧；颜色表示边的伸长比。 [源图](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/docs/images/05_trajectory_dark.png)

![梁框架 FEM 示例；颜色表示 sigma_total（轴向应力绝对值与弯曲应力之和）。](https://ml-biomat.com/static/images/fibernet/fem_showcase_dark.webp?v=9528bb432d96)

梁框架 FEM 示例；颜色表示 sigma_total（轴向应力绝对值与弯曲应力之和）。 [源图](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/docs/images/fem_showcase_dark.png)

![Voronoi 网络计算示例 · 目标伸长比 1.5。](https://ml-biomat.com/static/images/fibernet/voronoi_1.5x_auto.webp?v=e8a06dbbbab0)

Voronoi 网络计算示例 · 目标伸长比 1.5。 [源图](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/docs/images/voronoi_1.5x_auto.png)

学习与搜索图例

![分类示例：混淆矩阵、ROC、特征重要性与学习曲线。](https://ml-biomat.com/static/images/fibernet/09_ml_analysis_dark.webp?v=1d577a2906f4)

分类示例：混淆矩阵、ROC、特征重要性与学习曲线。 [源图](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/docs/images/09_ml_analysis_dark.png)

![CEM 搜索示例：每轮目标值与当前最优值。](https://ml-biomat.com/static/images/fibernet/11_rl_reward_dark.webp?v=6f458966f86e)

CEM 搜索示例：每轮目标值与当前最优值。 [源图](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/docs/images/11_rl_reward_dark.png)

## 文档与示例

[PyPI 4.2.0](https://pypi.org/project/fibernet/4.2.0/)[4.2.0 发行说明](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/docs/RELEASE_4_2_0.md)[快速开始](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/docs/quickstart.rst)[梁 FEM 模型与单位](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/docs/METHODS_BEAM_FEM_CONTRACT.md)[示例目录](https://github.com/GellmanSparrowS/fibernet/tree/v4.2.0/examples)[完整 Notebook 教程](https://github.com/GellmanSparrowS/fibernet/blob/v4.2.0/tutorials/complete_tutorial_v4.ipynb)
