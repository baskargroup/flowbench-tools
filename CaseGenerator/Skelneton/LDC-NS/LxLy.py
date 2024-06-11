import numpy as np
import os
import random

def calculate_Lx_Ly(points):
    """
    Calculate Lx and Ly of a shape given its boundary points.

    Parameters:
    points (numpy.ndarray): A 2D array of shape (n, 2) where n is the number of points,
                            and each row contains the (x, y) coordinates of a point.

    Returns:
    tuple: (Lx, Ly) where Lx is the maximum x-distance and Ly is the maximum y-distance.
    """
    x_points = points[:, 0]
    y_points = points[:, 1]

    Lx = np.max(x_points) - np.min(x_points)
    Ly = np.max(y_points) - np.min(y_points)

    return Lx, Ly

base_path = './'
output_file = 'LxLy.txt'

# Open the output file in write mode
with open(output_file, 'w') as f:
    # Write the header
    f.write('case,Lx,Ly\n')

    for i in range(1, 101):
        case_folder = f'skelneton_case_{i}'
        case_path = os.path.join(base_path, case_folder)

        if not os.path.isdir(case_path):
            print(f"{case_folder} does not exist")
            continue

        # List all Re_* folders
        re_folders = [d for d in os.listdir(case_path) if os.path.isdir(os.path.join(case_path, d)) and d.startswith('Re_')]

        if not re_folders:
            print(f"No Re_* folders found in {case_folder}")
            continue

        # Randomly select one Re_* folder
        selected_re_folder = random.choice(re_folders)
        re_folder_path = os.path.join(case_path, selected_re_folder)

        # Find any .npz file in the selected Re_* folder
        npz_files = [f for f in os.listdir(re_folder_path) if f.endswith('.npz')]

        if not npz_files:
            print(f"No .npz files found in {re_folder_path}")
            continue

        # Use the first .npz file found
        npz_file_path = os.path.join(re_folder_path, npz_files[0])

        if not npz_file_path:
            print(f"{npz_file_path} does not exist")
            continue

        # Load the .npz file
        data = np.load(npz_file_path)

        # List all keys in the .npz file
        print(f"Keys in the {npz_file_path} file:")
        print(data.files)

        # Assuming the .npz file contains 'x' and 'y' keys for the coordinates
        if 'x' in data.files and 'y' in data.files:
            x_points = data['x']
            y_points = data['y']
            shape_points = np.column_stack((x_points, y_points))
        else:
            print(f"x or y not found in {npz_file_path}")
            continue

        # Calculate Lx and Ly
        Lx, Ly = calculate_Lx_Ly(shape_points)

        print(f"The Lx and Ly of the shape in {npz_file_path} are: {Lx}, {Ly}")

        # Write the result to the file
        f.write(f'{i},{Lx},{Ly}\n')
