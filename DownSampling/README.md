# Python Script for Converting PVTU Data to NPZ Format in LDC cases (PV-python Version)

This script provides a way to convert data from a PVTU file format to an NPZ file format. This process has been used to convert Dendrite outputs (PVTU) to npz format.

## Purpose

The primary purpose of this script is to:
1. Load data from a PVTU file.
2. Resample the data into a specified image format.
3. Extract specific fields from the resampled data.
4. Combine these fields into a single array.
5. Save the combined array in NPZ format for easy loading and use in Python.

## How to Use

1. **Set the Input and Output Paths:**
   - Define the path to the input PVTU file by setting the `input_file` variable.
   - Define the path to save the output NPZ file by setting the `output_npz_file` variable.

2. **Load the PVTU File:**
   - The script uses ParaView's `XMLPartitionedUnstructuredGridReader` to read the PVTU file.

3. **Resample the Data:**
   - The data is resampled to a specified image dimension using `ResampleToImage`. Adjust the `SamplingDimensions` as needed.

4. **Convert Point Data to Cell Data:**
   - The script converts point data to cell data using the `PointDatatoCellData` filter.

5. **Extract Data Fields:**
   - Extract specific data fields (`u`, `v`, `p`) from the cell data. Ensure that these fields exist in your data.

6. **Combine and Save the Data:**
   - Combine the extracted fields into a single 3D array.
   - Save the combined array as an NPZ file using `np.savez`.