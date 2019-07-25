from io import BytesIO
from PIL import Image, ImageDraw, ImageColor
import ja2py.fileformats.Sti # load Pillow plugin


CHECKBOXES = [ "CHECKBOX.STI", "SMCHECKBOX.STI" ]


def add_CHECKBOX_SMCHECKBOX_STI(source_fs, target_fs):
    for checkbox in CHECKBOXES:
        images = [Image.open(BytesIO(source_fs.getcontents("%s/%d.gif" % (checkbox, i)))) for i in range(4)]
        buf = BytesIO()
        images[0].save(buf, format='STCI', save_all=True, flags=['INDEXED', 'ETRLE'], append_images=images[1:])
        with target_fs.open(checkbox, 'wb') as f:
            f.write(buf.getbuffer())


def add_RADIOBUTTON_STI(source_fs, target_fs):
    pencil = ImageColor.getrgb('#3a3a3a')
    images = [None] * 4
    # normal
    normal = ImageColor.getrgb('#f3f3f3')
    image = Image.new('RGBA', (12,12), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.ellipse([(1,1), (11,11)], fill=normal, outline=pencil)
    images[0] = image.copy()
    draw.ellipse([(4,4), (8,8)], fill=pencil, outline=pencil)
    images[2] = image
    # hilite
    hilite = ImageColor.getrgb('#b9b9b9')
    draw = ImageDraw.Draw(image)
    draw.ellipse([(1,1), (11,11)], fill=hilite, outline=pencil)
    images[1] = image.copy()
    draw.ellipse([(4,4), (8,8)], fill=pencil, outline=pencil)
    images[3] = image
    buf = BytesIO()
    images[0].save(buf, format='STCI', save_all=True, flags=['INDEXED', 'ETRLE'], append_images=images[1:])
    with target_fs.open("RADIOBUTTON.STI", 'wb') as f:
        f.write(buf.getbuffer())


def add_to_free_editorslf(source_fs, target_fs):
    add_CHECKBOX_SMCHECKBOX_STI(source_fs, target_fs)
    add_RADIOBUTTON_STI(source_fs, target_fs)

