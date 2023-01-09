import calendar

import yaml
from dateutil.relativedelta import relativedelta
from datetime import datetime

with open('config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
wibor_6m = config['wibor_6m']
spread = config['spread']
lending_rate = spread + wibor_6m
capital = config['capital']
last_installment_date = datetime.strptime(config['last_installment_date'], '%m-%Y').date()

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def calc_interest(capital, datetime, lending_rate):
    days_in_month = calendar.monthrange(datetime.year, datetime.month)[1]
    return capital * lending_rate * days_in_month / 365

def calc_schedule(current_date, capital, lending_rate, total_num_of_installments, num_of_installments_left, overpayment, data):
    if (capital <= 0):
        return data
    installment_capital_part = capital / num_of_installments_left
    installment_interest = calc_interest(capital, current_date, lending_rate)
    capital_left = capital - installment_capital_part - overpayment
    installment = installment_capital_part + installment_interest

    record = dict()
    record['Date'] = current_date
    record['Installment_number'] = total_num_of_installments - num_of_installments_left
    record['Installment_capital_part'] = installment_capital_part
    record['Installment_interest'] = installment_interest
    record['Installment'] = installment
    record['Capital'] = capital
    data.append(record)

    if(num_of_installments_left > 1):
        next_month = current_date + relativedelta(months=1)
        return calc_schedule(next_month, capital_left, lending_rate, total_num_of_installments, num_of_installments_left - 1, overpayment, data)
    else:
        return data


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