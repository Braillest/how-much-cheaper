import re
import pickle
import csv
import pandas
import matplotlib.pyplot as plt
from PIL import Image
import os
import time
import math

braillest_results_csv_path = "/braillest/data/braillest-results.csv"
classical_results_csv_path = "/braillest/data/classical-results.csv"
figures_path = "/braillest/data/figures/"
gif_path = "/braillest/data/output.gif"

braillest_results = []
classical_results = []

# Populate results

for books in range(1, 50):
    for pages in range(1, 50):

        binders = math.ceil(pages / 100)

        braillest = {
            "x" : books,
            "y" : pages,
            "z" : min(
                1.029 * ((1.5 * pages) + (0.04 * pages * books) + (3 * binders * books)) + 0.30,
                (1.5 * pages) + (0.04 * pages * books) + (3 * binders * books) + 5
            )
        }

        classical = {
            "x" : books,
            "y" : pages,
            "z" : (0.75 * pages * books) + (3 * binders * books)
        }

        braillest_results.append(braillest)
        classical_results.append(classical)

# Save results to csv files

with open(braillest_results_csv_path, "w") as file:

    writer = csv.DictWriter(file, fieldnames=["x", "y", "z"])
    writer.writeheader()
    writer.writerows(braillest_results)

with open(classical_results_csv_path, "w") as file:

    writer = csv.DictWriter(file, fieldnames=["x", "y", "z"])
    writer.writeheader()
    writer.writerows(classical_results)

# Load in values into dataframe

braillest_df = pandas.DataFrame(braillest_results)
classical_df = pandas.DataFrame(classical_results)

# Plot results

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=0, azim=-90)
ax.grid(True)

# ax.scatter(braillest_df["x"], braillest_df["y"], braillest_df["z"], c="green", marker="o", label="Braillest", alpha=.5)
# ax.scatter(classical_df["x"], classical_df["y"], classical_df["z"], c="black", marker=".", label="Classical", alpha=.5)

ax.scatter(classical_df["x"], classical_df["y"], classical_df["z"] - braillest_df["z"], c=(classical_df["z"] - braillest_df["z"] > 0).map({True: "green", False: "red"}), marker=".", alpha=1)

ax.set_xlabel("Copies")
ax.set_ylabel("Pages")
ax.set_zlabel("Price difference (USD)")

# ax.legend()

# Create a series of photos across a rotational sweep

for azim in range(-94, -176, -1):
        ax.view_init(elev=0, azim=azim)
        plt.savefig(figures_path + str(time.time()) + ".png")

for azim in range(-176, -94, 1):
    ax.view_init(elev=0, azim=azim)
    plt.savefig(figures_path + str(time.time()) + ".png")

try:
    # Get a sorted list of image file paths
    image_files = sorted(
        [
            os.path.join(figures_path, file)
            for file in os.listdir(figures_path)
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
        ]
    )

    if not image_files:
        print("No image files found in the directory.")

    # Open the images
    images = [Image.open(image_file) for image_file in image_files]

    # Create the GIF
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=10,  # Duration in milliseconds per frame
        loop=0  # Loop forever
    )

    print(f"GIF successfully created and saved to {gif_path}")
except Exception as e:
    print(f"An error occurred: {e}")
