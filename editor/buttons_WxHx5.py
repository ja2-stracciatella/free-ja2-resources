from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import ja2py.fileformats.Sti # load Pillow plugin


BUTTONS_30x30x5 = {
    "ADDROOM.STI": "ADD\nROOM", # not used
    "ADDTILEROOM.STI": "ADD\nTILE\nROOM",
    "BANKS.STI": "BAN\nKS",
    "CANCEL.STI": "CAN\nCEL",
    "CAVES.STI": "CA\nVES",
    "COPYROOM.STI": "COPY\nROOM",
    "CRACKWALL.STI": "CRA\nCK\nWALL",
    "DEBRIS.STI": "DE\nBRIS",
    "DECAL.STI": "DE\nCAL",
    "DECOR.STI": "DE\nCOR",
    "DELROOM.STI": "DEL\nROOM",
    "DOOR.STI": "DOOR",
    "DOWNARROW.STI": "DOWN\nAR\nROW",
    "DOWNGRID.STI": "DOWN\nGRID",
    "ERASER.STI": "ERA\nSER",
    "EXITGRIDBUT.STI": "EXIT\nGRID\nBUT",
    "EXITGRIDQ.STI": "EXIT\nGRID\nQ", # not used
    "EXITGRIDXBUT.STI": "EXIT\nGRID\nXBUT", # not used
    "FAKELIGHT.STI": "FAKE\nLIGHT",
    "FILL.STI": "FILL",
    "FLOOR.STI": "FLO\nOR",
    "KEY.STI": "KEY",
    "KILLTILEROOM.STI": "KILL\nTILE\nROOM",
    "LIGHT.STI": "LI\nGHT",
    "LIGHT2.STI": "LI\nGHT2", # not used
    "LOAD.STI": "LOAD",
    "MOVEROOM.STI": "MOVE\nROOM",
    "NEW.STI": "NEW",
    "NEWROOF.STI": "NEW\nROOF",
    "NEWROOM.STI": "NEW\nROOM",
    "NUM1.STI": "NUM1",
    "NUM2.STI": "NUM2",
    "NUM3.STI": "NUM3", # not used
    "NUM4.STI": "NUM4", # not used
    "OK.STI": "OK",
    "PAINT.STI": "PAI\nNT",
    "ROAD.STI": "ROAD",
    "ROOF.STI": "ROOF",
    "SAVE.STI": "SAVE",
    "SAWROOM.STI": "SAW\nROOM",
    "TILESET.STI": "TILE\nSET",
    "TOILET.STI": "TOI\nLET",
    "TREE.STI": "TREE",
    "UNDO.STI": "UNDO",
    "UPARROW.STI": "UP\nAR\nROW",
    "UPGRID.STI": "UP\nGRID",
    "WALL.STI": "WALL",
    "WINDOW.STI": "WIN\nDOW",
}

BUTTONS_WxHx5 = {
    ("CENTER.STI", 30, 21): "CEN\nTER",
    ("EAST.STI", 30, 20): "EAST",
    ("ISOLATED.STI", 30, 21): "ISOL\nATED",
    ("LEFTARROW.STI", 30, 20): "LEFT\nARR",
    ("LEFTSCROLL.STI", 49, 39): "LEFT\nSCR",
    ("LGDOWNARROW.STI", 28, 41): "LG\nDOWN\nARR",
    ("MERCAPPEARANCE.STI", 34, 26): "MERC\nAPP",
    ("MERCATTRIBUTES.STI", 34, 26): "MERC\nATT",
    ("MERCGENERAL.STI", 34, 26): "MERC\nGEN",
    ("MERCGLOWSCHEDULE.STI", 34, 26): "MERCG\nSCHED",
    ("MERCINVENTORY.STI", 34, 26): "MERC\nINV",
    ("MERCPROFILE.STI", 34, 26): "MERC\nPROF",
    ("MERCSCHEDULE.STI", 34, 26): "MERC\nSCHED",
    ("NORTH.STI", 30, 20): "NOR\nTH",
    ("RIGHTARROW.STI", 30, 20): "RIGHT\nARR",
    ("RIGHTSCROLL.STI", 49, 39): "RIGHT\nSCROLL",
    ("SOUTH.STI", 30, 20) : "SOU\nTH",
    ("WEST.STI", 30, 20): "WEST",
}


def make_button_WxHx5_sti(base, width, height, text, font, color):
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
    images[0].save(buf, format='STCI', save_all=True, flags=['INDEXED', 'ETRLE'], append_images=images[1:])
    return buf


def add_to_free_editorslf(source_fs, target_fs):
    """Make generic 30x30 buttons by drawing text over a button base."""
    font = ImageFont.truetype(source_fs.getsyspath("silkscreen/slkscr.ttf"), 8)
    color = (53,53,53,255)
    buttons_30x30x5 = Image.open(source_fs.getsyspath("buttons_30x30x5.png")).convert('RGBA')
    for filename, text in BUTTONS_30x30x5.items():
        # make button
        buf = make_button_WxHx5_sti(buttons_30x30x5, 30, 30, text, font, color)
        with target_fs.open(filename, 'wb') as f:
            f.write(buf.getbuffer())
    for (filename, width, height), text in BUTTONS_WxHx5.items():
        # create base image from buttons_30x30x5
        assert width <= 28 + 28 and height <= 28 + 28 # 2 pixel border in buttons_30x30x5
        base = Image.new('RGBA', (width*5,height), color=(0, 0, 0, 0))
        x = width // 2
        y = height // 2
        x_pos_to_range = { # position in base => range in 30x30 button
            0: (0,x),
            x: (30+x-width,30),
        }
        y_pos_to_range = { # position in base => range in 30x30 button
            0: (0,y),
            y: (30+y-height,30),
        }
        for y, (y0, y1) in y_pos_to_range.items():
            for x, (x0, x1) in x_pos_to_range.items():
                for i in range(5):
                    base.paste(buttons_30x30x5.crop((x0+i*30,y0,x1+i*30,y1)), (x+i*width,y))
        # make button
        buf = make_button_WxHx5_sti(base, width, height, text, font, color)
        with target_fs.open(filename, 'wb') as f:
            f.write(buf.getbuffer())

