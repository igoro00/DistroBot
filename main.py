from lxml import html, etree
from html5print import HTMLBeautifier
import requests



mainurl="https://distrowatch.com/"
distro = "EndlessOS"
page = requests.get('https://distrowatch.com/table.php?distribution=%s'%distro)
tree = html.fromstring(page.content)
logo = tree.xpath("//td[@class='TablesTitle']/a/img")[0]

print(mainurl+logo.attrib["src"])