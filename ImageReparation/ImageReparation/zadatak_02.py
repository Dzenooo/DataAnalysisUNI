from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# 1. Učitaj sliku
img = Image.open("data/broken_image.png")
arr = np.array(img)

# 2. Rotiraj za 180°
arr_rotated = np.rot90(arr, k=2)

# 3. Zamijeni R i B kanal slicingom (RGB -> BGR -> ponovo RGB)
arr_fixed = arr_rotated[:, :, ::-1]

# 4. Prikaži
plt.imshow(arr_fixed)
plt.title("Ispravljena slika")
plt.axis("off")
plt.show()
