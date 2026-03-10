import pandas as pd

# wczytanie danych
df = pd.read_csv("Online_Retail.csv", encoding="ISO-8859-1")

# -------------------
# CUSTOMER
# -------------------
customers = df[['CustomerID', 'Country']].drop_duplicates()

# -------------------
# PRODUCT
# -------------------
products = df[['StockCode', 'Description', 'UnitPrice']].drop_duplicates()

# -------------------
# INVOICE
# -------------------
invoices = df[['InvoiceNo', 'InvoiceDate', 'CustomerID']].drop_duplicates()

# -------------------
# INVOICE ITEMS (łączenie faktury z produktem)
# -------------------
invoice_items = df[['InvoiceNo', 'StockCode', 'Quantity']]

# -------------------
# podgląd danych
# -------------------
print("CUSTOMERS")
print(customers.head())

print("\nPRODUCTS")
print(products.head())

print("\nINVOICES")
print(invoices.head())

print("\nINVOICE ITEMS")
print(invoice_items.head())