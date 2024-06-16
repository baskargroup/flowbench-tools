# Import necessary modules
from codes.data.dataset import LidDrivenDataset
from codes.models.FNO import TensorizedFNO
from codes.utils.trainer import TrainFNO
from codes.utils.device import device
import torch

# Create an instance of the LidDrivenDataset
LidDriven_dataset = LidDrivenDataset(
   file_path_x='data/harmonics/harmonics_lid_driven_cavity_X.npz',
   file_path_y='data/harmonics/harmonics_lid_driven_cavity_y.npz'
)

# Create data loaders for training and validation
train_loader, val_loader = LidDriven_dataset.create_dataloader(batch_size=5, split_fraction=0.8, shuffle=True)

# Create an instance of the TensorizedFNO model
model = TensorizedFNO(n_modes=(256, 256), in_channels=3, out_channels=3, hidden_channels=64, projection_channels=128)

# Set the learning rate and number of epochs
learning_rate = 0.001
num_epochs = 2000

# Define loss function and optimizer
criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Create an instance of the TrainFNO class
FNO_trainer = TrainFNO(model=model, optimizer=optimizer, loss_fn=criterion,
                      train_loader=train_loader, val_loader=val_loader, epochs=num_epochs,
                      device=device)

FNO_trainer.train()