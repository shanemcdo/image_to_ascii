import numpy as np
from PIL import Image, ImageOps

ASCII_SCALE = ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
ASCII_SCALE_LEN = len(ASCII_SCALE)

def convert_to_ascii(filename: str, output_filename: str = None) -> str:
    """
    :filename: the name of the image to read
    :output_filename: [optional] the name of the text file to write to
    """
    img = Image.open(filename)
    img = ImageOps.grayscale(img)
    width, height = img.size
    img = img.resize((width, height // 2))
    arr = np.array(img)
    brightest_pixel = -1
    darkest_pixel = 99999
    for row in arr:
        for cell in row:
            brightest_pixel = max(cell, brightest_pixel)
            darkest_pixel = min(cell, darkest_pixel)
    brightness_diff = brightest_pixel - darkest_pixel
    brightness_scaler = brightness_diff / ASCII_SCALE_LEN
    f = lambda x: int((x - darkest_pixel) / brightness_scaler) - 1
    with open(output_filename if output_filename else '.'.join(filename.split('.')[:-1]) + '.txt', 'w') as file:
        for row in arr:
            for cell in row:
                file.write(ASCII_SCALE[f(cell)])
            file.write('\n')

if __name__ == '__main__':
    convert_to_ascii('yea.png')
