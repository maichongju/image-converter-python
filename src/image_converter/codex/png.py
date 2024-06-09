from PIL import Image
import typing

EXTENSIONS = ['png']


def png_encode(image: Image, out_file: typing.BinaryIO):
    image.save(out_file, format='PNG')


def png_decode(in_file: str) -> Image:
    image = Image.open(in_file, formats=['PNG'])
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    return image
