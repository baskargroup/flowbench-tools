import torch

if torch.cuda.is_available():
    # Set the default device to CUDA
    device = torch.device('cuda')
    #torch.set_default_device(device)
    print('Using CUDA for tensor operations')
    torch.cuda.empty_cache()
else:
    device = torch.device('cpu')
    print('CUDA is not available. Using CPU for tensor operations')