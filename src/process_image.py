from __future__ import division,print_function

import cv2
import numpy as np
import argparse
import itertools as it

NUMBER_BINS=4 #Number of bins each
SIZE_PIXEL=1 #Real size of one pixel, in square centimeters

class Binner(object):
    def __init__(self,number_bins):
        self.number_bins=number_bins
        self.cache=self.initialize_cache()

    @staticmethod
    def _bin(number, number_bins):
        #Number should be a np.uint8
        #Returns approximate average value of bin
        bin_size=256/number_bins
        bin=np.floor(number / bin_size)
        return np.uint8((bin+0.5)*bin_size)

    def initialize_cache(self):
        cache={}
        for i in range(256):
            cache[i]=self._bin(i,self.number_bins)
        return cache

    def __call__(self, number):
        return self.cache[number]


def resize_image(img,size,size_pixel):
    size=np.array(size,dtype=np.float)
    size/=size_pixel
    size=np.floor(size)
    return cv2.resize(img,(int(size[0]),int(size[1])))

def bin_image(img,number_bins):
    binner = np.vectorize(Binner(number_bins))
    return binner(img)

def process_image(img_path, size, size_pixel, number_bins, output_path=None):
    img = cv2.imread(img_path)
    img=resize_image(img,size,size_pixel)
    img=bin_image(img,number_bins)
    if output_path is not None:
        cv2.imwrite(output_path,img)
    return img

def box_image(img,block_size=16):
    #Need to trim image for splitting, then cut
    img = img[:img.shape[0] // block_size * block_size, :img.shape[1] // block_size * block_size]
    for slice in np.hsplit(img,img.shape[0]/16):
        for dice in np.vsplit(slice,img.shape[1]/16):
            yield dice

def make_row(dice):
    ls=[]
    for i,j in it.product(range(dice.shape[0]),repeat=2):
        ls.append(dice[i,j])
    ls=map(str,ls)
    return ','.join(ls)+'\n'

def make_basket(img_path, size, size_pixel, number_bins, output_file, image_output_path=None, block_size=16):
    img=process_image(img_path,size,size_pixel,number_bins,image_output_path)
    with open(output_file,'w') as f:
        map(f.write,map(make_row,box_image(img,block_size)))


def string_to_array(s):
    np.array(eval(s.replace(' ', ',')), dtype=np.uint8)

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="Resize and bin images for use with association rule data mining")
    parser.add_argument("img_path",type=str,help="Image to process")
    parser.add_argument("Width", type=str, help="Width of the image in centimeters")
    parser.add_argument("Height", type=str, help="Height of the image in centimeters")
    parser.add_argument("-s", "--size-pixel", type=float, dest="size_pixel",default=SIZE_PIXEL, help="The desired size of a single pixel in square centimeters")
    parser.add_argument("-n", "--number-bins", type=int, dest="number_bins",default=NUMBER_BINS,
                        help="The desired number of bins per color")
    parser.add_argument("-o","--output",type=str,dest="output",default=None,help="Output Path")
    args=parser.parse_args()

    output_path=args.output
    if output_path is None:
        output_path=args.img_path[:-4]+"_processed"+args.img_path[-4:]

    # if not hasattr(args,"output_path"):
    #     output_path=args.img_path[:-4]+"_processed"+args.img_path[-4:]
    # else:
    #     output_path = args.output
    process_image(args.img_path,(args.Height,args.Width),args.size_pixel,args.number_bins,output_path)