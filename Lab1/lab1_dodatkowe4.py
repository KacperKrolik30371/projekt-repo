import pandas as pd

df = pd.read_csv("sales_raw.csv")

df["total_price"] = df["quantity"] * df["unit_price"]

df["order_date"] = pd.to_datetime(df["order_date"])
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month

print("=== TOP 3 klienci w każdym kraju ===")

top_clients = (
    df.groupby(["country", "customer_name"])["total_price"]
      .sum()
      .reset_index()
)

top_clients["rank"] = (
    top_clients.groupby("country")["total_price"]
               .rank(method="first", ascending=False)
)

print(top_clients[top_clients["rank"] <= 3])


print("\n=== Ranking produktów w każdej kategorii ===")

product_ranking = (
    df.groupby(["category", "product_name"])["total_price"]
      .sum()
      .reset_index()
)

product_ranking["rank"] = (
    product_ranking.groupby("category")["total_price"]
                   .rank(method="first", ascending=False)
)

print(product_ranking.sort_values(["category", "rank"]))


print("\n=== Udział procentowy kategorii w sprzedaży ===")

category_sales = df.groupby("category")["total_price"].sum()

category_share = (category_sales / category_sales.sum()) * 100

print(category_share)


print("\n=== BONUS: Klient z największym wzrostem zakupów ===")

customer_growth = (
    df.groupby(["customer_name", "year", "month"])["total_price"]
      .sum()
      .reset_index()
)

customer_growth["previous_month"] = (
    customer_growth.groupby("customer_name")["total_price"]
                   .shift(1)
)

customer_growth["growth"] = (
    customer_growth["total_price"] - customer_growth["previous_month"]
)

print(customer_growth.sort_values("growth", ascending=False).head(1))