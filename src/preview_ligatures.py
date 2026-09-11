"""Render a labelled proof using HarfBuzz's actual OpenType shaping."""
from pathlib import Path
import json, subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent.parent
sequences=list(json.loads((ROOT/'work/font-report.json').read_text())['ligatures'])
ui='/System/Library/Fonts/Supplemental/Arial.ttf'
for stem,title in [('MixedCompany','MixedCompany / standard'),('MixedCompanyMono','MixedCompany Mono')]:
    canvas=Image.new('RGB',(1680,1160),'#f5f0e4');draw=ImageDraw.Draw(canvas)
    draw.text((60,40),title+' / programming ligatures',font=ImageFont.truetype(ui,38),fill='#252621')
    draw.text((60,103),'Typed sequence above; shaped result below. Ligatures can be disabled in your app.',font=ImageFont.truetype(ui,23),fill='#78786b')
    for i,sequence in enumerate(sequences):
        x=60+(i%4)*400;y=180+(i//4)*230
        draw.rectangle((x,y,x+385,y+210),outline='#c9c1b2',width=2)
        draw.text((x+20,y+15),sequence,font=ImageFont.truetype(ui,27),fill='#d33b31')
        out=ROOT/'work'/('ligature-'+stem+'-'+str(i)+'.png')
        subprocess.run(['hb-view',str(ROOT/'outputs'/stem/(stem+'-Regular.ttf')), '--text='+sequence,
            '--font-size=110','--background=f5f0e4','--foreground=252621','--margin=0',
            '--output-file='+str(out)],check=True)
        with Image.open(out) as rendered:
            assert rendered.width<=365 and rendered.height<=160
            canvas.paste(rendered.convert('RGB'),(x+(385-rendered.width)//2,y+45))
    canvas.save(ROOT/'outputs'/stem/(stem+'-Ligatures.png'))
