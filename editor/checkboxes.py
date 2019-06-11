from io import BytesIO
from PIL import Image
import ja2py.fileformats.Sti # load Pillow plugin

CHECKBOXES = [ "CHECKBOX.STI", "SMCHECKBOX.STI" ]

def add_to_free_editorslf(source_fs, target_fs):
    for checkbox in CHECKBOXES:
        images = [Image.open(BytesIO(source_fs.getcontents("%s/%d.gif" % (checkbox, i)))) for i in range(4)]
        buf = BytesIO()
        images[0].save(buf, format='STCI', save_all=True, flags=['INDEXED', 'ETRLE'], append_images=images[1:])
        with target_fs.open(checkbox, 'wb') as f:
            f.write(buf.getbuffer())

