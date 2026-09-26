"""Reject article URLs longer than six ASCII letters/digits before publishing."""
from pathlib import Path
from html.parser import HTMLParser
import re

ROOT = Path(__file__).resolve().parents[1] / 'dist'

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.article = False
        self.redirect = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'main' and attrs.get('id') == 'article':
            self.article = True
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            self.redirect = True

errors = []
for path in ROOT.rglob('*.html'):
    if path == ROOT / 'index.html':
        continue
    page = Page()
    page.feed(path.read_text())
    if page.redirect and not page.article:
        continue
    relative = path.relative_to(ROOT)
    if path.name != 'index.html' or len(relative.parts) != 2 or not re.fullmatch(r'[a-z0-9]{1,6}', relative.parts[0]):
        errors.append(str(relative))
if errors:
    raise SystemExit('Use dist/<slug>/index.html with 1–6 lowercase ASCII letters/digits: ' + ', '.join(errors))
print('Article URLs: OK (1–6 characters).')
