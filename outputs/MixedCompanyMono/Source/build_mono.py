"""Mixed Company Mono 2.0: varied original letterforms in fixed-width cells.
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

FAMILY='Mixed Company Mono'
STEM='MixedCompanyMono'
OUT=ROOT/'outputs'/STEM
OUT.mkdir(exist_ok=True)
shapes={};metrics={};glyphs={};cmap={};labels={}
missing=box(85,0,555,710).difference(box(125,40,515,670))
glyphs['.notdef']=as_glyph(missing);metrics['.notdef']=(CELL,85)
glyphs['space']=TTGlyphPen(None).glyph();metrics['space']=(CELL,0);cmap[32]='space';cmap[160]='space'
for c in G:
    geom,adv=make_geometry(c);name='uni%04X'%ord(c)
    shapes[c]=geom;glyphs[name]=as_glyph(geom);metrics[name]=(CELL,round(geom.bounds[0]));cmap[ord(c)]=name;labels[c]=DESIGNS[c][-1]

# Preserve the original accent coverage, fitting accents within the same cell.
import unicodedata
accents={'\u0301':[path('M-65 0 L75 120')],'\u0300':[path('M-75 120 L65 0')],
'\u0302':[path('M-130 0 L0 125 L130 0')],'\u0303':[path('M-140 30 C-60 150 65 -80 145 50')],
'\u0308':[[(-100,65)],[(100,65)]],'\u030a':[oval(0,65,72,65)],'\u0327':[path('M10 0 L-35 -70 C140 -55 100 -205 -45 -160')]}
for cp in list(range(0xC0,0x100))+[0x178]:
    c=chr(cp);dec=unicodedata.normalize('NFD',c)
    if len(dec)!=2 or dec[0] not in shapes or dec[1] not in accents:continue
    base,mark=dec;geom=shapes[base]
    if base=='i':geom=geom.intersection(box(0,-300,CELL,525))
    x1,y1,x2,y2=geom.bounds
    accent=unary_union([stroke(p,43,'round') for p in accents[mark]])
    yy=-8 if mark=='\u0327' else y2+82
    accent=translate(accent,xoff=(x1+x2)/2,yoff=yy)
    geom=unary_union([geom,accent]);name='uni%04X'%cp
    glyphs[name]=as_glyph(geom);metrics[name]=(CELL,round(geom.bounds[0]));cmap[cp]=name;shapes[c]=geom;labels[c]=labels[base]+' with accent'

fb=FontBuilder(1000,isTTF=True);fb.setupGlyphOrder(list(glyphs));fb.setupCharacterMap(cmap);fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics(metrics);fb.setupHorizontalHeader(ascent=1000,descent=-320,lineGap=0)
fb.setupNameTable({'familyName':FAMILY,'styleName':'Regular','uniqueFontIdentifier':'Mixed Company Mono 2.000 Original 2026',
'fullName':FAMILY+' Regular','psName':STEM+'-Regular','version':'Version 2.000',
'copyright':'Original vector design created for Stuart Alldred, 2026.',
'description':'Distinct character constructions in a genuine fixed-pitch display font. All glyph advances are 640 units; no kerning or ligatures.'})
fb.setupOS2(sTypoAscender=1000,sTypoDescender=-320,sTypoLineGap=0,usWinAscent=1000,usWinDescent=320,
sxHeight=520,sCapHeight=710,usWeightClass=400,usWidthClass=5,fsType=0,fsSelection=0x40,xAvgCharWidth=CELL)
fb.font['OS/2'].panose.bFamilyType=2;fb.font['OS/2'].panose.bProportion=9
fb.setupPost(isFixedPitch=1);fb.setupMaxp();fb.font['head'].fontRevision=2
fontpath=OUT/(STEM+'-Regular.ttf');fb.save(fontpath)
wf=TTFont(fontpath);wf.flavor='woff2';wf.save(OUT/(STEM+'-Regular.woff2'))

# Actual-font specimen, plus a column alignment proof.
PAPER='#f5f0e5';INK='#252622';ACCENT='#c94b31';LINE='#c8c2b4';MUTED='#6d7066'
ui='/System/Library/Fonts/Supplemental/Arial.ttf';uib='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def font(n,display=False,bold=False):return ImageFont.truetype(str(fontpath) if display else (uib if bold else ui),n)
im=Image.new('RGB',(1800,2300),PAPER);d=ImageDraw.Draw(im)
def txt(x,y,s,size=28,display=False,color=INK,bold=False):d.text((x,y),s,font=font(size,display,bold),fill=color,anchor='lt')
def rule(y):d.line((84,y,1716,y),fill=LINE,width=2)
txt(84,62,'MIXED COMPANY / MONO',25,bold=True);txt(1310,62,'SECOND EDITION',25)
rule(111)
txt(84,165,'Mixed Company',180,True)
txt(84,360,'More character. Equal space.',39,bold=True)
txt(84,426,'New letter constructions · 179 characters · One fixed width',27,color=MUTED)
rule(494)
txt(84,530,'01 / CAPITALS',23,color=ACCENT,bold=True)
for row,s in enumerate(['ABCDEFGHIJKLM','NOPQRSTUVWXYZ']):txt(84,590+176*row,s,178,True)
rule(950)
txt(84,990,'02 / LOWERCASE',23,color=ACCENT,bold=True)
for row,s in enumerate(['abcdefghijklm','nopqrstuvwxyz']):txt(84,1050+181*row,s,176,True)
rule(1425)
txt(84,1464,'03 / NUMBERS & PUNCTUATION',23,color=ACCENT,bold=True)
txt(84,1530,'0123456789!?&',168,True)
txt(84,1705,'£€$%+−×÷=@#*',133,True)
rule(1884)
txt(84,1922,'04 / EVERY COLUMN ALIGNS',23,color=ACCENT,bold=True)
rows=['WIDE  IIII  0000','thin  llll  1111','mix!  ....  £€$%']
size=102;cw=size*CELL/1000;start=84
for j in range(len(rows[0])+1):
    d.line((start+j*cw,1987,start+j*cw,2260),fill='#dfd9cd',width=1)
for n,s in enumerate(rows):d.text((start,2058+n*87),s,font=font(size,True),fill=INK,anchor='ls')
im.save(OUT/(STEM+'-Preview.png'))

chars=[chr(cp) for cp in sorted(cmap) if cp not in (32,160)]
cols=12;cw=143;ch=167
proof=Image.new('RGB',(cols*cw+100,math.ceil(len(chars)/cols)*ch+180),PAPER);p=ImageDraw.Draw(proof)
p.text((50,32),FAMILY+' / full character set',font=font(32,bold=True),fill=INK)
for i,c in enumerate(chars):
    x=50+(i%cols)*cw;y=115+(i//cols)*ch
    p.rectangle((x,y,x+cw,y+ch),outline=LINE)
    p.text((x+(cw-91*CELL/1000)/2,y+103),c,font=font(91,True),anchor='ls',fill=INK)
    p.text((x+9,y+136),f'{c}   U+{ord(c):04X}',font=font(15),fill=MUTED)
proof.save(OUT/(STEM+'-All-Glyphs.png'))

# Paired specimens make the increase in visual variety reviewable.
oldpath=ROOT/'outputs'/'MixedCompany-Regular.ttf'
if oldpath.exists():
    comp=Image.new('RGB',(1800,2060),PAPER);p=ImageDraw.Draw(comp)
    p.text((84,45),'THE ORIGINAL → THE NEW MONO EDITION',font=font(28,bold=True),fill=INK)
    examples=['ABCDEFGHIJKLM','NOPQRSTUVWXYZ','abcdefghijklm','nopqrstuvwxyz','0123456789']
    for i,s in enumerate(examples):
        y=133+i*371
        p.text((84,y),'ORIGINAL',font=font(18,bold=True),fill=MUTED)
        p.text((84,y+36),s,font=ImageFont.truetype(str(oldpath),123),fill='#96958c',anchor='lt')
        p.text((84,y+170),'NEW MONO',font=font(18,bold=True),fill=ACCENT)
        p.text((84,y+205),s,font=font(150,True),fill=INK,anchor='lt')
        p.line((84,y+350,1716,y+350),fill=LINE)
    comp.save(OUT/(STEM+'-Before-After.png'))

# An offline tester; it embeds the actual WOFF2 and uses a fixed-width grid.
encoded=base64.b64encode((OUT/(STEM+'-Regular.woff2')).read_bytes()).decode()
cells=''.join('<div class="cell"><span>'+html.escape(c)+'</span><small>'+html.escape(c)+' · '+f'{ord(c):04X}'+'</small></div>' for c in chars)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mixed Company Mono — try it</title><style>
@font-face{font-family:MixedMono;src:url(data:font/woff2;base64,FONTDATA) format('woff2');font-display:swap}*{box-sizing:border-box}body{margin:0;background:#f5f0e5;color:#252622;font:16px system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:34px 28px}header{display:flex;justify-content:space-between;gap:20px;padding-bottom:22px;border-bottom:1px solid #c8c2b4;font-size:13px;letter-spacing:.07em}h1{font:clamp(36px,6.1vw,84px)/1.4 MixedMono;margin:40px 0 14px}p{max-width:840px;line-height:1.6}nav{display:flex;flex-wrap:wrap;gap:25px;align-items:center;padding:22px 0;margin-top:32px;border-top:1px solid #c8c2b4}label{display:inline-flex;align-items:center;gap:10px;font-size:14px}input{accent-color:#c94b31}textarea{font:72px/1.38 MixedMono;--cell:46.08px;font-kerning:none;font-variant-ligatures:none;letter-spacing:0;tab-size:4;width:100%;height:430px;border:1px solid #c8c2b4;padding:20px;resize:vertical;background-color:transparent;color:inherit;outline-color:#c94b31;font-synthesis:none}textarea.guides{background-image:repeating-linear-gradient(to right,transparent 0,transparent calc(var(--cell) - 1px),#dcd6cb calc(var(--cell) - 1px),#dcd6cb var(--cell));background-origin:content-box;background-clip:content-box}.tip{font-size:13px;color:#666a60}.status{min-height:24px;color:#b3462e;font-size:14px}h2{font-size:14px;letter-spacing:.09em;text-transform:uppercase;margin:40px 0 20px;color:#c94b31}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));border-left:1px solid #c8c2b4;border-top:1px solid #c8c2b4}.cell{min-height:128px;display:flex;flex-direction:column;align-items:center;justify-content:center;border-right:1px solid #c8c2b4;border-bottom:1px solid #c8c2b4}.cell span{font:66px/1.35 MixedMono}.cell small{font-size:11px;color:#6d7066;margin:5px 0 12px}footer{font-size:13px;color:#6d7066;border-top:1px solid #c8c2b4;margin-top:40px;padding-top:18px}
</style><main><header><strong>MIXED COMPANY / MONO</strong><span>SECOND EDITION · FIXED PITCH</span></header><h1>Mixed Company</h1><p>More distinct character constructions, with one shared width. Pixel steps, brush strokes, dots, loops, diamond bowls, fine serifs and engraved strokes each bring a different personality.</p><nav><label>Size <input id="size" type="range" min="24" max="140" value="72"><output id="sizeout">72 px</output></label><label><input id="guides" type="checkbox" checked> Show character columns</label><label>Ink <input id="color" type="color" value="#252622"></label></nav><textarea id="tester" class="guides" aria-label="Try Mixed Company Mono" spellcheck="false">Every letter has a story.
WIDE  IIII  0000
thin  llll  1111
mix!  ....  £€$%</textarea><p class="tip">Every supported character, including spaces and punctuation, occupies exactly one column. Repeated letters retain their design. Best at larger sizes. The font is embedded, so this page works offline.</p><p id="status" class="status" aria-live="polite"></p><h2>179 characters / complete coverage</h2><section class="grid">CELLS</section><footer>Install MixedCompanyMono-Regular.ttf and select Mixed Company Mono. Accented characters follow their base letter. This is a display font with a selected Latin character set; it is not a full programming-symbol font.</footer></main><script>
const tester=document.querySelector('#tester'),size=document.querySelector('#size'),guides=document.querySelector('#guides'),color=document.querySelector('#color');
size.oninput=()=>{tester.style.fontSize=size.value+'px';tester.style.setProperty('--cell',Number(size.value)*.64+'px');document.querySelector('#sizeout').value=size.value+' px'};
guides.onchange=()=>tester.classList.toggle('guides',guides.checked);color.oninput=()=>tester.style.color=color.value;
const supported=new Set(CODEPOINTS);tester.oninput=()=>{const missing=[...new Set([...tester.value].filter(c=>!supported.has(c.codePointAt(0))&&!/\\s/.test(c)))];document.querySelector('#status').textContent=missing.length?'Unsupported characters use a fallback and may not align: '+missing.join(' '):''};tester.oninput();
</script></html>'''.replace('FONTDATA',encoded).replace('CELLS',cells).replace('CODEPOINTS',json.dumps(sorted(cmap)))
(OUT/(STEM+'-Try-It.html')).write_text(page)
(ROOT/'work'/'mono-tester.js').write_text(page.split('<script>')[1].split('</script>')[0])
report={'family':FAMILY,'version':2,'encoded_characters':len(cmap),'advance_width':CELL,'units_per_em':1000,'base_designs':len(DESIGNS),'styles':labels}
(ROOT/'work'/'mono-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps({k:v for k,v in report.items() if k!='styles'},indent=2))
