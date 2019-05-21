import os
import argparse
import json
from PIL import Image
from ja2py.content import Images8Bit, SubImage8Bit
from ja2py.fileformats import load_8bit_sti, save_8bit_sti, SlfFS, BufferedSlfFS
from fs.osfs import OSFS

def same_palette(subimages):
    """Returns true if all the images use the same palette"""
    palette = None
    for img in subimages:
        if img is None:
            return False # empty image
        if img.mode != 'P':
            return False # no palette
        if palette == None:
            palette = img.palette
        elif palette != img.palette:
            return False # different palette
    return True

def normalize_subimages(subimages):
    """Make sure all subimages have the same palette."""

    if same_palette(subimages):
        print("same palette")
        return subimages

    # paste in RGB canvas
    color = None
    boxes = list()
    mode = 'RGB'
    for img in subimages:
        if img.mode == 'RGBA' or (img.mode == 'P' and img.palette.mode == 'RGBA'):
            print("WARNING ja2py does not support alpha channel in STIs, alpha channel will be lost")
        if color is None and img.width > 0 and img.height > 0:
            pass # TODO how do I get a color?
        if len(boxes) > 0:
            # place at the right of the last image
            x = boxes[-1][2]
            boxes.append((x, 0, x + img.width, img.height))
        else:
            # place at origin
            boxes.append(img.getbbox())
    if color is None:
        color = 0 # default of Image.new
    width = max([box[2] for box in boxes])
    height = max([box[3] for box in boxes])
    canvas = Image.new(mode, (width, height), color)
    for i in range(len(boxes)):
        canvas.paste(subimages[i], boxes[i])

    # convert to palette
    assert canvas.getcolors(256) is not None, "too many palette colors"
    canvas = canvas.convert(mode='P', palette='ADAPTATIVE', colors=256)
    subimages = [canvas.crop(box).copy() for box in boxes]
    return subimages

def create_sti(fs, spec):
    # get all subimages
    subimages = list()
    default_path = spec.get('image')
    for subimage_spec in spec.get('subimages', []):
        path = subimage_spec.get('image', default_path)
        assert path is not None, "empty subimages not supported"
        with fs.open(path, 'rb') as f:
            img = Image.open(f).copy()
        box = subimage_spec.get('crop') # left, upper, right, and lower pixel coordinate
        if box:
            img = img.crop(tuple(box))
        subimages.append(img)
    assert len(subimages) > 0, "0 subimages not supported"
    if not same_palette(subimages):
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
                    spec = json.load(f)
                sti = create_sti(source_fs, spec)
                # write
                path = path[:-5]
                with target_fs.open(path, 'wb') as f:
                    save_8bit_sti(sti, f)
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
