import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_documents(date):
  url = 'https://disclosure.edinet-fsa.go.jp/api/v1/documents.json'
  params = {
    "date": date,
    "type": "2"
  }
  res = requests.get(url, params=params, verify=False)
  body = json.loads(res.text)
  return body['results'] if 'results' in body else []

# params=typeの種別
# 1 提出本文書及び監査報告書(*1)を取得します。
# 2 PDF(*2)を取得します。
# 3 代替書面・添付文書を取得します。
# 4  文ファイルを取得します。
def get_document(docID, type=1):
  url = f'https://disclosure.edinet-fsa.go.jp/api/v1/documents/{docID}'
  params = { "type": type }
  return requests.get(url, params=params, verify=False)