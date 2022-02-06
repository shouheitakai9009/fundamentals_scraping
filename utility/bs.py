from bs4 import BeautifulSoup

def get_item(soup: BeautifulSoup, tag: str, context: str):
  lower_tag = tag.lower()
  context_ref = {"contextRef".lower(): context}
  result = soup.find(lower_tag, attrs=context_ref)
  non_consolidate_s = f'{context_ref}_NonConsolidatedMember'
  if result == None:
    return soup.find(lower_tag, attrs=non_consolidate_s)
  else:
    return soup.find(lower_tag, attrs=context_ref)

def is_non_consolidated(soup: BeautifulSoup):
  lower_tag = "xbrldi:explicitMember".lower()
  dimension = {"dimension": "jppfs_cor:ConsolidatedOrNonConsolidatedAxis"}
  result = soup.find(lower_tag, attrs=dimension)
  if result == None:
    return False # 非連結ではない=連結決算である
  else:
    return result.text == "jppfs_cor:NonConsolidatedMember"