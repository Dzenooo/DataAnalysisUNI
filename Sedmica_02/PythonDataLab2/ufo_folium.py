import pandas as pd
import folium

df = pd.read_csv(r"C:\Users\korisnik\Downloads\ufo_sightings.csv", low_memory=False)

df["latitude"]  = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

df = df.dropna(subset=["latitude", "longitude"])

df = df.sample(3000)

ufo_map = folium.Map(location=[20, 0], zoom_start=2)

for index, row in df.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=2,
        color="red",
        popup=row["city"]
    ).add_to(ufo_map)

ufo_map.save("ufo_map.html")