# 🦠 Simulador de Ransomware Académico

**⚠️ ADVERTENCIA:** Software educativo. Solo usar en máquinas virtuales aisladas y con permiso.

## 📦 Qué hace

- **Encripta** archivos (.txt, .pdf, .docx, .jpg, .png) en Escritorio, Documentos y Descargas.
- **Ofusca** el malware para que parezca una imagen (.png).
- **Incluye herramienta de recuperación** con contraseña predefinida.

## 🔧 Compilación PASO A PASO

### 1. Instalar dependencias (en tu PC real o VM)

```bash
pip install cryptography pyinstaller
```

### 2. Compilar el ransomware principal

```bash
# Crea un .exe de 64 bits (asegúrate de usar Python 64-bit)
pyinstaller --onefile --noconsole --name=malware joseo.PY
```

El ejecutable `malware.exe` estará en la carpeta `/dist`.

### 3. Compilar el wrapper ofuscado (para hacerlo parecer una imagen)

```bash
# Copia el malware compilado y una imagen real a la misma carpeta
copy dist\malware.exe .
copy tu_imagen_real.png imagen.png

# Compila el wrapper
pyinstaller --onefile --noconsole --name="Foto_Inocente" wrapper.py
```

### 4. Renombrar para engañar (en la VM de prueba)

```bash
# Cambia el nombre para que parezca una imagen (Windows oculta ".exe")
ren dist\Foto_Inocente.exe "Vacaciones_2024.png.exe"
```

**Resultado:** El archivo `Vacaciones_2024.png.exe` mostrará el icono de un ejecutable, pero al usuario le parecerá una imagen llamada `Vacaciones_2024.png`.

### 5. Compilar el decryptor

```bash
pyinstaller --onefile --name=DecryptorTool decryptor.py
```

## 🧪 Ejecutar la prueba (EN LA VM AISLADA)

#### A. Ejecutar el ransomware directamente:

```bash
malware.exe
```

#### B. Ejecutar la versión ofuscada (simula un ataque real):

Hacer doble clic en `Vacaciones_2024.png.exe`.

### ¿Qué ocurrirá?

- Se encriptarán los archivos de las carpetas objetivo.
- Se añadirá la extensión `.locked`.
- Se creará un archivo `READ_ME.txt` con instrucciones falsas.

## 🔓 Recuperar los archivos

```bash
# Ejecuta la herramienta de recuperación
DecryptorTool.exe

# Introduce la contraseña cuando se pida:
# Contraseña por defecto: Melointrodujeronymegustó___67
```

## ⚙️ Personalización

Antes de compilar, puedes modificar en `ransomware.py`:

- **TARGET_DIRS:** Carpetas a atacar.
- **FILE_EXTENSIONS:** Tipos de archivo a encriptar.
- **PASSWORD:** Contraseña para la recuperación.

## 📝 Para tu informe académico

Documenta:

- **Técnicas usadas:** Encriptación (AES-256 via Fernet), ofuscación (steganografía por nombre).
- **Propósito educativo:** Entender el funcionamiento para mejorar las defensas.
- **Prevención:** Activar "Mostrar extensiones de archivo" en Windows y usar antivirus.

---

**⚠️ IMPORTANTE:** Todo el código debe ejecutarse únicamente en un entorno de pruebas controlado y aislado (máquina virtual sin conexión a red).
