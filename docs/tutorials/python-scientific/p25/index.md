# 从公开接口获取可追溯的数据

Source: https://ml-biomat.com/tutorials/python-scientific/p25/
Language: zh-CN

从四个蛋白质数据库条目出发，把网址、嵌套 JSON、科学含义与可重复的数据表连接起来。

## 一张结构表，是怎样从数据库来到电脑里的

准备比较蛋白质或核酸结构时，我们常常先做一张表：每个结构叫什么名字，用哪种实验方法得到，包含多少个原子，结构的分辨率是多少。如果只有两条记录，打开网页抄写似乎很快；当记录增加到几十条，真正耗时的事情便出现了：有的数字藏在不同栏目里，有的条目没有同一种指标，有的字段更新后需要重新检查。Python 适合接手这一段重复劳动。数据库提供一种供程序访问的入口，称为应用程序接口，通常简称 API。程序按约定的地址提出请求，数据库返回结构清楚的数据，随后我们再根据科学问题挑选字段、检查含义、生成表格和图。

本章使用 RCSB Protein Data Bank 的公开接口，读取 1UBQ、4HHB、1BNA 和 1D3Z 四个条目。它们分别涉及泛素、血红蛋白、DNA 和溶液核磁共振得到的泛素结构。这样的选择有一个具体目的：前三个条目能在衍射分辨率这一列中比较，第四个条目则要求我们认真处理“这一指标不适用于当前实验方法”的情况。学习结束时，你会得到四份保留原始内容的 JSON 文件、一张字段含义明确的 CSV 表，以及能够解释这些数字的图。更重要的是，你能沿着表格中的任意一个数值，找回它来自哪个条目、哪一层字段、哪一份原始响应。

API 可以理解为图书馆的标准借阅窗口。网址说明要找哪本书，请求说明想执行什么操作，响应状态说明这次办理是否成功，而返回的内容才是交到你手上的材料。这个类比还包含一个容易忽略的细节：借阅成功并不意味着这本书恰好回答你的研究问题。程序仍要核对身份和内容。我们会把网络通信与科学解释分别做好，再将它们接起来，因此遇到新的数据库时，能够沿用相同的工作方法，而不必重新猜测每一步的职责。

## 从共享坐标到可以连接的数据记录

蛋白质数据库在 1971 年宣布建立。结构研究需要共享的核心成果之一，是原子在三维空间中的坐标；有了坐标，其他研究者才能查看分子形状、计算距离、比较结合位点，并将结构用于新的问题。随着档案积累，坐标之外的说明也变得越来越重要。同样叫“泛素”的分子，可以通过不同实验方法研究，可以在不同条件下测量，也可能有多份独立提交的结构。因此，科学数据的组织需要一个稳定的条目身份，以及与身份连接的实验方法、分子组成和文献等信息。本章的四字符编号就是条目入口，编号对应的是一条档案记录，而不是一种蛋白质在所有条件下的唯一形状。

这种组织方式解释了为什么网页、坐标文件和 API 可以互相配合。网页帮助人阅读，坐标文件保存空间结构，接口则帮助程序提取结构化信息。它们围绕同一条目连接，但承担的任务不同。本章访问的是 `core/entry` 入口，返回条目层面的说明；其中的原子数是一项档案元数据。若下一步要计算两个原子之间的距离，还需要下载并读取坐标文件。先明确当前层级，可以避免把“有一条结构记录”误解为“已经把分子坐标读进 Python”。

![共享结构档案的发展与条目实体实例层级。](https://ml-biomat.com/static/tutorials/python-scientific/figures/6e451c3dc032223b2b658089.svg?v=6e451c3dc032)

图 1原创档案结构图：1971 年 PDB 建立、1977 年计算机档案论文，以及今天围绕条目连接的网页、接口和坐标。下方区分条目、实体与实例。

一个条目还可以继续分成聚合物实体和结构中的链。实体描述某一种聚合物分子，例如某条特定氨基酸序列；链描述结构中出现的实例。同一种实体可以在结构中出现多次。血红蛋白条目 4HHB 的 `polymer_entity_count` 为 2，表达的是两种聚合物实体，不能直接读成“两条链”。这种差异看似属于生物学，却会直接决定代码怎样命名列、怎样连接表。我们把结果列命名为 `polymer_entities`，就是要让数据对象的名字保留原字段的科学层级。

## 把一次请求拆成能够检查的步骤

访问 1UBQ 的完整地址为 `https://data.rcsb.org/rest/v1/core/entry/1UBQ`。前面的部分指定服务与资源类型，末尾的编号选择条目。使用 Requests 时，`session.get(...)` 发出 HTTP GET 请求，返回一个响应对象。这个对象同时保存状态、响应头和正文。`raise_for_status()` 检查 HTTP 错误状态，使不存在的地址或服务器错误在下载阶段明确暴露。随后调用 `response.json()`，把 JSON 文本解析成 Python 对象。两个动作检查的是不同事情：前者关注服务器怎样回应，后者关注正文能否按照 JSON 语法读懂。

JSON 中用花括号包围的对象通常转成 Python 字典，方括号中的有序集合转成列表，数字转成相应数值，`null` 转成 `None`。例如实验方法位于一个列表中，读取第一项的方法需要先取 `exptl`，再取列表中的第 0 项，最后取其中的 `method`。这条索引路径描述的是数据结构，不是一个可以随意省略的写法。列表保留多个项目的可能性，所以示例会收集全部方法并连接成文本，而不是默认每条记录永远只有一个方法。理解这层对应关系后，新的嵌套字段也可以按相同方式逐层检查。

网络等待也需要具体的设置。代码使用 `timeout=(10, 60)`，分别给连接阶段和读取阶段设置等待时限，单位是秒。这有助于在服务暂时不可达或响应迟迟没有到来时结束当前尝试。读取超时关注接收数据时的等待间隔，并不是承诺整个任务一定在 70 秒内完成。我们只有四个条目，按顺序访问并在请求间留出间隔即可。将来扩大到大量条目时，应先查看服务提供的查询和批量获取方式，复用已经下载的记录，再决定怎样组织请求，避免把相同内容反复传输。

一个 JSON 能正常解析，还不等于它适合进入结果表。示例的 `validate_record` 会检查返回的条目编号是否与请求一致，实验方法是否为非空文本列表，原子数是否为正整数。这些检查来自本章表格的用途：如果身份错了，后面的每一列都会归到错误对象名下；如果方法缺失，分辨率的解释就失去上下文；如果原子数不是合理的计数，绘图也没有清楚含义。检查应围绕将要使用的字段设计，同时保留完整原始响应，便于以后增加新的字段。

## 完整示例：先保留原始记录，再生成分析表

下面的程序可以直接运行。默认模式读取随示例提供的四份公开 JSON 快照，因而没有网络也能完成解析和绘图。需要获取数据库当前内容时，加入 `--refresh` 参数；程序通过 Requests 下载新的响应，并把它们写入本次输出目录。两种模式共用同一套字段检查和绘图逻辑。这样，课堂上看到的图有明确的输入版本，之后也能用新记录重新计算，而不会在刷新时悄悄改掉原来的教学数据。

### 读取、检查并比较四条 PDB 记录

默认读取随包保存的原始响应；加入 --refresh 后通过 Requests 获取当前记录并另存于输出目录。

```
"""Read four public PDB entry records, validate their identities, and plot metadata.

Default execution reads the bundled JSON snapshots.  --refresh retrieves current
records with Requests and places the new snapshots inside the output directory.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import platform
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import requests

IDS = ("1UBQ", "4HHB", "1BNA", "1D3Z")
BASE_URL = "https://data.rcsb.org/rest/v1/core/entry/"
HERE = Path(__file__).resolve().parent



def available_plot_fonts():
    """Choose installed fonts; keep a Latin fallback on every platform."""
    choices = ["Noto Sans CJK SC", "Noto Sans SC", "Microsoft YaHei", "SimHei", "DejaVu Sans"]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    return [name for name in choices if name in installed]



def fetch_record(session, pdb_id, destination):
    """Download one identified entry. A failed request never replaces a cache."""
    response = session.get(BASE_URL + pdb_id, timeout=(10, 60))
    response.raise_for_status()
    value = response.json()
    validate_record(value, pdb_id)
    destination.write_bytes(response.content)
    return value


def validate_record(record, requested_id):
    if record.get("rcsb_id") != requested_id:
        raise ValueError("The response identifier differs from the requested entry")
    methods = record.get("exptl", [])
    if not methods or not all(isinstance(x.get("method"), str) for x in methods):
        raise ValueError("The entry has no readable experimental method")
    info = record.get("rcsb_entry_info", {})
    atom_count = info.get("deposited_atom_count")
    if not isinstance(atom_count, int) or atom_count <= 0:
        raise ValueError("The deposited atom count must be a positive integer")


def select_fields(record, raw):
    info = record["rcsb_entry_info"]
    resolutions = info.get("resolution_combined", [])
    return {
        "pdb_id": record["rcsb_id"],
        "title": record["struct"]["title"],
        "method": "; ".join(x["method"] for x in record["exptl"]),
        "deposited_atoms": info["deposited_atom_count"],
        "polymer_entities": info["polymer_entity_count"],
        "resolution_angstrom": float(resolutions[0]) if resolutions else None,
        "response_bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def figures(rows, records, output, language):
    zh = language == "zh"
    plt.rcParams.update({"font.family": available_plot_fonts(),
        "font.size": 12, "axes.spines.top": False, "axes.spines.right": False,
        "svg.fonttype": "none", "axes.unicode_minus": False, "figure.facecolor": "#faf9f5",
        "axes.facecolor": "#faf9f5", "text.color": "#172534", "axes.labelcolor": "#172534"})
    blue, orange, grey = "#205b8c", "#b4482e", "#6a7782"
    fig = plt.figure(figsize=(12.2, 7.5), layout="constrained")
    grid = fig.add_gridspec(2, 2, width_ratios=[1.35, 1])
    ax = fig.add_subplot(grid[:, 0])
    positions = np.arange(len(rows))
    colours = [orange if "NMR" in r["method"] else blue for r in rows]
    ax.hlines(positions, 0, [r["deposited_atoms"] for r in rows], color=colours, lw=3)
    ax.scatter([r["deposited_atoms"] for r in rows], positions, c=colours, s=80, zorder=3)
    ax.set_yticks(positions, [r["pdb_id"] for r in rows]); ax.invert_yaxis()
    ax.set_xlim(0, max(r["deposited_atoms"] for r in rows) * 1.24)
    ax.set_xlabel("条目报告的存档原子数" if zh else "Deposited atom count reported by the entry")
    ax.set_title("A  同一字段，四个结构条目" if zh else "A  One field across four structure entries", loc="left", pad=22)
    for i, r in enumerate(rows):
        ax.text(r["deposited_atoms"] + 100, i, f'{r["deposited_atoms"]:,}', va="center", fontsize=12)
    ax.grid(axis="x", color="#dde1e3", lw=.6); ax.set_axisbelow(True)
    bx = fig.add_subplot(grid[0, 1])
    valid = [r for r in rows if r["resolution_angstrom"] is not None]
    bx.scatter([r["resolution_angstrom"] for r in valid], np.arange(len(valid)), color=blue, s=75)
    bx.set_yticks(np.arange(len(valid)), [r["pdb_id"] for r in valid]); bx.invert_yaxis()
    bx.set_xlabel("报告的分辨率 / Å" if zh else "Reported resolution / Å")
    bx.set_xlim(0, max(r["resolution_angstrom"] for r in valid) * 1.25)
    bx.set_title("B  有该字段的X射线条目" if zh else "B  X-ray entries with this field", loc="left")
    bx.grid(axis="x", color="#dde1e3", lw=.6)
    cx = fig.add_subplot(grid[1, 1]); cx.axis("off")
    txt = ("实验方法是解释数字的前提\n\n蓝：X-RAY DIFFRACTION\n橙：SOLUTION NMR\n\n1D3Z 的分辨率字段缺失，\n保留为 null；不填成 0 Å。" if zh else
           "Read the experimental method first\n\nBlue: X-RAY DIFFRACTION\nOrange: SOLUTION NMR\n\nThe resolution field for 1D3Z is absent.\nKeep null; do not substitute 0 Å.")
    cx.text(.02, .95, txt, va="top", linespacing=1.7, fontsize=12)
    fig.savefig(output / f"entry-comparison-{language}.svg", metadata={"Date": None}); plt.close(fig)
    fig, axes = plt.subplots(2, 3, figsize=(14, 7.2), gridspec_kw={"width_ratios":[1.4,1,1.45],"height_ratios":[2.5,1]}, layout="constrained")
    for axis in axes.ravel(): axis.axis("off")
    info = records[0]["rcsb_entry_info"]
    source_fields = {"rcsb_id":records[0]["rcsb_id"],"rcsb_entry_info":{key:info[key] for key in ["deposited_atom_count","polymer_entity_count","resolution_combined"]}}
    axes[0,0].set_title("A  真实响应中的选定字段" if zh else "A  Selected fields in the actual response",loc="left",fontsize=13)
    axes[0,0].text(.02,.9,json.dumps(source_fields,indent=2),va="top",family="DejaVu Sans Mono",fontsize=13,linespacing=1.45,
                   bbox={"facecolor":"#edf2f4","edgecolor":"#cad5dc","pad":14})
    axes[0,1].set_title("B  从嵌套路径到结果列" if zh else "B  Nested paths become result columns",loc="left",fontsize=13)
    for y,key,name,value,color in [(.83,'deposited_atom_count','deposited_atoms',rows[0]['deposited_atoms'],blue),
                                   (.53,'polymer_entity_count','polymer_entities',rows[0]['polymer_entities'],'#277a78'),
                                   (.23,'resolution_combined[0]','resolution_angstrom',rows[0]['resolution_angstrom'],orange)]:
        axes[0,1].text(0,y,'rcsb_entry_info.\n'+key,va='top',fontsize=12.5,color=color,linespacing=1.4)
        axes[0,1].text(0,y-.17,'→ '+name+' = '+str(value),fontsize=12,color=color)
    axes[0,2].set_title("C  同一路径用于四条记录" if zh else "C  Apply the same path to all four records",loc="left",fontsize=13)
    labels=['编号','原子数','实体数','Å'] if zh else ['ID','Atoms','Entities','Å']
    table=axes[0,2].table(cellText=[[r['pdb_id'],r['deposited_atoms'],r['polymer_entities'],r['resolution_angstrom'] if r['resolution_angstrom'] is not None else 'null'] for r in rows],colLabels=labels,cellLoc='center',bbox=[0,.14,1,.72],colWidths=[.23,.27,.25,.25])
    table.auto_set_font_size(False);table.set_fontsize(13)
    for (r,c),cell in table.get_celld().items():
        cell.set_edgecolor('#cbd7dd');cell.set_facecolor('#e7eef3' if r==1 else '#ffffff')
        if r==0:cell.set_facecolor(['#172534',blue,'#277a78',orange][c]);cell.get_text().set_color('white')
        if r==4 and c==3:cell.set_facecolor('#f3e5df');cell.get_text().set_color(orange)
    nmr=next(record for record in records if record['rcsb_id']=='1D3Z')
    missing='resolution_combined' not in nmr['rcsb_entry_info']
    axes[1,0].text(.02,.9,'1D3Z · '+nmr['exptl'][0]['method'],color=orange,fontsize=14,va='top')
    axes[1,0].text(.02,.55,('rcsb_entry_info 中没有\nresolution_combined 字段' if zh else 'resolution_combined is absent\nfrom rcsb_entry_info') if missing else 'resolution_combined is present',fontsize=12,va='top',linespacing=1.5)
    axes[1,1].text(0,.9,'→ Python: None\n→ JSON: null\n→ CSV: '+('空单元格' if zh else 'empty cell'),fontsize=13,va='top',linespacing=1.6,color=orange)
    axes[1,2].text(0,.9,'1D3Z'+(' 保留身份与实验方法\n分辨率图不放置数值点\n缺失状态随记录保存' if zh else ' keeps its identity and method\nNo point on the resolution axis\nMissing state remains in the record'),fontsize=12,va='top',linespacing=1.7)
    fig.savefig(output / f"response-to-table-{language}.svg", metadata={"Date": None})
    fig.savefig(output / f"response-to-table-{language}.png", dpi=150); plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--language", choices=["zh", "en"], default="zh")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    data_dir = HERE / "data"
    if args.refresh:
        data_dir = args.output / "refreshed-data"; data_dir.mkdir(exist_ok=True)
        with requests.Session() as session:
            session.headers["User-Agent"] = "ScientificPythonCourse/1.0"
            for pdb_id in IDS:
                fetch_record(session, pdb_id, data_dir / f"{pdb_id}.json")
                time.sleep(.2)
    rows = []; records = []
    for pdb_id in IDS:
        raw = (data_dir / f"{pdb_id}.json").read_bytes()
        record = json.loads(raw); validate_record(record, pdb_id)
        records.append(record)
        rows.append(select_fields(record, raw))
    with (args.output / "entries.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    summary = {"source": "RCSB PDB core entry API", "entry_count": len(rows), "rows": rows,
               "resolution_present": sum(r["resolution_angstrom"] is not None for r in rows),
               "missing_resolution_ids": [r["pdb_id"] for r in rows if r["resolution_angstrom"] is None]}
    (args.output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    figures(rows, records, args.output, args.language)
    print(json.dumps({"entry_count": len(rows), "resolution_present": summary["resolution_present"]}))


if __name__ == "__main__":
    main()
```

代码可以沿着数据流来阅读。`fetch_record` 负责与服务器交流并保留响应，`validate_record` 负责检查本章依赖的字段，`select_fields` 将嵌套记录变成一行，`figures` 将多行数据转成图，最后的 `main` 把输入、参数和输出组织起来。函数之间传递的都是普通的路径、字典和列表；每个函数名字都对应一个能够单独说明的动作。与把所有语句堆在一个循环中相比，这种安排使你更容易判断某个问题发生在下载、解析还是解释阶段，也方便在下一章把结果接入 Excel。

下载完成后，程序先检查返回内容，再把原始字节写入文件。保存字节的好处是，响应中的字段顺序、空白和完整内容都能保留下来；如果先解析再重新写成 JSON，科学字段可能相同，文件字节却会改变。代码同时计算 SHA-256 摘要，它相当于这份文件的内容指纹。日后重新读取同一份文件，若摘要一致，就能确认比较的是同一串字节。摘要帮助核对版本，科学正确性仍由字段含义、实验方法和研究问题共同决定，两者在工作流程中各有用途。

运行时给 `--output` 一个希望保存结果的目录，给 `--language` 选择 `zh` 或 `en`。程序会生成 `entries.csv`、`summary.json` 和两张 SVG 科学图。CSV 适合继续用 pandas 或电子表格读取，摘要 JSON 还保留了输入文件的字节数和摘要，SVG 则便于放大、排版和检查文字。输出文件的角色不同，但它们都由同一组已检查的行记录产生，因此表格和图中的数字能够相互核对。

## 空值也有科学含义：怎样比较四条记录

示例快照中的原子数分别为 660、4779、566 和 602。这里使用的是数据库返回的 `deposited_atom_count`，所以图中写成“存档原子数”。这个指标帮助了解条目规模，涉及具体的存档模型、分子组成和记录规则；它与蛋白质序列长度并不是一回事。一个氨基酸含有多个原子，记录还可能包含水分子或其他组分。为保证比较口径一致，代码对每条记录都提取同一个字段，而不是对某些条目数氨基酸、对另一些条目数坐标行。

![原子数点图、三条衍射分辨率及核磁条目说明。](https://ml-biomat.com/static/tutorials/python-scientific/figures/8e3cc8b4d324948dd086f752.svg?v=8e3cc8b4d324)

图 2四条公开记录的存档原子数与实验方法；分辨率面板保留 Å 单位，并明确标记 NMR 条目没有本例使用的衍射分辨率。

三个 X 射线衍射条目的分辨率依次为 1.80、1.74 和 1.90 Å，Å 是埃，1 Å 等于 0.1 nm。这个指标描述衍射数据能够分辨的空间尺度，在相应实验语境下，较小的数值对应更精细的空间信息。阅读时要同时看方法和结构用途：分辨率是一项重要描述，还需要结合模型检验指标和具体区域的实验支持来判断某个结构问题。图中把分辨率放在独立的面板内，横轴保留单位，并直接标出条目，读者便能看清比较的是哪一种量。

1D3Z 的方法是溶液核磁共振。它没有本例所用的衍射分辨率字段，因此表中保存 `None`，写 CSV 时留下空单元格，图上则说明当前记录没有该指标。如果把空值填成 0，排序时它会被排到最小值一端，产生“分辨率最好”的错误解释；如果把整行删除，又会丢掉一个真实有效的结构条目。这里需要保留记录身份，将缺失状态与实验方法一起展示。空值处理因此属于科学建模的一部分，不能只根据哪种写法方便绘图来决定。

本例比较选定四条记录的元数据，并通过它们说明接口、档案层级和实验方法的差异。研究某类蛋白质在数据库中的分辨率分布时，应先明确检索条件、重复结构处理、实验方法筛选以及样本范围，再收集相应条目。先写出问题对应的总体，才能判断当前数据表是否包含了足够的信息。这一步会直接影响后续代码中的筛选条件和分组方式。

## 沿着字段路径，查看同一个数值的三种表示

下面的交互把记录、字段路径和比较图放在同一个工作区。选择一个条目，右侧显示它的实验方法和选定字段；切换字段后，柱形长度和表格数值同步变化。你可以先选择“存档原子数”，观察 4HHB 的条目规模，再选择“分辨率”，看 1D3Z 怎样保留自己的位置并显示空值。图上的每条记录也可以直接选择，键盘使用原生下拉框即可完成相同操作。这里读取的是随课程保存的四份记录，页面切换不会向数据库发送请求。

### 记录与字段联动

字段路径: ``

```

```

[Figure: 比较图](https://ml-biomat.com/tutorials/python-scientific/p25/#P25-chart)

| 条目 | 方法 | 值 |
| --- | --- | --- |

最值得练习的动作，是从图上的一个值反向寻找原始字段。选中 1UBQ 与分辨率后，路径指向 `rcsb_entry_info.resolution_combined[0]`，数值为 1.8；选择聚合物实体数，则指向另一个字段，单位也变成计数。两个数都来自同一条目，却描述不同层面的属性。这样的反向检查能够发现许多表面上像“数据异常”的问题：字段选错、单位没写、把实体与实例混在一起，或把空值转成零。交互中的联动让这些关系直接可见，也为自己编写数据检查界面提供了一个完整例子。

## 让下一次分析仍然找得到这一次的输入

网络数据库会修订条目、补充字段和改进服务。重复运行一段网址相同的程序，并不自动保证收到的字节完全一样。一个可重复的分析目录因此需要同时保存原始响应和提取后的表格：前者记录当时实际收到什么，后者表达这次研究选用了什么。程序中的 JSON 快照、输入摘要和字段路径将这两件事接在一起。原始文件保持完整，分析脚本则可以不断改进，例如加入发布日期、分子名称或相关文献，而不必为了每个新问题重新下载全部输入。

![真实 JSON 的嵌套字段、提取路径与四记录表逐项对应；下方追踪 1D3Z 缺失分辨率在 Python、JSON、CSV 和图中的一致表达。](https://ml-biomat.com/static/tutorials/python-scientific/figures/e27c45e00983a181c4c8353c.svg?v=e27c45e00983)

图 3真实 JSON 的嵌套字段、提取路径与四记录表逐项对应；下方追踪 1D3Z 缺失分辨率在 Python、JSON、CSV 和图中的一致表达。

图中的三列把这条追踪关系展开：左侧从真实原始响应中选出相关字段，中间写出嵌套路径及结果列名，右侧将同一路径用于四条记录。颜色沿着原子数、实体数和分辨率三个字段保持一致，因此可以直接追踪 1UBQ 的 1.8 怎样进入结果表。下方单独追踪 1D3Z：原始记录没有分辨率字段，Python 保存为 None，导出的 JSON 保存为 null，CSV 保留空单元格，比较图则保留方法说明。这些表示方式服务于不同文件格式，保存的是同一个科学状态。调整表格定义时，应同时更新路径和列名，使后来的读者能够区分直接读取、筛选取得和进一步计算的数值。

在实际研究中，还应把接口地址、获取时间、数据许可和使用的字段定义与结果一起保存。公开 PDB 档案数据采用 CC0，RCSB 页面同时说明部分整合的外部资源遵循各自的使用条款。本章使用的是四条核心结构记录，保留其公开身份和学术引用入口。对于另一个数据库，可以沿用相同的代码结构，但应先读它的接口和数据使用说明，再安排缓存、请求频率与引用方式。清楚记录输入身份，能够让合作者把精力放在科学问题上，而不用猜测一列数值是从哪里来的。

## 把这个小流程扩展成自己的数据入口

最自然的练习是再加入一个条目，并在运行前写下你预期检查的内容：编号是否匹配、实验方法是什么、分辨率字段是否适用、原子数是否为正整数。随后刷新新记录，查看原始 JSON，再读输出表和图，确认新增条目确实沿着同一套规则进入结果。若条目包含多种实验方法，保留方法列表提供的信息，重新思考比较图该怎样分组。这个练习把“改一个编号”推进成“验证一个数据对象”，也使你逐渐积累适合自己研究对象的检查规则。

当条目数量增加，可以把编号列表放进文本文件，先检查重复编号，再逐条读取缓存；需要更新的条目才访问网络。把失败记录单独列出，保留错误类型和编号，之后针对这些记录重试。对成功结果和失败结果分别保存明确的状态，比在异常发生后悄悄跳过更容易追踪。再往后，可以将提取函数交给测试程序，使用一个正常条目、一个缺少可选字段的条目和一个身份不符的条目，检查程序是否作出预期响应。[程序检查与复用](https://ml-biomat.com/tutorials/python-scientific/p27/)会继续展开这一做法。

本章建立的入口可直接连接后面的科学计算：结构表可以交给 pandas 分组，坐标可以交给 Biopython 或 MDAnalysis 读取，结果可以写入 [Excel 报告](https://ml-biomat.com/tutorials/python-scientific/p26/)。无论接入哪一个工具，都保留“条目身份—原始响应—字段定义—结果”的关系。这样，当一个图中的点引起兴趣时，研究者能够回到具体结构和实验条件继续追问，而不是停留在一张失去上下文的数字表上。

[下载本篇完整代码与数据](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P25.zip)

解压后按 README 运行；代码与本篇示例一致。

## 参考与延伸阅读

1. [RCSB PDB Data API](https://data.rcsb.org/)

   REST 资源层级、条目字段和请求示例。
2. [Requests: Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)

   GET、JSON 解析、HTTP 错误与超时语义。
3. [RCSB PDB Policies](https://www.rcsb.org/pages/policies)

   PDB 核心数据 CC0 许可与档案文献引用。

   PDB core archive data: CC0; site documentation: CC BY 4.0.
4. [The Protein Data Bank: a computer-based archival file for macromolecular structures (1977)](https://doi.org/10.1016/S0022-2836%2877%2980200-3)

   结构数据计算机档案的历史背景。
5. [1UBQ · Structure of ubiquitin refined at 1.8 A resolution. (1987)](https://doi.org/10.1016/0022-2836%2887%2990679-6)

   对应结构条目的原始研究。[查看 1UBQ 条目](https://www.rcsb.org/structure/1UBQ)。
6. [4HHB · The crystal structure of human deoxyhaemoglobin at 1.74 A resolution (1984)](https://doi.org/10.1016/0022-2836%2884%2990472-8)

   对应结构条目的原始研究。[查看 4HHB 条目](https://www.rcsb.org/structure/4HHB)。
7. [1BNA · Structure of a B-DNA dodecamer: conformation and dynamics. (1981)](https://doi.org/10.1073/pnas.78.4.2179)

   对应结构条目的原始研究。[查看 1BNA 条目](https://www.rcsb.org/structure/1BNA)。
8. [1D3Z · Validation of Protein Structure from Anisotropic Carbonyl Chemical Shifts in a Dilute Liquid Crystalline Phase (1998)](https://doi.org/10.1021/ja9812610)

   对应结构条目的原始研究。[查看 1D3Z 条目](https://www.rcsb.org/structure/1D3Z)。
