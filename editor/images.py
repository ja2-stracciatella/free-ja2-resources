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
    """map of Arulco (16x16 grid, 2 pixel border)"""
    text = "OMERTA"
    water_color = ImageColor.getrgb('#4A5FFF')
    shore_color = ImageColor.getrgb('#CCAD76')
    land_color = ImageColor.getrgb('#428021')
    pen_color = ImageColor.getrgb('#080808')
    town_color = ImageColor.getrgb('#BF7737')
    font = ImageFont.truetype(source_fs.getsyspath("silkscreen/slkscr.ttf"), 8)
    image = Image.new('RGB', (212, 212), water_color)
    draw = ImageDraw.Draw(image)
    def pixel(coord):
        return 2 + int(round(208 * coord / 16))
    def pixels(x, y, off):
        arr = []
        arr.append(pixel(x))
        arr.append(pixel(y))
        for i in range(len(off)):
            if i % 2 == 0:
                x += off[i]
                arr.append(pixel(x))
            else:
                y += off[i]
                arr.append(pixel(y))
        return arr
    shoreline = pixels(1.5,-.5, [
        -1,1, 0,2, 1,1, 0,2, -1,1,
        0,1, 1,0, 1,1, -1,1, 0,1,
        -1,1, 2,2, 0,2, 2,-2, 2,0,
        1,1, 1,0, 1,-1, 0,-1, 1,-1,
        1,0, 1,1, 0,1, 1,1, 0,1,
        1,1, 2,0, 0,-17])
    draw.polygon(shoreline, land_color, shore_color)
    def paste_texts(arr):
        for i in range(0, len(arr), 3):
            x0 = pixel(arr[i])
            y0 = pixel(arr[i + 1])
            x1 = pixel(arr[i] + 1) + 1
            y1 = pixel(arr[i + 1] + 1) - 1
            text = arr[i + 2]
            text_image = make_glow_text_image(x1-x0, y1-y0, text, font, pen_color, shore_color)
            image.paste(text_image, (x0,y0,x1,y1), text_image)
    # town grid cells
    draw.polygon(pixels(1, 0, [1,0, 0,2, -1,0]), town_color, None) # chitzena
    draw.polygon(pixels(8, 0, [2,0, 0,1, -2,0]), town_color, None) # omerta
    draw.polygon(pixels(12, 1, [1,0, 0,3, -1,0]), town_color, None) # drassen
    draw.polygon(pixels(4, 2, [2,0, 0,1, -1,0, 0,1, -2,0, 0,-1, 1,0]), town_color, None) # san mona
    draw.polygon(pixels(7, 5, [2,0, 0,2, -1,0, 0,1, -1,0]), town_color, None) # cambria
    draw.polygon(pixels(0, 6, [2,0, 0,1, 1,0, 0,1, -3,0]), town_color, None) # grumm
    draw.polygon(pixels(12, 7, [2,0, 0,2, -2,0]), town_color, None) # alma
    draw.polygon(pixels(10, 11, [2,0, 0,1, -2,0]), town_color, None) # balime
    draw.polygon(pixels(2, 13, [3,0, 0,1, -1,0, 0,1, -1,0, 0,1, -1,0]), town_color, None) # meduna
    # roads
    draw.line(pixels(1.5, 2, [0,0.5, 1,0, 0,7, -1,0, 0,3, 1,0, 0,0.5]), pen_color, 3)
    draw.line(pixels(4.5, 13, [0,-0.5, 1,0, 0,-6, 1,0, 0,-3, -1,0, 0,-1, 3,0, 0,-2]), pen_color, 3)
    draw.line(pixels(2, 7.5, [0.5,0, 0,-1, 6,0, 0,-5, 4,0, 0,3, -1,0, 0,3, 2,0, 0,3, -8,0]), pen_color, 3)
    draw.line(pixels(5, 13.5, [4.5,0, 0,-3, 1,0, 0,1, 0.5,0]), pen_color, 3)
    draw.line(pixels(8.5, 6.5, [3,0, 0,1, 1,0, 0,1, 1,0]), pen_color, 3)
    # labels
    T = "" # town
    M = "M" # town with mine
    A = "A" # town with airport
    P = "P" #  town with palace
    paste_texts([1,0,T, 1,1,M]) # chitzena
    paste_texts([8,0,T, 9,0,T]) # omerta
    paste_texts([12,1,A, 12,2,T, 12,3,M]) # drassen
    paste_texts([4,2,T, 5,2,T, 3,3,M, 4,3,T]) # san mona
    paste_texts([7,5,T, 8,5,T, 7,6,T, 8,6,T, 7,7,M]) # cambria
    paste_texts([0,6,T, 1,6,T, 0,7,T, 1,7,T, 2,7,M]) # grumm
    paste_texts([12,7,T, 13,7,T, 12,8,T, 13,8,M]) # alma
    paste_texts([10,11,T, 11,11,T]) # balime
    paste_texts([2,13,A, 3,13,T, 4,13,T, 2,14,T, 3,14,T, 2,15,P]) # meduna
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


