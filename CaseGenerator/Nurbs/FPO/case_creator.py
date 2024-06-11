import os
import shutil
from NURBStoMSH import NURBStoMSH
from config_generator import write_config_file
import numpy as np
from scipy.stats import qmc

N_shapes = 100 

Re_V = ""

# Define the ranges for random number generation
ranges = [(100, 1000)]

# Function to generate 5 random numbers within a given range using Sobol sequence
def generate_sobol_numbers(rng, seed, n=5):
    sampler = qmc.Sobol(d=1, scramble=True, seed=seed)
    lower, upper = rng
    samples = qmc.scale(sampler.random(n), lower, upper).flatten()
    return np.round(samples).astype(int)

# Generate random numbers for each range and sort them
Re_values = [[] for _ in range(N_shapes)]
for i in range(N_shapes):
    for r in ranges:
        seed = 10000 + i
        Re_values[i].extend(generate_sobol_numbers(r, seed))

# Sort each sublist individually
for i in range(N_shapes):
    Re_values[i] = sorted(Re_values[i])


for c in range(N_shapes):
    directory1 = f"nurbs_case_{c+1}"
    os.makedirs(directory1, exist_ok=True)
    for Re in Re_values[c]:
        # Define the output file path within the newly created directory
        mesh_name = f"case_{c+1}.msh"

        mesh_fileDir = f"{directory1}/Re_{Re}/case_{c+1}.msh"
        config_Dir = f"{directory1}/Re_{Re}/config.txt"
        # Create a directory name based on the Reynolds number
        directory2 = f"{directory1}/Re_{Re}"
        # Create the directory if it does not exist
        os.makedirs(directory2, exist_ok=True)
        coreset_path = f"./coreset_curve.npy"
        NURBStoMSH(coreset_path, directory2, c+1)

        if (Re <= 800):
            Re_V = f"[10, 100, {Re}, {Re},{Re},{Re},{Re},{Re},{Re}]"
        else:
             Re_V = f"[10, 100, 800, {Re},{Re},{Re},{Re},{Re},{Re}]"

        write_config_file(Re, Re_V, mesh_name, config_Dir)