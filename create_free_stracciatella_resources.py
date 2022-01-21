import os
import argparse
import sys
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import ja2py.fileformats.Sti # load Pillow plugin


if sys.version_info[0] < 3 or sys.version_info[1] < 5:
    print("This script requires Python>=3.5")
    exit(1)

def make_not_found_graphic(width, height, font_size, text):
    font = ImageFont.truetype("editor/silkscreen/slkscr.ttf", font_size)
    color = (255,0,255,255)
    base = Image.new('RGBA', (width,height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    text_width, text_height = draw.multiline_textsize(text, font=font, spacing=-1)
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    images = []
    for i in range(5):
        image = base.crop((i*width, 0, i*width+width, height))
        image.load()
        draw = ImageDraw.Draw(image)
        draw.multiline_text((x,y), text, fill=color, font=font, spacing=-1, align='center')
        images.append(image)
    buf = BytesIO()
    images[0].save(buf, format='STCI', flags=['INDEXED', 'ETRLE'], semi_transparent="opaque")
    return buf

def main():
    parser = argparse.ArgumentParser(description='Create free stracciatella resources')
    parser.add_argument('--original', help="Original editor.slf")
    parser.add_argument(
        '-o',
        '--output',
        default='build/stracciatella',
        help="Where to store the created files"
    )
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    not_found_small_small_pocket = make_not_found_graphic(25, 15, 8, "IMG\nMISS")
    with open(f"{args.output}/inventory-graphic-not-found-small-sp.sti", 'wb') as target_file:
        target_file.write(not_found_small_small_pocket.getvalue())
    not_found_small_big_pocket = make_not_found_graphic(50, 25, 11, "IMAGE\nMISSING")
    with open(f"{args.output}/inventory-graphic-not-found-small-bp.sti", 'wb') as target_file:
        target_file.write(not_found_small_big_pocket.getvalue())
    not_found_big = make_not_found_graphic(100, 50, 18, "IMAGE\nMISSING")
    with open(f"{args.output}/inventory-graphic-not-found-big.sti", 'wb') as target_file:
        target_file.write(not_found_big.getvalue())


if __name__ == "__main__":
    main()
