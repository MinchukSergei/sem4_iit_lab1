from lab1.html_converter import HTMLConverter
from lab1.mml_graph import MMLGraph
from lab1.parser import Parser
from pathlib import Path
import webbrowser
import os

from lab1.path_finder import PathFinder


def main():
    # mml_to_html()
    find_shortest_paths()


def find_shortest_paths():
    pages = Path('../data_path_find')

    mml_graph = MMLGraph()
    mml_graph.graph_from_pages(pages)
    path_finder = PathFinder(mml_graph.graph)
    path_finder.find_paths()
    paths = path_finder.paths

    for i in paths:
        for j in paths:
            if paths[i][j]:
                path = list(paths[i][j])
            else:
                path = []
            print(f'Path from {i} to {j} = {path}')

    pass


def mml_to_html():
    example_path = Path('../example.mml')
    parser = Parser()
    parser.parse(example_path)

    mml = parser.root
    html_converter = HTMLConverter(mml)
    example_html_path = Path('../example.html')

    with open(example_html_path, mode='w') as f:
        html_converter.convert(f)

    html_path = 'file://' + str(Path('../example.html').absolute())
    if 'CHROME_PATH' in os.environ:
        chrome_path = os.environ['CHROME_PATH'].replace(os.sep, '/')
        chrome_path = f'{chrome_path} %s'
        webbrowser.get(chrome_path).open_new_tab(html_path)
    else:
        webbrowser.open_new_tab(html_path)


if __name__ == '__main__':
    main()
