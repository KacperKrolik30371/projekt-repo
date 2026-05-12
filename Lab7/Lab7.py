import pandas as pd
import time

# =========================
# ETAP 1 — WCZYTANIE DANYCH
# =========================

start_load = time.time()

df = pd.read_csv(
    "Online_Retail.csv",
    encoding="ISO-8859-1"
)

end_load = time.time()

print("=== ETAP 1 ===")

print("Czas wczytywania danych:", end_load - start_load)

print("\nLiczba rekordów:", df.shape[0])
print("Liczba kolumn:", df.shape[1])

print("\nBrakujące wartości:")
print(df.isnull().sum())

print("\nTypy danych:")
print(df.dtypes)

# pamięć przed optymalizacją
memory_before = df.memory_usage(deep=True).sum() / 1024**2

print("\nZużycie pamięci przed optymalizacją:", memory_before, "MB")


# =========================
# ETAP 2 — OPTYMALIZACJA
# =========================

print("\n=== ETAP 2 ===")

# kopia dataframe
df_opt = df.copy()

# tekst -> category
df_opt["Country"] = df_opt["Country"].astype("category")
df_opt["Description"] = df_opt["Description"].astype("category")
df_opt["InvoiceNo"] = df_opt["InvoiceNo"].astype("category")

# liczby -> mniejsze typy
df_opt["Quantity"] = pd.to_numeric(
    df_opt["Quantity"],
    downcast="integer"
)

df_opt["UnitPrice"] = pd.to_numeric(
    df_opt["UnitPrice"],
    downcast="float"
)

# poprawna konwersja daty
df_opt["InvoiceDate"] = pd.to_datetime(
    df_opt["InvoiceDate"],
    format="mixed",
    errors="coerce"
)

# pamięć po optymalizacji
memory_after = df_opt.memory_usage(deep=True).sum() / 1024**2

print("Zużycie pamięci po optymalizacji:", memory_after, "MB")

print("Zaoszczędzona pamięć:",
      memory_before - memory_after,
      "MB")


# =========================
# DODANIE NOWYCH KOLUMN
# =========================

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    format="mixed",
    errors="coerce"
)

df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
df_opt["TotalPrice"] = df_opt["Quantity"] * df_opt["UnitPrice"]

df["Month"] = df["InvoiceDate"].dt.month
df_opt["Month"] = df_opt["InvoiceDate"].dt.month


# =========================
# ETAP 3 — ANALIZA
# =========================

print("\n=== ETAP 3 ===")


# -------------------------
# grupowanie po kraju
# -------------------------

start = time.time()

country_sales = df.groupby("Country")["TotalPrice"].sum()

end = time.time()

print("\nGrupowanie po kraju BEFORE:", end - start)

start = time.time()

country_sales_opt = df_opt.groupby(
    "Country",
    observed=False
)["TotalPrice"].sum()

end = time.time()

print("Grupowanie po kraju AFTER:", end - start)


# -------------------------
# grupowanie po miesiącu
# -------------------------

start = time.time()

month_sales = df.groupby("Month")["TotalPrice"].sum()

end = time.time()

print("\nGrupowanie po miesiącu BEFORE:", end - start)

start = time.time()

month_sales_opt = df_opt.groupby(
    "Month",
    observed=False
)["TotalPrice"].sum()

end = time.time()

print("Grupowanie po miesiącu AFTER:", end - start)


# -------------------------
# TOP 10 klientów
# -------------------------

start = time.time()

top_customers = (
    df.groupby("CustomerID")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

end = time.time()

print("\nTOP 10 klientów BEFORE:", end - start)

start = time.time()

top_customers_opt = (
    df_opt.groupby("CustomerID")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

end = time.time()

print("TOP 10 klientów AFTER:", end - start)


# -------------------------
# filtrowanie UK
# -------------------------

start = time.time()

uk_products = df[df["Country"] == "United Kingdom"]

end = time.time()

print("\nFiltrowanie UK BEFORE:", end - start)

start = time.time()

uk_products_opt = df_opt[df_opt["Country"] == "United Kingdom"]

end = time.time()

print("Filtrowanie UK AFTER:", end - start)


# -------------------------
# rekordy > 1000
# -------------------------

start = time.time()

high_sales = df[df["TotalPrice"] > 1000]

end = time.time()

print("\nFiltrowanie >1000 BEFORE:", end - start)

start = time.time()

high_sales_opt = df_opt[df_opt["TotalPrice"] > 1000]

end = time.time()

print("Filtrowanie >1000 AFTER:", end - start)


# =========================
# PRZYKŁADOWE WYNIKI
# =========================

print("\n=== PRZYKŁADOWE WYNIKI ===")

print("\nSuma sprzedaży według kraju:")
print(country_sales_opt.head())

print("\nSuma sprzedaży według miesiąca:")
print(month_sales_opt)

print("\nTOP 10 klientów:")
print(top_customers_opt)

print("\nProdukty sprzedane w UK:")
print(uk_products_opt.head())

print("\nRekordy o wartości sprzedaży > 1000:")
print(high_sales_opt.head())


# =========================
# ETAP 4 — WNIOSKI
# =========================

# Wnioski:
# 1. Optymalizacja zmniejszyła zużycie pamięci danych.
#
# 2. Zamiana object na category przyspieszyła
#    operacje grupowania i filtrowania.
#
# 3. Downcasting typów liczbowych zmniejszył
#    ilość zajmowanej pamięci.
#
# 4. Nie każda operacja przyspieszyła bardzo mocno,
#    ale większość wykonywała się szybciej.
#
# 5. Mniejsze zużycie pamięci może poprawić wydajność,
#    szczególnie przy dużych zbiorach danych.