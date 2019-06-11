from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import ja2py.fileformats.Sti # load Pillow plugin


BUTTONS_30x30x5 = {
    # ADDROOM.STI not used
    "ADDTILEROOM.STI": "ADD\nTILE\nROOM",
    "BANKS.STI": "BANKS",
    "CANCEL.STI": "CANCEL",
    "CAVES.STI": "CAVES",
    "COPYROOM.STI": "COPY\nROOM",
    "CRACKWALL.STI": "CRACK\nWALL",
    "DEBRIS.STI": "DEBRIS",
    "DECAL.STI": "DECAL",
    "DECOR.STI": "DECOR",
    "DELROOM.STI": "DEL\nROOM",
    "DOOR.STI": "DOOR",
    "DOWNARROW.STI": "DOWN\nARROW",
    "DOWNGRID.STI": "DOWN\nGRID",
    "ERASER.STI": "ERASER",
    "EXITGRIDBUT.STI": "EXIT\nGRID\nBUT",
    # EXITGRIDQ.STI not used
    # EXITGRIDXBUT.STI not used
    "FAKELIGHT.STI": "FAKE\nLIGHT",
    "FILL.STI": "FILL",
    "FLOOR.STI": "FLOOR",
    "KEY.STI": "KEY",
    "KILLTILEROOM.STI": "KILL\nTILE\nROOM",
    "LIGHT.STI": "LIGHT",
    # LIGHT2.STI not used
    "LOAD.STI": "LOAD",
    "MOVEROOM.STI": "MOVE\nROOM",
    "NEW.STI": "NEW",
    "NEWROOF.STI": "NEW\nROOF",
    "NEWROOM.STI": "NEW\nROOM",
    "NUM1.STI": "NUM1",
    "NUM2.STI": "NUM2",
    # NUM3.STI not used
    # NUM4.STI not used
    "OK.STI": "OK",
    "PAINT.STI": "PAINT",
    "ROAD.STI": "ROAD",
    "ROOF.STI": "ROOF",
    "SAVE.STI": "SAVE",
    "SAWROOM.STI": "SAW\nROOM",
    "TILESET.STI": "TILE\nSET",
    "TOILET.STI": "TOILET",
    "TREE.STI": "TREE",
    "UNDO.STI": "UNDO",
    "UPARROW.STI": "UP\nARROW",
    "UPGRID.STI": "UP\nGRID",
    "WALL.STI": "WALL",
    "WINDOW.STI": "WINDOW",
}

def add_to_free_editorslf(source_fs, target_fs):
    """Make generic 30x30 buttons by drawing text over a button base."""
    font = ImageFont.truetype(source_fs.getsyspath("silkscreen/slkscr.ttf"), 8)
    for filename, text in BUTTONS_30x30x5.items():
        base = Image.open(source_fs.getsyspath("buttons_30x30x5.png")).convert('RGBA')
        draw = ImageDraw.Draw(base)
        width, height = draw.multiline_textsize(text, font=font, spacing=-1)
        x = (30 - width) // 2
        y = (30 - height) // 2
        images = []
        for i in range(5):
            image = base.crop((i*30, 0, i*30+30, 30))
            image.load()
            draw = ImageDraw.Draw(image)
            draw.multiline_text((x,y), text, fill=(53,53,53,255), font=font, spacing=-1, align='center')
            images.append(image)
        buf = BytesIO()
        images[0].save(buf, format='STCI', save_all=True, flags=['INDEXED', 'ETRLE'], append_images=images[1:])
        with target_fs.open(filename, 'wb') as f:
            f.write(buf.getbuffer())

