dim_country = df[["Country"]].drop_duplicates().reset_index(drop=True)
dim_country["CountryKey"] = dim_country.index + 1

dim_country.head()

fact = fact.merge(dim_country, on="Country")

fact_sales = fact[[
    "CustomerKey",
    "ProductKey",
    "DateKey",
    "CountryKey",
    "Quantity",
    "Revenue"
]]

fact_sales["AvgPrice"] = fact_sales["Revenue"] / fact_sales["Quantity"]

dim_customer_scd = dim_customer.copy()

dim_customer_scd["StartDate"] = pd.Timestamp("2020-01-01")
dim_customer_scd["EndDate"] = pd.NaT
dim_customer_scd["IsCurrent"] = 1

dim_customer_scd.head()

# wybierz przykładowego klienta
customer_id = dim_customer_scd.loc[0, "CustomerID"]

# stary rekord
old_record = dim_customer_scd[dim_customer_scd["CustomerID"] == customer_id].iloc[0]

# zamykamy stary rekord
dim_customer_scd.loc[
    dim_customer_scd["CustomerID"] == customer_id, "EndDate"
] = pd.Timestamp("2021-01-01")

dim_customer_scd.loc[
    dim_customer_scd["CustomerID"] == customer_id, "IsCurrent"
] = 0

# dodajemy nowy rekord (zmiana kraju)
new_record = old_record.copy()
new_record["Country"] = "NewCountry"
new_record["StartDate"] = pd.Timestamp("2021-01-01")
new_record["EndDate"] = pd.NaT
new_record["IsCurrent"] = 1

dim_customer_scd = pd.concat([dim_customer_scd, pd.DataFrame([new_record])], ignore_index=True)

dim_customer_scd.head()