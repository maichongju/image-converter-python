import pytest
from image_converter.codex import ImageFormat, convert_image
import itertools
import os

formats = ImageFormat.get_all_formats()

tests = list(itertools.product(formats, formats))

tests_name = [f'test_convert_image_{test[0]}_to_{test[1]}' for test in tests]

test_dir = os.path.join(os.path.dirname(__file__))
resources_dir = os.path.join(test_dir, 'resources')
output_dir = os.path.join(test_dir, 'output')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def get_input_file_path(file_format: str):
    return os.path.join(resources_dir, f'test.{file_format.lower()}')


def get_output_file_path(file_format: str):
    return os.path.join(output_dir, f'test.{file_format.lower()}')


@pytest.mark.parametrize('in_format, out_format', tests, ids=tests_name)
def test_convert_image(in_format: str, out_format: str):
    input_file = get_input_file_path(in_format)
    # Ensure the input file exists
    assert os.path.exists(input_file), f'Input file {input_file} does not exist'

    output_file = get_output_file_path(out_format)
    if os.path.exists(output_file):
        os.remove(output_file)

    convert_image(input_file, output_dir, ImageFormat.from_str(out_format))

    assert os.path.exists(output_file), f'Output file {output_file} does not exist'

    # Clean up
    os.remove(output_file)
