from PIL import Image, ImageDraw, ImageFont
def add_num(img):
    draw = ImageDraw.Draw(img)
    myfont = ImageFont.truetype('C:/windows/fonts/Arial.ttf', size=40)
    fillcolor = "#ff0000"
    width, height = img.size
    draw.text((width-50, 5), '99', font=myfont, fill=fillcolor)
    img.save('result.jpg','jpeg')
    return 0


def add_other(im,mark):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    layer.paste(mark, (im.size[0] - 150, im.size[1] - 150))
    out = Image.composite(layer, im, layer)
    out.save('result.jpg','jpeg')
    out.show()
    return 0


if __name__ == '__main__':
    # image = Image.open('C:/Users/amelie/Pictures/Saved Pictures/s3113179.jpg')
    # add_num(image)
    image = Image.open('C:/Users/amelie/Pictures/Saved Pictures/s3113179.jpg')
    mark = Image.open('C:/Users/amelie/Pictures/Camera Roll/1.png')
    add_other(image,mark)
    image.show()