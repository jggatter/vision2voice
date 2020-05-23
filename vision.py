import io
import os
import os.path as osp

from google.cloud import vision
from google.cloud.vision import types
import argparse

# Loads the image into memory
def load_image(image):
    with io.open(image, 'rb') as image:
        content = image.read()
    return types.Image(content=content)

# The whole annotation including newlines
def get_full_annotation(response):
    return response.full_text_annotation.text

# Word by word, no newlines
def get_word_by_word(response):
    words=[]
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    words.append(word_text)
    return words

def main(args):
    # Instantiates a client
    if args.credentials is not None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = osp.abspath(args.credentials)
    client = vision.ImageAnnotatorClient()

    image = load_image(
        osp.abspath(args.image)
    )
    
    response = client.document_text_detection(image=image)

    if args.word_by_word:
        print(get_word_by_word(response))
    else:
        print(get_full_annotation(response))

# Argument parsing
# Ex: python --image /path/to/image
parser = argparse.ArgumentParser(description='Read an image and extract the text.')
parser.add_argument(
    '-i', "--image", 
    help="Path to image"
)
parser.add_argument(
    '-c', '--credentials', 
    help="Path to service account credentials file",
    required=False
)
parser.add_argument(
    '-w', "--word-by-word",
    help="If true, output each word on a new line.",
    action="store_true"
)
args = parser.parse_args()
if __name__ == "__main__": main(args)