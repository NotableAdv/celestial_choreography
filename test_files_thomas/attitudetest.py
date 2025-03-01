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
rpo_plan["sensorAngleToMoon"] = pd.to_numeric(rpo_plan["sensorAngleToMoon"], errors="coerce")
rpo_plan["sensorAngleToEarth"] = pd.to_numeric(rpo_plan["sensorAngleToEarth"], errors="coerce")
rpo_plan["lunarPercentIlluminated"] = pd.to_numeric(rpo_plan["lunarPercentIlluminated"], errors="coerce")

# Define thresholds for "bad vision" hot zones
MOON_ANGLE_THRESHOLD = 45  # Example: Anything below 45 degrees is a problem
EARTH_ANGLE_THRESHOLD = 100  # Example: Anything above 100 degrees is bad
ILLUMINATION_THRESHOLD = 80  # Example: High illumination might cause glare

# Categorize hot zones
rpo_plan["HotZone_Moon"] = rpo_plan["sensorAngleToMoon"] < MOON_ANGLE_THRESHOLD
rpo_plan["HotZone_Earth"] = rpo_plan["sensorAngleToEarth"] > EARTH_ANGLE_THRESHOLD
rpo_plan["HotZone_Glare"] = rpo_plan["lunarPercentIlluminated"] > ILLUMINATION_THRESHOLD

# Initialize Dash App
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Vision Obstruction Analysis"),
    dcc.Dropdown(
        id="hotzone-selector",
        options=[
            {"label": "Show All", "value": "all"},
            {"label": "Highlight Bad Moon Angle", "value": "HotZone_Moon"},
            {"label": "Highlight Bad Earth Angle", "value": "HotZone_Earth"},
            {"label": "Highlight High Lunar Glare", "value": "HotZone_Glare"},
        ],
        value="all",
        clearable=False
    ),
    dcc.Graph(id="hotzone-plot"),
])

@app.callback(
    Output("hotzone-plot", "figure"),
    Input("hotzone-selector", "value")
)
def update_plot(selected_hotzone):
    fig = go.Figure()
    
    # Plot all data
    fig.add_trace(go.Scatter(
        x=rpo_plan["secondsSinceStart"],
        y=rpo_plan["sensorAngleToMoon"],
        mode="lines",
        name="Sensor Angle to Moon",
        line=dict(color="blue")
    ))
    fig.add_trace(go.Scatter(
        x=rpo_plan["secondsSinceStart"],
        y=rpo_plan["sensorAngleToEarth"],
        mode="lines",
        name="Sensor Angle to Earth",
        line=dict(color="green")
    ))
    fig.add_trace(go.Scatter(
        x=rpo_plan["secondsSinceStart"],
        y=rpo_plan["lunarPercentIlluminated"],
        mode="lines",
        name="Lunar Percent Illuminated",
        line=dict(color="orange")
    ))
    
    # Highlight problem areas with markers
    if selected_hotzone != "all":
        hotzone_data = rpo_plan[rpo_plan[selected_hotzone]]
        fig.add_trace(go.Scatter(
            x=hotzone_data["secondsSinceStart"],
            y=hotzone_data["sensorAngleToMoon" if selected_hotzone == "HotZone_Moon" else "sensorAngleToEarth" if selected_hotzone == "HotZone_Earth" else "lunarPercentIlluminated"],
            mode="markers",
            marker=dict(color="red", size=6),
            name="Highlighted Hot Zone"
        ))
    
    fig.update_layout(title="Vision Issues Over Time", xaxis_title="Time (Seconds)", yaxis_title="Angle / Illumination (%)")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
