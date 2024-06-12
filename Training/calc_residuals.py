import os
import sys
import json
import torch
from torch.utils import data
import numpy as np
import pandas as pd

#sys.path.append("/work/mech-ai/bkhara/diffnet")
sys.path.append("/work/mech-ai-scratch/arabeh/mlprojects/diffnet")
import matplotlib
# matplotlib.use("pgf")
matplotlib.rcParams.update({
    # 'font.family': 'serif',
    'font.size':12,
})
from matplotlib import pyplot as plt
from IPython.display import Image

import pytorch_lightning as pl
from pytorch_lightning import Trainer, seed_everything
from pytorch_lightning.loggers import TensorBoardLogger

import DiffNet
from DiffNet.networks.wgan import GoodNetwork
from DiffNet.DiffNetFEM import DiffNet2DFEM

from DiffNet.networks.unets import UNet
# from DiffNet.datasets.parametric.images import ImageIMBack
# from e1_complex_immersed_background import Poisson, MyPrintingCallback
from torch.utils.data import DataLoader


class ImageIMBack(data.Dataset):
    'PyTorch dataset for sampling coefficients'
    def __init__(self, dirname, domain_size=64):
        """
        Initialization
        """
        filenames = sorted(os.listdir(dirname))
        print(filenames)
        self.dataset = []
        for fname in filenames:
            filename = os.path.join(dirname, fname)
            sourcedata = np.load(filename)['data']            
            self.dataset.append(np.array([sourcedata]))
        self.dataset = np.array(self.dataset)
        self.n_samples = self.dataset.shape[0]

    def __len__(self):
        'Denotes the total number of samples'
        return self.n_samples

    def __getitem__(self, index):
        'Generates one sample of data'
        inputs = self.dataset[index]
        return torch.FloatTensor(inputs).squeeze()

class Poisson(DiffNet2DFEM):
    """docstring for Poisson"""
    def __init__(self, network, **kwargs):
        super(Poisson, self).__init__(network, **kwargs)
           
    def residual(self, dataX, dataY, hx, hy):
        r = dataX[:,0:1,...]        
        m = dataX[:,1:2,...]
        s = dataX[:,2:3,...]
        u = dataY[:,0:1,...]
        v = dataY[:,1:2,...]
        p = dataY[:,2:3,...]


        r_single_number = r[:,0,0,0] #r[:, 0, 0].int()
        gpw = self.gpw
        trnsfrm_jac = (0.5*hx)*(0.5*hy)
        JxW = (gpw*trnsfrm_jac).unsqueeze(-1).unsqueeze(-1).unsqueeze(0)

        u_gp = self.gauss_pt_evaluation(u)
        v_gp = self.gauss_pt_evaluation(v)
        u_x_gp = self.gauss_pt_evaluation_der_x(u)
        u_y_gp = self.gauss_pt_evaluation_der_y(u)
        v_x_gp = self.gauss_pt_evaluation_der_x(v)
        v_y_gp = self.gauss_pt_evaluation_der_y(v)
        p_x_gp = self.gauss_pt_evaluation_der_x(p)
        p_y_gp = self.gauss_pt_evaluation_der_y(p)

        r1_gp = (u_gp * u_x_gp + v_gp * u_y_gp + p_x_gp)**2
        r2_gp = (u_gp * v_x_gp + v_gp * v_y_gp + p_y_gp)**2

        r1_elm_gp = r1_gp * JxW
        r2_elm_gp = r2_gp * JxW

        r1_elm = torch.sum(r1_elm_gp, 1)
        r2_elm = torch.sum(r2_elm_gp, 1)
        r1_total_squared = torch.sum(torch.sum(r1_elm, -1), -1)
        r2_total_squared = torch.sum(torch.sum(r2_elm, -1), -1)
        r_Total = (r1_total_squared + r2_total_squared)**0.5
        div_gp = u_x_gp + v_y_gp
        div_elm_gp = div_gp * JxW
        div_elm = torch.sum(div_elm_gp, 1)
        div_Total = torch.sum(torch.sum(div_elm, -1), -1)
        print(u_gp.shape)
        print(u_x_gp.shape)
        print(r1_gp.shape)
        print(r1_elm_gp.shape)
        print(r1_elm.shape)
        print(r1_total_squared.shape)
        print(r_Total.shape)
        print(div_Total.shape)
        
        # transformation_jacobian = self.gpw.unsqueeze(-1).unsqueeze(-1).unsqueeze(0).type_as(nu_gp)
        # res_elmwise = transformation_jacobian * (nu_gp * (u_x_gp**2 + u_y_gp**2) - (u_gp * f_gp))
        # res_elmwise = torch.sum(res_elmwise, 1) 

        # loss = torch.mean(res_elmwise)
        return r_single_number, torch.sqrt(r1_total_squared), torch.sqrt(r2_total_squared), r_Total, div_Total

case_dir = '/work/mech-ai-scratch/arabeh/residual_calculation/inp' #'./cib/version_1'
query_inp_path = '/work/mech-ai-scratch/arabeh/residual_calculation/inp' #'/work/mech-ai/bkhara/diffnet/examples/ali/inp' # can be any directory containing only the test images, no other files
query_out_path = '/work/mech-ai-scratch/arabeh/residual_calculation/inp' #'/work/mech-ai/bkhara/diffnet/examples/ali/out'
if not os.path.exists(query_out_path):
    os.makedirs(query_out_path)

batch_size = 16
dataset = ImageIMBack(query_inp_path, domain_size=256)
#dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
network = UNet(in_channels=2, out_channels=1)
basecase = Poisson(network, batch_size=batch_size, domain_size=256)

logger = pl.loggers.TensorBoardLogger('.', name="cib")


idir = '/work/mech-ai/rtali/projects/all-neural-operators/TimeDependentNS/LidData_Final_Tensors/512x512'

dataX_list = []
dataY_list = []
fileX_list = ['harmonics_lid_driven_cavity_X.npz', 'nurbs_lid_driven_cavity_X.npz', 'skelneton_lid_driven_cavity_X.npz']
fileY_list = ['harmonics_lid_driven_cavity_Y.npz', 'nurbs_lid_driven_cavity_Y.npz', 'skelneton_lid_driven_cavity_Y.npz']

#print('reading data')
for fileX, fileY in zip(fileX_list, fileY_list):
    print('reading data')
    rdataX = np.load(os.path.join(idir, fileX))['data']
    rdataY = np.load(os.path.join(idir, fileY))['data']
    print('data loaded from files')
    dataX_list.append(rdataX)
    dataY_list.append(rdataY)

#print('data loaded from files')
    
dataX = torch.FloatTensor(np.concatenate(dataX_list, axis=0))
dataY = torch.FloatTensor(np.concatenate(dataY_list, axis=0))
    
fileX = 'lid_driven_cavity_X.npz'
fileY = 'lid_driven_cavity_Y.npz'

# print('reading data')
# rdataX = np.load(os.path.join(idir,fileX))['data']
# rdataY = np.load(os.path.join(idir,fileY))['data']
# print('data loaded from files')
# dataX = torch.FloatTensor(rdataX)
# dataY = torch.FloatTensor(rdataY)

print('res calc')
L = 2
nsample = dataX.shape[0]
nx = dataX.shape[-1]
ny = dataX.shape[-2]
hx = L/nx
hy = L/ny
res = torch.zeros(nsample, 5)
#total_vals = torch.zeros(nsample, 2)
bs = 100
nmb = nsample // bs
# res = nsample % bs
sidx = -bs
fidx = 0
for i in range(nmb+1):
    sidx += bs
    fidx += bs
    if i == nmb:
        fidx = nsample
    print(sidx, fidx)
    r_single_number, r1, r2, rtotal, div = basecase.residual(dataX[sidx:fidx],dataY[sidx:fidx],hx, hy)
    res[sidx:fidx, 0] = r_single_number/(nx*ny)
    res[sidx:fidx, 1] = r1/(nx*ny)
    res[sidx:fidx, 2] = r2/(nx*ny)
    res[sidx:fidx, 3] = rtotal/(nx*ny)
    res[sidx:fidx, 4] = div/(nx*ny)

#np.save('./residuals.npy', res)
res_np = res.numpy()
df = pd.DataFrame(res_np, columns=['Re', 'rx', 'ry', 'rtotal', 'div'])
df.to_csv('residuals_512x512.csv', sep=',', header=True, index=False)
