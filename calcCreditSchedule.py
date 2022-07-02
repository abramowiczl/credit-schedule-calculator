from datetime import datetime

import pandas as pd
import plotly.express as px
import yaml
from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output

from utils.calculations import calcSchedule
from utils.formats import format2DecimalPoints

with open('config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
wibor_6m = config['wibor_6m']
spread = config['spread']
lending_rate = spread + wibor_6m
capital = config['capital']
amount_of_installments_left = config['amount_of_installments_left']

def calcScheduleWithOverpayment(overpayment, initial_overpayment = 0):
    initial_capital = capital - initial_overpayment
    return calcSchedule(
        datetime(2022, 7, 1),
        initial_capital,
        lending_rate,
        amount_of_installments_left,
        amount_of_installments_left,
        overpayment,
        []
    )

def createFig(schedule):
    return px.bar(
        schedule,
        x="Date",
        y=["Installment_capital_part", "Installment_interest"],
        labels={
            "value": "Rata (PLN)",
            "variable": "Czesc raty",
            "Installment_capital_part": "Czesc kapitalowa",
            "Installment_interest": "Czesc odsetkowa",
            "Date": "Data"
        }
    )

schedule_no_overpayment = calcScheduleWithOverpayment(0)
total_interest_no_overpayment = pd.DataFrame(schedule_no_overpayment)['Installment_interest'].sum()

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.Span('Wysokosc nadplaty: '),
        dcc.Input(value=1000, type="number", id="overpayment-input", step=250),
        html.Div('Roznica w koszcie kredytu to: '),
        html.Span(
            id='cost-diff',
            style={
                'font-weight': 'bold',
                'font-size': '36px',
                'color': 'gray'
            }
        ),
        dcc.Loading(
            id="graph-loader",
            children=[
                html.Div(
                    id="graph-loader-placeholder"
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
