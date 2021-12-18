#!/usr/bin/env python3

import numpy as np
import sys
import argparse
from PIL import Image, ImageOps
from typing import Tuple

LONG_SPARSE_TO_DENSE = ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
SHORT_SPARSE_TO_DENSE = ' .:-=+*#%@'

def convert_to_ascii(filename: str, scale: (int, int), ascii_scale: str) -> str:
    """
    :filename: the name of the image to read
    :output_filename: [optional] the name of the text file to write to
    """
    img = Image.open(filename)
    img = ImageOps.grayscale(img)
    width, height = img.size
    img = img.resize((int(width // scale[0]), int(height // scale[1])))
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

def main():
    """
    image_to_ascii - An app that converts images to ascii images
        usage:
            img2ascii {filename} [flags]
        flags:
            -o {output filename} or --output {output filname}: outputs a file with the passed name instead of printing
            -s {width divisor} {height divisor} or --size {width divisor} {height divisor}: scales the height and width of the output
            -r or --reverse: reverses the ascii scale so the characters are the most dense where the image is the darkest (used for dark text on light background)
            -b or --basic: use a less complex ascii scale
    """
    ascii_scale = LONG_SPARSE_TO_DENSE
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
        nargs=2,
        default=[1.0, 2.0],
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
    args = parser.parse_args()
    if args.basic:
        ascii_scale = SHORT_SPARSE_TO_DENSE
    ascii_image = convert_to_ascii(
        args.filename,
        args.scale,
        ascii_scale[::-1] if args.reverse else ascii_scale
    )
    if args.output:
        with open(args.output, 'w') as f:
            f.write(ascii_image)
    else:
        print(ascii_image)

if __name__ == '__main__':
    main()
