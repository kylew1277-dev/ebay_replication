import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('input/PaidSearch.csv')

# Parse date column
df['date'] = pd.to_datetime(df['date'])

# Log revenue
df['log_revenue'] = np.log(df['revenue'])
# -----------------------------
# Step 2 — Pivot tables (treated vs untreated)
# -----------------------------

treated = df[df["search_stays_on"] == 0].copy()
untreated = df[df["search_stays_on"] == 1].copy()

treated_pivot = treated.pivot_table(
    index="dma",
    columns="treatment_period",
    values="log_revenue",
    aggfunc="mean"
)
untreated_pivot = untreated.pivot_table(
    index="dma",
    columns="treatment_period",
    values="log_revenue",
    aggfunc="mean"
)
# Rename columns: 0 -> pre, 1 -> post
treated_pivot = treated_pivot.rename(columns={0: "log_revenue_pre", 1: "log_revenue_post"})
untreated_pivot = untreated_pivot.rename(columns={0: "log_revenue_pre", 1: "log_revenue_post"})

# Compute post - pre
treated_pivot["log_revenue_diff"] = treated_pivot["log_revenue_post"] - treated_pivot["log_revenue_pre"]
untreated_pivot["log_revenue_diff"] = untreated_pivot["log_revenue_post"] - untreated_pivot["log_revenue_pre"]

# Save pivot tables
treated_pivot.to_csv("temp/treated_pivot.csv")
untreated_pivot.to_csv("temp/untreated_pivot.csv")
# -----------------------------
# Step 3 — Summary stats
# -----------------------------

n_treated_dmas = treated["dma"].nunique()
n_untreated_dmas = untreated["dma"].nunique()

date_min = df["date"].min().date()
date_max = df["date"].max().date()

print(f"Treated DMAs: {n_treated_dmas}")
print(f"Untreated DMAs: {n_untreated_dmas}")
print(f"Date range: {date_min} to {date_max}")

# -----------------------------
# Step 4 — Figure 5.2 (avg revenue over time)
# -----------------------------

# Ensure output directory exists
import os
os.makedirs("output/figures", exist_ok=True)

# Average revenue by date and group
daily_rev = (
    df.groupby(["date", "search_stays_on"])["revenue"]
      .mean()
      .reset_index()
)

# Pivot so we can plot two lines easily
daily_pivot = daily_rev.pivot(index="date", columns="search_stays_on", values="revenue")
daily_pivot = daily_pivot.sort_index()

plt.figure()
# Control = 1, Treatment = 0
plt.plot(daily_pivot.index, daily_pivot[1], label="Control (search stays on)")
plt.plot(daily_pivot.index, daily_pivot[0], label="Treatment (search goes off)")

# Vertical treatment date line
plt.axvline(pd.Timestamp("2012-05-22"), linestyle="--")

plt.xlabel("Date")
plt.ylabel("Revenue")
plt.title("Figure 5.2: Average Revenue Over Time (Treatment vs Control)")
plt.legend()

plt.tight_layout()
plt.savefig("output/figures/figure_5_2.png")
plt.close()

# -----------------------------
# Step 5 — Figure 5.3 (log-scale revenue gap over time)
# -----------------------------

daily_logrev = (
    df.groupby(["date", "search_stays_on"])["log_revenue"]
      .mean()
      .reset_index()
)

# Pivot to get one column per group for each date
daily_log_pivot = daily_logrev.pivot(index="date", columns="search_stays_on", values="log_revenue")
daily_log_pivot = daily_log_pivot.sort_index()

# Difference: control (1) - treatment (0)
daily_log_pivot["log_gap"] = daily_log_pivot[1] - daily_log_pivot[0]

plt.figure()
plt.plot(daily_log_pivot.index, daily_log_pivot["log_gap"])

plt.axvline(pd.Timestamp("2012-05-22"), linestyle="--")

plt.xlabel("Date")
plt.ylabel("log(rev_control) - log(rev_treat)")
plt.title("Figure 5.3: Log Revenue Gap (Control - Treatment) Over Time")

plt.tight_layout()
plt.savefig("output/figures/figure_5_3.png")
plt.close()

