
import cv2
import numpy as np
import tensorflow as tf
import os

# --- Configuración ---
IMG_SIZE = 224
DATASET_PATH = "dataset"

# Cargar el modelo entrenado
model = tf.keras.models.load_model("modelo_entrenado.h5")

# Cargar nombres de las clases
class_names = sorted(os.listdir(DATASET_PATH))
print("Clases detectadas:", class_names)

# Detector de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Captura de video
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("⚠ No se pudo acceder a la cámara.")
    exit()

print("\n🎥 Reconocimiento facial iniciado...")
print("Presiona 'q' para salir.\n")

while True:
    ret, frame = cap.read()
    if not ret: break

    # Espejo (opcional, se siente más natural)
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # COPIA del frame para dibujar (para no ensuciar la imagen original si quisieras guardarla)
    display_frame = frame.copy()

    # Detectar rostros
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    for (x, y, w, h) in faces:
        # --- CORRECCIÓN CRÍTICA ---
        # 1. Extraer la región de interés (ROI)
        face_roi = frame[y:y+h, x:x+w]
        
        # 2. CONVERTIR DE BGR A RGB (Vital para Keras/TensorFlow)
        face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
        
        # 3. Redimensionar y Normalizar
        face_resized = cv2.resize(face_rgb, (IMG_SIZE, IMG_SIZE))
        face_normalized = face_resized / 255.0
        face_input = np.expand_dims(face_normalized, axis=0)

        # Predicción
        preds = model.predict(face_input, verbose=0)
        class_id = np.argmax(preds)
        prob = preds[0][class_id]

        # Lógica de visualización
        if prob < 0.50: # Puedes subir esto a 0.7 si quieres ser más estricto
            label = "Desconocido"
            color = (0, 0, 255) # Rojo
        else:
            label = f"{class_names[class_id]}: {prob*100:.1f}%"
            color = (0, 255, 0) # Verde

        # Dibujar en el frame original (que sigue en BGR para que OpenCV lo muestre bien)
        cv2.rectangle(display_frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(display_frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Reconocimiento Facial - CNN", display_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()
