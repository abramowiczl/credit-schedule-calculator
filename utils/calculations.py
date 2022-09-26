import calendar
from dateutil.relativedelta import relativedelta

def calcInterest(capital, datetime, lending_rate):
    days_in_month = calendar.monthrange(datetime.year, datetime.month)[1]
    return capital * lending_rate * days_in_month / 365

def calcSchedule(current_date, capital, lending_rate, total_num_of_installments, num_of_installments_left, overpayment, data):
    if (capital <= 0):
        capital = 0
        overpayment = 0
    installment_capital_part = capital / num_of_installments_left
    installment_interest = calcInterest(capital, current_date, lending_rate)
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
        return calcSchedule(next_month, capital_left, lending_rate, total_num_of_installments, num_of_installments_left - 1, overpayment, data)
    else:
        return data