import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html

# Load CSV files
payload_events = pd.read_csv("Data/PayloadEvents.csv")
ground_contacts = pd.read_csv("Data/GroundContacts.csv")

# Ensure timestamps are numeric
payload_events["startSeconds"] = pd.to_numeric(payload_events["startSeconds"], errors="coerce")
payload_events["stopSeconds"] = pd.to_numeric(payload_events["stopSeconds"], errors="coerce")

ground_contacts["startSeconds"] = pd.to_numeric(ground_contacts["startSeconds"], errors="coerce")
ground_contacts["stopSeconds"] = pd.to_numeric(ground_contacts["stopSeconds"], errors="coerce")

# Convert data into a format for timeline visualization
payload_events["Task"] = "Payload Event"
ground_contacts["Task"] = "Ground Contact"

timeline_df = pd.concat([
    payload_events.rename(columns={"startSeconds": "Start", "stopSeconds": "End"})[["Task", "Start", "End"]],
    ground_contacts.rename(columns={"startSeconds": "Start", "stopSeconds": "End"})[["Task", "Start", "End"]]
])

# Initialize Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Mission Timeline: Event Durations in Seconds Since Start"),
    
    dcc.Graph(id="timeline-plot")
])

@app.callback(
    dash.Output("timeline-plot", "figure"),
    dash.Input("timeline-plot", "id")
)
def update_plot(_):
    fig = go.Figure()

    # Add bars for each event type
    for _, row in timeline_df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["Start"], row["End"]],
            y=[row["Task"], row["Task"]],
            mode="lines+markers",
            name=row["Task"],
            line=dict(width=8),
            marker=dict(size=10)
        ))

    # Adjust layout for a proper mission timeline
    fig.update_layout(
        title="Mission Timeline: Event Durations (Seconds Since Start)",
        xaxis_title="Seconds Since Start",
        yaxis_title="Event Type",
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis=dict(
            showgrid=True,
            zeroline=True,
            rangeslider=dict(visible=True)  # Allows zooming in on specific mission windows
        ),
        hovermode="x unified"
    )

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
