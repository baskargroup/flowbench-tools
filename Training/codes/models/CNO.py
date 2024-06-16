import os
import torch
import torch.nn as nn
from codes.models.Modules.CNO.CNOModule import CNO
import glob

class CompressedCNO(nn.Module):
    def __init__(self, in_dim, out_dim, N_layers, in_size, out_size):
        super(CompressedCNO, self).__init__()
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.N_layers = N_layers
        self.in_size = in_size
        self.out_size = out_size

        # Initialize the CNO with Tucker factorization
        self.cno = CNO(in_dim  = self.in_dim, 
                       out_dim = self.out_dim,
                       N_layers = self.N_layers,
                       in_size = self.in_size,
                       out_size = self.out_size)
    def forward(self, x):
        """
        Forward pass of the CNO model.

        Args:
            x (Tensor): Input tensor.

        Returns:
            Tensor: Output tensor after passing through the CNO.
        """
        return self.cno(x)

    def save_checkpoint(self, save_name, save_folder='experiments/cno/checkpoints'):
        """
        Saves the model weights to a checkpoint file.

        Args:
            save_name (str): Name of the checkpoint file.
            save_folder (str, optional): Folder to save the checkpoint. Defaults to '../../experiments/cno/checkpoints'.
        """
        os.makedirs(save_folder, exist_ok=True)
        torch.save(self.state_dict(), os.path.join(save_folder, f'{save_name}.pth'))

    def load_checkpoint(self, save_name=None, save_folder='experiments/cno/checkpoints'):
        """
        Loads the model weights from a checkpoint file.

        Args:
            save_name (str, optional): Name of the checkpoint file. If None, loads the latest checkpoint.
            save_folder (str, optional): Folder containing the checkpoint. Defaults to '../../experiments/cno/checkpoints'.
        """
        if save_name is None:
            # Load the latest checkpoint based on the modification time
            checkpoints = glob.glob(os.path.join(save_folder, '*.pth'))
            if not checkpoints:
                raise FileNotFoundError("No checkpoints found in the specified folder.")
            latest_checkpoint = max(checkpoints, key=os.path.getmtime)
        else:
            latest_checkpoint = os.path.join(save_folder, f'{save_name}.pth')

        self.load_state_dict(torch.load(latest_checkpoint))

# Example usage:
# model = CompressedCNO(in_dim=11, out_dim=10, N_layers=5, in_size=64, out_size=64)
# model.save_checkpoint(save_name='model_checkpoint')
# model.load_checkpoint()
