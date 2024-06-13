import numpy as np
import gmsh
import random
import matplotlib.pyplot as plt

def generate_mesh(H, output_filename, x0 = 0, y0 = 0, seed=None):
    
    # Set the random seed for reproducibility
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    
    H = random.randint(8, 15)
    
    # Coefficients for the radial function with reduced amplitude
    a = np.random.randn(H) * 0.02  # Smaller coefficients for cosine terms
    b = np.random.randn(H) * 0.02  # Smaller coefficients for sine terms

    np.random.shuffle(a)  # Shuffle the array 'a' in-place
    np.random.shuffle(b)  # Shuffle the array 'b' in-place

    # More sampling points for smoother curve
    t = np.linspace(0, 2 * np.pi, 500)

    # Initialize radial function
    r = np.zeros_like(t) + 0.5  # Start with a base radius to avoid too sharp changes

    # Construct radial function using harmonics
    for h in range(1, H+1):
        r += a[h-1] * np.cos(h * t) + b[h-1] * np.sin(h * t)

    # Normalize to ensure no self-intersecting shapes
    r /= np.abs(r).max() / 0.5

    # Reconstruct x(t), y(t) from r(t)
    x = r * np.cos(t)
    y = r * np.sin(t)

    gmsh.initialize()
    gmsh.model.add("curve_mesh")
    

    # Create points
    points = []
    for xi, yi in zip(x, y):
        points.append(gmsh.model.geo.addPoint(xi + x0, yi + y0, 0, meshSize=0.1))

    # Create lines
    lines = []
    num_points = len(points)
    for i in range(num_points-1):
        lines.append(gmsh.model.geo.addLine(points[i], points[(i + 1)]))

    # Create Curve Loop and Plane Surface
    # curve_loop = gmsh.model.geo.addCurveLoop(lines)
    # plane_surface = gmsh.model.geo.addPlaneSurface([curve_loop])

    # # Adding Physical Groups
    # curve_group = gmsh.model.addPhysicalGroup(1, lines)
    # surface_group = gmsh.model.addPhysicalGroup(2, [plane_surface])

    # # Set names for physical groups (optional but helpful for identifying in solvers)
    # gmsh.model.setPhysicalName(1, curve_group, "OuterBoundary")
    # gmsh.model.setPhysicalName(2, surface_group, "MainSurface")

    # Synchronize and mesh
    gmsh.model.geo.synchronize()

    # Set the option for recombining triangles into quadrilaterals
    # gmsh.option.setNumber('Mesh.RecombineAll', 1)
    # gmsh.option.setNumber('Mesh.Algorithm', 8)  # Use the mesh algorithm that supports recombination

    gmsh.model.mesh.generate(1)  # Generate 1D mesh elements along curves
    # gmsh.model.mesh.generate(2)  # Generate 2D mesh, now with quadrilaterals

    # Set mesh format to MSH4
    gmsh.option.setNumber("Mesh.MshFileVersion", 4.1)
    gmsh.option.setNumber("Mesh.Format", 0)  # Set to 0 for ASCII format

    # Optional: Save and visualize mesh
    gmsh.write(output_filename)
    
    
    # Plotting the curve using matplotlib
    plt.figure(figsize=(6,6))
    plt.plot(x, y, '-b')
    plt.axis('equal')
    plt.title('Generated Curve')
    plt.grid(True)
    plt.savefig(output_filename.replace('.msh', '.png'))
    plt.close()
    
    
   # Save the coordinates in a compressed numpy file
    np.savez_compressed(output_filename.replace('.msh', '.npz'), x=x, y=y)
    
    # gmsh.fltk.run()

    gmsh.finalize()

# Generate mesh
# output_filename = 'arbitrary_mesh_simple.msh'
# generate_mesh(10, output_filename, 1.0, 1.0)
