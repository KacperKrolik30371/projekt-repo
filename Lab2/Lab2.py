import pandas as pd

# wczytanie pliku CSV
df = pd.read_csv("Online_Retail.csv", sep=",", encoding="ISO-8859-1")

# liczba rekordów
print("Liczba rekordów:", df.shape[0])

# liczba kolumn
print("Liczba kolumn:", df.shape[1])

# 5 przykładowych wierszy
print("\n5 przykładowych wierszy:")
print(df.head())