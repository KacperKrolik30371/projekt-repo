import pandas as pd

df = pd.read_csv("sales_raw.csv")

df["total_price"] = df["quantity"] * df["unit_price"]
df["order_date"] = pd.to_datetime(df["order_date"])

dim_customer = df[["customer_name", "country"]].drop_duplicates().reset_index(drop=True)
dim_customer["customer_id"] = dim_customer.index + 1

dim_product = df[["product_name", "category", "unit_price"]].drop_duplicates().reset_index(drop=True)
dim_product["product_id"] = dim_product.index + 1

fact_sales = df.merge(dim_customer, on=["customer_name", "country"])
fact_sales = fact_sales.merge(dim_product, on=["product_name", "category", "unit_price"])

fact_sales = fact_sales[[
    "customer_id",
    "product_id",
    "order_date",
    "quantity",
    "total_price",
    "country",
    "category"
]]

print("=== DIM CUSTOMER ===")
print(dim_customer)

print("\n=== DIM PRODUCT ===")
print(dim_product)

print("\n=== FACT SALES ===")
print(fact_sales.head())


print("\n=== OLAP: sprzedaż wg kraju i kategorii ===")

olap_country_category = (
    fact_sales.groupby(["country", "category"])["total_price"]
              .sum()
)

print(olap_country_category)


fact_sales["quarter"] = fact_sales["order_date"].dt.to_period("Q")

quarterly_sales = (
    fact_sales.groupby("quarter")["total_price"]
              .sum()
)

print(quarterly_sales)