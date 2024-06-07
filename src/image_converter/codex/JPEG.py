from PIL import Image
import typing

EXTENSIONS = ['jpeg', 'jpg']


def jpeg_encode(image: Image, out_file: typing.TextIO):
    image.save(out_file, format='JPEG')


def jpeg_decode(in_file: typing.TextIO) -> Image:
    return Image.open(in_file)
