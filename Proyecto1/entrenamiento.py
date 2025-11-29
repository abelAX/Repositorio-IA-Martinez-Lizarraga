import os
import tensorflow as tf
import pandas as pd

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# --- Configuración ---
DATASET_PATH = "dataset"
IMG_SIZE = 224
BATCH_SIZE = 32

# Contar clases automáticamente
clases = sorted(os.listdir(DATASET_PATH))
num_clases = len(clases)
print(f"Clases detectadas ({num_clases}): {clases}")

# --- Data Augmentation ---
train_datagen = ImageDataGenerator(
    rescale=1/255,
    validation_split=0.2,
    rotation_range=25,
    zoom_range=0.25,
    horizontal_flip=True,
    width_shift_range=0.15,
    height_shift_range=0.15,
    shear_range=0.15,
)

val_datagen = ImageDataGenerator(
    rescale=1/255,
    validation_split=0.2
)

train_gen = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_gen = val_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# --- Modelo base ---
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.4)(x)
preds = Dense(num_clases, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=preds)

# Compilación inicial
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("Entrenando primera etapa (solo capas superiores)...")

# se guarda este historial
history1 = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=20,
    callbacks=[EarlyStopping(monitor='val_accuracy', patience=3, restore_best_weights=True)]
)

# Segunda etapa
print("\nActivando fine-tuning...")

for layer in base_model.layers[-30:]:
    layer.trainable = True

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.00005),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

early_stop = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2)

print("Entrenando segunda etapa (fine-tuning)...")

#se guarda este historial
history2 = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=20,
    callbacks=[early_stop, reduce_lr]
)

# Combinar historiales
full_history = {}

for key in history1.history.keys():
    full_history[key] = history1.history[key] + history2.history[key]

# Convertir a DataFrame
hist_df = pd.DataFrame(full_history)

print("\n===== TABLA DE ENTRENAMIENTO =====\n")
print(hist_df)

# Guardar tabla
hist_df.to_csv("historial_entrenamiento.csv", index=False)
print("\nHistorial guardado como historial_entrenamiento.csv")

# Guardar modelo
model.save("modelo_entrenado.h5")
print("\n Modelo mejorado guardado como modelo_entrenado.h5")
