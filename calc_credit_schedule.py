from datetime import datetime

import pandas as pd
import plotly.express as px
import yaml

from utils.calculations import calc_schedule, diff_month

with open('config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
wibor_6m = config['wibor_6m']
spread = config['spread']
lending_rate = spread + wibor_6m
capital = config['capital']
last_installment_date = datetime.strptime(config['last_installment_date'], '%m-%Y').date()

def calc_schedule_w_overpayment(overpayment, initial_overpayment = 0):
    initial_capital = capital - initial_overpayment
    total_num_of_installments = diff_month(last_installment_date, datetime.now())
    return calc_schedule(
        datetime.now(),
        initial_capital,
        lending_rate,
        total_num_of_installments,
        total_num_of_installments,
        overpayment,
        []
    )

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

schedule_no_overpayment = calc_schedule_w_overpayment(0)
total_interest_no_overpayment = pd.DataFrame(schedule_no_overpayment)['Installment_interest'].sum()
