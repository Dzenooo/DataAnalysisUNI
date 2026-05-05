import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

#najjednostavniji graf
x = [1, 2, 3, 4, 5]
y = [2, 4, 7, 11, 16]

plt.plot(x, y)
plt.title("Moj prvi graf")
plt.xlabel("X osa")
plt.ylabel("Y osa")
plt.show()

#Stilizacija linijskog grafa

x = np.linspace(0, 10, 100)

plt.plot(x, np.sin(x), label="sin(x)", color="blue", linewidth=2)
plt.plot(x, np.cos(x), label="cos(x)", color="red", linestyle="--")

plt.title("Trigonometrijske funkcije")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


#Scatter plot (IMDB dataset)

df = pd.read_csv("data/imdb_top_1000.csv")

plt.figure(figsize=(10, 6))
plt.scatter(df["IMDB_Rating"], df["Meta_score"],
            alpha=0.5, s=20, color="teal")
plt.title("IMDB Rating vs Metascore")
plt.xlabel("IMDB Rating")
plt.ylabel("Metascore")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

#Bar chart (IMDB redatelji)

top_dirs = df["Director"].value_counts().head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_dirs.index, top_dirs.values, color="coral")
plt.title("Top 10 reditelja u IMDB Top 1000")
plt.xlabel("Broj filmova")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

#Histogram (distribucija ocjena)

plt.figure(figsize=(10, 5))
plt.hist(df["IMDB_Rating"], bins=20, color="steelblue",
         edgecolor="white", alpha=0.8)
plt.title("Distribucija IMDB ocjena (Top 1000)")
plt.xlabel("IMDB Rating")
plt.ylabel("Broj filmova")
plt.axvline(df["IMDB_Rating"].mean(), color="red",
            linestyle="--", label=f"Prosjek: {df['IMDB_Rating'].mean():.2f}")
plt.legend()
plt.tight_layout()
plt.show()

#Subplots (više grafova odjednoom)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Lijevi graf: histogram
axes[0].hist(df["IMDB_Rating"], bins=20, color="steelblue")
axes[0].set_title("Distribucija ocjena")
axes[0].set_xlabel("IMDB Rating")

# Desni graf: scatter
axes[1].scatter(df["IMDB_Rating"], df["No_of_Votes"],
                alpha=0.3, s=10, color="coral")
axes[1].set_title("Rating vs Glasovi")
axes[1].set_xlabel("IMDB Rating")
axes[1].set_ylabel("Broj glasova")

plt.tight_layout()
plt.show()

#Učitavanje slike i prikaz

img = np.asarray(Image.open("data/pypy.jpg"))

print(f"type:  {type(img)}")
print(f"shape: {img.shape}")
print(f"dtype: {img.dtype}")

plt.imshow(img)
plt.title("Python — doslovno!")
plt.axis("off")
plt.show()

#Izdvajanje kanala + colormaps

red_channel = img[:, :, 0]
print(f"Red channel shape: {red_channel.shape}")

# Default colormap (viridis)
plt.imshow(red_channel)
plt.colorbar()
plt.title("Crveni kanal — viridis colormap")
plt.show()

# Hot colormap
plt.imshow(red_channel, cmap="hot")
plt.colorbar()
plt.title("Crveni kanal — hot colormap")
plt.show()

#Histogram slike (analiza piksela)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].imshow(img)
axes[0].set_title("Originalna slika")
axes[0].axis("off")

axes[1].hist(red_channel.ravel(), bins=range(1, 256),
             color="red", alpha=0.7)
axes[1].set_title("Histogram crvenog kanala")
axes[1].set_xlabel("Vrijednost piksela (0-255)")
axes[1].set_ylabel("Broj piksela")

plt.tight_layout()
plt.show()

#Podešavanje kontrasta

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].imshow(red_channel, cmap="gray")
axes[0].set_title("Puni raspon (0-255)")

axes[1].imshow(red_channel, cmap="gray", clim=(50, 200))
axes[1].set_title("clim=(50, 200)")

axes[2].imshow(red_channel, cmap="gray", clim=(170, 180))
axes[2].set_title("clim=(100, 180)")

for ax in axes:
    ax.axis("off")
plt.tight_layout()
plt.show()

#Interpolacija

small = Image.open("data/pypy.jpg")
small.thumbnail((16, 16))

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].imshow(small, interpolation="nearest")
axes[0].set_title("Nearest (pikselizirano)")

axes[1].imshow(small, interpolation="bilinear")
axes[1].set_title("Bilinear (glatkije)")

axes[2].imshow(small, interpolation="bicubic")
axes[2].set_title("Bicubic (najglatkije)")

for ax in axes:
    ax.axis("off")
plt.tight_layout()
plt.show()

#ZADATAK 1 IMDB TOP ŽANROVI

df = pd.read_csv("data/imdb_top_1000.csv")
df["PrviZanr"] = df["Genre"].str.split(",").str[0].str.strip()

top_zanrovi = df["PrviZanr"].value_counts().head(10)

plt.figure(figsize=(10, 6))
bars = plt.barh(top_zanrovi.index, top_zanrovi.values, color="teal")
plt.title("Top 10 žanrova u IMDB Top 1000")
plt.xlabel("Broj filmova")
plt.gca().invert_yaxis()

# Bonus: brojevi na stupcima
for bar in bars:
    plt.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
             str(int(bar.get_width())), va="center", fontsize=10)

plt.tight_layout()
plt.show()

#ZADATAK 2 - IMDB ocjene kroz decenije (line plot)

df["Released_Year"] = pd.to_numeric(df["Released_Year"], errors="coerce")
df["Decenija"] = (df["Released_Year"] // 10) * 10

prosjek = df.groupby("Decenija")["IMDB_Rating"].mean()

plt.figure(figsize=(10, 5))
plt.plot(prosjek.index, prosjek.values, "--", color="navy",
         linewidth=2, markersize=8, label="Prosječna ocjena")
plt.title("Prosječna IMDB ocjena po deceniji")
plt.xlabel("Decenija")
plt.ylabel("Prosječna ocjena")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

#ZADATAK 3 - Subplots : 4 grafa u jednoj figuri

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Gore lijevo: histogram IMDB_Rating
axes[0, 0].hist(df["IMDB_Rating"], bins=20, color="steelblue",
                edgecolor="white")
axes[0, 0].set_title("Distribucija IMDB ocjena")
axes[0, 0].set_xlabel("IMDB Rating")
axes[0, 0].set_ylabel("Broj filmova")

# Gore desno: histogram Meta_score
axes[0, 1].hist(df["Meta_score"].dropna(), bins=20, color="coral",
                edgecolor="white")
axes[0, 1].set_title("Distribucija Metascore")
axes[0, 1].set_xlabel("Metascore")
axes[0, 1].set_ylabel("Broj filmova")

# Dolje lijevo: scatter Rating vs Votes
axes[1, 0].scatter(df["IMDB_Rating"], df["No_of_Votes"],
                    alpha=0.3, s=10, color="teal")
axes[1, 0].set_title("Rating vs Glasovi")
axes[1, 0].set_xlabel("IMDB Rating")
axes[1, 0].set_ylabel("Broj glasova")

# Dolje desno: bar chart top 5 reditelja
top5 = df["Director"].value_counts().head(5)
axes[1, 1].barh(top5.index, top5.values, color="green")
axes[1, 1].set_title("Top 5 reditelja")
axes[1, 1].set_xlabel("Broj filmova")
axes[1, 1].invert_yaxis()

plt.tight_layout()
plt.show()

#ZADATAK 4 - Analiza slike pypy.jbg

print(f"Shape: {img.shape}, Dtype: {img.dtype}")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Gore lijevo: originalna slika
axes[0, 0].imshow(img)
axes[0, 0].set_title("Original")
axes[0, 0].axis("off")

# Gore desno: zeleni kanal
axes[0, 1].imshow(img[:, :, 1], cmap="Greens")
axes[0, 1].set_title("Zeleni kanal")
axes[0, 1].axis("off")

# Dolje lijevo: grayscale
gray = img.mean(axis=2)
axes[1, 0].imshow(gray, cmap="gray")
axes[1, 0].set_title("Grayscale")
axes[1, 0].axis("off")

# Dolje desno: RGB histogram
for i, boja in enumerate(["red", "green", "blue"]):
    axes[1, 1].hist(img[:, :, i].ravel(), bins= range(1, 256),
                     color=boja, alpha=0.5, label=boja.upper())
axes[1, 1].set_title("RGB Histogram")
axes[1, 1].set_xlabel("Vrijednost piksela (0-255)")
axes[1, 1].set_ylabel("Broj piksela")
axes[1, 1].legend()

plt.tight_layout()
plt.show()

#ZADATAK 5 - MINI CHALLENGE

#Koji žanrovi zarađuju najviše?

df["Gross_clean"] = df["Gross"].str.replace(",", "").astype(float)
df["PrviZanr"] = df["Genre"].str.split(",").str[0].str.strip()

zarada_po_zanru = (df.groupby("PrviZanr")["Gross_clean"]
                     .mean()
                     .dropna()
                     .sort_values(ascending=True)
                     .tail(10))

plt.figure(figsize=(10, 6))
plt.barh(zarada_po_zanru.index, zarada_po_zanru.values / 1e6,
         color="goldenrod", edgecolor="white")
plt.title("Prosječna zarada po žanru (IMDB Top 1000)", fontsize=14)
plt.xlabel("Prosječna zarada (milioni $)")
plt.tight_layout()
plt.show()

#Koliko filmova po deceniji?

df["Released_Year"] = pd.to_numeric(df["Released_Year"], errors="coerce")
df["Decenija"] = (df["Released_Year"] // 10) * 10
po_deceniji = df.groupby("Decenija").size()

plt.figure(figsize=(10, 5))
bars = plt.bar(po_deceniji.index.astype(int), po_deceniji.values,
               width=8, color="steelblue", edgecolor="white")

for bar in bars:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
             str(int(bar.get_height())), ha="center", fontsize=9)

plt.title("Broj filmova u IMDB Top 1000 po deceniji", fontsize=14)
plt.xlabel("Decenija")
plt.ylabel("Broj filmova")
plt.tight_layout()
plt.show()

#Koji reditelji ima najbolji prosječni rating?

dir_counts = df["Director"].value_counts()
dirs_3plus = dir_counts[dir_counts >= 3].index

df_filtered = df[df["Director"].isin(dirs_3plus)]
best_dirs = (df_filtered.groupby("Director")["IMDB_Rating"]
                        .mean()
                        .sort_values(ascending=True)
                        .tail(10))

plt.figure(figsize=(10, 6))
plt.barh(best_dirs.index, best_dirs.values, color="darkgreen",
         edgecolor="white")
plt.title("Top 10 reditelja po prosječnom ratingu (min. 3 filma)")
plt.xlabel("Prosječni IMDB Rating")
plt.xlim(left=7.5)
plt.tight_layout()
plt.show()

#pypy.jpg kroz razne colormap-e

img = np.asarray(Image.open("data/pypy.jpg"))
gray = img.mean(axis=2)

cmaps = ["gray", "viridis", "hot", "cool", "nipy_spectral", "terrain"]

fig, axes = plt.subplots(2, 3, figsize=(15, 9))

for ax, cmap_name in zip(axes.ravel(), cmaps):
    ax.imshow(gray, cmap=cmap_name)
    ax.set_title(f'cmap="{cmap_name}"', fontsize=12)
    ax.axis("off")

plt.suptitle("python.jpg — 6 različitih colormap-a", fontsize=16, y=0.98)
plt.tight_layout()
plt.show()


