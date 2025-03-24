import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import os
import cv2

# Define the dataset path (update with your local path)
dataset_path = "Images/DatasetImages"

# Image dimensions (adjust as needed)
IMG_HEIGHT, IMG_WIDTH = 64, 64


# Step 1: Load and preprocess the dataset
def load_images_from_folder(folder, img_height, img_width):
    images = []
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        img = cv2.imread(file_path)
        if img is not None:
            # Resize and normalize the image
            img = cv2.resize(img, (img_width, img_height))
            img = img.astype("float32") / 255.0
            images.append(img)
    return np.array(images)


# Load the dataset
x_data = load_images_from_folder(dataset_path, IMG_HEIGHT, IMG_WIDTH)

# Split into training and test sets
split_index = int(0.8 * len(x_data))
x_train = x_data[:split_index]
x_test = x_data[split_index:]


# Step 2: Define the Autoencoder model
def build_autoencoder(input_shape):
    encoder_input = layers.Input(shape=input_shape)

    # Encoder
    x = layers.Conv2D(32, (3, 3), activation="relu", padding="same")(encoder_input)
    x = layers.MaxPooling2D((2, 2), padding="same")(x)
    x = layers.Conv2D(64, (3, 3), activation="relu", padding="same")(x)
    x = layers.MaxPooling2D((2, 2), padding="same")(x)
    x = layers.Conv2D(128, (3, 3), activation="relu", padding="same")(x)
    encoded = layers.MaxPooling2D((2, 2), padding="same")(x)

    # Decoder
    x = layers.Conv2D(128, (3, 3), activation="relu", padding="same")(encoded)
    x = layers.UpSampling2D((2, 2))(x)
    x = layers.Conv2D(64, (3, 3), activation="relu", padding="same")(x)
    x = layers.UpSampling2D((2, 2))(x)
    x = layers.Conv2D(32, (3, 3), activation="relu", padding="same")(x)
    x = layers.UpSampling2D((2, 2))(x)
    decoded = layers.Conv2D(3, (3, 3), activation="sigmoid", padding="same")(x)

    # Autoencoder model
    autoencoder = models.Model(encoder_input, decoded)
    # Encoder model (for feature extraction)
    encoder = models.Model(encoder_input, encoded)

    autoencoder.compile(optimizer="adam", loss="binary_crossentropy")
    return autoencoder, encoder


# Create the autoencoder and encoder models
input_shape = (IMG_HEIGHT, IMG_WIDTH, 3)
autoencoder, encoder = build_autoencoder(input_shape)

# Step 3: Train the autoencoder
autoencoder.fit(
    x_train,
    x_train,
    epochs=20,
    batch_size=64,
    shuffle=True,
    validation_data=(x_test, x_test),
)


# Step 4: Extract features using the trained encoder
def extract_features(encoder, images):
    return encoder.predict(images).reshape(len(images), -1)


# Extract features for the training set
features = extract_features(encoder, x_train)

# Standardize the features
scaler = StandardScaler()
features = scaler.fit_transform(features)

# Step 5: Fit a Nearest Neighbors model for retrieval
nn_model = NearestNeighbors(n_neighbors=5, metric="euclidean")
nn_model.fit(features)


# Step 6: Define a function to retrieve similar images
def retrieve_similar_images(query_image, x_train, encoder, nn_model, scaler):
    # Extract features from the query image
    query_features = extract_features(encoder, np.expand_dims(query_image, axis=0))
    query_features = scaler.transform(query_features)

    # Find similar images
    distances, indices = nn_model.kneighbors(query_features)
    similar_images = x_train[indices.flatten()]

    # Display the query image and the retrieved images
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 6, 1)
    plt.imshow(query_image)
    plt.title("Query Image")
    plt.axis("off")

    for i, img in enumerate(similar_images):
        plt.subplot(1, 6, i + 2)
        plt.imshow(img)
        plt.title(f"Match {i + 1}")
        plt.axis("off")

    plt.show()


# Step 7: Test the retrieval with a random query image
query_idx = np.random.randint(len(x_test))
query_image = x_test[query_idx]
retrieve_similar_images(query_image, x_train, encoder, nn_model, scaler)
