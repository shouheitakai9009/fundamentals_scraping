from utility import document
from utility import file

documents = document.get_documents("2022-01-11")

for i, document_item in enumerate(documents):
  if document_item["xbrlFlag"] == '1' and (document_item["formCode"] == "043000"):
    res = document.get_document(document_item["docID"])
    file.zip_write(document_item["docID"], res)
    file.select_file_in_zip(document_item["docID"])
    file.move_xbrl(document_item["docID"])
    file.remove_trash(document_item["docID"])