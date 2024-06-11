import os
import shutil
from mesh_gen2 import generate_mesh
from mesh_gen4 import generate_ellipse_mesh
from config_generator import write_config_file
import numpy as np
from scipy.stats import qmc


def copy_directory(source_dir, destination_dir):
    # Ensure the source directory exists
    if not os.path.exists(source_dir):
        print("Source directory does not exist.")
        return

    # Create the destination directory if it does not exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Walk through the source directory
    for dirpath, dirnames, filenames in os.walk(source_dir):
        # Construct the path in the destination directory
        dest_path = dirpath.replace(source_dir, destination_dir, 1)

        # If this path does not exist in the destination directory, create it
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        # For each file in the current directory, copy it to the destination directory
        for file in filenames:
            src_file = os.path.join(dirpath, file)
            dest_file = os.path.join(dest_path, file)
            shutil.copy2(src_file, dest_file)  # copy2 preserves metadata


# Gr_values = [1, 5, 10, 50, 100, 200, 500, 1000, 1500, 2000, 2500, 3000, 5000, 8000, 10000]
ab_ratio = [0.143, 0.167, 0.2, 0.25, 0.33, 0.5, 0.95, 1.0, 1.05, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]

N_arbitrary = 85

# Define the ranges for random number generation
ranges = [(1000, 10000), (10000, 100000)]

# Function to generate 5 random numbers within a given range using Sobol sequence
def generate_sobol_numbers(rng, seed, n=5):
    sampler = qmc.Sobol(d=1, scramble=True, seed=seed)
    lower, upper = rng
    samples = qmc.scale(sampler.random(n), lower, upper).flatten()
    return np.round(samples).astype(int)

# Generate random numbers for each range and sort them
Gr_values = [[] for _ in range(N_arbitrary + len(ab_ratio))]
for i in range(N_arbitrary + len(ab_ratio)):
    for r in ranges:
        seed = 300 + i
        Gr_values[i].extend(generate_sobol_numbers(r, seed))

# Sort each sublist individually
for i in range(N_arbitrary + len(ab_ratio)):
    Gr_values[i] = sorted(Gr_values[i])


for c in range(1, N_arbitrary + 1):
    directory1 = f"case_{c}"
    os.makedirs(directory1, exist_ok=True)
        # Run the generate_mesh function
        # generate_mesh(10, mesh_fileDir, 1.0, 1.0)
    for Gr in Gr_values[c]:
        # Define the output file path within the newly created directory
        mesh_name = f"case_{c}.msh"

        mesh_fileDir = f"{directory1}/Gr_{Gr}/case_{c}.msh"
        config_Dir = f"{directory1}/Gr_{Gr}/config.txt"
        # Create a directory name based on the Reynolds number
        directory2 = f"{directory1}/Gr_{Gr}"
        # Create the directory if it does not exist
        os.makedirs(directory2, exist_ok=True)
        generate_mesh(10, mesh_fileDir, 1.0, 1.0, c)

        write_config_file(Gr,mesh_name, config_Dir)

for c in range(len(ab_ratio)):
    directory1 = f"case_{N_arbitrary + 1 + c}"
    os.makedirs(directory1, exist_ok=True)
        # generate_ellipse_mesh(ab_ratio[c], mesh_fileDir, 1.0, 1.0)
    for Gr in Gr_values[N_arbitrary + c]:
        mesh_name = f"case_{N_arbitrary + 1 + c}.msh"

        # Define the output file path within the newly created directory
        mesh_fileDir = f"{directory1}/Gr_{Gr}/case_{N_arbitrary + 1 + c}.msh"
        config_Dir = f"{directory1}/Gr_{Gr}/config.txt"
        # Create a directory name based on the Reynolds number
        directory2 = f"{directory1}/Gr_{Gr}"
        # Create the directory if it does not exist
        os.makedirs(directory2, exist_ok=True)
        generate_ellipse_mesh(ab_ratio[c], mesh_fileDir, 1.0, 1.0)
        write_config_file(Gr, mesh_name, config_Dir)
