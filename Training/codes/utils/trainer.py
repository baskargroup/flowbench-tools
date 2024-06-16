import os
import torch

from codes.models.FNO import TensorizedFNO
from codes.models.CNO import CompressedCNO
from codes.utils.functions import L2_norm, LInf_norm
from codes.utils.visualization import plot_ldc_like


class Trainer:
    def __init__(self, model, optimizer, loss_fn, train_loader, val_loader, epochs, device, log_dir=None, checkpoint_frequency = 1):
        self.model = model.to(device)
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.epochs = epochs
        self.device = device
        self.log_dir = log_dir
        self.checkpoint_frequency = checkpoint_frequency

        self.log_file = os.path.join(log_dir, 'log.txt') if log_dir else None

    def train_epoch(self):
        self.model.train()
        total_loss = 0

        for batch in self.train_loader:
            inputs, targets = batch[0].to(self.device), batch[1].to(self.device)
            self.optimizer.zero_grad()
            outputs = self.model.forward(inputs)
            loss = self.loss_fn(outputs, targets)
            loss.backward()
            self.optimizer.step()
            total_loss += loss.item()

        return total_loss / len(self.train_loader.dataset)

    def evaluate(self, epoch = None):
        self.model.eval()
        total_loss = 0
        totall2_loss = 0
        totalinf_loss = 0

        with torch.no_grad():
            for batch in self.val_loader:
                inputs, targets = batch[0].to(self.device), batch[1].to(self.device)
                outputs = self.model.forward(inputs)
                loss = self.loss_fn(outputs, targets)

                _l2_loss = L2_norm(outputs.cpu().numpy(), targets.cpu().numpy(), 1/511, 1/511)
                _linf_loss = LInf_norm(outputs.cpu().numpy(), targets.cpu().numpy(), 1/511, 1/511)

                total_loss += loss.item()
                totall2_loss += _l2_loss
                totalinf_loss += _linf_loss

                if epoch is not None:
                    plot_ldc_like(targets.cpu().numpy(), outputs.cpu().numpy(), 0, os.path.join(self.log_dir, 'plots', str(epoch), f'{total_loss}.png'))

        return total_loss / len(self.val_loader.dataset), totall2_loss / len(self.val_loader.dataset), totalinf_loss / len(self.val_loader.dataset)

    def train(self):
        best_val_loss = float('inf')

        for epoch in range(self.epochs):
            train_loss = self.train_epoch()
            val_loss, l2_loss, linf_loss = self.evaluate()

            log_line = f'Epoch {epoch+1}/{self.epochs}, Train Loss: {train_loss}, Val Loss: {val_loss}, L2 Loss: {l2_loss}, LInf Loss: {linf_loss}'
            print(log_line)

            if self.log_file:
                log_dir = os.path.dirname(self.log_file)
                os.makedirs(log_dir, exist_ok=True)

                with open(self.log_file, 'a') as log_file_handle:
                    log_file_handle.write(log_line + '\n')

            if (epoch+1) % self.checkpoint_frequency == 0:
                self.model.save_checkpoint(save_folder= os.path.join(log_dir, 'checkpoints') if log_dir else None, 
                                           save_name=str(epoch+1))

        print("Training complete.")

    def load_model(self):
        self.model.load_checkpoint()

class TrainFNO(Trainer):
    def __init__(self, model, optimizer, loss_fn, train_loader, val_loader, epochs, device, log_dir = 'experiments/fno/', checkpoint_frequency = 1):
        super().__init__(model, optimizer, loss_fn, train_loader, val_loader, epochs, device, log_dir, checkpoint_frequency)
        if not isinstance(model, TensorizedFNO):
            raise TypeError("The model should be an instance of TensorizedFNO")

class TrainCNO(Trainer):
    def __init__(self, model, optimizer, loss_fn, train_loader, val_loader, epochs, device, log_dir = 'experiments/cno/', checkpoint_frequency = 1):
        super().__init__(model, optimizer, loss_fn, train_loader, val_loader, epochs, device, log_dir, checkpoint_frequency)
        if not isinstance(model, CompressedCNO):
            raise TypeError("The model should be an instance of CompressedCNO")