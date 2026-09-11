"""Render all audited character groups in both fonts at 40 and 76 px."""
from pathlib import Path
import json,subprocess,math
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent
groups=json.loads((ROOT/'work/contrast-audit.json').read_text())['groups']
ui=lambda size:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',size)
for page in range(math.ceil(len(groups)/9)):
    rows=groups[page*9:(page+1)*9]
    im=Image.new('RGB',(1600,155+len(rows)*185),'#f5f0e4');d=ImageDraw.Draw(im)
    d.text((45,30),'MixedCompany / contrast audit / '+str(page+1),font=ui(32),fill='#252621')
    d.text((245,91),'STANDARD / 76 px and 40 px',font=ui(18),fill='#78786b')
    d.text((930,91),'MONO / 76 px and 40 px',font=ui(18),fill='#78786b')
    for row,(title,chars) in enumerate(rows):
        y=145+row*185
        d.text((45,y+24),title,font=ui(20),fill='#d33b31')
        for col,stem in enumerate(['MixedCompany','MixedCompanyMono']):
            x=245+col*685
            for size,dy in [(76,0),(40,108)]:
                png=ROOT/'work'/f'pair-{page}-{row}-{col}-{size}.png'
                subprocess.run(['hb-view',str(ROOT/'outputs'/stem/(stem+'-Regular.ttf')),
                    '--text='+' '.join(chars),'--features=liga=0','--font-size='+str(size),
                    '--background=f5f0e4','--foreground=252621','--margin=0','--output-file='+str(png)],check=True)
                with Image.open(png) as glyphs:
                    assert glyphs.width<=640
                    im.paste(glyphs.convert('RGB'),(x,y+dy))
        d.line((45,y+177,1555,y+177),fill='#c9c1b2',width=1)
    im.save(ROOT/'outputs'/f'MixedCompany-Contrast-{page+1}.png')
