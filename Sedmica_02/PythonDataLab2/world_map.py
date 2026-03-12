import pandas as pd
import plotly.express as px

df = pd.read_csv(r"C:\Users\korisnik\Downloads\ufo_sightings.csv", low_memory=False)

fig = px.scatter_geo(
    df,
    lat="latitude",
    lon="longitude",
    hover_name = "city",
    title = "UFO Sightings Around the World",
)

fig.show()