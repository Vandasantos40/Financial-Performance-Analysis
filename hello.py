import pandas as pd
import matplotlib.ticker as ticker
from pathlib import Path

financial_data = [
{"year": 2023, "revenue": 150000, "cost": 95000, "target": 145000, "cost_target": 96000, "variable_cost": 57000},
{"year": 2024, "revenue": 165000, "cost": 98000, "target": 160000, "cost_target": 100000, "variable_cost": 58800},
{"year": 2025, "revenue": 180000, "cost": 100000, "target": 175000, "cost_target": 102000, "variable_cost": 60000},
{"year": 2026, "revenue": 200000, "cost": 95000, "target": 190000, "cost_target": 100000, "variable_cost": 57000}
]

df = pd.DataFrame(financial_data)
df["revenue_variance"] = df["revenue"] - df["target"]
df["cost_variance"] = df["cost"] - df["cost_target"]
df["cost_variance_pct"] = df["cost_variance"] / df["cost_target"]
df["revenue_variance_pct"] = df["revenue_variance"] / df["target"]
df["variable_cost_pct"] = df["variable_cost"] / df["revenue"]
df["profit"] = df["revenue"] - df["cost"]
df["profit_margin"] = df["profit"] / df["revenue"]
df["revenue_growth"] = df["revenue"].pct_change()
df["profit_growth"] = df["profit"].pct_change()
df["variable_cost_growth"] = df["variable_cost"].pct_change()

best_profit_growth = df["profit_growth"].idxmax()

print("Year with highest profit growth:")
print(df.loc[best_profit_growth, "year"])

best_margin = df["profit_margin"].idxmax()

print("Year with highest profit margin:")
print(df.loc[best_margin, "year"])

latest_year = df["year"].iloc[-1]
latest_revenue = df["revenue"].iloc[-1]
latest_profit = df["profit"].iloc[-1]
latest_margin = df["profit_margin"].iloc[-1]
latest_revenue_growth = df["revenue_growth"].iloc[-1]
latest_profit_growth = df["profit_growth"].iloc[-1]

print()
print("EXECUTIVE SUMMARY")
print("-----------------")
print(f"In {latest_year}, revenue reached ${latest_revenue:,.0f}.")
print(f"Profit reached ${latest_profit:,.0f}.")
print(f"Profit margin was {latest_margin:.1%}.")
print(f"Revenue growth was {latest_revenue_growth:.1%}.")
print(f"Profit growth was {latest_profit_growth:.1%}.")

if latest_profit_growth > latest_revenue_growth:
    print("Profit growth exceeded revenue growth.")

if df["profit_margin"].iloc[-1] > df["profit_margin"].iloc[-2]:
    print("Profit margin improved compared with the previous year.")

previous_revenue = df["revenue"].iloc[-2]
latest_cost = df["cost"].iloc[-1]
previous_cost = df["cost"].iloc[-2]

if latest_cost < previous_cost:
    print("Cost decreased compared with the previous year.")

if latest_revenue > previous_revenue and latest_cost < previous_cost:
    print("Revenue increased while costs decreased.")

cost_change = (latest_cost - previous_cost) / previous_cost

print(f"Cost changed by {cost_change:.1%} compared with the previous year.")

cost_saving = previous_cost - latest_cost

print(f"Cost saving was ${cost_saving:,.0f} compared with the previous year.")

latest_revenue_variance_pct = df["revenue_variance_pct"].iloc[-1]
variance_threshold = 0.05
if latest_revenue_variance_pct > 0 and abs(latest_revenue_variance_pct) >= variance_threshold:
    print(f"Revenue exceeded the target by {latest_revenue_variance_pct:.1%}, and the variance requires attention.")

elif latest_revenue_variance_pct > 0 and abs(latest_revenue_variance_pct) < variance_threshold:
    print(f"Revenue exceeded the target by {latest_revenue_variance_pct:.1%}, but the variance is within the acceptable range.")

elif latest_revenue_variance_pct < 0:
    print(f"Revenue was below the target by {abs(latest_revenue_variance_pct):.1%}.")

else:
    print("Revenue met the target.")

print("\nVariable Cost Analysis:")

print(df[["year", "revenue", "variable_cost"]].assign(variable_cost_pct=df["variable_cost_pct"].map("{:.1%}".format)
    ).to_string(index=False))

print("\nVariable Cost Growth Analysis")
print(df[["year", "variable_cost", "variable_cost_growth"]].to_string(index=False))
print("\nVariable Cost Growth Analysis:")

print(
    df[["year", "variable_cost"]].assign(
        variable_cost_growth=df["variable_cost_growth"].map(
         lambda x: f"{x:.2%}" if pd.notna(x) else "N/A"
        )).to_string(index=False))

latest_year = df.iloc[-1]

variable_cost_growth = latest_year["variable_cost_growth"]

if variable_cost_growth < 0:
    cost_insight = "Variable costs decreased compared with the previous year."
elif variable_cost_growth > 0:
    cost_insight = "Variable costs increased compared with the previous year."
else:
    cost_insight = "Variable costs remained unchanged."

print("\nFinancial Insight:")
print(cost_insight)
revenue_growth = latest_year["revenue_growth"]

if revenue_growth > 0:
    revenue_insight = "Revenue increased compared with the previous year."
elif revenue_growth < 0:
    revenue_insight = "Revenue decreased compared with the previous year."
else:
    revenue_insight = "Revenue remained unchanged."

print(revenue_insight)
profit_margin = latest_year["profit_margin"]

if profit_margin > 0.50:
    margin_insight = "Profit margin is above 50%."
elif profit_margin < 0.50:
    margin_insight = "Profit margin is below 50%."
else:
    margin_insight = "Profit margin is exactly 50%."

print(margin_insight)
print(df)

import sqlite3
import pandas as pd

database_path = str(Path(__file__).resolve().parent / "financial_analysis_correct.db")

connection = sqlite3.connect(database_path)

df_sql = pd.read_sql_query(
    """
    SELECT
        year,
        revenue,
        cost,
        target,
        revenue - cost AS profit,
        revenue - target AS revenue_variance
    FROM financial_data
    ORDER BY year
    """,
    connection
)


print("\nData imported from SQLite:")
print(df_sql.to_string(index=False))

print("\nColumns in df_sql:")
print(df_sql.columns.tolist())

best_year = df_sql.loc[df_sql["profit"].idxmax()]

print("\nData in df_sql:")
print(df_sql.to_string(index=False))

print("\nBest Financial Year:")

print(f"Year: {int(best_year['Year'])}")
print(f"Profit: ${best_year['profit']:,.2f}")
print(f"Revenue: ${best_year['Revenue']:,.2f}")
print(f"Revenue Variance: ${best_year['revenue_variance']:,.2f}")

print("\nFinancial Insight:")

if best_year["revenue_variance"] > 0:
    print("Revenue exceeded the target.")
elif best_year["revenue_variance"] < 0:
    print("Revenue was below the target.")
else:
    print("Revenue met the target exactly.")

# Compare profit margins between 2025 and 2026
previous_year = df_sql.loc[df_sql["Year"] == 2025].iloc[0]
current_year = df_sql.loc[df_sql["Year"] == 2026].iloc[0]

previous_margin = (
    (previous_year["Revenue"] - previous_year["Cost"])
    / previous_year["Revenue"] * 100
)

current_margin = (
    (current_year["Revenue"] - current_year["Cost"])
    / current_year["Revenue"] * 100
)

margin_change = current_margin - previous_margin

print("\nProfit Margin Analysis:")
print(f"2025 Profit Margin: {previous_margin:.2f}%")
print(f"2026 Profit Margin: {current_margin:.2f}%")
print(f"Margin Change: {margin_change:+.2f} percentage points")

if margin_change > 0:
    print("Insight: Profit margin improved.")
elif margin_change < 0:
    print("Insight: Profit margin declined.")
else:
    print("Insight: Profit margin remained stable.")


# Cost Performance Analysis: 2025 vs. 2026
previous_cost = previous_year["Cost"]
current_cost = current_year["Cost"]

cost_change = current_cost - previous_cost
cost_change_pct = (cost_change / previous_cost) * 100

revenue_change_pct = (
    (current_year["Revenue"] - previous_year["Revenue"])
    / previous_year["Revenue"]
) * 100

print("\nCost Performance Analysis:")
print(f"2025 Cost: ${previous_cost:,.2f}")
print(f"2026 Cost: ${current_cost:,.2f}")
print(f"Cost Change: ${cost_change:,.2f}")
print(f"Cost Change: {cost_change_pct:+.2f}%")
print(f"Revenue Growth: {revenue_change_pct:+.2f}%")

if cost_change_pct < 0 and revenue_change_pct > 0:
    print("Insight: Costs decreased while revenue increased.")
elif cost_change_pct > 0 and revenue_change_pct > 0:
    print("Insight: Both costs and revenue increased.")
elif cost_change_pct < 0 and revenue_change_pct < 0:
    print("Insight: Both costs and revenue decreased.")
else:
    print("Insight: Review cost and revenue trends.")

# Executive Summary
print("\n" + "=" * 45)
print("EXECUTIVE SUMMARY - 2026")
print("=" * 45)

revenue = best_year["Revenue"]
profit = best_year["profit"]
target = best_year["Target"]
profit_margin = (profit / revenue) * 100
revenue_variance = revenue - target

print(
    f"Revenue reached ${revenue:,.0f}, "
    f"${revenue_variance:,.0f} above target."
)

print(
    f"Profit reached ${profit:,.0f}, "
    f"with a profit margin of {profit_margin:.2f}%."
)

print(
    f"Compared with 2025, costs changed by "
    f"{cost_change_pct:+.2f}%, while revenue grew by "
    f"{revenue_change_pct:+.2f}%."
)

print("=" * 45)

# Overall Financial Performance Assessment
print("\nOVERALL FINANCIAL PERFORMANCE ASSESSMENT")

if (
    revenue > target
    and margin_change > 0
    and cost_change_pct < 0
):
    print(
        "Positive performance: revenue exceeded target, "
        "profit margin improved, and costs decreased."
    )

elif revenue < target:
    print(
        "Attention required: revenue was below target. "
        "Review sales performance and corrective actions."
    )

elif margin_change < 0:
    print(
        "Attention required: profit margin declined. "
        "Review pricing, costs, and profitability."
    )

else:
    print(
        "Mixed performance: review financial KPIs "
        "to identify improvement opportunities."
    )

# Financial KPI Summary - All Years
df_sql["Profit_Margin"] = (
    df_sql["profit"] / df_sql["Revenue"] * 100
)

df_sql["Revenue_Variance_%"] = (
    df_sql["revenue_variance"] / df_sql["Target"] * 100
)

print("\n" + "=" * 70)
print("FINANCIAL KPI SUMMARY - 2023 TO 2026")
print("=" * 70)

kpi_columns = [
    "Year",
    "Revenue",
    "Target",
    "profit",
    "Profit_Margin",
    "revenue_variance",
    "Revenue_Variance_%"
]

print(df_sql[kpi_columns].round(2).to_string(index=False))
print("=" * 70)

import matplotlib.pyplot as plt

# Revenue vs. Target Chart
plt.figure(figsize=(10, 6))

plt.plot(
    df_sql["Year"],
    df_sql["Revenue"],
    marker="o",
    label="Actual Revenue"
)

plt.plot(
    df_sql["Year"],
    df_sql["Target"],
    marker="o",
    linestyle="--",
    label="Revenue Target"
)

# Display values on each point
for year, revenue_value in zip(
    df_sql["Year"], df_sql["Revenue"]
):
    plt.annotate(
        f"${revenue_value:,.0f}",
        (year, revenue_value),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=8
    )

for year, target_value in zip(
    df_sql["Year"], df_sql["Target"]
):
    plt.annotate(
        f"${target_value:,.0f}",
        (year, target_value),
        textcoords="offset points",
        xytext=(0, -15),
        ha="center",
        fontsize=8
    )

plt.title("Actual Revenue vs. Target (2023–2026)")
plt.xlabel("Year")
plt.ylabel("Amount (USD)")

plt.gca().yaxis.set_major_formatter(
    ticker.StrMethodFormatter('${x:,.0f}')
)
plt.xticks(df_sql["Year"])
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("revenue_vs_target.png", dpi=300)
plt.show()


# Profit Margin Trend Chart
plt.figure(figsize=(10, 6))

plt.plot(
    df_sql["Year"],
    df_sql["Profit_Margin"],
    marker="o",
    label="Profit Margin"
)

# Display margin percentages on each point
for year, margin in zip(
    df_sql["Year"], df_sql["Profit_Margin"]
):
    plt.annotate(
        f"{margin:.2f}%",
        (year, margin),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=9
    )

plt.title("Profit Margin Trend (2023–2026)")
plt.xlabel("Year")
plt.ylabel("Profit Margin (%)")
plt.xticks(df_sql["Year"])
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("profit_margin_trend.png", dpi=300)
plt.show()

# Revenue, Cost & Profit Analysis
plt.figure(figsize=(10, 6))

plt.plot(
    df_sql["Year"],
    df_sql["Revenue"],
    marker="o",
    label="Revenue"
)

plt.plot(
    df_sql["Year"],
    df_sql["Cost"],
    marker="o",
    label="Cost"
)

plt.plot(
    df_sql["Year"],
    df_sql["profit"],
    marker="o",
    label="Profit"
)

# Display values on each point
for year, revenue_value, cost_value, profit_value in zip(
    df_sql["Year"],
    df_sql["Revenue"],
    df_sql["Cost"],
    df_sql["profit"]
):
    plt.annotate(
        f"${revenue_value:,.0f}",
        (year, revenue_value),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=8
    )

    plt.annotate(
        f"${cost_value:,.0f}",
        (year, cost_value),
        textcoords="offset points",
        xytext=(0, -12),
        ha="center",
        fontsize=8
    )

    plt.annotate(
        f"${profit_value:,.0f}",
        (year, profit_value),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center",
        fontsize=8
    )

plt.title("Revenue, Cost & Profit Analysis (2023–2026)")
plt.xlabel("Year")
plt.ylabel("Amount (USD)")

plt.gca().yaxis.set_major_formatter(
    ticker.StrMethodFormatter('${x:,.0f}')
)
plt.xticks(df_sql["Year"])
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("revenue_cost_profit.png", dpi=300)
plt.show()

connection.close()


