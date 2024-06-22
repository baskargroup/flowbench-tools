# Geometry Creation

## Overview
In this section you can find scripts which have been used to automate the generation of configuration files for the Dendrite framework to simulate LDC/FPO problems with various geometries and parameters. It processes STL files, generates random Reynolds numbers using a Sobol sequence, and organizes the output into structured directories with appropriate configurations.

## Geometries

Our dataset includes three distinct categories of geometries. Below is a description of these geometries.

### Parametric NURBS Shapes:
The first set of geometries consists of parametric shapes generated using Non-Uniform Rational B-Splines (NURBS) curves. We use a uniform knot vector with a second-order (quadratic) basis function, which remains fixed. However, the positions of eight control points are randomly varied to produce a variety of curves. All shapes are normalized to fit within the unit hypercube. We provide the code and the control points to recreate these geometries in the Nurbs folder. 

### Parametric Spherical Harmonics Shapes:
The next set of geometries consists of parametric shapes generated using spherical harmonics. We randomly select 8 to 15 harmonics with amplitudes ranging from 0 to 0.2. All shapes are normalized to fit within the unit hypercube. We provide the code to recreate these geometries in the Harmonics folder. 

### Non-Parametric SkelNetOn Shapes:
The last set of geometries consist of non-parametric shapes sampled from the grayscale dataset in SkelNetOn. We apply a Gaussian blur filter with a scale of 2 to smoothen out some of the thin features of the object. All shapes are normalized to fit within the unit hypercube. We provide the code and the control points to recreate these geometries in the Skelneton folder. 

### 3D Geometries:
For the 3D geometries, we selected 50 shapes of ellipsoids and rings, normalized to fit within the unit hypercube. The ellipsoids have varying ratios of major to minor axis lengths, and the rings have different ratios of inner to outer radius lengths. The STL files of these geometries are provided in the 3D_LDC folder.
