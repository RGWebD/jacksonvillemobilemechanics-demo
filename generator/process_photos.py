"""Curate + export photos to WebP. Plates blurred, watermark cropped."""
from PIL import Image, ImageFilter, ImageOps
import imagehash, os, itertools
SRC='/workspace/site-research/photos/'
OUT=os.path.join(os.path.dirname(__file__),'..','img')
os.makedirs(OUT,exist_ok=True)
KEEP=['g01','g02','g03','g05','g06','g07','g08','g09','g10','g11','g12','g14','g15','g16','g17','g18','g20','g23','g24']
BLUR={'g02':[(925,1285,1170,1432)],'g16':[(870,844,944,884)]}
CROP={'g23':(0,0,900,1690)}
hs={}
for k in KEEP:
    im=ImageOps.exif_transpose(Image.open(SRC+k+'.jpg')).convert('RGB')
    for b in BLUR.get(k,[]):
        reg=im.crop(b).filter(ImageFilter.GaussianBlur(18)); reg=reg.filter(ImageFilter.GaussianBlur(18)); im.paste(reg,b[:2])
    if k in CROP: im=im.crop(CROP[k])
    hs[k]=imagehash.phash(im)
    big=im.copy(); big.thumbnail((1600,1600)); big.save(f'{OUT}/{k}.webp','WEBP',quality=80,method=6)
    sm=im.copy(); sm.thumbnail((760,760)); sm.save(f'{OUT}/{k}-s.webp','WEBP',quality=76,method=6)
for a,b in itertools.combinations(hs,2):
    d=hs[a]-hs[b]
    if d<14: print('close',a,b,d)
# OG image
og=Image.open(SRC+'g11.jpg').convert('RGB'); w,h=og.size
og=og.crop((0,int(h*.2),w,int(h*.2)+int(w*630/1200))).resize((1200,630))
og.save(f'{OUT}/og-base.jpg',quality=85)
print('done')
