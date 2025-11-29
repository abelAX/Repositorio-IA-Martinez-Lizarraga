import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import cv2
import numpy as np
import tensorflow as tf
import os


IMG_SIZE = 224
DATASET_PATH = "dataset"
MODEL_PATH = "modelo_entrenado.h5"


print("Cargando modelo y clases...")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    class_names = sorted(os.listdir(DATASET_PATH))
    print("Sistema listo. Clases:", class_names)
except Exception as e:
    print(f"Error cargando modelo o dataset: {e}")
    exit()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


cap = None
is_running = False



def iniciar_camara():
    global cap, is_running
    
    if not is_running:
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW) 
        if not cap.isOpened():
            print("No se pudo abrir la cámara 1, intentando con 0...")
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            
        is_running = True
        lbl_estado.config(text="Estado: Cámara Activa", fg="green")
        actualizar_frame()

def detener_camara():
    global cap, is_running
    is_running = False
    if cap:
        cap.release()
    lbl_video.config(image='') # Limpiar la imagen
    lbl_estado.config(text="Estado: Detenido", fg="red")

def actualizar_frame():
    global cap, is_running
    
    if is_running and cap:
        ret, frame = cap.read()
        if ret:
           
            frame = cv2.flip(frame, 1)
            
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
            
            for (x, y, w, h) in faces:
                try:
 
                    face_roi = frame[y:y+h, x:x+w]
                    face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
                    face_resized = cv2.resize(face_rgb, (IMG_SIZE, IMG_SIZE))
                    face_normalized = face_resized / 255.0
                    face_input = np.expand_dims(face_normalized, axis=0)

                    #prediccion
                    preds = model.predict(face_input, verbose=0)
                    class_id = np.argmax(preds)
                    prob = preds[0][class_id]

                    if prob < 0.50:
                        label_text = "Desconocido"
                        color = (0, 0, 255) # Rojo (BGR)
                    else:
                        label_text = f"{class_names[class_id]} {prob*100:.0f}%"
                        color = (0, 255, 0) # Verde (BGR)

                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                except Exception as e:
                    pass # Si falla un cuadro lo ignora

            #convierte para tkinter
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(image=img_pil)

            # etiqueta
            lbl_video.imgtk = img_tk
            lbl_video.configure(image=img_tk)

  
            lbl_video.after(10, actualizar_frame)
        else:
            detener_camara()

#interfaz grafica
root = tk.Tk()
root.title("Sistema de Reconocimiento Facial - Proyecto IA")
root.geometry("1280x720")


tk.Label(root, text="Panel de Control de Reconocimiento", font=("Arial", 20, "bold")).pack(pady=10)

lbl_video = Label(root)
lbl_video.pack()


lbl_estado = tk.Label(root, text="Estado: Esperando...", font=("Arial", 12))
lbl_estado.pack(pady=5)

frame_botones = tk.Frame(root)
frame_botones.pack(pady=20)

btn_iniciar = Button(frame_botones, text=" Iniciar Captura", bg="#4CAF50", fg="white", font=("Arial", 14), command=iniciar_camara)
btn_iniciar.pack(side="left", padx=20)

btn_detener = Button(frame_botones, text=" Detener Captura", bg="#f44336", fg="white", font=("Arial", 14), command=detener_camara)
btn_detener.pack(side="left", padx=20)


root.mainloop()