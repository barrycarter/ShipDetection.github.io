#!/usr/local/bin/bython -k

from glob import *
from math import *
from PIL import Image, ImageDraw
import json
import re
import os
import sys
from bclib import *

# do this check early on, no point in doing computations otherwise

if (not os.path.exists("TILES")):die("TILES must exist")

# to store pixels

pixels = dict()

colors = ["122,4,3", "201,41,3", "245,105,23", "251,185,56",
"201,239,52", "116,254,93", "26,229,182", "53,171,249", "70,98,216",
"48,18,59"]

debugcount = 0

for i in glob("../data/*.js"):
    
    data = open(i).read()
    
    # remove var ... =
    data = re.sub("var [a-zA-Z0-9_]+\s*\=\s*", "", data)
    
    jdata = json.loads(data)
    
    for j in jdata["features"]:
        
        lng, lat = j["geometry"]["coordinates"]
        
        age = float(j["properties"]["DaysOld"])
        
        color = colors[floor((age-1)/12)]
        
        for z in range(11):
            
            conv = lngLat2Tile(lng=lng, lat=lat, z=z)
            
            # the keys are the tile and then pixel, the value is the color
            
            key1 = "%d,%d,%d" % (z,conv['x'],conv['y'])
            key2 = "%d,%d" % (conv['px'],conv['py'])
            
            if (not (key1 in pixels)):
                pixels[key1] = dict()
            
            
            pixels[key1][key2] = color
            
        
    


for tile in pixels.keys():
    
    print("TILE", tile)
    
    # find the z, x, y for this tile and create TILES/z/x if needed
    z, x, y = tile.split(",")
    
    dir = "TILES/%s/%s" % (z,x)
    
    file = "%s/%s.png" % (dir,y)
    
    # print("FILE", file)
    
    if (not os.path.exists(dir)):
        os.makedirs(dir)
    
    
    img = Image.new("RGBA", (256, 256), color = (0, 0, 0, 0))
    
    for pixel in pixels[tile]:
        
        
        # TODO: there is doubtless a better way to do this but couldn't use map()
        
        x, y = pixel.split(",")
        x = int(x)
        y = int(y)
        
        r, g, b = pixels[tile][pixel].split(",")
        r = int(r)
        g = int(g)
        b = int(b)
        
        #  print("X",x,"Y",y,"R",r,"G",g,"B",b)
        
        img.putpixel((x,y), (r,g,b))
    
    
    img.save(file)
    
    #  print("TILE",tile,"PIXEL",pixel)



