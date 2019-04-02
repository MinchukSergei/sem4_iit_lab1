from collections import deque
import copy

TAG_TABLE = {
    'PRIMAL': 'BODY',
    'HDR': 'H1',
    'BOLD': 'B',
    'ITALIC': 'I',
    'LST': 'UL',
    'LITEM': 'LI',
    'LINK': 'A',
    'DVNCHOBJ': 'IMG',
    'QUOTE': 'ADDRESS',
    'BL': 'DIV',
    'CENTERLINED': 'DEL',
    'UNDERLINED': 'U'
}

MML_ESCAPE_TABLE = {
    '{vline}': '|',
    '{sl}': '/',
    '{bsl}': '\\',
    '{cbr}': '{',
    '{bcbr}': '}',
    '{VLINE}': '|',
    '{SL}': '/',
    '{BSL}': '\\',
    '{CBR}': '{',
    '{BCBR}': '}'
}

HTML_ESCAPE_TABLE = {
    '<': '&lt',
    '>': '&gt',
    '&': '&amp;'
}

LINK_TAG = 'LINK'
DVNCHOBJ_TAG = 'DVNCHOBJ'


class HTMLConverter:
    def __init__(self, mml):
        self.mml = copy.deepcopy(mml)
        self.open_tags()

    def open_tags(self):
        q = deque()
        q.append(self.mml)

        while True:
            if not q:
                break

            node = q.popleft()
            node.closed = False

            children = node.children

            if children:
                for c in children:
                    q.append(c)

    def convert(self, file=None):
        q = deque()
        q.append(self.mml)

        while True:
            if not q:
                break

            node = q.pop()
            tag = node.tag

            if tag:
                tag = tag.upper()

                if LINK_TAG == tag:
                    self.build_link(node, file)
                    continue

                if DVNCHOBJ_TAG == tag:
                    self.build_image(node, file)
                    continue

                html_tag = TAG_TABLE[tag]
                if html_tag:
                    html_tag = html_tag.lower()
                    if not node.closed:
                        print(f'<{html_tag}>', end='', file=file)
                    else:
                        print(f'</{html_tag}>', end='', file=file)

            if node.closed:
                continue
            else:
                node.closed = True

            children = node.children

            if children:
                q.append(node)
                for c in reversed(children):
                    q.append(c)
            else:
                if node.value:
                    print(self.escape_mml_html(node.value).strip(), end='', file=file)

    def build_link(self, node, file):
        ch = node.children

        if len(ch) > 0 and ch[0].value:
            link_values = ch[0].value.split('|')

            if len(link_values) > 1:
                print(f'<a href="{self.escape_mml(link_values[1]).strip()}">{self.escape_mml_html(link_values[0]).strip()}</a>', end='', file=file)
            else:
                print(f'<a href="{self.escape_mml(link_values[0]).strip()}">{self.escape_mml_html(link_values[0]).strip()}</a>', end='', file=file)
        else:
            print(f'<a></a>', end='', file=file)

    def build_image(self, node, file):
        ch = node.children

        if len(ch) > 0 and ch[0].value:
            print(f'<img src="{self.escape_mml(ch[0].value).strip()}">', end='', file=file)
        else:
            print(f'<img>', end='', file=file)

    def escape_mml_html(self, value):
        value = self.escape_mml(value)
        value = self.escape_html(value)
        return value

    def escape_mml(self, value):
        for v, e in MML_ESCAPE_TABLE.items():
            value = value.replace(v, e)
        return value

    def escape_html(self, value):
        for v, e in HTML_ESCAPE_TABLE.items():
            value = value.replace(v, e)
        return value
