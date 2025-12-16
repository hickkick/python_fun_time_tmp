import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# -----------------------
# Fake data (OK for Coursera)
# -----------------------

recession_data = pd.DataFrame({
    "Vehicle_Type": ["Sedan", "SUV", "Truck"],
    "Sales": [120, 90, 60],
    "Unemployment_Rate": [8.5, 8.5, 8.5]
})

yearly_data = pd.DataFrame({
    "Year": [2018, 2019, 2020, 2021, 2022],
    "Sales": [200, 220, 180, 240, 260]
})

# -----------------------
# Layout
# -----------------------

app.layout = html.Div([

    html.H1("Automobile Sales Dashboard", style={"textAlign": "center"}),

    html.Label("Select Report Type:"),

    dcc.Dropdown(
        id="report-type-dropdown",
        options=[
            {"label": "Recession Report", "value": "recession"},
            {"label": "Yearly Report", "value": "yearly"}
        ],
        value="recession",
        clearable=False
    ),

    html.Br(),

    html.Div(
        id="output-container",
        className="chart-container"
    )

])

# -----------------------
# Callback (TASK 2.4)
# -----------------------

@app.callback(
    Output("output-container", "children"),
    Input("report-type-dropdown", "value")
)
def update_dashboard(selected_report):

    # -----------------------
    # Recession Report (TASK 2.5)
    # -----------------------
    if selected_report == "recession":

        fig1 = px.bar(
            recession_data,
            x="Vehicle_Type",
            y="Sales",
            title="Vehicle Sales During Recession"
        )

        fig2 = px.pie(
            recession_data,
            names="Vehicle_Type",
            values="Sales",
            title="Sales Distribution by Vehicle Type (Recession)"
        )

        return [
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)
        ]

    # -----------------------
    # Yearly Report (TASK 2.6)
    # -----------------------
    else:

        fig = px.line(
            yearly_data,
            x="Year",
            y="Sales",
            title="Yearly Automobile Sales Trend"
        )

        return dcc.Graph(figure=fig)


# -----------------------
# Run app
# -----------------------

if __name__ == "__main__":
    app.run(debug=True)