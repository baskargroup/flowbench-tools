# FlowBench 

This is the repository for the [FlowBench](https://baskargroup.bitbucket.io/). It contains the link to the full dataset and the code used for training the SciML operators. Additionally, we include a collection of scripts for preparing data into machine learning format and downsampling data into lower resolution.

<!-- [Model](https://huggingface.co/imageomics/bioclip) | [Data](https://huggingface.co/datasets/imageomics/TreeOfLife-10M) | [Website](https://huggingface.co/datasets/imageomics/TreeOfLife-10M)
--- -->

FlowBench is an extensive flow dataset which contains over 10,000 data samples of a fully resolved numerical simulation for modeling transport phenomena in complex geometries. FlowBench will facilitate the evaluation of the interplay between complex geometry, coupled flow phenomena, and data sufficiency on the performance of current and future neural PDE solvers.


## Table of Contents

1. [Model](#model)
2. [Data](#data)
3. [Website](#website)
<!-- 4. [Citation](#citation) -->

## Model

We include workflows to train three types of neural operators: Fourier Neural Operators (FNO), Convolutional Neural Operators (CNO), and Deep Operator Networks (DeepONets). The implementation of the three networks are included here.

## Data

FlowBench offers over 10,000 solutions for flow around complex geometries in both 2D and 3D. Simulation include fluid flow and thermal flow scenarios, and our solutions are available as either single snapshots or time sequences, addressing both steady-state and time-dependent scenarios. The [dataset](https://figshare.com/s/15e9d23790d0a14e8f71) is provided at three different resolutions and includes essential features like a geometry mask and a signed distance field. It is specifically designed to support the development of next-generation scientific machine learning (SciML) neural PDE solvers, particularly those tackling complex geometries and multiphysics phenomena.


<h2> Website </h2>

We have a [project website](https://baskargroup.bitbucket.io/) which highlights FlowBench main results. Our website gives an overview of our dataset, geometries, solver, and our research team that worked on this project.


<!-- ## Citation

Our paper:

```
@inproceedings{stevens2024bioclip,
  title = {{B}io{CLIP}: A Vision Foundation Model for the Tree of Life}, 
  author = {Samuel Stevens and Jiaman Wu and Matthew J Thompson and Elizabeth G Campolongo and Chan Hee Song and David Edward Carlyn and Li Dong and Wasila M Dahdul and Charles Stewart and Tanya Berger-Wolf and Wei-Lun Chao and Yu Su},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year = {2024}
}
```

Our code (this repository):
```
@software{bioclip2023code,
  author = {Samuel Stevens and Jiaman Wu and Matthew J. Thompson and Elizabeth G. Campolongo and Chan Hee Song and David Edward Carlyn},
  doi = {10.5281/zenodo.10895871},
  title = {BioCLIP},
  version = {v1.0.0},
  year = {2024}
}
```


Also consider citing OpenCLIP, iNat21 and BIOSCAN-1M:

```
@software{ilharco_gabriel_2021_5143773,
  author={Ilharco, Gabriel and Wortsman, Mitchell and Wightman, Ross and Gordon, Cade and Carlini, Nicholas and Taori, Rohan and Dave, Achal and Shankar, Vaishaal and Namkoong, Hongseok and Miller, John and Hajishirzi, Hannaneh and Farhadi, Ali and Schmidt, Ludwig},
  title={OpenCLIP},
  year={2021},
  doi={10.5281/zenodo.5143773},
}
```

```
@misc{inat2021,
  author={Van Horn, Grant and Mac Aodha, Oisin},
  title={iNat Challenge 2021 - FGVC8},
  publisher={Kaggle},
  year={2021},
  url={https://kaggle.com/competitions/inaturalist-2021}
}
```

```
@inproceedings{gharaee2023step,
  author={Gharaee, Z. and Gong, Z. and Pellegrino, N. and Zarubiieva, I. and Haurum, J. B. and Lowe, S. C. and McKeown, J. T. A. and Ho, C. Y. and McLeod, J. and Wei, Y. C. and Agda, J. and Ratnasingham, S. and Steinke, D. and Chang, A. X. and Taylor, G. W. and Fieguth, P.},
  title={A Step Towards Worldwide Biodiversity Assessment: The {BIOSCAN-1M} Insect Dataset},
  booktitle={Advances in Neural Information Processing Systems ({NeurIPS}) Datasets \& Benchmarks Track},
  year={2023},
}
``` -->
