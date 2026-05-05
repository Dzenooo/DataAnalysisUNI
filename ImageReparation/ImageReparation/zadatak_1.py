import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Primjer 1 — Seaborn tema i prvi graf

sns.set_theme(style="whitegrid", palette="muted")

df = pd.read_csv("data/imdb_top_1000.csv")

sns.scatterplot(data=df, x="IMDB_Rating", y="Meta_score", alpha=0.5)
plt.title("IMDB Rating vs Metascore")
plt.show()

# Primjer 2 — Moć hue parametra
# ---------------------------------------------------------------

df["PrviZanr"] = df["Genre"].str.split(",").str[0].str.strip()

top5_zanrovi = df["PrviZanr"].value_counts().head(5).index
df_top5 = df[df["PrviZanr"].isin(top5_zanrovi)]

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_top5, x="IMDB_Rating", y="Meta_score",
                hue="PrviZanr", style="PrviZanr", alpha=0.7)
plt.title("Rating vs Metascore — po žanru")
plt.show()


# Primjer 3 — Distribucije: histplot i kdeplot
# ---------------------------------------------------------------

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

sns.histplot(data=df, x="IMDB_Rating", bins=20, ax=axes[0],
             color="steelblue")
axes[0].set_title("Histogram")

sns.kdeplot(data=df, x="IMDB_Rating", ax=axes[1],
            color="coral", fill=True)
axes[1].set_title("KDE plot")

sns.histplot(data=df, x="IMDB_Rating", bins=20, ax=axes[2],
             kde=True, color="teal")
axes[2].set_title("Histogram + KDE")

plt.tight_layout()
plt.show()

# Primjer 4 — Distribucije po kategoriji
# ---------------------------------------------------------------

plt.figure(figsize=(10, 5))
sns.histplot(data=df_top5, x="IMDB_Rating", hue="PrviZanr",
             bins=15, alpha=0.5)
plt.title("Distribucija ocjena po žanru")
plt.show()

plt.figure(figsize=(10, 5))
sns.kdeplot(data=df_top5, x="IMDB_Rating", hue="PrviZanr",
            fill=True, alpha=0.4)
plt.title("KDE po žanru")
plt.show()

# Primjer 5 — Boxplot i violinplot
# ---------------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.boxplot(data=df_top5, x="PrviZanr", y="IMDB_Rating",
            ax=axes[0], palette="Set2")
axes[0].set_title("Boxplot — Ocjene po žanru")

sns.violinplot(data=df_top5, x="PrviZanr", y="IMDB_Rating",
               ax=axes[1], palette="Set2")
axes[1].set_title("Violinplot — Ocjene po žanru")

plt.tight_layout()
plt.show()

# Primjer 6 — Heatmap korelacijske matrice
# ---------------------------------------------------------------

num_cols = ["IMDB_Rating", "Meta_score", "No_of_Votes", "Runtime"]
df["Runtime"] = df["Runtime"].str.replace(" min", "").astype(float)

korelacija = df[num_cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(korelacija, annot=True, cmap="coolwarm",
            center=0, fmt=".2f", linewidths=1)
plt.title("Korelacijska matrica — IMDB dataset")
plt.tight_layout()
plt.show()

# Primjer 7 — Pairplot (brzi pregled)
# ---------------------------------------------------------------

sns.pairplot(df[num_cols + ["PrviZanr"]].dropna(),
             hue="PrviZanr", palette="Set2",
             plot_kws={"alpha": 0.5, "s": 20})
plt.suptitle("Pairplot — IMDB Top 1000", y=1.02)
plt.show()

# Primjer 8 — Barplot s intervalom povjerenja
# ---------------------------------------------------------------

plt.figure(figsize=(10, 5))
sns.barplot(data=df_top5, x="PrviZanr", y="IMDB_Rating",
            palette="viridis", errorbar=("ci", 95))
plt.title("Prosječna ocjena po žanru (s intervalom povjerenja)")
plt.ylabel("Prosječna IMDB ocjena")
plt.show()

# Zadatak 1 — Top žanrovi (countplot)
# ---------------------------------------------------------------

df["PrviZanr"] = df["Genre"].str.split(",").str[0].str.strip()

top10 = df["PrviZanr"].value_counts().head(10).index
df_top10 = df[df["PrviZanr"].isin(top10)]

plt.figure(figsize=(10, 6))
sns.countplot(data=df_top10, y="PrviZanr",
              order=top10, palette="viridis")
plt.title("Top 10 žanrova — IMDB Top 1000")
plt.xlabel("Broj filmova")
plt.tight_layout()
plt.show()

# Zadatak 2 — Boxplot + Stripplot kombinirani
# ---------------------------------------------------------------

top5_zanrovi = df["PrviZanr"].value_counts().head(5).index
df_top5 = df[df["PrviZanr"].isin(top5_zanrovi)]

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df_top5, x="PrviZanr", y="IMDB_Rating",
            ax=ax, palette="Set2", order=top5_zanrovi)
sns.stripplot(data=df_top5, x="PrviZanr", y="IMDB_Rating",
              ax=ax, color="black", alpha=0.4, size=4,
              order=top5_zanrovi)
plt.title("IMDB ocjene po žanru — boxplot + strip")
plt.tight_layout()
plt.show()

# Zadatak 3 — Heatmap: Prosječna ocjena po deceniji i žanru
# ---------------------------------------------------------------

df["Released_Year"] = pd.to_numeric(df["Released_Year"], errors="coerce")
df["Decenija"] = (df["Released_Year"] // 10) * 10

df_top5 = df_top5.copy()
df_top5["Released_Year"] = pd.to_numeric(df_top5["Released_Year"], errors="coerce")
df_top5["Decenija"] = (df_top5["Released_Year"] // 10) * 10

pivot = pd.pivot_table(df_top5, values="IMDB_Rating",
                       index="Decenija", columns="PrviZanr",
                       aggfunc="mean")
pivot = pivot.loc[pivot.index >= 1950]

plt.figure(figsize=(10, 8))
sns.heatmap(pivot, annot=True, cmap="YlOrRd", fmt=".1f",
            linewidths=0.5)
plt.title("Prosječna IMDB ocjena — Decenija vs Žanr")
plt.tight_layout()
plt.show()

# Zadatak 4 — Seaborn dashboard (subplots 2x2)
# ---------------------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

sns.histplot(data=df, x="IMDB_Rating", bins=20, kde=True,
             ax=axes[0, 0], color="steelblue")
axes[0, 0].set_title("Distribucija IMDB ocjena")

df["Runtime_num"] = pd.to_numeric(df["Runtime"], errors="coerce")
df_top5["Runtime_num"] = pd.to_numeric(df_top5["Runtime"], errors="coerce")
sns.boxplot(data=df_top5, x="PrviZanr", y="Runtime_num",
            ax=axes[0, 1], palette="Set2")
axes[0, 1].set_title("Runtime po žanru")

sns.scatterplot(data=df_top5, x="IMDB_Rating", y="No_of_Votes",
                hue="PrviZanr", alpha=0.5, ax=axes[1, 0])
axes[1, 0].set_title("Rating vs Glasovi")

prosjek = df.groupby("Decenija")["IMDB_Rating"].mean().reset_index()
prosjek = prosjek[prosjek["Decenija"] >= 1960]
sns.barplot(data=prosjek, x="Decenija", y="IMDB_Rating",
            ax=axes[1, 1], color="coral")
axes[1, 1].set_title("Prosjek po deceniji")
axes[1, 1].tick_params(axis="x", rotation=45)

plt.suptitle("IMDB Top 1000 — Seaborn Dashboard", fontsize=16)
plt.tight_layout()
plt.show()
