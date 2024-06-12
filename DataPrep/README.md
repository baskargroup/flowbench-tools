# Dataset Preparation Script

## Overview
We provide a script for each family of our datasets. This prepares the final tensors that can be fed into a SciML model. They are enumerated as follows:

- 2D LDC - NS - ldc2dns.py
- 2D LDC - NS+HT [Constant Reynolds] - ldc2dnsht-constRe.py
- 2D LDC - NS+HT [Variable Reynolds] - ldc2dnsht-varRe.py
- 2D FPO - NS - fpo2d.py
- 3D LDC - NS - ldc3dns.py

For a glossary of abbreviations, please refer to Table - 5 in the appendix to our main paper.

## Features

-  For the LDC family of datasets, we generate the steady state solutions. Users obtain the input and output tensors with the following formats

	- 2D LDC - NS - ldc2dns.py - e.g., ```X[3000][Re,g,s][512][512] , Y[3000][u,v,p,C][512][512]```. Refer to Table 1 in our supplementary for details about C.
	- 2D LDC - NS+HT [Constant Reynolds] - ldc2dnsht-constRe.py - e.g., ```X[2990][Gr,g,s][512][512] , Y[2990][u,v,p,theta,C*][512][512]```. Refer to Table 1 in our supplementary for details about C*.
	- 2D LDC - NS+HT [Variable Reynolds] - ldc2dnsht-varRe.py - e.g., ```X[3000][Ri, Re, g, s][512][512] , Y[3000][u,v,p,theta,C*][512][512]```. Refer to Table 1 in our supplementary for details about C*.
	- 2D FPO - NS - fpo2d.py - e.g., ```Y[1150][u,v,p][t1...t240][512][128]```.
	- 3D LDC - NS - ldc3dns.py - e.g., ```X[500][Re,g,s][128][128][128] , Y[500][u,v,p][128][128][128]```.

## Requirements

- Python 3.9+.
- Required libraries : numpy, pandas.
- Additional Constants Files are required for some cases. These are provided in our data store. They are as follows:
	- ldc2dns.py - ```HARMONICS_2D_NS.txt, NURBS_2D_NS.txt SKELNETON_2D_NS.txt```.
	- ldc2dnsht-constRe.py - ```HARMONICS_2D_NS.txt, NURBS_2D_NS.txt SKELNETON_2D_NS.txt```.
	- ldc2dnsht-varRe.py - ```HARMONICS_2D_NS.txt, NURBS_2D_NS.txt SKELNETON_2D_NS.txt```.

- The constants files are different for each case and are used to obtain dimensionless numbers [Cd,Cl,Nu] for the respective cases.

## Usage

- Each Script necessitates that the user provide the following:
	- Path to the downsampled files. Please refer to the directory ```Downsampling``` for detailed instructions.
	- Desired Output Resolution (One of 128, 256 or 512)
	- Full path of the desired X and Y tensors outputs.
	- Full path of the constants file. We have one constants file per geometry type and problem type. This is not dependent on the output resolution desired.
	- Full path to the input geometries folder. Note, we have three geometries (100 cases each) at three resolutions each. Please match geometry type and resolution.
	- Note that these values will have to be edited in the respective script itself before executing the next steps. The relevant variable names associated with the above settings are self explanatory.
	- Note that the FPO is a transient problem. We fit a Seq to Seq model. Hence the geometry is irrelevant for the problem.

- To execute run the following commands
	- ```python3 ldc2dns.py```
	- ```python3 ldc2dnsht-constRe.py```  
	- ```python3 ldc2dnsht-varRe.py```
	- ```python3 fpo2d.py t_start_in t_end_in t_start_out t_end_out ```
	- ```python3 ldc3dns.py```


