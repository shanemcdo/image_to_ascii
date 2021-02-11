# img2ascii

An application that converts images into ASCII representations of them

### usage:
    img2ascii {filename} [flags]
### flags:
- -o {output filename} or --output {output filname}: outputs a file with the passed name instead of printing
- -s {width divisor} {height divisor} or --size {width divisor} {height divisor}: scales the height and width of the output
- -r or --reverse: reverses the ascii scale so the characters are the most dense where the image is the darkest (used for dark text on light background)
- -b or --basic: use a less complex ascii scale
