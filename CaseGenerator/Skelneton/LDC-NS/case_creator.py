import os
import shutil
from PNGtoMSH import generate_mesh_from_image
from config_generator import write_config_file
import numpy as np
from scipy.stats import qmc
import re

# Define the directory you want to loop through
folder_path = 'skelneton'
# Initialize an empty list to hold the image names
image_names = []
# Loop through the folder
for file_name in os.listdir(folder_path):
    # Check if the file is an image by looking at its extension
    if file_name.lower().endswith(('.png')):
        # Append the image name to the list
        name_without_extension = os.path.splitext(file_name)[0]
        image_names.append(name_without_extension)


# Function to create a sort key
def sort_key(name):
    # Split the name into the first character (letter) and the rest (digits)
    match = re.match(r'([a-zA-Z]+)(\d+)', name)
    if match:
        letter_part = match.group(1)
        number_part = int(match.group(2))
        return (letter_part, number_part)
    else:
        return (name, 0)  # For names without digits, use the name itself with a zero number part

# Sort the image names using the custom sort key
image_names.sort(key=sort_key)

N_shapes = len(image_names)

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
        seed = 3000 + i
        Re_values[i].extend(generate_sobol_numbers(r, seed))

# Sort each sublist individually
for i in range(N_shapes):
    Re_values[i] = sorted(Re_values[i])


for c in range(N_shapes):
    directory1 = f"skelneton_case_{c+1}"
    os.makedirs(directory1, exist_ok=True)
    for Re in Re_values[c]:
        # Define the output file path within the newly created directory
        mesh_name = f"{image_names[c]}.msh"

        mesh_fileDir = f"{directory1}/Re_{Re}/{image_names[c]}.msh"
        config_Dir = f"{directory1}/Re_{Re}/config.txt"
        # Create a directory name based on the Reynolds number
        directory2 = f"{directory1}/Re_{Re}"
        # Create the directory if it does not exist
        os.makedirs(directory2, exist_ok=True)

        generate_mesh_from_image(f"skelneton/{image_names[c]}.png",directory2)

        if (Re <= 100):
            t_final = "[1000, 1010]"
            dt = "[100, 1]"
            OutputSpan = "[10000, 10]"
            baseLevel = 9
            DoReRamping = "false"
            CdStartTimeStep = 0
            lvl_V = "[9, 9]"
        elif (Re > 100 and Re <= 1500):
            t_final = "[1000, 1010]"
            dt = "[10, 1]"
            OutputSpan = "[10000, 10]"
            baseLevel = 9
            DoReRamping = "false"
            CdStartTimeStep = 0
            lvl_V = "[9, 9]"
        else:
            t_final = "[800, 1000, 1100]"
            dt = "[10, 10, 1]"
            OutputSpan = "[10000, 10, 10]"
            DoReRamping = "false"
            RampingRe = Re
            RampingTime = 500
            baseLevel = 10
            CdStartTimeStep = 500
            lvl_V = "[8, 10, 10]"

        write_config_file(Re, dt, t_final, OutputSpan, lvl_V, CdStartTimeStep, baseLevel, DoReRamping, RampingTime, RampingRe, mesh_name, config_Dir)


