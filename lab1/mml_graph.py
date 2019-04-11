import math
from collections import deque

from lab1.parser import Parser

LINK_TAG = 'LINK'


class MMLGraph:
    def __init__(self):
        self.graph = {}

    def graph_from_pages(self, path):
        pages = list(path.glob('*.mml'))
        parsed_mml = {}

        self.init_graph(pages)

        parser = Parser()
        for p in pages:
            parsed_mml[p.name] = parser.parse(p)

        self.build_graph(parsed_mml)

    def init_graph(self, pages):
        for i in pages:
            r = {}
            for j in pages:
                if i.name == j.name:
                    r[j.name] = 0
                else:
                    r[j.name] = math.inf
            self.graph[i.name] = r

    def build_graph(self, parsed_mml):
        for n, mml in parsed_mml.items():
            link_values = self.get_link_values(mml)

            for lv in link_values:
                if n in self.graph:
                    if lv in self.graph[n]:
                        if n != lv:
                            self.graph[n][lv] = 1

    def get_link_values(self, mml):
        link_values = []
        q = deque()
        q.append(mml)

        while True:
            if not q:
                break

            node = q.pop()

            if node.tag:
                if LINK_TAG == node.tag.upper():
                    link_values.append(self.get_link(node))

            children = node.children

            if children:
                for c in children:
                    q.append(c)

        return link_values

    def get_link(self, node):
        link_value = ''
        ch = node.children

        if ch and len(ch) > 0:
            v = ch[0].value.split('|')
            link_value = v[1] if len(v) > 1 else v[0]

        return link_value.strip()
