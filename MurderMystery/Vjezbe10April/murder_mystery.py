import pandas as pd
from datetime import time

izvjestaj = pd.read_csv('data/policijski_izvjestaj.csv')
osumnjiceni = pd.read_csv('data/osumnjiceni.csv')
kartice = pd.read_csv('data/pristupne_kartice.csv')
svjedoci = pd.read_csv('data/izjave_svjedoka.csv')
telefoni = pd.read_csv('data/telefonski_zapisi.csv')
finansije = pd.read_csv('data/finansijski_zapisi.csv')

print(f"Osumnjičenih: {len(osumnjiceni)}")
print(f"Pristupnih zapisa: {len(kartice)}")
print(f"Telefonskih zapisa: {len(telefoni)}")
print(f"Finansijski zapisa: {len(finansije)}")

ubistvo = izvjestaj[izvjestaj["tip"] == "ubistvo"]
print(ubistvo[["datum", "vrijeme", "lokacija", "opis"]].to_string(index=False))

tech_hub_15 = kartice[(kartice["zgrada"] == "Tech Hub") &
                      (kartice["datum"] == "2026-03-15")]


u_zgradi = tech_hub_15.merge(osumnjiceni, on="ime_prezime")

print(f"Ukupno ulazaka: {len(tech_hub_15)}")
print(f"Od toga osumnjiceni: {len(u_zgradi)}")
print(u_zgradi[["ime_prezime", "vrijeme_ulaza", "vrijeme_izlaza", "veza_sa_zrtvom"]].to_string(index=False))


tech_hub_sve = kartice[kartice["zgrada"] == "Tech Hub"]
sve = tech_hub_sve.merge(osumnjiceni, on="ime_prezime")

print(sve.groupby("ime_prezime")["datum"].nunique()
      .sort_values(ascending=False).to_string())

print(u_zgradi["ime_prezime"].value_counts().to_string())


# Ko je bio u zgradi između 19:30 i 20:30 (preklapanje sa intervalom).
start_time = time(19, 30)
end_time = time(20, 30)

ulaz = pd.to_datetime(tech_hub_15["vrijeme_ulaza"], format="%H:%M").dt.time
izlaz = pd.to_datetime(tech_hub_15["vrijeme_izlaza"], format="%H:%M").dt.time

u_prozoru = tech_hub_15[(ulaz <= end_time) & (izlaz >= start_time)]
print(f"\nPrisustvo u Tech Hub između {start_time.strftime('%H:%M')} i {end_time.strftime('%H:%M')}:")
if u_prozoru.empty:
    print("Nema zapisa.")
else:
    print(u_prozoru[["ime_prezime", "vrijeme_ulaza", "vrijeme_izlaza"]].to_string(index=False))

# Filtriraj sve koji su izašli poslije 19:30.
izlaz_poslije = time(19, 30)
kasni_izlazak = tech_hub_15[izlaz > izlaz_poslije]
print(f"\nIzlazak poslije {izlaz_poslije.strftime('%H:%M')}:")
if kasni_izlazak.empty:
    print("Nema zapisa.")
else:
    print(kasni_izlazak[["ime_prezime", "vrijeme_ulaza", "vrijeme_izlaza"]].to_string(index=False))


print(f"Izjava: {len(svjedoci)}")

izjave_emir = svjedoci[svjedoci["spominje_osumnjicenog"] == "Emir Begović"]

print(izjave_emir[["opis", "lokacija", "vrijeme"]].to_string(index=False))

izjave_dino = svjedoci[svjedoci["spominje_osumnjicenog"] == "Dino Delić"]

print(izjave_dino[["opis", "lokacija", "vrijeme"]].to_string(index=False))



izjava_emir = svjedoci[svjedoci["svjedok"] == "Emir Begović"]

print(izjava_emir[["opis", "lokacija", "vrijeme"]].to_string(index=False))



izjava_dino = svjedoci[svjedoci["svjedok"] == "Dino Delić"]

print(izjava_dino[["opis", "lokacija", "vrijeme"]].to_string(index=False))



nepoznati = svjedoci[svjedoci["spominje_osumnjicenog"].isna() |
                     (svjedoci["spominje_osumnjicenog"] == "")]
print(nepoznati[["izjava_id", "vrijeme", "opis"]].to_string(index=False))



print(osumnjiceni[(osumnjiceni["visina_cm"] > 180) &
                  (osumnjiceni["boja_kose"] == "crna")]
      [["ime_prezime", "visina_cm", "boja_kose"]].to_string(index=False))




sve = tech_hub_sve.merge(osumnjiceni, on="ime_prezime")

sve = tech_hub_sve.merge(osumnjiceni, on="ime_prezime")
#merge za pozivatelja
# sa_imenima = telefoni.merge(
#     osumnjiceni[["ime_prezime", "telefon"]],
#     left_on="ime_prezime",
#     right_on="telefon", how="left")
#
# sa_imenima = sa_imenima.rename(columns={"ime_prezime": "pozivatelj"})
# #merge za primaoca
# sa_imenima = sa_imenima.merge(
#     osumnjiceni[["ime_prezime", "telefon"]],
#     left_on="telefon_primaoca",
#     right_on="telefon", how="left",
#     suffixes=("", "_primalac"))
# sa_imenima = sa_imenima.rename(columns={"ime_prezime": "primalac"})
#
# #emirovi pozivi
#
# emir_kasno = sa_imenima[
#     (sa_imenima["pozivatelj"] == "Emir Begović") &
#     (sa_imenima["datum"] == "2026-03-15") &
#     (sa_imenima["vrijeme"] > "20:00")]
#
# print(emir_kasno[["vrijeme", "telefon_primaoca", "primalac",
#                   "trajanje_sekundi"]].sort_values("vrijeme")
#       .to_string(index=False))

#sav bilans
print(finansije.groupby("ime_prezime")["iznos_KM"].sum())

