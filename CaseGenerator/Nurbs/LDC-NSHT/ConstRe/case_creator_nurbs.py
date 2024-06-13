import os
import shutil
from NURBStoMSH import NURBStoMSH
from config_generator import write_config_file
import numpy as np
from scipy.stats import qmc

N_shapes = 100

dt = ""
t_final = ""
OutputSpan = ""
lvl_V = ""
DoReRamping = "false"
RampingTime = 0
RampingRe = 0
baseLevel = 8
CdStartTimeStep = 0

# Define the ranges for random number generation
ranges = [(1000, 10000), (10000, 100000)]

# Function to generate 5 random numbers within a given range using Sobol sequence
def generate_sobol_numbers(rng, seed, n=5):
    sampler = qmc.Sobol(d=1, scramble=True, seed=seed)
    lower, upper = rng
    samples = qmc.scale(sampler.random(n), lower, upper).flatten()
    return np.round(samples).astype(int)

# Generate random numbers for each range and sort them
Gr_values = [[] for _ in range(N_shapes)]
for i in range(N_shapes):
    for r in ranges:
        seed = 30000 + i
        Gr_values[i].extend(generate_sobol_numbers(r, seed))

# Sort each sublist individually
for i in range(N_shapes):
    Gr_values[i] = sorted(Gr_values[i])


for c in range(N_shapes):
    directory1 = f"nurbs_case_{c+1}"
    os.makedirs(directory1, exist_ok=True)
    for Gr in Gr_values[c]:
        # Define the output file path within the newly created directory
        mesh_name = f"case_{c+1}.msh"

        mesh_fileDir = f"{directory1}/Gr_{Gr}/case_{c+1}.msh"
        config_Dir = f"{directory1}/Gr_{Gr}/config.txt"
        # Create a directory name based on the Reynolds number
        directory2 = f"{directory1}/Gr_{Gr}"
        # Create the directory if it does not exist
        os.makedirs(directory2, exist_ok=True)
        coreset_path = f"./coreset_curve.npy"
        NURBStoMSH(coreset_path, directory2, c+1)

        write_config_file(Gr, mesh_name, config_Dir)
