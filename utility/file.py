# Zipファイルを書き込みます
def zip_write(docID, res):
  filename = f'{docID}.zip'
  if res.status_code == 200:
    with open(f'./files/tmp/{filename}', 'wb') as f:
      for chunk in res.iter_content(chunk_size=1024):
        f.write(chunk)