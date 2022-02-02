import zipfile
import shutil
import glob
import os
from bs4 import BeautifulSoup

# ゴミディレクトリとファイルを削除
def remove_trash(docID):
  shutil.rmtree('files/tmp/XBRL')
  os.remove(f'files/zip/{docID}.zip')

# XBRLファイルをtmpからxbrlディレクトリへ移動する
def move_xbrl(docID):
  files = glob.glob(f'files/tmp/XBRL/PublicDoc/**.xbrl')
  if len(files) < 1: return
  shutil.move(files[0], f'files/xbrl/{docID}.xbrl')

# Zipファイルの一部を取り出す
def select_file_in_zip(docID):
  with zipfile.ZipFile(f'files/zip/{docID}.zip') as existing_zip:
    existing_zip.extractall(f'files/tmp')

# Zipファイルを書き込みます
def zip_write(docID, res):
  filename = f'{docID}.zip'
  if res.status_code == 200:
    with open(f'files/zip/{filename}', 'wb') as f:
      for chunk in res.iter_content(chunk_size=1024):
        f.write(chunk)

def read_xbrl(docID):
  with open(f"files/xbrl/{docID}.xbrl", "r", encoding="utf-8") as f:
    return BeautifulSoup(f.read(), features="lxml")