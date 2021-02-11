import numpy as np
import sys
from PIL import Image, ImageOps

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
    """
    try:
        output_file = None
        scale = 1, 2
        reverse = False
        sys.argv.pop(0)
        if not len(sys.argv):
            raise ValueError('Not enough arguments')
        i = 0
        while i < len(sys.argv):
            if sys.argv[i].lower() in ['-o', '--output']:
                sys.argv.pop(i)
                output_file = sys.argv.pop(i)
            elif sys.argv[i].lower() in ['-s', '--size']:
                sys.argv.pop(i)
                scale = float(sys.argv.pop(i)), float(sys.argv.pop(i))
            elif sys.argv[i].lower() in ['-r', '--reverse']:
                sys.argv.pop(i)
                reverse = True
            else:
                i += 1
        ascii_image = convert_to_ascii(sys.argv[0], scale, LONG_SPARSE_TO_DENSE[::-1] if reverse else LONG_SPARSE_TO_DENSE)
        if output_file:
            with open(output_file, 'w') as f:
                f.write(ascii_image)
        else:
            print(ascii_image)
    except Exception as e:
        print(f'Error: {e}\n' + main.__doc__)

if __name__ == '__main__':
    main()
