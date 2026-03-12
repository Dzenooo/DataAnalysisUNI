import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\korisnik\Downloads\ufo_sightings.csv", low_memory=False)

df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

df["year"] = df["datetime"].dt.year

year_counts = df["year"].value_counts().sort_index()

plt.figure()
year_counts.plot()

plt.title("UFO Sightings per Year")
plt.xlabel("Year")
plt.ylabel("Number of UFO Sightings")

plt.show()
