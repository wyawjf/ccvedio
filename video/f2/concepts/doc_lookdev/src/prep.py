# Prepare graded photo plates at exact display pixel sizes (grain is added later, full-frame).
import sys, numpy as np
sys.path.insert(0,'.')
from treat import *
from PIL import Image, ImageDraw, ImageFilter
from skimage import segmentation, filters, measure, morphology
from scipy import ndimage as ndi
OUT='plates/'; import os; os.makedirs(OUT,exist_ok=True)

def save(a,name): Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).save(OUT+name)
def load(name,mode): return Image.open(LIB+name).convert(mode)
def up(im,size):
    w,h=im.size; s=size[0]/w
    r=im.resize(size,Image.LANCZOS)
    if s>1.05: r=r.filter(ImageFilter.UnsharpMask(radius=0.8*s,percent=45,threshold=2))
    return r
def deblock_sky(im, ymax):
    a=np.asarray(im).astype(np.float32)/255
    L=a.mean(-1); g=np.hypot(*np.gradient(ndi.gaussian_filter(L,1.0)))
    m=(g<0.012).astype(np.float32); m[ymax:]=0; m=ndi.gaussian_filter(m,2)
    b=np.stack([ndi.gaussian_filter(a[...,c],1.4) for c in range(3)],-1)
    return Image.fromarray(((a*(1-m[...,None])+b*m[...,None])*255).astype(np.uint8))

def color_plate(im,size,sat=0.80,hal=True,thr=0.80):
    a=np.asarray(up(im,size)).astype(np.float32)/255
    a=color_grade(a,sat=sat)
    if hal: a=halation(a,thr=thr,radius=10*size[0]/900,strength=0.22)
    return a
def mono_plate(im,size):
    a=np.asarray(up(im,size)).astype(np.float32)/255
    return mono_tone(a)

# S02 espresso 1.30x -> 780x520
save(color_plate(load('coffee.png','RGB'),(780,520),sat=0.84),'coffee_780.png')
# S03 rocket slit crop x223-423, 2.0x -> 400x854 (deblock sky first)
rk=deblock_sky(load('rocket.jpg','RGB'),330).crop((223,0,423,427))
save(color_plate(rk,(400,854),sat=0.74,thr=0.78),'rocket_slit_400.png')
# S04 coins plate 2.0x -> 768x606 (B/W warm tone)
save(mono_plate(load('coins.png','L'),(768,606)),'coins_768.png')
# Cover coins plate 2.0x same
# S01 coin #18 at 3.62x, circular alpha, 229x229
c=load('coins.png','L'); cx,cy,r=347.0,186.7,31.6
box=(cx-34,cy-34,cx+34,cy+34); crop=c.crop(tuple(int(round(v)) for v in box))
S=3.62; size=int(round(68*S)); cimg=mono_plate(crop,(size,size))
yy,xx=np.mgrid[0:size,0:size]; rr=np.hypot(xx-size/2+0.5,yy-size/2+0.5); alpha=np.clip((r*S+0.5-rr),0,1)
save(np.dstack([cimg,alpha]),'coin18_rgba.png')
# Sheet thumbnails (downscaled, sharp): fit into 284x180 box
sheet=[('coins.png','L'),('coffee.png','RGB'),('rocket.jpg','RGB'),('hubble_deep_field.jpg','RGB'),('retina.jpg','RGB'),
       ('camera.png','L'),('astronaut.png','RGB'),('grace_hopper.jpg','RGB'),('moon.png','L'),('text.png','L'),('clock_motion.png','L')]
for i,(n,mode) in enumerate(sheet,1):
    im=load(n,mode); w,h=im.size; s=min(284/w,180/h); size=(round(w*s),round(h*s))
    im=im.resize(size,Image.LANCZOS)
    a=np.asarray(im).astype(np.float32)/255
    a=mono_tone(a) if mode=='L' else color_grade(a,sat=0.82)
    save(a,f'sheet_{i:02d}.png'); print(i,n,size)
# S05 Hubble 1.08x -> 1080x942 ; S06 retina 800px disc ; S07 camera 1.5x 768
save(color_plate(load('hubble_deep_field.jpg','RGB'),(1080,942),sat=0.86,thr=0.62),'hubble_1080.png')
rt=load('retina.jpg','RGB').resize((800,800),Image.LANCZOS)
a=np.asarray(rt).astype(np.float32)/255; a=color_grade(a,sat=0.86); a=halation(a,thr=0.70,radius=12,strength=0.28); save(a,'retina_800.png')
save(mono_plate(load('camera.png','L'),(768,768)),'camera_768.png')
print('done')
