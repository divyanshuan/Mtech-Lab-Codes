import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
from skimage.feature import local_binary_pattern


def compute_texture_features(image, radius=3, n_points=24):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate Local Binary Pattern (LBP)
    lbp = local_binary_pattern(gray_image, n_points, radius, method="uniform")

    # Compute histogram of LBP and normalize
    hist, _ = np.histogram(
        lbp.ravel(), bins=np.arange(0, n_points + 3), range=(0, n_points + 2)
    )
    hist = hist.astype("float32")
    hist /= hist.sum() + 1e-6  # Normalize to avoid division by zero
    return hist


def retrieve_images_texture(query_image_path, image_folder):
    # Read the query image
    query_image = cv2.imread(query_image_path)

    if query_image is None:
        print(f"Error: Could not load query image from {query_image_path}")
        return []

    # Compute LBP histogram for the query image
    query_texture = compute_texture_features(query_image)

    results = []

    # Iterate through each image in the dataset folder
    for image_name in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_name)

        # Skip non-image files like .DS_Store
        if not image_name.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
            continue

        image = cv2.imread(image_path)

        if image is None:
            print(f"Error: Could not load image from {image_path}")
            continue

        # Compute LBP histogram for the dataset image
        texture = compute_texture_features(image)

        # Compute similarity using Chi-square distance
        similarity = cv2.compareHist(query_texture, texture, cv2.HISTCMP_CHISQR)

        # Append result as a tuple of image name and similarity score
        results.append((image_name, similarity))

    # Sort results by similarity score (lower is better)
    results.sort(key=lambda x: x[1])
    return results


if __name__ == "__main__":
    image_folder = "Images/DatasetImages"  # Path to dataset
    query_image_path = "Images/QueryImages/train_0329.jpg"  # Path to the query image

    # Check if the dataset folder exists
    if not os.path.exists(image_folder):
        print(f"Error: Dataset folder '{image_folder}' does not exist.")
    elif not os.path.exists(query_image_path):
        print(f"Error: Query image '{query_image_path}' does not exist.")
    else:
        # Retrieve similar images based on texture
        results = retrieve_images_texture(query_image_path, image_folder)

        # Display top 5 results
        if results:
            for i, (image_name, score) in enumerate(results[:5]):
                image_path = os.path.join(image_folder, image_name)
                image = cv2.imread(image_path)
                plt.subplot(1, 5, i + 1)
                plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                plt.title(f"Score: {score:.2f}")
                plt.axis("off")
            plt.show()
        else:
            print("No similar images found.")
