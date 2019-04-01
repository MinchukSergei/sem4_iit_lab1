from lab1.parser import Parser
from pathlib import Path
import webbrowser


def main():
    example_path = Path('../example.mml')
    parser = Parser(example_path)
    parser.parse()

    # chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    # translated_path = Path('../puk.html')
    # webbrowser.get(chrome_path).open('file://' + str(translated_path.absolute()))
    pass


if __name__ == '__main__':
    main()
