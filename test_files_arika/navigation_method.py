import os
import pandas as pd
import dash
from dash import dcc, html, dash_table

# Define the directory where CSV files are stored
DATA_DIR = "Data"

# Load RPO Plan Data (each row is a maneuver)
rpo_plan_path = os.path.join(DATA_DIR, "RpoPlan.csv")

# Ensure the file exists
if not os.path.exists(rpo_plan_path):
    raise FileNotFoundError(f"Error: {rpo_plan_path} not found!")

# Load RPO data
rpo_plan = pd.read_csv(rpo_plan_path)

# Ensure necessary columns exist
required_columns = ["navigationMethod", "sensorAngleToEarth", "sensorAngleToSun", "sensorAngleToMoon"]
for col in required_columns:
    if col not in rpo_plan.columns:
        raise ValueError(f"Error: Column '{col}' not found in RpoPlan.csv.")

# Convert to numeric where necessary
rpo_plan["sensorAngleToEarth"] = pd.to_numeric(rpo_plan["sensorAngleToEarth"], errors="coerce")
rpo_plan["sensorAngleToSun"] = pd.to_numeric(rpo_plan["sensorAngleToSun"], errors="coerce")
rpo_plan["sensorAngleToMoon"] = pd.to_numeric(rpo_plan["sensorAngleToMoon"], errors="coerce")

# Remove rows with missing values
rpo_plan = rpo_plan.dropna(subset=required_columns)

# Ensure one row per maneuver by resetting index
rpo_plan = rpo_plan.reset_index(drop=True)

# Add a Maneuver ID column for clarity
rpo_plan.insert(0, "Maneuver ID", rpo_plan.index + 1)

# Initialize Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Maneuver Navigation Data Table"),
    
    # **Dash DataTable**
    dash_table.DataTable(
        id="maneuver-table",
        columns=[
            {"name": "Maneuver ID", "id": "Maneuver ID"},
            {"name": "Navigation Method", "id": "navigationMethod"},
            {"name": "Sensor Angle to Earth (°)", "id": "sensorAngleToEarth"},
            {"name": "Sensor Angle to Sun (°)", "id": "sensorAngleToSun"},
            {"name": "Sensor Angle to Moon (°)", "id": "sensorAngleToMoon"},
        ],
        data=rpo_plan.to_dict("records"),  # Convert DataFrame to dictionary format
        style_table={"overflowX": "auto"},  # Make table scrollable if needed
        style_header={"fontWeight": "bold"},
        sort_action="native",  # Enable sorting
        filter_action="native",  # Enable filtering
        page_size=10,  # Show 10 rows per page
    ),
])

if __name__ == "__main__":
    app.run_server(debug=True)
