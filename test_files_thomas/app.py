import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

# Load RPO data
rpo_df = pd.read_csv("data/RpoPlan.csv")

# Extract positions
chief_x, chief_y, chief_z = rpo_df["positionChiefEciX"], rpo_df["positionChiefEciY"], rpo_df["positionChiefEciZ"]
deputy_x, deputy_y, deputy_z = rpo_df["positionDeputyEciX"], rpo_df["positionDeputyEciY"], rpo_df["positionDeputyEciZ"]

# Create 3D Plot
fig = go.Figure()
fig.add_trace(go.Scatter3d(x=chief_x, y=chief_y, z=chief_z, mode="lines", name="Chief (RSO)", line=dict(color="blue")))
fig.add_trace(go.Scatter3d(x=deputy_x, y=deputy_y, z=deputy_z, mode="lines", name="Deputy (Chaser)", line=dict(color="red")))
fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode="markers", marker=dict(size=8, color="green"), name="Earth"))

# Initialize Dash App
app = dash.Dash(__name__)

# Define Layout
app.layout = html.Div([
    html.H1("Celestial Choreography Dashboard"),
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
