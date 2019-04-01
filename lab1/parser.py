from lab1.node import Node


class Parser:
    def __init__(self, path):
        self.path = path
        self.index = 0
        self.root = None
        self.content = None

    def parse(self):
        with open(self.path) as f:
            content = ' '.join(f.read().splitlines())
            self.content = ' '.join(content.split())

        self.parse_tree()

    def parse_tree(self, parent_node=None):
        while True:
            open_tag = self.parse_open_tag()
            if open_tag:
                node = Node()
                node.tag = open_tag

                if parent_node:
                    parent_node.children.append(node)
                else:
                    self.root = node

                self.parse_tree(node)

            value = self.parse_value()
            if value:
                node = Node()
                # node.value = value.replace('\t', ' ').strip()
                node.value = value
                parent_node.children.append(node)

            close_tag = self.parse_close_tag()
            if close_tag and parent_node.tag == close_tag:
                parent_node.closed = True
                return

            if not open_tag and not value and not close_tag:
                return

    def parse_open_tag(self):
        open_tag = ''
        is_open_tag = False
        index = self.index

        while True and self.has_next():
            c = self.content[index]
            if not c:
                return
            c = c.strip()
            if not c:
                index += 1
                continue

            if not is_open_tag and c == '/':
                is_open_tag = True
                index += 1
                continue

            if not is_open_tag and c != '/':
                return None

            if is_open_tag and c == '\\':
                index += 1
                break

            if is_open_tag:
                index += 1
                open_tag += c

        self.index = index
        return open_tag

    def parse_value(self):
        value = ''
        is_value = False
        index = self.index

        while True and self.has_next():
            c = self.content[index]
            if not c:
                return
            if not is_value:
                c = c.strip()
            if not c:
                index += 1
                continue

            if not is_value and c != '/' and c != '\\':
                is_value = True

            if not is_value and (c == '/' or c == '\\'):
                return None

            if is_value and (c == '/' or c == '\\'):
                break

            if is_value:
                index += 1
                value += c

        self.index = index
        return value

    def parse_close_tag(self):
        close_tag = ''
        is_close_tag = False
        index = self.index

        while True and self.has_next():
            c = self.content[index]
            if not c:
                return
            c = c.strip()
            if not c:
                index += 1
                continue

            if not is_close_tag and c == '\\':
                is_close_tag = True
                index += 1
                continue

            if not is_close_tag and c != '\\':
                return None

            if is_close_tag and c == '/':
                index += 1
                break

            if is_close_tag:
                index += 1
                close_tag += c

        self.index = index
        return close_tag

    def has_next(self):
        return self.index < len(self.content)
