import tensorflow as tf

# Load the model
model = tf.keras.models.load_model('sleep_apnea_detection_model.h5')

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])