from tabulate import tabulate

from utils.formats import format2DecimalPoints, formatColumnSplit


def prepareSummary(data_overpayment, data_no_overpayment):
    summary = []
    for i in range(0, len(data_no_overpayment)):
        diff_installment_capital_part = data_no_overpayment[i]['Installment_capital_part'] - data_overpayment[i][
            'Installment_capital_part']
        diff_installment_interest = data_no_overpayment[i]['Installment_interest'] - data_overpayment[i][
            'Installment_interest']
        diff_installment = data_no_overpayment[i]['Installment'] - data_overpayment[i]['Installment']
        diff_capital = data_no_overpayment[i]['Capital'] - data_overpayment[i]['Capital']

        summary.append([
            format2DecimalPoints(data_overpayment[i]['Installment_number']),
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