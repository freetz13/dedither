import sys
import argparse
from pathlib import Path

from PIL import Image, ImageChops

from . import chess_split


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("-K", "--keep",
                        help="Keep whites, blacks and their filtered versions",
                        action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    args.input = Path(args.input)
    args.output = Path(args.output)

    image = Image.open(args.input).convert("RGBA")

    if (image.width % 2) or (image.height % 2):
        return f"{args.input}'s hight and width must be multiple 2"

    whites, blacks, whites_filtered, blacks_filtered = chess_split(image)

    if args.keep:
        stem = args.output.stem
        images = {
            args.output.with_name(f"{stem}_whites"): whites,
            args.output.with_name(f"{stem}_blacks"): blacks,
            args.output.with_name(f"{stem}_whites_filtered"): whites_filtered,
            args.output.with_name(f"{stem}_blacks_filtered"): blacks_filtered,
        }

        for filename, image in images.items():
            image.save(filename.with_suffix(".png"))

    result = ImageChops.blend(whites_filtered, blacks_filtered, 0.5)
    result.save(args.output)


if __name__ == '__main__':
    sys.exit(main())
