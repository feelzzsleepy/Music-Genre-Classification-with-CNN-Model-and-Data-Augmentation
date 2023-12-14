# -*- coding: utf-8 -*-
"""Music Genre Classification using CNN Model with Data Augmentation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Gvkw9t2Lvzf2B6bO4DGhxCir0QW_DpwR

# Genre Classification CNN Model with Data Augmentation
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import sys
import os
import pickle
import librosa
import librosa.display
from IPython.display import Audio
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow import keras
import IPython


# Seed value
seed_value = 1

# 1. Set `PYTHONHASHSEED` environment variable at a fixed value
os.environ['PYTHONHASHSEED'] = str(seed_value)

# 2. Set `python` built-in pseudo-random generator at a fixed value
import random
random.seed(seed_value)

# 3. Set `numpy` pseudo-random generator at a fixed value
np.random.seed(seed_value)

# 4. Set the `tensorflow` pseudo-random generator at a fixed value
tf.random.set_seed(seed_value)

# 5. Configure a new global `tensorflow` session
session_conf = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
sess = tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph(), config=session_conf)
tf.compat.v1.keras.backend.set_session(sess)

# # Dataset path
# path_dataset = "/content/drive/MyDrive/Colab Notebooks/Dataset GTZAN/features_30_sec.csv"
# df = pd.read_csv(path_dataset)

# # Display the first 1000 rows of the DataFrame
# df.head(1000)

# # Display the shape and data types of the DataFrame
# print(df.shape)
# print(df.dtypes)

# # Drop the 'filename' column from the DataFrame
# df = df.drop(labels='filename', axis=1)

# def load_and_augment_audio(file_path, augment=False):
#     audio, sr = librosa.load(file_path)

#     if augment:
#         # Apply data augmentation
#         stretched_audio = librosa.effects.time_stretch(audio, rate=1.2)
#         pitch_shifted_audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=2)
#         noisy_audio = audio + 0.005 * np.random.randn(len(audio))

#         return audio, sr, stretched_audio, pitch_shifted_audio, noisy_audio
#     else:
#         return audio, sr

# # Example audio file path
# audio_recording = "/content/drive/MyDrive/Colab Notebooks/Dataset GTZAN/genres_original/blues/blues.00005.wav"

# # Load and display original audio
# data, sr = load_and_augment_audio(audio_recording, augment=False)
# Audio(data, rate=sr)

# # Load and display augmented audio
# augmented_data, _, _, _, _ = load_and_augment_audio(audio_recording, augment=True)
# Audio(augmented_data, rate=sr)

# # Display waveform plot for original audio
# plt.figure(figsize=(12, 4))
# librosa.display.waveshow(data, color="#2B4F75")
# plt.show()

# # Display waveform plot for augmented audio
# plt.figure(figsize=(12, 4))
# librosa.display.waveshow(augmented_data, color="#FF5733")
# plt.show()

# # Compute Short-Time Fourier Transform (STFT)
# stft = librosa.stft(data)
# stft_db = librosa.amplitude_to_db(abs(stft))

# # Display spectrogram
# plt.figure(figsize=(14, 6))
# librosa.display.specshow(stft_db, sr=sr, x_axis='time', y_axis='hz')
# plt.title("Short-Time Fourier Transform (STFT)")
# plt.colorbar()

# # Compute Chroma features
# chroma = librosa.feature.chroma_stft(y=data, sr=sr)

# # Display Chroma features
# plt.figure(figsize=(16, 6))
# librosa.display.specshow(chroma, sr=sr, x_axis='time', y_axis='chroma', cmap='coolwarm')
# plt.colorbar()
# plt.title("Chroma Features")
# plt.show()

# # Zoom in on a section of the data
# start = 1000
# end = 1200

# # Extract the zoomed-in section
# data_zoom = data[start:end]

# # Calculate the new time axis
# time_zoom = np.linspace(0, (end - start) / sr, len(data_zoom))

# # Plot the zoomed-in section
# plt.figure(figsize=(14, 5))
# plt.plot(time_zoom, data_zoom, color="#2B4F72")
# plt.grid()
# plt.xlabel("Time (s)")
# plt.ylabel("Amplitude")
# plt.title("Zoomed-in Signal Section")
# plt.show()

# # Calculate zero-crossings
# zero_cross_rate = librosa.zero_crossings(data[start:end], pad=False)
# print("The number of zero-crossings is:", sum(zero_cross_rate))

# # Extract class labels and encode them
# class_list = df.iloc[:, -1]
# convertor = LabelEncoder()
# y = convertor.fit_transform(class_list)

# Display DataFrame except the last column
# print(df.iloc[:, :-1])

# Standardize features using StandardScaler
# from sklearn.preprocessing import StandardScaler
# fit = StandardScaler()
# X = fit.fit_transform(np.array(df.iloc[:, :-1], dtype=float))

# """# Test & Training Data"""

# # Split data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
# print("Length of training set:", len(y_train))

# # Adjust test size for a 50/50 split between training and testing
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=seed_value)
# print("Length of training set:", len(y_train))

# # Define a simple neural network model
# model = Sequential([
#     Dense(512, activation='relu', input_shape=(X_train.shape[1],)),
#     Dropout(0.5),
#     Dense(256, activation='relu'),
#     Dropout(0.5),
#     Dense(128, activation='relu'),
#     Dropout(0.5),
#     Dense(64, activation='relu'),
#     Dropout(0.5),
#     Dense(10, activation="softmax"),
# ])

# # Compile the model
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# # Set a flag to enable or disable data augmentation
# augment_data = True  # Set this to True during training

# # Load and augment audio data
# _, _, stretched_audio, pitch_shifted_audio, noisy_audio = load_and_augment_audio(audio_recording, augment=augment_data)

# # Ensure that the number of frames matches the original number of samples
# num_frames = X_train.shape[0]

# # Extract MFCC features for each augmented audio and ensure matching frame count
# mfcc_stretched = librosa.feature.mfcc(y=stretched_audio, sr=sr, n_mfcc=X_train.shape[1]).T[:num_frames]
# mfcc_pitch_shifted = librosa.feature.mfcc(y=pitch_shifted_audio, sr=sr, n_mfcc=X_train.shape[1]).T[:num_frames]
# mfcc_noisy = librosa.feature.mfcc(y=noisy_audio, sr=sr, n_mfcc=X_train.shape[1]).T[:num_frames]

# # Use the augmented data for training
# X_train_augmented = np.vstack([X_train, mfcc_stretched, mfcc_pitch_shifted, mfcc_noisy])
# y_train_augmented = np.concatenate([y_train] * 4)  # Assuming each augmentation creates 4 new samples

# # Train the model
# history_augmented = model.fit(X_train_augmented, y_train_augmented, validation_data=(X_test, y_test), epochs=100, batch_size=128, verbose=2)

# """# Creating a Model"""

# model.save("musicgenreclassification.h5")

# """# Original Model Accuracy"""

# # Evaluate the model on the test set
# test_loss, test_acc = model.evaluate(X_test, y_test, batch_size=128)
# print("Test Loss:", test_loss)
# print("Test Accuracy:", test_acc*100)

# # Plot model accuracy
# plt.plot(history.history['accuracy'])
# plt.plot(history.history['val_accuracy'])
# plt.title('Model Accuracy')
# plt.ylabel('Accuracy')
# plt.xlabel('Epoch')
# plt.legend(['Train', 'Validation'], loc='upper left')
# plt.show()

# """# Augmented Model Accuracy"""

# # Evaluate the model on the augmented test set
# test_loss_augmented, test_acc_augmented = model.evaluate(X_test, y_test, batch_size=128)
# print("The test Loss with Augmentation is:", test_loss_augmented)
# print("The Best Accuracy with Augmentation is:", test_acc_augmented * 100)

# # Visualize the training history with augmentation
# plt.plot(history_augmented.history['accuracy'])
# plt.plot(history_augmented.history['val_accuracy'])
# plt.title('Augmented CNN Model Accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['train', 'val'], loc='upper left')
# plt.show()

# """# GUI for Genre Classification"""

from tensorflow.keras.models import load_model

# Load your trained model
# model = load_model('musicgenreclassification.h5')  # Replace with the actual model file

model = load_model('musicgenreclassification.h5', custom_objects={'<custom_layer>': <CustomLayerClass>}, compile=False)

# Function to preprocess audio and make predictions

def classify_genre(audio_path):
    # Load and preprocess the audio file
    data, sr = librosa.load(audio_path, sr=None)  # Load with original sample rate
    mfcc = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=X_train.shape[1]).T
    
    # Make predictions using your model
    prediction = model.predict(np.expand_dims(mfcc, axis=0))

    # Map predictions to genre names (adjust as needed)
    genre_mapping = {0: 'Blues', 1: 'Jazz', 2: 'Rock', 3: 'Pop', 4: 'Hip-Hop'}
    predicted_genre = genre_mapping[np.argmax(prediction)]

    return predicted_genre

# Streamlit app
def main():
    st.title("Music Genre Classifier")

    # File uploader
    uploaded_file = st.file_uploader("Choose an audio file", type=["wav"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav", start_time=0)

        # Perform genre classification
        predicted_genre = classify_genre(uploaded_file)
        st.write(f"Predicted Genre: {predicted_genre}")

# Run the app
if __name__ == "__main__":
    main()
