import os
import re

size_re = re.compile(r'([0-9.]+)x([0-9.]+)cm')


def extract_size(filename):
    m=size_re.search(filename)
    if m is None:
        print(filename)
    width,height=map(float,m.group(1,2))
    return width,height


def generate_output_name(path,extension='.basket'):
    return os.path.splitext(path)[0]+extension