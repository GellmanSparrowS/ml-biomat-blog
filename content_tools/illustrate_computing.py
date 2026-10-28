"""Generate bilingual explanatory SVGs and insert them into 12 existing article pairs.

All numeric examples are teaching data. Run from the repository root.
The script preserves existing text and code; additions are idempotent.
"""
from pathlib import Path
from html import escape
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'static/images/article-guides'
OUT.mkdir(parents=True, exist_ok=True)
INK='#203348'; BLUE='#386fd1'; TEAL='#13887f'; ORANGE='#ca7b37'; MUTED='#526678'; LINE='#d6e1ec'; BG='#f7fafc'
FONT='Microsoft YaHei'
plt.rcParams.update({'font.family':FONT, 'font.size':18, 'axes.titlesize':23,
 'axes.labelsize':20, 'xtick.labelsize':18, 'ytick.labelsize':18, 'legend.fontsize':18,
 'svg.fonttype':'none', 'axes.spines.top':False, 'axes.spines.right':False,
 'axes.labelcolor':INK, 'text.color':INK, 'xtick.color':INK, 'ytick.color':INK,
 'axes.edgecolor':MUTED, 'figure.facecolor':BG, 'axes.facecolor':BG})

def choose(lang,en,zh): return zh if lang=='zh' else en

class Drawing:
 def __init__(self,title,subtitle='',height=460):
  self.height=height
  self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="{height}" viewBox="0 0 760 {height}" role="img"><title>{escape(title)}</title><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{MUTED}"/></marker></defs><rect width="760" height="{height}" rx="16" fill="{BG}"/>']
  self.text(30,42,title,26,weight=600)
  if subtitle:self.text(30,76,subtitle,18,MUTED)
 def text(self,x,y,s,size=20,color=INK,anchor='start',weight=400):
  self.parts.append(f'<text x="{x}" y="{y}" font-family="&quot;Microsoft YaHei&quot;,&quot;Noto Sans SC&quot;,Arial,sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(s))}</text>')
 def rect(self,x,y,w,h,fill='white',stroke=LINE,rx=9):
  self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>')
 def line(self,x1,y1,x2,y2,color=MUTED,width=2,arrow=False,dash=False):
  self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="6 5"' if dash else '')+'/>')
 def circle(self,x,y,r=23,label='',fill='white',stroke=BLUE):
  self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')
  if label:self.text(x,y+7,label,21,anchor='middle',weight=600)
 def table(self,x,y,rows,widths,rowh=44,header=True):
  for i,row in enumerate(rows):
   xx=x
   for j,v in enumerate(row):
    self.rect(xx,y+i*rowh,widths[j],rowh,'#eaf1fa' if i==0 and header else 'white',rx=0)
    self.text(xx+widths[j]/2,y+i*rowh+rowh/2+7,v,20,anchor='middle',weight=600 if i==0 and header else 400)
    xx+=widths[j]
 def footer(self,s):self.text(30,self.height-23,s,18,MUTED)
 def save(self,key,lang):
  (OUT/f'comp-guide-{key}-{lang}.svg').write_text('\n'.join(self.parts)+ '</svg>','utf-8')

def native(key,lang):
 T=lambda a,b:choose(lang,a,b)
 if key=='environment-isolation':
  d=Drawing(T('Separate projects, separate dependencies','项目隔离：解释器与依赖各自独立'),T('Version labels below are schematic.','图中版本代号用于说明环境隔离。'))
  for x,name,py,pkg,col in [(30,'project-a','Python A','NumPy v1',BLUE),(400,'project-b','Python B','NumPy v2',TEAL)]:
   d.rect(x,112,330,250);d.text(x+24,150,name,24,col,weight=600)
   for yy,txt in [(180,py),(242,pkg)]:d.rect(x+24,yy,282,48,'#eef5fa');d.text(x+165,yy+31,txt,22,anchor='middle')
   d.text(x+165,337,T('Own installation directory','独立安装目录'),20,anchor='middle')
  d.line(380,124,380,355,LINE,2,dash=True)
  d.footer(T('Activating an environment selects its interpreter and packages.','激活环境后，调用该环境的解释器与工具包。'))
 elif key=='jupyter-kernel':
  d=Drawing(T('Which Python executes a notebook?','Notebook 代码由哪个 Python 执行？'),T('The selected kernel determines the runtime environment.','选中的内核决定代码实际运行的环境。'))
  d.rect(30,116,250,214);d.text(155,155,'JupyterLab',24,BLUE,anchor='middle',weight=600)
  d.rect(52,180,206,50,'#eef5fa');d.text(155,212,T('Notebook cells','Notebook 单元格'),20,anchor='middle')
  d.text(155,286,T('Browser interface','浏览器界面'),20,anchor='middle')
  d.line(285,223,355,223,arrow=True);d.text(320,199,T('run','执行'),18,anchor='middle')
  d.rect(367,116,363,214);d.text(548,154,T('Selected kernel','当前内核'),24,TEAL,anchor='middle',weight=600)
  d.text(548,201,'project-a / Python',22,anchor='middle');d.line(548,218,548,249,arrow=True)
  d.text(548,281,'NumPy · SciPy · pandas',20,anchor='middle')
  d.rect(108,360,544,55,'#eaf1fa');d.text(380,395,'import sys; print(sys.executable)',22,anchor='middle')
 elif key=='neuron':
  d=Drawing(T('One neuron: weighted sum, then activation','一个神经元：加权求和，再做激活'),T('Teaching example: x = (2, −1), w = (0.5, 1), b = 0.2','教学示例：x = (2, −1)，w = (0.5, 1)，b = 0.2'))
  d.circle(100,176,38,'2');d.circle(100,298,38,'−1');d.line(142,180,285,229,BLUE,3,True);d.line(142,295,285,249,TEAL,3,True)
  d.text(202,177,'× 0.5',20,BLUE,anchor='middle');d.text(199,309,'× 1',20,TEAL,anchor='middle')
  d.rect(296,190,160,98);d.text(376,230,T('Sum + bias','求和 + 偏置'),21,anchor='middle');d.text(376,265,'z = 0.2',24,anchor='middle',weight=600)
  d.line(462,239,522,239,arrow=True);d.rect(535,190,195,98);d.text(632,229,'ReLU(z)',24,BLUE,anchor='middle');d.text(632,265,'max(0, z) = 0.2',18,anchor='middle')
  d.text(380,365,'2 × 0.5 + (−1) × 1 + 0.2 = 0.2',23,anchor='middle');d.footer(T('Weights set each input contribution; the activation maps the result.','权重控制各输入的贡献，激活函数把求和结果映射为输出。'))
 elif key=='gradient-step':
  d=Drawing(T('A gradient step, worked through','一次梯度更新，逐步算清楚'),T('Teaching example: prediction = w × x; x = 2, target = 1','教学示例：预测值 = w × x；x = 2，目标值 = 1'))
  for x,title,lines,col in [(30,T('Before the step','更新前'),['w = 0.25',T('Prediction = 0.50','预测值 = 0.50'),'L = 0.125'],BLUE),(410,T('After the step','更新后'),['w = 0.35',T('Prediction = 0.70','预测值 = 0.70'),'L = 0.045'],TEAL)]:
   d.rect(x,117,320,182);d.text(x+160,151,title,23,col,anchor='middle',weight=600)
   for i,s in enumerate(lines):d.text(x+160,192+i*36,s,21,anchor='middle')
  d.line(355,211,401,211,arrow=True)
  d.text(380,344,'L = 0.5 × (w × x − y)²',22,anchor='middle')
  d.text(380,380,'dL/dw = (0.50 − 1) × 2 = −1',22,anchor='middle')
  d.footer(T('Learning rate 0.1:  w ← 0.25 − 0.1 × (−1) = 0.35','学习率为 0.1：w ← 0.25 − 0.1 × (−1) = 0.35'))
 elif key=='confusion-matrix':
  d=Drawing(T('Read the counts before the scores','先看混淆矩阵，再看指标'),T('Teaching data: 20 binary classifications','教学数据：20 个二分类样本'))
  d.table(30,122,[[T('Actual / predicted','实际 / 预测'),'+','−'],['+',8,1],['−',2,9]],[188,110,110],66)
  d.text(452,150,T('Precision','精确率'),21,BLUE,weight=600);d.text(452,181,'8 / (8 + 2) = 0.800',19)
  d.text(452,224,T('Recall','召回率'),21,TEAL,weight=600);d.text(452,255,'8 / (8 + 1) ≈ 0.889',19)
  d.text(452,298,T('Accuracy','准确率'),21,ORANGE,weight=600);d.text(452,329,'(8 + 9) / 20 = 0.850',19)
  d.footer(T('False positives = 2; false negatives = 1. The costs can differ.','假阳性为 2，假阴性为 1；两类错误可对应不同代价。'))
 elif key=='adjacency':
  d=Drawing(T('A graph and its adjacency matrix','同一张图的节点与邻接矩阵'),T('Undirected, unweighted; node order A, B, C, D','无向、无权图；矩阵节点顺序为 A、B、C、D'))
  pos={'A':(80,165),'B':(265,165),'C':(172,284),'D':(80,366)}
  for a,b in [('A','B'),('A','C'),('B','C'),('C','D')]:d.line(*pos[a],*pos[b],BLUE,3)
  for n,(x,y) in pos.items():d.circle(x,y,26,n)
  d.table(350,115,[['','A','B','C','D'],['A',0,1,1,0],['B',1,0,1,0],['C',1,1,0,1],['D',0,0,1,0]],[60]*5,49)
  d.text(525,393,T('Row C sums to degree 3','C 行求和得到度数 3'),20,TEAL,anchor='middle')
  d.footer(T('An edge appears twice in a symmetric adjacency matrix.','每条无向边在对称邻接矩阵中出现两次。'))
 elif key=='weighted-path':
  d=Drawing(T('Fewest hops or lowest total weight?','最少跳数，还是最小权重和？'),T('The edge labels are teaching weights, all nonnegative.','边上的数字为非负教学权重。'))
  pos={'A':(90,230),'B':(300,125),'C':(300,335),'D':(505,230)}
  for a,b,w,col in [('A','B',1,TEAL),('B','D',2,TEAL),('A','C',2,LINE),('C','D',4,LINE),('A','D',5,ORANGE)]:
   d.line(*pos[a],*pos[b],col,4);x=(pos[a][0]+pos[b][0])/2;y=(pos[a][1]+pos[b][1])/2;d.rect(x-15,y-17,30,31,BG,BG,3);d.text(x,y+6,w,20,anchor='middle')
  for n,(x,y) in pos.items():d.circle(x,y,26,n)
  d.text(562,172,T('By hops','按跳数'),21,ORANGE,weight=600);d.text(562,205,'A → D',21);d.text(562,278,T('By weight','按权重'),21,TEAL,weight=600);d.text(562,312,'A → B → D',20)
  d.footer(T('A → D: 1 hop, weight 5.  A → B → D: 2 hops, weight 3.','A → D：1 跳，权重 5；A → B → D：2 跳，权重 3。'))
 elif key=='boolean-mask':
  d=Drawing(T('A Boolean mask keeps aligned observations','布尔掩码保留对应位置的数据'),T('Teaching data; the strict test excludes strain = 0.020.','教学数据；严格小于条件会排除应变 0.020。'))
  d.table(30,115,[[T('Strain','应变'),'0','0.005','0.010','0.020'],[T('Stress / MPa','应力 / MPa'),'0','8','15','28'],['strain < 0.02','T','T','T','F']],[220,120,120,120,120],57,False)
  for x in [310,430,550]:d.line(x,298,x,331,TEAL,2,True)
  d.rect(190,348,380,55,'#eaf5f2');d.text(380,383,'stress[mask] = [0, 8, 15]',23,TEAL,anchor='middle')
 elif key=='broadcasting':
  d=Drawing(T('Broadcasting: center each column','广播运算：每列减去该列均值'),T('Teaching matrix, shape (2, 3); mean(axis=0) has shape (3,).','教学矩阵形状为 (2, 3)，mean(axis=0) 的形状为 (3,)。'))
  d.text(135,135,T('Original array','原数组'),22,BLUE,anchor='middle');d.table(30,160,[[1,2,3],[4,5,6]],[70]*3,56,False)
  d.text(380,135,T('Column means','列均值'),22,ORANGE,anchor='middle');d.table(275,188,[[2.5,3.5,4.5]],[70]*3,56,False)
  d.text(630,135,T('Centered array','中心化数组'),22,TEAL,anchor='middle');d.table(525,160,[['−1.5']*3,['1.5']*3],[70]*3,56,False)
  d.text(257,225,'−',25,anchor='middle');d.text(505,225,'=',25,anchor='middle')
  d.text(380,338,T('The same row of means is used for both rows.','同一行列均值参与每一行的减法。'),21,anchor='middle')
  d.footer('centered = data - data.mean(axis=0)')
 elif key=='groupby':
  d=Drawing(T('Group rows, then compute summaries','按条件分组，再计算统计量'),T('Teaching data: modulus in GPa','教学数据：模量单位为 GPa'))
  d.table(30,119,[[T('Group','组别'),T('Modulus','模量')],['A',2],['A',4],['B',6],['B',8]],[130,130],49)
  d.line(300,240,401,240,arrow=True);d.text(350,211,'groupby',19,anchor='middle')
  d.table(415,158,[[T('Group','组别'),'n',T('Mean','均值')],['A',2,3],['B',2,7]],[110,75,120],56)
  d.footer(T('Each summary retains the group identity and the number of samples.','统计结果保留组别与样本数，便于比较不同实验条件。'))
 elif key=='merge':
  d=Drawing(T('Match measurements by sample ID','按样品编号匹配两类测量'),T('Teaching tables; inner join keeps IDs present in both.','教学表格；内连接只保留两张表共有的样品编号。'))
  d.table(30,118,[[T('ID','编号'),'E / GPa'],['A1',2],['A2',3]],[100,135],49)
  d.table(495,118,[[T('ID','编号'),'d / nm'],['A2',50],['A3',60]],[100,135],49)
  d.line(270,194,335,194,arrow=True);d.text(380,200,'merge',21,TEAL,anchor='middle');d.line(490,194,425,194,arrow=True)
  d.line(380,218,380,288,arrow=True)
  d.table(180,310,[[T('ID','编号'),'E / GPa','d / nm'],['A2',3,50]],[110,145,145],47)
 elif key=='covariance':
  d=Drawing(T('What the covariance matrix contains','协方差矩阵里有哪些信息？'),T('Teaching covariance for slope m and intercept b','教学示例：斜率 m 与截距 b 的协方差'))
  d.table(30,125,[['','m','b'],['m','0.040','−0.015'],['b','−0.015','0.010']],[70,120,120],60)
  d.text(385,155,T('Diagonal → standard errors','对角元 → 参数标准误'),22,BLUE,weight=600)
  d.text(385,198,'SE(m) = √0.040 = 0.200',21);d.text(385,238,'SE(b) = √0.010 = 0.100',21)
  d.text(385,300,T('Off-diagonal → correlation','非对角元 → 参数相关性'),22,TEAL,weight=600)
  d.text(385,343,'ρ = −0.015 / (0.2 × 0.1)',20);d.text(385,376,'   = −0.75',20)
  d.footer(T('A 95% interval also needs a multiplier and the model assumptions.','95% 置信区间还需要相应分位数与模型假设。'))
 elif key=='data-structures':
  d=Drawing(T('Choose a data structure for the object','根据研究对象选择数据结构'),T('The same project can use arrays, tables and atomic structures.','同一项目可以同时使用数组、带标签的表格与原子结构。'))
  for x,name,col in [(30,'NumPy',BLUE),(275,'pandas',TEAL),(520,'ASE',ORANGE)]:d.rect(x,115,210,282);d.text(x+105,154,name,24,col,anchor='middle',weight=600)
  d.table(50,190,[[1,2,3],[4,5,6]],[55]*3,43,False);d.text(135,350,T('Numeric array','数值数组'),21,anchor='middle')
  d.table(294,184,[['ID','E'],['A1','2.0'],['A2','3.0']],[85]*2,40);d.text(380,350,T('Labeled table','带标签的表格'),21,anchor='middle')
  d.rect(552,185,145,115,'white',ORANGE,0)
  for x,y,s in [(570,207,'C'),(610,264,'O'),(674,220,'H')]:d.circle(x,y,17,s,stroke=ORANGE)
  d.text(625,337,T('Positions + cell','位置 + 晶胞'),20,anchor='middle');d.text(625,367,T('and species','及原子种类'),20,anchor='middle')
 elif key=='segmentation':
  d=Drawing(T('From a binary mask to region areas','从二值掩码到连通区域面积'),T('Teaching pixel grid; one pixel represents s × s in physical units.','教学像素网格；每个像素对应实际尺寸 s × s。'))
  cells={(1,1):1,(1,2):1,(2,1):1,(2,2):1,(4,4):2,(4,5):2,(5,4):2,(5,5):2,(6,4):2,(6,5):2}
  for k,x0 in enumerate([30,295]):
   d.text(x0+108,125,T('Binary mask','二值掩码') if k==0 else T('Labeled regions','区域标记'),21,anchor='middle')
   for r in range(7):
    for c in range(7):
     val=cells.get((r,c),0);fill=(INK if k==0 else BLUE if val==1 else TEAL) if val else 'white';d.rect(x0+c*30,145+r*30,30,30,fill,LINE,0)
  d.line(249,250,283,250,arrow=True)
  d.text(555,202,T('Region A','区域 A'),23,BLUE,weight=600);d.text(555,238,'4 pixels → 4s²',20)
  d.text(555,297,T('Region B','区域 B'),23,TEAL,weight=600);d.text(555,333,'6 pixels → 6s²',20)
  if lang=='zh':d.parts=[p.replace('4 pixels','4 像素').replace('6 pixels','6 像素') for p in d.parts]
  d.footer(T('Scale calibration converts a pixel count into physical area.','标尺校准把像素数转换为实际面积。'))
 elif key=='fiber-features':
  d=Drawing(T('Turn a specimen into a feature row','把一个样品整理成一行特征'),T('Schematic network and teaching values; one row represents one sample.','网络示意与教学数值；一行对应一个样品。'))
  d.rect(30,120,222,210)
  fiber_angles=np.array([-np.sqrt(252),-6,6,np.sqrt(252)])
  assert np.isclose(np.std(fiber_angles),12)
  def fiber_y(i,x): return 160+45*i+(x-141)*np.tan(np.deg2rad(fiber_angles[i]))
  for i in range(4):d.line(46,fiber_y(i,46),236,fiber_y(i,236),BLUE,4)
  for i,x in [(0,110),(1,170),(2,120)]:d.line(x,fiber_y(i,x),x,fiber_y(i+1,x),TEAL,3)
  d.line(262,222,313,222,arrow=True)
  d.table(330,125,[[T('Feature X','特征 X'),T('Value','数值')],[T('Diameter','直径'),'45 nm'],[T('Angle spread','角度离散程度'),'12°'],[T('Crosslink content','交联含量'),'2.5%']],[245,150],47)
  d.rect(330,337,395,53,'#eaf5f2');d.text(527,371,T('Target y: modulus = 2.8 GPa','目标 y：模量 = 2.8 GPa'),21,TEAL,anchor='middle')
  d.footer(T('Keep the measured target separate from all input features.','把待预测的测量目标与所有输入特征分开。'))
 elif key=='bootstrap':
  d=Drawing(T('Bootstrap: resample, fit, compare','Bootstrap：重采样、拟合、比较'),T('Teaching example: repeated sample IDs are allowed within a resample.','教学示例：同一次重采样可以重复抽到同一个样品。'))
  d.text(130,147,T('Original IDs','原样品编号'),21,BLUE,anchor='middle');d.rect(30,176,200,60);d.text(130,214,'A  B  C  D',23,anchor='middle')
  d.line(238,207,291,207,arrow=True)
  d.table(305,117,[[T('Resample','重采样'),T('Prediction','预测值')],['A  A  C  D','2.5'],['B  C  C  D','2.8'],['A  B  D  D','3.1']],[225,190],53)
  d.text(380,377,T('Mean = 2.8; spread across these models ≈ 0.245','均值 = 2.8；这组模型的预测标准差 ≈ 0.245'),22,anchor='middle')
  d.footer(T('Spread uses np.std(..., ddof=0); prediction units are arbitrary.','标准差采用 np.std(..., ddof=0)，预测值为任意单位。'))
 elif key=='one-hot':
  d=Drawing(T('One-hot encoding with a reference level','以一个类别为参照进行独热编码'),T('drop="first": ethanol is the reference in this teaching example.','drop="first"：本教学示例以乙醇为参照类别。'))
  d.table(70,127,[[T('Solvent','溶剂'),T('methanol','甲醇列'),T('water','水列')],[T('ethanol','乙醇'),0,0],[T('methanol','甲醇'),1,0],[T('water','水'),0,1]],[240,190,190],58)
  d.text(380,403,T('A zero row identifies the reference; it is not missing data.','全零行表示参照类别，不表示数据缺失。'),21,TEAL,anchor='middle')
 elif key=='train-scaling':
  d=Drawing(T('Fit preprocessing on training data','预处理参数只从训练数据中计算'),T('Teaching values; population standard deviation as in StandardScaler','教学数值；标准差采用 StandardScaler 的总体标准差定义'))
  d.rect(30,118,330,225);d.text(195,156,T('Training: [2, 4, 6]','训练集：[2, 4, 6]'),23,BLUE,anchor='middle',weight=600)
  d.text(195,205,'mean = 4',23,anchor='middle');d.text(195,246,'std = √(8/3) ≈ 1.633',22,anchor='middle');d.text(195,299,T('Fit once; retain parameters','计算一次，保留参数'),20,anchor='middle')
  d.line(367,231,401,231,arrow=True);d.rect(410,118,320,225);d.text(570,156,T('Test: [8]','测试集：[8]'),23,TEAL,anchor='middle',weight=600)
  d.text(570,213,'z = (8 − 4) / √(8/3)',21,anchor='middle');d.text(570,259,'≈ 2.449',26,TEAL,anchor='middle');d.text(570,303,T('Apply training parameters','沿用训练集参数'),20,anchor='middle')
  d.footer(T('Refitting the scaler on test data changes the coordinate system.','若在测试集重新拟合缩放器，就改变了数据的坐标基准。'))
 else:raise ValueError(key)
 d.save(key,lang)

def quantitative(key,lang):
 T=lambda a,b:choose(lang,a,b)
 fig=plt.figure(figsize=(760/72,500/72),dpi=72)
 if key=='regularization':
  ax=fig.add_axes([.14,.18,.72,.66]);t=np.linspace(0,2*np.pi,361)
  ax.plot(np.cos(t),np.sin(t),color=BLUE,lw=3,label=T('L2: w1² + w2² ≤ 1','L2：w1² + w2² ≤ 1'))
  ax.plot([1,0,-1,0,1],[0,1,0,-1,0],color=TEAL,lw=3,label=T('L1: |w1| + |w2| ≤ 1','L1：|w1| + |w2| ≤ 1'))
  ax.axhline(0,color=LINE,zorder=0);ax.axvline(0,color=LINE,zorder=0);ax.set(xlim=(-1.3,1.3),ylim=(-1.3,1.3),xlabel='w1',ylabel='w2',aspect='equal');fig.legend(*ax.get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.5,.025),frameon=False,fontsize=18)
  fig.suptitle(T('L1 corners and L2 smooth contours','L1 的尖角与 L2 的光滑边界'),fontsize=26,y=.97);ax.set_xticks([-1,0,1]);ax.set_yticks([-1,0,1])
  # Leave room for both legend lines.
  ax.set_position([.25,.34,.5,.52])
 elif key=='svr-tube':
  ax=fig.add_axes([.13,.19,.82,.61]);x=np.linspace(0,4,200);eps=.6
  ax.fill_between(x,x-eps,x+eps,color=BLUE,alpha=.13,label=T('ε tube','ε 容忍带'));ax.plot(x,x,color=BLUE,lw=2,label='f(x) = x')
  xp=np.array([.5,1.5,2.6,3.4]);yp=np.array([.7,2.6,2.3,2.1]);ax.scatter(xp,yp,s=65,color=TEAL,zorder=5)
  for xx,yy in zip(xp,yp):
   if abs(yy-xx)>eps:ax.plot([xx,xx],[yy,xx+np.sign(yy-xx)*eps],color=ORANGE,lw=4)
  ax.set(xlabel='x',ylabel='y',xlim=(0,4),ylim=(-.7,4.7));ax.legend(loc='upper left',frameon=False,fontsize=18)
  fig.suptitle(T('SVR penalizes only error outside the tube','SVR 只惩罚容忍带之外的误差'),fontsize=26,y=.96)
  fig.text(.13,.86,T('Teaching example: ε = 0.6; orange segments incur loss.','教学示例：ε = 0.6；橙色线段对应受惩罚的误差。'),fontsize=18)
  fig.text(.13,.045,'loss = max(0, |y − f(x)| − ε)',fontsize=20)
 elif key=='sigmoid':
  ax=fig.add_axes([.13,.26,.82,.54]);z=np.linspace(-6,6,300);p=1/(1+np.exp(-z));ax.plot(z,p,color=BLUE,lw=3);ax.axhline(.5,color=MUTED,ls='--');ax.axvline(0,color=MUTED,ls='--');ax.fill_between(z,0,p,where=z>=0,color=TEAL,alpha=.10);ax.scatter([0],[.5],color=ORANGE,s=70,zorder=4)
  ax.set(xlabel=T('Linear score z','线性得分 z'),ylabel=T('Probability p','概率 p'),ylim=(0,1.05),xlim=(-6,6));ax.set_yticks([0,.5,1]);ax.set_xticks([-6,-3,0,3,6]);ax.tick_params(axis='x',pad=12)
  fig.suptitle(T('A probability becomes a class decision','由概率得到类别判断'),fontsize=26,y=.96);fig.text(.13,.86,'p = 1 / (1 + exp(−z))',fontsize=21);fig.text(.13,.045,T('At threshold 0.5: predict positive when z ≥ 0.','阈值取 0.5 时：z ≥ 0 判为正类。'),fontsize=20)
 elif key=='residuals':
  x=np.arange(5);y=np.array([1.2,2.8,5.1,6.9,9.]);coef=np.polyfit(x,y,1);pred=np.polyval(coef,x)
  ax=fig.add_axes([.14,.44,.80,.34]);ax.plot(x,pred,color=BLUE,lw=2);ax.scatter(x,y,color=TEAL,s=55,zorder=5)
  for xx,yy,pp in zip(x,y,pred):ax.plot([xx,xx],[yy,pp],color=ORANGE,lw=3)
  ax.set(ylabel=T('Value y','数值 y'),xticks=[0,1,2,3,4]);ax.tick_params(labelbottom=False)
  ar=fig.add_axes([.14,.17,.80,.20]);ar.axhline(0,color=MUTED,lw=1);ar.scatter(x,y-pred,color=ORANGE,s=50);ar.vlines(x,0,y-pred,color=ORANGE);ar.set(xlabel='x',ylabel=T('Residual','残差'),xticks=[0,1,2,3,4],ylim=(-.3,.3),yticks=[-.2,0,.2])
  fig.suptitle(T('A fit and the errors it leaves behind','拟合曲线与剩余误差'),fontsize=26,y=.96);fig.text(.14,.86,T('Teaching data: fitted y = 1.97x + 1.06','教学数据：拟合得到 y = 1.97x + 1.06'),fontsize=19);fig.text(.14,.035,T('Residual = observed y − fitted y','残差 = 观测值 − 拟合值'),fontsize=18)
 elif key=='distribution':
  ax=fig.add_axes([.14,.19,.81,.61]);a=np.arange(1,6);b=np.array([2.8,2.9,3,3.1,3.2]);offset=np.linspace(-.12,.12,5)
  for i,(v,c) in enumerate([(a,BLUE),(b,TEAL)]):ax.scatter(i+offset,v,s=85,color=c,zorder=3);ax.plot([i-.23,i+.23],[np.mean(v)]*2,color=ORANGE,lw=3)
  ax.set(xticks=[0,1],xticklabels=[T('Group A','A 组'),T('Group B','B 组')],ylabel=T('Value (arbitrary units)','数值（任意单位）'),ylim=(.5,5.6),xlim=(-.6,1.6));fig.suptitle(T('The same mean can hide different spreads','同样的均值，可以有不同的离散程度'),fontsize=25,y=.96);fig.text(.14,.86,T('Teaching data: five points per group; both means equal 3.','教学数据：每组 5 个点，两组均值都为 3。'),fontsize=18);fig.text(.14,.045,T('Show individual observations as well as the summary.','展示统计量的同时，也展示每个观测点。'),fontsize=20)
 elif key=='heatmap':
  ax=fig.add_axes([.18,.20,.59,.60]);v=np.array([[1,.7,-.4],[.7,1,-.1],[-.4,-.1,1]]);im=ax.imshow(v,cmap='RdBu_r',vmin=-1,vmax=1)
  for i in range(3):
   for j in range(3):ax.text(j,i,f'{v[i,j]:.1f}',ha='center',va='center',fontsize=24,color='white' if abs(v[i,j])>.6 else INK)
  ax.set(xticks=[0,1,2],yticks=[0,1,2],xticklabels=['A','B','C'],yticklabels=['A','B','C']);cax=fig.add_axes([.82,.20,.035,.60]);fig.colorbar(im,cax=cax,ticks=[-1,0,1]);fig.suptitle(T('Use a diverging scale for signed correlation','正负相关：以零为中心的发散色阶'),fontsize=25,y=.96);fig.text(.12,.86,T('Teaching correlation matrix; the full scale is −1 to +1.','教学相关矩阵；色阶固定为 −1 至 +1。'),fontsize=18);fig.text(.12,.045,T('Neutral color marks zero; numbers make the values explicit.','中性色表示零，数值标注给出具体相关系数。'),fontsize=19)
 else:raise ValueError(key)
 figpath=OUT/f'comp-guide-{key}-{lang}.svg'
 fig.savefig(figpath,format='svg',metadata={'Creator':'ml-biomat teaching illustrations','Date':None});plt.close(fig)
 svg=figpath.read_text('utf-8').replace("font-family: 'Microsoft YaHei'","font-family: 'Microsoft YaHei', 'Noto Sans SC', sans-serif")
 figpath.write_text(svg,'utf-8')

NATIVE=['environment-isolation','jupyter-kernel','neuron','gradient-step','confusion-matrix','adjacency','weighted-path','boolean-mask','broadcasting','groupby','merge','covariance','data-structures','segmentation','fiber-features','bootstrap','one-hot','train-scaling']
QUANT=['regularization','svr-tube','sigmoid','residuals','distribution','heatmap']

# File names, topic anchors, localized captions and search summaries.
ARTICLES = [
 dict(en='python-env-setup.md',zh='python-env-setup.md',keys=['environment-isolation','jupyter-kernel'],
  anchors_en=['4. Creating and Managing Virtual Environments','6. JupyterLab'],anchors_zh=['四、创建与管理虚拟环境','六、JupyterLab'],
  caps_en=['Each project keeps its own Python interpreter and package versions. The version labels are schematic; activating an environment chooses which installation a command will use.','The browser displays the notebook, while the selected kernel executes its cells. Check sys.executable inside a cell to identify the Python installation and locate packages in the correct environment.'],
  caps_zh=['每个项目分别保存自己的 Python 解释器与依赖版本。图中的版本代号用于说明隔离关系；激活环境决定命令调用哪一套安装。','浏览器负责显示 Notebook，选中的内核负责执行代码。在单元格中查看 sys.executable，可以确认实际使用的 Python，再到对应环境安装工具包。'],
  desc_en='Set up isolated Python environments, install the scientific stack, and connect the right interpreter to JupyterLab and VS Code. Learn how to diagnose package conflicts and reproduce a working setup.',
  desc_zh='从独立环境、工具包安装到 JupyterLab 内核与 VS Code 解释器，逐步建立可复用的科研计算环境。结合版本冲突、安装路径与环境导出示例，说明常见故障该从哪里排查。'),
 dict(en='regression-models.md',zh='regression-models-zh.md',keys=['regularization','svr-tube'],
  anchors_en=['3. Ridge and Lasso','5. Support Vector Regression'],anchors_zh=['三、岭回归与 Lasso','五、支持向量回归'],
  caps_en=['These unit-radius constraint regions show the geometry behind L1 and L2 regularization. L1 has corners on the coordinate axes, which helps explain why its solutions can contain exactly zero coefficients.','For the teaching function f(x) = x and a fixed epsilon of 0.6, points inside the shaded tube incur no epsilon-insensitive loss. Orange segments show only the portion of an error that exceeds epsilon.'],
  caps_zh=['图中为单位尺度下的 L1 与 L2 约束区域。L1 边界在坐标轴上有尖角，有助于理解为什么它容易得到部分系数恰好为零的解。','教学示例取 f(x) = x、固定 ε = 0.6。容忍带内的点不产生 ε 不敏感损失；橙色线段只表示误差超过 ε 的部分。'],
  desc_en='Compare linear regression, regularization, kernel methods, tree ensembles, and boosting through their assumptions and fitting behavior. Use residuals, cross-validation, and suitable error metrics to select a model for numerical prediction.',
  desc_zh='沿着线性回归、正则化、核方法、树集成与梯度提升，理解各类回归模型如何表达输入和数值目标之间的关系。结合残差、交叉验证与误差指标，判断模型复杂度并选择适合数据的方案。'),
 dict(en='deep-learning-intro.md',zh='deep-learning-intro-zh.md',keys=['neuron','gradient-step'],
  anchors_en=['2. The Basic Components','4. Backpropagation and Gradient Descent'],anchors_zh=['二、神经网络的基本构件','四、反向传播与梯度下降'],
  caps_en=['A neuron multiplies each input by its weight, adds the bias, and applies an activation. This numerical example gives z = 0.2 and ReLU(z) = 0.2, making each operation visible.','This one-parameter teaching model shows how an error produces a gradient and a weight update. With learning rate 0.1, the update changes w from 0.25 to 0.35 and reduces the squared-error loss from 0.125 to 0.045.'],
  caps_zh=['一个神经元先将输入乘以权重，加上偏置，再通过激活函数。这个数值示例得到 z = 0.2、ReLU(z) = 0.2，可以逐项核对每一步运算。','这个单参数教学模型展示误差如何产生梯度并更新权重。学习率取 0.1 时，w 从 0.25 变为 0.35，平方误差损失由 0.125 降至 0.045。'],
  desc_en='Follow a neural network from weighted inputs and activations to loss functions, backpropagation, and optimization. Connect these operations to convolutional, recurrent, and attention models, with practical guidance on training and small datasets.',
  desc_zh='从神经元的加权求和与激活函数出发，逐步理解前向传播、损失函数、反向传播和梯度更新。再联系卷积、序列与注意力模型，讨论正则化、迁移学习及小样本研究中的选用方法。'),
 dict(en='networkx-fundamentals.md',zh='networkx-fundamentals-zh.md',keys=['adjacency','weighted-path'],
  anchors_en=['3. Building Graphs','6. Shortest-Path Algorithms'],anchors_zh=['三、构建图','六、最短路径算法'],
  caps_en=['The four-node graph and matrix encode the same edges in the order A, B, C, D. In this undirected graph the matrix is symmetric, and the sum of row C gives its degree of three.','A shortest path depends on the quantity being minimized. In this teaching graph, the direct A–D edge uses one hop, while A–B–D has the lowest total weight, 1 + 2 = 3.'],
  caps_zh=['四节点图和矩阵按 A、B、C、D 的顺序记录同一组连边。无向图的邻接矩阵对称，C 行元素之和为 3，对应节点 C 的度数。','最短路径取决于要最小化的量。在这个教学网络中，直接走 A–D 只需一跳；按边权求和时，A–B–D 的总权重为 1 + 2 = 3，更小。'],
  desc_en='Represent nodes, edges, directions, and weights in NetworkX, then calculate degree, centrality, clustering, and shortest paths. Compare graph models and community methods while keeping the meaning of each network metric explicit.',
  desc_zh='用 NetworkX 表达节点、连边、方向与权重，再计算度数、中心性、聚类和最短路径。结合邻接矩阵、经典网络模型与社区发现，说明不同指标回答什么问题，以及如何把结构数据转成可分析的图。'),
 dict(en='ml-classification-models.md',zh='ml-classification-models-zh.md',keys=['sigmoid','confusion-matrix'],
  anchors_en=['2. Logistic Regression','8. Evaluation Metrics'],anchors_zh=['二、逻辑回归','八、评估指标'],
  caps_en=['Logistic regression maps the linear score z to a probability through the sigmoid function. A threshold of 0.5 corresponds to z = 0; changing the threshold changes the class decision without changing the fitted probabilities.','The 20 teaching predictions contain eight true positives, nine true negatives, two false positives, and one false negative. Precision, recall, and accuracy use different denominators and therefore answer different questions.'],
  caps_zh=['逻辑回归通过 sigmoid 函数，把线性得分 z 映射为概率。概率阈值 0.5 对应 z = 0；改变阈值会改变分类结果，但不会改变模型给出的概率。','这组教学数据包含 8 个真阳性、9 个真阴性、2 个假阳性和 1 个假阴性。精确率、召回率与准确率采用不同分母，分别回答不同的评价问题。'],
  desc_en='Compare logistic regression, support vector machines, trees, ensembles, nearest neighbors, and naive Bayes. Read class probabilities and confusion matrices, then choose metrics and validation procedures that match the cost of classification errors.',
  desc_zh='比较逻辑回归、支持向量机、决策树、集成模型、近邻与朴素贝叶斯的判断方式。结合概率阈值、混淆矩阵和交叉验证，理解分类错误的类型，并按实际问题选择评价指标与模型。'),
 dict(en='scipy-curve-fitting.md',zh='scipy-curve-fitting.md',keys=['residuals','covariance'],
  anchors_en=['2. Linear Regression','6. Confidence Intervals'],anchors_zh=['二、线性回归','五、置信区间'],
  caps_en=['The five teaching points are fitted by y = 1.97x + 1.06. The lower panel shows observed minus fitted values, separating the remaining errors from the trend so that their signs and magnitudes are easy to compare.','This illustrative covariance matrix gives standard errors of 0.2 for the slope and 0.1 for the intercept, with correlation −0.75. Converting these standard errors into confidence intervals also requires a confidence level and an appropriate model-based multiplier.'],
  caps_zh=['五个教学数据点拟合得到 y = 1.97x + 1.06。下图将观测值减去拟合值，使剩余误差脱离整体趋势，便于比较残差的正负与大小。','该教学协方差矩阵给出斜率标准误 0.2、截距标准误 0.1，以及参数相关系数 −0.75。计算置信区间还需指定置信水平，并结合模型选取相应的分位数。'],
  desc_en='Fit linear trends, stress relaxation, and indentation models with SciPy while tracking parameter units and initial guesses. Interpret residuals, covariance matrices, and confidence intervals to turn a fitted curve into an inspectable physical calculation.',
  desc_zh='从线性趋势、应力松弛到压痕模型，演示 SciPy 曲线拟合中的函数定义、初值、单位与参数边界。通过残差、协方差矩阵和置信区间，理解拟合参数的含义，并检查模型与测量数据是否匹配。'),
 dict(en='scientific-visualization.md',zh='scientific-visualization-python-zh.md',keys=['distribution','heatmap'],
  anchors_en=['1. Multi-Panel Figure Template','3. Heatmaps for Matrix Data'],anchors_zh=['四、统计图表','五、色彩方案'],
  caps_en=['Both teaching groups have a mean of three, yet their observations have very different spreads. Showing the five points in each group makes this difference visible; a bar chart of means alone would hide it.','This teaching correlation matrix uses a diverging scale centered at zero and fixed to the full −1 to +1 range. Numeric labels allow exact comparisons without relying on color alone.'],
  caps_zh=['两个教学组的均值都为 3，但观测值的离散程度不同。展示每组的五个数据点，就能看见只画均值柱状图时容易遗漏的差异。','这个教学相关矩阵使用以零为中心、范围固定为 −1 至 +1 的发散色阶。数值标注便于准确比较，也减少了对颜色辨识的依赖。'],
  desc_en='Build readable line plots, distributions, heatmaps, and multi-panel figures with Matplotlib and Seaborn. Match visual encodings to the data, keep units and uncertainty visible, and export figures at the dimensions needed for a manuscript.',
  desc_zh='使用 Matplotlib 与 Seaborn 绘制折线、散点、分布、热图和多幅子图，理解图形选择如何影响读者对数据的判断。结合配色、单位、不确定性、版面尺寸与导出设置，完成可直接用于论文排版的图表。'),
 dict(en='python-tools-materials.md',zh='python-tools-materials-research-zh.md',keys=['data-structures','segmentation'],
  anchors_en=['The Core Stack','Image Analysis for Microscopy'],anchors_zh=['核心科学计算栈','六、scikit-image'],
  caps_en=['Arrays hold numerical measurements, DataFrames attach labels to observations, and atomic structures combine species, positions, and a simulation cell. Choosing the representation first makes it easier to select the appropriate library and calculation.','The binary teaching mask contains separate regions of four and six pixels. Connected-component labeling identifies them; a calibrated pixel length s converts their areas to 4s² and 6s². The grid is a schematic, not a microscope image.'],
  caps_zh=['数组适合保存数值测量，DataFrame 为观测值附上列名和样品标签，原子结构则同时保存种类、坐标与晶胞。先确定数据表示，再选择相应工具与计算方法。','这个教学二值掩码包含分别由 4 个和 6 个像素构成的独立区域。连通区域标记将它们区分开，标定后的像素长度 s 则把面积转换为 4s² 与 6s²。网格为示意图。'],
  desc_en='Connect NumPy, SciPy, pandas, plotting libraries, atomistic tools, and image analysis to common materials-research tasks. Follow examples of force-curve processing, grouped statistics, microscopy segmentation, and predictive modeling.',
  desc_zh='围绕材料研究中的数据对象，连接 NumPy、SciPy、pandas、绘图、原子结构和图像分析工具。通过力曲线处理、分组统计、显微图像分割与机器学习示例，说明各工具在实际分析中的分工与衔接。'),
 dict(en='pandas-materials-data.md',zh='pandas-materials-data.md',keys=['groupby','merge'],
  anchors_en=['Group Statistics','Advanced Data Operations'],anchors_zh=['三、分组统计','四、数据合并'],
  caps_en=['Grouping the four teaching measurements by condition gives means of 3 GPa for A and 7 GPa for B, with two samples in each group. Keeping the sample count beside the mean helps readers interpret each summary.','An inner join on sample ID connects the mechanics and morphology tables. Only A2 appears in both teaching tables, so the resulting row contains its modulus of 3 GPa and diameter of 50 nm.'],
  caps_zh=['将四条教学测量按条件分组，A 组均值为 3 GPa，B 组为 7 GPa，各有两个样本。把样本数与均值一起保留，可以让汇总结果更容易解释。','按样品编号进行内连接，把力学表和形貌表对应起来。两张教学表只有 A2 共同出现，合并后得到它的模量 3 GPa 与直径 50 nm。'],
  desc_en='Organize experimental records with DataFrames, clean missing or inconsistent values, and summarize repeated measurements by condition. Merge related tables by sample identity and export results while retaining the labels needed for later analysis.',
  desc_zh='用 DataFrame 整理实验记录，处理缺失值、列名与异常数据，再按实验条件汇总重复测量。结合样品编号合并、数据透视和结果导出，保留样品与测量之间的对应关系，方便继续绘图和建模。'),
 dict(en='numpy-crash-course.md',zh='numpy-crash-course.md',keys=['boolean-mask','broadcasting'],
  anchors_en=['5. Boolean Indexing','6. Reshaping and Combining'],anchors_zh=['六、布尔索引','四、向量化运算'],
  caps_en=['The same Boolean mask selects matching entries from the strain and stress arrays. In this teaching subset, strain < 0.02 retains the first three observations and excludes the entry exactly equal to 0.02.','Subtracting mean(axis=0) centers each column of this teaching array. NumPy broadcasts the three column means across both rows, producing zero column means without writing a loop.'],
  caps_zh=['同一个布尔掩码用于应变和应力数组时，会保留彼此对应的观测值。这个教学子集中，strain < 0.02 保留前三项，排除恰好等于 0.02 的一项。','对这个教学数组减去 mean(axis=0)，即可逐列中心化。NumPy 将三个列均值广播到两行，得到列均值为零的新数组，无需逐行编写循环。'],
  desc_en='Load experimental measurements into arrays and work with slicing, Boolean masks, broadcasting, and summary statistics. Use these operations to align observations, center columns, fit simple relationships, and save processed numerical results.',
  desc_zh='把实验测量整理为数组，逐步使用切片、布尔筛选、广播运算和统计聚合。通过应变与应力数据、逐列中心化及简单拟合示例，理解形状和索引如何影响计算，并将处理结果保存为后续分析可用的数据。'),
 dict(en='ml-predict-fiber-mechanics.md',zh='ml-fiber-biomaterials.md',keys=['fiber-features','bootstrap'],
  anchors_en=['Data Preparation','Uncertainty Quantification'],anchors_zh=['典型的数据长什么样','第四步：不确定性'],
  caps_en=['The schematic links a fiber specimen to one row of descriptive features and a separately measured target. The numbers are teaching values; diameter, orientation spread, and crosslink content do not by themselves determine a unique modulus.','Each bootstrap sample draws training observations with replacement and fits a new model. The three teaching predictions have mean 2.8 and standard deviation about 0.245; this summarizes variation across the fitted models, while prediction-interval calibration is a separate evaluation step.'],
  caps_zh=['示意图把一个纤维样品对应到一行描述特征，以及单独测量的预测目标。图中为教学数值；直径、取向离散程度和交联含量共同作为输入，用于学习与模量之间的关系。','每个 Bootstrap 样本都从训练观测中有放回抽样，再拟合一个模型。三次教学预测的均值为 2.8、标准差约为 0.245，概括了这组模型之间的预测波动；预测区间的覆盖率可进一步通过独立数据评估。'],
  desc_en='Build a small-data regression workflow for fiber mechanics, from specimen features and preprocessing to model comparison. Examine cross-validation, bootstrap variation, and feature importance to connect numerical predictions with material descriptors.',
  desc_zh='从纤维样品的结构与制备特征出发，组织小样本回归的数据准备、预处理、模型比较与评价。结合交叉验证、Bootstrap 波动和特征重要性，理解数值预测如何与材料描述对应，并安排后续验证。'),
 dict(en='feature-engineering-materials.md',zh='feature-engineering-materials.md',keys=['one-hot','train-scaling'],
  anchors_en=['Encoding Categorical Variables','Checklist'],anchors_zh=['分类变量编码','深入探讨：特征缩放'],
  caps_en=['With ethanol as the reference level, the two indicator columns distinguish three solvents. The all-zero row is a valid category representation; it does not mean the sample has missing information.','This teaching scaler learns mean 4 and standard deviation √(8/3) from training values [2, 4, 6]. Applying those same parameters transforms the test value 8 to approximately 2.449, preserving one shared coordinate system.'],
  caps_zh=['以乙醇为参照类别时，两列指示变量即可区分三种溶剂。全零行是有效的类别表示，并不意味着该样品的信息缺失。','这个教学缩放器从训练值 [2, 4, 6] 得到均值 4 和标准差 √(8/3)。将同一组参数用于测试值 8，结果约为 2.449，从而让训练与测试数据处于一致的坐标基准。'],
  desc_en='Construct useful material descriptors, encode categorical processing conditions, and handle interactions and missing values. Learn how feature selection and training-only preprocessing keep a small-data model interpretable and its evaluation consistent.',
  desc_zh='从材料描述符与制备条件构造特征矩阵，处理分类变量、物理交互项和缺失信息。结合小样本特征选择与训练集内的缩放方法，说明怎样保留变量含义、避免目标泄漏，并让模型评价保持一致。'),
]

def insert_articles(articles=None):
 for item in (ARTICLES if articles is None else articles):
  for lang in ['en','zh']:
   path=ROOT/'content/posts'/lang/item[lang]
   original=path.read_text('utf-8'); text=original
   desc=item['desc_'+lang]
   assert len(desc)>=(150 if lang=='en' else 60), (path,len(desc))
   text,n=re.subn(r'^description: .*$', 'description: "'+desc+'"',text,count=1,flags=re.M)
   assert n==1,path
   for key,anchor,caption in zip(item['keys'],item['anchors_'+lang],item['caps_'+lang]):
    url=f'/static/images/article-guides/comp-guide-{key}-{lang}.svg'
    # The site's Markdown image parser does not accept nested square brackets.
    alt=caption.split('. ')[0].split('。')[0].replace('[','(').replace(']',')')
    if url in text:
     pattern=r'^!\[[^\n]*\]\('+re.escape(url)+r'\)$'
     text, repaired=re.subn(pattern,lambda _: '!['+alt+']('+url+')',text,flags=re.M)
     assert repaired==1,(path,url,'Expected one existing image line')
     continue
    matches=list(re.finditer(r'^#{2,3} [^\n]*'+re.escape(anchor)+r'[^\n]*$',text,re.M))
    assert len(matches)==1,(path,anchor,len(matches))
    match=matches[0]
    text=text[:match.end()]+'\n\n!['+alt+']('+url+')\n\n'+caption+'\n'+text[match.end():]
   # Confirm every original fenced code block remains byte-for-byte unchanged.
   assert re.findall(r'```.*?```',original,re.S)==re.findall(r'```.*?```',text,re.S),path
   path.write_text(text,'utf-8')

if __name__=='__main__':
 for lang in ['en','zh']:
  for key in NATIVE:native(key,lang)
  for key in QUANT:quantitative(key,lang)
 insert_articles()
 print('Generated 48 bilingual explanatory SVGs and updated 24 article introductions/captions.')
