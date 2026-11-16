# 组织有名字的多维实验数据

Source: https://ml-biomat.com/tutorials/python-scientific/s03/
Language: zh-CN

用温度场理解坐标对齐、缺失覆盖与HDF5分块，让每个数值保留它的物理位置和单位。

## 四个轴都有名字，分析才知道沿哪里进行

一台相机记录一张温度图时，每个像素都有横纵位置；连续拍摄以后，还多出时间；比较两种材料时，又增加材料条件。这样的数据很快就超过二维表格的直觉。一个形状为(2,61,60,80)的数组究竟表示什么，单看数字无法确定：哪个轴是时间，哪两个是空间，两个条件又是什么？xarray把这些问题写进数据对象，通过维度名、坐标和属性，把数组的数值与科学含义放在一起。

本章建立两种热扩散率条件下的二维温度场。每个条件有61个时刻，每个时刻包含60×80个空间单元，单元间距为0.2 mm。数据由无限平面上的高斯热扩散解析模型生成，初始温度峰值为100 °C，背景为20 °C；它是一组有明确规律的教学场。我们还人为设置一块从20 s开始缺失的矩形区域，用来观察有效数据范围怎样改变平均值。完整场与缺失场同时保存，读者可以直接检查变化来自物理过程还是采样范围。

xarray负责按科学含义选择与计算，h5py负责把多维数组、坐标和单位存入HDF5，并按需要读取其中一部分。两者连接起来，可以形成一个长期可读的数据文件，而不是一堆依靠文件名和个人记忆解释的数组。本章最终会生成两种存储布局的HDF5文件，比较空间快照和单点时间序列分别触及多少数据块，并在交互里同步查看温度图、剖面、时间曲线和存储请求。

## 先给温度场一个可以解释的变化规律

想象在一张足够大的均匀薄片上短暂加热一个区域，随后停止加热。热从较热处传向较冷处，局部温度峰值下降，受影响的范围变宽。我们的模型把初始温升画成一座平滑的椭圆山包，中心位于(1.1,−0.5) mm，两个方向的初始宽度分别为1.8和1.2 mm。热扩散率α描述温度变化在材料中扩散的快慢，这里比较0.2和0.5 mm²/s两个条件，其他初始设置相同。

$$
\begin{aligned}w_x^2(t)&=\sigma_x^2+2\alpha t,\qquad w_y^2(t)=\sigma_y^2+2\alpha t\\T(x,y,t)&=T_b+\Delta T_0\frac{\sigma_x\sigma_y}{w_x(t)w_y(t)}\exp\left[-\frac12\left(\frac{(x-x_0)^2}{w_x^2(t)}+\frac{(y-y_0)^2}{w_y^2(t)}\right)\right]\end{aligned}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8f5e8856b86122b7ce047547.svg) | 位置(x,y)、时刻t的温度，K |
| ![Formula](https://ml-biomat.com/static/agent-math/78b803e9ef905a830a512636.svg) | 空间坐标与热点中心坐标，mm；中心为(1.1,−0.5) mm |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | 时间，s，本例0到60 s |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | 热扩散率，mm²/s，本例0.2或0.5 |
| ![Formula](https://ml-biomat.com/static/agent-math/92a2a2de680d59d4186c0571.svg) | 初始高斯宽度，mm，本例1.8和1.2 |
| ![Formula](https://ml-biomat.com/static/agent-math/ccddec3bddcb880f73f5bca6.svg) | 扩散后的两个方向宽度，mm |
| ![Formula](https://ml-biomat.com/static/agent-math/268897e0a26bd3db213c08b9.svg) | 背景温度293.15 K，即20 °C |
| ![Formula](https://ml-biomat.com/static/agent-math/4df209ad4efd080121d47c05.svg) | 初始中心温升80 K |
| ![Formula](https://ml-biomat.com/static/agent-math/64460da0d752153c52e1bd62.svg) | 自然指数函数；指数中的坐标差平方除以宽度平方为无量纲 |

这是均匀无限平面上高斯初始温升的扩散解。扩散使宽度平方增加2αt，前面的宽度比同时降低峰值，保持整张无限平面上的温升面积积分。t=0且位于热点中心时，两宽度等于初值、指数为0，温度为293.15+80=373.15 K，即100 °C。α=0.2 mm²/s、t=20 s时，宽度平方分别为3.24+8=11.24 mm²和1.44+8=9.44 mm²，对应宽度约3.3526和3.0725 mm。

公式中的宽度平方随时间线性增加，因此宽度本身不是匀速增加；峰值前面的比例则随两个宽度增大而减小。它把“越扩越宽”和“峰值降低”联系在一起。两个扩散率在初始时刻给出相同温度场，随后较大的扩散率使温升更快铺开。这里截取横向−8到8 mm、纵向−6到6 mm的观察窗口，窗口外仍然存在同一无限平面的温度场，并没有在窗口边缘额外施加保温条件。

![两个扩散率、三个时刻的同一高斯扩散模型，使用统一温标；窗口截取无限平面的一部分。](https://ml-biomat.com/static/tutorials/python-scientific/figures/3c34a333130bba767a0f8456.svg?v=3c34a333130b)

图 1两个扩散率、三个时刻的同一高斯扩散模型，使用统一温标；窗口截取无限平面的一部分。

六幅图共享20到100 °C色标，因而同一种颜色始终对应同一温度。后期图变暗，表示温升确实减小；同时它在空间上变得更宽。若每一幅图都把自己的最低与最高值自动拉到色标两端，较弱的温升也会重新显示成亮黄色，就容易把“扩散得更宽”与“仍然一样热”混在一起。后面的剖面曲线保留纵轴数值，帮助读取那些在共同色标下较暗的细节。

程序用K存温度，用°C展示温度图。两种刻度之间的换算需要真正修改数值，而不是只改标签。相比之下，温差1 K与温差1 °C具有相同大小，所以描述温升和误差时使用K很方便。数组属性里的`units`记录了单位含义，但普通xarray运算不会仅凭这个字符串自动完成单位换算；换算应当像下面这样明确写出，并相应更新结果属性。

$$
T_{\degree\mathrm C}=T_{\mathrm K}-273.15
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d0fd16bf369d52ab9d375978.svg) | 温度按摄氏度表示时的数值 |
| ![Formula](https://ml-biomat.com/static/agent-math/6d443f0ab15429bfcc4eb1d9.svg) | 同一温度按开尔文表示时的数值 |
| ![Formula](https://ml-biomat.com/static/agent-math/41eb4d81094d336d45d3ea35.svg) | 两种温标零点的固定数值差 |

这里换算的是同一物理温度在两种刻度下的数值。293.15 K对应293.15−273.15=20 °C，373.15 K对应100 °C。两个温度相减时固定偏移抵消，所以80 K温差与80 °C温差大小相同。保存数组属性时单位要跟随数值的换算更新。

## 维度、坐标、属性分别解决哪一个问题

一个`DataArray`可以理解为“数值数组加上坐标说明”。本例维度顺序为`diffusivity, time, y, x`，分别对应2、61、60、80个位置。维度名告诉程序某一个轴是什么；坐标告诉程序这个轴上的每个位置对应哪个物理值；属性则保存单位和模型含义。比如`time`的坐标从0到60，单位为s；`x`的80个坐标是单元中心，从−7.9到7.9 mm，并不是数组编号0到79本身。

`isel`按位置选择，`sel`按坐标选择。`isel(time=20)`拿第21个时间位置，`sel(time=20)`拿坐标值为20 s的时刻；这份每秒采样的数据里，两者恰好一致。若以后时间坐标改为每5 s一个点，同样的索引20就对应100 s，二者的含义便明显不同。空间选择也一样：要求x=1.1 mm是在找物理位置，不是在取第1.1个元素。

把完整温度场和缺失视图放进同一个`Dataset`，可以让两项变量共享维度与坐标。它类似把几张有关联的科学表放进同一个容器，但每个变量仍然可以有自己的维度组合。例如全场温度保留四个轴，空间平均温度只保留扩散率和时间两个轴。调用`mean(['y','x'])`时，程序根据名称消去空间方向；即使以后为了存储或绘图调换轴顺序，这一写法仍然描述同一个计算。

这种按名字计算的方式，也让代码更接近研究问题。读取某种材料在20 s的温度图，可以写成`temperature.sel(diffusivity=0.2, time=20)`；比较两种扩散率则分别选出相同时间与空间坐标上的数据。数组形状、坐标单位和变量名都保留在结果里，读者能继续检查自己取到的是一张空间快照、一条剖面，还是一个位置随时间的记录。

## 坐标对齐与缺失值，会直接改变科学结论

把同一张图的x顺序反转以后，数值仍然属于原来的物理位置，只是存储顺序改变了。用两个NumPy数组直接相减，会把左边第一个元素减去右边第一个元素，实际上比较了不同位置；由于热点偏离窗口中心，差值最大可达到约52.5282 K。xarray则根据x坐标对齐后再相减，同一物理位置的温度与自己相减，结果处处为零。这个对照说明，数组位置相同与物理坐标相同是两件不同的事。

自动对齐依赖坐标的准确性。如果两组坐标采用不同单位却都叫x，或者一组测的是单元中心、另一组测的是边界，名字相同仍然不能保证物理位置一致。需要先统一单位与坐标定义，再决定按共同标签相减还是插值到共同网格。对仅有部分坐标重合的数组，还应检查运算后保留了哪些位置，避免把范围缩小误读成数据自然变少。这里反转的是同一组坐标，因此能用零差值明确检验对齐行为。

![完整与缺失区域、空间均值、坐标反转后的相减共同展示采样与标签的影响。缺失区域从20 s起生效，完整解析场保持连续。](https://ml-biomat.com/static/tutorials/python-scientific/figures/74b9d8032f46df8ffb73eec4.svg?v=74b9d8032f46)

图 2完整与缺失区域、空间均值、坐标反转后的相减共同展示采样与标签的影响。缺失区域从20 s起生效，完整解析场保持连续。

缺失区域带来另一类变化。我们把x从0到3 mm、y从−2到1 mm的225个单元，在20 s及以后的缺失视图中设为`NaN`。完整温度场没有改变，缺失视图也没有把该区域当成零温度。对浮点数组使用`mean(..., skipna=True)`会跳过这些值，并按剩余4575个单元计算平均。相同时间的完整场有4800个单元，两种均值因此对应不同的空间范围。

$$
\overline T_{\rm valid}=\frac{1}{N_{\rm valid}}\sum_{(i,j)\in\mathcal V}T_{ij},\qquad f_{\rm valid}=\frac{N_{\rm valid}}{N_{\rm all}}
$$

| 符号 | 含义与单位 |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6fa439d6e71a5c78c00edf6c.svg) | 有效单元的平均温度，K |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | 空间单元的行列编号，无量纲 |
| ![Formula](https://ml-biomat.com/static/agent-math/09a167b42cf9b0ee95226228.svg) | 具有有效数值的空间单元集合 |
| ![Formula](https://ml-biomat.com/static/agent-math/da5f776e1e01a0f2e5cb8938.svg) | 指定扩散率与时刻下单元(i,j)温度，K |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | 对有效集合中的温度逐项相加 |
| ![Formula](https://ml-biomat.com/static/agent-math/03a8f63d99ba4d42f78d37e1.svg) | 有效与全部单元数，无量纲计数 |
| ![Formula](https://ml-biomat.com/static/agent-math/448cb411f8cabff5424d5145.svg) | 有效覆盖比例，无量纲 |

本例单元面积相同，因此空间平均可按有效单元等权计算。20 s以后缺失225个单元，有效数为4800−225=4575，覆盖4575/4800=0.953125，即95.3125%。α=0.2、t=20 s时，有效均值297.870916 K对应24.720916 °C；完整4800单元均值298.376697 K对应25.226697 °C。非均匀网格的面积平均需要按单元面积加权。

α=0.2 mm²/s、t=20 s时，完整场空间均温约为25.226697 °C，有效单元均温约为24.720916 °C。差别约0.506 °C，因为构造的缺失区域覆盖了较热的中心部分。图中虚线在20 s处的跳变来自可用区域变化，完整场的温度仍然平滑变化。报告空间平均时把有效单元数或覆盖率一起保存，就能把这种采样变化与材料本身的变化区分开。

## 把坐标与数值一起存下来，而不依赖记忆

科学数据在不同计算机之间交换，早就遇到过“读到了字节，却不知道它们代表什么”的问题。HDF最初面向多种计算平台上的科学数据共享，1988年发布，HDF5于1998年首次发布；它把多维数组与描述它们的结构放进同一个文件。Hoyer和Hamman在2017年介绍的xarray，则把有名字的多维数组带入Python分析流程。这两条线索在本例中相遇：文件保存可解释的数据结构，分析程序继续沿用这些名称和坐标。

HDF5里的`Group`类似目录，`Dataset`保存数组，`attrs`保存附加说明。这里创建`/coordinates`与`/fields`两个组，分别存坐标与温度变量。温度数据集不仅有形状(2,61,60,80)，还把每个轴的标签设成维度名，并通过dimension scale关联相应坐标数组。这样读者能够从文件本身找到“第2个轴叫time，坐标是什么，单位是什么”。

![实际HDF5布局中的坐标关联与两种块形状。黑点为x索引45、y索引27；下方比较一个快照与单点61时刻请求触及的块数。](https://ml-biomat.com/static/tutorials/python-scientific/figures/ce9049a9c4ce687b1825ec86.svg?v=ce9049a9c4ce)

图 3实际HDF5布局中的坐标关联与两种块形状。黑点为x索引45、y索引27；下方比较一个快照与单点61时刻请求触及的块数。

h5py对HDF5提供接近数组切片的读取方式，但一个普通HDF5文件并不天然具有某一种上层软件约定。完整例子因此明确写出读取函数：从坐标组读取坐标，从各轴标签恢复维度顺序，从属性恢复单位，再创建xarray对象。已有NetCDF等带约定的数据可通过相应后端直接读取；使用自己定义的HDF5布局时，保持读写规则一致，可以让字段含义清楚地跨越存储边界。

写完文件后，程序重新读回两种温度变量，检查数值和缺失位置与原对象一致，并核对每个轴都关联了一个坐标尺度。它还直接从HDF5读取一张快照与一个点的时间序列，和内存里的相同切片比较。这样既检查整份文件，也检查实际研究中经常请求的两类数据。单位字符串、维度标签和坐标数组与数值一样，都是后续分析需要保存的内容。

## 存储块怎样影响“我只想看这一小部分”

压缩数据通常按块存储。请求一个数组切片时，文件系统与HDF5需要访问和解码与该切片相交的块，再取出其中需要的值。因此块形状应当考虑常见的读取方式。本例用同样数据创建两份文件：`snapshot.h5`的块形状为(1,1,20,20)，`time_series.h5`为(1,10,10,10)，数字依次对应扩散率、时间、y、x方向。它们使用相同gzip压缩与shuffle设置，改变的是数据在块中的组织。

读取一个扩散率、一个时刻的完整60×80快照时，第一种布局沿y需要3块、沿x需要4块，共12块；第二种布局沿y需要6块、沿x需要8块，共48块。读取一个空间点的61个时刻时，第一种布局每个时间块只含一个时刻，需要61块；第二种每块容纳10个时刻，需要7块。图中的橙色块标出所选点落在哪里，块计数把“适合哪种读取”变成可以手工复核的问题。

这些计数描述请求触及的逻辑块数，实际耗时还取决于每块字节数、压缩后大小、缓存命中和存储设备。两个文件的总大小也由实际压缩结果决定，不能只凭块数推断哪一个必然更快。选择布局时，可以先列出最常见的快照、剖面或时间窗口请求，计算它们跨过多少块，再对有代表性的真实数据计时。本例保留两份文件，方便读者按自己的读取比例继续实验。

空间维度变大后，切片本身还能避免一次把整份文件读入内存。`dataset[0,20,:,:]`只请求一张快照，而`dataset[:]`读出整个数组。这里完整数据量适中，读回函数一次恢复全部变量以便教学检查；处理更大项目时，可以保留文件句柄按需读取，或采用支持延迟计算的上层数组。无论选择哪种方式，坐标和单位都应跟随每个切片，而不是因为只读了一小部分就丢失。

## 完整例子与同步的数据探索

下面的程序生成解析场，建立有名字的数组，设置明确的缺失区域，写入两份HDF5文件并读回验证。`spatial-means.csv`把完整场的空间平均导出为表格，保留扩散率和时间两列坐标；`summary.json`记录对齐、覆盖率和块请求的结果。图形与页面交互均来自这些计算，温度场的生成规则和每一个保存步骤都包含在同一份代码里。

### 生成并读取两份HDF5文件

使用zh生成中文图。

```
python main.py --output results --language en
```

### 有坐标的温度场、HDF5读写与分块比较

温度模型、缺失规则、命名数组、两种存储布局和完整读取函数均包含在此。

```
"""Labeled analytic diffusion fields, missing regions, and HDF5 chunk layouts."""
from pathlib import Path
import argparse
import base64
import json
import numpy as np
import xarray as xr
import h5py
from scipy.special import erf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle

BASE=293.15  # K
AMPLITUDE=80.0  # K
SX0,SY0=1.8,1.2  # mm
X0,Y0=1.1,-.5  # mm
DIMS=('diffusivity','time','y','x')
LAYOUTS={'snapshot':(1,1,20,20),'time_series':(1,10,10,10)}



def available_plot_fonts():
    """Choose installed fonts; keep a Latin fallback on every platform."""
    choices = ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]



def make_dataset():
    coords={'diffusivity':[.2,.5],'time':np.arange(61,dtype=float),
            'y':-5.9+.2*np.arange(60),'x':-7.9+.2*np.arange(80)}
    alpha,time,y,x=np.meshgrid(*(coords[d] for d in DIMS),indexing='ij')
    sx2=SX0**2+2*alpha*time;sy2=SY0**2+2*alpha*time
    values=BASE+AMPLITUDE*SX0*SY0/np.sqrt(sx2*sy2)*np.exp(-.5*((x-X0)**2/sx2+(y-Y0)**2/sy2))
    field=xr.DataArray(values,dims=DIMS,coords=coords,name='temperature',
                       attrs={'units':'K','model':'analytic Gaussian diffusion on an infinite plane'})
    for name,unit in [('diffusivity','mm^2/s'),('time','s'),('y','mm'),('x','mm')]:field.coords[name].attrs['units']=unit
    mask=(field.time>=20)&(field.x>=0)&(field.x<3)&(field.y>=-2)&(field.y<1)
    dataset=xr.Dataset({'temperature':field,'sensor_view':field.where(~mask)},
                        attrs={'data_identity':'analytic teaching fields; sensor_view includes a constructed missing rectangle',
                               'baseline_K':BASE,'initial_amplitude_K':AMPLITUDE,'center_x_mm':X0,'center_y_mm':Y0})
    return dataset


def save_hdf(dataset,path,chunks):
    with h5py.File(path,'w') as f:
        for key,value in dataset.attrs.items():f.attrs[key]=value
        coordinates=f.create_group('coordinates');fields=f.create_group('fields')
        for dim in DIMS:
            scale=coordinates.create_dataset(dim,data=dataset.coords[dim].values)
            scale.make_scale(dim);scale.attrs['units']=dataset.coords[dim].attrs['units']
        for name in dataset.data_vars:
            array=fields.create_dataset(name,data=dataset[name].values,chunks=chunks,
                                         compression='gzip',compression_opts=4,shuffle=True)
            array.attrs['units']='K';array.attrs['dimension_order']=json.dumps(DIMS)
            for axis,dim in enumerate(DIMS):
                array.dims[axis].label=dim
                array.dims[axis].attach_scale(coordinates[dim])


def read_hdf(path):
    with h5py.File(path,'r') as f:
        coords={dim:xr.DataArray(f['coordinates'][dim][:],dims=dim,
                                 attrs={'units':f['coordinates'][dim].attrs['units']}) for dim in DIMS}
        variables={}
        for name,array in f['fields'].items():
            dims=tuple(array.dims[i].label for i in range(array.ndim))
            if dims!=DIMS or any(len(array.dims[i])!=1 for i in range(4)):
                raise ValueError('Expected one named coordinate scale per axis')
            variables[name]=xr.DataArray(array[:],dims=dims,coords=coords,attrs={'units':array.attrs['units']})
        return xr.Dataset(variables,attrs=dict(f.attrs))


def touched_chunks(shape,chunks,selection):
    total=1
    for length,chunk,part in zip(shape,chunks,selection):
        if isinstance(part,int):count=1
        else:
            start,stop,step=part.indices(length)
            if step!=1:raise ValueError('This example counts contiguous slices')
            count=0 if stop<=start else (stop-1)//chunk-start//chunk+1
        total*=count
    return total


def exact_window_integral(alpha,time):
    sx=np.sqrt(SX0**2+2*alpha*time);sy=np.sqrt(SY0**2+2*alpha*time)
    fraction_x=.5*(erf((8-X0)/(np.sqrt(2)*sx))-erf((-8-X0)/(np.sqrt(2)*sx)))
    fraction_y=.5*(erf((6-Y0)/(np.sqrt(2)*sy))-erf((-6-Y0)/(np.sqrt(2)*sy)))
    return AMPLITUDE*2*np.pi*SX0*SY0*fraction_x*fraction_y


def figures(dataset,summary,output,language):
    zh=language=='zh';tr=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':available_plot_fonts() if zh else ['DejaVu Sans'],
                         'font.size':13,'axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False,'svg.fonttype':'none'})
    def save(fig,name):
        for ext in ['svg','png']:fig.savefig(output/f'{name}-{language}.{ext}',dpi=160,bbox_inches='tight',facecolor='#faf9f5')
        plt.close(fig)
    fig,axes=plt.subplots(2,3,figsize=(13,6.6),layout='constrained',sharex=True,sharey=True)
    for i,alpha in enumerate([.2,.5]):
        for j,time in enumerate([0,10,40]):
            field=dataset.temperature.sel(diffusivity=alpha,time=time)
            im=axes[i,j].pcolormesh(field.x,field.y,field-273.15,cmap='inferno',vmin=20,vmax=100,shading='nearest',rasterized=True)
            axes[i,j].set_aspect('equal');axes[i,j].set_title(f'α={alpha} mm²/s; t={time} s',fontsize=13)
            if i==1:axes[i,j].set_xlabel('x / mm')
            if j==0:axes[i,j].set_ylabel('y / mm')
    fig.colorbar(im,ax=axes,label=tr('温度 / °C（全部面板同一色标）','Temperature / °C (one scale for all panels)'),shrink=.75)
    save(fig,'labeled-diffusion')
    fig=plt.figure(figsize=(13,8),layout='constrained');gs=fig.add_gridspec(2,2)
    for j,name in enumerate(['temperature','sensor_view']):
        ax=fig.add_subplot(gs[0,j]);field=dataset[name].sel(diffusivity=.2,time=20)
        cmap=plt.get_cmap('inferno').copy();cmap.set_bad('#dbe3e6')
        im=ax.pcolormesh(field.x,field.y,field-273.15,vmin=20,vmax=40,cmap=cmap,shading='nearest',rasterized=True)
        ax.set_aspect('equal');ax.set(xlabel='x / mm',ylabel='y / mm',title=tr('完整解析场','Complete analytical field') if j==0 else tr('构造的缺失区域；α=0.2, t=20 s','Constructed missing region; α=0.2, t=20 s'))
        fig.colorbar(im,ax=ax,label=tr('温度 / °C','Temperature / °C'),shrink=.8)
    ax=fig.add_subplot(gs[1,0]);other=fig.add_subplot(gs[1,1])
    for alpha,color in [(.2,'#205b8c'),(.5,'#bd5535')]:
        full=dataset.temperature.sel(diffusivity=alpha).mean(['y','x'])-273.15
        observed=dataset.sensor_view.sel(diffusivity=alpha).mean(['y','x'],skipna=True)-273.15
        ax.plot(dataset.time,full,color=color,lw=2.5,label=f'α={alpha}: '+tr('完整','complete'))
        ax.plot(dataset.time,observed,color=color,ls='--',lw=2,label=f'α={alpha}: '+tr('有效像素均值','valid-cell mean'))
    ax.set(xlabel=tr('时间 / s','Time / s'),ylabel=tr('空间均值 / °C','Spatial mean / °C'));ax.legend(fontsize=11)
    snapshot=dataset.temperature.sel(diffusivity=.2,time=0,y=Y0,method='nearest')
    reversed_snapshot=snapshot.isel(x=slice(None,None,-1))
    positional=snapshot.values-reversed_snapshot.values
    labeled=snapshot-reversed_snapshot
    other.plot(snapshot.x,positional,color='#bd5535',label=tr('按数组位置','By array position'))
    other.plot(labeled.x,labeled,color='#205b8c',lw=3,label=tr('按x坐标对齐','Aligned by x'))
    other.set(xlabel='x / mm',ylabel=tr('温差 / K','Temperature difference / K'),title=tr('同一条剖面，把x顺序倒转','Reverse x order in the same profile'));other.legend(fontsize=12,loc='upper left')
    save(fig,'mask-and-alignment')
    fig=plt.figure(figsize=(13,8.5),layout='constrained');gs=fig.add_gridspec(2,3,width_ratios=[1.2,1,1],height_ratios=[1.25,1])
    info=fig.add_subplot(gs[:,0]);info.axis('off')
    lines=['HDF5','/coordinates','  diffusivity  [0.2, 0.5]  mm²/s','  time          [0 … 60]  s',tr('  y             60个单元中心  mm','  y             60 cell centers  mm'),tr('  x             80个单元中心  mm','  x             80 cell centers  mm'),'/fields','  temperature  (2, 61, 60, 80)','  sensor_view   (2, 61, 60, 80)','  units = K',tr('  维度 → 关联的坐标尺度','  dimensions → attached scales')]
    for i,line in enumerate(lines):info.text(0,1-i*.065,line,fontsize=12.5 if i else 19,transform=info.transAxes,color='#172534',weight='bold' if i in [0,1,6] else 'normal')
    info.text(0,.18,tr('1988：HDF公开发布\n1998：HDF5首次发布\n2017：xarray命名数组论文','1988: HDF public release\n1998: first HDF5 release\n2017: xarray labeled-array paper'),fontsize=13,linespacing=1.8,transform=info.transAxes)
    for j,(name,chunks) in enumerate(LAYOUTS.items()):
        ax=fig.add_subplot(gs[0,j+1]);cy,cx=chunks[-2:]
        for y in range(0,60,cy):
            for x in range(0,80,cx):
                selected=x<=45<x+cx and y<=27<y+cy
                ax.add_patch(Rectangle((x,y),cx,cy,facecolor='#d5e1e7' if not selected else '#d38d58',edgecolor='white',lw=1.4))
        ax.plot(45,27,'o',color='#172534',ms=6);ax.set(xlim=(0,80),ylim=(0,60),xlabel=tr('x单元索引','x cell index'),ylabel=tr('y单元索引','y cell index'),title=f'{chunks}\n'+tr('α、t、y、x方向块尺寸','chunk shape: α, t, y, x'));ax.set_aspect('equal')
    bars=fig.add_subplot(gs[1,1:]);x=np.arange(2);width=.34
    for j,name in enumerate(LAYOUTS):
        values=[summary['storage'][name]['snapshot_chunks'],summary['storage'][name]['trace_chunks']]
        bars.bar(x+(j-.5)*width,values,width,label=name,color=['#205b8c','#bd5535'][j])
        for k,value in enumerate(values):bars.text(x[k]+(j-.5)*width,value+1,str(value),ha='center',fontsize=13)
    bars.set(xticks=x,xticklabels=[tr('一张完整快照','One complete snapshot'),tr('一个点的61时刻','61 times at one point')],ylabel=tr('请求触及的块数','Chunks touched by the request'),ylim=(0,75));bars.legend(fontsize=12)
    save(fig,'coordinates-and-chunks')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=Path('results'));parser.add_argument('--language',choices=['zh','en'],default='en');args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    dataset=make_dataset();storage={};shape=dataset.temperature.shape
    snapshot_request=(0,20,slice(None),slice(None));trace_request=(0,slice(None),27,45)
    for name,chunks in LAYOUTS.items():
        path=args.output/f'{name}.h5';save_hdf(dataset,path,chunks);restored=read_hdf(path)
        xr.testing.assert_allclose(restored.temperature,dataset.temperature)
        xr.testing.assert_allclose(restored.sensor_view,dataset.sensor_view)
        with h5py.File(path,'r') as f:
            assert np.array_equal(f['fields/temperature'][snapshot_request],dataset.temperature.values[snapshot_request])
            assert np.array_equal(f['fields/temperature'][trace_request],dataset.temperature.values[trace_request])
        storage[name]={'chunks':list(chunks),'file_bytes':path.stat().st_size,
                        'snapshot_chunks':touched_chunks(shape,chunks,snapshot_request),
                        'trace_chunks':touched_chunks(shape,chunks,trace_request)}
    initial=dataset.temperature.sel(diffusivity=.2,time=0)
    reverse=initial.isel(x=slice(None,None,-1))
    labeled=float(abs(initial-reverse).max());positional=float(abs(initial.values-reverse.values).max())
    numeric=float((initial-BASE).sum()*.2*.2);exact=float(exact_window_integral(.2,0))
    assert labeled==0 and positional>40 and abs(numeric/exact-1)<1e-4
    summary={'shape':list(shape),'dimensions':list(DIMS),'initial_peak_K':float(initial.max()),
              'labeled_reversal_difference_K':labeled,'positional_reversal_difference_K':positional,
              'initial_window_integral_K_mm2':numeric,'analytic_window_integral_K_mm2':exact,
              'valid_cells_t20':int(dataset.sensor_view.sel(diffusivity=.2,time=20).count()),
              'full_cells':60*80,'full_mean_t20_K':float(dataset.temperature.sel(diffusivity=.2,time=20).mean()),
              'valid_mean_t20_K':float(dataset.sensor_view.sel(diffusivity=.2,time=20).mean()),'storage':storage}
    states=[];frames=[]
    for alpha in [.2,.5]:
        for time in range(0,61,5):
            full=dataset.temperature.sel(diffusivity=alpha,time=time);masked=dataset.sensor_view.sel(diffusivity=alpha,time=time)
            frames.append(full.values)
            states.append({'diffusivity':alpha,'time':time,'full_mean_K':float(full.mean()),
                           'valid_mean_K':float(masked.mean()),'valid_cells':int(masked.count()),'peak_K':float(full.max())})
    arrays=np.asarray(frames,dtype='<f8')
    data={'x':dataset.x.values.tolist(),'y':dataset.y.values.tolist(),'states':states,
          'shape':list(arrays.shape),'field_f64_le':base64.b64encode(arrays.tobytes()).decode('ascii'),
          'colormap_rgb':(plt.get_cmap('inferno')(np.linspace(0,1,256))[:,:3]*255).astype(int).tolist(),
          'storage':storage,'missing_region':{'from_time':20,'xmin':0,'xmax':3,'ymin':-2,'ymax':1}}
    (args.output/'lab-data.json').write_text(json.dumps(data),encoding='utf8')
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    dataset.temperature.mean(['y','x']).to_dataframe(name='mean_temperature_K').to_csv(args.output/'spatial-means.csv')
    figures(dataset,summary,args.output,args.language);print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

程序还把初始温升乘单元面积后求和，得到观察窗口内温升的面积积分约1085.663657 K·mm²；用高斯函数在同一有限矩形上的解析积分得到约1085.663043 K·mm²，二者接近。这个量把网格间距和温度值一起检查，单位是温度乘面积；若要换算真实热量，还需要材料体积热容和薄片厚度。后续温升向窗口外扩散，窗口内积分可以下降，与无限平面模型的总温升积分守恒相容。

### 沿坐标选择场、剖面与时间记录

[Figure: 温度场与选定坐标](https://ml-biomat.com/tutorials/python-scientific/s03/#S03-map)

[Figure: 所选行的双条件温度剖面](https://ml-biomat.com/tutorials/python-scientific/s03/#S03-profile)

[Figure: 选定位置的双条件时间曲线](https://ml-biomat.com/tutorials/python-scientific/s03/#S03-trace)

[Figure: 空间分块、请求覆盖和时间块数](https://ml-biomat.com/tutorials/python-scientific/s03/#S03-chunks)

在交互中选择扩散率和时刻，再移动x、y索引，热图十字标记、当前行剖面和选定位置的时间曲线会一起更新。坐标旁边同时显示索引与毫米位置，便于体会`isel`和`sel`的差别。打开缺失区域后，落在矩形中的值显示为空，相关剖面与时间曲线留下空段；均温与有效单元数也随之改变。灰色缺失区域与较冷的深色区域保持不同外观，避免把没有数据解释成低温。

切换读取请求，可以进一步比较完整快照与选定点时间序列在两种块布局中需要访问的区域。空间块网格展示当前点所在的位置，计数分别跟随快照或时间序列定义更新。页面使用Python保存的13个展示时刻及实际存储布局；原始HDF5仍保留每秒一个时刻的61帧，下载例子可以取出更细的时间变化。显示采样与存储采样的区别，也被明确保留在数据说明中。

## 把有名字的数据组织方式带进实际研究

组织新的多维数据时，可以先写出一段能够回答“一个元素是什么”的句子：某个样品、某个时刻、某个空间位置的温度，或某个波长、某种处理条件下的光谱强度。句子里用于定位的部分通常成为维度与坐标，被记录的物理量成为变量，单位和实验条件成为属性。这样得到的数据结构来自研究对象，后续选择、平均和比较就有明确方向。

还应区分维度坐标与统计独立性。61个连续时刻属于同一个变化过程，并不会因为它们各占一个数组位置，就自动成为61次独立重复测量。两种扩散率也是两个设定条件，不能在没有研究含义的情况下随意求总体平均。缺失值处理同样要保留覆盖范围：跳过缺失单元计算的是有效区域均值，恢复完整区域均值需要额外的测量或明确的插值模型。

xarray与h5py组合起来，让分析对象和保存对象之间保持一条清楚的连接：名字定义轴，坐标确定位置，属性解释单位，块布局服务读取。读者可以从一幅热图回到相应数组，再回到文件中的坐标与变量。对于显微图像序列、散射图、空间场和多条件实验，这种组织方式既减少轴方向混淆，也为后续共享和复用留下完整的科学含义。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/S03.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [xarray quick overview](https://docs.xarray.dev/en/stable/getting-started-guide/quick-overview.html)

   DataArray、Dataset、命名维度和坐标的开放教程。

   xarray Apache-2.0; original chapter implementation.
2. [xarray indexing and selecting data](https://docs.xarray.dev/en/stable/user-guide/indexing.html)

   按位置或标签选择，以及坐标对齐。

   xarray Apache-2.0.
3. [h5py datasets](https://docs.h5py.org/en/stable/high/dataset.html)

   切片、分块和压缩设置。

   h5py BSD-3-Clause.
4. [h5py dimension scales](https://docs.h5py.org/en/stable/high/dims.html)

   维度标签与坐标尺度关联。

   h5py BSD-3-Clause.
5. [The HDF Group: Balancing Performance and Preservation (2010)](https://docs.hdfgroup.org/archive/support/pubs/papers/HDFandpreservation_NIST_2010_paper_Folk.pdf)

   1988年HDF与1998年HDF5发布历史、保存科学数据含义的问题。

   Historical factual citation; original file-structure and chunk diagrams.
6. [Hoyer and Hamman (2017), xarray: N-D labeled Arrays and Datasets in Python](https://doi.org/10.5334/jors.148)

   有名字的多维数组在科学Python中的设计背景。

   Open research software paper; scientific citation.
