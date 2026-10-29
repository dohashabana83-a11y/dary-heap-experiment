"""Compare binary, ternary and 4-ary heaps for INSERT and EXTRACT-MAX.

Usage:
    python benchmark.py
    python benchmark.py --sizes 100000 500000 --repeats 5
Outputs:
    results/results.csv   times and comparison counts
    results/heaps.png     bar charts of the results
"""

from __future__ import annotations

import argparse
import csv
import os
import random
import time

from dary_heap import DaryHeap

NAMES = {2: "binary (d=2)", 3: "ternary (d=3)", 4: "4-ary (d=4)"}


def run(d: int, data: list, repeats: int):
    best_ins = best_ext = float("inf")
    cmp_ins = cmp_ext = 0
    for _ in range(repeats):
        h = DaryHeap(d)
        t0 = time.perf_counter()
        for x in data:
            h.insert(x)
        t1 = time.perf_counter()
        cmp_ins = h.comparisons
        h.comparisons = 0
        prev = None
        for _ in range(len(data)):
            v = h.extract_max()
            assert prev is None or prev >= v, "extract order is wrong"
            prev = v
        t2 = time.perf_counter()
        cmp_ext = h.comparisons
        best_ins = min(best_ins, t1 - t0)
        best_ext = min(best_ext, t2 - t1)
    return best_ins, best_ext, cmp_ins, cmp_ext


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", type=int, nargs="+", default=[100_000, 500_000])
    parser.add_argument("--ds", type=int, nargs="+", default=[2, 3, 4])
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--out", default="results")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    rows = []
    for n in args.sizes:
        random.seed(42)
        data = [random.randint(0, 10**9) for _ in range(n)]
        for d in args.ds:
            t_ins, t_ext, c_ins, c_ext = run(d, data, args.repeats)
            rows.append({"n": n, "d": d,
                         "insert_s": round(t_ins, 4), "extract_s": round(t_ext, 4),
                         "insert_cmp": c_ins, "extract_cmp": c_ext})
            print(f"n={n:>8,} d={d}  insert {t_ins:6.3f}s ({c_ins:>10,} cmp)   "
                  f"extract-max {t_ext:6.3f}s ({c_ext:>10,} cmp)")

    csv_path = os.path.join(args.out, "results.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Saved {csv_path}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed - skipping plot")
        return

    n_big = max(args.sizes)
    sel = [r for r in rows if r["n"] == n_big]
    labels = [NAMES.get(r["d"], f"d={r['d']}") for r in sel]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    for ax, key, title in (
        (axes[0], "insert", "INSERT"),
        (axes[1], "extract", "EXTRACT-MAX"),
    ):
        ax.bar(labels, [r[f"{key}_s"] for r in sel], color=["#4c78a8", "#f58518", "#54a24b"][:len(sel)])
        ax.set_title(f"{title} ({n_big:,} operations)")
        ax.set_ylabel("Time (seconds)")
        ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    png_path = os.path.join(args.out, "heaps.png")
    fig.savefig(png_path, dpi=150)
    print(f"Saved {png_path}")


if __name__ == "__main__":
    main()
