from perlin import PerlinNoiseFactory
import PIL.Image
from PIL import ImageFilter
from PIL import Image
import cv2
import sys
import itertools
import os
import time
import random

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)
   
def listToString(s):  
    str1 = "" 
    for ele in s: 
        str1 += ele  
    return str1

def convert(image_folder):
    video_name = 'video.avi'
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    
    video = cv2.VideoWriter(video_name, 0, 24, (width,height))
    bar2 = Bar('Conversion to video',images)
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
        bar2.next()
    bar2.finish()
    cv2.destroyAllWindows()
    video.release()

class Bar:
    prog = 0
    bar1=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    empty = ' '
    full = '#'
    def __init__(self,type_s,max_value):
        if isinstance(max_value,int):
            self.max_value = max_value
        else:
            self.max_value = len(max_value)
        self.type_s = type_s
        for i in range(10):
            self.bar1[i] = self.empty
        self.timer = time.perf_counter()
        self.val = self.prog/(self.max_value/100)
        sys.stdout.write(" %s progress: %d%% [%s] [%d|%d] %d s.  \r" % (self.type_s,self.val,listToString(self.bar1),self.prog,self.max_value,(time.perf_counter()-self.timer)))
        sys.stdout.flush()
        
    def next (self):
        self.prog+=1
        self.val = self.prog/(self.max_value/100)
        barprog = int (self.val / 10)
        for i in range(barprog):
            self.bar1[i]=self.full
        sys.stdout.write(" %s progress: %d%% [%s] [%d|%d] %d s.  \r" % (self.type_s,self.val,listToString(self.bar1),self.prog,self.max_value,(time.perf_counter()-self.timer)))
        sys.stdout.flush()
    def finish(self):
        sys.stdout.write("\n")
        self.prog = 0
        for i in range(10):
            self.bar1[i] = self.full
class spiner:
    pos = 0
    symb = ['|','-',' ']
    timer = 0
    def __init__(self):
        pass
    def next (self):
        self.pos = self.pos +1
        if self.pos % 2: 
            t = 0
        else:
            t = 1
        sys.stdout.write("%s\r" % (self.symb[t]))
        sys.stdout.flush()
        
class filter:
    def __init__(self):
        pass
    def detail (frames,framesize):
        bar = Bar('Detail filter',frames)
        for i in range(frames):
            img = PIL.Image.open("imgout/noise{:03d}.png".format(i))
            img.filter(ImageFilter.DETAIL)
            img.save("imgout/noise{:03d}.png".format(i))
            bar.next()
        bar.finish()
    def blur (frames,framesize):
        bar = Bar('Blur filter',frames)
        for i in range(frames):
            img = PIL.Image.open("imgout/noise{:03d}.png".format(i))
            img.filter(ImageFilter.BLUR)
            img.save("imgout/noise{:03d}.png".format(i))
            bar.next()
        bar.finish()
    def sharpen (frames,framesize):
        bar = Bar('Sharpen filter',frames)
        for i in range(frames):
            img = PIL.Image.open("imgout/noise{:03d}.png".format(i))
            img.filter(ImageFilter.SHARPEN)
            img.save("imgout/noise{:03d}.png".format(i))
            bar.next()
        bar.finish()

def noise(framesize,frames,res):
        bar = Bar('Image generation',frames)
        pnf1 = PerlinNoiseFactory(3, octaves=2, tile=(framesize*framesize, framesize*framesize, frames))
        pnf2 = PerlinNoiseFactory(3, octaves=3, tile=(framesize*framesize, framesize*framesize, frames))
        pnf3 = PerlinNoiseFactory(3, octaves=4, tile=(framesize*framesize, framesize*framesize, frames))
        for t in range(frames):
                s=spiner()
                img = PIL.Image.new('RGB',(framesize,framesize))
                for i in range(framesize):
                    n1 = pnf1(i/(framesize/res),i/(framesize/res),t/frames)
                    for j in range(framesize):
                        n2 = pnf2(i/(framesize/res),j/(framesize/res),t/frames)
                        n3 = pnf3(i/(framesize/res),j/(framesize/res),t/frames)
                        cval1 = int(clamp(((n1+0.5) * 255),0,255))
                        cval2 = int(clamp(((n2+0.5) * 255),0,255))
                        cval3 = int(clamp(((n3+0.5) * 255),0,255))
                        output = (int(clamp(cval1,0,255)),int(clamp(cval3,0,255)),int(clamp(cval2,0,255)))
                        img.putpixel((i,j),output)
                        s.next()
                img.save("imgout/noise{:03d}.png".format(t))
                bar.next()
        bar.finish()
def main ():
        framesize = int(input ("framesize :"))
        frames = int(input ("frames :"))
        res = int(input ("res :"))
        noise(framesize,frames,res)
        filter.blur(frames,framesize)
        convert("imgout")
main()