# Retrieving Traceable Data from Public APIs

Source: https://ml-biomat.com/tutorials/python-scientific/p25/en/
Language: en

Connect URLs, nested JSON, scientific meaning, and reproducible tables through four Protein Data Bank entries.

## How a structure table travels from a database to your computer

A comparison of protein or nucleic-acid structures often begins with a modest table: the name of each structure, its experimental method, the number of deposited atoms, and its resolution. Copying two records from a website is manageable. With dozens of records, the demanding work becomes keeping the columns consistent, noticing when a measurement does not apply, and revisiting records after they change. Python can perform the repeated retrieval and transformation. An application programming interface, or API, provides an agreed entrance for programs: a request identifies the desired resource, the service returns structured data, and the analysis selects and interprets the fields needed for a scientific question.

This chapter retrieves four entries from the RCSB Protein Data Bank: 1UBQ, 4HHB, 1BNA, and 1D3Z. They concern ubiquitin, haemoglobin, DNA, and a solution-NMR ubiquitin structure. The selection has a teaching purpose. Three records contain a diffraction-resolution value; the fourth asks us to handle a measurement that does not apply to its experimental method. The completed example produces four original JSON responses, a CSV table with clearly defined columns, and figures that explain the recorded values. You will also be able to trace a number in that table back to its entry, its nested field, and the particular response file used to generate it.

Think of an API as a library's standardized service desk. The address identifies the requested item, the request specifies an operation, the response status reports what happened, and the response body contains the material delivered. A successful transaction still leaves a scientific question: is this the right item, and does it contain what the analysis needs? We therefore check communication and content separately before connecting them. This separation gives each part of the program a clear job and makes the workflow transferable to another database.

## From shared coordinates to connected scientific records

The Protein Data Bank was announced in 1971. Atomic coordinates are among the central results that structural research needs to share: another researcher can inspect molecular shape, measure distances, compare binding sites, or investigate a new problem using those coordinates. As the archive grows, the accompanying descriptions become increasingly valuable. A molecule called ubiquitin can be studied by different experimental methods, under different conditions, and in multiple independent depositions. Organizing this information requires an entry identity connected to experimental methods, molecular composition, and publications. The four-character identifiers in this example locate archive entries; each identifier describes a particular record rather than the single universal shape of a protein.

This organization explains how a website, a coordinate file, and an API work together. The website supports human reading, a coordinate file carries the spatial model, and the API supports programmatic extraction of structured information. Our request uses the `core/entry` resource and returns entry-level descriptions. An atom count in that response is archive metadata. Calculating the distance between two atoms would require the coordinates themselves. Identifying the level of information needed is an early design decision: it determines which resource the program should request and which objects it should create.

![Development of the shared archive and entry/entity/instance levels.](https://ml-biomat.com/static/tutorials/python-scientific/figures/42e1da4e5926cf3194d793bf.svg?v=42e1da4e5926)

Figure 1Original archive diagram linking the 1971 PDB announcement and 1977 computer-based archive paper to current website, API, and coordinate resources. Entry, entity, and instance levels are distinguished below.

An entry can also be described through polymer entities and chain instances. An entity represents a particular polymer molecule, such as a particular amino-acid sequence, while a chain is an instance occurring in the structure. One entity can have several instances. The value of `polymer_entity_count` in 4HHB is 2: it counts two polymer entities, not two chains. This biological distinction has immediate consequences for programming. It determines column names and table joins. Calling the output column `polymer_entities` preserves the level of the original field and helps the next person interpret the number correctly.

## Separate a request into steps you can inspect

The complete address for 1UBQ is `https://data.rcsb.org/rest/v1/core/entry/1UBQ`. The first part identifies the service and resource type; the final identifier selects an entry. In Requests, `session.get(...)` sends an HTTP GET request and returns a response object containing the status, headers, and body. Calling `raise_for_status()` exposes HTTP error responses, such as an unavailable resource or a server error. Calling `response.json()` then interprets the body as JSON. These operations answer different questions: how did the server respond, and can its body be parsed using JSON syntax?

A JSON object enclosed in braces usually becomes a Python dictionary. An ordered array in square brackets becomes a list, numbers become numeric values, and `null` becomes `None`. The experimental method is nested inside a list: accessing a method involves selecting `exptl`, selecting an item from that list, and reading its `method` field. That indexing path describes the structure of the data. A list also allows more than one item, so the example collects every reported method rather than assuming that one method must always be present. Once this connection between JSON and Python is clear, unfamiliar nested fields can be inspected one layer at a time.

Network waiting needs an explicit setting. The example uses `timeout=(10, 60)`, giving the connection and read stages waiting limits in seconds. These settings allow a stalled request to end when a service cannot be reached or stops delivering data. The read timeout concerns waiting between received data, rather than guaranteeing that the entire task finishes within seventy seconds. With four entries, sequential requests and a short interval are sufficient. Before scaling to many entries, inspect the service's query and bulk-retrieval facilities, reuse downloaded records, and design requests around the actual data needed.

A valid JSON document still needs to match the analysis. The example's `validate_record` function checks that the returned entry identifier matches the request, that the experimental methods form a nonempty list of strings, and that the deposited atom count is a positive integer. Each check follows from the table's purpose. A wrong identifier assigns every value to the wrong object; a missing method removes the context required to interpret resolution; an invalid count makes the size comparison meaningless. Checks should cover the fields the analysis relies on, while the complete original response remains available for later additions.

## A complete example: preserve the response before making the table

The program below runs directly. Its default mode reads four public JSON snapshots included with the example, so parsing and plotting work offline. Adding `--refresh` retrieves current responses with Requests and saves them in the new output directory. Both modes use the same validation, extraction, and plotting functions. The figures shown in this chapter therefore have a definite input version, while a later run can use updated records without silently replacing the teaching inputs.

### Read, validate, and compare four PDB records

Read bundled original responses by default; add --refresh to retrieve current records with Requests into the output directory.

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

Read the program by following the data. `fetch_record` communicates with the service and saves a response; `validate_record` checks the fields used here; `select_fields` transforms a nested record into one row; `figures` makes figures from the collected rows; and `main` organizes parameters, inputs, and outputs. Paths, dictionaries, and lists pass between these functions. Each function corresponds to an action that can be explained independently. This organization makes it easier to locate a problem in downloading, parsing, or interpretation and to connect the resulting table to the Excel workflow in the next chapter.

The download function validates the received record before writing its original bytes. Keeping those bytes preserves the full response, including field order and whitespace. Parsing a response and writing a newly formatted JSON file can preserve the scientific fields while changing its byte representation. The program also calculates a SHA-256 digest, a content fingerprint that can be recalculated when the file is read again. Matching digests identify matching byte sequences. Scientific correctness has a different role: it comes from the meanings of the fields, the experimental method, and the question being asked. Both file identity and scientific interpretation belong in a reproducible workflow.

Use `--output` to choose a result directory and `--language` to select `zh` or `en`. The program writes `entries.csv`, `summary.json`, and two SVG figures. The CSV can be read with pandas or a spreadsheet. The summary retains input byte counts and digests as well as extracted values. SVG graphics remain readable when enlarged and are convenient for publication layout. These files serve different purposes, but all derive from the same validated rows, allowing the table and figures to be checked against each other.

## A missing value can carry scientific meaning

The deposited atom counts in the example snapshots are 660, 4779, 566, and 602. These values come from `deposited_atom_count`, so the figure explicitly labels them as deposited atom counts. They describe the size of particular deposited records, whose contents depend on the model, molecular composition, and archive conventions. An atom count is different from an amino-acid sequence length: one amino acid contains several atoms, and a coordinate model may include water molecules or other components. The program extracts the same field from every record to maintain a consistent definition across the comparison.

![Atom-count plot, three diffraction resolutions, and the NMR missing-value state.](https://ml-biomat.com/static/tutorials/python-scientific/figures/60536867a1b403215f4663ef.svg?v=60536867a1b4)

Figure 2Deposited atom counts and experimental methods for four public records. The resolution panel retains ångström units and identifies the absent diffraction-resolution value for the NMR entry.

The three X-ray diffraction entries have resolution values of 1.80, 1.74, and 1.90 Å. An ångström is 0.1 nm. In the context of diffraction, resolution describes the spatial scale of information that the data can resolve, with smaller values corresponding to finer spatial information. The method and intended structural question still matter: model-validation measures and the experimental support for a specific region also contribute to an assessment. The resolution plot therefore has its own axis with units and directly identifies the entries being compared.

Entry 1D3Z was determined using solution NMR. It does not have the diffraction-resolution field used by this example. The program preserves that state as `None`, writes an empty CSV cell, and explains the absence in the figure. Filling the field with zero would place it at the smallest end of a resolution ranking and create a false interpretation. Deleting the entire row would discard a valid structure entry. Keeping the identity, experimental method, and missing-value state together provides the information needed to interpret the record. Missing-data handling is consequently part of the scientific model of the table.

The four entries were chosen to expose interface structure, archive levels, and method differences. They are a teaching collection, rather than a statistical sample of the archive. The plotted comparison answers a question about these four records. A question about the resolution distribution of a protein family would require explicit search criteria, handling of repeated structures, method selection, and a defined population of entries. Writing down that population before collecting data helps determine whether the resulting table contains the right information and which grouping or filtering operations are appropriate.

## Follow one value through its record, field, and plot

The interactive workspace connects entry selection, a nested field path, and a comparison plot. Select an entry to inspect its method and selected value. Change the field to update the bars and table together. Start with deposited atoms to inspect the scale of 4HHB, then choose resolution and observe how 1D3Z retains its identity while displaying an absent value. Records in the plot can also be selected directly; the native select controls provide the same interaction with a keyboard. This workspace reads the four bundled snapshots and sends no database request when a selection changes.

### Linked records and fields

Field path: ``

```

```

[Figure: Comparison](https://ml-biomat.com/tutorials/python-scientific/p25/en/#P25-chart)

| Entry | Method | Value |
| --- | --- | --- |

A useful exercise is to work backwards from a plotted value. With 1UBQ and resolution selected, the path is `rcsb_entry_info.resolution_combined[0]` and the value is 1.8. Selecting polymer entities changes the path and changes the quantity to a count. Both values belong to one entry, yet describe different properties. Following the path can reveal problems that initially look like unusual data: an incorrect field, an omitted unit, an entity confused with an instance, or a missing value converted to zero. The linked views make these relationships visible and provide a practical model for an inspection interface of your own.

## Keep the inputs available for the next analysis

Online databases revise entries, add fields, and improve services. Repeating a request to the same address does not guarantee an identical sequence of response bytes. A reproducible analysis directory therefore retains both the original responses and the extracted table. The responses record what was received; the table expresses what this analysis selected. Snapshot files, input digests, and field paths connect those two roles. With complete original records available, an extraction script can be improved to include release dates, molecular names, or publications without requesting the same input for every new question.

![Actual nested JSON fields, extraction paths, and the four-record table are connected explicitly. The lower row follows the absent 1D3Z resolution through Python, JSON, CSV, and the figure.](https://ml-biomat.com/static/tutorials/python-scientific/figures/ed8d3e4819046aa050391d62.svg?v=ed8d3e481904)

Figure 3Actual nested JSON fields, extraction paths, and the four-record table are connected explicitly. The lower row follows the absent 1D3Z resolution through Python, JSON, CSV, and the figure.

The figure expands that traceability across three columns. Selected fields from the actual response appear on the left, nested paths and output names in the middle, and the four-record table on the right. Consistent colors follow atom count, entity count, and resolution, so the value 1.8 for 1UBQ can be traced directly into the table. The lower row follows 1D3Z separately: its original resolution field is absent, Python retains None, exported JSON retains null, CSV has an empty cell, and the figure preserves the method context. These formats express the same scientific state. Updating paths and column names when a table definition changes helps another reader distinguish directly retrieved, selected, and calculated quantities.

A research workflow should also retain the endpoint, retrieval time, data terms, and field definitions alongside its results. Public PDB archive data are released under CC0; RCSB's policy separately identifies integrated external resources that follow their own terms. This example uses four core entry records and preserves their public identities and scientific citation links. For another database, the same program structure remains useful, while its interface documentation and data terms determine caching, request frequency, and attribution. Clearly identified inputs let collaborators investigate the scientific question without reconstructing the origin of an unexplained column.

## Develop this workflow into your own data entrance

Add one entry and write down the checks you expect before running the program: the returned identifier, experimental method, applicability of resolution, and a positive integer atom count. Retrieve the record, inspect its original JSON, and compare the resulting table and plot to those expectations. If the entry reports several methods, preserve that information and reconsider how the comparison should be grouped. This exercise turns a change of identifier into the validation of a data object and gradually builds checks appropriate to the molecules you study.

For a larger collection, place identifiers in a text file, check duplicates, and read available cached records before making network requests. Keep failed requests in a separate list with their identifiers and error types, then retry those records deliberately. Explicit success and failure states are easier to investigate than silently skipped rows. Extraction functions can subsequently be tested with a normal record, a record missing an optional field, and a record with the wrong identity. The chapter on [testable and reusable programs](https://ml-biomat.com/tutorials/python-scientific/p27/en/) develops this approach.

This entrance connects naturally to later scientific work. pandas can group the structure table, Biopython or MDAnalysis can read coordinate data, and the results can become an [Excel report](https://ml-biomat.com/tutorials/python-scientific/p26/en/). Preserve the connection between entry identity, original response, field definition, and result as the data move between tools. When an interesting point appears in a figure, that connection allows the investigation to return to a particular structure and its experimental context.

[Download complete code and data](https://ml-biomat.com/static/tutorials/python-scientific/downloads/P25.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [RCSB PDB Data API](https://data.rcsb.org/)

   REST resource levels, entry fields, and request examples.
2. [Requests: Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)

   GET, JSON parsing, HTTP errors, and timeout semantics.
3. [RCSB PDB Policies](https://www.rcsb.org/pages/policies)

   CC0 terms for PDB core data and archive publication citations.

   PDB core archive data: CC0; site documentation: CC BY 4.0.
4. [The Protein Data Bank: a computer-based archival file for macromolecular structures (1977)](https://doi.org/10.1016/S0022-2836%2877%2980200-3)

   Historical context for the computer-based structural archive.
5. [1UBQ · Structure of ubiquitin refined at 1.8 A resolution. (1987)](https://doi.org/10.1016/0022-2836%2887%2990679-6)

   Original study for this structure entry. [Inspect entry 1UBQ](https://www.rcsb.org/structure/1UBQ).
6. [4HHB · The crystal structure of human deoxyhaemoglobin at 1.74 A resolution (1984)](https://doi.org/10.1016/0022-2836%2884%2990472-8)

   Original study for this structure entry. [Inspect entry 4HHB](https://www.rcsb.org/structure/4HHB).
7. [1BNA · Structure of a B-DNA dodecamer: conformation and dynamics. (1981)](https://doi.org/10.1073/pnas.78.4.2179)

   Original study for this structure entry. [Inspect entry 1BNA](https://www.rcsb.org/structure/1BNA).
8. [1D3Z · Validation of Protein Structure from Anisotropic Carbonyl Chemical Shifts in a Dilute Liquid Crystalline Phase (1998)](https://doi.org/10.1021/ja9812610)

   Original study for this structure entry. [Inspect entry 1D3Z](https://www.rcsb.org/structure/1D3Z).
