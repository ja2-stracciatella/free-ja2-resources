import os
import argparse
import json
import sys
import hashlib
from importlib.util import spec_from_file_location, module_from_spec
from fs.osfs import OSFS
from ja2py.content import Images8Bit, SubImage8Bit
from ja2py.fileformats import load_8bit_sti, save_8bit_sti, SlfFS, BufferedSlfFS


if sys.version_info[0] < 3 or sys.version_info[1] < 5:
    print("This script requires Python>=3.5")
    exit(1)


def create_free_editorslf(name):
    """
    Creates a BufferedSlfFS exclusively from the contents of the editor directory.

    The python files inside the editor directory are responsible for creating the STI images and adding them to the SLF.

    Each file should contain the function:
    ```
    def add_to_free_editorslf(source_fs, target_fs):
        pass
    ```
    source_fs is the source OSFS (editor directory)
    target_fs is the target BufferedSlfFS
    """
    target_fs = BufferedSlfFS()
    target_fs.library_name = name or "Free editor.slf"
    target_fs.library_path = "editor\\"
    target_fs.version = 0x0200 # 2.0
    target_fs.sort = 0 # BufferedSlfFS does not guarantee that the entries are sorted
    source_fs = OSFS('editor')
    for path in source_fs.walkfiles():
        if path.endswith(".py"):
            # run python file inside the editor directory
            name = ("editor" + path)[:-3].replace("/", ".")
            spec = spec_from_file_location(name, source_fs.getsyspath(path))
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            module.add_to_free_editorslf(source_fs, target_fs)
    for path in sorted(target_fs.walkfiles()):
        print(path)
    return target_fs


def generate_md5_file(slf_filename):
    m = hashlib.md5()
    with open(slf_filename, "rb") as f:
        m.update(f.read())
    md5_filename = slf_filename + ".md5"
    md5 = m.hexdigest()
    with open(md5_filename, "wb") as f:
        f.write(bytes(md5, "utf-8"))
    print("MD5: %s" % md5)


def main():
    parser = argparse.ArgumentParser(description='Create free editor.slf')
    parser.add_argument('--original', help="Original editor.slf")
    parser.add_argument(
        '-o',
        '--output',
        default='build/editor.slf',
        help="Where to store the created slf file"
    )
    parser.add_argument('--name', help="Library name")
    args = parser.parse_args()

    if not os.path.exists(os.path.dirname(args.output)):
        os.makedirs(os.path.dirname(args.output))

    if args.original is None:
        target_fs = create_free_editorslf(args.name)
        with open(args.output, 'wb') as target_file:
            target_fs.save(target_file)
        generate_md5_file(args.output)
        return

    # create editor.slf by replacing images in the original editor.slf
    target_fs = BufferedSlfFS()
    replacement_fs = OSFS('editor')
    with open(args.original, 'rb') as source_file:
        source_fs = SlfFS(source_file)

        target_fs.library_name = args.name or source_fs.library_name
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
    generate_md5_file(args.output)


if __name__ == "__main__":
    main()
