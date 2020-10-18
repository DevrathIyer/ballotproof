from PIL import Image
import json
from glob import glob
from collections import Counter
import random

ballot1 = Image.open("examples\\SampleBallot-1.png")
json1 = json.load(open("AZ-5-1.json", "r+"))
ballot2 = Image.open("examples\\SampleBallot-2.png")
json2 = json.load(open("AZ-5-2.json", "r+"))

redFiles = Counter(glob("primitives\\*R.png"))
accurateFiles = Counter(glob("primitives\\accurate*")) - Counter(redFiles)
badFiles = Counter(glob("primitives\\*")) - Counter(accurateFiles) - Counter(redFiles)

sections1 = json1["sections"]
sections2 = json2["sections"]
counter = 1

def setToString(set):
    output = ''
    for string in set:
        output = output + "," + string
    return output

def generate(file, color, extra, zero, bad_mark):
    global counter
    name1 = "test\\generatedballot-1-" + str(counter) + ".png"
    name2 = "test\\generatedballot-2-" + str(counter) + ".png"
    errorArray1 = set()
    errorArray2 = set()
    files = accurateFiles
    if color:
        errorArray1.add("bad color")
        errorArray2.add("bad color")
        files = files + redFiles
    if bad_mark:
        errorArray1.add("bad mark")
        errorArray2.add("bad mark")
        files = files + badFiles

    fileList = list(files)

    generatedballot1 = ballot1.copy().convert('RGBA')
    for section in sections1:
        bubbles = section["bubbles"]
        max = section["max"]

        if extra and zero:
            extraRand = random.random() > .5
            zeroRand = random.random() > .5
            if zeroRand:
                max = 0
                errorArray1.add("blank section")
            elif extraRand:
                max = max + 1
                errorArray1.add("extra bubble")
        elif extra:
            extraRand = random.random() > .5
            if extraRand:
                max = max + 1
                errorArray1.add("extra bubble")
        elif zero:
            zeroRand = random.random() > .5
            if zeroRand:
                max = 0
                errorArray1.add("blank section")
        if bubbles is not None:
            bubblesToUse = random.sample(bubbles, max)
            for bubble in bubblesToUse:
                shape = Image.open(fileList[random.randint(0, len(fileList) - 1)])
                shape_x, shape_y = shape.size
                center_x = bubble["TL_X"] + bubble["BR_X"]
                center_y = bubble["TL_Y"] + bubble["BR_Y"]
                generatedballot1.paste(shape, ((center_x - shape_x) // 2, (center_y - shape_y) // 2), mask=shape)

    generatedballot2 = ballot2.copy().convert('RGBA')
    for section in sections2:
        bubbles = section["bubbles"]
        max = section["max"]
        if extra and zero:
            extraRand = random.random() > .5
            zeroRand = random.random() > .5
            if zeroRand:
                max = 0
                errorArray2.add("blank section")
            elif extraRand:
                max = max + 1
                errorArray2.add("extra bubble")
        elif extra:
            extraRand = random.random() > .5
            if extraRand:
                max = max + 1
                errorArray2.add("extra bubble")
        elif zero:
            zeroRand = random.random() > .5
            if zeroRand:
                max = 0
                errorArray2.add("blank section")
        if bubbles is not None:
            bubblesToUse = random.sample(bubbles, max)
            for bubble in bubblesToUse:
                shape = Image.open(fileList[random.randint(0, len(fileList) - 1)])
                shape_x, shape_y = shape.size
                center_x = bubble["TL_X"] + bubble["BR_X"]
                center_y = bubble["TL_Y"] + bubble["BR_Y"]
                generatedballot2.paste(shape, ((center_x - shape_x) // 2, (center_y - shape_y) // 2), mask=shape)

    color1 = (random.randint(0,200),random.randint(0,200),random.randint(0,200))
    color2 = (random.randint(0,200),random.randint(0,200),random.randint(0,200),)
    generatedballot1 = generatedballot1.rotate(40*random.random()-20, Image.BICUBIC, expand=1, fillcolor=color1)
    generatedballot2 = generatedballot2.rotate(40*random.random()-20, Image.BICUBIC, expand=1, fillcolor=color2)

    bkgnd1 = Image.new("RGB", (3000, 4500), color1)
    bkgnd2 = Image.new("RGB", (3000, 4500), color2)

    bkgnd1.paste(generatedballot1, (100,100))
    bkgnd2.paste(generatedballot2, (100,100))
    bkgnd1.save(name1)
    bkgnd2.save(name2)
    file.write(name1+setToString(errorArray1)+"\n"+name2+setToString(errorArray2)+"\n")
    counter = counter + 1

f = open("test\\test.txt", "w")
f.close()
f = open("test\\test.txt", "a+")
while counter <= 80:
    color = random.random() > .5
    extra = random.random() > .5
    zero = random.random() > .5
    bad_mark = random.random() > .5
    generate(f, color, extra, zero, bad_mark)
f.close()