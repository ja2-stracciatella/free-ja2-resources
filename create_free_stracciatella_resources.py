import os
import argparse
import sys
import colorsys
import time
import math
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import ja2py.fileformats.Sti # load Pillow plugin

if sys.version_info[0] < 3 or sys.version_info[1] < 5:
    print("This script requires Python>=3.5")
    exit(1)

class AutoIndexedImage():
    def __init__(self):
        self.images = []
    
    def append(self, image):
        self.images.append(image)

    def to_image(self):
        total_width = max([i.width for i in self.images])
        total_height = sum([i.height for i in self.images])
        image = Image.new('RGBA', (total_width,total_height), color=(0, 0, 0, 0))
        current_y = 0
        for i in self.images:
            image.paste(i, (0, current_y))
            current_y += i.height
        return image.convert('P', palette=Image.ADAPTIVE, colors=255).convert('RGBA')

    def to_indexed_stci(self):
        indexed = []
        image = self.to_image()
        current_y = 0
        for i in self.images:
            sub = image.copy().crop((0, current_y, i.width, current_y+i.height))
            indexed.append(sub)
            current_y += i.height

        buf = BytesIO()
        indexed[0].save(buf, format='STCI', flags=['INDEXED', 'ETRLE'], semi_transparent="opaque", append_images=indexed[1:])
        return buf        

    def to_png(self):
        image = self.to_image()
        buf = BytesIO()
        image.save(buf, format='PNG')
        return buf

    def save(self, filename, format='stci'):
        data = self.to_indexed_stci() if format == 'stci' else self.to_png()
        with open(filename, 'wb') as target_file:
            target_file.write(data.getvalue())        


def make_not_found_graphic(width, height, font_size, text):
    auto_indexed = AutoIndexedImage()
    font = ImageFont.truetype("editor/silkscreen/slkscr.ttf", font_size)
    color = (255,0,255,255)
    image = Image.new('RGBA', (width,height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.multiline_textsize(text, font=font, spacing=-1)
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.multiline_text((x,y), text, fill=color, font=font, spacing=-1, align='center')
    auto_indexed.append(image)
    return auto_indexed

def apply_rgb_noise(width, height, pixel_map, strength):
        for x in range(width):
            for y in range(height):
                random = np.random.normal(1.0, strength, 3)
                rgb = pixel_map[x, y]
                pixel_map[x, y] = (int(rgb[0] * random[0]), int(rgb[1] * random[1]), int(rgb[2] * random[2]))

def modify_hls(rgb, luminescense_multiplier, saturation_multiplier):
    hls = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    return colorsys.hls_to_rgb(int(hls[0]), int(hls[1] * luminescense_multiplier), int(hls[2] * saturation_multiplier))

def apply_border(width, height, pixel_map, border_width, outset):
    # Light borders
    top_right_border_luminescense = [2, 2.5, 3] if outset else [0.7, 0.8, 0.9]
    top_right_border_saturation = [0.8, 0.7, 0.6] if outset else [0.8, 0.9, 1.]
    # Top border
    start = 1
    for y in range(border_width):
        for x in range(start, width-start):
            pixel_map[x, y] = modify_hls(pixel_map[x, y], top_right_border_luminescense[y], top_right_border_saturation[y])
        start += 1
    # Right border
    start = 0
    for offset_x in range(border_width):
        for y in range(start, height-start):
            x = width - 1 - offset_x
            pixel_map[x, y] = modify_hls(pixel_map[x, y], top_right_border_luminescense[offset_x], top_right_border_saturation[offset_x])
        start += 1

    # Dark borders
    bottom_right_border_luminescense = [0.7, 0.8, 0.9] if outset else [2, 2.5, 3]
    borrom_right_border_saturation = [0.8, 0.9, 1.] if outset else [0.8, 0.9, 1.]
    # Left border
    start = 0
    for x in range(border_width):
        for y in range(start, height-start):
            pixel_map[x, y] = modify_hls(pixel_map[x, y], bottom_right_border_luminescense[x], borrom_right_border_saturation[x])
        start += 1
    # Bottom border
    start = 1
    for offset_y in range(border_width):
        for x in range(start, width-start):
            y = height - 1 - offset_y
            pixel_map[x, y] = modify_hls(pixel_map[x, y], bottom_right_border_luminescense[offset_y], borrom_right_border_saturation[offset_y])
        start += 1
    # Bottom border highlight
    for x in range(border_width, width - border_width):
        y = height - border_width - 1
        pixel_map[x, y] = modify_hls(pixel_map[x, y], 1.1, 1.0)

def make_standard_button(width, height, background_color, border_width):
    base = Image.new('RGB', (width,height), color=background_color)
    pixel_map = base.load()

    # Rgb noise
    apply_rgb_noise(width, height, pixel_map, 0.1)

    images = []
    for outset in [True, False]:
        image = base.copy()
        pixel_map = image.load()
        apply_border(width, height, pixel_map, border_width, outset)
        images.append(image)

    return images

def make_save_load_screen_additions():
    auto_indexed = AutoIndexedImage()

    item_default = Image.open("sources/save-load-item-default.png")
    item_selected = Image.open("sources/save-load-item-selected.png")
    auto_indexed.append(item_default)
    auto_indexed.append(item_selected)

    skull_default = Image.open("sources/skull-sharp-default.png")
    skull_selected = Image.open("sources/skull-sharp-selected.png")
    skull_highlighted = Image.open("sources/skull-sharp-highlighted.png")
    auto_indexed.append(skull_default)
    auto_indexed.append(skull_selected)
    auto_indexed.append(skull_highlighted)

    return auto_indexed

def make_scroll_bar():
    border_color = (40, 40, 40, 255)
    text_color = (155, 155, 155, 255)

    auto_indexed = AutoIndexedImage()

    width, height = 23, 23
    standard_button = make_standard_button(width, height, "#312921", 2)
    
    # triangle coordinates
    left = math.floor(width * 0.33)
    center = math.floor(width / 2)
    right = math.ceil(width * 0.66)
    top = math.floor(height * 0.33)
    bottom = math.ceil(height * 0.66)

    # up button
    btn = [standard_button[0].copy(), standard_button[1].copy()]
    draw = ImageDraw.Draw(btn[0])
    draw.polygon([(center + 1, top + 1), (right + 1, bottom + 1), (left + 1, bottom + 1)], outline="black", fill="black")
    draw.polygon([(center, top), (right, bottom), (left, bottom)], outline=text_color, fill=text_color)
    draw = ImageDraw.Draw(btn[1])
    draw.polygon([(center + 2, top + 2), (right + 2, bottom + 2), (left + 2, bottom + 2)], outline="black", fill="black")
    draw.polygon([(center + 1, top + 1), (right + 1, bottom + 1), (left + 1, bottom + 1)], outline=text_color, fill=text_color)
    auto_indexed.append(btn[0].convert("RGBA"))
    auto_indexed.append(btn[1].convert("RGBA"))

    # down button
    btn = [standard_button[0].copy(), standard_button[1].copy()]
    draw = ImageDraw.Draw(btn[0])
    draw.polygon([(center + 1, bottom + 1), (left + 1, top + 1), (right + 1, top + 1)], outline="black", fill="black")
    draw.polygon([(center, bottom), (left, top), (right, top)], outline=text_color, fill=text_color)
    draw = ImageDraw.Draw(btn[1])
    draw.polygon([(center + 2, bottom + 2), (left + 2, top + 2), (right + 2, top + 2)], outline="black", fill="black")
    draw.polygon([(center + 1, bottom + 1), (left + 1, top + 1), (right + 1, top + 1)], outline=text_color, fill=text_color)
    auto_indexed.append(btn[0].convert("RGBA"))
    auto_indexed.append(btn[1].convert("RGBA"))

    scrollbar = Image.new('RGBA', (width,height), color=(0, 0, 0, 255))
    scrollbar_pixel_map = scrollbar.load()
    for y in range(height):
        scrollbar_pixel_map[0, y] = border_color
        scrollbar_pixel_map[width-1, y] = border_color
    auto_indexed.append(scrollbar)

    scrollbar_indicator = make_standard_button(width-4, height-4, "#312921", 2)
    auto_indexed.append(scrollbar_indicator[0])

    return auto_indexed     

def main():
    parser = argparse.ArgumentParser(description='Create free stracciatella resources')
    parser.add_argument('--original', help="Original editor.slf")
    parser.add_argument(
        '-o',
        '--output',
        default='build/stracciatella',
        help="Where to store the created files"
    )
    parser.add_argument(
        '-f',
        '--format',
        default='stci',
        choices=['stci', 'png'],
        help="What kind of images to store"
    )
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)
    extension = 'sti'
    if args.format != 'stci':
        extension = 'png'

    # Inventory not found graphics
    make_not_found_graphic(25, 15, 8, "IMG\nMISS").save(f"{args.output}/inventory-graphic-not-found-small-sp.{extension}", args.format)
    make_not_found_graphic(50, 25, 11, "IMAGE\nMISSING").save(f"{args.output}/inventory-graphic-not-found-small-bp.{extension}", args.format)
    make_not_found_graphic(100, 50, 18, "IMAGE\nMISSING").save(f"{args.output}/inventory-graphic-not-found-big.{extension}", args.format)

    # Save/Load Screen
    make_save_load_screen_additions().save(f"{args.output}/save-load-addons.{extension}", args.format)

    # Generic iron scroll bar
    make_scroll_bar().save(f"{args.output}/scroll-bar.{extension}", args.format)

if __name__ == "__main__":
    main()
