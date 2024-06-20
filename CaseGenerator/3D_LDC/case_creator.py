import os
import shutil
import glob
from config_generator import write_config_file
import numpy as np
from scipy.stats import qmc
import re



stl_files = glob.glob('shapes/*.stl')

# Function to create a sort key
def sort_key(name):
    base_name = os.path.basename(name)
    # Split the name into the first character (letter) and the rest (digits)
    match = re.match(r'([a-zA-Z_]+)(\d+)', base_name)
    if match:
        letter_part = match.group(1)
        number_part = int(match.group(2))
        return (letter_part, number_part)
    else:
        return (base_name, 0)  # For names without digits, use the name itself with a zero number part

# Sort the image names using the custom sort key
stl_files.sort(key=sort_key)
N_shapes = len(stl_files)


dt = ""
t_final = ""
OutputSpan = ""
lvl_V = ""
DoReRamping = "false"
RampingTime = 0
RampingRe = 0
baseLevel = 7
CdStartTimeStep = 0

# Define the ranges for random number generation
ranges = [(10, 100), (100, 1000)]

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
        seed = 55 + i
        Re_values[i].extend(generate_sobol_numbers(r, seed))

# Sort each sublist individually
for i in range(N_shapes):
    Re_values[i] = sorted(Re_values[i])


for c, stl_file in enumerate(stl_files):
    base_name = os.path.basename(stl_file).replace('.stl', '')
    directory1 = f"case_{c+1}"
    os.makedirs(directory1, exist_ok=True)
    for Re in Re_values[c]:
        directory2 = f"{directory1}/Re_{Re}"
        os.makedirs(directory2, exist_ok=True)
        mesh_name = f"{base_name}.stl"
        config_Dir = f"{directory2}/config.txt"
        # Copy the STL file to the directory
        shutil.copy(stl_file, os.path.join(directory2, mesh_name))

        if (Re <= 500):
            t_final = "[500, 510]"
            dt = "[5, 1]"
            OutputSpan = "[10000, 10]"
            baseLevel = 7
            DoReRamping = "false"
            CdStartTimeStep = 0
            lvl_V = "[7, 7]"
        else:
            t_final = "[500, 510]"
            dt = "[5, 1]"
            OutputSpan = "[10000, 10]"
            baseLevel = 7
            DoReRamping = "false"
            CdStartTimeStep = 0
            lvl_V = "[7, 7]"


        write_config_file(Re, dt, t_final, OutputSpan, lvl_V, CdStartTimeStep, baseLevel, DoReRamping, RampingTime, RampingRe, mesh_name, config_Dir)


