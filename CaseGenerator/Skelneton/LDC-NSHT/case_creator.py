import os
import shutil
from PNGtoMSH import generate_mesh_from_image
from config_generator import write_config_file
import numpy as np
from scipy.stats import qmc
import re

def copy_directory(source_dir, destination_dir):
    if not os.path.exists(source_dir):
        print("Source directory does not exist.")
        return

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for dirpath, dirnames, filenames in os.walk(source_dir):
        dest_path = dirpath.replace(source_dir, destination_dir, 1)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        for file in filenames:
            src_file = os.path.join(dirpath, file)
            dest_file = os.path.join(dest_path, file)
            shutil.copy2(src_file, dest_file)

ri_ranges = [(0.1, 1), (1, 10)]
re_ranges = [(10, 100), (100, 1000)]
N_shapes = 100

def generate_sobol_numbers(rng, seed, n):
    sampler = qmc.Sobol(d=1, scramble=True, seed=seed)
    lower, upper = rng
    samples = qmc.scale(sampler.random(n), lower, upper).flatten()
    return samples

def generate_values(n_cases, n_per_range, seed):
    # Generate Sobol sequences for each range
    ri_01_1 = generate_sobol_numbers(ri_ranges[0], seed, n_cases * n_per_range)
    ri_1_10 = generate_sobol_numbers(ri_ranges[1], seed + 1, n_cases * n_per_range)
    re_10_100 = generate_sobol_numbers(re_ranges[0], seed + 2, n_cases * n_per_range)
    re_100_1000 = generate_sobol_numbers(re_ranges[1], seed + 3, n_cases * n_per_range)

    # Round values appropriately
    ri_01_1 = np.round(ri_01_1, 3)
    ri_1_10 = np.round(ri_1_10, 3)
    re_10_100 = np.round(re_10_100).astype(int)
    re_100_1000 = np.round(re_100_1000).astype(int)

    return ri_01_1, ri_1_10, re_10_100, re_100_1000

def generate_cases(n_cases, n_folders_per_case, seed):
    n_per_range = n_folders_per_case // 2  # 5 values per range
    ri_01_1, ri_1_10, re_10_100, re_100_1000 = generate_values(n_cases, n_per_range, seed)

    cases = []
    for i in range(n_cases):
        ri_case_values = np.concatenate([ri_01_1[i * n_per_range:(i + 1) * n_per_range], ri_1_10[i * n_per_range:(i + 1) * n_per_range]])
        re_case_values = np.concatenate([re_10_100[i * n_per_range:(i + 1) * n_per_range], re_100_1000[i * n_per_range:(i + 1) * n_per_range]])

        # Ensure the same seed is used to shuffle in the same way every time
        np.random.seed(seed + i)
        np.random.shuffle(ri_case_values)
        np.random.shuffle(re_case_values)

        case_tuples = [(ri, re, round(ri * re**2, 3)) for ri, re in zip(ri_case_values, re_case_values)]
        cases.append(case_tuples)

    return cases

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

# Use a fixed seed for reproducibility
seed = 70
num_cases = 100
num_folders_per_case = 10

ri_re_gr_cases = generate_cases(num_cases, num_folders_per_case, seed)

def format_ri(ri):
    return str(ri).replace('.', 'p')

# For each arbitrary case
for c in range(N_shapes):
    directory1 = f"case_{c+1}"
    os.makedirs(directory1, exist_ok=True)
    mesh_name = f"{image_names[c]}.msh"
    for i, (Ri, Re, Gr) in enumerate(ri_re_gr_cases[c]):
        folder_name = f"Ri_{format_ri(Ri)}_Re_{Re}"
        mesh_fileDir = f"{directory1}/{folder_name}/{image_names[c]}.msh"
        config_Dir = f"{directory1}/{folder_name}/config.txt"
        directory2 = f"{directory1}/{folder_name}"
        os.makedirs(directory2, exist_ok=True)
        generate_mesh_from_image(f"skelneton/{image_names[c]}.png",directory2)
        write_config_file(Gr, Re, mesh_name, config_Dir)
