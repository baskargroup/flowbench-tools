import numpy as np
import os
import random

def calculate_perimeter(points):
    """
    Calculate the perimeter of a shape given its boundary points.

    Parameters:
    points (numpy.ndarray): A 2D array of shape (n, 2) where n is the number of points,
                            and each row contains the (x, y) coordinates of a point.

    Returns:
    float: The perimeter of the shape.
    """
    perimeter = 0.0
    num_points = points.shape[0]

    for i in range(num_points):
        j = (i + 1) % num_points  # Next point index, wrapping around to the start
        distance = np.linalg.norm(points[i] - points[j])
        perimeter += distance

    return perimeter

base_path = './'
output_file = 'perimeter.txt'

# Open the output file in write mode
with open(output_file, 'w') as f:
    # Write the header
    f.write('case,perimeter\n')

    for i in range(1, 101):
        case_folder = f'nurbs_case_{i}'
        npz_name = f'case_{i}'
        case_path = os.path.join(base_path, case_folder)

        if not os.path.isdir(case_path):
            print(f"{case_folder} does not exist")
            continue

        # List all Gr_* folders
        gr_folders = [d for d in os.listdir(case_path) if os.path.isdir(os.path.join(case_path, d)) and d.startswith('Gr_')]

        if not gr_folders:
            print(f"No Gr_* folders found in {case_folder}")
            continue

        # Randomly select one Gr_* folder
        selected_gr_folder = random.choice(gr_folders)
        npz_file_path = os.path.join(case_path, selected_gr_folder, f'{npz_name}.npz')

        if not os.path.isfile(npz_file_path):
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

        # Calculate the perimeter
        perimeter = calculate_perimeter(shape_points)

        print(f"The perimeter of the shape in {npz_file_path} is: {perimeter}")

        # Write the result to the file
        f.write(f'{i},{perimeter}\n')
