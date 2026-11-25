"""Hand-built vector logo for Jacksonville Mobile Mechanics (text converted to paths)."""
import os, math
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,'..','brand'); os.makedirs(OUT,exist_ok=True)
LIME='#C8F031'; INK='#0A0F1C'; WHITE='#F4F6EF'
_f={}
def font(w):
    if w not in _f:
        f=TTFont(os.path.join(HERE,'fonts','Unbounded.ttf'))
        _f[w]=instancer.instantiateVariableFont(f,{'wght':w})
    return _f[w]
def text_path(s,w,size,x,y,track=0):
    f=font(w); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm; sc=size/upm
    pen=SVGPathPen(gs); cx=x
    for ch in s:
        g=cmap.get(ord(ch)); 
        if g is None: continue
        tp=TransformPen(pen,(sc,0,0,-sc,cx,y)); gs[g].draw(tp)
        cx+=gs[g].width*sc+track
    return pen.getCommands(), cx-track-x
def emblem(cx,cy,r,ring,accent,cut_id,n=24):
    """24-tick dial with a wrench for a clock hand (points ~ 1:30 = 'any hour')."""
    ticks=[]
    for i in range(n):
        a=math.radians(i*360/n); long=i%(n//4)==0
        r1=r*0.80 if long else r*0.86; r2=r*0.95
        ticks.append(f'<line x1="{cx+r1*math.sin(a):.2f}" y1="{cy-r1*math.cos(a):.2f}" x2="{cx+r2*math.sin(a):.2f}" y2="{cy-r2*math.cos(a):.2f}" stroke="{ring}" stroke-width="{r*((0.09 if n<24 else 0.07) if long else (0.06 if n<24 else 0.035)):.2f}" stroke-linecap="round"/>')
    s=r/50
    # wrench drawn pointing up, then rotated 45deg
    wrench=(f'<g transform="translate({cx} {cy}) rotate(42) scale({s})">'
      f'<mask id="{cut_id}"><rect x="-60" y="-80" width="120" height="160" fill="#fff"/>'
      f'<rect x="-4.6" y="-52" width="9.2" height="15" rx="1.6" fill="#000"/></mask>'
      f'<g mask="url(#{cut_id})" fill="{accent}"><circle cx="0" cy="-35" r="12.5"/>'
      f'<rect x="-5.4" y="-30" width="10.8" height="44" rx="5.4"/></g>'
      f'<circle cx="0" cy="0" r="8" fill="{accent}"/><circle cx="0" cy="0" r="2.6" fill="{INK if accent!=INK else WHITE}" opacity=".9"/></g>')
    # the short bottom-of-wrench 'tail' handle opposite side for a clock look
    return (f'<circle cx="{cx}" cy="{cy}" r="{r*0.985:.2f}" fill="none" stroke="{ring}" stroke-width="{r*0.03:.2f}" opacity=".35"/>'
            + ''.join(ticks) + wrench)
def svg(w,h,body,bg=None):
    b=f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{b}{body}</svg>'
def horizontal(fg,ring,accent,sub,name,bg=None):
    E=emblem(46,46,44,ring,accent,'m'+name)
    p1,w1=text_path('JACKSONVILLE',500,15,108,36,track=4.2)
    p2,w2=text_path('MOBILE MECHANICS',800,24,106,70,track=0.6)
    W=int(max(108+w1,106+w2)+6)
    body=E+f'<path d="{p1}" fill="{sub}"/><path d="{p2}" fill="{fg}"/>'
    open(f'{OUT}/{name}.svg','w').write(svg(W,92,body,bg)); return W
def stacked(fg,ring,accent,sub,name,bg=None):
    p1,w1=text_path('JACKSONVILLE',500,15,0,0,track=4.2)
    p2,w2=text_path('MOBILE MECHANICS',800,24,0,0,track=0.6)
    W=int(max(w1,w2))+20
    E=emblem(W/2,52,48,ring,accent,'s'+name)
    p1,_=text_path('JACKSONVILLE',500,15,(W-w1)/2,136,track=4.2)
    p2,_=text_path('MOBILE MECHANICS',800,24,(W-w2)/2,170,track=0.6)
    open(f'{OUT}/{name}.svg','w').write(svg(W,184,E+f'<path d="{p1}" fill="{sub}"/><path d="{p2}" fill="{fg}"/>',bg))
def mark(name,ring,accent,bg=None,rounded=False):
    body=''
    if rounded: body+=f'<rect width="100" height="100" rx="22" fill="{INK}"/>'
    body+=emblem(50,50,44 if rounded else 48,ring,accent,'e'+name,n=12 if rounded else 24)
    open(f'{OUT}/{name}.svg','w').write(svg(100,100,body,bg))
horizontal(WHITE,WHITE,LIME,'#9AA3B5','logo-horizontal-dark')
horizontal(INK,INK,'#5E7A00','#4A5368','logo-horizontal-light')
horizontal('#000','#000','#000','#000','logo-horizontal-black')
horizontal('#fff','#fff','#fff','#fff','logo-horizontal-white')
stacked(WHITE,WHITE,LIME,'#9AA3B5','logo-stacked-dark')
stacked(INK,INK,'#5E7A00','#4A5368','logo-stacked-light')
mark('emblem-dark',WHITE,LIME)
mark('emblem-light',INK,'#5E7A00')
mark('emblem-black','#000','#000')
mark('favicon',WHITE,LIME,rounded=True)
print('ok')
