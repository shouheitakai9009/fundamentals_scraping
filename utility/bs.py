from bs4 import BeautifulSoup

def get_item(soup: BeautifulSoup, tag: str, context: str):
  lower_tag = tag.lower()
  context_ref = {"contextRef".lower(): context}
  return soup.find(lower_tag, attrs=context_ref)