import argparse
import sys
import os
import markdown
import logging
from bs4 import BeautifulSoup


# todo: need a way to deal w. duplicates or updates; would be nice to have some level of
#       state

parser = argparse.ArgumentParser()
parser.add_argument('filepaths', type=str, nargs='+', help='List of markdown filenames.')
args = parser.parse_args()

print(args.filepaths)

def validate_paths():
    """makes sure that all paths exist; but doesn't check at processing time"""
    for path in args.filepaths:
        if not os.path.exists(path):
            print(f'path: {path} does not exist, exiting.')
            exit(1)

def markdown_file_to_html(path: str):
    """converts markdown file to html, returns the resulting doc"""
    # library does not raise exceptions.
    return  markdown.markdown(path)

def get_card_elements(parsedHtml):
    cards: list = parsedHtml.findAll('card')
    # good place to validate
    # where to handle if no cards?
    return cards
    
def process_card_images(side: object, path_to_file: str):
    """returns the path to images found on the side of this card"""
    images: list = side.findAll('img')
    if len(images) == 0:
        # we have to exten
        return list()
    for image in images:
        filename: str = image.attrs['src']
        file_dirname: str = os.path.dirname(path_to_file)
        image_path: str = os.path.join(file_dirname, filename)

        # is url? is filepath?
        pass

def process_document_cards(cards: list, path_to_file: str):
    for card in cards:
        error_text: str = 'Card element formatting error.'
        if len(card.findAll('front')) != 1:
            raise Exception(error_text)
        if len(card.findAll('back')) != 1:
            raise Exception(error_text)

        front: object = card.findAll('front')[0]
        back: object = card.findAll('back')[0]
        image_paths: list = list()
        image_paths.extend(process_card_images(front, path_to_file))
        image_paths.extend(process_card_images(back, path_to_file))


        front_text: str = str(front)
        back_text: str = str(back)
        

def walk_md_files():
    validate_paths()
    for path in args.filepaths:
        with open(path, 'r') as f:
            file_string: str = f.read()
            html_str: object = markdown_file_to_html(file_string)
            parsedHtml: object = BeautifulSoup(html_str, "html.parser")
            print(parsedHtml.findAll('h1'))
            cards: list = get_card_elements(parsedHtml)
            process_document_cards(cards, path)


walk_md_files()
        