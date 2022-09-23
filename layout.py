
import pandas as pd
import dash_bootstrap_components as dbc

from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output

from calcCreditSchedule import calcScheduleWithOverpayment, total_interest_no_overpayment, createFig
from utils.formats import format2DecimalPoints

# app = Dash(__name__)
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    children=[
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
                        'width': '4em',
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
        Input("overpayment-input", "value")
)
def update_graph(overpayment: int):
    if overpayment is None:
        overpayment = 0
    schedule = calcScheduleWithOverpayment(overpayment)
    total_interest = pd.DataFrame(schedule)['Installment_interest'].sum()
    diff = total_interest_no_overpayment - total_interest
    return createFig(schedule), format2DecimalPoints(diff), ''

if __name__ == '__main__':
    app.run_server(debug=True)