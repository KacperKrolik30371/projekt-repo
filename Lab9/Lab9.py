import pandas as pd

print("=" * 70)
print("RAPORT SPRZEDAŻY - ONLINE RETAIL")
print("=" * 70)

# =====================================================
# 1. Wczytanie danych
# =====================================================

df = pd.read_csv("Online_Retail.csv", encoding="latin1")

print(f"\nLiczba rekordów przed czyszczeniem: {len(df)}")

# =====================================================
# 2. Czyszczenie danych
# =====================================================

df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)].copy()

df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Poprawione wczytanie dat
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    format="%m/%d/%Y %H:%M",
    errors="coerce"
)

print(f"Liczba rekordów po czyszczeniu: {len(df)}")

# =====================================================
# Wykrycie nazwy kolumny klienta
# =====================================================

if "CustomerID" in df.columns:
    customer_col = "CustomerID"
elif "Customer ID" in df.columns:
    customer_col = "Customer ID"
else:
    customer_col = None

# =====================================================
# RAPORT 1 - KRAJE
# =====================================================

country_report = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\n")
print("=" * 70)
print("RAPORT 1 - SPRZEDAŻ WEDŁUG KRAJÓW")
print("=" * 70)

print(country_report.head(10))

# =====================================================
# RAPORT 2 - KLIENCI
# =====================================================

print("\n")
print("=" * 70)
print("RAPORT 2 - TOP KLIENCI")
print("=" * 70)

if customer_col:

    customer_report = (
        df.dropna(subset=[customer_col])
        .groupby(customer_col)["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    print(customer_report.head(10))

else:

    customer_report = None
    print("Brak kolumny klienta w zbiorze danych.")

# =====================================================
# RAPORT 3 - PRODUKTY
# =====================================================

product_report = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

print("\n")
print("=" * 70)
print("RAPORT 3 - NAJPOPULARNIEJSZE PRODUKTY")
print("=" * 70)

print(product_report.head(10))

# =====================================================
# RAPORT 4 - SPRZEDAŻ MIESIĘCZNA
# =====================================================

monthly_report = (
    df.groupby(df["InvoiceDate"].dt.to_period("M"))["Revenue"]
    .sum()
)

print("\n")
print("=" * 70)
print("RAPORT 4 - SPRZEDAŻ MIESIĘCZNA")
print("=" * 70)

print(monthly_report)

# =====================================================
# DANE DO WNIOSKÓW
# =====================================================

best_country = country_report.index[0]
best_country_value = country_report.iloc[0]

best_product = product_report.index[0]
best_product_quantity = product_report.iloc[0]

if customer_report is not None:
    best_customer = customer_report.index[0]
    best_customer_value = customer_report.iloc[0]

# =====================================================
# ODPOWIEDZI NA PYTANIA BIZNESOWE
# =====================================================

print("\n")
print("=" * 70)
print("ODPOWIEDZI NA PYTANIA BIZNESOWE")
print("=" * 70)

print("\n1. Które kraje generują największą sprzedaż?")
print(
    f"Największą sprzedaż wygenerował kraj {best_country} "
    f"o wartości {best_country_value:,.2f}."
)

print("\n2. Który klient kupuje najwięcej?")

if customer_report is not None:
    print(
        f"Największą wartość zakupów wygenerował klient "
        f"{int(best_customer)} "
        f"na kwotę {best_customer_value:,.2f}."
    )
else:
    print("Brak danych o klientach.")

print("\n3. Jaki produkt sprzedaje się najlepiej?")
print(
    f"Najpopularniejszym produktem jest "
    f"'{best_product}', "
    f"sprzedano {best_product_quantity:,} sztuk."
)

print("\n4. Jak zmieniała się sprzedaż?")
print(
    "Analiza miesięczna pokazuje zmiany sprzedaży "
    "w kolejnych miesiącach oraz występowanie okresów "
    "o zwiększonym popycie."
)

# =====================================================
# INSIGHTY DLA BIZNESU
# =====================================================

print("\n")
print("=" * 70)
print("INSIGHTY DLA BIZNESU")
print("=" * 70)

print(f"""
1. Największy udział w przychodach generuje kraj:
   {best_country}.

2. Najpopularniejszym produktem jest:
   {best_product}.

3. Firma powinna utrzymywać odpowiedni poziom
   zapasów dla najczęściej kupowanych produktów.

4. Analiza sprzedaży miesięcznej pozwala
   identyfikować okresy wzmożonego popytu
   i lepiej planować zakupy magazynowe.
""")

if customer_report is not None:
    print(f"""
5. Najbardziej wartościowym klientem jest:
   {int(best_customer)}.

   Warto rozważyć program lojalnościowy
   lub indywidualne oferty dla kluczowych klientów.
""")

print("""
6. Pandas umożliwia szybkie przygotowanie raportów,
   agregację danych oraz tworzenie analiz biznesowych
   bez konieczności używania SQL.
""")

# =====================================================
# PODSUMOWANIE
# =====================================================

print("\n")
print("=" * 70)
print("PODSUMOWANIE")
print("=" * 70)

print(f"""
Największą sprzedaż wygenerował kraj: {best_country}.
Najpopularniejszy produkt: {best_product}.

Analiza danych pozwala wskazać kluczowe rynki,
najważniejszych klientów oraz produkty generujące
największe zainteresowanie. Informacje te mogą
wspierać decyzje biznesowe dotyczące marketingu,
sprzedaży oraz zarządzania zapasami.
""")