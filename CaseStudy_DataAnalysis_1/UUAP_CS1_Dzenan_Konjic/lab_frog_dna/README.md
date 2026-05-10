# Lab Frog DNA — Klasifikacija DNA sekvenci s k-merima

## Opis projekta
Analiza i klasifikacija mitohondrijalnih DNA sekvenci triju vrsta žaba 
korištenjem k-mer frekvencijskog kodiranja, PCA vizualizacije i mašinskog učenja.

## Vrste žaba
- frog_species_1 — Xenopus tropicalis (zapadna pandžaša) | NCBI: NC_006839
- frog_species_2 — Xenopus laevis (afrička pandžaša)     | NCBI: NC_001573
- frog_species_3 — Rana temporaria (evropska smeđa žaba) | NCBI: NC_042226

## Struktura projekta
lab_frog_dna/
├── data/
│   ├── frog_species_1.fasta
│   ├── frog_species_2.fasta
│   └── frog_species_3.fasta
├── lab_pipeline.py
└── README.md

## Pokretanje
python lab_pipeline.py

## Zavisnosti
- numpy
- scikit-learn
- matplotlib

## Autor
Dzenan Konjic — Uvod u analizu podataka 2025/2026