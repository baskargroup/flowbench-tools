import cv2
import numpy as np
import gmsh
import os
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

def generate_mesh_from_image(image_path, output_dir):
    # Step 1: Read the PNG file and extract the contours
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blur to smooth the image
    smoothed_image = gaussian_filter(image, sigma=2.0)

    # Binarize the image
    _, binary_image = cv2.threshold(smoothed_image, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the main contour (assume the largest contour is the shape we want)
    contour = max(contours, key=cv2.contourArea)

    # Normalize the contour points to fit within the square [0, 1] x [0, 1] and preserve the orientation
    contour = contour.astype(np.float32)
    x_min, y_min = contour.min(axis=0)[0]
    x_max, y_max = contour.max(axis=0)[0]
    contour[:, 0, 0] = (contour[:, 0, 0] - x_min) / (x_max - x_min)
    contour[:, 0, 1] = 1 - (contour[:, 0, 1] - y_min) / (y_max - y_min)  # Flip y-axis to preserve orientation

    # Step 2: Initialize Gmsh
    gmsh.initialize()
    gmsh.model.add("mesh_from_image")

    # Convert contour to Gmsh points with normalized coordinates
    points = []
    for i, pt in enumerate(contour):
        x, y = pt[0]
        points.append(gmsh.model.geo.addPoint(x, y, 0))

    # Create lines between points to form the shape
    lines = []
    for i in range(len(points)):
        start = points[i]
        end = points[(i + 1) % len(points)]
        lines.append(gmsh.model.geo.addLine(start, end))

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

    # Ensure the output directory exists
    #os.makedirs(output_dir, exist_ok=True)

    # Construct the mesh file path using the output directory
    base_name = os.path.basename(image_path).replace('.png', '')
    mesh_file_path = os.path.join(output_dir, f"{base_name}.msh")
    gmsh.write(mesh_file_path)
    
    # Save the coordinates in a compressed numpy file
    np.savez_compressed(mesh_file_path.replace('.msh', '.npz'), x=contour[:, 0, 0], y=contour[:, 0, 1])

    # Step 4: Visualize the mesh
    #gmsh.fltk.run()

    # Construct the absolute file path for saving the PNG file
    png_file_path = os.path.join(output_dir, f"{base_name}.png")

    # Close the contour loop by adding the first point to the end of the contour
    closed_contour = np.vstack([contour, contour[0][np.newaxis, ...]])
    # Plotting the curve using matplotlib
    plt.figure()
    plt.plot(closed_contour[:, 0, 0], closed_contour[:, 0, 1], '-b')
    plt.axis('equal')
    plt.title('Generated Curve')
    plt.savefig(png_file_path)
    plt.close()


    # Create a view and save it as an image
    #gmsh.fltk.run()
    #gmsh.option.setNumber("General.Graphics", 1)  # Ensure graphics are enabled
    #gmsh.write(f"{os.path.join(output_dir, base_name)}.png")  # Save the mesh as an image file
    #gmsh.fltk.finalize()

    # Finalize Gmsh
    gmsh.finalize()


# Example usage
#generate_mesh_from_image('PNGtoMSH/butterfly-1.png')
