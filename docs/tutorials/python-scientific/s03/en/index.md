# Organizing Labeled Multidimensional Data

Source: https://ml-biomat.com/tutorials/python-scientific/s03/en/
Language: en

Use thermal fields to understand coordinate alignment, missing coverage, and HDF5 chunks while preserving location and units.

## Named axes let an analysis know where to operate

A camera temperature map gives every pixel a horizontal and vertical position. Repeated imaging adds time; comparing two materials adds another condition. Such data soon exceed the intuition of a two-dimensional table. The shape (2,61,60,80) alone cannot identify the time axis, the spatial axes, or the meaning of the two conditions. xarray places those meanings inside the data object through dimension names, coordinates, and attributes, keeping numerical arrays connected to their scientific interpretation.

This chapter creates two-dimensional temperature fields for two thermal diffusivities. Each condition has 61 times and 60×80 spatial cells per time, with a spacing of 0.2 mm. An analytical Gaussian diffusion model on an infinite plane generates the fields, starting with a 100 °C peak above a 20 °C background. These are teaching fields with an explicit physical rule. A constructed rectangular region becomes missing from 20 s onward so that we can examine how data coverage changes a mean. Complete and masked fields are retained together, allowing physical evolution and sampling changes to be inspected separately.

xarray selects and calculates by scientific meaning. h5py stores multidimensional arrays, coordinates, and units in HDF5 and reads selected portions. Together they support interpretable files whose meaning does not depend on filenames and personal memory. The project produces two HDF5 layouts and compares how many storage chunks are touched by a spatial snapshot or a point’s time series. An interactive explorer links temperature maps, spatial profiles, temporal traces, and storage requests.

## Giving the temperature field an interpretable evolution

Imagine briefly heating part of a sufficiently large uniform thin sheet and then stopping the heating. Heat spreads from warmer to cooler regions, lowering the local peak and broadening the affected area. Our initial temperature excess is a smooth elliptical mound centered at (1.1,−0.5) mm, with widths of 1.8 and 1.2 mm along the two directions. Thermal diffusivity α controls the rate of spreading. We compare 0.2 and 0.5 mm²/s while retaining the same initial field.

$$
\begin{aligned}w_x^2(t)&=\sigma_x^2+2\alpha t,\qquad w_y^2(t)=\sigma_y^2+2\alpha t\\T(x,y,t)&=T_b+\Delta T_0\frac{\sigma_x\sigma_y}{w_x(t)w_y(t)}\exp\left[-\frac12\left(\frac{(x-x_0)^2}{w_x^2(t)}+\frac{(y-y_0)^2}{w_y^2(t)}\right)\right]\end{aligned}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/8f5e8856b86122b7ce047547.svg) | temperature at position (x,y) and time t, K |
| ![Formula](https://ml-biomat.com/static/agent-math/78b803e9ef905a830a512636.svg) | spatial and hot-spot center coordinates, mm; center (1.1,−0.5) mm |
| ![Formula](https://ml-biomat.com/static/agent-math/707bb132def3690d81bf1f0c.svg) | time, s, from 0 to 60 s here |
| ![Formula](https://ml-biomat.com/static/agent-math/7995b2daef1650484d2fa651.svg) | thermal diffusivity, mm²/s, 0.2 or 0.5 here |
| ![Formula](https://ml-biomat.com/static/agent-math/92a2a2de680d59d4186c0571.svg) | initial Gaussian widths, mm, 1.8 and 1.2 here |
| ![Formula](https://ml-biomat.com/static/agent-math/ccddec3bddcb880f73f5bca6.svg) | widths after diffusion along each direction, mm |
| ![Formula](https://ml-biomat.com/static/agent-math/268897e0a26bd3db213c08b9.svg) | background temperature 293.15 K, or 20 °C |
| ![Formula](https://ml-biomat.com/static/agent-math/4df209ad4efd080121d47c05.svg) | initial central temperature excess, 80 K |
| ![Formula](https://ml-biomat.com/static/agent-math/64460da0d752153c52e1bd62.svg) | natural exponential; squared displacement divided by squared width is dimensionless |

This is the diffusion solution for a Gaussian initial temperature excess on a uniform infinite plane. Diffusion increases squared widths by 2αt; the width ratio reduces the peak while preserving the excess-temperature area integral over the whole plane. At t=0 at the center, widths equal their initial values and the exponent is zero, giving 293.15+80=373.15 K, or 100 °C. At α=0.2 mm²/s and t=20 s, squared widths are 3.24+8=11.24 mm² and 1.44+8=9.44 mm², corresponding to approximately 3.3526 and 3.0725 mm.

Squared widths increase linearly with time, so the widths themselves do not grow at a constant rate. The amplitude factor falls as both widths increase, connecting broadening with a declining peak. Both diffusivities yield the same field at time zero; the larger diffusivity subsequently spreads the excess temperature more rapidly. We observe a window from −8 to 8 mm horizontally and −6 to 6 mm vertically. The same infinite-plane solution continues beyond that window: its edges are observation boundaries, without an additional insulating condition.

![One Gaussian diffusion model at two diffusivities and three times, with a shared temperature scale; the window samples part of an infinite plane.](https://ml-biomat.com/static/tutorials/python-scientific/figures/87d5fda1e1a4eaca78fa07dc.svg?v=87d5fda1e1a4)

Figure 1One Gaussian diffusion model at two diffusivities and three times, with a shared temperature scale; the window samples part of an infinite plane.

All six maps use one 20–100 °C color scale, so a given color always means the same temperature. Later maps darken because the temperature excess decreases, while its spatial distribution broadens. Automatically stretching every map’s own minimum and maximum across the color scale would turn even a weak late peak bright yellow again, making it easy to confuse a broader distribution with equally strong heating. Numerical profiles complement the common-scale maps by showing details that appear relatively dark.

The program stores temperature in kelvin and displays maps in degrees Celsius. Changing scales requires changing values, rather than editing an axis label alone. In contrast, a temperature difference of 1 K has the same magnitude as a difference of 1 °C, making kelvin convenient for temperature excess and error. A `units` attribute records the unit meaning, but ordinary xarray arithmetic does not automatically convert units from that string. The conversion is written explicitly, and the resulting attribute is updated accordingly.

$$
T_{\degree\mathrm C}=T_{\mathrm K}-273.15
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d0fd16bf369d52ab9d375978.svg) | numerical temperature value expressed in degrees Celsius |
| ![Formula](https://ml-biomat.com/static/agent-math/6d443f0ab15429bfcc4eb1d9.svg) | numerical value of the same temperature expressed in kelvin |
| ![Formula](https://ml-biomat.com/static/agent-math/41eb4d81094d336d45d3ea35.svg) | fixed numerical offset between the two temperature scales |

This converts the numerical representation of the same physical temperature. 293.15 K becomes 293.15−273.15=20 °C, and 373.15 K becomes 100 °C. The constant offsets cancel in a temperature difference, so differences of 80 K and 80 °C have equal magnitude. Update the unit attribute along with the numerical conversion.

## What dimensions, coordinates, and attributes each contribute

A `DataArray` is a numerical array accompanied by coordinate information. Here its dimension order is `diffusivity, time, y, x`, with lengths 2, 61, 60, and 80. A dimension name identifies an axis; its coordinate identifies the physical value at each position along it; attributes preserve units and model meaning. The `time` coordinate runs from zero to sixty seconds. The eighty `x` coordinates are cell centers from −7.9 to 7.9 mm, rather than the integer array indices zero through seventy-nine.

`isel` selects by position and `sel` selects by coordinate. `isel(time=20)` selects the twenty-first position, whereas `sel(time=20)` selects the coordinate value 20 s. They happen to agree in this one-second sampling grid. If the coordinate later changes to five-second spacing, index twenty corresponds to 100 s and the meanings separate clearly. Spatial selection behaves similarly: requesting x=1.1 mm identifies a physical location, rather than element number 1.1.

A `Dataset` holds the complete temperature field and masked view together with shared dimensions and coordinates. It resembles a container of related scientific tables, while allowing each variable its own dimension combination. Full temperature retains four axes; spatial mean temperature retains diffusivity and time. Calling `mean(['y','x'])` removes spatial dimensions by name. If axis order is later rearranged for storage or plotting, the same expression continues to describe the same scientific operation.

Named operations also bring code closer to a research question. A map for one diffusivity at 20 s is `temperature.sel(diffusivity=0.2, time=20)`. A comparison of diffusivities selects corresponding times and spatial coordinates under each condition. Shape, coordinate units, and variable names remain available in the result, allowing the reader to check whether a selection produced a map, a profile, or a time record at one location.

## Coordinate alignment and missing values change the meaning of results

Reversing the x order of a map changes storage order while preserving the physical position associated with every value. Direct subtraction of two NumPy arrays pairs their first elements, then their second elements, and so on, comparing different locations. Because the hot spot is off-center, the largest resulting discrepancy is approximately 52.5282 K. xarray instead aligns matching x coordinates before subtraction. Every temperature is compared with itself, and the difference is zero everywhere. Equal array positions and equal physical coordinates are different relationships.

Automatic alignment depends on correct coordinates. Two axes both named x can still use different units, or one may describe cell centers while the other describes boundaries. Unify units and coordinate definitions before deciding whether to subtract common labels or interpolate onto a common grid. If coordinate sets only partly overlap, inspect which positions remain after arithmetic. Otherwise a reduced domain can be mistaken for naturally disappearing data. Reversing exactly the same coordinates here makes a zero result an unambiguous check of alignment behavior.

![Complete and masked fields, spatial means, and subtraction after coordinate reversal reveal effects of coverage and labels. The mask starts at 20 s while the complete analytical field stays continuous.](https://ml-biomat.com/static/tutorials/python-scientific/figures/534f210e5ea8f15c8c385c1d.svg?v=534f210e5ea8)

Figure 2Complete and masked fields, spatial means, and subtraction after coordinate reversal reveal effects of coverage and labels. The mask starts at 20 s while the complete analytical field stays continuous.

The missing region creates another kind of change. In the masked view, 225 cells with x from 0 to 3 mm and y from −2 to 1 mm become `NaN` at and after 20 s. The complete analytical field is unchanged, and the masked field does not treat that region as zero temperature. With `mean(..., skipna=True)`, floating-point missing values are skipped and the average uses the remaining 4575 cells. The complete field at the same instant contains 4800 cells, so the two means summarize different spatial domains.

$$
\overline T_{\rm valid}=\frac{1}{N_{\rm valid}}\sum_{(i,j)\in\mathcal V}T_{ij},\qquad f_{\rm valid}=\frac{N_{\rm valid}}{N_{\rm all}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6fa439d6e71a5c78c00edf6c.svg) | mean temperature over valid cells, K |
| ![Formula](https://ml-biomat.com/static/agent-math/1f848077b31e64f57fc97f4b.svg) | dimensionless row and column indices of spatial cells |
| ![Formula](https://ml-biomat.com/static/agent-math/09a167b42cf9b0ee95226228.svg) | set of spatial cells with valid values |
| ![Formula](https://ml-biomat.com/static/agent-math/da5f776e1e01a0f2e5cb8938.svg) | cell (i,j) temperature at a specified diffusivity and time, K |
| ![Formula](https://ml-biomat.com/static/agent-math/9b9441d841a7d77652c30687.svg) | sum temperature values over the valid set |
| ![Formula](https://ml-biomat.com/static/agent-math/03a8f63d99ba4d42f78d37e1.svg) | valid and total cell counts, dimensionless |
| ![Formula](https://ml-biomat.com/static/agent-math/448cb411f8cabff5424d5145.svg) | valid coverage fraction, dimensionless |

Cells have equal area, so a spatial mean gives equal weight to valid cells. From 20 s onward, 225 missing cells leave 4800−225=4575, a fraction 4575/4800=0.953125 or 95.3125%. At α=0.2 and t=20 s, the valid mean is 297.870916 K or 24.720916 °C; the complete-cell mean is 298.376697 K or 25.226697 °C. Area means on nonuniform grids require cell-area weighting.

At α=0.2 mm²/s and t=20 s, the complete-domain mean is approximately 25.226697 °C, while the valid-cell mean is approximately 24.720916 °C. The difference is about 0.506 °C because the constructed missing rectangle covers a warmer central region. The dashed curve’s jump at 20 s arises from changing coverage; the complete temperature field evolves smoothly. Saving valid-cell count or coverage alongside a spatial mean distinguishes this sampling change from a change in the material response.

## Saving coordinates together with values

Scientific computing has long faced the problem of reading bytes without knowing what they represent. HDF originated in sharing scientific data across computing platforms, with its first release in 1988 and HDF5 first released in 1998. It stores multidimensional values together with structures that describe them. Hoyer and Hamman’s 2017 xarray paper brought labeled multidimensional arrays into Python analysis. These developments meet in this example: the file retains an interpretable structure, and the analysis continues using its names and coordinates.

An HDF5 `Group` resembles a directory, a `Dataset` holds an array, and `attrs` stores additional description. This example creates `/coordinates` and `/fields` groups for coordinate arrays and temperature variables. A temperature dataset has shape (2,61,60,80), but also labels every axis and attaches its corresponding coordinate dataset as a dimension scale. A reader can therefore discover from the file itself that the second axis is time, what its values are, and which units they use.

![Coordinate associations and two chunk shapes in the actual HDF5 layouts. The black point has x index 45 and y index 27; bars compare chunk counts for a snapshot and a 61-time point trace.](https://ml-biomat.com/static/tutorials/python-scientific/figures/e95d9db38a90d4e762e2e8f3.svg?v=e95d9db38a90)

Figure 3Coordinate associations and two chunk shapes in the actual HDF5 layouts. The black point has x index 45 and y index 27; bars compare chunk counts for a snapshot and a 61-time point trace.

h5py offers array-like slicing of HDF5 datasets, while a generic HDF5 file does not automatically follow a particular higher-level convention. The complete example consequently defines its reader explicitly: read coordinates from the coordinate group, recover dimension order from axis labels, recover units from attributes, and construct xarray objects. Convention-based data such as NetCDF can use an appropriate direct backend. For a custom HDF5 layout, a consistent reader and writer keep field meanings explicit across the storage boundary.

After writing, the program reads both variables back and compares their values and missing positions with the original objects. It checks that each axis has one attached coordinate scale. It also directly reads a complete snapshot and one point’s temporal trace from HDF5 and compares those selections with their in-memory equivalents. This checks both complete-file recovery and two common research queries. Unit strings, dimension labels, and coordinate arrays are part of the reusable scientific data alongside the numerical field.

## How storage chunks affect a request for a small part

Compressed multidimensional data are commonly stored in chunks. To satisfy a slice request, HDF5 accesses and decodes the intersecting chunks before selecting the required values. Chunk shape should therefore reflect common reading patterns. We write the same dataset twice: `snapshot.h5` uses chunks (1,1,20,20), while `time_series.h5` uses (1,10,10,10). Entries correspond to diffusivity, time, y, and x. Both files use the same gzip and shuffle settings; their difference is how values are grouped into chunks.

A full 60×80 snapshot at one diffusivity and one time touches three y chunks and four x chunks in the first layout, totaling twelve. In the second layout it touches six by eight spatial chunks, totaling forty-eight. Reading all 61 times at one spatial point instead touches 61 chunks in the first layout, which contains one time per chunk, and seven in the second, which contains ten. The orange spatial block identifies where the selected point lies, while the counts make each reading pattern independently checkable.

These are counts of logical chunks touched by the request. Elapsed time also depends on bytes per chunk, compressed size, cache behavior, and the storage device. File sizes follow from actual compression and cannot be inferred from chunk count alone. In practice, list common snapshot, profile, or time-window requests, estimate their intersecting chunks, and then benchmark representative data. Both layouts remain available in the example so that a reader can investigate a workload with their own mixture of requests.

Slicing also avoids reading an entire large file into memory. `dataset[0,20,:,:]` requests one snapshot, while `dataset[:]` reads the whole array. These teaching arrays are modest enough for the reader function to recover complete variables for comparison. Larger projects can keep a file open for selective reads or use a higher-level array supporting delayed computation. Coordinate and unit meaning should follow the resulting slice regardless of how much data are loaded.

## The full example and synchronized exploration

The program below generates the analytical fields, constructs labeled arrays, applies the specified missing rectangle, and writes and verifies two HDF5 files. `spatial-means.csv` exports complete-field spatial averages while retaining diffusivity and time coordinates. `summary.json` records alignment, coverage, and chunk-query results. Figures and the interactive explorer use these computations; the field-generation rule and every storage operation are included in the same program.

### Generate and read both HDF5 files

Use zh for Chinese figures.

```
python main.py --output results --language en
```

### Labeled thermal fields, HDF5 round trips, and chunk comparison

The temperature model, missing-region rule, labeled arrays, two layouts, and complete reader are included.

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

The program also sums initial temperature excess multiplied by cell area, obtaining a window integral of approximately 1085.663657 K·mm². Analytical integration of the Gaussian over the same finite rectangle gives approximately 1085.663043 K·mm². This comparison checks both spacing and field values. The quantity is temperature times area; conversion to physical heat would additionally require volumetric heat capacity and sheet thickness. As temperature excess spreads outside the window, its integral inside the window can decrease consistently with conservation over the entire infinite plane.

### Select fields, profiles, and traces by coordinates

[Figure: Temperature field and selected coordinates](https://ml-biomat.com/tutorials/python-scientific/s03/en/#S03-map)

[Figure: Temperature profiles for both conditions at the selected row](https://ml-biomat.com/tutorials/python-scientific/s03/en/#S03-profile)

[Figure: Temporal traces for both conditions at the selected point](https://ml-biomat.com/tutorials/python-scientific/s03/en/#S03-trace)

[Figure: Spatial chunks, requested coverage, and temporal chunk count](https://ml-biomat.com/tutorials/python-scientific/s03/en/#S03-chunks)

Select diffusivity and time, then move the x and y indices. The map crosshair, selected-row profile, and temporal trace at the selected location update together. Controls show both index and millimetre coordinate, making the difference between `isel` and `sel` tangible. Enabling the missing rectangle replaces affected values with missing data and leaves gaps in the corresponding profiles and traces. Mean and valid-cell count change with coverage. Missing cells are gray, distinct from darker cold cells, so absent data are not visually interpreted as low temperature.

Changing the storage request compares a complete snapshot with the selected point’s time series under both chunk layouts. Spatial chunk grids show where the point falls, and counts follow the requested data shape. The page uses thirteen display times saved by Python together with the actual storage layout. Original HDF5 files retain all 61 one-second frames, allowing the downloadable example to inspect finer temporal changes. Display sampling and stored sampling are therefore identified separately.

## Bringing labeled organization into research data

Begin a new multidimensional dataset by writing a sentence that identifies one element: temperature for a specimen at a time and spatial position, or spectral intensity at a wavelength under a treatment condition. Parts that locate the element usually become dimensions and coordinates. The measured quantity becomes a variable, while units and experimental conditions become attributes. This builds the data structure from the research object and gives subsequent selection, averaging, and comparison explicit directions.

Dimension positions should also be distinguished from statistical independence. Sixty-one successive times belong to one evolving process; occupying separate array positions does not turn them into independent experimental repeats. The two diffusivities are specified conditions, and averaging them requires an actual research interpretation. Missing-data handling similarly retains its domain: skipping missing cells computes a valid-region mean, while recovering a complete-region mean requires additional measurement or an explicit interpolation model.

xarray and h5py maintain a readable connection between the analysis object and the stored object. Names identify axes, coordinates locate values, attributes describe units, and chunk layout serves access patterns. A reader can move from a map to the corresponding array and then to coordinates and variables in the file. For microscopy series, scattering maps, field outputs, and multiple-condition experiments, this organization reduces axis confusion while preserving the scientific meaning needed for sharing and further analysis.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/S03.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [xarray quick overview](https://docs.xarray.dev/en/stable/getting-started-guide/quick-overview.html)

   Open tutorial for DataArray, Dataset, named dimensions, and coordinates.

   xarray Apache-2.0; original chapter implementation.
2. [xarray indexing and selecting data](https://docs.xarray.dev/en/stable/user-guide/indexing.html)

   Selection by position or label and coordinate alignment.

   xarray Apache-2.0.
3. [h5py datasets](https://docs.h5py.org/en/stable/high/dataset.html)

   Slicing, chunks, and compression settings.

   h5py BSD-3-Clause.
4. [h5py dimension scales](https://docs.h5py.org/en/stable/high/dims.html)

   Dimension labels and attached coordinate scales.

   h5py BSD-3-Clause.
5. [The HDF Group: Balancing Performance and Preservation (2010)](https://docs.hdfgroup.org/archive/support/pubs/papers/HDFandpreservation_NIST_2010_paper_Folk.pdf)

   HDF’s 1988 and HDF5’s 1998 releases and the problem of preserving scientific meaning.

   Historical factual citation; original file-structure and chunk diagrams.
6. [Hoyer and Hamman (2017), xarray: N-D labeled Arrays and Datasets in Python](https://doi.org/10.5334/jors.148)

   Design context of labeled multidimensional arrays in scientific Python.

   Open research software paper; scientific citation.
