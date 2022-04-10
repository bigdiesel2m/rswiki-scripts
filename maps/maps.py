from PIL import Image

im = Image.open('maps/map.png')

print(im.format, im.size, im.mode)

box = (2560, 2560, 2816, 2816)
im = im.crop(box)

print(im.format, im.size, im.mode)

im.save('maps/crop.png')