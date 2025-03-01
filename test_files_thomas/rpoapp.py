import os
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import re

# Define the directory where CSV files are stored
DATA_DIR = "Data"

# Load the full RPO plan
rpo_plan_path = os.path.join(DATA_DIR, "RpoPlan.csv")
rpo_plan = pd.read_csv(rpo_plan_path)

# Ensure numeric columns
rpo_plan["secondsSinceStart"] = pd.to_numeric(rpo_plan["secondsSinceStart"], errors="coerce")
rpo_plan["relativeRange"] = pd.to_numeric(rpo_plan["relativeRange"], errors="coerce")

# Extract RPO trajectory
rpo_time = rpo_plan["secondsSinceStart"]
rpo_x, rpo_y, rpo_z = (
    rpo_plan["positionDepRelToChiefLvlhX"],
    rpo_plan["positionDepRelToChiefLvlhY"],
    rpo_plan["positionDepRelToChiefLvlhZ"]
)
rpo_range = rpo_plan["relativeRange"]

# **Chief (RSO) static position**
chief_x, chief_y, chief_z = [0], [0], [0]  # Adjust if there's a specific position

# Function to extract maneuver number for sorting
def extract_number(filename):
    match = re.search(r"(\d+)", filename)
    return int(match.group(0)) if match else float("inf")

# Find and sort all maneuver branch files numerically
branch_files = sorted(
    [f for f in os.listdir(DATA_DIR) if f.startswith("ManeuverBranchId") and f.endswith(".csv")],
    key=extract_number
)

# Identify flagged branches where relativeRange <= 100m
flagged_branches = []
for f in branch_files:
    branch_path = os.path.join(DATA_DIR, f)
    branch_df = pd.read_csv(branch_path)
    if (branch_df["relativeRange"] <= 100).any():
        flagged_branches.append(f)

# Create dropdown options dynamically
dropdown_options = [{"label": "Full RPO Plan (No Failure)", "value": "main"}]
dropdown_options += [
    {"label": f"⚠ Miss Maneuver {extract_number(f)} (Close Approach!)" if f in flagged_branches else f"Miss Maneuver {extract_number(f)}",
     "value": f} for f in branch_files
]

# Initialize Dash App
app = Dash(__name__)

app.layout = html.Div([
    html.H1("RPO Flight Path & Relative Range Analysis"),
    
    # Dropdown for maneuver selection
    dcc.Dropdown(
        id="maneuver-selector",
        options=dropdown_options,
        value="main",
        clearable=False
    ),
    
    # 3D Flight Path Visualization
    dcc.Graph(id="flight-path-plot"),
    
    # 2D Relative Range Over Time Visualization
    dcc.Graph(id="relative-range-plot"),
])

@app.callback(
    [Output("flight-path-plot", "figure"),
     Output("relative-range-plot", "figure")],
    Input("maneuver-selector", "value")
)
def update_plots(selected_maneuver):
    fig_3d = go.Figure()
    fig_2d = go.Figure()

    if selected_maneuver == "main":
        # 3D: Full RPO path
        fig_3d.add_trace(go.Scatter3d(
            x=rpo_x, y=rpo_y, z=rpo_z,
            mode='lines',
            name='Full RPO Plan',
            line=dict(color='blue', width=2)
        ))

        # 2D: Full RPO range plot
        fig_2d.add_trace(go.Scatter(
            x=rpo_time, y=rpo_range,
            mode="lines",
            name="Full RPO Plan",
            line=dict(color="blue", width=2)
        ))

        # **Find & plot markers for close approaches (≤ 100m)**
        close_approach_mask = rpo_range <= 100  # Boolean mask where relative range is ≤ 100m
        if close_approach_mask.any():
            fig_2d.add_trace(go.Scatter(
                x=rpo_time[close_approach_mask], y=rpo_range[close_approach_mask],
                mode="markers",
                marker=dict(color="orange", size=8, symbol="circle"),
                name="Close Approach (≤100m)"
            ))


    else:
        # Load maneuver branch
        branch_path = os.path.join(DATA_DIR, selected_maneuver)
        maneuver_branch = pd.read_csv(branch_path)

        # Ensure numeric columns
        maneuver_branch["secondsSinceStart"] = pd.to_numeric(maneuver_branch["secondsSinceStart"], errors="coerce")
        maneuver_branch["relativeRange"] = pd.to_numeric(maneuver_branch["relativeRange"], errors="coerce")

        # Dynamically determine the break-off time
        break_off_time = maneuver_branch["secondsSinceStart"].min()
        end_maneuver_time = maneuver_branch["secondsSinceStart"].max()

        # Find RPO data until break-off
        rpo_before_index = rpo_time[rpo_time <= break_off_time].index
        if rpo_before_index.empty:
            print(f"Warning: No valid break-off point found for {selected_maneuver}. Skipping visualization.")
            return fig_3d, fig_2d
        
        break_index = rpo_before_index[-1]

        # 3D: RPO path until failure
        fig_3d.add_trace(go.Scatter3d(
            x=rpo_x[:break_index], y=rpo_y[:break_index], z=rpo_z[:break_index],
            mode="lines",
            name="RPO Path (Until Failure)",
            line=dict(color="blue", width=2)
        ))

        # 3D: Maneuver branch path
        fig_3d.add_trace(go.Scatter3d(
            x=maneuver_branch["positionDepRelToChiefLvlhX"],
            y=maneuver_branch["positionDepRelToChiefLvlhY"],
            z=maneuver_branch["positionDepRelToChiefLvlhZ"],
            mode="lines",
            name=f"Path after {selected_maneuver}",
            line=dict(color="red", width=3)
        ))
        # Find actual break-off coordinates
        break_x, break_y, break_z = rpo_x.iloc[break_index], rpo_y.iloc[break_index], rpo_z.iloc[break_index]

        # Extract RPO trajectory **after break-off** for dashed continuation path
        expected_rpo_indices = rpo_time[(rpo_time >= break_off_time) & (rpo_time <= end_maneuver_time)].index
        if not expected_rpo_indices.empty:
            expected_rpo_x = rpo_x[expected_rpo_indices]
            expected_rpo_y = rpo_y[expected_rpo_indices]
            expected_rpo_z = rpo_z[expected_rpo_indices]

            # Plot the expected RPO continuation (dashed green)
            fig_3d.add_trace(go.Scatter3d(
                x=expected_rpo_x, y=expected_rpo_y, z=expected_rpo_z,
                mode="lines",
                name="Expected RPO Continuation",
                line=dict(color="green", width=2, dash="dash")
            ))

        # Mark the break-off point dynamically
        fig_3d.add_trace(go.Scatter3d(
            x=[break_x], y=[break_y], z=[break_z],
            mode="markers",
            marker=dict(color="green", size=4, symbol="diamond"),
            name="Break-off Point"
        ))

        # 2D: RPO range until break-off
        fig_2d.add_trace(go.Scatter(
            x=rpo_time[:break_index], y=rpo_range[:break_index],
            mode="lines",
            name="RPO Plan (Until Failure)",
            line=dict(color="blue", width=2)
        ))

        # 2D: Maneuver branch range
        fig_2d.add_trace(go.Scatter(
            x=maneuver_branch["secondsSinceStart"], y=maneuver_branch["relativeRange"],
            mode="lines",
            name=f"Range after {selected_maneuver}",
            line=dict(color="red", width=2)
        ))

        # **Find & plot markers for close approaches (≤ 100m) in maneuver branch**
        branch_close_approach_mask = maneuver_branch["relativeRange"] <= 100  # Boolean mask
        if branch_close_approach_mask.any():
            fig_2d.add_trace(go.Scatter(
                x=maneuver_branch["secondsSinceStart"][branch_close_approach_mask],
                y=maneuver_branch["relativeRange"][branch_close_approach_mask],
                mode="markers",
                marker=dict(color="orange", size=8, symbol="circle"),
                name="Close Approach (≤100m) - Maneuver"
            ))


        # Expected RPO continuation (dashed green)
        expected_rpo_indices = rpo_time[(rpo_time >= break_off_time) & (rpo_time <= end_maneuver_time)].index
        if not expected_rpo_indices.empty:
            fig_2d.add_trace(go.Scatter(
                x=rpo_time[expected_rpo_indices], y=rpo_range[expected_rpo_indices],
                mode="lines",
                name="Expected RPO Continuation",
                line=dict(color="green", width=2, dash="dash")
            ))

    # **3D: Chief (RSO) as a static marker**
    fig_3d.add_trace(go.Scatter3d(
        x=chief_x, y=chief_y, z=chief_z,
        mode="markers",
        marker=dict(color="black", size=6, symbol="circle"),
        name="Chief (RSO)"
    ))

    # Format 3D plot
    fig_3d.update_layout(scene=dict(xaxis_title="Relative X (km)", yaxis_title="Relative Y (km)", zaxis_title="Relative Z (km)"))

    # Dynamically determine y-axis range based on selected maneuver
    if selected_maneuver == "main":
        y_min, y_max = rpo_range.min(), rpo_range.max()
        x_min, x_max = rpo_time.min(), rpo_time.max()  # Show full RPO timeline
    else:
        y_min, y_max = maneuver_branch["relativeRange"].min(), maneuver_branch["relativeRange"].max()
        x_min, x_max = maneuver_branch["secondsSinceStart"].min(), maneuver_branch["secondsSinceStart"].max()

    # Format 2D plot with dynamic y-axis scaling and zoomed x-axis
    fig_2d.update_layout(
        xaxis_title="Time (secondsSinceStart)",
        yaxis_title="Relative Range (m)",
        margin=dict(l=0, r=0, b=40, t=40),
        legend=dict(x=0, y=1),
        yaxis=dict(range=[y_min * 0.95, y_max * 1.05]),  # Adds a small buffer so points aren't at the extreme edges
        xaxis=dict(range=[x_min, x_max], rangeslider=dict(visible=True)),  # Auto-zoom x-axis to relevant time range
    )



    return fig_3d, fig_2d

if __name__ == '__main__':
    app.run_server(debug=True)