# coding=utf-8
import argparse

import process_image
from utilities import extract_size, generate_output_name

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Create .basket files from images for use with association rule data mining in Orange.")
    parser.add_argument("images", type=str, nargs='+', help="Images to process")
    parser.add_argument("-s", "--size-pixel", type=float, dest="size_pixel", default=process_image.SIZE_PIXEL,
                        help="The desired size of a single pixel in square centimeters")
    parser.add_argument("-n", "--number-bins", type=int, dest="number_bins", default=process_image.NUMBER_BINS,
                        help="The desired number of bins per color")
    args = parser.parse_args()

    for index,image in enumerate(args.images):
        print("Processing image {}/{}: {}".format(index,len(args.images),image))
        process_image.make_basket(img_path=image,
                                  size=extract_size(image),
                                  size_pixel=args.size_pixel,
                                  number_bins=args.number_bins,
                                  output_file=generate_output_name(image),
                                  block_size=16)
