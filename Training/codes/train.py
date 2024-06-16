from codes.data.dataset import LidDrivenDataset
from codes.models.FNO import TensorizedFNO
from codes.models.CNO import CompressedCNO
from codes.utils.trainer import TrainFNO
from codes.utils.trainer import TrainCNO
from codes.utils.device import device

import os
import yaml
import torch

def list_folders(base_path):
    # List to store the folder paths
    folder_paths = []

    # Walk through the directory
    for root, dirs, files in os.walk(base_path):
        for directory in dirs:
            # Get the full path of each directory
            dir_path = os.path.join(root, directory)
            folder_paths.append(dir_path)
    
    return folder_paths

def read_yaml_file(folder_path, file_name):
    # Construct the full file path
    file_path = os.path.join(folder_path, file_name)

    # Read the YAML file
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as exc:
            print(f"Error reading YAML file: {exc}")
            return None
        
def fno_train(config_data, folder):
    LidDriven_dataset = LidDrivenDataset(
        file_path_x= config_data['file_path_x'],
        file_path_y= config_data['file_path_y']
    )

    # Create data loaders for training and validation
    train_loader, val_loader = LidDriven_dataset.create_dataloader(batch_size= config_data['batch_size'], 
                                                                   split_fraction= config_data['split_fraction'], 
                                                                   shuffle=True)
    
    os.makedirs(os.path.join(folder, 'dataset'), exist_ok=True)
    torch.save(train_loader.dataset, os.path.join(folder, 'dataset','train.pt'))
    torch.save(val_loader.dataset, os.path.join(folder, 'dataset','val.pt'))
    
    # Set the learning rate and number of epochs
    learning_rate = config_data['learning_rate']
    num_epochs = config_data['num_epochs']

    # Create an instance of the TensorizedFNO model
    model = TensorizedFNO(n_modes = config_data['n_modes'], in_channels = config_data['in_channels'], 
                          out_channels = config_data['out_channels'], hidden_channels = config_data['hidden_channels'], 
                          projection_channels = config_data['projection_channels'], n_layers = config_data['n_layers'])
    
    # Define loss function and optimizer
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Create an instance of the TrainFNO class
    FNO_trainer = TrainFNO(model=model, optimizer=optimizer, loss_fn=criterion,
                           train_loader=train_loader, val_loader=val_loader, epochs=num_epochs,
                           device=device, log_dir = folder, checkpoint_frequency = config_data['checkpoint_frequency'])
    
    FNO_trainer.train()

def cno_train(config_data, folder):
    LidDriven_dataset = LidDrivenDataset(
        file_path_x= config_data['file_path_x'],
        file_path_y= config_data['file_path_y']
    )

    # Create data loaders for training and validation
    train_loader, val_loader = LidDriven_dataset.create_dataloader(batch_size= config_data['batch_size'], 
                                                                   split_fraction= config_data['split_fraction'], 
                                                                   shuffle=True)
    
    os.makedirs(os.path.join(folder, 'dataset'), exist_ok=True)
    torch.save(train_loader.dataset, os.path.join(folder, 'dataset','train.pt'))
    torch.save(val_loader.dataset, os.path.join(folder, 'dataset','val.pt'))
    
    # Set the learning rate and number of epochs
    learning_rate = config_data['learning_rate']
    num_epochs = config_data['num_epochs']

    # Create an instance of the CompressedCNO model
    model = CompressedCNO(in_dim = config_data['in_dim'], out_dim = config_data['out_dim'], 
                          N_layers = config_data['N_layers'], in_size = config_data['in_size'], 
                          out_size = config_data['out_size'])
    
    # Define loss function and optimizer
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    # Create an instance of the TrainFNO class
    CNO_trainer = TrainCNO(model=model, optimizer=optimizer, loss_fn=criterion,
                           train_loader=train_loader, val_loader=val_loader, epochs=num_epochs,
                           device=device, log_dir = folder, checkpoint_frequency = config_data['checkpoint_frequency'])
    
    CNO_trainer.train()

# Base directory path
base_path = 'experiments'

# Get the list of folder paths
folders = list_folders(base_path)

# Print the folder paths
for folder in folders:
    # Create an instance of the LidDrivenDataset
    print(folder)
    config_data = read_yaml_file(folder, "config.yaml")
    print(config_data, '\n')

    if config_data['model'] == 'fno':
        fno_train(config_data, folder)

    elif config_data['model'] == 'cno':
        cno_train(config_data, folder)

    print('\n')