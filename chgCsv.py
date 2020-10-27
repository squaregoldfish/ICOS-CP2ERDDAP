# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pathlib import Path


def time_format(tt,dd):

    #2019-07-11T10:55:52.000000Z
    #2019-07-11T10:55:52.000Z
    from dateutil.parser import parse
    dt=parse(tt)

    cc = 10**(6-dd)
    dd=str(dd)

    fmt1 = "%s.%0"+str(dd)+"i%s"
    fmt2 = "%"+str(dd)+"i"

    return fmt1 % (
        dt.strftime('%Y-%m-%dT%H:%M:%S'),
        float(fmt2 % (round(dt.microsecond / cc))),
        dt.strftime('Z')
    )
    #fmt1 = "%s:%3."+dd+"f%s"
    #fmt2 = "%3."+dd+"f"
    #print(dt.second)
    #print(round(dt.microsecond / 1e6))
    #return fmt1 % (
    #    dt.strftime('%Y-%m-%dT%H:%M'),
    #    float(fmt2 % (dt.second + dt.microsecond / 1e6)),
    #    dt.strftime('Z')
    #)

def modify(f):
    # Load the Pandas libraries with alias 'pd'
    import pandas as pd
    import re

    # Read data from file 'filename.csv'
    # (in the same directory that your python process is based)
    # Control delimiters, rows, column names with read_csv (see later)
    print('load ',f)
    #data = pd.read_csv(f,parse_dates=['Date/Time'])
    data = pd.read_csv(f)
    # Preview the first 5 lines of the loaded data

    # remove units from variable name
    # or see to write second line with unit, or unit between parenthese ?
    data.rename(columns=lambda x: re.sub('(.*)(\[.*\])(.*)',r'\1'r'\3', x), inplace=True)

    # format Date/time with less decimal
    data["Date/Time"] = data["Date/Time"].apply(lambda x: time_format(x,3))

    #data.to_csv('test.csv',date_format=pd.to_datetime.dt.strftime('%Y-%m-%dT%H:%M%:%SZ'),index=False)
    #data.to_csv('test.csv',date_format=datetime.datetime.isoformat,index=False)
    #data.to_csv('test.csv',date_format='%Y-%m-%dT%H:%M:%S.%fZ',index=False)

    print(data.head())
    # Warning : overwrite file
    data.to_csv(f,date_format='%Y-%m-%dT%H:%M:%S.%fZ',index=False)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    csvDir = Path('/home/jpa029/Data/ICOS2ERDDAP/58GS20190711_SOCAT_enhanced')
    csv = csvDir / '58GS20190711_SOCAT_enhanced.csv.bak'

    modify(csv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
