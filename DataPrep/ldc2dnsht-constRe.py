import numpy as np
import os
import glob
import pandas as pd
'''
Output Data for the 2D lid-driven cavity problem needs to be arranged in the following way:
- (samples x channel x grid x grid)

Input Data lies in the following directory structure:

        - ~/1
        
            - Re<1>sol.npz
            - Re<2>sol.npz
            - ...
            
        - ~/2
        
            - Re<1>sol.npz
            - Re<2>sol.npz
            - ...
            
        - ...
        
        - ~/100
        
            - Re<1>sol.npz
            - Re<2>sol.npz
            - ...
            
'''

# Define the function to look up Cd and Cl based on Case and Re
def lookup_values(df, case_value, gr_value):
    # Filter the DataFrame based on Case and Re
    filtered_df = df[(df['Case'] == case_value) & (df['Gr'] == gr_value)]
    
    if filtered_df.empty:
        print('Couldn\'t filter anything')
        return None, None
    
    # Get the Cd and Cl values
    cd_value = filtered_df.iloc[0]['Cd']
    cl_value = filtered_df.iloc[0]['Cl']
    nu_value = filtered_df.iloc[0]['Nu']
    
    return cd_value, cl_value, nu_value

def lid_driven_cavity(base_folder_data : str, 
                      base_folder_geom : str ,
                      num_in_channels : int , 
                      num_out_channels: int, 
                      grid_size: int, 
                      num_geometry : int, 
                      num_Res : int,
                      output_dir : str,
                      constants_df) -> None:
    
    """ Does full data processing for the lid-driven cavity problem - Steady State."""
    
    #Check if the base folder exists
    assert os.path.exists(base_folder_data) and os.path.exists(base_folder_geom), "The base folder does not exist."
    
    #Check number of channels >= 1
    assert num_in_channels * num_out_channels >= 9, "The number of channels should be 3 each."
    
    #Check grid size > 0
    assert grid_size > 0, "The grid size should be greater than 0."
    
    #Check number of geometries > 0
    assert num_geometry > 0, "The number of geometries should be greater than 0."
    
    
    # @total_samples : int : Total number of samples - Combine all the Reynolds numbers and geometries e.g. 15 Re x 100 Geometries = 1500 samples
    #Total number of samples
    total_samples = num_Res * num_geometry #990 for nurbs
    
    '''
    Numpy tensor initialization for the input and output data
    '''
    #Create an empty 4d array - (samples x channel x grid x grid) - Input data
    _lhs = np.zeros((total_samples, num_in_channels, grid_size, grid_size))
    
    #Create an empty 4d array - (samples x channel x grid x grid) - Output data
    _rhs = np.zeros((total_samples, num_out_channels, grid_size, grid_size))
    
    '''
    Add the data to the 4D arrays : Input and Output
    '''
    sample_ctr = 0
    
    #Loop over all the cases
    for case in range(1, num_geometry+1):
        
        if case != 1e6:
            
            #Go to the respective folder
            case_dir = os.path.join(base_folder_data, str(case))
            
            #There are 10 files in this directory - <>sol.npz. Get the Reynolds numbers from the files
            _reynolds = glob.glob(os.path.join(case_dir, '*sol.npz'))
            
            #Extract the Reynolds numbers from the file names
            reynold_nos = [int(os.path.basename(_reynolds[i]).split('_')[0]) for i in range(num_Res)]
            
            #Loop over the Reynolds numbers
            for reynold_no in reynold_nos:
                
                '''
                    Prepare Input data
                '''
                
                #Reynold# Channel
                _ResChannel = np.ones((grid_size, grid_size), dtype=int) * reynold_no
                #Sign distance field Channel
                _SDFChannel = np.load(os.path.join(base_folder_geom, 'sdf' + str(case) + '_reduced.npy'))
                #Geometry Channel
                _GeomChannel = np.where(_SDFChannel > 0, 255, 0) #Binary channel - 0 or 255 - Black & White
                
                
                #Add the data to the 4D arrays - Input and Output
                _lhs[sample_ctr, 0, :, :] = _ResChannel
                _lhs[sample_ctr, 1, :, :] = _SDFChannel
                _lhs[sample_ctr, 2, :, :] = _GeomChannel
                
                
                '''
                    Prepare Output data
                '''
                Cd, Cl, Nu = lookup_values(constants_df, case, reynold_no)
                
                #Load the data from the npz file
                _data = np.load(os.path.join(case_dir, str(reynold_no) + '_sol.npz'))
                
                #The data is stored as a csv file with columns as x, y, u, v, p
                #Load the data into the 4D array
                
                
                fourth_grid = int(grid_size/4)
                half_grid = int(grid_size/2)
                
                _rhs[sample_ctr, 0, :, :] = _data['data'][:,:,0]
                _rhs[sample_ctr, 1, :, :] = _data['data'][:,:,1]
                _rhs[sample_ctr, 2, :, :] = _data['data'][:,:,2]
                _rhs[sample_ctr, 3, :, :] = _data['data'][:,:,3]
                _rhs[sample_ctr, 4, :, :fourth_grid] = Cd*np.ones((grid_size, fourth_grid), dtype=float)
                _rhs[sample_ctr, 4, :, fourth_grid:half_grid] = Cl*np.ones((grid_size, fourth_grid), dtype=float)   
                _rhs[sample_ctr, 4, :, half_grid:] = Nu*np.ones((grid_size, half_grid), dtype=float)            
            
                
                #Increment the sample counter
                sample_ctr += 1
                
    #Save the data - data_set is contained in the npz file i.e., you have to specify the key 'data_set' to access the data from the npz file
    np.savez_compressed(output_dir + 'lid_driven_cavity_X.npz', data = _lhs)
    np.savez_compressed(output_dir + 'lid_driven_cavity_Y.npz', data = _rhs) 


if __name__ == '__main__':
    #Provide all settings
    HARMONICS_CONST_FILE  = 'Cd-Cl-Nu_cases_harmonics.txt'
    NURBS_CONST_FILE = 'Cd-Cl-Nu_cases_nurbs.txt'
    SKELETON_CONST_FILE = 'Cd-Cl-Nu_cases_skelneton.txt'
    base_folder_data = ''
    base_folder_geom = ''
    output_dir = ''
    num_geometry = 100
    num_Reynolds = 10
    grid_size = 512
    num_in_channels = 3
    num_out_channels = 5
    const_df = pd.read_csv(HARMONICS_CONST_FILE, sep = ',') #Change the constants file as necessary
    
    #Create Input and Output tensors for the lid-driven cavity problem
    lid_driven_cavity(base_folder_data = base_folder_data, 
                      base_folder_geom = base_folder_geom, 
                      num_in_channels = num_in_channels, 
                      num_out_channels = num_out_channels, 
                      grid_size = grid_size, 
                      num_geometry = num_geometry, 
                      num_Res = num_Reynolds,
                      output_dir = output_dir,
                      constants_df = const_df)
