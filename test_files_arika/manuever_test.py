import os
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Define the directory where CSV files are stored
DATA_DIR = "Data"

# Load the maneuver plan data
maneuver_plan_path = os.path.join(DATA_DIR, "ManeuverPlan.csv")
maneuver_plan = pd.read_csv(maneuver_plan_path)

# Ensure numeric columns
maneuver_plan["secondsSinceStart"] = pd.to_numeric(maneuver_plan["secondsSinceStart"], errors="coerce")

# Estimate maneuver duration (if WaypointTransferTime exists, use it; otherwise, assume 120s default)
if "WaypointTransferTime" in maneuver_plan.columns:
    maneuver_plan["duration_seconds"] = pd.to_numeric(maneuver_plan["WaypointTransferTime"], errors="coerce").fillna(120)
else:
    maneuver_plan["duration_seconds"] = 120  # Assume 2 minutes if unknown

# Calculate end times
maneuver_plan["end_seconds"] = maneuver_plan["secondsSinceStart"] + maneuver_plan["duration_seconds"]

# Sort maneuvers by start time
maneuver_plan = maneuver_plan.sort_values(by="secondsSinceStart")

# Create a unique maneuver label
maneuver_plan["Maneuver"] = "Maneuver " + maneuver_plan.index.astype(str)

# Initialize Dash App
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Maneuver Gantt Chart"),
    dcc.Graph(id="gantt-chart"),
])

@app.callback(
    Output("gantt-chart", "figure"),
    Input("gantt-chart", "id")  # Placeholder to trigger update
)
def update_gantt_chart(_):
    fig = go.Figure()

    for i, row in maneuver_plan.iterrows():
        fig.add_trace(go.Bar(
            x=[row["duration_seconds"]],
            y=[row["Maneuver"]],
            base=row["secondsSinceStart"],
            orientation="h",
            marker=dict(color="blue", opacity=0.7),
            hoverinfo="x+y",
            name=row["Maneuver"]
        ))

    fig.update_layout(
        title="Maneuver Timeline (Gantt Chart)",
        xaxis_title="Time Since Start (Seconds)",
        yaxis_title="Maneuver ID",
        xaxis=dict(type="linear", tickformat=",d", showgrid=True),
        height=800,
        showlegend=False
    )

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
