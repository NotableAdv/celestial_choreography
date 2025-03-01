import plotly.graph_objects as go
import numpy as np

# Define orbital parameters
num_points = 500
theta = np.linspace(0, 2 * np.pi, num_points)

# Define Chief (Target) Orbit
r_chief = 7000
x_chief = r_chief * np.cos(theta)
y_chief = r_chief * np.sin(theta)
z_chief = np.zeros(num_points)

# Define Deputy (Chaser) Orbit (Slightly different altitude)
r_deputy = 7050
x_deputy = r_deputy * np.cos(theta)
y_deputy = r_deputy * np.sin(theta)
z_deputy = np.zeros(num_points)

# Create 3D figure
fig = go.Figure()

# Add Chief orbit
fig.add_trace(go.Scatter3d(x=x_chief, y=y_chief, z=z_chief, mode='lines', name='Chief (RSO)', line=dict(color='blue')))

# Add Deputy orbit
fig.add_trace(go.Scatter3d(x=x_deputy, y=y_deputy, z=z_deputy, mode='lines', name='Deputy (Chaser)', line=dict(color='red')))

# Add Earth
fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers', marker=dict(size=8, color='green'), name='Earth'))

fig.update_layout(title="Satellite Orbits in 3D", scene=dict(xaxis_title='X (km)', yaxis_title='Y (km)', zaxis_title='Z (km)'))

fig.show()
