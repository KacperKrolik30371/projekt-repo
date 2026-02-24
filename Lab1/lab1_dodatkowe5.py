import pandas as pd

df = pd.read_csv("sales_raw.csv")

df["total_price"] = df["quantity"] * df["unit_price"]

print("=== Produkty kupowane razem przez klienta ===")

products_together = (
    df.groupby("customer_name")["product_name"]
      .apply(list)
)

print(products_together)


print("\n=== Średnia liczba produktów w zamówieniu ===")

products_per_order = (
    df.groupby("order_id")["product_name"]
      .count()
)

print(products_per_order.mean())


print("\n=== Korelacja cena vs ilość ===")

correlation = df["unit_price"].corr(df["quantity"])
print(correlation)


product_hierarchy = df["product_name"].value_counts()

print(product_hierarchy)