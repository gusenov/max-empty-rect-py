# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import os
import numpy
from PIL import Image
import sys
import getopt

DEBUGGING = False


def largest(nrows, ncols, im, bgcolor, fgcolor):
    maxarea = (0, [])

    h = numpy.zeros(dtype=int, shape=(nrows, ncols))
    w = numpy.zeros(dtype=int, shape=(nrows, ncols))

    for r in range(nrows):  # y
        for c in range(ncols):  # x
            # Пропускать всё что не подходит под цвет фона:
            if (bgcolor is not None) and im.getpixel((c, r)) != bgcolor:
                continue

            # Пропускать всё что подходит под цвет переднего плана:
            if (fgcolor is not None) and im.getpixel((c, r)) == fgcolor:
                continue

            if r == 0:
                h[r][c] = 1
            else:
                h[r][c] = h[r - 1][c] + 1

            if c == 0:
                w[r][c] = 1
            else:
                w[r][c] = w[r][c - 1] + 1

            minw = w[r][c]
            for dh in range(h[r][c]):
                minw = min(minw, w[r - dh][c])
                area = (dh + 1) * minw
                if area > maxarea[0]:
                    maxarea = (area, [(r - dh, c - minw + 1, r, c)])
    return maxarea


def fill(imgrgb, maxarea, fillcolor):
    pixels = imgrgb.load()
    for i in range(maxarea[1][0][0], maxarea[1][0][2]):
        for j in range(maxarea[1][0][1], maxarea[1][0][3]):
            pixels[j, i] = fillcolor
    return imgrgb


def main(argv):
    img = None
    outputfile = None
    fillcolor = (255, 0, 0)
    bgcolor = None
    fgcolor = None

    try:
        opts, args = getopt.getopt(argv, "i:o:f:e:b:", ["input=", "output=", "fill=", "empty=", "busy="])
    except getopt.GetoptError:

        print('rect.py --input <input/image> --output <output/image> --fill <color> --empty <color>')
        print('rect.py -i <input/image> -o <output/image> -f <color> -e <color>')

        print('rect.py --input <input/image> --output <output/image> --fill <color> --busy <color>')
        print('rect.py -i <input/image> -o <output/image> -f <color> -b <color>')

        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print('rect.py -i <input/image> -o <output/image> -f <color> -e <color>')
            print('rect.py -i <input/image> -o <output/image> -f <color> -b <color>')
            sys.exit()
        elif opt == "--help":
            print('rect.py --input <input/image> --output <output/image> --fill <color> --empty <color>')
            print('rect.py --input <input/image> --output <output/image> --fill <color> --busy <color>')
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
            img = Image.open(inputfile).convert('RGB')
            if DEBUGGING:
                print('Image Width: %d\nImage Height: %d' % img.size)
        elif opt in ("-o", "--output"):
            outputfile = arg
        elif opt in ("-f", "--fill"):
            fillcolor = tuple(map(int, arg.split(',')))
        elif opt in ("-e", "--empty"):
            bgcolor = tuple(map(int, arg.split(',')))
        elif opt in ("-b", "--busy"):
            fgcolor = tuple(map(int, arg.split(',')))

    width, height = img.size
    maxarea = largest(height, width, img, bgcolor, fgcolor)
    print(maxarea)  # (S, [(y1, x1, y2, x2)])

    if DEBUGGING:
        print('Maximum-area empty rectangle: %d' % maxarea[0])
        for t in maxarea[1]:
            print('Upper-left Point: ({}, {})\nLower-right Point: ({}, {})'.format(*t))

    if outputfile:
        imgrgb = fill(img, maxarea, fillcolor)
        imgrgb.save(outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
