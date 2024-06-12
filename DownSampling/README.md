# Python Script for Converting PVTU Data to NPZ Format
## LDCdownsampling2D.py

This script provides a way to convert data from a PVTU file format to an NPZ file format. This script has been used to convert Dendrite outputs (PVTU) to npz format in Lid Driven Cavity cases.

## Purpose

The primary purpose of this script is to:
1. Load data from a PVTU file.
2. Resample the data into a specified resolution e.g., 512x512.
3. Extract specific fields e.g., `u,v,p` from the resampled data.
4. Combine these fields into a single array.
5. Save the combined array in NPZ format for easy loading and use by downstream tensor creation for ML. Refer to the `DataPrep` directory in this repository.

## How to Use

1. **Set the Input and Output Paths:**
   - Define the path to the input PVTU file by setting the `input_file` variable.
   - Define the path to save the output NPZ file by setting the `output_npz_file` variable.

2. **Load the PVTU File:**
   - The script uses ParaView's `XMLPartitionedUnstructuredGridReader` to read the PVTU file.

3. **Resample the Data to a desired resolution:**
   - The data is resampled to a specified image dimension using `ResampleToImage`. Adjust the `SamplingDimensions` as needed. Choose 512x512 or 256x256 or 128x128

4. **Convert Point Data to Cell Data:**
   - The script converts point data to cell data using the `PointDatatoCellData` filter.

5. **Extract Data Fields:**
   - Extract specific data fields (`u`, `v`, `p`) from the cell data. Ensure that these fields exist in your data.

6. **Combine and Save the Data:**
   - Combine the extracted fields into a single 3D array.
   - Save the combined array as an NPZ file using `np.savez`.


## FPOdownsampling2D.py

This script provides a method to convert data from a PVTU file format to an NPZ file format. This script has been used to convert Dendrite outputs (PVTU) to npz format in Flwo Past an Object cases.


## Purpose

The primary purpose of this script is to:
1. Load data from a PVTU file.
2. Resample the data into a specified resolution.
3. Extract specific fields from the resampled data.
4. Combine these fields into a single array.
5. Save the combined array in NPZ format for easy loading and use in Python.

## How to Use

1. **Set the Input and Output Paths:**
   - Define the path to the input PVTU file by setting the `input_file` variable.
   - Define the path to save the output NPZ file by setting the `output_npz_file` variable.

2. **Load the PVTU File:**
   - The script uses VTK's `vtkXMLPUnstructuredGridReader` to read the PVTU file.

3. **Resample the Data to a desired resolution:**
   - The data is resampled to a specified image dimension using `vtk.vtkResampleToImage`. Adjust the `SetSamplingDimensions` and `SetSamplingBounds` as needed.
   - Choose one of 512x128, 1024x256 and 2048x512

4. **Convert Point Data to Cell Data:**
   - The script converts point data to cell data using the `vtkPointDataToCellData` filter.

5. **Extract Data Fields:**
   - Extract specific data fields (`u`, `v`, `p`) from the cell data. Ensure that these fields exist in your data.

6. **Combine and Save the Data:**
   - Combine the extracted fields into a single 3D array.
   - Save the combined array as an NPZ file using `np.savez`.



## LDCdownsampling3D.py

This script provides a way to convert data from a 3D PVTU file format to an NPZ file format. This script has been used to convert Dendrite outputs (PVTU) to npz format in 3D Lid Driven Cavity cases.

## Purpose

The primary purpose of this script is to:
1. Load data from a PVTU file.
2. Resample the data into a specified resolution. Choose 128x128x128
3. Extract specific fields from the resampled data.
4. Combine these fields into a single array.
5. Save the combined array in NPZ format for easy loading and use in Python.

## How to Use

1. **Set the Input and Output Paths:**
   - Define the path to the input PVTU file by setting the `input_file` variable.
   - Define the path to save the output NPZ file by setting the `output_npz_file` variable.

2. **Load the PVTU File:**
   - The script uses ParaView's `XMLPartitionedUnstructuredGridReader` to read the PVTU file.

3. **Resample the Data to desired resolution:**
   - The data is resampled to a specified image dimension using `ResampleToImage`. Adjust the `SamplingDimensions` as needed.

4. **Convert Point Data to Cell Data:**
   - The script converts point data to cell data using the `PointDatatoCellData` filter.

5. **Extract Data Fields:**
   - Extract specific data fields (`u`, `v`, `w`, `p`) from the cell data. Ensure that these fields exist in your data.

6. **Combine and Save the Data:**
   - Combine the extracted fields into a single 3D array.
   - Save the combined array as an NPZ file using `np.savez`.

