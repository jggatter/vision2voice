import io
import os.path as osp

from google.cloud import vision
from google.cloud.vision import types
import argparse

# Argument parsing
# Ex: python --image /path/to/image
parser = argparse.ArgumentParser(description='Read an image.')
parser.add_argument('--image', help='Path to image')
args = parser.parse_args()

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
image = osp.abspath(args.image)

# Loads the image into memory
with io.open(args.image, 'rb') as image:
    content = image.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)