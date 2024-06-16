import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from geomdl import BSpline
import gmsh

# Function to generate polygon from control points using NURBS
def NURBStoMSH(coreset_path, directory, index = 1):
    
    
    # Load the coreset_curve.npy file with allow_pickle=True
    coreset = np.load(coreset_path)
    curve_index = index - 1
    
    # Select one curve to plot (e.g., the first curve)
    control_pts = coreset[curve_index]
    
    
    knotvec = [0, 0, 0, 0.14285714, 0.28571429, 0.42857143, 0.57142857, 0.71428571, 0.85714286, 1, 1, 1]
    delta = 0.007


    # Create a 3-dimensional B-spline Curve
    curve = BSpline.Curve()
    curve.degree = 2

    # Extend control points to 3D by adding a zero for the z-coordinate
    control_pts_3d = np.hstack([control_pts, np.zeros((control_pts.shape[0], 1))])
    curve.ctrlpts = control_pts_3d.tolist()

    curve.knotvector = knotvec
    curve.delta = delta
    eval_pts = curve.evalpts

    # Convert the evaluated points to 2D by dropping the z-coordinate
    eval_pts_2d = np.array(eval_pts)[:, :2]

    # Normalize the points to fit within [0, 1] x [0, 1]
    x_min, y_min = eval_pts_2d.min(axis=0)
    x_max, y_max = eval_pts_2d.max(axis=0)
    eval_pts_2d[:, 0] = (eval_pts_2d[:, 0] - x_min) / (x_max - x_min)
    eval_pts_2d[:, 1] = (eval_pts_2d[:, 1] - y_min) / (y_max - y_min)
    
    
    # Visualization
    plt.figure(figsize=(5, 5))
    plt.gca().add_patch(Polygon(eval_pts_2d, edgecolor='red', fill=None, linewidth=2))
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.title(f'Nurbs - Sample {index}')
    fig_file_path = file_path = f"{directory}/case_{index}.png"
    plt.savefig(fig_file_path)
    # plt.show()
    

    # Extract x and y coordinates
    x = eval_pts_2d[:, 0]
    y = eval_pts_2d[:, 1]


    gmsh.initialize()
    gmsh.model.add("curve_mesh")


    # Create points
    points = []
    for xi, yi in zip(x, y):
        points.append(gmsh.model.geo.addPoint(xi, yi, 0, meshSize=0.1))

    # Create lines
    lines = []
    num_points = len(points)
    for i in range(num_points-1):
        lines.append(gmsh.model.geo.addLine(points[i], points[(i + 1)]))


    # Create a curve loop and a plane surface
    curve_loop = gmsh.model.geo.addCurveLoop(lines)
    plane_surface = gmsh.model.geo.addPlaneSurface([curve_loop])

    # Synchronize and mesh
    gmsh.model.geo.synchronize()

    # Set the option for recombining triangles into quadrilaterals (optional)
    # gmsh.option.setNumber('Mesh.RecombineAll', 1)
    # gmsh.option.setNumber('Mesh.Algorithm', 8)  # Use the mesh algorithm that supports recombination

    gmsh.model.mesh.generate(1)  # Generate 1D mesh elements along curves
    # gmsh.model.mesh.generate(2)  # Generate 2D mesh, now with quadrilaterals

    # Set mesh format to MSH4
    gmsh.option.setNumber("Mesh.MshFileVersion", 4.1)
    gmsh.option.setNumber("Mesh.Format", 0)  # Set to 0 for ASCII format

    # # Save the mesh to a file with the same name but .msh extension
    mesh_file_path = file_path = f"{directory}/case_{index}.msh"
    gmsh.write(mesh_file_path)

    # # Save the coordinates in a compressed numpy file
    np.savez_compressed(mesh_file_path.replace('.msh', '.npz'), x=x, y=y)

    # Step 4: Visualize the mesh
    #gmsh.fltk.run()

    # Finalize Gmsh
    gmsh.finalize()
    

