# Dataset Preparation Script

## Overview
We provide a script for each family of our datasets. This prepares the final tensors that can be fed into a SciML model. They are enumerated as follows:

- 2D LDC - NS - ldc2dns.py
- 2D LDC - NS+HT [Constant Reynolds] - ldc2dnsht-constRe.py
- 2D LDC - NS+HT [Variable Reynolds] - ldc2dnsht-varRe.py
- 2D FPO - NS - ldc2dfpo.py
- 3D LDC - NS - ldc3dns.py

For a glossary of abbreviations, please refer to Table - 5 in the appendix to our main paper.

## Features

-  For the LDC family of datasets, we generate the steady state solutions. Users obtain the input and output tensors with the following formats

	- 2D LDC - NS - ldc2dns.py - e.g., ```X[3000][Re,g,s][512][512] , Y[3000][u,v,p,C][512][512]```. Refer to Table 1 in our supplementary for details about C.
	- 2D LDC - NS+HT [Constant Reynolds] - ldc2dnsht-constRe.py - e.g., ```X[2990][Gr,g,s][512][512] , Y[2990][u,v,p,theta,C*][512][512]```. Refer to Table 1 in our supplementary for details about C*.
	- 2D LDC - NS+HT [Variable Reynolds] - ldc2dnsht-varRe.py - e.g., ```X[3000][Ri, Re, g, s][512][512] , Y[3000][u,v,p,theta,C*][512][512]```. Refer to Table 1 in our supplementary for details about C*.
	- 2D FPO - NS - ldc2dfpo.py - e.g., ```X[1150][Re,g,s][512][512] , Y[1150][u,v,p][512][512]```.
	- 3D LDC - NS - ldc3dns.py - e.g., ```X[500][Re,g,s][128][128][128] , Y[500][u,v,p][128][128][128]```.

## Requirements

- Python 3.9+.
- Required libraries : numpy, pandas.
- Additional Constants Files are required for some cases. These are provided in our data store. They are as follows:
	- ldc2dns.py - ```HARMONICS\_2D\_NS.txt, NURBS\_2D\_NS.txt SKELNETON\_2D\_NS.txt```.
	- ldc2dnsht-constRe.py - ```HARMONICS\_2D\_NS.txt, NURBS\_2D\_NS.txt SKELNETON\_2D\_NS.txt```.
	- ldc2dnsht-varRe.py - ```HARMONICS\_2D\_NS.txt, NURBS\_2D\_NS.txt SKELNETON\_2D\_NS.txt```.

- The constants files are different for each case and are used to obtain dimensionless numbers [Cd,Cl,Nu] for the respective cases.

## Usage
-  


