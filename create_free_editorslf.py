import os
import argparse
from PIL import Image
from ja2py.fileformats import load_8bit_sti, save_8bit_sti, SlfFS, BufferedSlfFS
from fs.osfs import OSFS

def main():
    parser = argparse.ArgumentParser(description='Create free editor.slf')
    parser.add_argument('original', help="Original editor.slf")
    parser.add_argument(
        '-o',
        '--output',
        default='build/editor.slf',
        help="Where to store the created slf file"
    )
    args = parser.parse_args()

    if not os.path.exists(os.path.dirname(args.output)):
        os.makedirs(os.path.dirname(args.output))

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
                replacement_path = base_name + '.png'
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
                        replacement_path = replacement_dir + '/{}.png'.format(i)

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
