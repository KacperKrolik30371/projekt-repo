import pandas as pd

df = pd.read_csv("Online_Retail.csv", encoding='ISO-8859-1')

# usunięcie brakujących CustomerID
df = df.dropna(subset=["CustomerID"])

# usunięcie anulowanych transakcji (InvoiceNo zaczyna się na "C")
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# usunięcie błędnych wartości
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]

# konwersja daty
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# usunięcie duplikatów
df = df.drop_duplicates()

# dodanie kolumny Revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

df.head()

dim_customer = df[["CustomerID", "Country"]].drop_duplicates()
dim_customer = dim_customer.reset_index(drop=True)
dim_customer["CustomerKey"] = dim_customer.index + 1

dim_customer.head()

dim_product = df[["StockCode", "Description"]].drop_duplicates()
dim_product = dim_product.reset_index(drop=True)
dim_product["ProductKey"] = dim_product.index + 1

dim_product.head()

dim_date = pd.DataFrame()
dim_date["InvoiceDate"] = df["InvoiceDate"].drop_duplicates()
dim_date = dim_date.sort_values("InvoiceDate").reset_index(drop=True)

dim_date["DateKey"] = dim_date.index + 1
dim_date["Year"] = dim_date["InvoiceDate"].dt.year
dim_date["Month"] = dim_date["InvoiceDate"].dt.month
dim_date["Day"] = dim_date["InvoiceDate"].dt.day

dim_date.head()

fact = df.merge(dim_customer, on=["CustomerID", "Country"])
fact = fact.merge(dim_product, on=["StockCode", "Description"])
fact = fact.merge(dim_date, on="InvoiceDate")

fact_sales = fact[[
    "CustomerKey",
    "ProductKey",
    "DateKey",
    "Quantity",
    "Revenue"
]]

fact_sales.head()

# przykładowa aktualizacja
dim_customer.loc[0, "Country"] = "NewCountry"

dim_customer.head()