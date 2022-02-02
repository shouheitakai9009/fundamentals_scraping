import json
from utility import document
from utility import file
from utility import bs
from bs4 import BeautifulSoup
import pandas as pd

# カラムが定義済みのJSONを読み込みデータフレームを作成しておく
json_file = json.load(open("files/sample/column.json", "r"))
csv_column = {}
for column in json_file['columns']:
  csv_column[column["label"]] = []

df = pd.DataFrame(csv_column)

# EDITNET APIからxbrlファイルだけを抽出してxbrlフォルダに入れる
documents = document.get_documents("2022-01-11")

for i, document_item in enumerate(documents):
  if document_item["xbrlFlag"] == '1' and (document_item["formCode"] == "043000"):
    res = document.get_document(document_item["docID"])
    file.zip_write(document_item["docID"], res)
    file.select_file_in_zip(document_item["docID"])
    file.move_xbrl(document_item["docID"])
    file.remove_trash(document_item["docID"])

    # xbrlファイルを読み込み解析する
    csv_row = []
    for column in json_file['columns']:
      soup = file.read_xbrl(document_item["docID"])
      item = bs.get_item(soup, column["tag"], column["context"])
      csv_row.append("" if item == None else item.text)
    
    df.loc[document_item["docID"]] = csv_row

print(df)