import matplotlib.pyplot as plt
import numpy as np
import os

def plot_ldc_like(y, y_hat, idx, plot_path):
    plot_dir = os.path.dirname(plot_path)
    os.makedirs(plot_dir, exist_ok=True)
    
    # Create the 3x3 grid of plots with specified aspect ratio and size
    fig, axs = plt.subplots(3, 3, figsize=(9, 9), subplot_kw={'aspect': 'auto'}, sharex=True, sharey=True, squeeze=True)
    
    # Remove x and y ticks for all subplots
    for ax_row in axs:
        for ax in ax_row:
            ax.set_xticks([])
            ax.set_yticks([])  

    # Plot the ground truth
    im0 = axs[0, 0].imshow(y[idx][0], cmap='jet', origin='lower')
    axs[0, 0].set_title('u')
    
    im1 = axs[0, 1].imshow(y[idx][1], cmap='jet', origin='lower')
    axs[0, 1].set_title('v')
    
    im2 = axs[0, 2].imshow(y[idx][2], cmap='jet', origin='lower')
    axs[0, 2].set_title('p')
    
    # Plot the prediction
    im3 = axs[1, 0].imshow(y_hat[idx][0], cmap='jet', origin='lower')
    axs[1, 0].set_title('u predicted')
    
    im4 = axs[1, 1].imshow(y_hat[idx][1], cmap='jet', origin='lower')
    axs[1, 1].set_title('v predicted')
    
    im5 = axs[1, 2].imshow(y_hat[idx][2], cmap='jet', origin='lower')
    axs[1, 2].set_title('p predicted')
    
    # Plot the error
    im6 = axs[2, 0].imshow(np.abs(y[idx][0] - y_hat[idx][0]), cmap='jet', origin='lower')
    axs[2, 0].set_title('u error')
    
    im7 = axs[2, 1].imshow(np.abs(y[idx][1] - y_hat[idx][1]), cmap='jet', origin='lower')
    axs[2, 1].set_title('v error')
    
    im8 = axs[2, 2].imshow(np.abs(y[idx][2] - y_hat[idx][2]), cmap='jet', origin='lower')
    axs[2, 2].set_title('p error')
    
    # Create a common colorbar at the bottom
    
    cbar_ax = fig.add_axes([1.01, 0.15, 0.05, 0.7])  # Add colorbar axis outside the subplots
    cbar = fig.colorbar(im0, cax=cbar_ax)
    cbar_ticks = np.linspace(cbar.vmin, cbar.vmax, num=5)  # Adjust the number of ticks as needed
    cbar.set_ticks(cbar_ticks)

    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    fig.subplots_adjust(wspace=0.1, hspace=0.3)

    # Save the plot
    plt.savefig(plot_path, bbox_inches='tight')
    #plt.show()
    
    # Close the plot
    plt.close()