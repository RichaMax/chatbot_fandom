from bs4 import BeautifulSoup

from parser.utils_scraper import extract_table

table_html = """
<table class="article-table sortable mw-collapsible jquery-tablesorter mw-made-collapsible" style="text-align:center;">
<thead><tr>
<th class="headerSort" tabindex="0" role="columnheader button" title="Sort ascending">
</th>
<th style="text-align:center;" class="headerSort" tabindex="0" role="columnheader button" title="Sort ascending">Name
</th>
<th style="text-align:center;" class="headerSort" tabindex="0" role="columnheader button" title="Sort ascending">Primary Spawn
</th>
<th style="text-align:center;" class="headerSort" tabindex="0" role="columnheader button" title="Sort ascending">HP
</th>
<th style="text-align:center;" class="headerSort" tabindex="0" role="columnheader button" title="Sort ascending">Damage<sup id="cite_ref-1" class="reference"><a href="#cite_note-1">[1]</a></sup>
</th>
<th class="unsortable" style="text-align:center;"><span class="mw-collapsible-toggle mw-collapsible-toggle-default" role="button" tabindex="0" aria-expanded="true"><a class="mw-collapsible-text">Collapse</a></span>Notes
</th></tr></thead><tbody>
<tr>
<td><a href="https://static.wikia.nocookie.net/valheim/images/6/6f/Boar.png/revision/latest?cb=20220216231230" class="image"><img alt="Boar" src="https://static.wikia.nocookie.net/valheim/images/6/6f/Boar.png/revision/latest/scale-to-width-down/50?cb=20220216231230" decoding="async" loading="lazy" width="50" height="47" data-image-name="Boar.png" data-image-key="Boar.png" data-relevant="1" data-src="https://static.wikia.nocookie.net/valheim/images/6/6f/Boar.png/revision/latest/scale-to-width-down/50?cb=20220216231230" class=" ls-is-cached lazyloaded"></a>
</td>
<td><a href="/wiki/Boar" title="Boar">Boar</a>
</td>
<td><strong class="mw-selflink selflink">Meadows</strong>
</td>
<td>10
</td>
<td>7.5-10
</td>
<td>
</td></tr>
<tr>
<td><a href="https://static.wikia.nocookie.net/valheim/images/6/67/Neck_0star.png/revision/latest?cb=20220227021430" class="image"><img alt="Neck 0star" src="https://static.wikia.nocookie.net/valheim/images/6/67/Neck_0star.png/revision/latest/scale-to-width-down/50?cb=20220227021430" decoding="async" loading="lazy" width="50" height="39" data-image-name="Neck 0star.png" data-image-key="Neck_0star.png" data-relevant="1" data-src="https://static.wikia.nocookie.net/valheim/images/6/67/Neck_0star.png/revision/latest/scale-to-width-down/50?cb=20220227021430" class=" ls-is-cached lazyloaded"></a>
</td>
<td><a href="/wiki/Neck" title="Neck">Neck</a>
</td>
<td><strong class="mw-selflink selflink">Meadows</strong>
</td>
<td>5
</td>
<td>5~
</td>
<td>
</td></tr>
<tr>
<td><a href="https://static.wikia.nocookie.net/valheim/images/4/4e/Greyling_0S.png/revision/latest?cb=20220212224338" class="image"><img alt="Greyling 0S" src="https://static.wikia.nocookie.net/valheim/images/4/4e/Greyling_0S.png/revision/latest/scale-to-width-down/50?cb=20220212224338" decoding="async" loading="lazy" width="50" height="50" data-image-name="Greyling 0S.png" data-image-key="Greyling_0S.png" data-relevant="1" data-src="https://static.wikia.nocookie.net/valheim/images/4/4e/Greyling_0S.png/revision/latest/scale-to-width-down/50?cb=20220212224338" class=" ls-is-cached lazyloaded"></a>
</td>
<td><a href="/wiki/Greyling" title="Greyling">Greyling</a>
</td>
<td><strong class="mw-selflink selflink">Meadows</strong>
</td>
<td>20
</td>
<td>3-5
</td>
<td>
</td></tr>
<tr>
<td><a href="https://static.wikia.nocookie.net/valheim/images/1/13/Draugr_0S.png/revision/latest?cb=20220216234809" class="image"><img alt="Draugr 0S" src="https://static.wikia.nocookie.net/valheim/images/1/13/Draugr_0S.png/revision/latest/scale-to-width-down/50?cb=20220216234809" decoding="async" loading="lazy" width="50" height="50" data-image-name="Draugr 0S.png" data-image-key="Draugr_0S.png" data-relevant="1" data-src="https://static.wikia.nocookie.net/valheim/images/1/13/Draugr_0S.png/revision/latest/scale-to-width-down/50?cb=20220216234809" class=" ls-is-cached lazyloaded"></a>
</td>
<td><a href="/wiki/Draugr" title="Draugr">Draugr</a>
</td>
<td><a href="/wiki/Swamp" title="Swamp">Swamp</a>
<p><strong class="mw-selflink selflink">Meadows</strong>
</p>
</td>
<td>100
</td>
<td>40-50
</td>
<td>In the Meadows, will only spawn in a <a href="/wiki/Draugr_village" title="Draugr village">Draugr village</a>.
<p>Spawns with a bow / axe / axe + wood shield / axe + banded shield
</p>
</td></tr></tbody><tfoot></tfoot></table>HTML
"""

soup = BeautifulSoup(table_html, "html.parser")
print(extract_table(soup))
