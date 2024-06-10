import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from image_converter.codex import ImageFormat

supported_formats = ImageFormat.get_all_formats()

parser = argparse.ArgumentParser(description='Image converter')
parser.add_argument('--no-gui', action='store_true', help='Run without GUI')
parser.add_argument('-o', '--output-dir', type=str, help='Output directory')
parser.add_argument('-i', '--input-file', type=str, nargs='+', help='Input files')
parser.add_argument('-f', '--format', choices=supported_formats, help='Output format')

args = parser.parse_args()

if args.no_gui:
    from image_converter.codex import convert_images

    if not args.input_file:
        print("Input files are not specified")
        sys.exit(1)

    if not args.output_dir:
        print("Output directory is not specified")
        sys.exit(1)

    if not args.format:
        print("Output format is not specified")
        sys.exit(1)

    result = convert_images(args.input_file, args.output_dir, ImageFormat.from_str(args.format))
    print(f"Total: {result.total} Success: {result.success} Failed: {result.failed}")
    if result.errors:
        print("Errors:")
        for error in result.errors:
            print(error)

else:
    # GUI mode can not run on python 3.12
    if sys.version_info >= (3, 12):
        print("GUI mode can not run on python 3.12")
        sys.exit(1)
    import qdarktheme
    from PySide6.QtWidgets import QApplication

    from image_converter.ui.main_window import MainWindow

    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme(theme='light')

    window = MainWindow()
    window.show()
    app.exec()
