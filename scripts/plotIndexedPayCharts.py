from pathlib import Path
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
WAGES_PATH = ROOT / "data" / "cleaned" / "wages.csv"
OUTPUT_DIR = ROOT / "data" / "cleaned" / "charts"


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return slug or "company"


def build_chart(company_wages, output_path):
    company_name = company_wages["Company"].iloc[0]
    company_wages = company_wages.sort_values("Year").copy()

    company_wages["ceo_pay"] = company_wages["ceo_pay_k"] * 1000
    company_wages["ceo_index"] = company_wages["ceo_pay"] / company_wages["ceo_pay"].iloc[0] * 100
    company_wages["median_index"] = company_wages["m_pay"] / company_wages["m_pay"].iloc[0] * 100

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        company_wages["Year"],
        company_wages["ceo_index"],
        marker="o",
        linewidth=2.5,
        color="#d62728",
        label="CEO pay index",
    )
    ax.plot(
        company_wages["Year"],
        company_wages["median_index"],
        marker="o",
        linewidth=2.5,
        color="#1f77b4",
        label="Median pay index",
    )

    ax.set_title(f"{company_name}: Indexed CEO Pay vs Median Pay", fontsize=16, weight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Index (first year = 100)")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend()

    fig.text(
        0.125,
        0.93,
        "Both series rebased to 100 in the first available year",
        fontsize=10,
        color="#555555",
    )

    fig.tight_layout(rect=[0, 0, 1, 0.9])
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    wages = pd.read_csv(WAGES_PATH)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for existing_chart in OUTPUT_DIR.glob("*.png"):
        existing_chart.unlink()

    company_names = sorted(wages["Company"].dropna().unique())

    for company_name in company_names:
        company_wages = wages[wages["Company"] == company_name].copy()
        output_path = OUTPUT_DIR / f"{slugify(company_name)}_indexed_pay.png"
        build_chart(company_wages, output_path)
        print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
