import dash
from dash import dcc, html, Input, Output
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Initialize Dash app
app = dash.Dash(__name__)

# Load Maneuver Data
maneuver_df = pd.read_csv("Data/ManeuverPlan.csv")
# TODO: Load ManeuverBranchId# files and structure them properly

# Create a decision tree using NetworkX
G = nx.DiGraph()
G.add_edges_from([
    ("Start", "Maneuver 1"),
    ("Maneuver 1", "Maneuver 2A"),
    ("Maneuver 1", "Maneuver 2B"),  # Alternative branch
    ("Maneuver 2A", "Maneuver 3"),
    ("Maneuver 2B", "Maneuver 3"),
])

# Get node positions for plotting
pos = nx.spring_layout(G, seed=42)

# Generate dropdown options
maneuver_options = ["Maneuver 1", "Maneuver 2A", "Maneuver 2B", "Maneuver 3"]

def plot_3d_trajectory(selected_maneuver):
    """Generates a 3D orbit plot for the selected maneuver."""
    fig = go.Figure()
    
    # Generate mock data (Replace with real trajectory data)
    t = np.linspace(0, 2 * np.pi, 100)
    x = np.cos(t) * 300000 + (50000 if "2B" in selected_maneuver else 0)
    y = np.sin(t) * 300000
    z = np.sin(2 * t) * 150000
    
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name=selected_maneuver))
    
    # Add Earth for reference
    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers', marker=dict(size=8, color='green'), name='Earth'))
    
    fig.update_layout(title=f"Orbit Trajectory - {selected_maneuver}", scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
    return fig

# Dash Layout
app.layout = html.Div([
    html.H1("Celestial Choreography Mission Visualization"),
    
    html.Label("Select a Maneuver Path:"),
    dcc.Dropdown(id='maneuver-dropdown', options=[{'label': m, 'value': m} for m in maneuver_options], value='Maneuver 1'),
    
    dcc.Graph(id='trajectory-3d'),
])

# Callback to update plot
@app.callback(
    Output('trajectory-3d', 'figure'),
    Input('maneuver-dropdown', 'value')
)
def update_trajectory(selected_maneuver):
    return plot_3d_trajectory(selected_maneuver)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
