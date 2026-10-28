import pandas as pd
data = pd.DataFrame({
    "destination": [
        "London", "Accra", "Accra", "Paris", "London",
        "Paris", "Dubai", "Dubai", "Dubai", "London"
    ],
    "tickets": [5, 4, 3, 3, 3, 2, 2, 2, 1, 1],
    "sales": [
        4250000, 1400000, 1050000, 2700000, 2550000,
        1800000, 1300000, 1300000, 650000, 850000
    ],
    "profit": [
        750000, 280000, 210000, 540000, 450000,
        360000, 300000, 300000, 150000, 150000
    ]
})
required_columns = [
    "destination", "tickets", "sales", "profit"
]
missing_columns = [
    col for col in required_columns 
    if col not in data.columns
]
if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )
if data[required_columns].isna().any().any():
    raise ValueError(
        "Missing values found. Review the source data."
    )
for col in ["tickets", "sales", "profit"]:
    data[col] = pd.to_numeric(data[col], errors="raise")
report = data.groupby("destination").agg(
    tickets=("tickets", "sum"),
    sales=("sales", "sum"),
    profit=("profit", "sum")
)
report["profit_margin_pct"] = (
    report["profit"] / report["sales"] * 100
)
company_sales = report["sales"].sum()
company_profit = report["profit"].sum()
company_tickets = report["tickets"].sum()
report["profit_contribution_pct"] = (
    report["profit"] / company_profit * 100
)
report["profit_rank"] = (
    report["profit"]
    .rank(method="min", ascending=False)
    .astype(int)
)
report = report.sort_values(
    "profit", ascending=False
)
assert company_tickets == 26, "Ticket total is incorrect"
assert company_sales == 17850000, "Sales total is incorrect"
assert company_profit == 3490000, "Profit total is incorrect"
print("\nDAY 44: PORTFOLIO REPORT")
print("=" * 55)
print(report.round(2).to_string())
print("\nCOMPANY KPIs")
print("Total tickets:", company_tickets)
print("Total sales:", company_sales)
print("Total profit:", company_profit)
print(
    "Overall profit margin:",
    round(company_profit / company_sales * 100, 2), 
    "%"
)
print("\nBUSINESS INSIGHTS")
print("Highest total profit:", report["profit"].idxmax())
print(
    "Highest profit margin:", 
    report["profit_margin_pct"].idxmax()
)
print("Lowest total profit:", report["profit"].idxmin())
report.to_csv("day44_destination_report.csv")
print("\nAll company total checks passed.")
print("\nDay 44 report saved sucessfully.")