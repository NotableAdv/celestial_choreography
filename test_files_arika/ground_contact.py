import os
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Define the directory where CSV files are stored
DATA_DIR = "Data"

# Load Stored Data from RPO Plan
rpo_plan_path = os.path.join(DATA_DIR, "RpoPlan.csv")
ground_contacts_path = os.path.join(DATA_DIR, "GroundContacts.csv")

# Ensure both files exist
if not os.path.exists(rpo_plan_path):
    raise FileNotFoundError(f"Error: {rpo_plan_path} not found!")

if not os.path.exists(ground_contacts_path):
    raise FileNotFoundError(f"Error: {ground_contacts_path} not found!")

# Load stored data
rpo_plan = pd.read_csv(rpo_plan_path)

# Ensure numeric columns
rpo_plan["secondsSinceStart"] = pd.to_numeric(rpo_plan["secondsSinceStart"], errors="coerce")
rpo_plan["storedData"] = pd.to_numeric(rpo_plan["storedData"], errors="coerce")

# Remove NaN values and sort by time
rpo_plan = rpo_plan.dropna(subset=["secondsSinceStart", "storedData"]).sort_values(by="secondsSinceStart")

# **Load Ground Contacts**
ground_contacts = pd.read_csv(ground_contacts_path)

# Ensure ground contacts have valid start & stop time columns
if "startSeconds" not in ground_contacts.columns or "stopSeconds" not in ground_contacts.columns:
    raise ValueError("Error: 'startSeconds' and 'stopSeconds' columns not found in GroundContracts.csv.")

# Convert to numeric
ground_contacts["startSeconds"] = pd.to_numeric(ground_contacts["startSeconds"], errors="coerce")
ground_contacts["stopSeconds"] = pd.to_numeric(ground_contacts["stopSeconds"], errors="coerce")

# Remove NaN values
ground_contacts = ground_contacts.dropna(subset=["startSeconds", "stopSeconds"])

# Debug: Print some ground contact times
print("Ground contact periods (first 5):")
print(ground_contacts.head())

# Initialize Dash App
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Stored Data Levels & Ground Contacts"),
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

    # **Find Y-axis range**
    y_min = rpo_plan["storedData"].min()
    y_max = rpo_plan["storedData"].max()

    # **Shaded Ground Contact Periods**
    for _, row in ground_contacts.iterrows():
        fig.add_shape(
            type="rect",
            x0=row["startSeconds"], x1=row["stopSeconds"],  # Ground contact duration
            y0=y_min, y1=y_max,  # Full y-axis coverage
            fillcolor="rgba(255, 0, 0, 0.3)",  # Darker red shading for visibility
            line_width=0,
            layer="below"
        )

    # **Layout Formatting**
    fig.update_layout(
        title="Stored Data Levels Over Time & Ground Contacts",
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
