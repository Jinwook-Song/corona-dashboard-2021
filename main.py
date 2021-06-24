import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import countries_df, totals_df
from builders import make_table

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

## Map
bubble_map = px.scatter_geo(
    countries_df,
    size="Confirmed",
    size_max=50,
    title="Confirmed By Country",
    color="Confirmed",
    hover_name="Country_Region",
    locations="Country_Region",
    locationmode="country names",
    template="plotly_dark",
    projection="natural earth",
    color_continuous_scale=px.colors.sequential.Oryel,
    hover_data={
        "Confirmed": ":,2f",
        "Deaths": ":,2f",
        "Recovered": ":,2f",
        "Country_Region": False,
    },
).update_layout(margin=dict(l=0, r=0, t=50, b=0))

## Bar
bars_graph = px.bar(
    totals_df,
    x="condition",
    y="count",
    template="plotly_dark",
    title="Total Global Cases",
    hover_data={"count": ":,"},
    labels={"condition": "Condition", "count": "Count", "color": "Condition"},
).update_traces(marker_color=["#d63031", "#a29bfe", "#0984e3"])

# Display
app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px", "marginBottom": 100},
            children=[html.H1("Corona Dashboard", style={"fontSize": "50"})],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": "50",
                "gridTemplateColumns": "repeat(4,1fr)",
            },
            children=[
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[dcc.Graph(figure=bubble_map)],
                ),
                html.Div(children=[make_table(countries_df)]),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(
                    children=[
                        dcc.Graph(figure=bars_graph),
                    ]
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
