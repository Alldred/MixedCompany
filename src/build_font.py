"""Mixed Company: original vector letterforms, built from drawn centreline paths.
Requires Python 3, fonttools, shapely, brotli, Pillow. No source fonts are used.
"""
from pathlib import Path
import sys, math, re, json, html, base64, zipfile, shutil
sys.path.insert(0, str(Path(__file__).parent / 'deps'))
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union
from shapely.affinity import scale, skew, translate, rotate
from shapely.geometry.polygon import orient
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._k_e_r_n import KernTable_format_0
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)
(ROOT / 'work').mkdir(exist_ok=True)
G = {}

def path(d):
    t = re.findall(r'[MLQCZ]|-?\d+(?:\.\d+)?', d)
    i=0; pts=[]; cmd=None
    while i<len(t):
        if t[i].isalpha(): cmd=t[i]; i+=1
        n={'M':2,'L':2,'Q':4,'C':6,'Z':0}[cmd]
        a=list(map(float,t[i:i+n])); i+=n
        if cmd in ('M','L'): pts.append(tuple(a)); cmd='L'
        elif cmd=='Z': pts.append(pts[0]); cmd=None
        else:
            p=pts[-1]; steps=28 if cmd=='C' else 20
            for j in range(1,steps+1):
                u=j/steps; v=1-u
                if cmd=='Q': pts.append((v*v*p[0]+2*v*u*a[0]+u*u*a[2],v*v*p[1]+2*v*u*a[1]+u*u*a[3]))
                else: pts.append((v**3*p[0]+3*v*v*u*a[0]+3*v*u*u*a[2]+u**3*a[4],v**3*p[1]+3*v*v*u*a[1]+3*v*u*u*a[3]+u**3*a[5]))
    return pts

def oval(cx,cy,rx,ry):
    return [(cx+rx*math.cos(i*math.tau/88),cy+ry*math.sin(i*math.tau/88)) for i in range(89)]

def add(c,*items):
    G[c]=[path(x) if isinstance(x,str) else x for x in items]

# Capitals: geometric, humanist and inscriptional constructions.
add('A','M0 0 L245 700 L490 0','M86 245 L403 245')
add('B','M0 0 L0 700 L220 700 C530 700 520 370 230 370 L0 370','M230 370 C570 370 560 0 220 0 L0 0')
add('C','M465 600 C320 795 0 710 0 350 C0 -10 325 -95 470 105')
add('D','M0 0 L0 700 L145 700 C650 700 650 0 145 0 Z')
add('E','M440 700 L0 700 L0 0 L455 0','M0 355 L360 355')
add('F','M0 0 L0 700 L450 700','M0 365 L355 365')
add('G','M465 605 C300 810 0 700 0 350 C0 -20 345 -80 475 100 L475 330 L280 330')
add('H','M0 0 L0 700','M480 0 L480 700','M0 350 L480 350')
add('I','M0 700 L320 700','M160 0 L160 700','M0 0 L320 0')
add('J','M100 700 L430 700 L430 180 C430 -70 0 -60 0 170')
add('K','M0 0 L0 700','M480 700 L0 250','M200 440 L490 0')
add('L','M0 700 L0 0 L440 0')
add('M','M0 0 L0 700 L300 230 L600 700 L600 0')
add('N','M0 0 L0 700 L480 0 L480 700')
add('O',oval(255,350,255,350))
add('P','M0 0 L0 700 L230 700 C560 700 560 335 230 335 L0 335')
add('Q',oval(255,350,255,350),'M305 185 L565 -90')
add('R','M0 0 L0 700 L235 700 C560 700 560 350 235 350 L0 350','M220 350 L500 0')
add('S','M440 605 C330 785 25 730 10 530 C-5 325 455 385 455 170 C455 -60 100 -50 0 100')
add('T','M0 700 L540 700','M270 700 L270 0')
add('U','M0 700 L0 235 C0 -80 490 -80 490 235 L490 700')
add('V','M0 700 L245 0 L490 700')
add('W','M0 700 L145 0 L340 530 L535 0 L680 700')
add('X','M0 700 L485 0','M0 0 L485 700')
add('Y','M0 700 L245 335 L490 700','M245 335 L245 0')
add('Z','M0 700 L475 700 L0 0 L490 0')

# Lowercase. Separate drawings, with a true x-height and useful ascenders.
add('a',oval(205,250,205,250),'M410 500 L410 0')
add('b','M0 0 L0 730','M0 250 C0 590 450 590 450 250 C450 -90 0 -90 0 250')
add('c','M400 420 C285 570 0 535 0 250 C0 -35 285 -70 405 90')
add('d',oval(210,250,210,250),'M420 0 L420 730')
add('e','M0 255 L430 255 C430 590 0 585 0 250 C0 -35 290 -65 405 90')
add('f','M110 0 L110 555 C110 760 275 780 355 695','M0 480 L315 480')
add('g',oval(210,250,210,250),'M420 500 L420 -70 C420 -260 110 -265 20 -140')
add('h','M0 0 L0 730','M0 345 C105 590 420 555 420 315 L420 0')
add('i','M0 0 L0 500',[(0,680)])
add('j','M190 500 L190 -65 Q190 -225 0 -175',[(190,680)])
add('k','M0 0 L0 730','M410 500 L0 170','M165 300 L425 0')
add('l','M0 730 L95 730 L95 110 Q95 -15 225 10')
add('m','M0 0 L0 500','M0 340 C70 560 325 580 325 335 L325 0','M325 340 C400 570 655 570 655 335 L655 0')
add('n','M0 0 L0 500','M0 335 C100 580 420 555 420 315 L420 0')
add('o',oval(225,250,225,250))
add('p','M0 -195 L0 500','M0 250 C0 590 450 590 450 250 C450 -90 0 -90 0 250')
add('q',oval(210,250,210,250),'M420 500 L420 -185 L510 -115')
add('r','M0 0 L0 500','M0 325 C55 480 170 555 315 455')
add('s','M365 430 C265 550 10 530 10 375 C10 215 385 300 385 125 C385 -40 100 -45 0 70')
add('t','M135 670 L135 115 Q135 -65 340 35','M0 480 L330 480')
add('u','M0 500 L0 180 C0 -85 420 -85 420 185 L420 500','M420 185 L420 0')
add('v','M0 500 L210 0 L420 500')
add('w','M0 500 L135 0 L310 395 L485 0 L620 500')
add('x','M0 500 L425 0','M0 0 L425 500')
add('y','M0 500 L220 10','M445 500 L170 -140 Q125 -235 15 -170')
add('z','M0 500 L410 500 L0 0 L425 0')

# Numbers: zero is explicitly slashed; one has a flag and a foot.
add('0','M110 0 Q0 0 0 135 L0 565 Q0 700 110 700 L330 700 Q440 700 440 565 L440 135 Q440 0 330 0 Z','M100 150 L340 550')
add('1','M0 560 L195 700 L195 0','M35 0 L360 0')
add('2','M0 550 C20 780 445 780 445 545 C445 365 0 210 0 0 L460 0')
add('3','M0 600 C115 775 440 730 440 540 C440 425 335 360 165 360','M165 360 C535 390 535 -10 230 0 Q55 0 0 110')
add('4','M355 0 L355 700 L0 205 L485 205')
add('5','M440 700 L50 700 L20 355 C180 495 460 410 460 190 C460 -50 110 -55 0 100')
add('6','M430 620 C200 845 -25 620 0 225 C20 -105 450 -60 450 205 C450 460 70 450 0 225')
add('7','M0 700 L470 700 L140 0','M130 335 L350 335')
add('8',oval(220,530,200,170),oval(220,180,220,180))
add('9','M0 85 C220 -150 460 115 445 485 C430 785 0 770 0 510 C0 260 370 285 445 485')

add('!','M0 235 L0 700',[(0,30)])
add('"','M0 700 L-20 525','M180 700 L160 525')
add('#','M60 0 L175 700','M300 0 L415 700','M0 235 L460 235','M35 480 L495 480')
add('$',*G['S'],'M235 -95 L235 805')
add('%','M0 0 L520 700',oval(100,560,100,140),oval(420,140,100,140))
add('&','M540 0 C315 150 70 405 70 550 C70 755 370 755 370 565 C370 350 0 355 0 160 C0 -65 400 -85 505 295','M425 295 L600 295')
add("'",'M30 700 L0 520')
add('(','M200 775 C-50 575 -50 125 200 -75')
add(')','M0 775 C250 575 250 125 0 -75')
add('*','M200 700 L200 325','M15 565 L385 445','M85 350 L315 655')
add('+','M0 300 L460 300','M230 70 L230 530')
add(',','M65 65 Q105 -50 0 -125')
add('-','M0 280 L310 280')
add('.',[(0,30)])
add('/','M0 -80 L410 780')
add(':',[(0,435)],[(0,45)])
add(';',[(70,435)],'M70 65 Q110 -50 0 -125')
add('<','M390 565 L0 300 L390 35')
add('=','M0 180 L465 180','M0 410 L465 410')
add('>','M0 565 L390 300 L0 35')
add('?','M0 555 C0 760 425 790 425 545 C425 405 215 425 215 215',[(215,30)])
add('@',oval(295,305,135,180),'M430 480 L430 150 C720 50 690 780 290 745 C-140 745 -130 -100 475 5')
add('[','M195 765 L0 765 L0 -65 L195 -65')
add('\\','M0 780 L410 -80')
add(']','M0 765 L195 765 L195 -65 L0 -65')
add('^','M0 440 L205 700 L410 440')
add('_','M0 -135 L470 -135')
add('`','M0 730 L135 580')
add('{','M240 780 C-10 790 190 350 0 350 C190 350 -10 -90 240 -80')
add('|','M0 -110 L0 790')
add('}','M0 780 C250 790 50 350 240 350 C50 350 250 -90 0 -80')
add('~','M0 285 C155 490 275 110 450 325')

add('£','M465 610 C310 825 50 685 120 420 L140 160 Q140 55 0 0 L490 0','M0 330 L325 330')
add('€','M495 615 C330 800 40 700 40 350 C40 0 330 -100 495 85','M0 435 L370 435','M0 265 L330 265')
add('¥','M0 700 L245 335 L490 700','M245 335 L245 0','M60 270 L430 270','M60 135 L430 135')
add('¢',*G['c'],'M230 -80 L230 635')
add('×','M0 65 L435 535','M0 535 L435 65')
add('÷','M0 300 L450 300',[(225,535)],[(225,65)])
add('±','M0 385 L460 385','M230 180 L230 590','M0 0 L460 0')
add('−','M0 300 L460 300')
add('°',oval(120,610,120,120))
add('•',[(0,310)])
add('…',[(0,30)],[(200,30)],[(400,30)])
add('–','M0 280 L530 280')
add('—','M0 280 L790 280')
add('‘','M90 745 Q-25 685 20 575')
add('’','M60 745 Q105 635 0 575')
add('“','M90 745 Q-25 685 20 575','M270 745 Q155 685 200 575')
add('”','M60 745 Q105 635 0 575','M240 745 Q285 635 180 575')
add('≤',*G['<'],'M0 -80 L390 -80')
add('≥',*G['>'],'M0 -80 L390 -80')
add('≠',*G['='],'M120 0 L360 600')
add('←','M0 300 L610 300','M230 530 L0 300 L230 70')
add('→','M0 300 L610 300','M380 530 L610 300 L380 70')
add('↑','M300 0 L300 630','M65 390 L300 630 L535 390')
add('↓','M300 0 L300 630','M65 240 L300 0 L535 240')
add('©',oval(350,350,350,350),'M505 495 C295 720 100 170 355 130 Q455 125 515 205')
add('®',oval(350,350,350,350),'M230 120 L230 585 L365 585 C580 585 555 350 365 350 L230 350','M355 350 L510 120')
add('™','M0 720 L270 720','M135 720 L135 385','M345 385 L345 720 L495 470 L645 720 L645 385')
add('¡',[(0,485)],'M0 275 L0 -190')
add('¿','M0 -40 C0 -250 425 -260 425 -30 C425 110 215 90 215 280',[(215,465)])

# Each base glyph gets its own prescribed treatment; no random font swapping.
# mode, stroke width, horizontal proportion, shear, terminal shape, label.
CAPS=[
('outline',115,.91,0,'flat','Architectural outline'),
('solid',104,1.02,0,'round','Soft balloon'),
('contrast',54,1.03,0,'flat','Classical contrast'),
('inline',112,.91,0,'round','Engraved oval'),
('stencil',101,.88,0,'flat','Industrial stencil'),
('solid',35,1.00,0,'flat','Architect hairline'),
('solid',72,.96,.13,'round','Forward grotesk'),
('slab',73,1.04,0,'flat','Egyptian slab'),
('outline',96,1.08,0,'flat','Open engraving'),
('solid',96,.93,-.07,'round','Soft brush'),
('stencil',83,.95,.025,'flat','Split diagonal'),
('wedge',62,1.03,0,'flat','Inscriptional wedge'),
('solid',58,1.08,0,'flat','Extended geometric'),
('outline',109,.90,.045,'flat','Folded ribbon'),
('contrast',60,.99,0,'round','High contrast oval'),
('slab',57,.80,0,'flat','Condensed book slab'),
('solid',41,1.03,.03,'round','Orbital monoline'),
('slab',99,.94,0,'flat','Chunky poster slab'),
('stencil',96,.91,-.025,'round','Curved stencil'),
('wedge',73,1.07,0,'flat','Flared inscription'),
('solid',75,.98,0,'round','Rounded humanist'),
('outline',117,.90,0,'round','Tubular chevron'),
('slab',53,.95,0,'flat','Typewriter wide'),
('contrast',70,.97,.07,'flat','Calligraphic crossing'),
('ball',49,.98,0,'round','Ball terminals'),
('inline',106,1.03,0,'flat','Deco inline')]
LOWER=[
('slab',57,.97,0,'flat','Schoolbook slab'),
('outline',104,.90,0,'round','Hollow round'),
('ball',44,1.07,.04,'round','Beaded crescent'),
('contrast',59,.91,.04,'flat','Book italic'),
('solid',92,1.03,0,'round','Friendly rounded'),
('wedge',49,.91,-.03,'flat','Flared hook'),
('solid',64,.95,.10,'round','Single-storey italic'),
('stencil',89,.93,0,'flat','Cut-stem sans'),
('slab',61,1.0,0,'flat','Slab with square dot'),
('solid',77,1.05,-.08,'round','Swing descender'),
('outline',99,.96,0,'flat','Wire-frame angular'),
('solid',43,.92,.02,'round','Loopless handwritten'),
('contrast',56,1.01,0,'round','Broad-pen arches'),
('slab',72,.96,0,'flat','Rounded slab'),
('stencil',84,1.08,0,'round','Broken circular'),
('inline',105,.93,.045,'round','Inline descender'),
('solid',99,.91,0,'flat','Heavy geometric'),
('wedge',64,.99,0,'flat','Wedge shoulder'),
('solid',40,1.08,.13,'round','Light script'),
('ball',52,.90,-.035,'round','Ball-ended crossbar'),
('outline',104,.98,.055,'round','Open tubular'),
('slab',55,.94,0,'flat','Serif chevron'),
('solid',87,.97,0,'round','Soft zigzag'),
('stencil',90,1.04,0,'flat','Stencil crossing'),
('contrast',55,.94,.075,'round','Pen-stroke tail'),
('inline',96,1.00,0,'flat','Linear deco')]
NUMS=[
('solid',67,.91,0,'flat','Slashed technical'),('slab',64,.92,0,'flat','Flagged slab'),
('outline',110,1.02,.025,'round','Outline numeral'),('solid',101,.98,0,'round','Round heavy'),
('solid',40,.97,0,'flat','Light open four'),('stencil',93,.96,0,'flat','Utility stencil'),
('contrast',59,1.04,-.025,'round','Old-style contrast'),('wedge',68,.93,.06,'flat','Crossed inscription'),
('inline',104,1.00,0,'round','Inline figure eight'),('ball',50,.97,.015,'round','Terminal flourish')]
SPECS={}
for chars,specs in [('ABCDEFGHIJKLMNOPQRSTUVWXYZ',CAPS),('abcdefghijklmnopqrstuvwxyz',LOWER),('0123456789',NUMS)]:
    SPECS.update(zip(chars,specs))
symbol_modes=['solid','slab','contrast','solid','outline','solid','wedge','solid','ball','solid','inline','solid']
for i,c in enumerate(x for x in G if x not in SPECS):
    mode=symbol_modes[i%len(symbol_modes)]
    w=48+(i*13)%34
    if mode in ('outline','inline'): w=96+(i%4)*4
    SPECS[c]=(mode,w,.92+(i%7)*.023,((i%5)-2)*.014,'round' if i%2==0 else 'flat',f'Symbol treatment {i+1:02}')
# Punctuation is small and needs a sturdy mark rather than an intricate outline.
for c in '.,:;\'"‘’“”`':
    old=SPECS[c]; SPECS[c]=('solid',72+(ord(c)%5)*7,old[2],old[3],old[4],old[5])
SPECS['•']=('solid',155,1,0,'round','Solid bullet')
SPECS['…']=('solid',77,1,0,'round','Three round points')
SPECS['!']=('contrast',85,1,0,'flat','Tapered exclamation')
SPECS['|']=('solid',42,1,0,'flat','Hairline pipe')
SPECS['–']=('solid',67,1,0,'flat','Square en dash')
SPECS['—']=('solid',51,1,0,'round','Rounded em dash')

def stroke(points,w,cap='round',contrast=False):
    if len(points)==1:
        x,y=points[0]
        return Point(x,y).buffer(w*.66,quad_segs=16) if cap=='round' else box(x-w*.6,y-w*.6,x+w*.6,y+w*.6)
    ln=LineString(points)
    if contrast:
        return scale(scale(ln,xfact=.57,origin=(0,0)).buffer(w/2,cap_style=1 if cap=='round' else 2,join_style=1,quad_segs=8),xfact=1/.57,origin=(0,0))
    return ln.buffer(w/2,cap_style=1 if cap=='round' else 2,join_style=1 if cap=='round' else 2,mitre_limit=2.2,quad_segs=10)

def make_geometry(c):
    mode,w,xf,slant,cap,label=SPECS[c]
    components=[]
    for p in G[c]:
        components.append(stroke(p,w,cap,mode=='contrast'))
        if mode in ('slab','wedge','ball') and len(p)>1 and p[0]!=p[-1]:
            for idx,near in [(0,1),(-1,-2)]:
                x,y=p[idx]; nx,ny=p[near]
                if mode=='ball':
                    components.append(Point(x,y).buffer(w*.80,quad_segs=12))
                elif abs(ny-y)>abs(nx-x)*1.3:
                    length=w*1.28
                    if mode=='slab': components.append(box(x-length,y-w*.20,x+length,y+w*.20))
                    else:
                        sg=1 if ny>y else -1
                        components.append(Polygon([(x-length,y-sg*w*.12),(x+length,y-sg*w*.12),(x+w*.45,y+sg*w*.75),(x-w*.45,y+sg*w*.75)]))
    geom=unary_union(components).buffer(0)
    if mode=='outline':
        geom=geom.difference(geom.buffer(-19,join_style=2)).buffer(0)
    elif mode=='inline':
        # Keep the inline entirely inside the thick stroke, including terminals.
        channels=unary_union([stroke(p,16,'round') for p in G[c] if len(p)>1])
        geom=geom.difference(channels.intersection(geom.buffer(-25))).buffer(0)
    elif mode=='stencil':
        ymin,ymax=geom.bounds[1],geom.bounds[3]
        yy=ymin+(ymax-ymin)*(.40 if c.islower() else .54)
        cut=box(-180,yy-13,1100,yy+13)
        geom=geom.difference(rotate(cut,7+(ord(c)%3)*4,origin=(230,yy))).buffer(0)
    # Coherent body heights, while retaining descenders and punctuation positions.
    yshift=w/2
    if c.isalpha() and c.isascii():
        target=710 if c.isupper() or c in 'bdfhkl' else 520
        if c in 'ij':
            sy=520/(500+w); geom=scale(translate(geom,yoff=yshift),yfact=sy,xfact=1,origin=(0,0))
        else:
            sy=target/(geom.bounds[3]+yshift)
            geom=scale(translate(geom,yoff=yshift),yfact=sy,xfact=1,origin=(0,0))
    elif c.isdigit():
        ymin,ymax=geom.bounds[1],geom.bounds[3]
        geom=scale(translate(geom,yoff=-ymin),yfact=710/(ymax-ymin),xfact=1,origin=(0,0))
    else:
        geom=translate(geom,yoff=18)
    geom=scale(geom,xfact=xf,yfact=1,origin=(0,0))
    geom=skew(geom,xs=math.degrees(math.atan(slant)),origin=(0,0))
    geom=geom.simplify(.48,preserve_topology=True).buffer(0)
    left=44 if c.isalnum() else 42
    geom=translate(geom,xoff=left-geom.bounds[0])
    return geom,int(math.ceil(geom.bounds[2]+left))

def as_glyph(geom):
    pen=TTGlyphPen(None)
    polygons=[geom] if geom.geom_type=='Polygon' else list(geom.geoms)
    for poly in polygons:
        if poly.geom_type!='Polygon' or poly.area<1: continue
        poly=orient(poly,sign=-1)
        for ring in [poly.exterior,*poly.interiors]:
            pts=[]
            for x,y in ring.coords[:-1]:
                q=(round(x),round(y))
                if not pts or q!=pts[-1]: pts.append(q)
            if len(pts)<3:continue
            pen.moveTo(pts[0])
            for q in pts[1:]:pen.lineTo(q)
            pen.closePath()
    return pen.glyph()

shapes={}; metrics={}; glyphs={}; cmap={}; labels={}
missing=box(45,0,495,710).difference(box(85,40,455,670))
glyphs['.notdef']=as_glyph(missing); metrics['.notdef']=(540,45)
glyphs['space']=TTGlyphPen(None).glyph(); metrics['space']=(315,0); cmap[32]='space';cmap[160]='space'
for c in G:
    geom,advance=make_geometry(c)
    name='uni%04X'%ord(c)
    shapes[c]=geom; glyphs[name]=as_glyph(geom);metrics[name]=(advance,round(geom.bounds[0]));cmap[ord(c)]=name
    labels[c]=SPECS[c][-1]

# Latin accents inherit the base character's treatment so names remain coherent.
import unicodedata
accent_paths={
    '\u0301':[path('M-65 0 L75 120')], '\u0300':[path('M-75 120 L65 0')],
    '\u0302':[path('M-130 0 L0 125 L130 0')],
    '\u0303':[path('M-140 30 C-60 150 65 -80 145 50')],
    '\u0308':[[(-100,65)],[(100,65)]],
    '\u030a':[oval(0,65,72,65)],
    '\u0327':[path('M10 0 L-35 -70 C140 -55 100 -205 -45 -160')],
}
for cp in list(range(0xC0,0x100))+[0x178]:
    c=chr(cp); dec=unicodedata.normalize('NFD',c)
    if len(dec)!=2 or dec[0] not in shapes or dec[1] not in accent_paths:continue
    base,mark=dec; geom=shapes[base]
    if base=='i':
        # The accent replaces the dot on i, as in normal Latin typography.
        geom=geom.intersection(box(-100,-300,1000,540))
    x1,y1,x2,y2=geom.bounds
    accent=unary_union([stroke(p,45,'round') for p in accent_paths[mark]])
    advance=metrics[cmap[ord(base)]][0]
    accent_width=accent.bounds[2]-accent.bounds[0]
    if accent_width>advance-64:
        accent=scale(accent,xfact=(advance-64)/accent_width,yfact=1,origin=(0,0))
    yy=-8 if mark=='\u0327' else y2+85
    accent=translate(accent,xoff=(x1+x2)/2,yoff=yy)
    combined=unary_union([geom,accent]);name='uni%04X'%cp
    glyphs[name]=as_glyph(combined); metrics[name]=(advance,round(combined.bounds[0]));cmap[cp]=name
    shapes[c]=combined;labels[c]=labels[base]+' with accent'

fb=FontBuilder(1000,isTTF=True)
fb.setupGlyphOrder(list(glyphs))
fb.setupCharacterMap(cmap)
fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics(metrics)
fb.setupHorizontalHeader(ascent=1000,descent=-300,lineGap=0)
fb.setupNameTable({'familyName':'Mixed Company','styleName':'Regular','uniqueFontIdentifier':'Mixed Company 1.000 Original 2026','fullName':'Mixed Company Regular','psName':'MixedCompany-Regular','version':'Version 1.000','copyright':'Original vector design created for Stuart Alldred, 2026.','description':'A readable display alphabet with individually styled characters. Original letterforms; no source fonts used.'})
fb.setupOS2(sTypoAscender=1000,sTypoDescender=-300,sTypoLineGap=0,usWinAscent=1000,usWinDescent=300,sxHeight=520,sCapHeight=710,usWeightClass=400,usWidthClass=5,fsType=0,fsSelection=0x40)
fb.setupPost()
fb.setupMaxp()
fb.font['head'].fontRevision=1.0
fb.font['head'].created=fb.font['head'].modified=3871929600

# Conservative spacing corrections for diagonal and overhanging letter pairs.
kerning={}
for pair,value in {'AV':-45,'AW':-35,'AY':-50,'AT':-32,'VA':-45,'WA':-30,'YA':-45,'TA':-32,'To':-40,'Ta':-35,'Te':-30,'Ty':-25,'Yo':-40,'Ya':-36,'Ye':-35,'Vo':-32,'Va':-32,'Ve':-26,'Wo':-22,'Wa':-22,'LT':-22,'LY':-32,'LV':-25,'FA':-25,'PA':-32,'Po':-12,'ry':-13}.items():
    kerning[(cmap[ord(pair[0])],cmap[ord(pair[1])])]=value
kern=newTable('kern'); kern.version=0
sub=KernTable_format_0();sub.version=0;sub.coverage=1;sub.kernTable=kerning;kern.kernTables=[sub];fb.font['kern']=kern
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
feature='feature kern {\n'+''.join(f'pos {a} {b} {v};\n' for (a,b),v in kerning.items())+'} kern;'
addOpenTypeFeaturesFromString(fb.font,feature)
fontpath=OUT/'MixedCompany-Regular.ttf';fb.save(fontpath)
web=TTFont(fontpath);web.flavor='woff2';web.save(OUT/'MixedCompany-Regular.woff2')

# A specimen is rasterized with the actual finished TTF, not substitute lettering.
INK='#24241f'; PAPER='#f4f0e6'; RED='#d6492f'; MUTED='#77766d'; LINE='#c8c6ba'
im=Image.new('RGB',(1800,2120),PAPER);draw=ImageDraw.Draw(im)
ui='/System/Library/Fonts/Supplemental/Arial.ttf'
uib='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def font(s,display=False,bold=False):return ImageFont.truetype(str(fontpath) if display else (uib if bold else ui),s)
def txt(x,y,t,s=30,fill=INK,display=False,bold=False):draw.text((x,y),t,font=font(s,display,bold),fill=fill,anchor='lt')
def rule(y):draw.line((90,y,1710,y),fill=LINE,width=2)
def fitline(text,x,y,max_width,size,fill=INK):
    while draw.textlength(text,font=font(size,True))>max_width:size-=1
    txt(x,y,text,size,fill,True)
txt(90,65,'MIXED COMPANY',27,bold=True)
txt(1305,65,'TYPE SPECIMEN   /   01',23)
rule(118)
fitline('Mixed Company',90,178,1630,168)
txt(95,385,'Different personalities. One readable alphabet.',32)
rule(470)
txt(90,516,'01   THE CAPITALS',23,RED,bold=True)
fitline('ABCDEFGHIJKLM',90,575,1620,157)
fitline('NOPQRSTUVWXYZ',90,745,1620,157)
rule(930)
txt(90,973,'02   THE LOWERCASE',23,RED,bold=True)
fitline('abcdefghijklm',90,1033,1620,158)
fitline('nopqrstuvwxyz',90,1202,1620,158)
rule(1390)
txt(90,1430,'03   NUMBERS & SYMBOLS',23,RED,bold=True)
fitline('0123456789  &@!?',90,1490,1620,133)
fitline('£ € $ % + − × ÷ = # *',90,1650,1620,99)
rule(1798)
fitline('Pack my box with five',90,1845,1620,92)
fitline('dozen liquor jugs.',90,1960,1620,92)
im.save(OUT/'MixedCompany-Preview.png')

# Complete labelled glyph proof for inspecting coverage and rendering.
chars=[chr(cp) for cp in sorted(cmap) if cp not in (32,160)]
cols=12;rows=math.ceil(len(chars)/cols); cw=140;ch=153
proof=Image.new('RGB',(cols*cw+100,rows*ch+190),PAPER);pd=ImageDraw.Draw(proof)
pd.text((50,35),'Mixed Company / complete character set',font=font(32,bold=True),fill=INK)
for i,c in enumerate(chars):
    x=50+(i%cols)*cw;y=120+(i//cols)*ch
    pd.rectangle((x,y,x+cw,y+ch),outline=LINE,width=1)
    ff=font(81,True);bounds=pd.textbbox((0,0),c,font=ff)
    xx=x+(cw-(bounds[2]-bounds[0]))/2-bounds[0]
    pd.text((xx,y+91),c,font=ff,anchor='ls',fill=INK)
    pd.text((x+10,y+122),f'U+{ord(c):04X}  {c}',font=font(16),fill=MUTED)
proof.save(OUT/'MixedCompany-All-Glyphs.png')

encoded=base64.b64encode((OUT/'MixedCompany-Regular.woff2').read_bytes()).decode()
cells=''.join(f'<div class="cell"><span>{html.escape(c)}</span><small>{html.escape(c)} · {ord(c):04X}</small></div>' for c in chars)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mixed Company — font tester</title>
<style>@font-face{font-family:MixedCompany;src:url(data:font/woff2;base64,FONTDATA) format('woff2');font-display:swap}*{box-sizing:border-box}body{margin:0;background:#f4f0e6;color:#24241f;font:16px system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:40px 32px}header{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #c8c6ba;padding-bottom:22px;gap:20px}header strong{letter-spacing:.08em}a{color:inherit}h1{font:clamp(48px,8vw,104px)/1.3 MixedCompany;margin:50px 0 18px}p{line-height:1.6;max-width:780px}label{display:inline-flex;gap:12px;align-items:center;font-size:14px}label input{accent-color:#d6492f}nav{display:flex;flex-wrap:wrap;gap:28px;align-items:center;padding:24px 0;border-top:1px solid #c8c6ba;margin-top:35px}textarea{font:84px/1.45 MixedCompany;width:100%;height:360px;border:1px solid #c8c6ba;background:transparent;color:inherit;padding:24px;resize:vertical;outline-color:#d6492f;font-synthesis:none}.tip{font-size:13px;color:#69695f}.unsupported{color:#a23120;min-height:25px}h2{font-size:14px;letter-spacing:.1em;margin:52px 0 24px;text-transform:uppercase;color:#b23b27}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr)));border-top:1px solid #c8c6ba;border-left:1px solid #c8c6ba}.cell{display:flex;min-height:128px;align-items:center;justify-content:center;flex-direction:column;border-right:1px solid #c8c6ba;border-bottom:1px solid #c8c6ba}.cell span{font:64px/1.4 MixedCompany}.cell small{font:11px system-ui;color:#77766d;margin:5px 0 12px}footer{margin-top:45px;border-top:1px solid #c8c6ba;padding-top:20px;font-size:13px;color:#69695f}@media(max-width:600px){main{padding:24px 18px}header{font-size:12px}textarea{font-size:52px;padding:12px}}</style>
<main><header><strong>MIXED COMPANY</strong><span>ORIGINAL DISPLAY FONT · VERSION 1.0</span></header><h1>Mixed Company</h1><p>A typographic gathering of rounded, serif, outlined, stencil and hand-drawn characters. Each base character has its own treatment, with shared heights and considered spacing. Best enjoyed at display sizes.</p><nav><label>Size <input id="size" type="range" min="24" max="160" value="84"><output id="sizeout">84 px</output></label><label>Spacing <input id="tracking" type="range" min="-1" max="12" value="0"><output id="trackout">0 px</output></label><label>Ink <input id="color" type="color" value="#24241f"></label></nav><textarea aria-label="Type to try Mixed Company" id="tester" spellcheck="false">Every letter has a story.
Meet the whole alphabet!</textarea><p class="tip">Type your own text. Repeated letters keep their assigned design. This tester works offline; the font is embedded.</p><p id="unsupported" class="unsupported" aria-live="polite"></p><h2>Complete character set · COUNT encoded characters</h2><section class="grid">CELLS</section><footer>Install MixedCompany-Regular.ttf to use the font in your apps. Accented letters inherit their base letter’s treatment. This first version covers basic Latin, common Latin accents, punctuation, currencies and selected symbols.</footer></main><script>
const size=document.querySelector('#size'), tracking=document.querySelector('#tracking'),color=document.querySelector('#color'),tester=document.querySelector('#tester');
size.oninput=()=>{tester.style.fontSize=size.value+'px';document.querySelector('#sizeout').value=size.value+' px'};
tracking.oninput=()=>{tester.style.letterSpacing=tracking.value+'px';document.querySelector('#trackout').value=tracking.value+' px'};
color.oninput=()=>tester.style.color=color.value;
const supported=new Set(CODEPOINTS); tester.oninput=()=>{const missing=[...new Set([...tester.value].filter(c=>!supported.has(c.codePointAt(0))&&!/\\s/.test(c)))];document.querySelector('#unsupported').textContent=missing.length?'Outside this font’s character set (shown using a fallback): '+missing.join(' '):''};tester.oninput();
</script></html>'''.replace('FONTDATA',encoded).replace('CELLS',cells).replace('COUNT',str(len(cmap))).replace('CODEPOINTS',json.dumps(sorted(cmap)))
page=page.replace('minmax(100px,1fr)))','minmax(100px,1fr))')
(OUT/'MixedCompany-Try-It.html').write_text(page)

report={'family':'Mixed Company','version':'1.000','encoded_characters':len(cmap),'glyphs':len(glyphs),'base_drawings':len(G),'kerning_pairs':len(kerning),'character_set':''.join(chr(c) for c in sorted(cmap)),'styles':labels}
(ROOT/'work'/'font-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps({k:v for k,v in report.items() if k not in ('styles','character_set')},indent=2))
print('Saved TTF, WOFF2, specimen, full glyph proof and offline tester.')
