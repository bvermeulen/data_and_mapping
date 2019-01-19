import glob
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from datetime import date, timedelta
from Utils.plogger import Logger
import inspect


PREFIX = r'autoseis_data\OUT_'
EXCEL_SUMMARY_FILE = 'geo_summary.xlsx'


class GeoData:
    '''  method for handling Geo data '''
    def __init__(self):
        self.logger = Logger.getlogger()

    def read_geo_data(self, _date):
        read_is_valid = False
        _geo_file = ''.join([PREFIX, 
                            f'{_date.year:04}', f'{_date.month:02}', f'{_date.day:02}', 
                            '*.xlsx'])
        _geo_file = glob.glob(_geo_file)
        self.logger.info(f'filename: {_geo_file}')

        if len(_geo_file) != 1:
            pass
        else:
            try:
                self.geo_df = pd.read_excel(_geo_file[0])
                self.date = _date
                self.add_bat_days_in_field_to_df()
                read_is_valid = True

            except FileNotFoundError:
                self.logger.info(f'{inspect.stack()[0][3]} - Exception FileNotFoundError": {_geo_file[0]}')
        
        if read_is_valid:
            return True, self.geo_df
        else:    
            return False, None

    def add_bat_days_in_field_to_df(self):
        days_in_field = []
        list_battery_starts = self.geo_df['BATSTART'].tolist()
        for battery_start in list_battery_starts:
            battery_start = str(battery_start)
            try:
                _year = int(battery_start[0:4])
                _julianday = int(battery_start[4:7])
                _date_in_field = date(_year, 1, 1) + timedelta(_julianday)
                _days_in_field = (self.date - _date_in_field).days
            except ValueError:
                self.logger.info(f'{inspect.stack()[0][3]} - Exception ValueError: {battery_start}')
                _days_in_field = np.NaN
            
            days_in_field.append(_days_in_field)

        # add the columns to the dataframe
        self.geo_df['days_in_field'] = days_in_field


def get_date():
    _date = input('date (YYMMDD) [q - quit]: ')
    if _date in ['q', 'Q']:
        exit()
    _date = date(int(_date[0:2])+2000, 
                 int(_date[2:4]), 
                 int(_date[4:6]))

    return _date


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_date_range():
    start_date = input('date (YYMMDD) [q - quit]: ')
    end_date = input('date (YYMMDD) [q - quit]: ')
    if start_date in ['q', 'Q'] or end_date in ['q', 'Q']:
        exit()
    start_date = date(int(start_date[0:2])+2000, 
                      int(start_date[2:4]), 
                      int(start_date[4:6]))
    end_date = date(int(end_date[0:2])+2000, 
                      int(end_date[2:4]), 
                      int(end_date[4:6]))
    end_date += timedelta(1)

    if start_date >= end_date:
        print('incorrect date range')
        start_date = -1
        end_date = -1

    return start_date, end_date


def append_df_to_excel(df, filename=EXCEL_SUMMARY_FILE, sheet_name='Sheet1', 
                       startrow=None,
                       **to_excel_kwargs):
    """
    Append a DataFrame [df] to existing Excel file [filename]
    into [sheet_name] Sheet.
    If [filename] doesn't exist, then this function will create it.

    Parameters:
    :filename: File path or existing ExcelWriter
               (Example: '/path/to/file.xlsx')
    :df: dataframe to save to workbook
    :sheet_name: Name of sheet which will contain DataFrame.
                 (default: 'Sheet1')
    :startrow: upper left cell row to dump data frame.
               Per default (startrow=None) calculate the last row
               in the existing DF and write to the next row...
    :to_excel_kwargs: arguments which will be passed to `DataFrame.to_excel()`
                      [can be dictionary]

    Returns: None
    """
    logger = Logger.getlogger()
    # ignore [engine] parameter if it was passed
    if 'engine' in to_excel_kwargs:
        to_excel_kwargs.pop('engine')

    writer = pd.ExcelWriter(filename, engine='openpyxl')

    try:
        # try to open an existing workbook
        writer.book = load_workbook(filename)

        # get the last row in the existing Excel sheet
        # if it was not specified explicitly
        if startrow is None and sheet_name in writer.book.sheetnames:
            startrow = writer.book[sheet_name].max_row

            # copy existing sheets
        writer.sheets = {ws.title:ws for ws in writer.book.worksheets}
    except FileNotFoundError:
        # file does not exist yet, we will create it
        logger.info(f'{inspect.stack()[0][3]} - Exception FileNotFoundError {filename}')

    if startrow is None:
        startrow = 0

    # write out the new sheet
    df.to_excel(writer, sheet_name, startrow=startrow, **to_excel_kwargs)

    # save the workbook
    writer.save()