import cv2
import numpy as np
import os
from matplotlib import pyplot as plt


def calculate_histogram(image, bins=(8, 8, 8)):
    # Check if the image is valid
    if image is None:
        print("Error: Image is None.")
        return None
    # Convert image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Calculate histogram and normalize
    histogram = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])
    cv2.normalize(histogram, histogram)
    return histogram.flatten()


def find_similar_images(target_image_path, dataset_folder):
    print(f"Loading target image from: {target_image_path}")
    target_image = cv2.imread(target_image_path)

    if target_image is None:
        print(f"Error: Could not load target image from {target_image_path}")
        return []

    target_hist = calculate_histogram(target_image)
    if target_hist is None:
        return []

    matches = []

    # Iterate over images in the dataset folder
    for file_name in os.listdir(dataset_folder):
        image_path = os.path.join(dataset_folder, file_name)
        print(f"Processing image: {image_path}")

        # Read the image
        image = cv2.imread(image_path)

        if image is None:
            print(f"Error: Could not load image from {image_path}")
            continue

        hist = calculate_histogram(image)

        if hist is None:
            continue

        # Compute similarity using correlation
        similarity_score = cv2.compareHist(target_hist, hist, cv2.HISTCMP_CORREL)
        matches.append((file_name, similarity_score))

    # Sort matches by similarity score
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches


if __name__ == "__main__":
    # Updated paths
    dataset_folder = "Images/DatasetImages"  # Directory containing the dataset
    target_image_path = "Images/QueryImages/train_0001.jpg"  # Path to the query image

    # Ensure the dataset folder exists
    if not os.path.exists(dataset_folder):
        print(f"Error: The folder '{dataset_folder}' does not exist.")
    elif not os.path.exists(target_image_path):
        print(f"Error: The target image '{target_image_path}' does not exist.")
    else:
        similar_images = find_similar_images(target_image_path, dataset_folder)

        # Display top 5 similar images
        if similar_images:
            for i, (file_name, score) in enumerate(similar_images[:5]):
                image = cv2.imread(os.path.join(dataset_folder, file_name))
                plt.subplot(1, 5, i + 1)
                plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                plt.title(f"Score: {score:.2f}")
                plt.axis("off")
            plt.show()
        else:
            print("No similar images found.")
