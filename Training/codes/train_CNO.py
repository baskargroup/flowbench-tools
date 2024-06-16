# Import necessary modules
from codes.data.dataset import LidDrivenDataset
from codes.models.CNO import CompressedCNO
from codes.utils.trainer import TrainCNO
from codes.utils.device import device
import torch

# Create an instance of the LidDrivenDataset
LidDriven_dataset = LidDrivenDataset(
   file_path_x='data/harmonics/harmonics_lid_driven_cavity_X.npz',
   file_path_y='data/harmonics/harmonics_lid_driven_cavity_y.npz'
)

# Create data loaders for training and validation
train_loader, val_loader = LidDriven_dataset.create_dataloader(batch_size=10, split_fraction=0.8, shuffle=True)

# Create an instance of the CompressedCNO model
model = CompressedCNO(in_dim=3, out_dim=3, N_layers=5, in_size=512, out_size=512)

# Set the learning rate and number of epochs
learning_rate = 0.001
num_epochs = 2000

# Define loss function and optimizer
criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Create an instance of the TrainCNO class
CNO_trainer = TrainCNO(model=model, optimizer=optimizer, loss_fn=criterion,
                      train_loader=train_loader, val_loader=val_loader, epochs=num_epochs,
                      device=device)

CNO_trainer.train()