# Look-dev treatment recipes (prototype of the grade described in the concept doc).
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
LIB='/home/user/ccvedio/video/assets/lib/'
rng=np.random.default_rng(7)

def srgb2lin(a): return np.where(a<=0.04045,a/12.92,((a+0.055)/1.055)**2.4)
def lin2srgb(a): a=np.clip(a,0,1); return np.where(a<=0.0031308,a*12.92,1.055*a**(1/2.4)-0.055)

def resize(im,scale):
    w,h=im.size; up=im.resize((round(w*scale),round(h*scale)),Image.LANCZOS)
    if scale>1.05: up=up.filter(ImageFilter.UnsharpMask(radius=0.8*scale,percent=45,threshold=2))
    return up

def curve(x,lift=0.035,gain=0.94,gamma=1.06,shoulder=0.82):
    # filmic: toe lift, gamma, soft shoulder roll-off above `shoulder`
    y=lift+(gain-lift)*np.clip(x,0,1)**gamma
    k=y>shoulder; y=np.where(k,shoulder+(1-np.exp(-(y-shoulder)/(1-shoulder)*1.4))*(gain-shoulder)/(1-np.exp(-1.4)),y)
    return y

def color_grade(a,sat=0.80,shadow_tint=(1.04,1.0,0.94),hi_tint=(1.02,1.0,0.95)):
    L=(a*[0.2126,0.7152,0.0722]).sum(-1,keepdims=True)
    a=L+(a-L)*sat
    a=curve(a)
    w=np.clip(1-L*2,0,1); a=a*(w*np.array(shadow_tint)+(1-w)*np.array(hi_tint))
    return np.clip(a,0,1)

TONE=np.array([[0.047,0.043,0.039],[0.55,0.52,0.47],[0.93,0.90,0.84]])  # warm B/W ramp: shadow / mid / high
def mono_tone(g):
    g=curve(g,lift=0.03,gain=0.95,gamma=1.08)
    lo=np.clip(g*2,0,1)[...,None]; hi=np.clip(g*2-1,0,1)[...,None]
    return np.where(g[...,None]<0.5, TONE[0]+(TONE[1]-TONE[0])*lo, TONE[1]+(TONE[2]-TONE[1])*hi)

def halation(a,thr=0.80,radius=10,strength=0.22,tint=(1.0,0.42,0.22)):
    L=a.mean(-1); m=np.clip((L-thr)/(1-thr),0,1)
    b=ndi.gaussian_filter(m,radius)
    return np.clip(a+b[...,None]*np.array(tint)*strength,0,1)

def grain(a,amt=0.040,size=1.35):
    h,w=a.shape[:2]
    n=rng.normal(0,1,(int(h/size)+2,int(w/size)+2)).astype(np.float32)
    n=np.asarray(Image.fromarray(n).resize((w,h),Image.BICUBIC))
    L=a.mean(-1)
    resp=(0.30+0.70*4*L*(1-L))[...,None]
    return np.clip(a+n[...,None]*amt*resp,0,1)

def vignette(a,amt=0.16):
    h,w=a.shape[:2]; y,x=np.mgrid[0:h,0:w]
    r=np.sqrt(((x-w/2)/(w/2))**2+((y-h/2)/(h/2))**2)/1.414
    return a*(1-amt*np.clip(r,0,1)[...,None]**2.2)

def plate(name,scale,crop=None,mono=False,hal=True,vig=0.12):
    im=Image.open(LIB+name)
    if crop: im=im.crop(crop)
    im=resize(im.convert('L' if mono else 'RGB'),scale)
    a=np.asarray(im).astype(np.float32)/255
    a=mono_tone(a) if mono else color_grade(a)
    if hal: a=halation(a)
    a=vignette(a,vig); a=grain(a)
    return Image.fromarray((a*255).astype(np.uint8))
