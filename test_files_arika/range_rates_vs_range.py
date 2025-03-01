import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Define the directory where CSV files are stored
DATA_DIR = "Data"

# Load the RPO plan data
rpo_plan_path = os.path.join(DATA_DIR, "RpoPlan.csv")

# Ensure the file exists
if not os.path.exists(rpo_plan_path):
    raise FileNotFoundError(f"Error: {rpo_plan_path} not found!")

# Load CSV and check contents
rpo_plan = pd.read_csv(rpo_plan_path)
print("Data loaded successfully. First 5 rows:")
print(rpo_plan.head())

# Ensure numeric columns
rpo_plan["relativeRange"] = pd.to_numeric(rpo_plan["relativeRange"], errors="coerce")
rpo_plan["relativeRangeRate"] = pd.to_numeric(rpo_plan["relativeRangeRate"], errors="coerce")

# Remove NaN values
rpo_plan = rpo_plan.dropna(subset=["relativeRange", "relativeRangeRate"])

# Debugging print statement
if rpo_plan.empty:
    raise ValueError("Error: Dataset is empty after cleaning!")

# Create a time-based color gradient (normalized)
rpo_plan["time_index"] = np.linspace(0, 1, len(rpo_plan))

# Initialize Dash App
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Range-Rate vs. Range"),
    dcc.Graph(id="range-rate-plot"),
])

@app.callback(
    Output("range-rate-plot", "figure"),
    Input("range-rate-plot", "id")  # Placeholder to trigger update
)
def update_range_rate_plot(_):
    fig = go.Figure()

    # **Scatter plot with color gradient**
    fig.add_trace(go.Scatter(
        x=rpo_plan["relativeRange"],
        y=rpo_plan["relativeRangeRate"],
        mode="lines+markers",
        marker=dict(
            color=rpo_plan["time_index"],  # Color by time progression
            colorscale="Blues",  # Adjust to match the original gradient
            size=4,
            showscale=True  # Show color scale for reference
        ),
        line=dict(width=2),
        name="Range-Rate Over Time"
    ))

    # **Start Point (Red)**
    fig.add_trace(go.Scatter(
        x=[rpo_plan["relativeRange"].iloc[0]],
        y=[rpo_plan["relativeRangeRate"].iloc[0]],
        mode="markers",
        marker=dict(color="red", size=12),
        name="Start"
    ))

    # **End Point (Green)**
    fig.add_trace(go.Scatter(
        x=[rpo_plan["relativeRange"].iloc[-1]],
        y=[rpo_plan["relativeRangeRate"].iloc[-1]],
        mode="markers",
        marker=dict(color="green", size=12),
        name="End"
    ))

    # **Layout Formatting with Sliding Range**
    fig.update_layout(
        title="Range-Rate vs. Range",
        xaxis_title="Range (m)",
        yaxis_title="Range-Rate (m/s)",
        template="plotly_white",
        height=600,

        # **Enable Sliding Range Selector**
        xaxis=dict(
            rangeslider=dict(visible=True),  # Enables draggable range slider
            type="linear",  # Ensure it's not treated as a date
            range=[rpo_plan["relativeRange"].min(), rpo_plan["relativeRange"].max()]  # Force visible range
        ),

        yaxis=dict(
            fixedrange=False  # Allow zooming on Y-axis
        )
    )

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
