import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load RPO data
rpo_df = pd.read_csv("data/RpoPlan.csv")  # Update with actual path

# Extract relevant columns
time = rpo_df["secondsSinceStart"]
chief_x, chief_y, chief_z = rpo_df["positionChiefEciX"], rpo_df["positionChiefEciY"], rpo_df["positionChiefEciZ"]
deputy_x, deputy_y, deputy_z = rpo_df["positionDeputyEciX"], rpo_df["positionDeputyEciY"], rpo_df["positionDeputyEciZ"]

# Create 3D Plot
fig = go.Figure()

# Add Chief (RSO) orbit trace
fig.add_trace(go.Scatter3d(
    x=chief_x, y=chief_y, z=chief_z,
    mode="lines",
    line=dict(color="blue", width=2),
    name="Chief (RSO)"
))

# Add Deputy (Chaser) orbit trace
fig.add_trace(go.Scatter3d(
    x=deputy_x, y=deputy_y, z=deputy_z,
    mode="lines",
    line=dict(color="red", width=2),
    name="Deputy (Chaser)"
))

# Add Earth (approximate)
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode="markers",
    marker=dict(size=8, color="green"),
    name="Earth"
))

# Configure layout
fig.update_layout(
    title="3D Orbit Visualization (ECI Frame)",
    scene=dict(
        xaxis_title="X (km)",
        yaxis_title="Y (km)",
        zaxis_title="Z (km)"
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

# Show plot
fig.show()
