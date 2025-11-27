# detectar_bolinhas.py

from PIL import Image
import numpy as np
from scipy.ndimage import label, center_of_mass
import os
import django

# ======== CONFIGURAR DJANGO =========
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PROJETO_SOFTWARE_MOVPUC.settings")
django.setup()

from app_usuarios.models import Vaga

# ======== CARREGAR IMAGEM ==========
print("Carregando imagem...")
img = Image.open("static/app_usuarios/img/estacionamento.png").convert("RGB")
arr = np.array(img)

# ======== DETECTAR PIXELS VERMELHOS =========
print("Detectando bolinhas vermelhas...")
mask = (arr[:,:,0] > 200) & (arr[:,:,1] < 80) & (arr[:,:,2] < 80)

# ======== ENCONTRAR COMPONENTES =========
labels, num = label(mask)
coords = center_of_mass(mask, labels, range(1, num+1))

h, w = arr.shape[:2]

print(f"Total detectado: {num}")
print("Salvando no banco...\n")

# ======== LIMPAR TABELA ANTES DE INSERIR =========
Vaga.objects.all().delete()

# ======== SALVAR NO BANCO =========
for i, (y, x) in enumerate(coords, 1):
    top = (y / h) * 100
    left = (x / w) * 100

    Vaga.objects.create(
        numero=i,
        top=top,
        left=left,
        ocupada=False
    )

    print(f"Vaga {i}: top={top:.2f}%, left={left:.2f}%")

print("\n✅ PRONTO! As vagas foram registradas no banco de dados.")