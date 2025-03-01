import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Define the directory where CSV files are stored
DATA_DIR = "Data"

# Load the full RPO plan
rpo_plan_path = os.path.join(DATA_DIR, "RpoPlan.csv")
rpo_plan = pd.read_csv(rpo_plan_path)

# Ensure numeric columns
rpo_plan["secondsSinceStart"] = pd.to_numeric(rpo_plan["secondsSinceStart"], errors="coerce")
rpo_plan["relativeRange"] = pd.to_numeric(rpo_plan["relativeRange"], errors="coerce")

# Drop rows with missing missionSegment values (if any)
rpo_plan = rpo_plan.dropna(subset=["missionSegment"])

# Create a **2D Plot** with color-coded mission segments
fig_2d = px.line(
    rpo_plan,
    x="secondsSinceStart",
    y="relativeRange",
    color="missionSegment",
    title="Relative Range Over Time by Mission Segment",
    labels={"secondsSinceStart": "Time (secondsSinceStart)", "relativeRange": "Relative Range (m)"},
    line_group="missionSegment",
)

# Improve layout & add zooming capabilities
fig_2d.update_layout(
    xaxis=dict(rangeslider=dict(visible=True)),  # Enables zooming
    yaxis=dict(title="Relative Range (m)", autorange=True),
    legend_title="Mission Segment",
    margin=dict(l=0, r=0, b=40, t=40),
)

# Initialize Dash App for Display
app = Dash(__name__)

app.layout = html.Div([
    html.H1("RPO Mission: Relative Range Visualization"),
    dcc.Graph(figure=fig_2d)
])

if __name__ == '__main__':
    app.run_server(debug=True)
