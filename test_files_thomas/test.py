import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define orbital parameters (Example: Circular orbit)
num_points = 500
theta = np.linspace(0, 2 * np.pi, num_points)  # Angle around the orbit

# Define Chief (Target) Orbit
r_chief = 7000  # Radius in km
x_chief = r_chief * np.cos(theta)
y_chief = r_chief * np.sin(theta)
z_chief = np.zeros(num_points)  # Assuming equatorial orbit

# Define Deputy (Chaser) Orbit (Slightly different altitude)
r_deputy = 7050
x_deputy = r_deputy * np.cos(theta)
y_deputy = r_deputy * np.sin(theta)
z_deputy = np.zeros(num_points)

# Plot in 3D
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot(x_chief, y_chief, z_chief, label="Chief (RSO)", color="blue")
ax.plot(x_deputy, y_deputy, z_deputy, label="Deputy (Chaser)", color="red")

# Earth for reference
ax.scatter(0, 0, 0, color="green", marker="o", label="Earth")

ax.set_xlabel("X (km)")
ax.set_ylabel("Y (km)")
ax.set_zlabel("Z (km)")
ax.set_title("Satellite Orbits in 3D")
ax.legend()

plt.show()