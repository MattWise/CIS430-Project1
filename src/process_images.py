import os
import argparse
import re
import process_image

size_re = re.compile(r'([0-9.]+)x([0-9.]+)cm')
def extract_size(filename):
    m=size_re.search(filename)
    if m is None:
        print(filename)
    width,height=map(float,m.group(1,2))
    return width,height

def generate_output_name(path):
    return os.path.splitext(path)[0]+'.basket'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Create .basket files from images for use with association rule data mining in Orange.")
    parser.add_argument("images", type=str, nargs='+', help="Images to process")
    parser.add_argument("-s", "--size-pixel", type=float, dest="size_pixel", default=process_image.SIZE_PIXEL,
                        help="The desired size of a single pixel in square centimeters")
    parser.add_argument("-n", "--number-bins", type=int, dest="number_bins", default=process_image.NUMBER_BINS,
                        help="The desired number of bins per color")
    args = parser.parse_args()

    for image in args.images:
        process_image.make_basket(img_path=image,
                                  size=extract_size(image),
                                  size_pixel=args.size_pixel,
                                  number_bins=args.number_bins,
                                  output_file=generate_output_name(image),
                                  block_size=16)
