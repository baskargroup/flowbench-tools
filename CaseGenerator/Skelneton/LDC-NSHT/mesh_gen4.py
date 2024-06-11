import numpy as np
import gmsh
import matplotlib.pyplot as plt

def generate_ellipse_mesh(a_over_b, output_filename='ellipse_mesh.msh', x0=1, y0=1):
    gmsh.initialize()
    gmsh.model.add("ellipse_mesh")


    # Bounding box constraints
    max_width = 1.0  # Width of the bounding box
    max_height = 1.0  # Height of the bounding box

    # Ellipse parameters
    if a_over_b >= 1:
        a = max_width / 2  # semi-major axis
        b = a / a_over_b  # semi-minor axis adjusted according to a/b ratio
    else:
        b = max_height / 2
        a = b * a_over_b  # Adjust semi-major axis based on the aspect ratio

    # Generate points on the ellipse
    t = np.linspace(0, 2 * np.pi, 800, endpoint=False)  # parametric angle
    x = x0 + a * np.cos(t)
    y = y0 + b * np.sin(t)

    # Create points in Gmsh
    points = []
    for xi, yi in zip(x, y):
        points.append(gmsh.model.geo.addPoint(xi, yi, 0))

    # Create lines between points
    lines = []
    num_points = len(points)
    for i in range(num_points):
        lines.append(gmsh.model.geo.addLine(points[i], points[(i + 1) % num_points]))




    # Synchronize and mesh
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(1)
    
    
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

# Example usage
# output_filename='ellipse_mesh.msh'
# a_over_b = 0.14 # Aspect ratio of ellipse, change this value as needed
# generate_ellipse_mesh(a_over_b,output_filename)
