#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 date:3/6/2022
 author:Cla1r3
 Cut image to sub-images.
"""

import os
from PIL import Image
import time

def splitimage(src, rownum, colnum, dstpath, overlap_pix,dump_image):
    if os.path.exists(src):
        print('File exist')
    else:
        print('File not exist')
        return

    if os.path.isdir(dstpath):
        print('Directory exist')
        pass
    else:
        print('Directory not exist, create one')
        os.mkdir(dstpath)
    Image.MAX_IMAGE_PIXELS = None
    img = Image.open(src)
    img1 = img.resize((4480,4480), Image.ANTIALIAS)

    w, h = img1.size

    if rownum <= h and colnum <= w:
        print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))

        s = os.path.split(src)
        if dstpath == '':
            dstpath = s[0]
        fn = s[1].split('.')

        ext = fn[-1]

        num = 0

        rowheight = h // (rownum - overlap_pix) + 1
        colwidth = w // (colnum - overlap_pix) + 1

        for r in range(rowheight):
            for c in range(colwidth):

                Lx = (c * colnum) - overlap_pix * c
                Ly = (r * rownum) - overlap_pix * r

                if (Lx <= 0):
                    Lx = 0

                if (Ly <= 0):
                    Ly = 0

                Rx = Lx + colnum
                Ry = Ly + rownum

                box = (Lx, Ly, Rx, Ry)
                img.crop(box).save(os.path.join(dstpath, dump_image+'_'+str(Lx) + '_' + str(Ly) + '_' + str(num) + '.' + ext))
                # crop(left, upper, right, lower) 名字中带有图像坐标
                num = num + 1

        print('The image is cut and a total of %s of small images are generated.' % num)
    else:
        print('Illegal row cut parameter!')


def main():
    start = time.time
    dump_image_path =r"Your rgb image file <directory name>"
    save_path =r"Your sub-img file <directory name>"
    row = 224
    col = 224
    overlap_pix = 0
    dump_image_dir = os.listdir(dump_image_path )

    for dump_image in  dump_image_dir :
        dump_image_dir = dump_image_path + "\\" + dump_image
        save_path1 = save_path+ "\\" + dump_image.split('.')[0]
        splitimage(dump_image_dir, row, col, save_path1, overlap_pix,dump_image)


    end = time.time()
    run_time = end - start
    print('Total cut photo time={}'.format(run_time))

if __name__ == '__main__':
    main()