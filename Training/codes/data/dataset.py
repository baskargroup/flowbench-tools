import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np

class LidDrivenDataset(Dataset):
    """
    Custom dataset for loading and processing Lid Driven Cavity problem data from .npz files.
    """
    def __init__(self, file_path_x, file_path_y, transform=None):
        """
        Initializes the dataset with the paths to the .npz files and an optional transform.
        
        Args:
            file_path_x (str): Path to the .npz file containing the input data.
            file_path_y (str): Path to the .npz file containing the target data.
            transform (callable, optional): Optional transform to be applied on a sample.
        """
        # Load data from .npz files
        x = np.load(file_path_x)['data']
        y = np.load(file_path_y)['data']
        #self.x = np.load(file_path_x)['data']
        #self.y = np.load(file_path_y)['data']

        
        # Convert numpy arrays to PyTorch tensors
        self.x = torch.tensor(x, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)
        
        self.transform = transform

    def __len__(self):
        """
        Returns the total number of samples in the dataset.
        """
        return self.x.shape[0]

    def __getitem__(self, idx):
        """
        Retrieves the sample and its label at the specified index.
        
        Args:
            idx (int): Index of the sample to retrieve.
        
        Returns:
            tuple: (sample, target) where sample is the input data and target is the expected output.
        """
        sample = self.x[idx]
        target = self.y[idx]
        #sample = torch.tensor(self.x[idx], dtype=torch.float32)
        #target = torch.tensor(self.y[idx], dtype=torch.float32)
        
        if self.transform:
            sample = self.transform(sample)
        
        return sample, target
    
    def create_dataloader(self, batch_size, split_fraction=0.8, shuffle=True):
        """
        Creates and returns data loaders for training and validation sets.

        Args:
            batch_size (int): Batch size for the data loaders.
            split_fraction (float, optional): Fraction of the dataset to use for training. Default is 0.8.
            shuffle (bool, optional): Whether to shuffle the dataset before splitting. Default is True.

        Returns:
            tuple: (train_loader, val_loader) where train_loader is the data loader for the training set
                   and val_loader is the data loader for the validation set.
        """
        dataset_size = len(self)
        train_size = int(dataset_size * split_fraction)
        val_size = dataset_size - train_size

        train_dataset, val_dataset = torch.utils.data.random_split(self, [train_size, val_size])

        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=shuffle)

        return train_loader, val_loader

# Example usage:
# dataset = LidDrivenDataset(
#     file_path_x='../../../../../rtali/projects/all-neural-operators/TimeDependentNS/LidData_Curated_Input/harmonics/harmonics_lid_driven_cavity_X.npz',
#     file_path_y='../../../../../rtali/projects/all-neural-operators/TimeDependentNS/LidData_Curated_Input/harmonics/harmonics_lid_driven_cavity_y.npz'
# 