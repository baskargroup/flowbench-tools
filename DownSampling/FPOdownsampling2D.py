import vtk
import numpy as np
import matplotlib.pyplot as plt
from vtkmodules.util import numpy_support

# Enable VTK multi-threading
vtk.vtkMultiThreader.SetGlobalDefaultNumberOfThreads(vtk.vtkMultiThreader.GetGlobalMaximumNumberOfThreads())

# Path to the input PVTU file
input_file = "results/sol_14950.pvtu"

# Path to save the output .npz file
output_npz_file = "output_image.npz"


# Start timer for loading PVTU file
# start_time = time.time()


# Load the PVTU file
reader = vtk.vtkXMLPUnstructuredGridReader()
reader.SetFileName(input_file)
reader.Update()

# Resample the data to an image
resample = vtk.vtkResampleToImage()
resample.SetInputConnection(reader.GetOutputPort())
resample.SetSamplingDimensions(1025, 257, 1)  # Adjusted for faster processing
resample.SetSamplingBounds(4.0, 20.0, 6.0, 10.0, 0.0, 0.0)
resample.Update()

# Convert point data to cell data
point_to_cell = vtk.vtkPointDataToCellData()
point_to_cell.SetInputConnection(resample.GetOutputPort())
point_to_cell.Update()

# Get the image data from the point_to_cell filter
image_data = point_to_cell.GetOutput()

# Get the cell data arrays
u_array = image_data.GetCellData().GetArray('u')
if u_array is None:
    raise ValueError("Field 'u' not found in the cell data.")
u_values = numpy_support.vtk_to_numpy(u_array)

v_array = image_data.GetCellData().GetArray('v')
if v_array is None:
    raise ValueError("Field 'v' not found in the cell data.")
v_values = numpy_support.vtk_to_numpy(v_array)

p_array = image_data.GetCellData().GetArray('p')
if p_array is None:
    raise ValueError("Field 'p' not found in the cell data.")
p_values = numpy_support.vtk_to_numpy(p_array)

# Get grid dimensions
dims = image_data.GetDimensions()

# Reshape the cell data arrays 
u_values = u_values.reshape((dims[1]-1, dims[0]-1))
v_values = v_values.reshape((dims[1]-1, dims[0]-1))
p_values = p_values.reshape((dims[1]-1, dims[0]-1))

# Combine u, v, and p arrays into a single 3D array
combined_array = np.stack((u_values, v_values, p_values), axis=-1)  # Shape will be [dims[1]-1, dims[0]-1, 3]


# Save the combined array as a .npz file
np.savez(output_npz_file, data=combined_array)

print("Combined array shape:", combined_array.shape)