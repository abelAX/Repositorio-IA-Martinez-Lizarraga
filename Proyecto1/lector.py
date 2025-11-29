import cv2
import os


nombre_clase = "familiar5"  
path_salida = f"dataset/{nombre_clase}/"
num_fotos = 50       

# crea la carpeta si no existe
if not os.path.exists(path_salida):
    os.makedirs(path_salida)

#detector de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


cap = cv2.VideoCapture(0)
contador = 0

print(f"Guardando fotos en: {path_salida}")
print("Presiona 'q' para salir antes de tiempo.")

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        rostro = frame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (224,224))  # tamaño estándar

        contador += 1
        file_name = path_salida + f"img_{contador}.jpg"
        cv2.imwrite(file_name, rostro)

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, f"Fotos: {contador}/{num_fotos}", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Captura de Fotos", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if contador >= num_fotos:
        break

cap.release()
cv2.destroyAllWindows()

print("✔ Captura completa.")
