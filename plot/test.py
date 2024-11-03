import matplotlib.pyplot as plt
import numpy as np

# Initialize the plot
plt.figure()
plt.title("Color Gradient Along X-Axis")

# Generate x and y data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Function to get color based on x-coordinate
def get_color(x_val):
    # Example: Color varies from blue to red along x-axis
    return (x_val / 10, 0, 1 - x_val / 10)

# Plot each segment with a color that depends on its x-coordinate
for i in range(len(x) - 1):
    x_segment = x[i:i+2]
    y_segment = y[i:i+2]
    plt.plot(x_segment, y_segment, color=get_color(x[i]))

plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.savefig("incremental_lines_plot.png")