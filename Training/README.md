# ML Training

## Overview

This directory provides a comprehensive list of ML training scripts that can be used to train FNO and CNO models on our data. In this repo, we provide the code to fit models for the steady state problems, i.e., given an input tensor comprising of the tuple e.g., [Re,g,s] for a LDC problem, we predict the steady solution [u,v,p,Cd+Cl]. This repository contains the full code for such steady state experiments. Fitting to transient problems involves a small change in the data preparation process. Essentially, we pose the space-time problem as a Seq. to Seq. Problem i.e., we feed a series (over a fixed set of time steps) of time steps of all field variables as an input and receive as output another set of time steps the same field variables. Therefore, in the data prep process, we first preparare a tensor e.g., of the form [samples][time][u,v,p,Cd+Cl][128][128] and then flatten the time dimension. This means the number of channels [u,v,p,Cd+Cl] get each multiplied with the number of input and output time steps respectively. 

## Features

- End to end code. Outputs various MSE statistics on a validation dataset and plots representing the quality of fit.

## Requirements

- ```pip install requirements.txt```

## Usage
- Have the input and output tensors ready.
- Under ```experiments``` directory, create a model specific directory e.g., ```cno_1``` or ```fno_1```. Within this second directory create a config file called ```config.yaml```. Follow the example we have provided in this repo.
- Adjust the following settings as required in the config file, if using CNO:

	- model: "cno"
	- file_path_x: ''
	- file_path_y: ''
	- batch_size: 5
	- split_fraction: 0.8
	- in_dim: 20
	- out_dim: 5
	- N_layers: 4
	- in_size: 512
	- out_size: 512
	- learning_rate: 0.001
	- num_epochs: 200
	- checkpoint_frequency: 50

- Adjust the the following settings as required in the config file, if using FNO:

	- model: "fno"
	- file_path_x: ''
	- file_path_y: ''
	- batch_size: 5
	- split_fraction: 0.8
	- n_modes:
  		- 32
  		- 32
	- n_layers: 5
	- in_channels: 20
	- out_channels: 5
	- hidden_channels: 32
	- projection_channels: 128
	- learning_rate: 0.001
	- num_epochs: 200
	- checkpoint_frequency: 50

- Run the script ```script.sh``` on a HPC server
- Training Results will be stored in a ```.out``` file.
- To output validation metrics per field and an overall error plot, run ```Validation.ipynb```. Detailed instructions in the file
- We provide an additional metric that calculates the numerical residuals of the fields and to get an estimate of the quality of the solution plots a histogram of the residuals over the entire field. Please run ```calc_residuals.py``` followed by ```plot_residuals.py```.
