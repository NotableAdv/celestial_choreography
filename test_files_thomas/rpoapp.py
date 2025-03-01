import os
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Define the directory where CSV files are stored
DATA_DIR = "Data"

# Load the full RPO plan
rpo_plan_path = os.path.join(DATA_DIR, "RpoPlan.csv")
rpo_plan = pd.read_csv(rpo_plan_path)

# Ensure numeric columns
rpo_plan["secondsSinceStart"] = pd.to_numeric(rpo_plan["secondsSinceStart"], errors="coerce")

# Extract RPO trajectory
rpo_time = rpo_plan["secondsSinceStart"]
rpo_x, rpo_y, rpo_z = (
    rpo_plan["positionDepRelToChiefLvlhX"],
    rpo_plan["positionDepRelToChiefLvlhY"],
    rpo_plan["positionDepRelToChiefLvlhZ"]
)

# Find all maneuver branch files
branch_files = [f for f in os.listdir(DATA_DIR) if f.startswith("ManeuverBranchId") and f.endswith(".csv")]
branch_files.sort()  # Sort for consistency

# Create dropdown options dynamically
dropdown_options = [{"label": "Full RPO Plan (No Failure)", "value": "main"}]
dropdown_options += [
    {"label": f"Miss Maneuver {f.split('ManeuverBranchId')[1].split('.')[0]}", "value": f} for f in branch_files
]

# Initialize Dash App
app = Dash(__name__)

app.layout = html.Div([
    html.H1("RPO 3D Flight Path Visualization"),
    
    dcc.Graph(id="flight-path-plot"),

    # Dropdown for maneuver failure selection
    dcc.Dropdown(
        id="maneuver-selector",
        options=dropdown_options,
        value="main",
        clearable=False
    )
])

@app.callback(
    Output("flight-path-plot", "figure"),
    Input("maneuver-selector", "value")
)
def update_plot(selected_maneuver):
    fig = go.Figure()

    if selected_maneuver == "main":
        # Plot full RPO plan
        fig.add_trace(go.Scatter3d(
            x=rpo_x, y=rpo_y, z=rpo_z,
            mode='lines',
            name='Full RPO Plan',
            line=dict(color='blue', width=2)
        ))
    else:
        # Load the selected maneuver branch
        branch_path = os.path.join(DATA_DIR, selected_maneuver)
        maneuver_branch = pd.read_csv(branch_path)

        # Ensure numeric columns
        maneuver_branch["secondsSinceStart"] = pd.to_numeric(maneuver_branch["secondsSinceStart"], errors="coerce")

        # Dynamically determine the break-off time based on the first valid timestamp in the maneuver branch
        break_off_time = maneuver_branch["secondsSinceStart"].min()

        # Find the nearest match in the RPO plan
        matching_rpo_indices = rpo_time[rpo_time <= break_off_time].index
        if matching_rpo_indices.empty:
            print(f"Warning: No valid break-off point found for {selected_maneuver}. Skipping visualization.")
            return fig  # Return plot without modifications

        break_index = matching_rpo_indices[-1]  # Use the last index before break-off

        # Extract RPO path **until failure**
        rpo_x_fail = rpo_x[:break_index]
        rpo_y_fail = rpo_y[:break_index]
        rpo_z_fail = rpo_z[:break_index]

        # Filter the maneuver branch to only include times **after** the break-off point
        maneuver_branch = maneuver_branch[maneuver_branch["secondsSinceStart"] >= break_off_time]

        if maneuver_branch.empty:
            print(f"Warning: No valid data after time {break_off_time} in {selected_maneuver}.")
            return fig  # Return RPO-only plot if branch data is missing

        # Extract maneuver trajectory
        branch_x = maneuver_branch["positionDepRelToChiefLvlhX"]
        branch_y = maneuver_branch["positionDepRelToChiefLvlhY"]
        branch_z = maneuver_branch["positionDepRelToChiefLvlhZ"]

        # Find actual break-off coordinates
        break_x, break_y, break_z = rpo_x.iloc[break_index], rpo_y.iloc[break_index], rpo_z.iloc[break_index]

        # Plot the RPO path until failure
        fig.add_trace(go.Scatter3d(
            x=rpo_x_fail, y=rpo_y_fail, z=rpo_z_fail,
            mode="lines",
            name="RPO Path (Until Failure)",
            line=dict(color='blue', width=2)
        ))

        # Plot the maneuver branch path
        fig.add_trace(go.Scatter3d(
            x=branch_x, y=branch_y, z=branch_z,
            mode="lines",
            name=f"Path after {selected_maneuver}",
            line=dict(color="red", width=3)
        ))

        # Mark the break-off point dynamically
        fig.add_trace(go.Scatter3d(
            x=[break_x], y=[break_y], z=[break_z],
            mode="markers",
            marker=dict(color="green", size=6, symbol="diamond"),
            name="Break-off Point"
        ))

    fig.update_layout(
        scene=dict(
            xaxis_title="Relative X (km)",
            yaxis_title="Relative Y (km)",
            zaxis_title="Relative Z (km)"
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        legend=dict(x=0, y=1)
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
