"""MixedCompany Mono 3.0: individually styled glyphs and accented bodies.
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

def stroke(points,w,cap='round',contrast=False):
    if len(points)==1:
        x,y=points[0]
        return Point(x,y).buffer(w*.66,quad_segs=16) if cap=='round' else box(x-w*.6,y-w*.6,x+w*.6,y+w*.6)
    ln=LineString(points)
    if contrast:
        return scale(scale(ln,xfact=.57,origin=(0,0)).buffer(w/2,cap_style=1 if cap=='round' else 2,join_style=1,quad_segs=8),xfact=1/.57,origin=(0,0))
    return ln.buffer(w/2,cap_style=1 if cap=='round' else 2,join_style=1 if cap=='round' else 2,mitre_limit=2.2,quad_segs=10)

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

# Second edition: deliberately different constructions, not width-only variants.
add('C',*G['C'],'M455 530 L470 680','M455 25 L475 175')
add('D','M0 0 L0 700 L305 700 L480 540 L480 160 L305 0 Z')
add('F','M0 0 L0 700 L450 700','M0 365 L355 365','M0 646 L450 646','M0 311 L355 311')
add('H','M0 0 L0 700','M480 0 L480 700','M0 350 L480 350',
    'M-85 700 L85 700','M395 700 L565 700','M-85 0 L85 0','M395 0 L565 0')
add('P','M0 0 L0 700','M0 700 L220 700 C550 700 550 335 220 335 L0 335')
add('R','M0 0 L0 700 L305 700 L450 575 L450 465 L305 350 L0 350','M220 350 L495 0')
add('V','M0 700 L245 0','M245 0 L490 700')
add('Z','M0 700 L475 700','M475 700 L0 0','M0 0 L490 0','M0 633 L335 633','M155 67 L490 67')
add('a','M5 435 C120 570 420 535 420 350 L420 0',
    'M420 265 C270 400 0 315 0 155 C0 -65 420 -30 420 210')
add('d','M115 0 Q0 0 0 115 L0 385 Q0 500 115 500 L310 500 Q420 500 420 385 L420 115 Q420 0 310 0 Z',
    'M420 730 L420 0 L495 20')
add('e','M0 215 L420 305 C385 630 -40 550 0 220 C30 -45 285 -55 405 95')
add('f','M15 -155 C105 -205 160 -20 175 195 L215 560 C235 805 470 750 430 625',
    'M0 470 L355 470')
add('g',oval(225,365,195,135),oval(205,-40,210,150),'M100 250 L95 105','M385 460 L485 500')
add('h','M0 0 L0 730','M0 350 L0 440 Q0 510 85 510 L340 510 Q420 510 420 430 L420 0')
add('i',*[[ (0,y) ] for y in (45,150,255,360,465)],[(0,680)])
add('j','M210 500 L210 -65 C210 -230 20 -215 0 -120',[(210,680)])
add('l','M350 30 C185 -30 125 65 175 160 L315 590 C395 800 135 865 115 630 C95 290 55 115 165 35 Q240 -25 350 30')
add('m','M0 0 L0 500','M0 350 L0 425 Q0 500 75 500 L200 500 Q285 500 285 425 L285 0',
    'M285 350 L285 425 Q285 500 360 500 L485 500 Q570 500 570 425 L570 0')
add('n','M-80 0 Q0 15 0 120 L0 500','M0 335 C100 580 420 555 420 315 L420 0')
add('o','M130 0 L320 0 L450 130 L450 370 L320 500 L130 500 L0 370 L0 130 Z')
add('q','M100 0 Q0 0 0 100 L0 400 Q0 500 100 500 L330 500 Q420 500 420 400 L420 100 Q420 0 330 0 Z',
    'M420 500 L420 -185 L515 -115')
add('r','M0 0 L0 500','M0 310 C65 550 260 525 305 475 C365 410 265 360 240 430')
add('s','M390 430 C265 550 10 530 10 375 C10 215 385 300 385 125 C385 -40 105 -45 -35 60')
add('w','M0 500 L0 180 C0 -80 275 -80 275 180 L275 480',
    'M275 180 C275 -80 550 -80 550 180 L550 500')
add('y','M0 500 L220 10','M445 500 L180 -125 C50 -285 -90 -155 10 -80 Q90 -35 185 -110')
add('z','M0 500 L410 500','M410 500 L0 0','M0 0 L425 0')
add('1','M0 520 L205 700 L205 0','M50 0 L375 0')
add('3','M0 700 L320 700 L450 575 L450 465 L320 350 L135 350',
    'M320 350 L450 235 L450 125 L320 0 L0 0')
add('6','M430 650 C260 815 0 610 0 240 C0 -65 445 -60 445 210 C445 430 90 450 75 215')
add('7','M0 635 Q250 745 485 700','M485 700 L150 0')
add('8','M220 700 L425 530 L220 350 L15 530 Z','M220 350 L450 170 L220 0 L-10 170 Z')
add('9',oval(225,505,225,195),'M450 510 C465 145 250 -120 30 70')

# mode, weight, slant, character's visual concept. One entry per base character.
DESIGNS={}
cap=[
('outline',116,0,'A · architectural outline'),
('round',120,0,'B · soft balloon'),
('contrast',47,0,'C · beaked Roman'),
('segments',99,0,'D · segmented octagon'),
('hatch',115,0,'E · woodcut stripes'),
('plain',27,0,'F · double-rule blueprint'),
('round',67,.20,'G · forward-leaning grotesk'),
('custom_h',62,0,'H · reverse-contrast slab'),
('tuscan_i',80,0,'I · bifurcated Tuscan'),
('brush',103,-.11,'J · tapered brush'),
('cut',88,0,'K · angular stencil'),
('shadow',81,0,'L · dimensional shadow'),
('pixel',73,0,'M · stepped pixel'),
('fold',114,0,'N · folded ribbon'),
('contrast',61,0,'O · high-contrast oval'),
('pinstripe',110,0,'P · pinstripe stem'),
('comet',50,0,'Q · comet tail'),
('slab',108,0,'R · octagonal wood type'),
('dots',56,0,'S · dotted marquee'),
('western_t',98,0,'T · western forks'),
('reverse',60,0,'U · reverse-contrast bowl'),
('chisel',95,0,'V · chisel contrast'),
('slab',40,0,'W · fine typewriter'),
('weave',98,0,'X · woven strokes'),
('ball',47,0,'Y · spindle terminals'),
('custom_z',75,0,'Z · racing rules')]
lower=[
('contrast_serif',50,0,'a · double-storey book'),
('rivet',108,0,'b · perforated bold'),
('diamond_ends',33,0,'c · diamond terminals'),
('contrast',50,.14,'d · squared italic'),
('round',76,-.025,'e · tilted humanist'),
('contrast',37,.10,'f · long calligraphic swash'),
('plain',52,0,'g · double-storey geometric'),
('arch_cut',80,0,'h · cut square arch'),
('dot_i',55,0,'i · dotted column / diamond dot'),
('triangle_j',35,-.055,'j · hairline hook / triangular dot'),
('hybrid_k',98,0,'k · tubular stem / solid branches'),
('round',34,.04,'l · looped script'),
('plain',39,0,'m · modular bridge'),
('round',91,.15,'n · cursive entry'),
('plain',93,0,'o · faceted octagon'),
('inline',112,0,'p · engraved descender'),
('custom_q',46,.04,'q · light bowl / heavy tail'),
('slab',59,0,'r · curled serif shoulder'),
('round',31,.14,'s · fine sweeping script'),
('split_t',77,0,'t · split crossbar'),
('outline',103,0,'u · double-wire bend'),
('notched_v',91,0,'v · notched wedge'),
('reverse',43,0,'w · connected double cup'),
('studded_x',57,0,'x · studded crossing'),
('contrast',61,.035,'y · looped descender'),
('reverse_z',110,0,'z · reverse-contrast zigzag')]
digits=[
('plain',66,0,'0 · technical slashed zero'),
('flag_one',75,0,'1 · pennant and wedge'),
('outline',102,.035,'2 · neon outline'),
('cut',94,0,'3 · squared stencil'),
('plain',32,0,'4 · open hairline'),
('slab',104,0,'5 · heavy woodblock'),
('round',43,0,'6 · open spiral'),
('brush_seven',88,0,'7 · swashed brush'),
('plain',68,0,'8 · stacked diamonds'),
('hybrid_nine',104,0,'9 · open bowl / solid tail')]
for chars,styles in [('ABCDEFGHIJKLMNOPQRSTUVWXYZ',cap),('abcdefghijklmnopqrstuvwxyz',lower),('0123456789',digits)]:
    DESIGNS.update(zip(chars,styles))

# Symbols get individual stroke, cap and construction decisions as well.
symbol_specs={
'!':('taper_bang',94,0,'tapered stem / square stop'),
'"':('plain',78,0,'parallel square quotes'), '#':('round',86,.04,'soft heavy hash'),
'$':('contrast',39,0,'fine currency contrast'), '%':('outline',108,0,'hollow percent'),
'&':('brush',86,-.035,'brushed ampersand'), "'":('diamond_ends',51,0,'diamond apostrophe'),
'(':('plain',33,0,'fine parenthesis'), ')':('reverse',44,0,'contrast parenthesis'),
'*':('ball',36,0,'beaded asterisk'), '+':('inline',104,0,'inlaid plus'),
',':('round',86,.09,'teardrop comma'), '-':('round',58,0,'capsule hyphen'),
'.':('diamond_dot',91,0,'diamond full stop'), '/':('taper',63,0,'tapered slash'),
':':('square_dots',59,0,'square colon'), ';':('mixed_semi',66,0,'ring and hook semicolon'),
'<':('plain',72,0,'square left angle'), '=':('reverse',40,0,'broad equals'),
'>':('round',45,0,'round right angle'), '?':('contrast',62,.05,'contrasted question'),
'@':('plain',39,0,'fine spiral at sign'), '[':('outline',96,0,'open left bracket'),
'\\':('plain',93,0,'solid backslash'), ']':('slab',47,0,'serif right bracket'),
'^':('chisel',67,0,'contrasted caret'), '_':('inline',94,0,'inlaid underscore'),
'`':('plain',56,-.1,'cut acute-backtick'), '{':('round',37,0,'hairline left brace'),
'|':('outline',83,0,'hollow vertical pipe'), '}':('contrast',67,0,'broad right brace'),
'~':('taper',73,0,'tapered wave'), '£':('ball',42,0,'terminal pound'),
'€':('plain',92,0,'heavy euro'), '¥':('outline',99,0,'outlined yen'),
'¢':('reverse',42,.04,'reverse-contrast cent'), '×':('weave',69,0,'woven multiplication'),
'÷':('round',51,0,'rounded division'), '±':('plain',78,0,'solid plus-minus'),
'−':('plain',36,0,'hairline minus'), '°':('contrast',47,0,'contrasted degree'),
'•':('round',146,0,'solid bullet'), '…':('square_dots',64,0,'square ellipsis'),
'–':('plain',65,0,'square en dash'), '—':('round',43,0,'round em dash'),
'‘':('plain',56,-.06,'angular opening quote'), '’':('round',82,.04,'soft closing quote'),
'“':('contrast',45,0,'fine opening double quote'), '”':('plain',83,0,'heavy closing double quote'),
'≤':('round',62,0,'soft less-or-equal'), '≥':('plain',39,0,'light greater-or-equal'),
'≠':('contrast',45,.025,'contrasted unequal'), '←':('outline',95,0,'hollow left arrow'),
'→':('plain',60,0,'square right arrow'), '↑':('ball',38,0,'ball-ended upward arrow'),
'↓':('taper',76,0,'tapered downward arrow'), '©':('plain',36,0,'light copyright'),
'®':('reverse',37,0,'contrasted registration'), '™':('outline',93,0,'outlined trademark'),
'¡':('plain',66,0,'square inverted exclamation'), '¿':('round',80,0,'rounded inverted question')}
for c,spec in symbol_specs.items():DESIGNS[c]=(*spec[:3],c+' · '+spec[3])
assert set(DESIGNS)==set(G),set(G)-set(DESIGNS)

def resample(points,step=14):
    if len(points)==1:return points
    line=LineString(points);n=max(1,math.ceil(line.length/step))
    return [(line.interpolate(i/n,normalized=True).x,line.interpolate(i/n,normalized=True).y) for i in range(n+1)]

def variable_stroke(p,w):
    if len(p)==1:return stroke(p,w,'round')
    pts=resample(p,12);pieces=[]
    for i,pt in enumerate(pts):
        t=i/max(1,len(pts)-1)
        radius=w*(.27+.29*math.sin(math.pi*(.14+.79*t)))
        pieces.append(Point(pt).buffer(radius,quad_segs=8))
    return unary_union(pieces)

def diamonds(points,r):
    return unary_union([Polygon([(x-r,y),(x,y+r),(x+r,y),(x,y-r)]) for x,y in points])

def raw_geometry(c):
    mode,w,slant,label=DESIGNS[c]; paths=G[c]
    cap='round' if mode in ('round','outline','inline','brush','ball','rivet','taper','reverse') else 'flat'
    def basic(weight=w):return unary_union([stroke(p,weight,cap,mode in ('contrast','contrast_serif')) for p in paths])
    geom=basic()
    if mode in ('brush','taper'):geom=unary_union([variable_stroke(p,w) for p in paths])
    elif mode=='reverse':
        geom=unary_union([scale(stroke([(x,y*.52) for x,y in p],w,cap),xfact=1,yfact=1/.52,origin=(0,0)) for p in paths])
    if mode in ('slab','contrast_serif','ball','diamond_ends'):
        extra=[]
        for p in paths:
            if len(p)<2 or p[0]==p[-1]:continue
            for idx,near in [(0,1),(-1,-2)]:
                x,y=p[idx];nx,ny=p[near]
                if mode=='ball':extra.append(Point(x,y).buffer(w*.94,quad_segs=12))
                elif mode=='diamond_ends':extra.append(diamonds([(x,y)],w*1.13))
                elif abs(ny-y)>abs(nx-x)*1.3:extra.append(box(x-w*1.48,y-w*.22,x+w*1.48,y+w*.22))
        geom=unary_union([geom,*extra])
    if mode in ('outline','fold'):geom=geom.difference(geom.buffer(-18,join_style=2))
    if mode=='fold':geom=unary_union([geom,basic().intersection(box(-200,302,1000,362))])
    if mode=='inline':
        channel=unary_union([stroke(p,18,'round') for p in paths if len(p)>1])
        geom=geom.difference(channel.intersection(geom.buffer(-24)))
    if mode in ('cut','segments','arch_cut'):
        if mode=='segments':cuts=[box(-200,y-13,1100,y+13) for y in [200,515]]
        elif mode=='arch_cut':cuts=[box(-200,290,90,319),box(345,472,370,590)]
        else:cuts=[rotate(box(-200,310,1100,339),13,origin=(230,325))]
        geom=geom.difference(unary_union(cuts))
    if mode=='hatch':
        cuts=[rotate(box(-200,y,1100,y+12),17,origin=(250,350)) for y in range(-120,950,67)]
        geom=geom.difference(unary_union(cuts).intersection(geom.buffer(-17)))
    if mode=='dots':
        geom=unary_union([Point(pt).buffer(25,quad_segs=12) for p in paths for pt in resample(p,64)])
    if mode=='pixel':
        squares=[];cell=28
        x1,y1,x2,y2=geom.bounds
        for x in range(math.floor(x1/cell),math.ceil(x2/cell)):
            for y in range(math.floor(y1/cell),math.ceil(y2/cell)):
                if geom.covers(Point((x+.5)*cell,(y+.5)*cell)):squares.append(box(x*cell,y*cell,(x+1)*cell,(y+1)*cell))
        geom=unary_union(squares)
    if mode=='shadow':
        shadow=translate(geom,xoff=43,yoff=-37)
        shadow=shadow.difference(shadow.buffer(-14)).difference(geom.buffer(12))
        geom=unary_union([geom,shadow])
    if mode=='custom_h':
        geom=unary_union([stroke(p,ww,'flat') for p,ww in zip(paths,[40,40,116,36,36,36,36])])
    if mode=='tuscan_i':
        geom=Polygon([(0,700),(430,700),(430,612),(270,612),(270,88),(430,88),(430,0),(0,0),(0,88),(160,88),(160,612),(0,612)])
        cuts=[Polygon([(x,y),(x+78,y),(x+39,y+sg*41)]) for x in [0,352] for y,sg in [(700,-1),(0,1)]]
        geom=geom.difference(unary_union(cuts))
    if mode=='pinstripe':
        stem=stroke(paths[0],116,'flat');bowl=stroke(paths[1],46,'round')
        stem=stem.difference(unary_union([box(x-6,40,x+6,660) for x in [-20,20]]))
        geom=unary_union([stem,bowl,box(-105,-15,105,15)])
    if mode=='comet':
        tail=stroke(paths[1],88,'flat');tail=tail.difference(stroke(paths[1],21,'flat').intersection(tail.buffer(-22)))
        geom=unary_union([stroke(paths[0],40,'round'),tail])
    if mode=='western_t':
        geom=unary_union([stroke(p,98,'flat') for p in paths]+[Polygon([(155,0),(385,0),(315,98),(225,98)])])
        geom=geom.difference(unary_union([Polygon([(x,650),(x,750),(x+sg*60,700)]) for x,sg in [(0,1),(540,-1)]]))
    if mode=='chisel':
        if len(paths)>1:geom=unary_union([stroke(paths[0],118,'flat'),stroke(paths[1],35,'flat')])
        else:
            p=paths[0];geom=unary_union([stroke(p[:2],87,'flat'),stroke(p[1:],29,'flat')])
    if mode=='weave':
        over=stroke(paths[0],w,'flat');under=stroke(paths[1],w*.47,'round')
        geom=unary_union([over,under.difference(over.buffer(15))])
    if mode=='custom_z':geom=unary_union([stroke(p,ww,'flat') for p,ww in zip(paths,[30,85,30,22,22])])
    if mode=='rivet':
        holes=[Point(pt).buffer(14,quad_segs=10) for p in paths for pt in resample(p,105)]
        geom=geom.difference(unary_union(holes).intersection(geom.buffer(-23)))
    if mode=='dot_i':
        geom=unary_union([Point(p[0]).buffer(34,quad_segs=14) for p in paths[:-1]]+[diamonds(paths[-1],58)])
    if mode=='triangle_j':
        x,y=paths[-1][0];geom=unary_union([stroke(paths[0],35,'round'),Polygon([(x-52,y-38),(x+52,y-38),(x,y+55)])])
    if mode=='hybrid_k':
        stem=stroke(paths[0],99,'round');stem=stem.difference(stem.buffer(-18))
        geom=unary_union([stem,stroke(paths[1],46,'flat'),stroke(paths[2],81,'flat')])
    if mode=='custom_q':geom=unary_union([stroke(paths[0],40,'flat'),stroke(paths[1],101,'flat')])
    if mode=='split_t':
        geom=geom.difference(box(225,420,252,540));geom=unary_union([geom,box(85,640,185,675)])
    if mode=='notched_v':
        geom=unary_union([geom,box(-55,480,80,511),box(340,480,475,511)])
        geom=geom.difference(diamonds([(210,12)],23))
    if mode=='studded_x':
        pts=resample(paths[1],82);geom=unary_union([stroke(paths[0],42,'round'),diamonds(pts,35)])
    if mode=='reverse_z':geom=unary_union([stroke(p,ww,'flat') for p,ww in zip(paths,[112,31,112])])
    if mode=='flag_one':
        geom=unary_union([stroke(paths[0],66,'flat'),Polygon([(30,0),(380,0),(205,90)]),Polygon([(0,520),(205,700),(205,570)])])
    if mode=='brush_seven':geom=unary_union([stroke(paths[0],37,'round'),variable_stroke(paths[1],104)])
    if mode=='hybrid_nine':
        ring=stroke(paths[0],101,'round');ring=ring.difference(ring.buffer(-18))
        geom=unary_union([ring,stroke(paths[1],79,'round')])
    if mode=='taper_bang':
        geom=unary_union([Polygon([(-65,700),(65,700),(25,235),(-25,235)]),box(-40,-10,40,70)])
    if mode=='diamond_dot':geom=diamonds(paths[0],57)
    if mode=='square_dots':geom=unary_union([box(p[0][0]-39,p[0][1]-39,p[0][0]+39,p[0][1]+39) for p in paths])
    if mode=='mixed_semi':
        x,y=paths[0][0];ring=Point(x,y).buffer(47,quad_segs=16).difference(Point(x,y).buffer(23,quad_segs=16))
        geom=unary_union([ring,stroke(paths[1],73,'round')])
    return geom.buffer(0)

CELL=640
def make_geometry(c):
    geom=raw_geometry(c);mode,w,slant,label=DESIGNS[c]
    # Baselines and body heights remain steady while silhouettes vary.
    if c.isascii() and c.isalnum():
        desc=c in 'Qfgjpqy'
        low=-w/2 if desc else geom.bounds[1]
        target=710 if c.isupper() or c.isdigit() or c in 'bdfhkl' else 520
        top=geom.bounds[3]
        if c in 'ij':top=500+w/2
        geom=scale(translate(geom,yoff=-low),xfact=1,yfact=target/(top-low),origin=(0,0))
    else:geom=translate(geom,yoff=18)
    geom=skew(geom,xs=math.degrees(math.atan(slant)),origin=(0,0))
    geom=geom.simplify(.42,preserve_topology=True).buffer(0)
    width=geom.bounds[2]-geom.bounds[0]
    maxwidth=532
    if width>maxwidth:geom=scale(geom,xfact=maxwidth/width,yfact=1,origin=(0,0))
    # Deliberate padding, not indiscriminate stretching of narrow letters.
    width=geom.bounds[2]-geom.bounds[0]
    geom=translate(geom,xoff=(CELL-width)/2-geom.bounds[0])
    return geom,CELL

# WILD EDITION: theme-specific construction, including independent accented bodies.
import copy, random, unicodedata
from shapely import make_valid
old_raw_geometry=raw_geometry
CLEAN_PATHS=copy.deepcopy(G)
BASE_LABELS={c:spec[3].split(' · ',1)[-1] for c,spec in DESIGNS.items()}

def rr(c):return random.Random(17391+ord(c)*911)

def union(parts):
    parts=[p for p in parts if not p.is_empty]
    return unary_union(parts).buffer(0) if parts else Polygon()

def roughen(g,rng,amount=7,step=18):
    polys=[g] if g.geom_type=='Polygon' else list(g.geoms)
    out=[]
    for poly in polys:
        if poly.geom_type!='Polygon':continue
        rings=[]
        for ring in [poly.exterior,*poly.interiors]:
            pts=resample(list(ring.coords),step)
            rings.append([(x+rng.uniform(-amount,amount),y+rng.uniform(-amount,amount)) for x,y in pts[:-1]])
        if len(rings[0])>=3:out.append(Polygon(rings[0],[r for r in rings[1:] if len(r)>=3]).buffer(0))
    return union(out)

def grain(g,rng,count=80,rmin=3,rmax=9):
    x1,y1,x2,y2=g.bounds;inside=g.buffer(-7);holes=[]
    for _ in range(count*6):
        p=Point(rng.uniform(x1,x2),rng.uniform(y1,y2))
        if inside.covers(p):
            holes.append(p.buffer(rng.uniform(rmin,rmax),quad_segs=4))
            if len(holes)>=count:break
    return g.difference(union(holes)).buffer(0)

def grid(g,cell=42,gap=0,shape='square',phase=0):
    x1,y1,x2,y2=g.bounds;parts=[]
    for ix in range(math.floor(x1/cell),math.ceil(x2/cell)):
        for iy in range(math.floor(y1/cell),math.ceil(y2/cell)):
            x=(ix+.5)*cell;y=(iy+.5)*cell
            if g.covers(Point(x,y)):
                if shape=='dot':tile=Point(x,y).buffer(cell*.41,quad_segs=8)
                elif shape=='diamond':tile=diamonds([(x,y)],cell*.50)
                else:tile=box(x-cell/2+gap,y-cell/2+gap,x+cell/2-gap,y+cell/2-gap)
                parts.append(tile)
    return union(parts)

def ends(paths):
    return [p[i] for p in paths if len(p)>1 and p[0]!=p[-1] for i in [0,-1]]

def nib_stroke(paths,width=103,angle=-37):
    nib=rotate(box(-width/2,-17,width/2,17),angle,origin=(0,0))
    parts=[]
    for p in paths:
        if len(p)==1:parts.append(translate(nib,xoff=p[0][0],yoff=p[0][1]));continue
        for a,b in zip(p,p[1:]):
            parts.append(union([translate(nib,xoff=a[0],yoff=a[1]),translate(nib,xoff=b[0],yoff=b[1])]).convex_hull)
    return union(parts)

def warped(paths,seed,amplitude=10):
    result=[]
    for j,p in enumerate(paths):
        pts=resample(p,12) if len(p)>1 else p
        result.append([(x+amplitude*math.sin(y/83+j+seed*.2),y+amplitude*.5*math.sin(x/69+j+seed)) for x,y in pts])
    return result

def themed(paths,mode,w,c):
    rng=rr(c);seed=ord(c)
    p=copy.deepcopy(paths)
    if mode=='googly':
        body=stroke(oval(225,250,225,250),100,'round')
        eyes=[(142,522,72),(306,536,79)]
        outer=union([body,*[Point(x,y).buffer(r,quad_segs=24) for x,y,r in eyes]])
        whites=union([Point(x,y).buffer(r-14,quad_segs=24) for x,y,r in eyes])
        pupils=union([Point(153,509).buffer(22,quad_segs=18),Point(292,530).buffer(24,quad_segs=18)])
        return union([outer.difference(whites),pupils])
    if mode=='gothic' and c=='A':
        outer=[(0,0),(0,425),(170,670),(250,723),(331,670),(500,425),(500,0),(400,0),(400,220),(100,220),(100,0)]
        counter=[(100,306),(400,306),(400,426),(250,619),(100,426)]
        body=Polygon(outer,[counter])
        feet=[Polygon([(-36,0),(126,0),(100,67),(48,36),(0,75)]),Polygon([(374,0),(536,0),(500,75),(451,36),(400,67)])]
        flourish=stroke(path('M3 414 C-96 478 -41 637 48 615 L83 580'),25,'flat')
        cuts=diamonds([(50,146),(450,146)],21)
        return union([body,*feet,flourish]).difference(cuts)
    if mode=='swirl_a':
        bowl=stroke(oval(210,250,210,250),70,'round')
        stem=stroke(path('M420 500 L420 0 L485 26'),80,'round')
        spiral=stroke(path('M210 470 C-40 440 60 95 235 155 C390 205 275 370 190 305 Q135 259 198 234'),21,'round')
        return union([bowl,stem,spiral])
    if mode=='lace':
        outer=union([stroke(q,w,'round') for q in p]);shell=outer.difference(outer.buffer(-11))
        loops=[Point(x,y).buffer(27,quad_segs=12).difference(Point(x,y).buffer(17,quad_segs=12)) for q in p for x,y in resample(q,43)]
        return union([shell,*loops])
    if mode=='buttons':
        spine=union([stroke(q,20,'round') for q in p]);buttons=[]
        for q in p:
            for x,y in resample(q,98):
                button=Point(x,y).buffer(39,quad_segs=14)
                button=button.difference(union([Point(x-12,y).buffer(7,quad_segs=8),Point(x+12,y).buffer(7,quad_segs=8)]))
                buttons.append(button)
        return union([spine,*buttons])
    if mode=='sword' and c=='Ì':
        blade=Polygon([(172,595),(272,595),(259,107),(222,-34),(183,107)])
        guard=Polygon([(10,586),(94,638),(190,611),(256,611),(353,638),(432,586),(331,568),(110,568)])
        grip=stroke([(222,619),(222,751)],47,'flat')
        pommel=diamonds([(222,755)],44)
        foot=stroke([(125,31),(316,31)],23,'flat')
        groove=Polygon([(214,577),(233,577),(226,125),(220,57),(213,125)])
        return union([blade,guard,grip,pommel,foot]).difference(groove)
    if mode=='archway':
        body=union([stroke(q,w,'flat') for q in p])
        plinths=[union([box(x-44,-7,x+44,18),box(x-28,18,x+28,43)]) for x in [0,285,570]]
        return union([body,*plinths])
    if mode in ['chalk','felt','pencil','brush_ink','paper','stone','scribble','topography','ripple']:
        p=warped(p,seed,13 if mode not in ['pencil','chalk'] else 6)
    if mode in ['gothic','uncial','shards']:
        # Broad-nib contrast and diamond terminals are structural, not an outline filter.
        g=nib_stroke(p,w,-38 if mode!='uncial' else -18)
        finials=diamonds(ends(p),w*.47)
        g=union([g,finials])
        if mode=='gothic':
            for x,y in ends(p):g=union([g,Polygon([(x-65,y),(x+65,y),(x+20,y+75),(x-20,y+75)])])
        return g
    if mode=='brush_ink':
        return union([variable_stroke(q,w) for q in p])
    g=union([stroke(q,w,'round' if mode not in ['pixels','bricks','lego','barcode','knit','paper','stone'] else 'flat') for q in p])
    x1,y1,x2,y2=g.bounds
    if mode=='pixels':return grid(g,47)
    if mode=='dotmatrix':return grid(g,31,shape='dot')
    if mode=='pixel_mosaic':return grid(g,34,2.8)
    if mode=='chalk':return grain(roughen(g,rng,5),rng,120,2,8)
    if mode=='paper':return roughen(g,rng,13,22)
    if mode=='stone':
        g=roughen(g,rng,8,36)
        cracks=[stroke(path(f'M{x} {y1-30} L{x+29} {(y1+y2)/2} L{x-45} {y2+20}'),7,'flat') for x in [x1+80,(x1+x2)/2,x2-75]]
        return g.difference(union(cracks))
    if mode=='felt':
        g=roughen(g,rng,3)
        splashes=[Point(x+rng.uniform(-35,35),y+rng.uniform(-35,35)).buffer(rng.uniform(8,17),quad_segs=8) for x,y in ends(p)]
        return union([g,*splashes])
    if mode=='goo':
        additions=[]
        for j,x in enumerate([x1+w*.60,(x1+x2)/2,x2-w*.54]):
            ray=g.intersection(LineString([(x,-500),(x,1000)]))
            if ray.is_empty:continue
            yy=ray.bounds[1]+w*.2;length=[88,155,62][j]
            additions.append(stroke([(x,yy),(x,yy-length)],w*.32,'round'))
            additions.append(Point(x,yy-length).buffer(w*.23,quad_segs=14))
        for x,y in ends(p):additions.append(Point(x,y).buffer(w*.72,quad_segs=16))
        return union([g,*additions]).buffer(12).buffer(-12)
    if mode=='balloon':
        g=union([g,*[Point(x,y).buffer(w*.59,quad_segs=16) for q in p for x,y in resample(q,100)]]).buffer(13).buffer(-13)
        highlights=[]
        for q in p:
            pts=resample(q,160)
            for x,y in pts[1::2]:highlights.append(rotate(Point(x-w*.15,y+w*.10).buffer(w*.19,quad_segs=12),-30,origin=(x,y)))
        return g.difference(union(highlights).intersection(g.buffer(-20)))
    if mode=='bone':
        g=union([stroke(q,w*.65,'round') for q in p]);parts=[g]
        for x,y in ends(p):parts.extend([Point(x-22,y).buffer(37,quad_segs=12),Point(x+22,y).buffer(37,quad_segs=12)])
        return union(parts)
    if mode=='thorns':
        parts=[g]
        for q in p:
            for i,(x,y) in enumerate(resample(q,112)):
                dx=70*(-1 if i%2 else 1)
                parts.append(Polygon([(x,y-18),(x+dx,y+52),(x,y+28)]))
        return union(parts)
    if mode in ['bricks','lego','basket','knit','stitch','candy','tire','piano','chrome','barcode','accordion']:
        cuts=[]
        if mode in ['bricks','lego']:
            for k,y in enumerate(range(-120,1000,68)):
                cuts.append(box(-250,y,1000,y+9))
                for x in range(-160+(k%2)*52,1000,104):cuts.append(box(x,y,x+8,y+68))
            out=g.difference(union(cuts))
            if mode=='lego':
                knobs=[Point(x,y).buffer(14,quad_segs=10).difference(Point(x,y).buffer(6,quad_segs=10)) for y in range(25,750,68) for x in range(20,650,104) if g.covers(Point(x,y))]
                out=union([out,*knobs])
            return out
        if mode=='basket':
            cuts=[rotate(box(-300,y,1100,y+9),a,origin=(230,300)) for y in range(-200,1100,43) for a in [40,-40]]
        elif mode=='knit':
            cuts=[stroke([(x-11,y+15),(x,y-8),(x+11,y+15)],6,'round') for y in range(-100,850,38) for x in range(-100,900,28)]
        elif mode=='stitch':
            cuts=[stroke([(x-15,y-13),(x+15,y+13)],6,'round') for q in p for x,y in resample(q,41)]
        elif mode in ['candy','tire','accordion']:
            thick=25 if mode=='candy' else 10
            cuts=[rotate(box(-250,y,1100,y+thick),35 if mode!='tire' else -35,origin=(250,350)) for y in range(-300,1200,64 if mode!='accordion' else 37)]
        elif mode=='piano':cuts=[box(x,0,x+11,900) for x in range(-30,900,55)]
        elif mode=='chrome':
            cuts=[rotate(box(-300,y,1100,y+thick),-16,origin=(250,350)) for y,thick in [(180,12),(210,29),(420,8),(460,37)]]
        elif mode=='barcode':
            cuts=[box(-200,y,1100,y+rrr) for y,rrr in [(j*31,4+((j*7)%14)) for j in range(-4,30)]]
        return g.difference(union(cuts).intersection(g.buffer(-12 if mode!='chrome' else -22)))
    if mode in ['copper_pipe','wire_cage','hairpin','zipper','ladder']:
        g=g.difference(g.buffer(-16 if mode!='hairpin' else -12))
        if mode=='hairpin':return g
        links=[]
        for q in p:
            for x,y in resample(q,80 if mode=='copper_pipe' else 48):
                links.append(box(x-w*.7,y-9,x+w*.7,y+9))
        if mode=='wire_cage':links += [stroke([(x,y),(x+35,y+42)],10,'flat') for q in p for x,y in resample(q,70)]
        return union([g,*links]).intersection(union([stroke(q,w+24,'round') for q in p]))
    if mode in ['chain','spring','braid','pencil','scribble','topography']:
        if mode=='chain':
            return union([Point(x,y).buffer(w*.47,quad_segs=12).difference(Point(x,y).buffer(w*.28,quad_segs=12)) for q in p for x,y in resample(q,w*.67)])
        if mode=='spring':
            return union([scale(Point(x,y).buffer(40,quad_segs=14).difference(Point(x,y).buffer(27,quad_segs=14)),xfact=1.35,yfact=.52,origin=(x,y)) for q in p for x,y in resample(q,27)])
        if mode=='topography':
            return union([union([stroke(warped([q],seed+j,j*2+1)[0],ww,'round') for q in p]).boundary.buffer(6) for j,ww in enumerate([52,94,138])])
        if mode=='pencil':
            return union([stroke(warped([q],seed+j,3+j*2)[0],13 if j else 21,'round') for j in range(3) for q in p])
        if mode=='scribble':
            return union([translate(stroke(warped([q],seed+j,10)[0],8,'round'),xoff=(j-2)*9) for j in range(5) for q in p])
        # Three intertwined cords with alternating crossings.
        parts=[]
        for q in p:
            pts=resample(q,10)
            for j in range(3):
                strand=[(x+24*math.sin(k*.8+j*math.tau/3),y+14*math.cos(k*.8+j*math.tau/3)) for k,(x,y) in enumerate(pts)]
                parts.append(stroke(strand,12,'round'))
        return union(parts)
    if mode in ['wheat','feather','coral','saw','flame','snowflake','vine']:
        parts=[g]
        for q in p:
            for j,(x,y) in enumerate(resample(q,81 if mode not in ['feather','saw'] else 45)):
                sign=1 if j%2 else -1
                if mode=='vine':
                    parts.append(rotate(scale(Point(x+sign*31,y+22).buffer(28,quad_segs=10),xfact=1.25,yfact=.48,origin=(x+sign*31,y+22)),sign*35,origin=(x,y)))
                elif mode=='snowflake':
                    parts += [stroke([(x,y),(x+sign*54,y+36),(x+sign*38,y+38)],13,'flat'),stroke([(x+sign*36,y+25),(x+sign*42,y+7)],10,'flat')]
                elif mode=='coral':
                    parts += [stroke([(x,y),(x+sign*48,y+53),(x+sign*29,y+78)],19,'round'),Point(x+sign*48,y+53).buffer(16,quad_segs=10)]
                elif mode=='flame':
                    parts.append(Polygon([(x-23,y),(x+12,y+88),(x+38,y+20),(x+23,y-14)]))
                elif mode=='wheat':parts.append(rotate(scale(Point(x+sign*24,y+24).buffer(28,quad_segs=10),xfact=.4,yfact=1,origin=(x+sign*24,y+24)),sign*-38,origin=(x,y)))
                else:parts.append(Polygon([(x,y-11),(x+sign*(59 if mode=='feather' else 42),y+37),(x,y+23)]))
        return union(parts)
    if mode in ['honeycomb','flower','sun','orbital']:
        if mode=='honeycomb':
            holes=[]
            for j,y in enumerate(range(-100,900,48)):
                for x in range(-100+(j%2)*28,850,56):
                    holes.append(Polygon([(x+24*math.cos(k*math.tau/6),y+24*math.sin(k*math.tau/6)) for k in range(6)]).boundary.buffer(4))
            return g.difference(union(holes).intersection(g.buffer(-12)))
        if mode=='orbital':
            return union([stroke([(x+(j-1)*25,y) for x,y in q],15,'round') for q in p for j in range(3)])
        petals=[]
        for q in p:
            for x,y in resample(q,71 if mode=='flower' else 102):
                cx=(x1+x2)/2;cy=(y1+y2)/2;dx=x-cx;dy=y-cy;ll=math.hypot(dx,dy) or 1
                if mode=='sun':petals.append(stroke([(x,y),(x+dx/ll*57,y+dy/ll*57)],17,'flat'))
                else:petals.append(Point(x+dx/ll*15,y+dy/ll*15).buffer(37,quad_segs=12))
        return union([g,*petals])
    if mode in ['negative_stamp','negative_seal']:
        if mode=='negative_stamp':
            plate=box(x1-35,y1-35,x2+35,y2+35)
            bites=[Point(x,y).buffer(12,quad_segs=8) for x in [x1-35,x2+35] for y in range(round(y1),round(y2),39)]
            bites += [Point(x,y).buffer(12,quad_segs=8) for y in [y1-35,y2+35] for x in range(round(x1),round(x2),39)]
            return plate.difference(union([g,*bites]))
        cx=(x1+x2)/2;cy=(y1+y2)/2
        plate=scale(Point(cx,cy).buffer(1,quad_segs=60),xfact=(x2-x1)/2+43,yfact=(y2-y1)/2+43,origin=(cx,cy))
        return plate.difference(g)
    if mode=='duotone':
        left=g.intersection(box(x1-1,y1-1,(x1+x2)/2,y2+1));right=g.difference(g.buffer(-16)).intersection(box((x1+x2)/2,y1-1,x2+1,y2+1))
        return union([left,right])
    if mode=='puzzle':
        knots=[];bites=[]
        for j,(x,y) in enumerate([pt for q in p for pt in resample(q,140)]):
            (knots if j%2 else bites).append(Point(x+w*.44,y).buffer(24,quad_segs=12))
        return union([g,*knots]).difference(union(bites))
    if mode=='bamboo':
        bands=[box(x-w*.72,y-10,x+w*.72,y+10) for q in p for x,y in resample(q,126)]
        return union([g,*bands]).difference(union([box(x-w*.30,y+17,x+w*.30,y+24) for q in p for x,y in resample(q,126)]))
    if mode=='pebbles':
        return union([scale(Point(x,y).buffer(w*.56,quad_segs=9),xfact=rng.uniform(.73,1.20),yfact=rng.uniform(.68,1.08),origin=(x,y)) for q in p for x,y in resample(q,w*.78)])
    if mode=='candle':
        g=union([stroke(q,w,'flat') for q in p])
        drip=stroke([(20,480),(72,451),(72,319)],22,'round')
        seam=stroke(path('M-46 424 Q-5 378 36 417 Q52 442 53 460'),10,'round')
        return union([g,drip,Point(72,319).buffer(19,quad_segs=10)]).difference(seam)
    if mode=='beads':return union([Point(x,y).buffer(w*.46,quad_segs=16) for q in p for x,y in resample(q,w*1.0)])
    if mode=='icicle':
        spikes=[Polygon([(x-24,y+12),(x+24,y+12),(x+8,y-110-rng.randrange(40))]) for q in p for x,y in resample(q,170)]
        return union([g,*spikes])
    if mode=='ripple':return union([stroke(warped([q],seed,20)[0],w,'round') for q in p])
    if mode=='circuit':
        dots=[Point(x,y).buffer(35,quad_segs=12).difference(Point(x,y).buffer(16,quad_segs=12)) for q in p for x,y in resample(q,145)]
        return union([union([stroke(q,27,'flat') for q in p]),*dots])
    if mode=='lightning':
        jagged=[]
        for q in p:
            pts=resample(q,95)
            jagged.append([(x+(-23 if j%2 else 23),y) for j,(x,y) in enumerate(pts)])
        return union([stroke(q,w,'flat') for q in jagged])
    if mode in ['filigree','crown','sword']:
        body=nib_stroke(p,w,-35) if mode=='sword' else union([stroke(q,w,'round') for q in p])
        ornaments=[]
        for x,y in ends(p):
            if mode=='sword':ornaments.append(Polygon([(x-43,y),(x,y+77),(x+43,y),(x,y-25)]))
            else:
                ornaments.append(stroke(path(f'M{x} {y} C{x+85} {y+110} {x+133} {y-40} {x+60} {y-15}'),14,'round'))
                if mode=='crown':ornaments.append(diamonds([(x+60,y+35)],24))
        return union([body,*ornaments])
    raise ValueError('Unimplemented theme: '+mode)

PRIMARY={
'A':('gothic',135,0,'Gothic blackletter'),
'B':('balloon',134,0,'Inflated vinyl'),
'G':('felt',92,.12,'Graffiti marker'),
'H':('bone',67,0,'Knuckled bones'),
'M':('pixels',96,0,'Chunky arcade pixels'),
'R':('thorns',80,0,'Punk thorns'),
'W':('filigree',35,0,'Wrought-iron scrolls'),
'b':('bricks',105,0,'Brickwork'),
'e':('brush_ink',74,-.05,'Loose ink handwriting'),
'h':('basket',107,0,'Woven basket'),
'i':('circuit',44,0,'Circuit column'),
'm':('archway',39,0,'Roman aqueduct'),
'o':('googly',100,0,'Googly-eyed creature'),
'q':('stone',91,.03,'Fractured stone'),
's':('pencil',44,.11,'Repeated pencil strokes'),
'u':('goo',126,0,'Dripping goo'),
'2':('chalk',85,.025,'Rough chalk'),
'3':('accordion',119,0,'Pleated paper'),
'5':('knit',123,0,'Knitted wool'),
'9':('topography',87,0,'Fingerprint contours'),
'#':('bamboo',58,.04,'Bamboo lattice'),
'$':('shards',83,0,'Engraved currency'),
'&':('vine',36,0,'Climbing vine'),
'?':('paper',94,.025,'Torn-paper question'),
'@':('scribble',56,0,'Scribbled spiral'),
'%':('circuit',69,0,'Electronic percentage'),
'€':('piano',101,0,'Euro keys'),
'£':('chrome',100,0,'Chrome pound'),
'¥':('saw',51,0,'Serrated yen'),
'{':('feather',28,0,'Feather brace'),
'}':('coral',26,0,'Coral brace'),
'*':('snowflake',22,0,'Snow crystal'),
'+':('lego',96,0,'Building-block plus'),
'~':('spring',74,0,'Coiled spring'),
'←':('lightning',54,0,'Lightning arrow'),
'→':('copper_pipe',82,0,'Pipework arrow'),
'↑':('crown',32,0,'Crowned arrow'),
'↓':('icicle',43,0,'Falling icicle')}
# One complete body treatment per accented character. No composite parent glyphs.
ACCENT={
'À':('pixel_mosaic',115,0,'Mosaic A'), 'Á':('brush_ink',100,.13,'Brush A'),
'Â':('icicle',78,0,'Ice A'), 'Ã':('ripple',51,0,'Ripple A'),
'Ä':('copper_pipe',99,0,'Plumbed A'), 'Å':('chain',79,0,'Chain-link A'),
'Ç':('vine',38,0,'Vine C'),
'È':('lego',119,0,'Toy-brick E'), 'É':('dotmatrix',100,0,'LED-matrix E'),
'Ê':('wheat',30,0,'Wheat E'), 'Ë':('wire_cage',103,0,'Wire-cage E'),
'Ì':('sword',112,-.10,'Sword I'), 'Í':('barcode',148,0,'Barcode I'),
'Î':('filigree',34,0,'Scrolled I'), 'Ï':('knit',130,0,'Cross-knit I'),
'Ñ':('negative_stamp',71,0,'Postage-stamp N'),
'Ò':('honeycomb',148,0,'Honeycomb O'), 'Ó':('sun',53,0,'Sunburst O'),
'Ô':('uncial',119,0,'Medieval uncial O'), 'Õ':('scribble',70,.045,'Scribbled O'),
'Ö':('orbital',60,0,'Orbital O'),
'Ù':('piano',126,0,'Piano-key U'), 'Ú':('chrome',139,0,'Liquid-chrome U'),
'Û':('circuit',70,0,'Circuit-board U'), 'Ü':('zipper',97,0,'Zipped U'),
'Ý':('feather',40,0,'Feather Y'), 'Ÿ':('crown',54,0,'Crowned Y'),
'à':('paper',96,0,'Torn-paper a'), 'á':('swirl_a',78,0,'Spiral a'),
'â':('lace',98,0,'Lacework a'), 'ã':('braid',82,0,'Braided a'),
'ä':('duotone',116,0,'Half-filled a'), 'å':('negative_seal',61,0,'Wax-seal a'),
'ç':('coral',26,0,'Coral c'),
'è':('candy',121,0,'Candy-stripe e'), 'é':('buttons',78,0,'Button-thread e'),
'ê':('flame',55,0,'Flaming e'), 'ë':('pebbles',94,0,'Pebble e'),
'ì':('candle',111,0,'Wax-candle i'), 'í':('beads',75,0,'Beaded i'),
'î':('spring',86,0,'Spring i'), 'ï':('ladder',115,0,'Ladder i'),
'ñ':('puzzle',97,0,'Jigsaw n'),
'ò':('tire',144,0,'Tyre-tread o'), 'ó':('topography',94,0,'Contour-map o'),
'ô':('flower',49,0,'Flower o'), 'õ':('stone',120,0,'Cracked-stone o'),
'ö':('pixel_mosaic',106,0,'Pixel-tile o'),
'ù':('stitch',135,0,'Stitched-leather u'), 'ú':('bamboo',75,.02,'Bamboo u'),
'û':('saw',50,0,'Sawblade u'), 'ü':('hairpin',87,.09,'Bent-wire u'),
'ý':('lightning',62,0,'Lightning y'), 'ÿ':('snowflake',31,0,'Crystalline y')}

def superoval(cx,cy,rx,ry,n=3):
    return [(cx+rx*math.copysign(abs(math.cos(k*math.tau/100))**(2/n),math.cos(k*math.tau/100)),
             cy+ry*math.copysign(abs(math.sin(k*math.tau/100))**(2/n),math.sin(k*math.tau/100))) for k in range(101)]

def accented_skeleton(c):
    base,mark=unicodedata.normalize('NFD',c);mode=ACCENT[c][0]
    paths=copy.deepcopy(CLEAN_PATHS[base])
    # Lowercase i uses a continuous body; the diacritic replaces its dot.
    if base=='i':paths=[path('M0 0 L0 500')]
    if base=='a':
        if c in 'àâä':paths=[oval(205,250,205,250),path('M410 500 L410 0')]
        else:paths=copy.deepcopy(CLEAN_PATHS['a'])
    if base in 'Oo':
        h=700 if base=='O' else 500;rx=240 if base=='O' else 215
        n={'honeycomb':4.1,'sun':2.0,'uncial':2.0,'scribble':2.35,'orbital':2.0,
           'tire':2.6,'topography':2.3,'flower':2.0,'stone':5.4,'pixel_mosaic':3.8}[mode]
        paths=[superoval(rx,h/2,rx,h/2,n)]
        if c=='Ô':paths=[path('M240 700 L75 520 L75 180 L240 0 L415 180 L415 520 Z')]
    if base in 'Uu' and mode in ['circuit','zipper','bamboo','stitch']:
        h=700 if base=='U' else 500
        paths=[path(f'M0 {h} L0 120 Q0 0 120 0 L300 0 Q420 0 420 120 L420 {h}')]
    if base=='A':
        if mode in ['pixel_mosaic','copper_pipe']:paths=[path('M0 0 L0 440 L205 700 L285 700 L490 440 L490 0'),path('M0 250 L490 250')]
        elif mode=='brush_ink':paths=[path('M-20 0 Q120 400 260 700 Q345 400 485 0'),path('M60 230 Q220 325 410 270')]
        elif mode=='ripple':paths=[path('M0 0 L245 700 L490 0'),path('M83 240 L405 240')]
    if mode in ['circuit','lego','dotmatrix','pixel_mosaic']:
        paths=[[(round(x/23)*23,round(y/23)*23) for x,y in p] for p in paths]
    return base,mark,paths

# Stronger blackletter A and a proper continuous i before the theme is applied.
G['A']=[path('M0 0 L225 700 L480 0'),path('M70 210 L400 270'),path('M15 460 L100 625 L205 700')]
G['H']=[path('M0 0 L0 700'),path('M480 0 L480 700'),path('M0 350 L480 350')]
G['i']=[path('M-55 490 L0 490 L0 0 L70 0'),[(0,675)]]
G['m']=[path('M0 0 L0 500'),path('M0 340 C0 570 285 570 285 340 L285 0'),path('M285 340 C285 570 570 570 570 340 L570 0')]

def body_raw(c):
    if c in ACCENT:
        base,mark,paths=accented_skeleton(c);mode,w,slant,label=ACCENT[c]
        return themed(paths,mode,w,c),base,w,slant,mode,label
    if c in PRIMARY:
        mode,w,slant,label=PRIMARY[c]
        return themed(G[c],mode,w,c),c,w,slant,mode,label
    mode,w,slant,label=DESIGNS[c]
    return old_raw_geometry(c),c,w,slant,mode,BASE_LABELS[c]

def normalize_body(c):
    geom,base,w,slant,mode,label=body_raw(c)
    if base.isascii() and base.isalnum():
        desc=base in 'Qfgjpqy' or mode in ['goo','icicle','candle']
        low=-w/2 if desc else geom.bounds[1]
        target=710 if base.isupper() or base.isdigit() or base in 'bdfhkl' else 520
        top=geom.bounds[3]
        if base in 'ij' and c not in ACCENT:top=500+w/2
        geom=scale(translate(geom,yoff=-low),xfact=1,yfact=target/(top-low),origin=(0,0))
    else:geom=translate(geom,yoff=18)
    geom=skew(geom,xs=math.degrees(math.atan(slant)),origin=(0,0)).simplify(.55,preserve_topology=True).buffer(0)
    return geom,mode,label

MARKS={'\u0301':[path('M-65 0 L75 120')],'\u0300':[path('M-75 120 L65 0')],
'\u0302':[path('M-130 0 L0 125 L130 0')],'\u0303':[path('M-140 30 C-60 150 65 -80 145 50')],
'\u0308':[[(-100,60)],[(100,60)]],'\u030a':[oval(0,62,69,62)],'\u0327':[path('M10 0 L-35 -68 C132 -58 100 -195 -45 -158')]}

def mark_geometry(c,mode):
    base,mark=unicodedata.normalize('NFD',c);p=MARKS[mark]
    weight=38 if mode in ['wire_cage','filigree','chain','hairpin','scribble','spring'] else 47
    markg=union([stroke(q,weight,'round') for q in p])
    if mode in ['pixel_mosaic','dotmatrix','lego','barcode']:markg=grid(markg,17,1 if mode=='pixel_mosaic' else 0)
    elif mark=='\u0308' and mode in ['ladder','wire_cage','orbital','flower','snowflake']:
        markg=union([diamonds(q,38) if mode in ['ladder','snowflake'] else Point(q[0]).buffer(38,quad_segs=12).difference(Point(q[0]).buffer(19,quad_segs=12)) for q in p])
    elif mode in ['paper','stone','stitch']:markg=roughen(markg,rr(c),4,17)
    return markg

def fit_glyph(c,body,mono=True):
    g=body
    limit=532 if mono else 720
    width=g.bounds[2]-g.bounds[0]
    if width>limit:g=scale(g,xfact=limit/width,yfact=1,origin=(0,0))
    if c in ACCENT:
        base,mark=unicodedata.normalize('NFD',c);mode=ACCENT[c][0]
        m=mark_geometry(c,mode);x1,y1,x2,y2=g.bounds
        center=(x1+x2)/2;yy=-10 if mark=='\u0327' else y2+82
        g=union([g,translate(m,xoff=center,yoff=yy)])
    width=g.bounds[2]-g.bounds[0]
    if width>limit:g=scale(g,xfact=limit/width,yfact=1,origin=(0,0));width=limit
    adv=640 if mono else math.ceil(width+86)
    g=translate(g,xoff=(adv-width)/2-g.bounds[0])
    return g,int(adv)

BODIES={};LABELS={}
for c in list(G)+list(ACCENT):
    body,mode,label=normalize_body(c);BODIES[c]=body;LABELS[c]=label
assert len(ACCENT)==54


# Additional directly encoded symbols and programming ligatures.
def symbol_paths(*paths, weight=48):
    return union([stroke(path(p),weight,'round') for p in paths])

EXTRA_SYMBOLS={
    '↔':(symbol_paths('M0 300 L620 300','M160 460 L0 300 L160 140','M460 460 L620 300 L460 140'), 'Double-headed spear'),
    '⇐':(symbol_paths('M200 245 L620 245','M200 355 L620 355','M215 500 L0 300 L215 100',weight=40), 'Twin-rail left arrow'),
    '⇒':(symbol_paths('M0 245 L420 245','M0 355 L420 355','M405 500 L620 300 L405 100',weight=40), 'Twin-rail right arrow'),
    '⇔':(symbol_paths('M200 245 L420 245','M200 355 L420 355','M215 500 L0 300 L215 100','M405 500 L620 300 L405 100',weight=40), 'Twin-rail bidirectional arrow'),
    '≡':(symbol_paths('M0 140 L500 140','M0 300 L500 300','M0 460 L500 460',weight=50), 'Triple-bar identity'),
    '≢':(symbol_paths('M0 140 L500 140','M0 300 L500 300','M0 460 L500 460','M150 40 L350 560',weight=44), 'Slashed identity'),
    '≈':(symbol_paths('M0 230 C140 410 360 50 500 230','M0 400 C140 580 360 220 500 400',weight=46), 'Ribbon approximation'),
}
for c,(body,label) in EXTRA_SYMBOLS.items():
    BODIES[c]=body;LABELS[c]=label
LIGATURES={
    '<=':'≤','>=':'≥','!=':'≠','==':'=','===':'≡','!==':'≢',
    '<-':'←','->':'→','<->':'↔','=>':'⇒','<=>':'⇔',
    '<--':'←','-->':'→','<==':'⇐','==>':'⇒','~=':'≈',
}
def ligature_name(sequence):
    return 'lig_'+'_'.join(f'{ord(c):04X}' for c in sequence)

FAMILIES=[('MixedCompany','MixedCompany',False),('MixedCompany Mono','MixedCompanyMono',True)]
BUILT={}
for family,stem,mono in FAMILIES:
    out=ROOT/'outputs'/stem;out.mkdir(exist_ok=True)
    shapes={};metrics={};glyphs={};cmap={}
    miss=box(85,0,555,710).difference(box(125,40,515,670))
    glyphs['.notdef']=as_glyph(miss);metrics['.notdef']=(640,85)
    glyphs['space']=TTGlyphPen(None).glyph();metrics['space']=(640 if mono else 305,0);cmap[32]='space';cmap[160]='space'
    for c,body in BODIES.items():
        g,adv=fit_glyph(c,body,mono);name='uni%04X'%ord(c)
        shapes[c]=g;glyphs[name]=as_glyph(g);metrics[name]=(adv,round(g.bounds[0]));cmap[ord(c)]=name
    for sequence,symbol in LIGATURES.items():
        g=BODIES[symbol]
        advance=sum(metrics[cmap[ord(c)]][0] for c in sequence)
        x1,y1,x2,y2=g.bounds
        # Multi-character glyphs retain the original text's total advance.
        g=scale(translate(g,xoff=-x1),xfact=(advance-108)/(x2-x1),yfact=1,origin=(0,0))
        g=translate(g,xoff=54)
        name=ligature_name(sequence)
        glyphs[name]=as_glyph(g);metrics[name]=(advance,54)
    fb=FontBuilder(1000,isTTF=True);fb.setupGlyphOrder(list(glyphs));fb.setupCharacterMap(cmap);fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=1040,descent=-380,lineGap=0)
    fb.setupNameTable({'familyName':family,'styleName':'Regular','uniqueFontIdentifier':family+' 3.002 Original 2026',
    'fullName':family+' Regular','psName':stem+'-Regular','version':'Version 3.002',
    'copyright':'Original vector design created for Stuart Alldred, 2026.',
    'description':'Wild display lettering with separately styled accented character bodies. '+('Each character has a 640-unit advance; ligatures preserve their input column count.' if mono else 'Proportional widths and optical kerning.')})
    fb.setupOS2(sTypoAscender=1040,sTypoDescender=-380,sTypoLineGap=0,usWinAscent=1040,usWinDescent=380,
                sxHeight=520,sCapHeight=710,usWeightClass=400,usWidthClass=5,fsType=0,fsSelection=0x40)
    fb.font['OS/2'].panose.bFamilyType=2;fb.font['OS/2'].panose.bProportion=9 if mono else 0
    fb.setupPost(isFixedPitch=1 if mono else 0);fb.setupMaxp();fb.font['head'].fontRevision=3.002
    from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
    feature=''
    if not mono:
        pairs={p:v for p,v in {'AV':-30,'AW':-25,'AY':-35,'AT':-23,'VA':-30,'WA':-22,'YA':-30,'TA':-22,'To':-25,'Ta':-22,'Te':-20,'Yo':-28,'Ya':-25,'Vo':-24,'Va':-22,'Wo':-18,'Wa':-18,'LT':-20,'LY':-25,'FA':-18,'PA':-24}.items()}
        kt={(cmap[ord(pair[0])],cmap[ord(pair[1])]):value for pair,value in pairs.items()}
        kern=newTable('kern');kern.version=0;sub=KernTable_format_0();sub.version=0;sub.coverage=1;sub.kernTable=kt;kern.kernTables=[sub];fb.font['kern']=kern
        feature='feature kern {\n'+''.join(f'pos {a} {b} {v};\n' for (a,b),v in kt.items())+'} kern;'
    feature+='\nfeature liga {\n'
    for sequence in sorted(LIGATURES,key=lambda seq:-len(seq)):
        inputs=' '.join(cmap[ord(c)] for c in sequence)
        feature+=f'sub {inputs} by {ligature_name(sequence)};\n'
    feature+='} liga;'
    addOpenTypeFeaturesFromString(fb.font,feature)
    fontpath=out/(stem+'-Regular.ttf');fb.save(fontpath)
    web=TTFont(fontpath);web.flavor='woff2';web.save(out/(stem+'-Regular.woff2'))
    BUILT[stem]={'family':family,'out':out,'font':fontpath,'mono':mono,'shapes':shapes,'cmap':cmap,'metrics':metrics}

# Draw every preview using the actual finished fonts.
PAPER='#f5f0e4';INK='#252621';RED='#d33b31';LINE='#c9c1b2';MUTED='#78786b';LIME='#d8eb65'
ui='/System/Library/Fonts/Supplemental/Arial.ttf';uib='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def uifont(size,bold=False):return ImageFont.truetype(uib if bold else ui,size)
def df(stem,size):return ImageFont.truetype(str(BUILT[stem]['font']),size)

for stem,info in BUILT.items():
    im=Image.new('RGB',(1800,2290),PAPER);d=ImageDraw.Draw(im)
    def text(x,y,s,size=28,display=False,color=INK,bold=False):d.text((x,y),s,font=df(stem,size) if display else uifont(size,bold),fill=color,anchor='lt')
    def rule(y):d.line((80,y,1720,y),fill=LINE,width=2)
    text(80,62,'MIXEDCOMPANY',25,bold=True);text(1330,62,'MONO / 03' if info['mono'] else 'PROPORTIONAL / 03',24)
    rule(112)
    text(80,166,'MixedCompany',179,True)
    text(80,378,'Gothic. Goo. Chalk. Pixels. And googly eyes.',33,bold=True)
    text(80,440,'186 characters · 54 independently styled accented letters',26,color=MUTED)
    rule(503)
    text(80,537,'01 / THE CAPITALS',23,color=RED,bold=True)
    for row,s in enumerate(['ABCDEFGHIJKLM','NOPQRSTUVWXYZ']):
        size=173
        while d.textlength(s,font=df(stem,size))>1630:size-=1
        text(80,596+175*row,s,size,True)
    rule(956)
    text(80,991,'02 / THE LOWERCASE',23,color=RED,bold=True)
    for row,s in enumerate(['abcdefghijklm','nopqrstuvwxyz']):
        size=169
        while d.textlength(s,font=df(stem,size))>1630:size-=1
        text(80,1051+183*row,s,size,True)
    rule(1440)
    text(80,1477,'03 / NUMBERS',23,color=RED,bold=True)
    text(80,1546,'0123456789',177,True)
    rule(1761)
    text(80,1799,'04 / THE ACCENTS HAVE ALTER EGOS',23,color=RED,bold=True)
    text(80,1868,'AÀÁÂÃÄÅ',163,True)
    text(80,2076,'uùúûü  eéèêë',144,True)
    im.save(info['out']/(stem+'-Preview.png'))

# Both compact family comparisons and the complete labelled atlas.
STEM='MixedCompanyMono';info=BUILT[STEM]
groups=['AÀÁÂÃÄÅ','aàáâãäå','CÇ cç','EÈÉÊË','eèéêë','IÌÍÎÏ','iìíîï','NÑ nñ','OÒÓÔÕÖ','oòóôõö','UÙÚÛÜ','uùúûü','YÝŸ yýÿ']
im=Image.new('RGB',(1800,2780),PAPER);d=ImageDraw.Draw(im)
d.text((80,50),'EVERY ACCENT HAS AN ALTER EGO',font=uifont(34,True),fill=INK)
d.text((80,106),'Parent letters in grey. Accented bodies are separate designs.',font=uifont(25),fill=MUTED)
for row,s in enumerate(groups):
    yy=177+row*194
    for col,c in enumerate(s):
        if c==' ':continue
        x=80+col*221
        d.text((x,yy),c,font=df(STEM,143),fill=INK if c in ACCENT else '#9b988e',anchor='lt')
        label=LABELS[c] if c in ACCENT else 'parent '+c
        size=18
        while d.textlength(label,font=uifont(size))>207:size-=1
        d.text((x,yy+146),label,font=uifont(size),fill=RED if c in ACCENT else MUTED)
    d.line((80,yy+177,1720,yy+177),fill=LINE,width=1)
im.save(ROOT/'outputs'/'MixedCompany-Accent-Families.png')

chars=[chr(cp) for cp in sorted(info['cmap']) if cp not in (32,160)]
cols=10;cw=169;ch=189
atlas=Image.new('RGB',(cols*cw+100,math.ceil(len(chars)/cols)*ch+180),PAPER);d=ImageDraw.Draw(atlas)
d.text((50,36),'MIXEDCOMPANY / COMPLETE CHARACTER & STYLE ATLAS',font=uifont(30,True),fill=INK)
for i,c in enumerate(chars):
    x=50+(i%cols)*cw;y=119+(i//cols)*ch
    d.rectangle((x,y,x+cw,y+ch),outline=LINE)
    d.text((x+(cw-99*.64)/2,y+112),c,font=df(STEM,99),fill=INK,anchor='ls')
    d.text((x+8,y+137),f'{c}  U+{ord(c):04X}',font=uifont(14),fill=MUTED)
    label=LABELS[c];size=13
    while d.textlength(label,font=uifont(size))>cw-15 and size>9:size-=1
    d.text((x+8,y+159),label,font=uifont(size),fill=RED)
atlas.save(ROOT/'outputs'/'MixedCompany-Character-Atlas.png')

# The same words in both actual fonts, including narrow-letter and spacing cases.
compare=Image.new('RGB',(1800,1330),PAPER);d=ImageDraw.Draw(compare)
d.text((80,45),'SAME CHARACTERS / TWO SPACING SYSTEMS',font=uifont(30,True),fill=INK)
for j,(stem,info) in enumerate(BUILT.items()):
    y=135+j*575
    d.text((80,y),info['family'].upper(),font=uifont(25,True),fill=RED)
    for k,s in enumerate(['A little weird?','Voilà! Déjà vu.','iiii  WWWW  1234']):
        d.text((80,y+72+k*150),s,font=df(stem,124),fill=INK,anchor='lt')
    d.line((80,y+535,1720,y+535),fill=LINE,width=2)
compare.save(ROOT/'outputs'/'MixedCompany-Spacing-Comparison.png')

encoded={stem:base64.b64encode((info['out']/(stem+'-Regular.woff2')).read_bytes()).decode() for stem,info in BUILT.items()}
cards=''.join('<div class="glyph"><span>'+html.escape(c)+'</span><small>'+html.escape(LABELS[c])+'</small></div>' for c in chars)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MixedCompany / try both fonts</title><style>
@font-face{font-family:MixedCompany;src:url(data:font/woff2;base64,PROPFONT) format('woff2')}@font-face{font-family:MixedCompanyMono;src:url(data:font/woff2;base64,MONOFONT) format('woff2')}*{box-sizing:border-box}body{margin:0;background:#f5f0e4;color:#252621;font:16px system-ui,sans-serif}main{max-width:1240px;padding:34px 28px;margin:auto}header{display:flex;justify-content:space-between;gap:24px;border-bottom:1px solid #c9c1b2;padding-bottom:24px;font-size:13px;letter-spacing:.07em}h1{font:clamp(43px,6.2vw,84px)/1.5 MixedCompany;margin:35px 0 14px}p{line-height:1.6;max-width:820px}nav{display:flex;flex-wrap:wrap;gap:22px;align-items:center;border-top:1px solid #c9c1b2;padding:23px 0;margin-top:30px}label{display:inline-flex;gap:10px;align-items:center;font-size:14px}select{padding:9px 12px;border:1px solid #b8b2a6;background:transparent;border-radius:4px;font:inherit}input{accent-color:#d33b31}textarea{font:74px/1.52 MixedCompany;width:100%;height:410px;background:transparent;color:inherit;border:1px solid #c9c1b2;resize:vertical;padding:20px;outline-color:#d33b31;font-synthesis:none}.mono{font-family:MixedCompanyMono;font-kerning:none;font-variant-ligatures:common-ligatures}.tip{font-size:13px;color:#77766b}.status{min-height:24px;color:#b23c2f;font-size:14px}h2{font-size:14px;letter-spacing:.1em;text-transform:uppercase;color:#d33b31;margin:43px 0 22px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));border-left:1px solid #c9c1b2;border-top:1px solid #c9c1b2}.glyph{min-height:153px;display:flex;flex-direction:column;align-items:center;justify-content:center;border-right:1px solid #c9c1b2;border-bottom:1px solid #c9c1b2;text-align:center;padding:5px}.glyph span{font:74px/1.5 MixedCompany}.grid.mono .glyph span{font-family:MixedCompanyMono}.glyph small{font-size:10px;color:#747466;line-height:1.4}footer{border-top:1px solid #c9c1b2;padding-top:20px;margin-top:40px;font-size:13px;color:#747466}</style>
<main><header><strong>MIXEDCOMPANY</strong><span>STANDARD + MONO</span></header><h1>MixedCompany</h1><p>Gothic, goo, chalk, pixels, handwriting, vines, bones and more. Every accented character has an independently styled body. Switch between proportional spacing and a strict one-character-per-column grid.</p><nav><label>Font <select id="face"><option value="MixedCompany">Proportional</option><option value="MixedCompanyMono">Monospaced</option></select></label><label>Size <input id="size" type="range" min="28" max="150" value="74"><output id="sizeout">74 px</output></label><label>Ink <input id="ink" type="color" value="#252621"></label></nav><textarea id="tester" aria-label="Try the MixedCompany fonts" spellcheck="false">A little weird? Voilà!
A À Á Â Ã Ä Å
u ù ú û ü  2
&lt;= >= != == === !==
&lt;- -> &lt;-> => &lt;=>
&lt;-- --> &lt;== ==> ~=</textarea><p class="tip">Both fonts are embedded for offline use. Common ligatures combine typed operators; Mono preserves their column count. The fine textures work best at larger sizes. Repeated characters retain their assigned designs.</p><p id="status" class="status" aria-live="polite"></p><h2>186 characters / 54 independently styled accented bodies</h2><section class="grid" id="grid">CARDS</section><footer>Install MixedCompany-Regular.ttf or MixedCompanyMono-Regular.ttf. Use precomposed accented letters; unsupported characters may display in a fallback font. Selected Latin coverage.</footer></main><script>
const tester=document.querySelector('#tester'),face=document.querySelector('#face'),size=document.querySelector('#size'),ink=document.querySelector('#ink'),grid=document.querySelector('#grid');
face.onchange=()=>{tester.style.fontFamily=face.value;tester.classList.toggle('mono',face.value==='MixedCompanyMono');grid.classList.toggle('mono',face.value==='MixedCompanyMono')};size.oninput=()=>{tester.style.fontSize=size.value+'px';document.querySelector('#sizeout').value=size.value+' px'};ink.oninput=()=>tester.style.color=ink.value;
const supported=new Set(CODEPOINTS);tester.oninput=()=>{const missing=[...new Set([...tester.value].filter(c=>!supported.has(c.codePointAt(0))&&!/\\s/.test(c)))];document.querySelector('#status').textContent=missing.length?'Outside this character set: '+missing.join(' '):''};tester.oninput();
</script></html>'''.replace('PROPFONT',encoded['MixedCompany']).replace('MONOFONT',encoded['MixedCompanyMono']).replace('CARDS',cards).replace('CODEPOINTS',json.dumps(sorted(info['cmap'])))
(ROOT/'outputs'/'MixedCompany-Try-It.html').write_text(page)
(ROOT/'work'/'font-tester.js').write_text(page.split('<script>')[1].split('</script>')[0])

# The comparison excludes accents, checking that the body really changed.
body_differences={}
for c in ACCENT:
    parent=unicodedata.normalize('NFD',c)[0]
    def unit(g):
        x1,y1,x2,y2=g.bounds
        return scale(translate(g,xoff=-x1,yoff=-y1),xfact=1/(x2-x1),yfact=1/(y2-y1),origin=(0,0))
    a,b=unit(BODIES[c]),unit(BODIES[parent]);overlap=a.intersection(b).area/a.union(b).area
    body_differences[c]={'parent':parent,'body_overlap':round(overlap,4),'style':LABELS[c]}
    assert overlap<.80,(c,parent,'accent body too close to parent',overlap)
report={'version':'3.002','families':[f[0] for f in FAMILIES],'encoded_characters':len(info['cmap']),'independent_accent_bodies':len(ACCENT),'styles':LABELS,'ligatures':LIGATURES,'accent_body_comparisons':body_differences}
(ROOT/'work'/'font-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps({'families':report['families'],'characters':report['encoded_characters'],'independent_accent_bodies':len(ACCENT),'maximum_accent_parent_body_overlap':max(d['body_overlap'] for d in body_differences.values())},indent=2))
