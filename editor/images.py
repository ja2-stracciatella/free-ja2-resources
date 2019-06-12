from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageColor
import ja2py.fileformats.Sti # load Pillow plugin


def make_glow_text_image(width, height, text, font, color, glow):
    glow_offsets = [
        (-1,-1),
        (-1,0),
        (-1,1),
        (0,-1),
        (0,1),
        (1,-1),
        (1,0),
        (1,1),
    ]
    image = Image.new('RGBA', (width,height), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.multiline_textsize(text, font=font, spacing=-1)
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    for off_x, off_y in glow_offsets:
        draw.multiline_text((x+off_x,y+off_y), text, fill=glow, font=font, spacing=-1, align='center')
    draw.multiline_text((x,y), text, fill=color, font=font, spacing=-1, align='center')
    return image


def add_ARROWSOFF_ARROWSON_STI(source_fs, target_fs):
    def make_arrows_sti(font, color, glow):
        arrows = [
            (29, 29, "NW"),
            (30, 30, "N"),
            (29, 29, "NE"),
            (30, 30, "E"),
            (29, 29, "SE"),
            (30, 30, "S"),
            (29, 29, "SW"),
            (30, 30, "W"),
        ]
        images = []
        for width, height, text in arrows:
            image = make_glow_text_image(width, height, text, font, color, glow)
            images.append(image)
        buf = BytesIO()
        images[0].save(buf, format='STCI', save_all=True, flags=['INDEXED', 'ETRLE'], semi_transparent='opaque', append_images=images[1:])
        return buf
    font = ImageFont.truetype(source_fs.getsyspath("silkscreen/slkscr.ttf"), 8)
    color = ImageColor.getrgb('#353535')
    glow_dark = ImageColor.getrgb('#b3995f')
    glow_light = ImageColor.getrgb('#ffeaba')
    buf = make_arrows_sti(font, color, glow_dark)
    with target_fs.open("ARROWSOFF.STI", 'wb') as f:
        f.write(buf.getbuffer())
    buf = make_arrows_sti(font, color, glow_light)
    with target_fs.open("ARROWSON.STI", 'wb') as f:
        f.write(buf.getbuffer())


def add_BIGX_STI(source_fs, target_fs):
    color = ImageColor.getrgb('#CC4233')
    image = Image.new('RGBA', (29,29), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.line([(2,2), (27,27)], color, 3)
    draw.line([(2,27), (27,2)], color, 3)
    buf = BytesIO()
    image.save(buf, format='STCI', flags=['INDEXED', 'ETRLE'])
    with target_fs.open("BIGX.STI", 'wb') as f:
        f.write(buf.getbuffer())


def add_CHECKMARK_STI(source_fs, target_fs):
    color = ImageColor.getrgb('#33CC3B')
    image = Image.new('RGBA', (31,27), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.line([(2,13), (11,25), (28,2)], color, 3)
    buf = BytesIO()
    image.save(buf, format='STCI', flags=['INDEXED', 'ETRLE'])
    with target_fs.open("CHECKMARK.STI", 'wb') as f:
        f.write(buf.getbuffer())


def add_EDITMODEBG_STI(source_fs, target_fs):
    color = ImageColor.getrgb('#5d6980')
    image = Image.new('RGB', (640,120), color)
    buf = BytesIO()
    image.save(buf, format='STCI', flags=['INDEXED', 'ETRLE'])
    with target_fs.open("EDITMODEBG.STI", 'wb') as f:
        f.write(buf.getbuffer())


def add_EXCLAMATION_STI(source_fs, target_fs):
    color = ImageColor.getrgb('#BFB467')
    image = Image.new('RGBA', (4,20), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.line([(1,1), (1,15)], color, 2)
    draw.line([(1,17), (1,18)], color, 2)
    buf = BytesIO()
    image.save(buf, format='STCI', flags=['INDEXED', 'ETRLE'])
    with target_fs.open("EXCLAMATION.STI", 'wb') as f:
        f.write(buf.getbuffer())


def add_INVPANEL_STI(source_fs, target_fs):
    color = ImageColor.getrgb('#5d6980')
    image = Image.new('RGB', (300,99), color)
    buf = BytesIO()
    image.save(buf, format='STCI', flags=['INDEXED', 'ETRLE'])
    with target_fs.open("INVPANEL.STI", 'wb') as f:
        f.write(buf.getbuffer())


def add_KEYIMAGE_STI(source_fs, target_fs):
    font = ImageFont.truetype(source_fs.getsyspath("silkscreen/slkscr.ttf"), 8)
    color = ImageColor.getrgb('#403C22')
    glow = ImageColor.getrgb('#E6D77C')
    image = make_glow_text_image(22, 12, "KEY", font, color, glow)
    image = image.rotate(90, expand=True)
    buf = BytesIO()
    image.save(buf, format='STCI', flags=['INDEXED', 'ETRLE'], semi_transparent='opaque')
    with target_fs.open("KEYIMAGE.STI", 'wb') as f:
        f.write(buf.getbuffer())


def add_LGDOWNARROW_LGUPARROW_STI(source_fs, target_fs):
    color = ImageColor.getrgb('#8c9dbf')
    border = ImageColor.getrgb('#a8bce6')
    image = Image.new('RGBA', (28,41), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.polygon([(0,0), (27,0), (14,40), (13,40)], outline=border, fill=color)
    buf = BytesIO()
    image.save(buf, format='STCI', flags=['INDEXED', 'ETRLE'])
    with target_fs.open("LGDOWNARROW.STI", 'wb') as f:
        f.write(buf.getbuffer())
    image = image.rotate(180)
    buf = BytesIO()
    image.save(buf, format='STCI', flags=['INDEXED', 'ETRLE'])
    with target_fs.open("LGUPARROW.STI", 'wb') as f:
        f.write(buf.getbuffer())


def add_OMERTA_STI(source_fs, target_fs):
    text = "OMERTA"
    font = ImageFont.truetype(source_fs.getsyspath("silkscreen/slkscr.ttf"), 32)
    color = ImageColor.getrgb('#403C22')
    backgound = ImageColor.getrgb('#E6D77C')
    image = Image.new('RGB', (212, 212), backgound)
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize(text, font=font, spacing=-1)
    x = (212 - text_width) // 2
    y = (212 - text_height) // 2
    draw.text((x,y), text, fill=color, font=font, spacing=-1, align='center')
    buf = BytesIO()
    image.save(buf, format='STCI', flags=['INDEXED', 'ETRLE'])
    with target_fs.open("OMERTA.STI", 'wb') as f:
        f.write(buf.getbuffer())


def add_to_free_editorslf(source_fs, target_fs):
    add_ARROWSOFF_ARROWSON_STI(source_fs, target_fs)
    add_BIGX_STI(source_fs, target_fs)
    add_CHECKMARK_STI(source_fs, target_fs)
    add_EDITMODEBG_STI(source_fs, target_fs) # not used
    add_EXCLAMATION_STI(source_fs, target_fs)
    add_INVPANEL_STI(source_fs, target_fs)
    add_KEYIMAGE_STI(source_fs, target_fs)
    add_LGDOWNARROW_LGUPARROW_STI(source_fs, target_fs)
    add_OMERTA_STI(source_fs, target_fs)

