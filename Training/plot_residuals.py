import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the residuals data from the CSV file
residuals_df = pd.read_csv('residuals_128x128.csv')

# Extract the necessary columns
rtotal = residuals_df['rtotal']
div = residuals_df['div']

# Calculate the logarithm base 10 of the absolute values
log_rtotal = np.log10(np.abs(rtotal))
log_div = np.log10(np.abs(div))

# Create the histogram plot for log_rtotal
plt.figure(figsize=(10, 6))
plt.hist(log_rtotal, bins=30, alpha=0.75)
# Add labels and title
plt.xlabel('log10(|Residual|)')
plt.ylabel('Frequency')
plt.title('Histogram of Log10 of Absolute Average Residuals')
# Save the plot as a PNG and PDF file
plt.grid(True)
plt.savefig('log10_residuals_histogram_128x128.png', format='png')

# Create the histogram plot for log_div
plt.figure(figsize=(10, 6))
plt.hist(log_div, bins=30, alpha=0.75)
# Add labels and title
plt.xlabel('log10(|Continuity|)')
plt.ylabel('Frequency')
plt.title('Histogram of Log10 of Absolute Average Continuity')
# Save the plot as a PNG and PDF file
plt.grid(True)
plt.savefig('log10_divergence_histogram_128x128.png', format='png')

