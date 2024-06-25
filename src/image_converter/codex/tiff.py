from PIL import Image
import typing

EXTENSIONS = ['tiff']


def tiff_encode(image: Image, out_file: typing.BinaryIO):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(out_file, format='TIFF')


def tiff_decode(in_file: str) -> Image:
    return Image.open(in_file, formats=['TIFF'])
