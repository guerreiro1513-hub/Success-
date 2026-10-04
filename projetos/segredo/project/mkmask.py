# Mascara de "lente": centro nitido, bordas desfocadas (simula pouca profundidade de campo).
import numpy as np
from PIL import Image
W, H = 1080, 1920
y, x = np.mgrid[0:H, 0:W].astype(float)
r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H * 0.47) / (H / 2)) ** 2)
m = np.clip((r - 0.62) / 0.55, 0, 1) ** 1.6
Image.fromarray((m * 255).astype(np.uint8), "L").save("/home/user/Success-/projetos/segredo/work/lente.png")
