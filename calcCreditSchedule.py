import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tabulate import tabulate
import yaml

def format2DecimalPoints(num):
    return "{:.2f}".format(num)

def formatColumnSplit(num):
    return '|' + str(format2DecimalPoints(num)) + '|'

def calcInterest(capital, datetime):
    days_in_month = calendar.monthrange(datetime.year, datetime.month)[1]
    return capital * LENDING_RATE * days_in_month / 365

def calcSchedule(current_date, capital, num_of_installments_left, overpayment, data):
    if (capital <= 0):
        capital = 0
        overpayment = 0
    installment_capital_part = capital / num_of_installments_left
    installment_interest = calcInterest(capital, current_date)
    capital_left = capital - installment_capital_part - overpayment
    installment = installment_capital_part + installment_interest

    record = dict()
    record['Num_of_installments_left'] = 222 - num_of_installments_left
    record['Installment_capital_part'] = installment_capital_part
    record['Installment_interest'] = installment_interest
    record['Installment'] = installment
    record['Capital'] = capital
    data.append(record)

    if(num_of_installments_left > 1):
        next_month = current_date + relativedelta(months=1)
        return calcSchedule(next_month, capital_left, num_of_installments_left - 1, overpayment, data)
    else:
        return data;

def prepareSummary(data_overpayment, data_no_overpayment):
    summary = []
    for i in range(0, len(data_no_overpayment)):
        diff_installment_capital_part = data_no_overpayment[i]['Installment_capital_part'] - data_overpayment[i]['Installment_capital_part']
        diff_installment_interest = data_no_overpayment[i]['Installment_interest'] - data_overpayment[i]['Installment_interest']
        diff_installment = data_no_overpayment[i]['Installment'] - data_overpayment[i]['Installment']
        diff_capital = data_no_overpayment[i]['Capital'] - data_overpayment[i]['Capital']

        summary.append([
        format2DecimalPoints(data_overpayment[i]['Num_of_installments_left']),
        format2DecimalPoints(data_overpayment[i]['Installment_capital_part']),
        format2DecimalPoints(data_no_overpayment[i]['Installment_capital_part']),
        formatColumnSplit(diff_installment_capital_part),
        format2DecimalPoints(data_overpayment[i]['Installment_interest']),
        format2DecimalPoints(data_no_overpayment[i]['Installment_interest']),
        formatColumnSplit(diff_installment_interest),
        format2DecimalPoints(data_overpayment[i]['Installment']),
        format2DecimalPoints(data_no_overpayment[i]['Installment']),
        formatColumnSplit(diff_installment),
        format2DecimalPoints(data_overpayment[i]['Capital']),
        format2DecimalPoints(data_no_overpayment[i]['Capital']),
        formatColumnSplit(diff_capital),
    ])
        
    return summary

def prettyPrint(summary):
    print(tabulate(
            summary,
            headers=[
                'i',
                'Cz kpt ndpl',
                'Cz kpt',
                'Roznica',
                'Ods ndpl',
                'Ods',
                'Roznica',
                'Rata ndpl',
                'Rata',
                'Roznica',
                'Kpt ndpl',
                'Kpt',
                'Roznica'
            ]
        ))


with open('config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
LENDING_RATE = config['lending_rate']
capital = config['capital']
amount_of_installments_left = config['amount_of_installments_left']
overpayment = config['overpayment']

data_overpayment = calcSchedule(datetime(2022, 3, 1), capital, amount_of_installments_left, overpayment, [])
data_no_overpayment = calcSchedule(datetime(2022, 3, 1), capital, amount_of_installments_left, 0, [])
summary = prepareSummary(data_overpayment, data_no_overpayment)

prettyPrint(summary)