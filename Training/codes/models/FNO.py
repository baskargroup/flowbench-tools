import os
import torch
import torch.nn as nn
from neuralop.models import TFNO
import glob

class TensorizedFNO(nn.Module):
    """
    Tensorized Fourier Neural Operator (TFNO) model for learning mappings between function spaces.
    """
    def __init__(self, n_modes, hidden_channels, in_channels, out_channels, projection_channels, n_layers = 4):
        """
        Initializes the TFNO model with specified parameters.

        Args:
            n_modes (tuple): Number of modes for Fourier layers.
            hidden_channels (int): Number of hidden channels.
            in_channels (int): Number of input channels.
            out_channels (int): Number of output channels.
        """
        super(TensorizedFNO, self).__init__()
        self.n_modes = n_modes
        self.hidden_channels = hidden_channels
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.projection_channels = projection_channels
        self.n_layers = n_layers

        # Initialize the TFNO with Tucker factorization
        self.tfno = TFNO(n_modes=self.n_modes, hidden_channels=self.hidden_channels,
                         in_channels=self.in_channels, out_channels=self.out_channels, 
                         projection_channels = self.projection_channels, n_layers = self.n_layers)

    def forward(self, x):
        """
        Forward pass of the TFNO model.

        Args:
            x (Tensor): Input tensor.

        Returns:
            Tensor: Output tensor after passing through the TFNO.
        """
        return self.tfno(x)

    def save_checkpoint(self, save_name, save_folder='experiments/fno/checkpoints'):
        """
        Saves the model weights to a checkpoint file.

        Args:
            save_name (str): Name of the checkpoint file.
            save_folder (str, optional): Folder to save the checkpoint. Defaults to 'experiments/fno'.
        """
        os.makedirs(save_folder, exist_ok=True)
        torch.save(self.state_dict(), os.path.join(save_folder, f'{save_name}.pth'))

    def load_checkpoint(self, save_name=None, save_folder='experiments/fno/checkpoints'):
        """
        Loads the model weights from a checkpoint file.

        Args:
            save_name (str, optional): Name of the checkpoint file. If None, loads the latest checkpoint.
            save_folder (str, optional): Folder containing the checkpoint. Defaults to 'experiments/fno'.
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
# model = TensorizedFNO(n_modes=(16, 16), hidden_channels=64, in_channels=1, out_channels=1)
# model.save_checkpoint(save_name='model_checkpoint')
# model.load_checkpoint()