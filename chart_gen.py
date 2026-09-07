# -*- coding: utf-8 -*-
"""Chart + table helpers for ml-biomat-blog posts.

Run with the anaconda python (has matplotlib + Pillow).
Examples:
  python chart_gen.py line --csv data.csv --x epoch --y loss --out fig.png \
      --title "Loss curve" --webp
  python chart_gen.py table --csv data.csv --max-rows 20
"""
import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager


def _cjk_prop():
    for p in (r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\SimHei.ttf"):
        if Path(p).exists():
            return font_manager.FontProperties(fname=p)
    return None


_CJ = _cjk_prop()
if _CJ is not None:
    plt.rcParams["font.sans-serif"] = [_CJ.get_name()]
plt.rcParams["axes.unicode_minus"] = False

ACCENT = "#2563eb"
GRID = "#e2e8f0"


class ChartKit:
    """Small plot factory so common look/feel stays consistent."""

    def __init__(self, dpi=120, size=(1200, 640)):
        self.dpi = dpi
        self.size = size

    def _new(self, title, xlabel, ylabel):
        fig, ax = plt.subplots(figsize=(self.size[0] / self.dpi, self.size[1] / self.dpi), dpi=self.dpi)
        ax.set_facecolor("white")
        fig.patch.set_facecolor("white")
        ax.grid(True, color=GRID, linewidth=0.8, alpha=0.7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if title:
            ax.set_title(title, fontsize=16, fontweight="bold", pad=14)
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)
        ax.tick_params(labelsize=10)
        return fig, ax

    def _save(self, fig, out, webp):
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            print("skip (exists):", out)
            return
        if webp:
            fig.savefig(out.with_suffix(".png"), format="png", bbox_inches="tight")
            from PIL import Image
            Image.open(out.with_suffix(".png")).convert("RGB").save(out, "WEBP", quality=85, method=6)
            out.with_suffix(".png").unlink()
        else:
            fig.savefig(out, bbox_inches="tight")
        plt.close(fig)
        print("saved:", out)

    @staticmethod
    def read_csv(csv_path):
        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            return list(csv.DictReader(f))

    def line(self, csv_path, x, y, out, title="", xlabel="", ylabel="", webp=False):
        rows = self.read_csv(csv_path)
        xs = [float(r[x]) for r in rows]
        ys = [float(r[y]) for r in rows]
        fig, ax = self._new(title, xlabel, ylabel)
        ax.plot(xs, ys, color=ACCENT, linewidth=2)
        self._save(fig, out, webp)

    def bar(self, csv_path, x, y, out, title="", xlabel="", ylabel="", webp=False):
        rows = self.read_csv(csv_path)
        xs = [str(r[x]) for r in rows]
        ys = [float(r[y]) for r in rows]
        fig, ax = self._new(title, xlabel, ylabel)
        ax.bar(xs, ys, color=ACCENT, alpha=0.9)
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
        self._save(fig, out, webp)

    def scatter(self, csv_path, x, y, out, title="", xlabel="", ylabel="", webp=False):
        rows = self.read_csv(csv_path)
        xs = [float(r[x]) for r in rows]
        ys = [float(r[y]) for r in rows]
        fig, ax = self._new(title, xlabel, ylabel)
        ax.scatter(xs, ys, color=ACCENT, alpha=0.75, s=24)
        self._save(fig, out, webp)

    def table(self, csv_path, max_rows=20):
        rows = self.read_csv(csv_path)
        if not rows:
            return ""
        heads = list(rows[0].keys())
        lines = ["| " + " | ".join(h for h in heads) + " |",
                 "| " + " | ".join("---" for _ in heads) + " |"]
        for r in rows[:max_rows]:
            lines.append("| " + " | ".join(r[h] for h in heads) + " |")
        if len(rows) > max_rows:
            lines.append(f"| _(showing {max_rows} of {len(rows)} rows)_ |" + " | " * (len(heads) - 1) )
        return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=("line", "bar", "scatter", "table"))
    ap.add_argument("--csv")
    ap.add_argument("--x")
    ap.add_argument("--y")
    ap.add_argument("--out")
    ap.add_argument("--title", default="")
    ap.add_argument("--xlabel", default="")
    ap.add_argument("--ylabel", default="")
    ap.add_argument("--webp", action="store_true")
    ap.add_argument("--max-rows", type=int, default=20)
    a = ap.parse_args()
    ck = ChartKit()
    if a.kind == "table":
        print(ck.table(a.csv, a.max_rows))
    else:
        getattr(ck, a.kind)(a.csv, a.x, a.y, a.out, a.title, a.xlabel, a.ylabel, a.webp)


if __name__ == "__main__":
    main()