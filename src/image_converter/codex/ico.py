from PIL import Image
import typing

EXTENSIONS = ['ico']


def ico_encode(image: Image, out_file: typing.BinaryIO):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(out_file, format='ICO')


def ico_decode(in_file: str) -> Image:
    return Image.open(in_file, formats=['ICO'])
