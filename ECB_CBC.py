from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os

def encrypt_image(image, key, mode):
    # Converter a imagem em bytes
    image_data = np.array(image)
    original_shape = image_data.shape
    data = image_data.tobytes()

    # Padding para múltiplos de 16 bytes
    padding_length = (-len(data)) % 16
    padded_data = data + b'\0' * padding_length

    # Selecionar modo de cifra
    if mode == 'ECB':
        cipher = Cipher(algorithms.AES(key), modes.ECB())
    elif mode == 'CBC':
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    else:
        raise ValueError("Modo inválido")

    # Cifrar
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Converter os bytes cifrados em imagem
    encrypted_data = encrypted_data[:len(data)]

    encrypted_array = np.frombuffer(
        encrypted_data, dtype=np.uint8
    ).reshape(original_shape)

    return Image.fromarray(encrypted_array)


# Chave AES-256
key = os.urandom(32)

# Imagem original
original = Image.open("VitoriaGuimaraes.png").convert("RGB")

# Cifrar nos dois modos
ecb = encrypt_image(original, key, 'ECB')
cbc = encrypt_image(original, key, 'CBC')

# Criar um único plot com as 3 imagens
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(original)
axes[0].set_title("Imagem Original")

axes[1].imshow(ecb)
axes[1].set_title("AES - ECB")

axes[2].imshow(cbc)
axes[2].set_title("AES - CBC")

# Remover eixos
for ax in axes:
    ax.axis('off')

plt.tight_layout()
plt.show()