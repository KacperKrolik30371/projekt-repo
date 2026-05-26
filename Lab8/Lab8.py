# ============================================================
# LABORATORIUM 8
# Analiza wpływu różnych metod agregacji danych na wydajność
# ============================================================

# ============================================================
# Import wymaganych bibliotek
# ============================================================

import pandas as pd
import time

# ============================================================
# ETAP 1 — PRZYGOTOWANIE DANYCH
# ============================================================

print("=" * 60)
print("ETAP 1 — PRZYGOTOWANIE DANYCH")
print("=" * 60)

# ------------------------------------------------------------
# 1. Wczytanie danych
# ------------------------------------------------------------

df = pd.read_csv("Online_Retail_II.csv")

print("\nLiczba rekordów przed czyszczeniem:")
print(df.shape)

# ------------------------------------------------------------
# 2. Usunięcie rekordów:
#    - z brakującym Customer ID
#    - z Quantity <= 0
# ------------------------------------------------------------

df = df.dropna(subset=['Customer ID'])
df = df[df['Quantity'] > 0]

print("\nLiczba rekordów po czyszczeniu:")
print(df.shape)

# ------------------------------------------------------------
# 3. Konwersja daty
# ------------------------------------------------------------

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# ------------------------------------------------------------
# 4. Utworzenie kolumny TotalPrice
# ------------------------------------------------------------

df['TotalPrice'] = df['Quantity'] * df['Price']

print("\nPrzykładowe dane:")
print(df.head())


# ============================================================
# ETAP 2 — AGREGACJA DANYCH
# ============================================================

print("\n")
print("=" * 60)
print("ETAP 2 — AGREGACJA DANYCH")
print("=" * 60)

# ============================================================
# ANALIZA 1 — SPRZEDAŻ WG KRAJU
# ============================================================

print("\nANALIZA 1 — SPRZEDAŻ WG KRAJU")

# ------------------------------------------------------------
# Metoda 1 — groupby()
# ------------------------------------------------------------

start = time.time()

country_groupby = df.groupby('Country')['TotalPrice'].sum()

end = time.time()

print("\nMetoda groupby():")
print(country_groupby.head())
print(f"Czas wykonania: {end - start:.6f} s")

# ------------------------------------------------------------
# Metoda 2 — pivot_table()
# ------------------------------------------------------------

start = time.time()

country_pivot = pd.pivot_table(
    df,
    values='TotalPrice',
    index='Country',
    aggfunc='sum'
)

end = time.time()

print("\nMetoda pivot_table():")
print(country_pivot.head())
print(f"Czas wykonania: {end - start:.6f} s")

# ------------------------------------------------------------
# Metoda 3 — set_index() + groupby()
# ------------------------------------------------------------

start = time.time()

df_country = df.set_index('Country')

country_setindex = df_country.groupby(level=0)['TotalPrice'].sum()

end = time.time()

print("\nMetoda set_index() + groupby():")
print(country_setindex.head())
print(f"Czas wykonania: {end - start:.6f} s")


# ============================================================
# ANALIZA 2 — SPRZEDAŻ WG MIESIĄCA
# ============================================================

print("\n")
print("=" * 60)
print("ANALIZA 2 — SPRZEDAŻ WG MIESIĄCA")
print("=" * 60)

# Utworzenie kolumny miesiąca

df['Month'] = df['InvoiceDate'].dt.to_period('M')

# ------------------------------------------------------------
# Metoda 1 — groupby()
# ------------------------------------------------------------

start = time.time()

month_groupby = df.groupby('Month')['TotalPrice'].sum()

end = time.time()

print("\nMetoda groupby():")
print(month_groupby.head())
print(f"Czas wykonania: {end - start:.6f} s")

# ------------------------------------------------------------
# Metoda 2 — pivot_table()
# ------------------------------------------------------------

start = time.time()

month_pivot = pd.pivot_table(
    df,
    values='TotalPrice',
    index='Month',
    aggfunc='sum'
)

end = time.time()

print("\nMetoda pivot_table():")
print(month_pivot.head())
print(f"Czas wykonania: {end - start:.6f} s")

# ------------------------------------------------------------
# Metoda 3 — set_index() + groupby()
# ------------------------------------------------------------

start = time.time()

df_month = df.set_index('Month')

month_setindex = df_month.groupby(level=0)['TotalPrice'].sum()

end = time.time()

print("\nMetoda set_index() + groupby():")
print(month_setindex.head())
print(f"Czas wykonania: {end - start:.6f} s")


# ============================================================
# ANALIZA 3 — LICZBA TRANSAKCJI WG KLIENTA
# ============================================================

print("\n")
print("=" * 60)
print("ANALIZA 3 — LICZBA TRANSAKCJI WG KLIENTA")
print("=" * 60)

# ------------------------------------------------------------
# Metoda 1 — groupby()
# ------------------------------------------------------------

start = time.time()

customer_groupby = df.groupby('Customer ID')['Invoice'].count()

end = time.time()

print("\nMetoda groupby():")
print(customer_groupby.head())
print(f"Czas wykonania: {end - start:.6f} s")

# ------------------------------------------------------------
# Metoda 2 — pivot_table()
# ------------------------------------------------------------

start = time.time()

customer_pivot = pd.pivot_table(
    df,
    values='Invoice',
    index='Customer ID',
    aggfunc='count'
)

end = time.time()

print("\nMetoda pivot_table():")
print(customer_pivot.head())
print(f"Czas wykonania: {end - start:.6f} s")

# ------------------------------------------------------------
# Metoda 3 — set_index() + groupby()
# ------------------------------------------------------------

start = time.time()

df_customer = df.set_index('Customer ID')

customer_setindex = df_customer.groupby(level=0)['Invoice'].count()

end = time.time()

print("\nMetoda set_index() + groupby():")
print(customer_setindex.head())
print(f"Czas wykonania: {end - start:.6f} s")


# ============================================================
# ETAP 3 — SYMULACJA DUŻEJ HURTOWNI DANYCH
# ============================================================

print("\n")
print("=" * 60)
print("ETAP 3 — SYMULACJA DUŻEJ HURTOWNI DANYCH")
print("=" * 60)

# ------------------------------------------------------------
# Powiększenie zbioru danych
# ------------------------------------------------------------

large_df = pd.concat([df] * 10, ignore_index=True)

print("\nRozmiar powiększonego zbioru:")
print(large_df.shape)

# ============================================================
# PONOWNA ANALIZA — SPRZEDAŻ WG KRAJU
# ============================================================

print("\n")
print("=" * 60)
print("PONOWNA ANALIZA — SPRZEDAŻ WG KRAJU")
print("=" * 60)

# ------------------------------------------------------------
# Metoda 1 — groupby()
# ------------------------------------------------------------

start = time.time()

large_groupby = large_df.groupby('Country')['TotalPrice'].sum()

end = time.time()

groupby_time = end - start

print("\nMetoda groupby():")
print(large_groupby.head())
print(f"Czas wykonania: {groupby_time:.6f} s")

# ------------------------------------------------------------
# Metoda 2 — pivot_table()
# ------------------------------------------------------------

start = time.time()

large_pivot = pd.pivot_table(
    large_df,
    values='TotalPrice',
    index='Country',
    aggfunc='sum'
)

end = time.time()

pivot_time = end - start

print("\nMetoda pivot_table():")
print(large_pivot.head())
print(f"Czas wykonania: {pivot_time:.6f} s")

# ------------------------------------------------------------
# Metoda 3 — set_index() + groupby()
# ------------------------------------------------------------

start = time.time()

large_set = large_df.set_index('Country')

large_setindex = large_set.groupby(level=0)['TotalPrice'].sum()

end = time.time()

setindex_time = end - start

print("\nMetoda set_index() + groupby():")
print(large_setindex.head())
print(f"Czas wykonania: {setindex_time:.6f} s")


# ============================================================
# ETAP 4 — RAPORT KOŃCOWY
# ============================================================

print("\n")
print("=" * 60)
print("ETAP 4 — RAPORT KOŃCOWY")
print("=" * 60)

print("""
1. Metoda groupby() charakteryzuje się bardzo dobrą wydajnością
   oraz prostą składnią. W większości przypadków była najszybsza.

2. Metoda pivot_table() jest bardziej rozbudowana i czytelna
   przy tworzeniu tabel przestawnych, jednak zwykle działa wolniej
   od groupby().

3. Metoda set_index() + groupby() może być korzystna w przypadku
   wielokrotnych operacji na indeksowanych danych, jednak dodatkowa
   operacja ustawiania indeksu wpływa na czas wykonania.

4. W przypadku bardzo dużych hurtowni danych mogą wystąpić:
   - problemy z wydajnością,
   - duże zużycie pamięci RAM,
   - wydłużony czas agregacji,
   - konieczność optymalizacji indeksów i struktur danych.

5. Skalowalność metod:
   - groupby() najlepiej sprawdza się przy dużych zbiorach,
   - pivot_table() oferuje większą funkcjonalność analityczną,
   - set_index() może być użyteczne przy pracy wieloetapowej.
""")

print("\nZakończono analizę.")