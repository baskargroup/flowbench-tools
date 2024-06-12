import numpy as np
import os
import glob
import sys

'''
Note - Transient Problems are usually modeled as Seq to Seq problems. This means we take certain time steps as input and predict some future time steps as output. Hence we are not using any geometrical information for FPO models.

Note - 242 time steps have been simulated but ignore the first two steps during any modeling process

Output Data for the 2D Multiphase Flow problem needs to be arranged in the following way:
- (samples x time x channel x grid x grid), 1150 samples in total.

Input Data lies in the following directory structure in Nova:

        - ~/1/
        
            - Re<1>
                sol_t1.npz ... sol_t242.npz -> 512 x 128 x 3
            - Re<2>
                sol_t1.npz ... sol_t242.npz
            - ...
            - Re<5>
                sol_t1.npz ... sol_t242.npz
            
        - ~/2/
        
            - Re<1>
                sol_t1.npz ... sol_t242.npz
            - Re<2>
                sol_t1.npz ... sol_t242.npz
            - ...
            - Re<5>
                sol_t1.npz ... sol_t242.npz
            
        - ...
        
        - ~/.../
        
            - Re<1>
                sol_t1.npz ... sol_t242.npz
            - Re<2>
                sol_t1.npz ... sol_t242.npz
            - ...
            - Re<5>
                sol_t1.npz ... sol_t242.npz
'''

def flow_past_object(base_folder_data : str, 
                      num_in_channels : int , 
                      num_out_channels: int, 
                      grid_size_x: int,
                      grid_size_y: int,
                      t_start_in: int, 
                      t_end_in: int,
                      t_start_out: int,
                      t_end_out: int,
                      output_dir : str) -> None:
    
    """ Does full data processing for the flow past an object problem."""
    
    #Check if the base folder exists
    assert os.path.exists(base_folder_data) and os.path.exists(output_dir), "The base folder does not exist."
    
    #Check number of channels >= 1
    assert num_in_channels * num_out_channels >= 9, "The number of channels should be 3 each."
    
    #Check grid size > 0
    assert grid_size_x > 0, "The grid size x should be greater than 0."
    assert grid_size_y > 0, "The grid size y should be greater than 0."
    
    #Check the time values passed to this function make sense
    assert t_start_in >= 2, "Start from the third time step."
    assert t_end_in >= t_start_in, "Travel forward in time. Not Backwards. t_start <= t_end"
    assert t_start_out > t_end_in, "Make sure that your output sequence starts after input sequence ends"
    assert t_start_end >= t_end_out, "Travel forward in time. Not Backwards. t_start <= t_end"
    
    
    #Total number of samples
    total_samples = 1150
    
    '''
    Calculate time lengths for the input and output data
    '''
    duration_in = t_end_in - t_start_in + 1
    duration_out = t_end_out - t_start_out + 1
    
    '''
    Numpy tensor initialization for the input and output data
    '''
    #Create an empty 4d array - (samples x channel x grid x grid) - Input data
    _lhs = np.zeros((total_samples, duration_in, num_channels_in, grid_size_y, grid_size_x))
    
    #Create an empty 4d array - (samples x channel x grid x grid) - Output data
    _rhs = np.zeros((total_samples, duration_out, num_channels_out, grid_size_y, grid_size_x))
    
    '''
    Add the data to the 4D arrays : Input and Output
    '''
    sample_ctr = 0
    
    #Loop over all the cases
    for case in range(1, num_geometry+1):
            
        #Go to the respective folder
        case_dir = os.path.join(base_folder_data, str(case))
        
        #There are 5 files in this directory - <>sol_t.npz. Get the Reynolds numbers from the files
        _reynolds = glob.glob(os.path.join(case_dir, 'Re*.npz'))
        
        #Extract the Reynolds numbers from the file names. The cryptic file names are of the form Re_<Reynolds#>.npz
        reynold_nos = [int(os.path.basename(_reynolds[i]).split('_')[1]) for i in range(len(_reynolds)]
        
        #Loop over the Reynolds numbers
        for reynold_no in reynold_nos:

            #Load the complete 240 steps for a Reynolds number in one go
            _data = np.load(os.path.join(case_dir, 'Re_' + str(reynold_no) + '.npz'))['data']
            
            '''
                Prepare Input data
            '''
            
            dur = 0
            #Loop over the time steps
            for time_step_in in range(t_start_in, t_end_in+1):
                
                #Add the data to the 4D arrays - Input and Output
                _lhs[sample_ctr, dur, 0, :, :] = _data[time_step_in,:,:,0]
                _lhs[sample_ctr, dur, 1, :, :] = _data[time_step_in,:,:,1]
                _lhs[sample_ctr, dur, 2, :, :] = _data[time_step_in,:,:,2]

                dur += 1
            
            '''
                Prepare Output data
            '''
            dur = 0
            #Loop over the time steps
            for time_step_out in range(t_start_out, t_end_out+1):
                  
                _rhs[sample_ctr, dur, 0, :, :] = _data[time_step_out,:,:,0]
                _rhs[sample_ctr, dur, 1, :, :] = _data[time_step_out,:,:,1]
                _rhs[sample_ctr, dur, 2, :, :] = _data[time_step_out,:,:,2]

                dur += 1
                
            #Increment the sample counter
            sample_ctr += 1
    
    #Print the total number of samples
    print("Total number of samples expected: ", total_samples)
    print("\nTotal number of samples processed: ", sample_ctr)

    #Adjust dimensions before saving
    _lhs = np.transpose(_lhs, (0,1,2,4,3))
    _rhs = np.transpose(_rhs, (0,1,2,4,3))
            
    #Save the data - data_set is contained in the npz file i.e., you have to specify the key 'data_set' to access the data from the npz file
    np.savez_compressed(output_dir + 'flow_past_object_X.npz', data = _lhs)
    np.savez_compressed(output_dir + 'flow_past_object_Y.npz', data = _rhs) 


if __name__ == '__main__':
    
    #Check the number of arguments passed to the script == 4
    if len(sys.argv) != 5:
        print("Usage: python3 flow_past_object_data.py needs 4 arguments - t_start_in t_end_in t_start_out t_end_out")
        sys.exit(1)
    
    #Set Parameters
    base_folder_data = ''
    output_dir = ''
    grid_size_x = 512
    grid_size_y = 128
    num_in_channels = 3
    num_out_channels = 3
    
    t_start_in = int(sys.argv[1])
    t_end_in = int(sys.argv[2])
    t_start_out = int(sys.argv[3])
    t_end_out = int(sys.argv[4])
    
    #Create Input and Output tensors for the lid-driven cavity problem
    flow_past_object(base_folder_data = base_folder_data, 
                      num_in_channels = num_in_channels, 
                      num_out_channels = num_out_channels, 
                      grid_size_x = grid_size_x, 
                      grid_size_y= grid_size_y,
                      t_start_in= t_start_in,
                      t_end_in= t_end_in,
                      t_start_out= t_start_out,
                      t_end_out= t_end_out,
                      output_dir = output_dir)
