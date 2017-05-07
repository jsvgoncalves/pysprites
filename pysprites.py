#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of PySprites.

""" """

from __future__ import division
from sys import exit
from os import path, listdir
from os.path import join as osp
from math import ceil

from PIL import Image


def get_from_folder(name, ext='.png'):
    """Return a list of images contained on the given folder.

    Args:
        name (str): The folder name
        ext (str, optional): The file extension to filter the images

    Returns:
        list(srt): A list with the paths to all the images
    """
    filelist = [osp(name, f) for f in listdir(name) if f.endswith(ext)]
    return filelist


def main(sources, output='spritesheet.png', cols=None):
    """PySprites entry point.

    Args:
        sources (str): A list of sources or a folder
        output (str, optional): Destination file
        cols (int, optional): Number of columns of the spritesheet
    """

    # Arguments or defaults
    # Note: The arguments can't be set as default, as None is passed
    #       by ArgumentParser().
    if cols is None:
        cols = 2  # cols, rows
    if output is None:
        output = 'spritesheet.png'

    # If `sources` is a folder, get the contents
    if path.isdir(sources[0]):
        sources = get_from_folder(sources[0])

    # Open all the images with PIL
    try:
        im = [Image.open(i).convert('RGBA') for i in sources]
    except IOError as ioe:
        print('Error: {}'.format(ioe))
        exit(1)

    # Pre-computer sizes and dimensions
    dims = (cols, int(ceil(len(im) / cols)))  # rows = total_images / columns
    # !TODO: Add option to have sprites of multiple sizes
    sprite_size = im[0].size  # width, height
    # spritesheet_size = (cols, rows) x (sprite_width, sprite_height)
    spritesheet_size = ([a * b for a, b in zip(sprite_size, dims)])

    # Generate final Image and paste in the sprites
    final = Image.new('RGBA', spritesheet_size, (0, 0, 0, 123))
    try:
        for row in xrange(0, dims[1]):
            for col in xrange(0, dims[0]):
                final.paste(im[dims[0] * row + col],
                            (col * sprite_size[0], row * sprite_size[1]))

    # !TODO: Fix this when `len(im)%cols > 0`
    # Note: This always happens when the final spritesheet will contain empty
    #       columns at the end.
    except IndexError as ie:
        print('Error: {}'.format(ie))
        print('Continuing... The rest of the image will be empty')

    final.save(output)

    print("# Created Spritesheet '{}' ({} x {} px)".format(
        output, final.size[0], final.size[1]))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'sources',
        help='images or a folder that contains the images', type=str,
        nargs='+')
    parser.add_argument(
        '-o', '--output',
        help='output to given file\
        \nDEFAULT: spritesheet.png')
    parser.add_argument(
        '-c', '--columns',
        help='number of columns per row, \
        \ne.g.: -c 4\
        \nDEFAULT: 2',
        type=int)
    args = parser.parse_args()

    main(sources=args.sources, output=args.output, cols=args.columns)
