import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sales_raw.csv")

df["total_price"] = df["quantity"] * df["unit_price"]

df["order_date"] = pd.to_datetime(df["order_date"])
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month

monthly_summary = (
    df.groupby(["country", "year", "month"])
      .agg({
          "total_price": "sum",
          "quantity": "sum"
      })
)

print(monthly_summary)

df["quarter"] = df["order_date"].dt.to_period("Q")

avg_price_by_product_quarter = (
    df.groupby(["product_name", "quarter"])["unit_price"]
      .mean()
)

print(avg_price_by_product_quarter)

laptops = df[df["product_name"].str.lower().str.contains("laptop")]

trend = (
    laptops.groupby(["country", "year", "month"])["total_price"]
           .sum()
           .reset_index()
)

for country in ["Poland", "Germany"]:
    data = trend[trend["country"] == country]
    plt.plot(
        data["year"].astype(str) + "-" + data["month"].astype(str),
        data["total_price"],
        label=country
    )

plt.xticks(rotation=45)
plt.legend()
plt.title("Laptop sales trend")
plt.tight_layout()
plt.show()

seasonality = df.groupby("month")["total_price"].mean()

print(seasonality)