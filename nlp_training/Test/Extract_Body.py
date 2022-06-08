import codecs

file = '/Greek Product Contact Point for Construction.html'
html_doc = codecs.open(file, "r", "utf-8")
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc.read(), 'html.parser')

print(soup.get_text())

#################################



