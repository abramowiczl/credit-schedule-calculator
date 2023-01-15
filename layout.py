import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px

from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output

from utils.calculations import calc_schedule_w_overpayment
from utils.formats import format_2_decimal_points

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Credit calculator'
app.layout = html.Div(
    children=[
        html.Div(
            [
                html.Span('Nadplata jednorazowa: '),
                dcc.Input(
                    value=0,
                    type="number",
                    id="initial-overpayment-input",
                    step=5000,
                    className="mx-2  border-0",
                    style=
                    {
                        'font-weight': 'bold',
                        'width': '8em',
                        'background': 'slategray',
                        'color': 'white',
                        'border-radius': '1em',
                        'padding-left': '0.5em'
                    }
                )
            ],
            className="d-flex justify-content-start px-5 pt-5"
        ),
        html.Div(
            [
                html.Span('Nadplacajac'),
                dcc.Input(
                    value=1000,
                    type="number",
                    id="overpayment-input",
                    step=250,
                    className="mx-2  border-0",
                    style=
                    {
                        'font-weight': 'bold',
                        'width': '5em',
                        'background': 'slategray',
                        'color': 'white',
                        'border-radius': '1em',
                        'padding-left': '0.5em'
                    }
                ),
                html.Span('zl roznica w koszcie kredytu to '),
                html.Span(
                    id='cost-diff',
                    style=
                    {
                        'font-weight': 'bold',
                        'background': 'lightgreen',
                        'color': 'white',
                        'border-radius': '1em',
                        'padding': '0 0.5em'
                    },
                    className="mx-2"
                ),
                html.Span(
                    ' zl.'
                )
            ],
            className="d-flex justify-content-start px-5 pt-5"
        )
        ,
        dcc.Loading(
            id="graph-loader",
            children=[
                html.Div(
                    id="graph-loader-placeholder",
                    className="mt-5"
                )
            ]
        ),
        dcc.Graph(id="graph")
    ],
    style={'font-size': '20px'}
)

@callback(
        Output("graph", "figure"),
        Output("cost-diff", "children"),
        Output("graph-loader-placeholder", "children"),
        Input("overpayment-input", "value"),
        Input("initial-overpayment-input", "value")
)
def update_graph(overpayment: int, initial_overpayment: int):
    print('Calculating with overpayment: %s and initial overpayment: %s' % (str(overpayment), str(initial_overpayment)))
    schedule = calc_schedule_w_overpayment(overpayment, initial_overpayment)
    total_interest = pd.DataFrame(schedule)['Installment_interest'].sum()
    diff = total_interest_no_overpayment - total_interest
    return create_fig(schedule), format_2_decimal_points(diff), ''

def create_fig(schedule):
    return px.bar(
        schedule,
        x="Date",
        y=["Installment_capital_part", "Installment_interest"],
        labels={
            "value": "Rata (PLN)",
            "variable": "Czesc raty",
            "Date": "Data"
        }
    )

if __name__ == '__main__':
    schedule_no_overpayment = calc_schedule_w_overpayment(0)
    total_interest_no_overpayment = pd.DataFrame(schedule_no_overpayment)['Installment_interest'].sum()
    app.run_server(debug=True)