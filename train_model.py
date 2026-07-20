import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Flatten, Dense, Dropout
dataset_path = "dataset"
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    validation_split=0.2
)
train_data = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical",
    subset="training"
)
print(train_data.class_indices)
exit()
validation_data = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical",
    subset="validation"
)
model = Sequential([
    
    Conv2D(32, (3,3), activation="relu", input_shape=(224,224,3)),
    MaxPooling2D(pool_size=(2,2)),
    
    Conv2D(64, (3,3), activation="relu"),
    MaxPooling2D(pool_size=(2,2)),
    
    Conv2D(128, (3,3), activation="relu"),
    MaxPooling2D(pool_size=(2,2)),
    
    Flatten(),
    
    Dense(512, activation="relu"),
    Dropout(0.5),
    
    Dense(train_data.num_classes, activation="softmax")
])
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
model.summary()
history = model.fit(
    train_data,
    validation_data=validation_data,
    epochs=1
)
model.save("model.h5")
print("\nModel trained successfully!")
model.save("models/plant_disease_model.keras")