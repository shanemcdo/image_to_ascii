import numpy as np
from PIL import Image, ImageOps

ASCII_SCALE = ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
ASCII_SCALE_LEN = len(ASCII_SCALE)

def convert_to_ascii(filename: str, scale: (int, int) = (1, 2)) -> str:
    """
    :filename: the name of the image to read
    :output_filename: [optional] the name of the text file to write to
    """
    img = Image.open(filename)
    img = ImageOps.grayscale(img)
    width, height = img.size
    img = img.resize((width // scale[0], height // scale[1]))
    arr = np.array(img)
    brightest_pixel = -1
    darkest_pixel = 99999
    for row in arr:
        for cell in row:
            brightest_pixel = max(cell, brightest_pixel)
            darkest_pixel = min(cell, darkest_pixel)
    brightness_diff = brightest_pixel - darkest_pixel
    brightness_scaler = brightness_diff / (ASCII_SCALE_LEN - 1)
    f = lambda x: int((x - darkest_pixel) / brightness_scaler)
    output = ''
    for row in arr:
        for cell in row:
            output += ASCII_SCALE[f(cell)]
        output += '\n'
    return output

def print_usage():
    print("""img2ascii filename [flags]
            flags:
                -o or --output: the name of the outputfile

            """)

if __name__ == '__main__':
    ascii_image = convert_to_ascii('CursedCat.jpg')
