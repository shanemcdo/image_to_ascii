#!/usr/bin/env python3

import numpy as np
import argparse
from os import get_terminal_size
from PIL import Image, ImageOps
from time import sleep

LONG_SPARSE_TO_DENSE = ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
SHORT_SPARSE_TO_DENSE = ' .:-=+*#%@'
RESET_FORMATTING = '\033[0m'


def hide_cursor():
    print('\033[?25l', end='')

def show_cursor():
    print('\033[?25h', end='')

def color_str(r: int, g: int, b: int) -> str:
    return f'\033[48;2;{r};{g};{b}m'

def convert_to_ascii_color(img: Image) -> str:
    img = img.convert('RGB')
    arr = np.array(img)
    output = ''
    for row in arr:
        prev = None
        for r, g, b in row:
            color = color_str(r, g, b)
            if prev != color:
                prev = color
                output += color
            output += ' '
        output += RESET_FORMATTING + '\n'
    return output[:-1] + RESET_FORMATTING

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
    return output[:-1]

def convert_to_ascii(img: Image, args) -> str:
    ascii_scale = LONG_SPARSE_TO_DENSE
    if args.basic:
        ascii_scale = SHORT_SPARSE_TO_DENSE
    if args.auto:
        term_size = get_terminal_size()
        if img.size[0] > img.size[1] * 2:
            new_size = (term_size[0], int(term_size[0] / img.size[0] * img.size[1] / 2))
        else:
            new_size = (int(term_size[1] / img.size[1] * img.size[0] * 2), term_size[1])
        img = img.resize(new_size)
    elif args.stretch:
        img = img.resize(get_terminal_size())
    else:
        width, height = img.size
        img = img.resize((int(width / args.scale * 2), int(height / args.scale)))
    if args.color:
        return convert_to_ascii_color(img)
    else:
        return convert_to_ascii_grayscale(
            img,
            ascii_scale[::-1] if args.reverse else ascii_scale
        )

def parse_args():
    parser = argparse.ArgumentParser('img2ascii', description='Converts an image or gif into ascii text')
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
    parser.add_argument(
        '-d',
        '--delay',
        type=float,
        default=0.1,
        help='Delay for displaying gifs in seconds'
    )
    parser.add_argument(
        '-a',
        '--auto',
        action='store_true',
        help='automatically resize image to what fits the terminal. preserves aspect ratio'
    )
    parser.add_argument(
        '-S',
        '--stretch',
        action='store_true',
        help='automatically resize image to what fits the terminal. doesn\'t preserve aspect ratio'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    img = Image.open(args.filename)
    if not getattr(img, 'is_animated', False):
        ascii_image = convert_to_ascii(img, args)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(ascii_image)
        else:
            print(ascii_image)
    else:
        frames = []
        for i in range(img.n_frames):
            img.seek(i)
            frames.append(convert_to_ascii(img, args))
        if args.output:
            with open(args.output, 'w') as f:
                for frame in frames:
                    f.write(frame + '\n\n')
        else:
            hide_cursor()
            try:
                while True:
                    for frame in frames:
                        # escape code goes to positon 1 1 on screen
                        print('\033[1;1H' + frame, end='')
                        sleep(args.delay)
            except KeyboardInterrupt:
                show_cursor()

if __name__ == '__main__':
    main()
