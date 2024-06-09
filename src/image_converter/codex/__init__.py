import typing
import enum
import os
from .jpeg import jpeg_decode, jpeg_encode, EXTENSIONS as JPEG_EXTENSIONS
from .webp import webp_decode, webp_encode, EXTENSIONS as WEBP_EXTENSIONS
from .png import png_decode, png_encode, EXTENSIONS as PNG_EXTENSIONS
from PIL import UnidentifiedImageError
import dataclasses
import logging
from image_converter.utils import setup_logger

logger = setup_logger(logging.DEBUG)

SUPPORTED_EXTENSIONS = JPEG_EXTENSIONS + WEBP_EXTENSIONS + PNG_EXTENSIONS


class ImageFormat(enum.Enum):
    JPEG = 'JPEG'
    WEBP = 'WEBP'
    PNG = 'PNG'

    def __str__(self):
        return self.value

    @classmethod
    def get_all_formats(cls):
        return [_format.value for _format in cls]

    @classmethod
    def from_str(cls, string: str):
        for _format in cls:
            if string.upper() == _format.value:
                return _format
        raise ValueError(f"Unsupported format: {string}")

    @classmethod
    def from_extension(cls, extension: str):
        if extension in JPEG_EXTENSIONS:
            return cls.JPEG
        elif extension in WEBP_EXTENSIONS:
            return cls.WEBP
        elif extension in PNG_EXTENSIONS:
            return cls.PNG
        else:
            raise ValueError(f"Unsupported extension: {extension}")



@dataclasses.dataclass
class ConvertResult:
    total: int
    success: int
    failed: int
    errors: typing.List[str] = dataclasses.field(default_factory=list)
    errors_obj: typing.List[Exception] = dataclasses.field(default_factory=list)


class UnidentifiedExtensionError(Exception):
    pass


def _encode_image(image: typing.BinaryIO, out_file: typing.BinaryIO, out_format: ImageFormat):
    if out_format == ImageFormat.JPEG:
        jpeg_encode(image, out_file)
    elif out_format == ImageFormat.WEBP:
        webp_encode(image, out_file)
    elif out_format == ImageFormat.PNG:
        png_encode(image, out_file)
    else:
        raise ValueError(f"Unsupported format: {out_format}")


def _decode_image(extension: str, file_path: str):
    if extension in JPEG_EXTENSIONS:
        return jpeg_decode(file_path)
    elif extension in WEBP_EXTENSIONS:
        return webp_decode(file_path)
    elif extension in PNG_EXTENSIONS:
        return png_decode(file_path)
    else:
        raise UnidentifiedExtensionError(f"Unsupported extension: {extension}")


def convert_image(file_path: str, out_dir: str, out_format: ImageFormat):
    extension = file_path.split('.')[-1].lower()

    image = _decode_image(extension, file_path)

    out_file_path = f"{out_dir}/{file_path.split('/')[-1].split('.')[0]}.{out_format.value.lower()}"

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    out_file_path = os.path.join(out_dir, f"{base_name}.{out_format.value.lower()}")

    with open(out_file_path, 'wb') as out_file:
        _encode_image(image, out_file, out_format)


def convert_images(file_paths: typing.List[str], out_dir: str, out_format: ImageFormat,
                   progress_cb: typing.Callable[[int], None] | None = None) -> ConvertResult:
    progress_cb(0)
    total = len(file_paths)
    success = 0
    errors = []
    errors_obj = []
    err_msg = None
    err_obj = None
    for i, file_path in enumerate(file_paths):
        try:
            convert_image(file_path, out_dir, out_format)
            success += 1
        except UnidentifiedImageError as e:
            err_msg = f"{file_path} is not a valid image file according to its extension"
            err_obj = e
        except UnidentifiedExtensionError as e:
            err_msg = f"{file_path} is not support by this application"
            err_obj = e
        except FileNotFoundError as e:
            err_msg = f"{file_path} not found"
            err_obj = e
        except OSError as e:
            err_msg = f"An error occurred while processing {file_path}"
            err_obj = e
        except Exception as e:
            err_msg = f"An unexpected error occurred while processing {file_path}"
            err_obj = e
        finally:
            progress_cb(i + 1)
            if err_msg:
                errors.append(err_msg)
                errors_obj.append(err_obj)
                logger.error(err_msg)
                err_msg = None
                err_obj = None

    return ConvertResult(total, success, total - success, errors, errors_obj)