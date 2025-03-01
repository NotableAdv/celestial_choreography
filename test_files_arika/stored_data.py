import os
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Define the directory where CSV files are stored
DATA_DIR = "Data"

# Load the RPO plan data (or modify for the correct dataset)
rpo_plan_path = os.path.join(DATA_DIR, "RpoPlan.csv")

# Ensure the file exists
if not os.path.exists(rpo_plan_path):
    raise FileNotFoundError(f"Error: {rpo_plan_path} not found!")

# Load CSV and check contents
rpo_plan = pd.read_csv(rpo_plan_path)

# Ensure numeric columns
rpo_plan["secondsSinceStart"] = pd.to_numeric(rpo_plan["secondsSinceStart"], errors="coerce")
rpo_plan["storedData"] = pd.to_numeric(rpo_plan["storedData"], errors="coerce")

# Remove NaN values
rpo_plan = rpo_plan.dropna(subset=["secondsSinceStart", "storedData"])

# Sort by time for correct plotting
rpo_plan = rpo_plan.sort_values(by="secondsSinceStart")

# Initialize Dash App
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Stored Data Levels Over Time"),
    dcc.Graph(id="stored-data-plot"),
])

@app.callback(
    Output("stored-data-plot", "figure"),
    Input("stored-data-plot", "id")  # Placeholder to trigger update
)
def update_stored_data_plot(_):
    fig = go.Figure()

    # **Line Graph for Stored Data Levels**
    fig.add_trace(go.Scatter(
        x=rpo_plan["secondsSinceStart"],
        y=rpo_plan["storedData"],
        mode="lines",
        line=dict(color="blue", width=2),
        name="Stored Data"
    ))

    # **Layout Formatting**
    fig.update_layout(
        title="Stored Data Levels Over Time",
        xaxis_title="Time Since Start (Seconds)",
        yaxis_title="Stored Data (Units)",
        template="plotly_white",
        height=600,

        # **Enable Sliding Range Selector**
        xaxis=dict(
            rangeslider=dict(visible=True),  # Enables draggable range slider
            type="linear"  # Ensure it's not treated as a date
        ),

        yaxis=dict(
            fixedrange=False  # Allow zooming on Y-axis
        )
    )

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
