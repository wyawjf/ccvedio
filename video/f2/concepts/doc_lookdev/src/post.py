# Final film post for look-dev: print bloom on everything, luminance grain, vignette. (Prototype of the GLSL post pass.)
import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0,'.')
from treat import grain, vignette
for name in sys.argv[1:]:
    a=np.asarray(Image.open(name).convert('RGB')).astype(np.float32)/255
    paper = a.mean() > 0.5
    bloom=np.stack([ndi.gaussian_filter(a[...,c],0.6) for c in range(3)],-1)
    a=np.clip(a*0.8+bloom*0.2+0.0,0,1)                       # 0.6px print bloom (kills the razor-digital edge)
    a=vignette(a,0.05 if paper else 0.14)
    a=grain(a,0.022 if paper else 0.034,1.35)
    Image.fromarray((a*255).astype(np.uint8)).save(name.replace('.png','_post.png'))
    print('post',name)
