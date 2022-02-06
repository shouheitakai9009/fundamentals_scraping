import datetime
import pandas_datareader as web
from utility import bs

def str_to_date(text):
  tdatetime = datetime.datetime.strptime(text, '%Y-%m-%d')
  return datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)

# 四半期末日時点の株価終値を取得
def get_dataframe_to_close(soup):
  current_period_item = bs.get_item(soup, "jpdei_cor:CurrentPeriodEndDateDEI", "FilingDateInstant")
  security_code_item = str(bs.get_item(soup, "jpdei_cor:SecurityCodeDEI", "FilingDateInstant").text).rstrip("0")
  current_period = str_to_date(current_period_item.text)
  df_close = web.DataReader(f'{security_code_item}.T', 'yahoo', start=current_period, end=current_period)
  return 0 if df_close.empty else int(df_close.at[current_period_item.text, "Close"])