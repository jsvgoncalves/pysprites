#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of PySprites.

""" """

from sys import exit

from PIL import Image


def main(images):
    try:
        im = [Image.open(i).convert('RGBA') for i in images]
    except IOError as ioe:
        print('Error: {}'.format(ioe))
        exit(1)

    # Pre processing
    dims = (1, 8)  # cols, rows
    sprite_size = im[0].size  # width, height
    spritesheet_size = ([a * b for a, b in zip(sprite_size, dims)])

    final = Image.new('RGBA', spritesheet_size, (0, 0, 0, 123))

    for i in im:
        final.paste(i, (dims[0] * sprite_size[0], 0))

    # Paste all the images
    try:
        for row in xrange(0, dims[1]):
            for col in xrange(0, dims[0]):
                final.paste(im[dims[0] * row + col],
                            (col * sprite_size[0], row * sprite_size[1]))
    except IndexError as ie:
        print('Error: {}'.format(ie))
        print('Continuing... The rest of the image will be empty')

    # Display image
    # final.show()
    final.save('spritesheet.png')
    print('## Created Spritesheet')
    print('Size: {}\nFormat: {}\nMode: {}'.format(
        final.size, final.format, final.mode))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'image',
        help='images or a folder that contains the images', type=str,
        nargs='+')

    args = parser.parse_args()

    main(images=args.image)
