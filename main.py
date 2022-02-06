import json
import pandas as pd
from datetime import date, timedelta
from utility import document
from utility import file
from utility import bs
from utility import data

# カラムが定義済みのJSONを読み込みデータフレームを作成しておく
json_file_consolidated = json.load(open("files/sample/column_consolidated.json", "r"))
json_file_nonconsolidated = json.load(open("files/sample/column_nonconsolidated.json", "r"))
csv_column = {}
for column in json_file_consolidated['columns']:
  csv_column[column["label"]] = []

df = pd.DataFrame(csv_column)

# EDITNET APIからxbrlファイルだけを抽出してxbrlフォルダに入れる
for i in range(3): # とりあえず3日分
  day = date.today() + timedelta(days=-i)
  document_1day = document.get_documents(day)

  for i, document_item in enumerate(document_1day):
    if document_item["xbrlFlag"] == '1' and document_item["formCode"] == "043000" and document_item["docTypeCode"] == "140":
      res = document.get_document(document_item["docID"])
      file.zip_write(document_item["docID"], res)
      file.select_file_in_zip(document_item["docID"])
      file.move_xbrl(document_item["docID"])

      # xbrlファイルを読み込み解析する
      csv_row = []
      soup = file.read_xbrl(document_item["docID"])
      is_non_consolidated = bs.is_non_consolidated(soup)
      json_file = json_file_nonconsolidated if is_non_consolidated else json_file_consolidated

      for column in json_file['columns']:
        if column["label"] == "株価(終値)":
          # 株価取得
          data_close = data.get_dataframe_to_close(soup)
          csv_row.append(data_close)

        elif column["label"] == "時価総額":
          # 時価総額取得
          data_close = data.get_dataframe_to_close(soup)
          close_num = bs.get_item(soup, "jpcrp_cor:NumberOfIssuedSharesAsOfFiscalYearEndIssuedSharesTotalNumberOfSharesEtc", "FilingDateInstant")
          csv_row.append(int(0 if data_close == None else data_close) * int(0 if close_num == None else close_num.text))

        elif column["label"] == "連結または非連結":
          # 連結または非連結取得
          csv_row.append("非連結" if is_non_consolidated else "連結")

        else:
          # 行列に値を追加
          item = bs.get_item(soup, column["tag"], column["context"])
          csv_row.append("" if item == None else item.text)
      #
      df.loc[document_item["docID"]] = csv_row
      file.remove_trash(document_item["docID"])

# CSVに吐き出し
with open("files/sample/sample.csv", mode="w", encoding="cp932", errors="ignore") as f:
  df.to_csv(f)
  print("CSV吐き出し完了")
