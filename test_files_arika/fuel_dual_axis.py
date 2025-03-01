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
maneuver_plan["dVMagnitude"] = pd.to_numeric(maneuver_plan["dVMagnitude"], errors="coerce")

# Convert time from seconds since start to UTC (if available)
if "timeUtcYear" in maneuver_plan.columns:
    maneuver_plan["time_utc"] = pd.to_datetime(
        maneuver_plan[["timeUtcYear", "timeUtcMonth", "timeUtcDay", "timeUtcHour", "timeUtcMinute", "timeUtcSecond"]]
    )
else:
    maneuver_plan["time_utc"] = maneuver_plan["secondsSinceStart"]  # Placeholder if no UTC columns exist

# Sort data by time
maneuver_plan = maneuver_plan.sort_values(by="time_utc")

# Compute cumulative ΔV
maneuver_plan["cumulative_dV"] = maneuver_plan["dVMagnitude"].cumsum()

# Initialize Dash App
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Delta-V Over Time with Running Total"),
    dcc.Graph(id="delta-v-plot"),
])

@app.callback(
    Output("delta-v-plot", "figure"),
    Input("delta-v-plot", "id")  # Placeholder to trigger update
)
def update_delta_v_plot(_):
    fig = go.Figure()

    # **Make Bars More Visible**
    fig.add_trace(go.Bar(
        x=maneuver_plan["time_utc"],
        y=maneuver_plan["dVMagnitude"],
        name="ΔV per Maneuver",
        marker_color="black",  # **Stronger color**
        marker_line_color="black",  # **Outline for contrast**
        marker_line_width=1.5,  # **Thicker bars**
        opacity=0.9,  # **Reduce transparency for emphasis**
    ))

    # **Red Line for Cumulative ΔV**
    fig.add_trace(go.Scatter(
        x=maneuver_plan["time_utc"],
        y=maneuver_plan["cumulative_dV"],
        mode="lines+markers",
        name="Cumulative ΔV",
        line=dict(color="red", width=3),  # **Thicker Line**
        marker=dict(symbol="circle", size=6, color="red"),
    ))

    # Layout Formatting
    fig.update_layout(
        title="Running Total of Delta-V Over Time".format(maneuver_plan["cumulative_dV"].iloc[-1]),
        xaxis_title="Time (UTC)",
        yaxis_title="ΔV (m/s)",
        legend=dict(x=0, y=1),
        xaxis=dict(rangeslider=dict(visible=True)),
        height=600,  # **Increase height for better separation**
        template="plotly_white"  # **Cleaner look**
    )

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
