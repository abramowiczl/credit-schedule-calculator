from datetime import datetime

import pandas as pd
import plotly.express as px
import yaml

from utils.calculations import calcSchedule

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

with open('config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
wibor_6m = config['wibor_6m']
spread = config['spread']
lending_rate = spread + wibor_6m
capital = config['capital']
last_installment_date = datetime.strptime(config['last_installment_date'], '%m-%Y').date()

def calcScheduleWithOverpayment(overpayment, initial_overpayment = 0):
    initial_capital = capital - initial_overpayment
    total_num_of_installments = diff_month(last_installment_date, datetime.now())
    return calcSchedule(
        datetime.now(),
        initial_capital,
        lending_rate,
        total_num_of_installments,
        total_num_of_installments,
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
            "Date": "Data"
        }
    )

schedule_no_overpayment = calcScheduleWithOverpayment(0)
total_interest_no_overpayment = pd.DataFrame(schedule_no_overpayment)['Installment_interest'].sum()
