from PIL import Image
import typing

EXTENSIONS = ['webp']


def webp_encode(image: Image, out_file: typing.BinaryIO):
    image.save(out_file, format='WEBP')


def webp_decode(in_file: str) -> Image:
    return Image.open(in_file, formats=['WEBP'])