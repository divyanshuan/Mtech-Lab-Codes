import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity as ssim


def compute_edge_features(image):
    if image is None:
        print("Error: Image is None. Skipping this image.")
        return None
    image = cv2.resize(image, (192, 128))
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 100, 200)
    return edges


def retrieve_images_shape(query_image_path, image_folder):
    query_image = cv2.imread(query_image_path)

    # Debugging: Check if the query image is loaded
    if query_image is None:
        print(f"Error: Could not load query image from {query_image_path}")
        return []

    query_edges = compute_edge_features(query_image)
    if query_edges is None:
        return []

    results = []

    # Iterate over images in the dataset folder
    for image_name in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_name)
        print(f"Processing image: {image_path}")  # Debugging: Print the image path

        image = cv2.imread(image_path)

        # Debugging: Check if the dataset image is loaded
        if image is None:
            print(f"Error: Could not load image from {image_path}. Skipping.")
            continue

        edges = compute_edge_features(image)

        if edges is None:
            continue

        # Compute similarity using Structural Similarity Index (SSIM)
        similarity, _ = ssim(query_edges, edges, full=True)
        results.append((image_name, similarity))

    # Sort results based on similarity score (higher is better for SSIM)
    results.sort(key=lambda x: x[1], reverse=True)
    return results


if __name__ == "__main__":
    image_folder = "Images/DatasetImages"  # Path to your dataset
    query_image_path = "Images/QueryImages/train_0322.jpg"  # Path to the query image

    # Ensure the dataset folder exists
    if not os.path.exists(image_folder):
        print(f"Error: The folder '{image_folder}' does not exist.")
    elif not os.path.exists(query_image_path):
        print(f"Error: The target image '{query_image_path}' does not exist.")
    else:
        results = retrieve_images_shape(query_image_path, image_folder)

        # Display top 5 results
        if results:
            for i, (image_name, score) in enumerate(results[:5]):
                image_path = os.path.join(image_folder, image_name)
                image = cv2.imread(image_path)
                plt.subplot(1, 5, i + 1)
                plt.tight_layout()
                plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                plt.title(f"Score: {score:.2f}")
                plt.axis("off")
            plt.show()
        else:
            print("No similar images found.")
