from PIL import Image
import os

# Convertir PNG a ICO
imagen_png = "foto_de_perfil_durísima.jpg"  # Cambia esto por tu imagen real
icono_ico = "icono.ico"

if os.path.exists(imagen_png):
    img = Image.open(imagen_png)
    
    # Los iconos necesitan múltiples tamaños (Windows)
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    
    # Redimensionar y guardar como ICO
    img.save(icono_ico, format='ICO', sizes=sizes)
    print(f"Icono creado: {icono_ico}")
else:
    print(f"Error: No se encuentra {imagen_png}")
    # Crear un icono básico como fallback
    img = Image.new('RGB', (64, 64), color='red')
    img.save(icono_ico, format='ICO')