import os
import shutil
from mesh_gen2 import generate_mesh
from mesh_gen4 import generate_ellipse_mesh
from config_generator import write_config_file
import numpy as np
from scipy.stats import qmc

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

ab_ratio = [0.143, 0.167, 0.2, 0.25, 0.33, 0.5, 0.95, 1.0, 1.05, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
N_arbitrary = 85

ri_ranges = [(0.1, 1), (1, 10)]
re_ranges = [(10, 100), (100, 1000)]

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

# Use a fixed seed for reproducibility
seed = 42
num_cases = N_arbitrary + len(ab_ratio)
num_folders_per_case = 10

ri_re_gr_cases = generate_cases(num_cases, num_folders_per_case, seed)

def format_ri(ri):
    return str(ri).replace('.', 'p')

# For each arbitrary case
for c in range(1, N_arbitrary + 1):
    directory1 = f"case_{c}"
    os.makedirs(directory1, exist_ok=True)
    for i, (Ri, Re, Gr) in enumerate(ri_re_gr_cases[c-1]):
        folder_name = f"Ri_{format_ri(Ri)}_Re_{Re}"
        mesh_name = f"case_{c}.msh"
        mesh_fileDir = f"{directory1}/{folder_name}/case_{c}.msh"
        config_Dir = f"{directory1}/{folder_name}/config.txt"
        directory2 = f"{directory1}/{folder_name}"
        os.makedirs(directory2, exist_ok=True)
        generate_mesh(10, mesh_fileDir, 1.0, 1.0, c)
        write_config_file(Gr, Re, mesh_name, config_Dir)

# For each ab_ratio case
for c in range(len(ab_ratio)):
    directory1 = f"case_{N_arbitrary + 1 + c}"
    os.makedirs(directory1, exist_ok=True)
    for i, (Ri, Re, Gr) in enumerate(ri_re_gr_cases[N_arbitrary + c]):
        folder_name = f"Ri_{format_ri(Ri)}_Re_{Re}"
        mesh_name = f"case_{N_arbitrary + 1 + c}.msh"
        mesh_fileDir = f"{directory1}/{folder_name}/case_{N_arbitrary + 1 + c}.msh"
        config_Dir = f"{directory1}/{folder_name}/config.txt"
        directory2 = f"{directory1}/{folder_name}"
        os.makedirs(directory2, exist_ok=True)
        generate_ellipse_mesh(ab_ratio[c], mesh_fileDir, 1.0, 1.0)
        write_config_file(Gr, Re, mesh_name, config_Dir)
