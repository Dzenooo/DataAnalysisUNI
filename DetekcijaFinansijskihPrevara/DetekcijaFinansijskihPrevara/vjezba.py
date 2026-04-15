import pandas as pd

df = pd.read_csv("data/account_profiles.csv")

print(df.shape)
print(df.columns)
print(df.head())
print(df.info())

edges = pd.read_csv("data/network_edges.csv")

print(edges.shape)
print(edges.head())
print(edges.isnull().sum())

edges_clean = edges.dropna()
print(edges_clean.shape)

edges_rings = edges.dropna(subset=["ring_id"])
print(edges_rings.shape)


#Koliko različitih prstena prevara ima

print(edges_rings["ring_id"].nunique())

#koji prsten ima najvise veza
print(edges_rings["ring_id"].value_counts().head(5))

#distribucija tipova veza u prstenima
print(edges_rings["shared_type"].value_counts())


#Umjesto brisanja, možemo popuniti nedostajuće vrijednosti

edges_filled = edges.fillna({"ring_id": "NEPOZNAT"})

print(edges_filled["ring_id"].value_counts().head(5))

fp = pd.read_csv("data/fraud_patterns.csv")
print(fp[["fraud_pattern", "transaction_count"]])

fp["fraud_pattern"] = fp["fraud_pattern"].replace({
    "card_not_present": "CNP prevara",
    "account_takeover": "Preuzimanje računa",
    "card_present_stolen": "Ukradena kartica",
    "friendly_fraud": "Lažna reklamacija",
    "atm_fraud": "ATM prevara",
    "money_laundering": "Pranje novca",
    "identity_theft": "Krađa identiteta"
})
print(fp[["fraud_pattern", "transaction_count"]])

#map() koristi rječin kao "tabelu prijevoda"

tip_prevod = {
    "personal": "Lični",
    "business": "Poslovni",
    "premium": "Premium"
}

df["tip_racuna"] = df["account_type"].map(tip_prevod)
print(df[["account_id", "account_type", "tip_racuna"]].head())


#Zadatak1 profil prevaranta
count_accounts = df.loc[df["fraud_count"] > 0, "account_id"].nunique()
print(count_accounts)

avg_risk_score_fraudster = df.loc[df["is_fraudster"] == 1, "risk_score"].mean()
print(avg_risk_score_fraudster)

avg_risk = df.loc[df["is_fraudster"] == 1, "risk_score"].mean()
print(avg_risk)


#izracunaj koji prevaranti nemaju 2fa



#zadatak2

network_e = pd.read_csv("data/network_edges.csv")
print(network_e.shape)
print(network_e.head())
print(network_e.isnull().sum())

network_e_rings = edges.dropna(subset=["ring_id"])
print(network_e_rings.shape)

print(network_e_rings["shared_type"].value_counts())

print(network_e_rings["ring_id"].value_counts().head(5))

#zadatak3

df["rizik_kategorija"] = pd.cut(
    df["risk_score"],
    bins=[-float("inf"), 25, 50, float("inf")],
    labels=["Nizak", "Srednji", "Visok"]
)
counts = df.groupby("rizik_kategorija")["account_id"].nunique()
print(counts)

#zadatak4

print(network_e.duplicated().sum())
print(network_e.duplicated(subset=["shared_type"]).sum())

unique_a = network_e.drop_duplicates(subset=["account_a"])
print(len(unique_a))

#zadatak5

fraud_counts = (
    df.loc[df["is_fraudster"] == 1]
      .groupby("account_type")["account_id"]
      .nunique()
      .sort_values(ascending=False)
)
print(fraud_counts)

print(fp.sort_values("avg_amount", ascending=False) [["fraud_pattern", "avg_amount"]])


