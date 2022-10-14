#!/usr/bin/env python3

import numpy as np
import argparse
from PIL import Image, ImageOps
from typing import Tuple

LONG_SPARSE_TO_DENSE = ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
SHORT_SPARSE_TO_DENSE = ' .:-=+*#%@'

def color_str(r: int, g: int, b: int) -> str:
    return f'\033[48;2;{r};{g};{b}m'

def get_image(filename: str, scale: int) -> Image:
    img = Image.open(filename)
    width, height = img.size
    return img.resize((int(width // scale * 2), int(height // scale)))

def convert_to_ascii_color(img: Image) -> str:
    img = img.convert('RGB')
    arr = np.array(img)
    output = ''
    prev = None
    for row in arr:
        for r, g, b in row:
            color = color_str(r, g, b)
            if prev != color:
                prev = color
                output += color
            output += ' '
        output += '\n'
    return output + '\033[0m'

def convert_to_ascii_grayscale(img: Image, ascii_scale: str) -> str:
    img = ImageOps.grayscale(img)
    arr = np.array(img)
    brightest_pixel = -1
    darkest_pixel = 99999
    for row in arr:
        for cell in row:
            brightest_pixel = max(cell, brightest_pixel)
            darkest_pixel = min(cell, darkest_pixel)
    brightness_diff = brightest_pixel - darkest_pixel
    brightness_scaler = brightness_diff / (len(ascii_scale) - 1)
    if brightness_scaler == 0:
         brightness_scaler = 1
    f = lambda x: int((x - darkest_pixel) / brightness_scaler)
    output = ''
    for row in arr:
        for cell in row:
            output += ascii_scale[f(cell)]
        output += '\n'
    return output

def parse_args():
    parser = argparse.ArgumentParser('img2ascii', description='Converts an image into ascii text')
    parser.add_argument(
        'filename',
        type=str,
        help='The name of the input file'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help='The name of the output file'
    )
    parser.add_argument(
        '-s',
        '--scale',
        type=float,
        default=1.0,
        help='Scale x and y of image'
    )
    parser.add_argument(
        '-b',
        '--basic',
        action="store_true",
        help='Use more basic ascii scale'
    )
    parser.add_argument(
        '-r',
        '--reverse',
        action="store_true",
        help='Reverse ascii scale'
    )
    parser.add_argument(
        '-c',
        '--color',
        action='store_true',
        help='use colors'
    )
    return parser.parse_args()

def main():
    ascii_scale = LONG_SPARSE_TO_DENSE
    args = parse_args()
    if args.basic:
        ascii_scale = SHORT_SPARSE_TO_DENSE
    img = get_image(args.filename, args.scale)
    if args.color:
        ascii_image = convert_to_ascii_color(img)
    else:
        ascii_image = convert_to_ascii_grayscale(
            img,
            ascii_scale[::-1] if args.reverse else ascii_scale
        )
    if args.output:
        with open(args.output, 'w') as f:
            f.write(ascii_image)
    else:
        print(ascii_image)

if __name__ == '__main__':
    main()
