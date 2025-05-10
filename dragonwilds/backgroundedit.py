from PIL import Image
import math

## Open and load in image
bg = Image.open("dragonwilds/ConceptCrop.png")
pixels = list(bg.getdata())

## Going through each pixel to get its transparency, note that I started with a 1920x500 image, manually cropped from a larger 1920-width image
i = 0
newpixels = []
width = bg.width
height = bg.height
for px in pixels:
	## Get x/y coordinates for a given pixel
	xval = i % width
	yval = math.floor(i/width)

	## Partial transparency, multiplied in a non-scientific way that I think looked alright.
	xratio = 3
	lrtrans = xratio-xval/(width/xratio)

	yratio = 2
	udtrans = yratio-yval/(height/yratio)
	multtrans = math.floor(255*min(1,(udtrans*lrtrans)))

	## Save transparency info and original color to new pixel list
	newpx = (px[0], px[1], px[2], multtrans)
	newpixels.append(newpx)
	i = i + 1

## Create a new image using the new pixels with transparency
newbg = Image.new("RGBA", bg.size)
newbg.putdata(newpixels)
newbg.save("dragonwilds/Background.png")