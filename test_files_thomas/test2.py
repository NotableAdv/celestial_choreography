import plotly.graph_objects as go
import numpy as np

theta = np.linspace(0, 2*np.pi, 100)
x = np.cos(theta)
y = np.sin(theta)
z = np.sin(2 * theta)

fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='lines', name='Orbit Path')])
fig.update_layout(title="3D Orbit Visualization", scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"))
fig.show()
