from PIL import Image
from gtts import gTTS
import easyocr
import numpy as np
import os

class TextoManuscritoAVoz:
    def __init__(self):
        #modelo EasyOCR
        print("Cargando modelo EasyOCR...")
        self.lector = easyocr.Reader(['es', 'en'])
        print("Modelo cargado correctamente\n")
    
    def preprocesar_imagen(self, ruta_imagen):
        #Carga y convierte la imagen
        print("Paso 1: Preprocesando imagen...")
        imagen = Image.open(ruta_imagen).convert("RGB")
        return imagen
    
    def detectar_y_reconocer_texto(self, imagen):
        #detecta y reconoce caracteres manuscritos
        print("Paso 2-3: Detectando y reconociendo texto manuscrito...")
        
        imagen_np = np.array(imagen)
        resultado = self.lector.readtext(imagen_np)
        texto_generado = ' '.join([texto[1] for texto in resultado])
        
        print(f"  - Texto detectado: '{texto_generado}'")
        return texto_generado
    
    def postprocesar_texto(self, texto):
        #limpia y normaliza el texto
        print("Paso 4: Post-procesando texto...")
        
        texto_limpio = texto.strip()
        
        # Agrega punto final si no tiene puntuacion
        if texto_limpio and texto_limpio[-1] not in '.!?':
            texto_limpio += '.'
        
        print(f"  - Texto limpio: '{texto_limpio}'")
        return texto_limpio
    
    def texto_a_voz(self, texto, ruta_salida="audio_salida.mp3"):
        #Convierte texto a audio en español
        print("Paso 5: Generando audio en español...")
        
        tts = gTTS(text=texto, lang='es', slow=False)
        tts.save(ruta_salida)
        
        print(f"  - Audio generado: {ruta_salida}")
        return ruta_salida
    
    def procesar_pipeline(self, ruta_imagen, audio_salida="audio_salida.mp3"):

        print("INICIANDO PIPELINE DE PROCESAMIENTO\n")

        
        try:
            #1 Preprocesamiento
            imagen = self.preprocesar_imagen(ruta_imagen)
            
            #2-3 Deteccion y Reconocimiento
            texto_reconocido = self.detectar_y_reconocer_texto(imagen)
            
            if not texto_reconocido:
                print("Error: No se detecto texto en la imagen")
                return None
            
            #4 Post-procesamiento
            texto_limpio = self.postprocesar_texto(texto_reconocido)
            
            #5 Sintesis de voz
            ruta_audio = self.texto_a_voz(texto_limpio, audio_salida)
            
            
            print("PIPELINE COMPLETADO EXITOSAMENTE\n")
            print(f"\nTexto final: {texto_limpio}")
            print(f"Audio guardado en: {ruta_audio}\n")
            
            return {
                'texto': texto_limpio,
                'ruta_audio': ruta_audio
            }
            
        except Exception as e:
            print(f"\nError en el pipeline: {str(e)}")
            return None


def main():

    sistema = TextoManuscritoAVoz()
    
    #procesar imagen
    ruta_imagen = "test8.jpg"
    
    if not os.path.exists(ruta_imagen):
        print(f"Archivo no encontrado: {ruta_imagen}")
        print("Coloca una imagen con texto manuscrito en el mismo directorio")
        print("o cambia la ruta en la linea: ruta_imagen = 'tu_imagen.jpg'")
        return
    
    #pipeline completo
    resultado = sistema.procesar_pipeline(
        ruta_imagen=ruta_imagen,
        audio_salida="texto_manuscrito_audio.mp3"
    )
    
    if resultado:
        print("Proceso completado. Puedes reproducir el audio generado.")


if __name__ == "__main__":
    main()