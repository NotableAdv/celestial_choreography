import pandas as pd
import plotly.graph_objects as go
import os
from dash import Dash, dcc, html, Input, Output

# Define directory for maneuver files
DATA_DIR = "Data"

# Load the main maneuver plan
maneuver_plan_path = os.path.join(DATA_DIR, "ManeuverPlan.csv")
maneuver_plan = pd.read_csv(maneuver_plan_path)

# Find all maneuver branch files dynamically
branch_files = [f for f in os.listdir(DATA_DIR) if f.startswith("ManeuverBranchId") and f.endswith(".csv")]
branch_files.sort()

# Create dropdown options based on available files
dropdown_options = [{"label": "Main Maneuver Plan", "value": "main"}]
dropdown_options += [{"label": f"Branch {f.split('ManeuverBranchId')[1].split('.')[0]}", "value": f} for f in branch_files]

# Initialize Dash App
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Maneuver Plan & Branching Paths"),

    dcc.Graph(id="maneuver-plot"),

    # Dropdown for selecting maneuver branches
    dcc.Dropdown(
        id="branch-selector",
        options=dropdown_options,
        value="main",
        clearable=False
    )
])

@app.callback(
    Output("maneuver-plot", "figure"),
    Input("branch-selector", "value")
)
def update_plot(selected_branch):
    fig = go.Figure()

    # Load the main maneuver trajectory
    main_x, main_y, main_z = maneuver_plan["x"], maneuver_plan["y"], maneuver_plan["z"]
    fig.add_trace(go.Scatter3d(
        x=main_x, y=main_y, z=main_z,
        mode='lines',
        name='Main Maneuver Plan',
        line=dict(color='blue', width=2)
    ))

    if selected_branch != "main":
        # Load the selected maneuver branch file
        branch_path = os.path.join(DATA_DIR, selected_branch)
        maneuver_branch = pd.read_csv(branch_path)

        branch_x, branch_y, branch_z = maneuver_branch["x"], maneuver_branch["y"], maneuver_branch["z"]
        fig.add_trace(go.Scatter3d(
            x=branch_x, y=branch_y, z=branch_z,
            mode='lines',
            name=f"Branch {selected_branch.split('ManeuverBranchId')[1].split('.')[0]}",
            line=dict(color='red', width=2, dash="dash")
        ))

    fig.update_layout(
        scene=dict(
            xaxis_title="X Position",
            yaxis_title="Y Position",
            zaxis_title="Z Position"
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        legend=dict(x=0, y=1)
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
