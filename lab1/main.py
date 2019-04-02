from lab1.html_converter import HTMLConverter
from lab1.parser import Parser
from pathlib import Path
import webbrowser
import os


def main():
    example_path = Path('../example.mml')
    parser = Parser(example_path)
    parser.parse()

    mml = parser.root
    html_converter = HTMLConverter(mml)
    example_html_path = Path('../example.html')

    with open(example_html_path, mode='w') as f:
        html_converter.convert(f)

    html_path = 'file://' + str(Path('../example.html').absolute())
    if 'CHROME_PATH' in os.environ:
        chrome_path = os.environ['CHROME_PATH'].replace('\\', '/')
        chrome_path = f"{chrome_path} %s"
        webbrowser.get(chrome_path).open(html_path)
    else:
        webbrowser.open(html_path)


if __name__ == '__main__':
    main()
