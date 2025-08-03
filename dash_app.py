import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html


df = pd.read_csv("benchmark_results.csv")


avg_df = df.groupby(["Array Size", "Method"])["Time (s)"].mean().reset_index()


app = dash.Dash(__name__)
app.title = "QuickSort Benchmark Dashboard"


app.layout = html.Div([
    html.H1("QuickSort Benchmark Dashboard", style={"textAlign": "center"}),

    dcc.Graph(
        id="benchmark-plot",
        figure=px.line(
            avg_df,
            x="Array Size",
            y="Time (s)",
            color="Method",
            markers=True,
            title="Average Sorting Time by Array Size and Method",
            labels={"Time (s)": "Average Time (s)"}
        )
    ),

    html.Div([
        html.H2("Raw Benchmark Results"),
        dcc.Graph(
            id="raw-times",
            figure=px.scatter(
                df,
                x="Array Size",
                y="Time (s)",
                color="Method",
                title="Individual Runs (Raw Data)",
                hover_data=["Run"]
            )
        )
    ], style={"marginTop": "40px"})
])

server = app.server  

if __name__ == "__main__":
    app.run_server(debug=True)
