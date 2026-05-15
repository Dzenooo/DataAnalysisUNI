import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

#FASTA loading

def load_fasta(file_path):
    sequences = []
    with open(file_path, "r") as f:
        seq = ""
        for line in f:
            if line.startswith(">"):
                if seq:
                    sequences.append(seq)
                    seq = ""
            else:
                seq += line.strip().upper()
        if seq:
            sequences.append(seq)
    return sequences

#Datasets & labels

DATA_DIR = "data"
sequences = []
labels = []

#Za zadatak 2 - isključivanje jedne vrste
#EXCLUDED_SPECIES = "frog_species_3"

for filename in os.listdir(DATA_DIR):
    if filename.endswith(".fasta"):
        species_map = {
            "frog_species_1": "Xenopus tropicalis",
            "frog_species_2": "Xenopus laevis",
            "frog_species_3": "Rana temporaria"
        }
        species_name = species_map.get(filename.replace(".fasta", ""), filename.replace(".fasta", ""))
        file_path = os.path.join(DATA_DIR, filename)
        seqs = load_fasta(file_path)
        sequences.extend(seqs)
        labels.extend([species_name] * len(seqs))

print(f"Učitano {len(sequences)} sekvenci iz {len(set(labels))} vrste")

#K-mer ekstrakcija i kreiranje matrice

def kmer_frequency(sequence, k):
    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    return Counter(kmers)

def build_kmer_matrix(sequences, k):
    all_kmers = set()
    kmer_counts = []
    for seq in sequences:
        counts = kmer_frequency(seq, k)
        kmer_counts.append(counts)
        all_kmers.update(counts.keys())
    all_kmers = sorted(all_kmers)
    X = np.zeros((len(sequences), len(all_kmers)))
    for i, counts in enumerate(kmer_counts):
        for j, kmer in enumerate(all_kmers):
            X[i, j] = counts.get(kmer, 0)
    return X


#Dijeljenje sekvenci na chunkove

def split_into_chunks(sequence, chunk_size=500, step=200):
    chunks = []
    for i in range(0, len(sequence) - chunk_size + 1, step):
        chunks.append(sequence[i:i+chunk_size])
    return chunks

chunked_sequences = []
chunked_labels = []

for seq, lab in zip(sequences, labels):
    chunks = split_into_chunks(seq, chunk_size=500, step=200)
    chunked_sequences.extend(chunks)
    chunked_labels.extend([lab] * len(chunks))

print(f"Nakon dijeljenja: {len(chunked_sequences)} chunkova iz {len(set(chunked_labels))} vrste")

#zadatak 1 - mijenjamo vrijednost k i pratimo promjenu rezultata
k = 4
X = build_kmer_matrix(chunked_sequences, k)
labels = chunked_labels
print(f"Feature matrica: {X.shape[0]} uzoraka x {X.shape[1]} k-mera (k={k})")


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

#PCA vizualizacija

plt.figure(figsize=(8, 6))
unique_labels = sorted(set(labels))
for lab in unique_labels:
    idx = [i for i, l in enumerate(labels) if l == lab]
    plt.scatter(X_pca[idx, 0], X_pca[idx, 1], label=lab, alpha=0.7)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title(f"PCA of Frog DNA k-mer Features (k={k})")
plt.legend()
plt.tight_layout()
plt.show()

#Klasifikacija

label_map = {lab: i for i, lab in enumerate(unique_labels)}
y = np.array([label_map[l] for l in labels])

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

#Zadatak 3 mijenjamo RandomForest sa logistickom regresijom

#model = LogisticRegression(max_iter=1000)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)


print("\n── Classification Report ──")
print(classification_report(y_test, y_pred, target_names=unique_labels))