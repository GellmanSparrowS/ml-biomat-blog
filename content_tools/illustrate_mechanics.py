"""Deterministic bilingual explanatory SVGs for twelve biomaterials articles.

All drawings are teaching schematics. Analytic curves use the equations and
parameters printed in their figures/captions; no experimental data are generated.
Run from the repository: python -B content_tools/illustrate_mechanics.py
Only mech-*.svg and the 24 explicitly listed source posts are touched.
"""
from pathlib import Path
from html import escape
import math
import re
import unicodedata
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'static/images/article-guides'
BLUE, TEAL, ORANGE = '#2563eb', '#087f75', '#c46818'
INK, MUTED, GRID, PALE = '#182f43', '#486174', '#dce5ec', '#eaf1f7'


class SVG:
    def __init__(self, lang, title, subtitle, height=540):
        self.lang, self.h = lang, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="{height}" viewBox="0 0 760 {height}" role="img" aria-labelledby="title desc" xml:lang="{lang}">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="context-stroke"/></marker></defs>',
            '<style>text{font-family:"Microsoft YaHei","Noto Sans SC","Noto Sans CJK SC",Arial,sans-serif;fill:#182f43}path,line,polyline{stroke-linecap:round;stroke-linejoin:round}</style>',
            f'<rect x="1" y="1" width="758" height="{height-2}" rx="16" fill="#f8fafc" stroke="{GRID}"/>']
        self.text(30, 42, title, 27, weight=700)
        self.wrap(30, 72, subtitle, 698, size=18, fill=MUTED)

    def t(self, en, zh): return zh if self.lang == 'zh' else en
    def text(self, x, y, s, size=20, fill=INK, anchor='start', weight=400):
        self.parts.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{fill}" style="fill:{fill}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(s))}</text>')
    def wrap(self, x, y, s, width=320, size=20, fill=INK, anchor='start', weight=400, leading=None):
        # Conservative glyph estimates; browser bounding boxes are checked separately.
        leading = leading or size*1.4
        tokens = list(s) if self.lang == 'zh' else re.findall(r'\S+\s*', s)
        lines, line, used = [], '', 0
        for token in tokens:
            w = sum(size*(1 if unicodedata.east_asian_width(c) in 'WF' else .56) for c in token)
            if line and used+w > width: lines.append(line.rstrip()); line, used = '', 0
            line += token; used += w
        if line: lines.append(line.rstrip())
        for i, line in enumerate(lines): self.text(x, y+i*leading, line, size, fill, anchor, weight)
    def line(self, x1, y1, x2, y2, color=MUTED, width=2, dash=None, arrow=False, both=False):
        extras = (f' stroke-dasharray="{dash}"' if dash else '') + (' marker-end="url(#arrow)"' if arrow or both else '') + (' marker-start="url(#arrow)"' if both else '')
        self.parts.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{width}"{extras}/>')
    def path(self, points, color=BLUE, width=3, fill='none', closed=False, dash=None):
        d = 'M'+' L'.join(f'{x:.3f},{y:.3f}' for x,y in points)+(' Z' if closed else '')
        self.parts.append(f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="{fill}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def circle(self, x, y, r, fill=BLUE, stroke='none', width=2):
        self.parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    def rect(self, x, y, w, h, fill=PALE, stroke=GRID, radius=8):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    def wave(self, x, y, w, a=10, cycles=3, color=BLUE, width=4):
        self.path([(x+w*i/100, y+a*math.sin(2*math.pi*cycles*i/100)) for i in range(101)],color,width)
    def note(self, en, zh, y=None): self.wrap(30, y or self.h-48, self.t(en,zh), 698, 18, MUTED)
    def finish(self):
        result='\n'.join(self.parts+['</svg>'])+'\n'
        ET.fromstring(result)
        return result


def axes(s, xr, yr, xlabel, ylabel, x=86, y=143, w=585, h=250, xticks=None, yticks=None):
    X=lambda v:x+(v-xr[0])/(xr[1]-xr[0])*w
    Y=lambda v:y+h-(v-yr[0])/(yr[1]-yr[0])*h
    for v in yticks or [yr[0],(yr[0]+yr[1])/2,yr[1]]:
        s.line(x,Y(v),x+w,Y(v),GRID,1)
        s.text(x-12,Y(v)+6,f'{v:g}',18,MUTED,'end')
    for v in xticks or [xr[0],(xr[0]+xr[1])/2,xr[1]]:
        s.line(X(v),y+h,X(v),y+h+6,MUTED)
        s.text(X(v),y+h+28,f'{v:g}',18,MUTED,'middle')
    s.line(x,y,x,y+h,MUTED);s.line(x,y+h,x+w,y+h,MUTED)
    s.text(x,y-22,ylabel,20)
    s.text(x+w/2,y+h+60,xlabel,20,anchor='middle')
    return X,Y


def curve(s,X,Y,fun,a,b,color=BLUE,n=160):
    pts=[(X(a+(b-a)*i/n),Y(fun(a+(b-a)*i/n))) for i in range(n+1)]
    assert all(math.isfinite(v) for p in pts for v in p)
    s.path(pts,color,4)


def coarse_centers(lang):
    s=SVG(lang, 'From atom groups to bead centers' if lang=='en' else '从原子分组到珠子质心',
          'A constructed mapping retains connectivity and assigns one center per group.' if lang=='en' else '构造映射：每组原子对应一个质心，链连接关系随映射保留。')
    groups=[[(72,200),(98,170),(120,209),(100,238)],[(220,230),(240,200),(266,230),(246,267)],[(355,192),(378,160),(401,192),(380,224)]]
    centers=[(sum(x for x,y in g)/4,sum(y for x,y in g)/4) for g in groups]
    s.text(30,134,s.t('Equal-mass example','等质量原子示例'),22,weight=700)
    for g,c,col in zip(groups,centers,[BLUE,TEAL,ORANGE]):
        s.circle(*c,48,'#edf3f8',col,1)
        s.path(g,col,3)
        for p in g:s.circle(*p,8,col)
        s.circle(*c,4,INK)
    s.line(*centers[0],*centers[1],MUTED,2,dash='4 6');s.line(*centers[1],*centers[2],MUTED,2,dash='4 6')
    s.line(442,220,490,220,MUTED,3,arrow=True)
    beads=[(530,210),(600,255),(686,195)]
    s.path(beads,MUTED,5)
    for p,col in zip(beads,[BLUE,TEAL,ORANGE]):s.circle(*p,19,col)
    s.text(503,134,s.t('Bead chain','珠子链'),22,weight=700)
    s.text(380,354,'R = Σ(mᵢrᵢ) / Σmᵢ',28,anchor='middle')
    s.wrap(65,404,s.t('Mass-weighted position; bead type carries the chosen chemistry.','质量加权位置；珠子类型编码所需的化学差异。'),630,21)
    s.note('Atomic mapping groups and their mass-weighted centers.','原子分组与对应的质量加权中心。')
    return s


def coarse_potential(lang):
    s=SVG(lang,'A distribution defines an effective potential' if lang=='en' else '由分布理解有效势',
          'One-dimensional Cartesian coordinate q; analytic teaching example.' if lang=='en' else '一维笛卡尔坐标 q 的解析教学示例。')
    # Independent scales are deliberately placed in separate panels.
    X,Y=axes(s,(-3,3),(0,.4),'q','p(q)',x=65,y=185,w=270,h=185,xticks=[-3,0,3],yticks=[0,.2,.4])
    curve(s,X,Y,lambda q:math.exp(-q*q/2)/math.sqrt(2*math.pi),-3,3,TEAL)
    X2,Y2=axes(s,(-3,3),(0,4.5),'q','U(q) / kBT',x=435,y=185,w=270,h=185,xticks=[-3,0,3],yticks=[0,2.25,4.5])
    curve(s,X2,Y2,lambda q:q*q/2,-3,3,BLUE)
    s.text(185,130,'p(q) = exp(−q²/2) / √(2π)',18,TEAL,'middle')
    s.text(585,130,'U(q) / kBT = q²/2',20,BLUE,'middle')
    s.text(380,467,'U(q) = −kBT ln p(q) + C',24,anchor='middle')
    return s


def testing_geometry(lang):
    s=SVG(lang,'Measure strain inside the gauge section' if lang=='en' else '在标距段内测量应变',
          'Optical markers separate specimen extension from fixture motion.' if lang=='en' else '用光学标记区分试样伸长与装夹系统的位移。')
    s.rect(80,145,235,250,'#e5f3f8','#9dbbc7')
    s.text(550,440,s.t('Controlled hydration','受控水合环境'),20,anchor='middle')
    s.rect(163,164,65,220,'#d4e4ef',BLUE,3)
    s.rect(139,135,113,44,'#758a9d',INK,3);s.rect(139,370,113,44,'#758a9d',INK,3)
    s.line(196,130,196,102,ORANGE,3,arrow=True);s.line(196,416,196,451,ORANGE,3,arrow=True)
    s.circle(195,220,6,ORANGE);s.circle(195,326,6,ORANGE)
    s.line(268,220,268,326,ORANGE,2,both=True);s.text(282,278,'L₀',22,ORANGE)
    s.line(199,220,264,220,MUTED,1,dash='4 5');s.line(199,326,264,326,MUTED,1,dash='4 5')
    s.rect(390,158,320,72,'#e9f3ed','#b5d7c7');s.text(550,202,'ε = ΔLmarkers / L₀',24,TEAL,'middle')
    s.wrap(390,275,s.t('Crosshead motion includes:','横梁位移包含：'),315,21,weight=700)
    for y,en,zh in [(315,'specimen extension','试样伸长'),(350,'fixture compliance','机架与夹具柔度'),(385,'grip slip and seating','夹持滑移与装夹就位')]:
        s.circle(400,y-6,4,ORANGE);s.text(416,y,s.t(en,zh),20)
    s.note('Track two markers in the same gauge region throughout the test.','全程跟踪同一标距段内的两个标记点。')
    return s


def testing_bias(lang):
    s=SVG(lang,'Diameter error propagates into modulus' if lang=='en' else '直径误差如何传到模量',
          'Circular section; force and strain are held fixed in this calculation.' if lang=='en' else '圆形截面；此计算保持力和应变测量不变。')
    X,Y=axes(s,(.8,1.2),(.6,1.6),s.t('Reported / true diameter','报告直径 / 真实直径'),s.t('Reported / true modulus','报告模量 / 真实模量'),xticks=[.8,.9,1,1.1,1.2],yticks=[.6,1,1.4,1.6])
    curve(s,X,Y,lambda r:1/r**2,.8,1.2)
    s.line(X(.8),Y(1),X(1.2),Y(1),TEAL,2,dash='6 5')
    s.circle(X(1.1),Y(1/1.21),6,ORANGE)
    s.line(X(1.1),Y(1/1.21)-8,535,270,ORANGE)
    s.text(440,227,s.t('+10% diameter','直径高估 10%'),20,ORANGE)
    s.text(440,255,s.t('−17.4% modulus','模量低估 17.4%'),20,ORANGE)
    s.note('Ereported / Etrue = (dtrue / dreported)²; A = πd²/4.','E报告 / E真实 = (d真实 / d报告)²；A = πd²/4。')
    return s


def auxetic(lang):
    s=SVG(lang,'Rotation can expand both directions' if lang=='en' else '转动使两个方向同时展开',
          'Ideal rotating squares: rigid panels joined at their corners.' if lang=='en' else '理想旋转方块：刚性面板通过角点铰接。')
    for cx,theta,col,lab in [(200,5,BLUE,s.t('θ = 5°','θ = 5°')),(560,30,TEAL,s.t('θ = 30°','θ = 30°'))]:
        a=math.radians(theta);side=83;pitch=side*(math.cos(a)+math.sin(a))
        for row in range(2):
            for coln in range(2):
                angle=a*(-1 if (row+coln)%2 else 1);c,sn=math.cos(angle),math.sin(angle)
                x=cx+(coln-.5)*pitch;y=265+(row-.5)*pitch
                pts=[(x+dx*c-dy*sn,y+dx*sn+dy*c) for dx,dy in [(-side/2,-side/2),(side/2,-side/2),(side/2,side/2),(-side/2,side/2)]]
                s.path(pts,col,2,'#dcecf2',True)
                for p in pts:s.circle(*p,3,ORANGE)
        s.text(cx,135,lab,23,anchor='middle',weight=700)
        s.line(cx-pitch,395,cx+pitch,395,col,2,both=True)
        s.text(cx,427,s.t('Period ∝ cosθ + sinθ','周期 ∝ cosθ + sinθ'),19,col,'middle')
    s.line(348,260,407,260,ORANGE,3,arrow=True)
    s.text(380,466,s.t('Ideal mechanism: εx = εy  →  ν = −1','理想机构：εx = εy  →  ν = −1'),23,anchor='middle')
    return s


def lattice_scaling(lang):
    s=SVG(lang,'Density and deformation mode' if lang=='en' else '密度与变形模式共同决定刚度',
          'Analytic density scaling with the geometric factor C = 1.' if lang=='en' else '取 C = 1 的解析标度对比，展示指数的作用。')
    X,Y=axes(s,(0,1),(0,1),s.t('Relative density  ρ* / ρs','相对密度 ρ* / ρs'),s.t('Relative modulus  E* / Es','相对模量 E* / Es'),xticks=[0,.25,.5,.75,1],yticks=[0,.25,.5,.75,1])
    curve(s,X,Y,lambda r:r,0,1,BLUE);curve(s,X,Y,lambda r:r*r,0,1,TEAL)
    s.text(110,182,s.t('n = 1: stretching model','n = 1：拉伸主导模型'),20,BLUE)
    s.text(110,212,s.t('n = 2: bending model','n = 2：弯曲主导模型'),20,TEAL)
    s.note('E* / Es = C(ρ* / ρs)ⁿ; real C and n depend on architecture and load.','E* / Es = C(ρ* / ρs)ⁿ；实际 C 和 n 随结构与载荷而变。')
    return s


def collagen_hierarchy(lang):
    s=SVG(lang,'Collagen: organization across scales' if lang=='en' else '胶原：跨尺度的组织结构',
          'Nested structural levels; the drawings are not to a common scale.' if lang=='en' else '从三股螺旋到原纤维束；各层级采用示意比例。')
    for x,en,zh in [(145,'Triple helix','三股螺旋'),(390,'Staggered packing','错位排列'),(632,'Fibril bundle','原纤维束')]:s.text(x,135,s.t(en,zh),21,anchor='middle',weight=700)
    for phase,col in [(0,BLUE),(2*math.pi/3,TEAL),(4*math.pi/3,ORANGE)]:
        s.path([(55+i*1.7,252+28*math.sin(i*.13+phase)) for i in range(101)],col,5)
    for row in range(5):
        for n in range(2):
            xx=295+row*11+n*90
            s.line(xx,196+row*27,min(xx+78,487),196+row*27,[BLUE,TEAL][row%2],8)
    for xx in [355,397,439]:s.line(xx,178,xx,329,GRID,9)
    for j in range(6):
        s.wave(550,185+j*27,160,3,2,TEAL,10)
        for xx in [575,605,635,665,695]:s.line(xx,180+j*27,xx,190+j*27,'#9bc9c1',3)
    s.line(240,250,276,250,MUTED,2,arrow=True);s.line(505,250,535,250,MUTED,2,arrow=True)
    s.wrap(44,378,s.t('Molecular conformation','分子构象'),195,20)
    s.wrap(285,378,s.t('Axial offset gives banding','轴向错位产生条带'),205,20)
    s.wrap(545,378,s.t('Bundles transfer load','成束结构传递载荷'),190,20)
    s.note('Chemical structure, molecular packing and bundle geometry are distinct levels.','分子构象、分子排列与成束几何属于不同结构层级。')
    return s


def nacre_crack(lang):
    s=SVG(lang,'Nacre: interfaces redirect a crack' if lang=='en' else '珍珠层：界面使裂纹改变路径',
          'Brick-and-mortar schematic of platelet sliding and crack deflection.' if lang=='en' else '砖泥结构中的片晶滑移与裂纹偏转示意。')
    s.rect(65,155,630,215,'#d4ece7','#a3cfc6',0)
    for row in range(4):
        for col in range(5):
            x=65+col*132-(66 if row%2 else 0)
            left,right=max(65,x),min(695,x+118)
            if right>left:s.rect(left,162+row*52,right-left,38,'#d4e3f3','#8ca7c0',3)
    crack=[(65,206),(180,206),(180,214),(246,214),(246,258),(380,258),(380,310),(510,310)]
    s.path(crack,ORANGE,5)
    s.line(515,300,562,300,ORANGE,3,arrow=True)
    s.text(67,133,s.t('Stiff platelets','刚性片晶'),21,BLUE)
    s.text(465,133,s.t('Compliant interlayers','柔性层间基质'),21,TEAL)
    s.line(612,138,612,208,TEAL,2,arrow=True)
    s.line(309,285,344,285,BLUE,3,arrow=True);s.line(309,335,275,335,BLUE,3,arrow=True)
    s.text(130,410,s.t('Deflected crack','偏转裂纹'),22,ORANGE)
    s.text(450,410,s.t('Relative platelet sliding','片晶相对滑移'),22,BLUE)
    s.note('Schematic of platelet sliding and crack deflection.','片晶滑移与裂纹偏转的机制示意。')
    return s


def gromacs_files(lang):
    s=SVG(lang,'What grompp and mdrun exchange' if lang=='en' else 'grompp 与 mdrun 交换什么',
          'Coordinates, interactions and run settings meet in the binary input.' if lang=='en' else '坐标、相互作用定义与运行设置共同形成二进制输入。')
    for y,name,en,zh in [(145,'.gro','Coordinates','坐标'),(245,'.top + .itp','Topology + parameters','拓扑与参数'),(345,'.mdp','Run settings','运行设置')]:
        s.rect(35,y,240,76,'#eef4f9',GRID);s.text(155,y+30,name,23,BLUE,'middle',600);s.text(155,y+59,s.t(en,zh),18,anchor='middle')
        s.line(280,y+38,320,282,MUTED,2,arrow=True)
    s.rect(330,245,155,76,'#dfefeb','#94c9bd');s.text(407,276,'gmx grompp',21,TEAL,'middle',600);s.text(407,304,'.tpr',22,anchor='middle')
    s.line(493,282,539,282,MUTED,2,arrow=True)
    s.rect(550,245,175,76,'#e5edfb','#a6bdf0');s.text(637,288,'gmx mdrun',23,BLUE,'middle',600)
    s.line(637,328,637,355,MUTED,2,arrow=True)
    s.text(637,386,'.xtc  .edr',22,anchor='middle');s.text(637,415,'.log  .cpt',22,anchor='middle')
    s.note('Keep each stage’s settings, topology, coordinates and checkpoint together.','每个阶段的设置、拓扑、坐标和检查点应配套保存。')
    return s


def trajectory_observables(lang):
    s=SVG(lang,'Three different questions for a trajectory' if lang=='en' else '用三个观测量区分三类变化',
          'Constructed point configurations clarify the definitions.' if lang=='en' else '用构造的点阵构型解释观测量的定义。')
    for cx,title in [(135,'RMSD'),(380,'RMSF'),(625,'Rg')]:s.text(cx,136,title,25,anchor='middle',weight=700)
    p=[(75,245),(111,196),(158,210),(194,274),(145,311)]
    s.path(p,TEAL,3);q=[(75,245),(111,196),(166,221),(194,274),(136,296)];s.path(q,BLUE,3,dash='5 5')
    for a,b in zip(p,q):s.circle(*a,5,TEAL);s.circle(*b,5,BLUE);s.line(*a,*b,ORANGE,2)
    for i in range(12):
        a=i*2.399;r=18+(i%3)*9;s.circle(380+r*math.cos(a),250+r*math.sin(a),5,BLUE)
    s.circle(380,250,6,ORANGE);s.line(380,250,413,270,ORANGE,2)
    p=[(565,258),(588,205),(636,191),(684,243),(669,293),(607,315)]
    com=(sum(x for x,y in p)/len(p),sum(y for x,y in p)/len(p));s.path(p,TEAL,3)
    for a in p:s.line(*com,*a,GRID,2);s.circle(*a,6,TEAL)
    s.circle(*com,6,ORANGE)
    for x,en,zh in [(35,'Frame vs reference after alignment','对齐后比较当前帧与参考帧'),(280,'Each atom vs its time-mean position','每个原子相对其时间平均位置'),(525,'Positions vs center of mass','各原子相对质心的位置')]:s.wrap(x,368,s.t(en,zh),200,20)
    s.note('Use consistent atom selections; RMSF requires removing rigid-body motion.','保持原子选择一致；RMSF 分析需先移除整体平移和转动。')
    return s


def stress_definitions(lang):
    s=SVG(lang,'Choose the reference geometry' if lang=='en' else '明确应力与应变的参考几何',
          'Engineering measures use the initial length and cross-sectional area.' if lang=='en' else '工程量采用初始长度与初始截面积。')
    for y,x,w,h,col,label in [(180,110,220,66,BLUE,s.t('Initial','初始')),(320,87,266,48,TEAL,s.t('Stretched','拉伸后'))]:
        s.rect(x,y,w,h,'#dfebf5',col,3)
        s.text(45 if y==180 else 220,215 if y==180 else 414,label,19,anchor='start' if y==180 else 'middle')
        s.line(x,y-21,x+w,y-21,col,2,both=True)
        s.text(x+w/2,y-32,'L₀' if y==180 else 'L',22,col,'middle')
    s.text(345,221,'A₀',23,BLUE);s.text(375,383,'A',23,TEAL)
    s.line(82,344,42,344,ORANGE,3,arrow=True);s.line(358,344,405,344,ORANGE,3,arrow=True)
    s.text(417,350,'F',23,ORANGE)
    for y,formula in [(188,'εeng = (L − L₀) / L₀'),(260,'σeng = F / A₀'),(332,'σtrue = F / A')]:s.text(455,y,formula,22)
    s.note('Area changes must be measured or supported by an explicit material assumption.','变形后的截面积应由测量或明确的材料假设确定。')
    return s


def hysteresis(lang):
    s=SVG(lang,'Hysteresis is an area, not a slope' if lang=='en' else '滞回耗能对应闭环面积',
          'Analytic normalized loop: loading 2e + e²; unloading e + 2e².' if lang=='en' else '解析归一化环：加载 2e + e²，卸载 e + 2e²。')
    X,Y=axes(s,(0,1),(0,3),s.t('Normalized strain  e = ε / εmax','归一化应变 e = ε / εmax'),s.t('Normalized stress  σ*','归一化应力 σ*'),xticks=[0,.25,.5,.75,1],yticks=[0,1,2,3])
    a=[(X(i/100),Y(2*i/100+(i/100)**2)) for i in range(101)]
    b=[(X(i/100),Y(i/100+2*(i/100)**2)) for i in range(100,-1,-1)]
    s.path(a+b,'none',0,'#dbece6',True)
    curve(s,X,Y,lambda e:2*e+e*e,0,1,BLUE);curve(s,X,Y,lambda e:e+2*e*e,0,1,TEAL)
    s.text(110,183,s.t('Loading →','加载 →'),21,BLUE);s.text(110,214,s.t('← Unloading','← 卸载'),21,TEAL)
    for e1,e2,fun,col in [(.55,.63,lambda e:2*e+e*e,BLUE),(.7,.62,lambda e:e+2*e*e,TEAL)]:s.line(X(e1),Y(fun(e1)),X(e2),Y(fun(e2)),col,3,arrow=True)
    s.note('Teaching curves: enclosed normalized area = ∫₀¹(e − e²) de = 1/6.','教学曲线的归一化闭环面积 = ∫₀¹(e − e²) de = 1/6。')
    return s


def silk_sheet(lang):
    s=SVG(lang,'Silk: ordered strands inside a crystal' if lang=='en' else '丝素：结晶区中的有序链段',
          'Antiparallel β-sheet schematic; hydrogen bonds join adjacent strands.' if lang=='en' else '反平行 β-折叠示意；氢键连接相邻链段。')
    for row in range(4):
        y=168+row*52
        pts=[(85+i*24,y+(9 if i%2 else -9)) for i in range(11)]
        s.path(pts,BLUE,4)
        s.line(90 if row%2==0 else 319,y-24,319 if row%2==0 else 90,y-24,TEAL,2,arrow=True)
        if row<3:
            for x in [110,158,206,254,302]:s.line(x,y+12,x,y+40,ORANGE,2,dash='3 5')
    s.text(204,393,s.t('Alternating chain directions','相邻链方向相反'),20,anchor='middle')
    s.rect(446,163,235,180,'#e4eef5','#97b5cd',12)
    for yy in [190,224,258,292]:
        s.line(465,yy,657,yy,BLUE,8)
        s.line(475,yy+14,645,yy+14,TEAL,5)
    s.line(350,245,423,245,MUTED,3,arrow=True)
    s.text(565,393,s.t('Packed sheet domains','折叠片层堆积'),20,anchor='middle')
    s.note('Antiparallel strands and packed sheets, drawn schematically.','反平行链段与片层堆积的结构示意。')
    return s


def silk_composite(lang):
    s=SVG(lang,'Crystalline nodes and extensible chains' if lang=='en' else '结晶节点与可伸展链段',
          'The same two-phase motif is shown before and during extension.' if lang=='en' else '同一两相结构单元在伸展前后的示意。')
    for y,left,right,a,lab in [(192,205,500,23,s.t('Initial','初始')),(345,155,550,7,s.t('Extended','伸展'))]:
        s.text(35,y-64,lab,22)
        for yy in [y-21,y+21]:s.wave(left+40,yy,right-left-40,a,3,TEAL,4)
        for x in [left,right]:
            s.rect(x,y-46,42,92,'#d2e4f5',BLUE,4)
            for k in range(3):s.line(x+9,y-31+k*30,x+33,y-31+k*30,BLUE,4)
    s.line(145,345,113,345,ORANGE,3,arrow=True);s.line(603,345,643,345,ORANGE,3,arrow=True)
    s.text(380,434,s.t('Crystal connections + chain extension','结晶连接 + 链段伸展'),23,anchor='middle')
    s.note('Two-phase schematic: crystalline connections and amorphous chains.','两相结构示意：结晶连接与非晶链段。')
    return s


def sem_masks(lang):
    s=SVG(lang,'One geometry, three image representations' if lang=='en' else '同一几何的三种图像表示',
          'Synthetic fibers illustrate thresholding and skeletonization.' if lang=='en' else '构造的纤维图像用于解释阈值分割与骨架提取。')
    for panel,(cx,en,zh) in enumerate([(140,'Input image','输入图像'),(380,'Binary mask','二值掩膜'),(620,'Skeleton','骨架')]):
        s.text(cx,137,s.t(en,zh),22,anchor='middle',weight=700)
        s.rect(cx-98,170,196,200,'#e1e6eb' if panel==0 else '#f0f4f8',GRID,4)
        for j in range(3):
            pts=[(cx-72+i*1.44,202+j*64+9*math.sin(i*.045+j)) for i in range(101)]
            s.path(pts,'#5d6e7c' if panel==0 else BLUE,16)
            if panel==2:s.path(pts,ORANGE,3)
    s.line(247,270,270,270,MUTED,2,arrow=True);s.line(487,270,510,270,MUTED,2,arrow=True)
    s.wrap(60,410,s.t('Threshold → foreground pixels; skeleton → fiber centerlines.','阈值分割得到前景像素；骨架提取得到纤维中心线。'),640,22)
    s.note('Synthetic fiber image for illustrating image-analysis steps.','用于解释图像分析步骤的构造纤维图像。')
    return s


def sem_measure(lang):
    s=SVG(lang,'Convert pixels into a local fiber width' if lang=='en' else '把像素距离转换为局部纤维宽度',
          'A straight strip makes the distance-transform definition visible.' if lang=='en' else '用直条带解释距离变换与骨架宽度的关系。')
    s.rect(74,188,333,104,'#dce8f9','#9cb5da',0)
    s.line(74,240,407,240,ORANGE,3,dash='6 5');s.circle(239,240,6,ORANGE)
    s.line(239,238,239,190,TEAL,2,both=True);s.text(258,218,'rpx',23,TEAL)
    s.line(98,188,98,292,BLUE,2,both=True);s.text(112,283,'2rpx',22,BLUE)
    s.text(476,198,'d = 2rpx × s',27,weight=600)
    s.wrap(476,245,s.t('s: length per pixel','s：每像素对应长度'),225,20)
    s.wrap(476,300,s.t('Evaluate on the centerline','在骨架中心线上取值'),225,20)
    s.line(90,370,190,370,INK,5);s.line(90,361,90,379,INK);s.line(190,361,190,379,INK)
    s.text(141,410,s.t('Calibration','标尺校准'),20,anchor='middle')
    s.wrap(263,378,s.t('At branches, crossings and edges, review width estimates separately.','分叉、交叉与图像边缘附近应单独检查宽度估计。'),428,21)
    s.note('Local diameter is twice the nearest-boundary distance for this strip geometry.','在该条带几何中，局部直径等于最近边界距离的两倍。')
    return s


def multiscale_transfer(lang):
    s=SVG(lang,'Transfer quantities, not just pictures' if lang=='en' else '跨尺度传递的是物理量',
          'Each representation retains the information required by the next model.' if lang=='en' else '每层模型保留下一层计算所需的信息。')
    for cx,en,zh in [(140,'Molecular','分子尺度'),(380,'Mesoscale','介观尺度'),(620,'Continuum','连续介质')]:s.text(cx,135,s.t(en,zh),23,anchor='middle',weight=700)
    pts=[(64+i*14,236+30*math.sin(i*.9)) for i in range(12)]
    s.path(pts,BLUE,3)
    for p in pts:s.circle(*p,7,BLUE)
    nodes=[(310,190),(380,175),(451,205),(301,284),(375,255),(449,303)]
    for a,b in [(0,1),(1,2),(0,3),(0,4),(1,4),(2,4),(2,5),(3,4),(4,5)]:s.line(*nodes[a],*nodes[b],TEAL,4)
    for p in nodes:s.circle(*p,6,ORANGE)
    for i in range(5):
        s.line(546+i*36,178,562+i*36,318,BLUE,2)
        s.line(546+i*4,178+i*35,690+i*4,178+i*35,BLUE,2)
    s.line(237,235,279,235,MUTED,2,arrow=True);s.line(479,235,521,235,MUTED,2,arrow=True)
    s.wrap(46,364,s.t('Bond and angle statistics','键长与键角统计'),192,20)
    s.wrap(287,364,s.t('Persistence, connectivity and crosslinks','持久长度、连接性与交联'),195,20)
    s.wrap(537,364,s.t('Effective constitutive response','有效本构响应'),195,20)
    s.note('Pass the state point, units and calibration range with every parameter.','每个传递参数同时携带状态点、单位和标定范围。')
    return s


def homogenization(lang):
    s=SVG(lang,'From a representative volume to stiffness' if lang=='en' else '从代表性体积得到有效刚度',
          'Small uniaxial strain with traction-free lateral faces: a schematic RVE.' if lang=='en' else '小应变单轴加载、侧面自由条件下的代表性体积示意。')
    s.rect(75,167,245,210,'#eff5f8','#9aafbf',0)
    for i in range(5):
        s.wave(86,191+i*37,220,12,2,TEAL,3)
    for i in range(5):s.line(97+i*49,180,112+i*49,358,BLUE,3)
    for y in [205,270,335]:
        s.line(69,y,35,y,ORANGE,3,arrow=True);s.line(326,y,361,y,ORANGE,3,arrow=True)
    s.text(197,412,s.t('Representative volume V','代表性体积 V'),21,anchor='middle')
    s.text(415,197,'⟨σxx⟩ = (1/V) ∫V σxx dV',21,weight=600)
    s.text(415,267,'Eeff = ⟨σxx⟩ / εxx',25,BLUE)
    s.wrap(415,318,s.t('Volume average of local stress at the prescribed small strain.','给定小应变下，对局部应力作体积平均。'),292,20)
    s.note('Other boundary conditions or anisotropy require the corresponding stiffness terms.','其他边界条件或各向异性情形需采用相应刚度分量。')
    return s


def periodic_box(lang):
    s=SVG(lang,'Periodic distance crosses the boundary' if lang=='en' else '周期距离可以跨越盒子边界',
          'One coordinate illustrates the minimum-image convention.' if lang=='en' else '用一个坐标方向解释最小镜像约定。')
    s.rect(130,155,480,210,'#edf5f8','#92adbd',0)
    for x in [130,610]:s.line(x,136,x,388,MUTED,2,dash='6 6')
    s.circle(178,254,16,BLUE);s.circle(562,254,16,TEAL);s.circle(82,254,16,'#b0d8d1',TEAL)
    s.text(178,215,'i',24,BLUE,'middle');s.text(562,215,'j',24,TEAL,'middle');s.text(82,215,'j′',24,TEAL,'middle')
    s.line(195,254,544,254,MUTED,2,both=True);s.text(370,240,'|Δx| = 0.8L',22,anchor='middle')
    s.line(86,305,176,305,ORANGE,3,both=True);s.text(139,340,'rmin = 0.2L',20,ORANGE,'middle')
    s.line(130,400,610,400,BLUE,2,both=True);s.text(370,429,'L',22,BLUE,'middle')
    s.note('Δxmin = Δx − L round(Δx/L); apply per axis in an orthorhombic box.','Δxmin = Δx − L round(Δx/L)；正交盒子按各坐标轴处理。')
    return s


def lj_potential(lang):
    s=SVG(lang,'Read the Lennard–Jones pair term' if lang=='en' else '读懂 Lennard–Jones 成对势',
          'Reduced units isolate the repulsive core and attractive well.' if lang=='en' else '用约化单位区分短程排斥与吸引势阱。')
    X,Y=axes(s,(.95,3),(-1.2,2),s.t('Separation  r / σ','粒子间距 r / σ'),'U / ε',xticks=[1,1.5,2,2.5,3],yticks=[-1,0,1,2])
    fun=lambda r:4*(r**-12-r**-6)
    curve(s,X,Y,fun,.95,3)
    s.line(X(.95),Y(0),X(3),Y(0),MUTED,1,dash='5 5')
    rmin=2**(1/6);s.circle(X(rmin),Y(-1),6,ORANGE)
    s.line(X(rmin)+8,Y(-1),340,Y(-1),ORANGE,2)
    s.text(350,Y(-1)+6,'rmin = 2¹ᐟ⁶σ',22,ORANGE)
    s.text(300,183,'U / ε = 4[(σ/r)¹² − (σ/r)⁶]',22)
    s.text(300,221,'F(r) = −dU/dr',23,TEAL)
    s.note('This pair term is one part of a force field; charged water also needs electrostatics.','成对势只是力场的一部分；带电水模型还包含静电相互作用。')
    return s


def fiber_recruitment(lang):
    s=SVG(lang,'Straightening changes the load path' if lang=='en' else '拉直过程改变纤维承载方式',
          'A conceptual fiber segment progresses from waviness to axial loading.' if lang=='en' else '单根纤维链段从弯曲形态逐渐转为轴向承载的概念示意。')
    for y,x,w,a,col,en,zh in [(193,175,410,33,BLUE,'Wavy segment','弯曲链段'),(350,112,536,8,TEAL,'Aligned segment','取向链段')]:
        s.wave(x,y,w,a,3,col,5)
        s.circle(x,y,9,ORANGE);s.circle(x+w,y,9,ORANGE)
        s.text(30,y-57,s.t(en,zh),22,weight=700)
        s.line(x-12,y,x-55,y,ORANGE,3,arrow=True);s.line(x+w+12,y,x+w+55,y,ORANGE,3,arrow=True)
    s.text(380,265,s.t('Bending and reorientation','弯曲与重取向'),21,BLUE,'middle')
    s.text(380,412,s.t('Increasing axial load contribution','轴向承载贡献增加'),21,TEAL,'middle')
    s.note('Conceptual transition from bending to axial loading.','从弯曲到轴向承载的概念示意。')
    return s


def fiber_stiffening(lang):
    s=SVG(lang,'Strain stiffening in a teaching model' if lang=='en' else '教学模型中的应变强化',
          'The polynomial is the same illustrative relation used in the article.' if lang=='en' else '采用正文代码中的同一示意多项式关系。')
    X,Y=axes(s,(0,.5),(0,.7),s.t('Strain  ε','应变 ε'),s.t('Schematic stress  σ*','示意应力 σ*'),xticks=[0,.1,.2,.3,.4,.5],yticks=[0,.2,.4,.6])
    fun=lambda e:.1*e+5*e**3;curve(s,X,Y,fun,0,.5)
    s.text(120,181,'σ* = 0.1ε + 5ε³',24,BLUE)
    s.text(120,217,'dσ*/dε = 0.1 + 15ε²',22,TEAL)
    for e in [.15,.4]:
        slope=.1+15*e**2;lo,hi=e-.04,e+.04
        s.line(X(lo),Y(fun(e)+slope*(lo-e)),X(hi),Y(fun(e)+slope*(hi-e)),ORANGE,3)
        s.circle(X(e),Y(fun(e)),5,ORANGE)
    s.note('Teaching curve in arbitrary units; orange lines mark local tangents.','任意单位的教学曲线；橙线为局部切线。')
    return s


def afm_calibration(lang):
    s=SVG(lang,'Separate cantilever bending from indentation' if lang=='en' else '区分悬臂偏转与样品压入',
          'After contact: piezo advance is shared by bending and indentation.' if lang=='en' else '接触后，压电推进量分配为悬臂偏转与样品压入。')
    s.path([(55,305),(285,305),(301,340),(311,345),(321,340),(337,305),(385,305),(385,415),(55,415)],'#96bfb3',2,'#d9eee9',True)
    s.line(55,305,385,305,MUTED,1,dash='5 5')
    s.path([(75,230),(290,190),(311,235)],BLUE,7)
    s.path([(295,235),(327,235),(311,345)],INK,2,'#9eb5c9',True)
    s.line(350,305,350,345,ORANGE,2,both=True);s.text(363,333,'δ',24,ORANGE)
    s.line(75,230,290,230,MUTED,2,dash='6 5');s.line(281,192,281,227,TEAL,2,both=True)
    s.text(293,209,'d',23,TEAL)
    s.text(455,181,'d = S × V',26,TEAL)
    s.text(455,235,'F = k × d',26,BLUE)
    s.text(455,289,'δ = Δz − d',26,ORANGE)
    s.wrap(455,345,s.t('S: deflection sensitivity; k: calibrated spring constant.','S：偏转灵敏度；k：标定的弹簧常数。'),265,20)
    s.note('Choose positive Δz into contact; subtract baselines and contact offsets first.','取压向样品为 Δz 正方向；先扣除基线与接触点偏移。')
    return s


def afm_hertz(lang):
    s=SVG(lang,'Hertz curves from stated model parameters' if lang=='en' else '由明确参数计算 Hertz 曲线',
          'Elastic half-space; rigid spherical tip, R = 5 μm and ν = 0.5.' if lang=='en' else '弹性半空间与刚性球形压头；R = 5 μm，ν = 0.5。')
    X,Y=axes(s,(0,200),(0,12),s.t('Indentation δ (nm)','压入深度 δ（nm）'),s.t('Force F (nN)','力 F（nN）'),xticks=[0,50,100,150,200],yticks=[0,4,8,12])
    def hertz(d,E):return 4/3*(E/(1-.5**2))*math.sqrt(5e-6)*(d*1e-9)**1.5*1e9
    for E,col in [(1e4,TEAL),(3e4,BLUE)]:curve(s,X,Y,lambda d:hertz(d,E),0,200,col)
    s.text(115,182,'E = 30 kPa',22,BLUE);s.text(115,215,'E = 10 kPa',22,TEAL)
    s.text(115,253,'F = (4/3) E*√R δ³ᐟ²',22)
    s.note('E* = E/(1 − ν²). Analytic elastic, non-adhesive curves.','E* = E/(1 − ν²)。解析弹性、非黏附接触曲线。')
    return s


# Each insertion is tied to a heading already present in the complete source.
# Figures appear at the end of the relevant section, immediately before the next heading.
POSTS = [
 ('coarse-grained-biomolecular-networks','coarse-grained-biomolecular-networks-zh',[
  ('coarse-centers',coarse_centers,'## Interaction Potentials','## 有效相互作用势',
   'Mapping groups of equal-mass atoms to their centers preserves chain connectivity. For unequal masses, use the mass-weighted center R = Σ(mᵢrᵢ)/Σmᵢ; bead types retain the selected chemical distinctions.',
   '将等质量原子分组并映射到质心，同时保留链连接关系。质量不同时采用 R = Σ(mᵢrᵢ)/Σmᵢ；珠子类型编码需要保留的化学差异。'),
  ('coarse-potential',coarse_potential,'## Simulation Setup','## 体系构建',
   'A Gaussian distribution in a dimensionless Cartesian coordinate q gives the harmonic effective potential U/kBT = q²/2, up to an additive constant. Bond-distance and angle distributions require their corresponding coordinate-measure corrections before inversion.',
   '对无量纲笛卡尔坐标 q，高斯分布对应 U/kBT = q²/2 的谐和有效势，允许相差一个加法常数。若反演键长或键角分布，还须处理相应坐标测度的修正。')]),
 ('biomaterials-mechanical-testing','biomaterials-mechanical-testing-zh',[
  ('testing-geometry',testing_geometry,'## From Force-Displacement','## 从力-位移',
   'Optical markers measure extension within the gauge section. Crosshead travel also includes fixture deformation, grip seating and slip, so it should not automatically be treated as specimen extension.',
   '光学标记测量的是标距段内的伸长；横梁位移还包含机架和夹具变形、装夹就位及滑移，计算应变时需区分这些来源。'),
  ('testing-bias',testing_bias,'## Recognizing Artifacts','## 在数据进入',
   'For a circular fiber with fixed force and strain, the calculated modulus scales as d⁻². A diameter overestimate of 10% gives Ereported/Etrue = 1/1.1² ≈ 0.826, or a 17.4% underestimate. The curve is an analytic error-propagation example.',
   '在力与应变测量不变时，圆截面纤维的计算模量与 d⁻² 成正比。直径高估 10% 时，E报告/E真实 = 1/1.1² ≈ 0.826，即模量低估约 17.4%。图为解析误差传播示例。')]),
 ('engineered-superstructures','engineered-superstructures-zh',[
  ('auxetic-squares',auxetic,'### Section 4:','### 第 4 节',
   'An ideal array of corner-hinged rigid squares expands in both directions as the alternating rotation angle increases from 5° to 30°. Equal axial and transverse strains give ν = −1 for this mechanism; compliant hinges and panel deformation modify a fabricated specimen’s response.',
   '角点铰接的理想刚性方块阵列从 5° 转到 30° 时，纵横两个方向同步展开。该机构的纵横应变相等，对应 ν = −1；实际试样还受铰链柔度和面板变形影响。'),
  ('lattice-scaling',lattice_scaling,'### Section 9:','### 第 9 节',
   'With C = 1, E*/Es = (ρ*/ρs)ⁿ separates the effect of the scaling exponent: n = 1 retains more stiffness at low density than n = 2. The curves illustrate the scaling relation; actual coefficients depend on geometry and loading direction.',
   '令 C = 1，用 E*/Es = (ρ*/ρs)ⁿ 单独比较标度指数：在低相对密度下，n = 1 比 n = 2 保留更多刚度。图中为教学曲线；实际系数还取决于几何与加载方向。')]),
 ('bio-hierarchical-structures','bio-hierarchical-structures-zh',[
  ('collagen-hierarchy',collagen_hierarchy,'### 3. Bone:','### 3. 骨：',
   'Collagen’s triple-helical conformation, staggered molecular packing and fibril bundles belong to distinct structural levels. The diagram emphasizes how organization changes across levels rather than using one common geometric scale.',
   '胶原的三股螺旋、分子错位排列与原纤维束属于不同结构层级。图中重点是各层级组织方式的变化，绘图比例未统一为同一空间尺度。'),
  ('nacre-crack',nacre_crack,'### 5. Spider Silk:','### 5. 蜘蛛丝：',
   'Stiff platelets and compliant interlayers create opportunities for relative sliding and crack deflection. The constructed crack path illustrates how interfaces change the direction of propagation.',
   '刚性片晶与柔性层间基质为相对滑移、裂纹偏转提供结构条件。构造的裂纹路径展示了界面如何改变传播方向。')]),
 ('gromacs-md-tutorial','gromacs-md-tutorial-zh',[
  ('gromacs-files',gromacs_files,'### Worked Example:','### 实战案例：',
   'grompp combines coordinates, topology and run settings into a .tpr input; mdrun uses that input to produce the trajectory, energy record, log and checkpoint. File provenance should follow each minimization, equilibration and production stage.',
   'grompp 将坐标、拓扑与运行设置组合成 .tpr 输入，mdrun 再输出轨迹、能量记录、日志和检查点。最小化、平衡与生产阶段都应保留对应的文件组合。'),
  ('trajectory-observables',trajectory_observables,'### Python Analysis Code','### 性能优化与多尺度',
   'RMSD compares each aligned frame with a reference; RMSF measures time fluctuations around each selected atom’s mean position; Rg measures mass-weighted spread around the center of mass. The constructed configurations make these different definitions visible.',
   'RMSD 比较对齐后的当前帧与参考帧；RMSF 衡量各选定原子围绕时间平均位置的涨落；Rg 衡量原子相对质心的质量加权空间分散程度。构造的点阵构型直观区分了这三个定义。')]),
 ('stress-strain-curves','stress-strain-curves',[
  ('stress-definitions',stress_definitions,'## Key Regions','## 曲线的五个',
   'Engineering stress and strain use the initial geometry A₀ and L₀, whereas true stress uses the instantaneous area A. The sketch separates these definitions before curve fitting or property extraction.',
   '工程应力和工程应变使用初始几何 A₀、L₀，真应力使用瞬时截面积 A。拟合曲线和提取性能之前，应先统一这些定义。'),
  ('stress-hysteresis',hysteresis,'## Common Mistakes','## 常见错误',
   'The teaching loop uses σ*load = 2e + e² and σ*unload = e + 2e², where e = ε/εmax. Its enclosed normalized area is 1/6; dimensional energy density additionally requires the stress and strain scales. It illustrates cyclic dissipation rather than work to fracture.',
   '教学滞回环取 σ*加载 = 2e + e²、σ*卸载 = e + 2e²，其中 e = ε/εmax。归一化闭环面积为 1/6，换算为有量纲能量密度还需应力与应变标度。这里解释的是循环耗能。')]),
 ('silk-fibroin','silk-fibroin-structure-mechanics-zh',[
  ('silk-sheets',silk_sheet,'## Mechanics and Processing','## 工艺-结构',
   'In the antiparallel β-sheet motif, neighboring chain segments run in opposite directions and form hydrogen bonds between strands. The drawing distinguishes a sheet from a packed crystalline domain; distances are schematic.',
   '反平行 β-折叠中，相邻链段方向相反，并通过链间氢键连接。示意图区分了单个折叠片层与堆积的结晶区，距离采用示意比例。'),
  ('silk-composite',silk_composite,'### Processing-Structure','## 实验建议',
   'Crystalline domains provide physical connections while intervening amorphous chains change conformation during extension. The paired drawings retain the same connections and illustrate the two-phase mechanism.',
   '结晶区提供物理连接，连接其间的非晶链段在伸展中改变构象。前后两图保留相同连接关系，用于解释两相机制。')]),
 ('sem-image-analysis','sem-image-analysis',[
  ('sem-masks',sem_masks,'### Step 4:','### 第四步：',
   'The same synthetic fiber geometry is shown as an intensity image, a foreground mask and a centerline overlay. Threshold selection changes the mask; skeletonization supplies the locations where a local distance-transform width can be sampled.',
   '同一构造纤维几何分别显示为灰度图、前景掩膜和中心线叠加图。阈值选择决定掩膜，骨架则提供采样局部距离变换宽度的位置。'),
  ('sem-width',sem_measure,'### Step 5:','### 第五步：',
   'For an isolated straight strip, the local width is d = 2rpxs, with rpx the distance from a skeleton point to the nearest background and s the physical length per pixel. Crossings, branches and edge-truncated objects require separate review.',
   '对孤立直条带，局部宽度为 d = 2rpxs，其中 rpx 是骨架点到最近背景的像素距离，s 是每像素对应的物理长度。交叉、分叉和被图像边缘截断的对象需单独检查。')]),
 ('multiscale-modeling-intro','duochidu-monijianjie',[
  ('multiscale-transfer',multiscale_transfer,'## Bridging Scales','## 用 Python',
   'A molecular model can supply conformational statistics for a mesoscopic chain or network, which in turn supplies an effective response to a continuum model. Each transfer must retain its units, state point and calibration range.',
   '分子模型可向介观链或网络模型提供构象统计，介观模型再向连续介质模型提供有效响应。每次传递都应保留参数单位、状态点和标定范围。'),
  ('multiscale-rve',homogenization,'## Key Challenges','## 实操建议',
   'For a representative volume in small uniaxial loading with traction-free lateral faces, averaging local axial stress gives the macroscopic stress. Eeff = ⟨σxx⟩/εxx describes this loading condition; anisotropy and different boundary constraints require the appropriate stiffness components.',
   '在侧面自由的小应变单轴加载下，对代表性体积的局部轴向应力求体积平均可得到宏观应力。Eeff = ⟨σxx⟩/εxx 描述这一加载条件；各向异性和不同约束需采用相应的刚度分量。')]),
 ('lammps-first-simulation','lammps-first-simulation',[
  ('lammps-periodic',periodic_box,'### Key Parameters','### 关键参数',
   'For the constructed one-dimensional example, particles separated by 0.8L in the displayed box are only 0.2L apart through a periodic boundary. Orthorhombic minimum-image distances can be calculated componentwise as Δxmin = Δx − L round(Δx/L).',
   '在构造的一维示例中，盒内坐标相差 0.8L 的粒子通过周期边界只相距 0.2L。正交盒子的最小镜像位移可逐分量计算为 Δxmin = Δx − L round(Δx/L)。'),
  ('lammps-lj',lj_potential,'### Trajectory Analysis','### 轨迹分析',
   'The Lennard–Jones term has its minimum U = −ε at r = 2^(1/6)σ, and its force is −dU/dr. This analytic reduced-unit curve explains one pair interaction; the water force field in a real simulation also requires its specified bonded and electrostatic terms.',
   'Lennard–Jones 势在 r = 2^(1/6)σ 处取最小值 U = −ε，力由 −dU/dr 给出。约化单位解析曲线解释一项成对相互作用；实际水模型还需采用其规定的键合与静电项。')]),
 ('fiber-network-mechanics','fiber-network-mechanics',[
  ('fiber-recruitment',fiber_recruitment,'### 1. Strain-Stiffening','### 应变强化',
   'A wavy fiber initially accommodates extension through bending and reorientation; further alignment increases axial load transfer. This mechanism sketch connects fiber geometry with a nonlinear network response.',
   '弯曲纤维在初期通过弯曲与重取向适应伸长，进一步取向后轴向承载贡献增加。机制图用于理解网络非线性响应。'),
  ('fiber-stiffening',fiber_stiffening,'### 2. Architecture','### 架构-性能',
   'The article’s illustrative polynomial σ* = 0.1ε + 5ε³ has tangent stiffness dσ*/dε = 0.1 + 15ε², which rises with strain. The ordinate is in arbitrary units; the curve is generated from the stated formula.',
   '正文的示意多项式 σ* = 0.1ε + 5ε³ 对应切线刚度 dσ*/dε = 0.1 + 15ε²，因此刚度随应变增加。纵轴采用任意单位，曲线由所示公式计算。')]),
 ('afm-data-processing','afm-data-processing',[
  ('afm-calibration',afm_calibration,'### 4. Baseline Correction','### 4. 基线校正',
   'After calibration, deflection d = SV gives force F = kd. With piezo advance defined positive into contact and offsets removed, indentation is δ = Δz − d. This geometry prevents piezo motion from being mistaken for sample indentation.',
   '标定后由偏转 d = SV 得到力 F = kd。取压向样品为压电位移正方向并扣除偏移后，压入深度为 δ = Δz − d；几何关系明确了压电位移与样品压入的区别。'),
  ('afm-hertz',afm_hertz,'## Scaling and Advanced','## 批量处理与进阶',
   'Hertz curves calculated with R = 5 μm, ν = 0.5 and E = 10 or 30 kPa show how modulus changes force at the same indentation. The model assumes a rigid spherical tip, a homogeneous elastic half-space and negligible adhesion; the curves are calculated analytic examples.',
   '取 R = 5 μm、ν = 0.5、E = 10 或 30 kPa 计算 Hertz 曲线，可比较相同压入深度下模量对力的影响。模型采用刚性球形压头、均匀弹性半空间与可忽略黏附的假设，图中为解析教学曲线。')]),
]


def insert_before_heading(text, prefix, block, url):
    if url in text:
        # Refresh this generator's exact image/caption block; leave other prose alone.
        pattern = r'!\[[^\n]*\]\('+re.escape(url)+r'\)\n\n[^\n]+\n\n'
        updated, count = re.subn(pattern,lambda _:block,text,count=1)
        if count != 1: raise ValueError(f'Unexpected existing image block: {url}')
        return updated
    matches=list(re.finditer(r'^'+re.escape(prefix)+r'[^\n]*$',text,re.M))
    if len(matches)!=1: raise ValueError(f'Ambiguous/missing insertion heading: {prefix}')
    i=matches[0].start()
    return text[:i]+block+text[i:]


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    assets=[];modified=[]
    for enfile,zhfile,figures in POSTS:
        for lang,filename in [('en',enfile),('zh',zhfile)]:
            post=ROOT/'content/posts'/lang/(filename+'.md')
            raw=post.read_bytes();bom=raw.startswith(b'\xef\xbb\xbf')
            newline='\r\n' if b'\r\n' in raw else '\n'
            source=raw.decode('utf-8-sig').replace('\r\n','\n');updated=source
            for key,draw,enanchor,zhanchor,encaption,zhcaption in figures:
                fig=draw(lang);asset=OUT/f'mech-{key}-{lang}.svg'
                asset.write_text(fig.finish(),encoding='utf-8',newline='\n')
                assets.append(asset)
                url='/static/images/article-guides/'+asset.name
                alt=ET.fromstring(fig.finish()).find('{http://www.w3.org/2000/svg}title').text
                caption=zhcaption if lang=='zh' else encaption
                block=f'![{alt}]({url})\n\n{caption}\n\n'
                updated=insert_before_heading(updated,zhanchor if lang=='zh' else enanchor,block,url)
            if updated!=source:
                post.write_bytes((b'\xef\xbb\xbf' if bom else b'')+updated.replace('\n',newline).encode('utf-8'));modified.append(post)
    assert len(assets)==48 and len(set(assets))==48
    print(f'Generated {len(assets)} bilingual SVGs; updated {len(modified)} source posts.')


if __name__=='__main__': main()
