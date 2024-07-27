import json
from PIL import Image, ImageDraw

def drawshape(region):
    if 'xLowerLeft' in region:
        oldLowX = region['xLowerLeft']
        oldHighX = region['xLowerRight']
        oldLowY = region['yLowerLeft']
        oldHighY = region['yUpperLeft']
        newLowX = region['xUpperLeft']
        newHighX = region['xUpperRight']
        newLowY = region['yLowerRight']
        newHighY = region['yUpperRight']
        print oldLowX == newLowX, oldLowY == newLowY, oldHighX == newHighX, oldHighY == newHighY
        validIcons.extend(getIconsInsideArea(region['plane'] + plane, oldLowX, oldHighX, oldLowY, oldHighY, allPlanes=plane==0))
        for x in range(oldLowX, oldHighX + 1):
            for y in range(oldLowY, oldHighY + 1):
                filename = "versions/%s/tiles/base/%s_%s_%s.png" % (version, region['plane'] + plane, x, y)
                if os.path.exists(filename):
                    square = Image.open(filename)
                    imX = (x-lowX+newLowX-oldLowX) * px_per_square * 64
                    imY = (highY-y) * px_per_square * 64
                    im.paste(square, box=(imX+256, imY+256))
    elif 'chunk_oldXLow' in region:
        filename = "versions/%s/tiles/base/%s_%s_%s.png" % (version, region['oldPlane'] + plane, region['oldX'], region['oldY'])
        dx = region['newX'] * 64 + region['chunk_newXLow'] * 8 - region['oldX'] * 64 - region['chunk_oldXLow'] * 8
        dy = region['newY'] * 64 + region['chunk_newYLow'] * 8 - region['oldY'] * 64 - region['chunk_oldYLow'] * 8
        dz = 0 - region['oldPlane']
        validIcons.extend(getIconsInsideArea(region['oldPlane'] + plane, region['oldX'], region['oldX'], region['oldY'], region['oldY'], region['chunk_oldXLow'], region['chunk_oldXHigh'], region['chunk_oldYLow'], region['chunk_oldYHigh'], dx, dy, dz, allPlanes=plane==0))
        if os.path.exists(filename):
            square = Image.open(filename)
            cropped = square.crop((region['chunk_oldXLow'] * px_per_square * 8,
                (8-region['chunk_oldYHigh'] - 1) * px_per_square * 8,
                (region['chunk_oldXHigh'] + 1) * px_per_square * 8,
                (8-region['chunk_oldYLow']) * px_per_square * 8))
            imX = (region['newX']-lowX) * px_per_square * 64 + region['chunk_newXLow'] * px_per_square * 8
            imY = (highY-region['newY']) * px_per_square * 64 + (7-region['chunk_newYHigh']) * px_per_square * 8
            im.paste(cropped, box=(imX+256, imY+256))
    elif 'chunk_xLow' in region:
        validIcons.extend(getIconsInsideArea(region['plane'] + plane, region['xLow'], region['xHigh'], region['yLow'], region['yHigh'], region['chunk_xLow'], region['chunk_xHigh'], region['chunk_yLow'], region['chunk_yHigh'], allPlanes=plane==0))
        filename = "versions/%s/tiles/base/%s_%s_%s.png" % (version, region['plane'] + plane, region['xLow'], region['yLow'])
        if os.path.exists(filename):
            square = Image.open(filename)
            cropped = square.crop((region['chunk_xLow'] * px_per_square * 8,
                (8-region['chunk_yHigh'] - 1) * px_per_square * 8,
                (region['chunk_xHigh'] + 1) * px_per_square * 8,
                (8-region['chunk_yLow']) * px_per_square * 8))
            imX = (region['xLow']-lowX) * px_per_square * 64 + region['chunk_xLow'] * px_per_square * 8
            imY = (highY-region['yLow']) * px_per_square * 64 + (7-region['chunk_yHigh']) * px_per_square * 8
            im.paste(cropped, box=(imX+256, imY+256))
    elif 'xLow' in region:
        validIcons.extend(getIconsInsideArea(region['plane'] + plane, region['xLow'], region['xHigh'], region['yLow'], region['yHigh'], allPlanes=plane==0))
        for x in range(region['xLow'], region['xHigh'] + 1):
            for y in range(region['yLow'], region['yHigh'] + 1):
                filename = "versions/%s/tiles/base/%s_%s_%s.png" % (version, region['plane'] + plane, x, y)
                if os.path.exists(filename):
                    square = Image.open(filename)
                    imX = (x-lowX) * px_per_square * 64
                    imY = (highY-y) * px_per_square * 64
                    im.paste(square, box=(imX+256, imY+256))
    else:
        raise ValueError(region)


with open('maps/mapiddefs.txt') as infile: #grab the >data<
    defs = json.load(infile)

# defkeys = defs[1].keys()
# print(defkeys)

testid = defs[1]
print(testid['name'])
print(len(testid['regionList']))
print(testid['regionList'][0])


exit()
image = Image.new("RGB",[100,200])
draw = ImageDraw.Draw(image)
for i in range(len(testid['regionList'])):
    region = testid['regionList'][i]
    #print(region)
    draw.polygon(((region['xLowerLeft'], 200-region['yLowerLeft']), (region['xLowerRight'], 200-region['yLowerRight']), (region['xUpperRight'], 200-region['yUpperRight']), (region['xUpperLeft'], 200-region['yUpperLeft'])), fill="green")

image.show()

exit()
for i in range(len(defs)):
    print(defs[i]['name'] + ' - ' + str(defs[i]['field463']))