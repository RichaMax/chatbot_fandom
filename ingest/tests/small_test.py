from bs4 import BeautifulSoup

from scraper.utils_scraper import parse_element

html_code = """
<ul><li>At the time of release, Yagluth was the last boss to defeat.
<ul><li>Yagluth has since been supplanted as final boss by <a href="/wiki/The_Queen" title="The Queen">The Queen</a> in the <a href="/wiki/Mistlands" title="Mistlands">Mistlands</a>.</li>
<li>His drop was called "Yagluth Thing," and its description said it was a placeholder for his actual drop. The Mistlands update added the <a href="/wiki/Torn_spirit" title="Torn spirit">Torn spirit</a>, which is used to craft the <a href="/wiki/Wisp_fountain" title="Wisp fountain">Wisp fountain</a>.</li></ul></li>
<li>After Yagluth spawns in, he breaks through the ground slowly. The player can attack him before he actually begins moving or attacking, racking up some free damage before the boss fight actually begins.</li></ul>
"""

soup = BeautifulSoup(html_code, "html.parser")
print(parse_element(soup))
