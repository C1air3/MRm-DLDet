#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 date:3/6/2022
 author:Cla1r3
 Transform binary file to a RGB PNG image by directory path, the image has
 the same name with the binary file.
"""

import time
import math
import os
import sys
from numba import jit

# pip install Pillow
from PIL import Image, ImageDraw

class FileData:
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

@jit(nopython=True, cache=True)
def determine_size(data):
    # size = int(math.sqrt(len(data)) + 1)
    num_bytes = len(data)
    num_pixels = int(math.ceil(float(num_bytes) / 3.0))
    sqrt = math.sqrt(num_pixels)
    size = int(math.ceil(sqrt))
    return size,size

@jit(nopython=True, cache=True)
def calccolor(byteval):
    return (
        ((byteval & 0o300) >> 6) * 64,
        ((byteval & 0o070) >> 3) * 32,
        (byteval & 0o007) * 32,
    )


def bin2img(data):
    colorfunc =  calccolor
    xsize, ysize = size = determine_size(data)
    print("size is :"+ str(xsize)+", "+str(ysize))
    img = Image.new("RGB", size, color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    print("Draw file begin!")
    try:
        i = 0
        for y in range(ysize):
            for x in range(xsize):
                draw.point((x, y), fill=colorfunc(data[i]))
                i += 1

    except IndexError:
        pass
    print("Draw file end!")
    return img


def error(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

def generate_image(infile):
    with open(infile, "rb") as f:
        data = f.read()
        print("read file success!")
    return bin2img(data)


if __name__ == "__main__":

    dumpath = r"Your bin file <directory name>"
    imagepath = r"Your RGB img file <directory name>"

    try:
        maldirs = os.listdir(dumpath)
        for maldir in maldirs:
            start = time.time()
            print("\n\n" + "FAMILY IS : " + maldir)
            malfiledir = dumpath + "\\" + maldir
            malfiles = os.listdir(malfiledir)

            outpath1 = imagepath + "\\" + maldir
            isExists = os.path.exists(outpath1)
            if not isExists:
                os.makedirs(outpath1)

            for source in malfiles:
                print("\n" + source)
                start = time.time()
                sourcepath = malfiledir + "\\" + source
                targetname = os.path.splitext(source)[0]+ ".png"
                targetpath = outpath1 + "\\" + targetname

                img = generate_image(sourcepath)
                print(f'Image generated from "{sourcepath}"')

                img.save(targetpath, "PNG", compress_level=9)

                print(f'Image stored at "{targetpath}"')

                end = time.time()
                run_time = end - start
                print('Average time={}'.format(run_time))

                if os.path.exists(sourcepath):  # delete the file if it exists
                    os.remove(sourcepath)
                    print('Successflly delete file:%s' % sourcepath)
                else:
                    print('no such file:%s' % sourcepath)

    except KeyboardInterrupt:
        print("Interrupted")