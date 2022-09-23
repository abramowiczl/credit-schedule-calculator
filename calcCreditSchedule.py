from datetime import datetime

import pandas as pd
import plotly.express as px
import yaml

from utils.calculations import calcSchedule

with open('config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
wibor_6m = config['wibor_6m']
spread = config['spread']
lending_rate = spread + wibor_6m
capital = config['capital']
amount_of_installments_left = config['amount_of_installments_left']
starting_month = config['starting_month']

def calcScheduleWithOverpayment(overpayment, initial_overpayment = 0):
    initial_capital = capital - initial_overpayment
    return calcSchedule(
        datetime(2022, starting_month, 1),
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
