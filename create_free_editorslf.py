import os
import argparse
import json
import sys
from PIL import Image
from ja2py.content import Images8Bit, SubImage8Bit
from ja2py.fileformats import load_8bit_sti, save_8bit_sti, SlfFS, BufferedSlfFS
from fs.osfs import OSFS

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

def same_palette(subimages):
    """Returns true if all the images use the same palette"""
    palette = None
    for img in subimages:
        if img is None:
            return False # empty image
        if img.mode != 'P':
            return False # no palette
        if palette is None:
            palette = img.palette
        elif palette != img.palette:
            return False # different palette
    return True

def normalize_subimages(subimages):
    """Make sure all subimages have the same palette."""

    if same_palette(subimages):
        print("same palette")
        return subimages

    # paste to RGBA canvas
    transparent = (0, 0, 0, 0) # ja2py STI assumes color 0 is transparent?
    boxes = list()
    mode = 'RGBA'
    for img in subimages:
        if len(boxes) > 0:
            # place at the right of the last image
            x = boxes[-1][2]
            boxes.append((x, 0, x + img.width, img.height))
        else:
            # place at origin
            boxes.append(img.getbbox())
    width = max([box[2] for box in boxes])
    height = max([box[3] for box in boxes])
    canvas = Image.new(mode, (width, height), transparent)
    for i in range(len(boxes)):
        canvas.paste(subimages[i], boxes[i])

    # convert to RGB palette
    palette = [ transparent[:3] ] # ja2py ETRLE assumes palette index 0 is transparent?
    index = { transparent: 0 }
    data = []
    for rgba in canvas.getdata():
        value = index.get(rgba)
        if value is None:
            if rgba[3] < 255:
                value = transparent # TODO maybe opaque color if alpha >= X?
                print("WARNING ja2py STI does not support alpha channel, converting all {0} to {1}".format(rgba, value))
                index[rgba] = value
            else:
                value = len(palette)
                assert value < 256, "too many colors for an exact match"
                palette.append(rgba[:3])
                index[rgba] = value
        if isinstance(value, list):
            value = index[value] # was converted to another value
            assert not isinstance(value, list), "double convertion"
        data.append(value)
    palette = [x for rgb in palette for x in rgb]
    palette += [0] * (256 * 3 - len(palette)) # palette must have exactly 256 values
    canvas = Image.new('P', (width, height), 0)
    canvas.putpalette(palette)
    canvas.putdata(data)

    # get subimages
    subimages = [canvas.crop(box).copy() for box in boxes]
    return subimages

def create_8bit_sti(fs, spec, dirpath):
    """
    Create an 8bit sti (palette) matching the spec.

    Spec in json:
        {
            "comment": "this is a sample spec",
            "comment-image": "image at this level represents the default image, paths are relative to the directory of the spec",
            "comment-subimages": "subimages describes how to create each subimage",
            "image": "path/to/image.gif",
            "subimages": [
                { "comment": "default image" },
                { "crop": [0, 0, 30, 30], "comment": "section of the default image" },
                { "image": "path/to/other/image.gif", "comment": "image" },
                { "image": "path/to/other/image.gif", "crop": [0, 0, 30, 30], "comment": "section of the image" },
                { "new": ["RGB", [30, 30], "black"], "comment": "new image with positional arguments, see Image.new" },
                { "new": {"mode": "RGB", "size": [30, 30], "color": "black"}, "comment": "new image with named arguments" }
            ]
        }
    """
    # get all subimages
    subimages = list()
    default_path = spec.get('image')
    for subimage_spec in spec.get('subimages', []):
        new = subimage_spec.get('new') # mode, (width, height), color=0 - parameters of Image.new, color is optional
        if new is not None:
            # create new image
            if isinstance(new, dict):
                # with names arguments
                img = Image.new(**new)
            elif isinstance(new, list):
                # with positional arguments
                img = Image.new(*new)
            else:
                assert False, "invalid new argument {0}".format(new)
        else:
            # open existing image
            path = subimage_spec.get('image', default_path)
            assert path is not None, "subimage is empty"
            with fs.open(dirpath + path, 'rb') as f:
                img = Image.open(f).copy()
        # crop image (optional)
        box = subimage_spec.get('crop') # (left, upper, right, lower) - pixel coordinates
        if box:
            img = img.crop(tuple(box))
        subimages.append(img)
    assert len(subimages) > 0, "0 subimages not supported"
    subimages = normalize_subimages(subimages)
    # create sti
    palette = subimages[0].palette
    subimages = [SubImage8Bit(img) for img in subimages]
    sti = Images8Bit(subimages, palette)
    return sti

def main():
    parser = argparse.ArgumentParser(description='Create free editor.slf')
    parser.add_argument('--original', help="Original editor.slf")
    parser.add_argument(
        '-o',
        '--output',
        default='build/editor.slf',
        help="Where to store the created slf file"
    )
    args = parser.parse_args()

    if not os.path.exists(os.path.dirname(args.output)):
        os.makedirs(os.path.dirname(args.output))

    if args.original is None:
        # create editor.slf exclusively from the contents of the editor directory
        source_fs = OSFS('editor')
        target_fs = BufferedSlfFS()
        target_fs.library_name = "Free EDITOR.SLF"
        target_fs.library_path = "editor\\"
        target_fs.version = 0x0200 # 2.0?
        target_fs.sort = 0xffff # sorted?
        for path in source_fs.walkfiles():
            if path.endswith(".json"):
                print("editor" + path)
                # build
                with source_fs.open(path, 'rb') as f:
                    spec = json.loads(f.read().decode("utf-8"))
                dirpath = path[:path.rindex('/') + 1]
                assert dirpath == "/", "BufferedSlfFS does not support makedir"
                sti = create_8bit_sti(source_fs, spec, dirpath)
                # write
                path = path[:-5]
                with target_fs.open(path, 'wb') as f:
                    save_8bit_sti(sti, f)

        with open(args.output, 'wb') as target_file:
            target_fs.save(target_file)
        return

    # create editor.slf by replacing images in the original editor.slf
    target_fs = BufferedSlfFS()
    replacement_fs = OSFS('editor')
    with open(args.original, 'rb') as source_file:
        source_fs = SlfFS(source_file)

        target_fs.library_name = source_fs.library_name
        target_fs.library_path = source_fs.library_path
        target_fs.version = source_fs.version
        target_fs.sort = source_fs.sort

        for directory in source_fs.walkdirs():
            if directory == '/':
                continue
            target_fs.makedir(directory)
        for file in source_fs.walkfiles():
            base_name, _ = os.path.splitext(file)
            with source_fs.open(file, 'rb') as source, target_fs.open(file, 'wb') as target:
                ja2_images = load_8bit_sti(source)
                replacement_path = base_name + '.gif'
                replacement_file_exists = replacement_fs.isfile(replacement_path)
                replacement_dir = file
                replacement_dir_exists = replacement_fs.isdir(replacement_dir)
                if len(ja2_images) == 1 and replacement_file_exists:
                    print("Replacing {0} with {1}".format(file, replacement_path))
                    replacement_img = Image.open(replacement_fs.open(replacement_path, 'rb'))
                    ja2_images._palette = replacement_img.palette
                    ja2_images.images[0]._image = replacement_img
                elif len(ja2_images) > 1 and replacement_dir_exists:
                    for i in range(len(ja2_images)):
                        replacement_path = replacement_dir + '/{}.gif'.format(i)

                        print("Replacing {0} with {1}".format(file, replacement_path))
                        replacement_img = Image.open(replacement_fs.open(replacement_path, 'rb'))
                        ja2_images._palette = replacement_img.palette
                        ja2_images.images[i]._image = replacement_img
                else:
                    print("Replacing {0} with nothingness".format(file))
                    for sub_image in ja2_images.images:
                        width, height = sub_image.image.size
                        sub_image._image = Image.new('P', (width, height), color=54)

                save_8bit_sti(ja2_images, target)

    with open(args.output, 'wb') as target_file:
        target_fs.save(target_file)


if __name__ == "__main__":
    main()
