def format2DecimalPoints(num):
    return "{:,.2f}".format(num)

def formatColumnSplit(num):
    return '|' + str(format2DecimalPoints(num)) + '|'