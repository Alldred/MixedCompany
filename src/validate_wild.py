"""Check the proportional and fixed-width Wild fonts after building them."""
from pathlib import Path
import sys, json, unicodedata
sys.path.insert(0,str(Path(__file__).parent/'deps'))
from fontTools.ttLib import TTFont
from fontTools.ttLib.sfnt import calcChecksum
from PIL import ImageFont

ROOT=Path(__file__).resolve().parent.parent
reports={}
reference=TTFont(ROOT/'outputs'/'MixedCompany-Regular.ttf').getBestCmap()
design=json.loads((ROOT/'work'/'wild-report.json').read_text())
assert len(design['accent_body_comparisons'])==54
assert max(item['body_overlap'] for item in design['accent_body_comparisons'].values())<.80
for stem,mono in [('MixedCompanyWild',False),('MixedCompanyWildMono',True)]:
    path=ROOT/'outputs'/stem/(stem+'-Regular.ttf')
    ttf=TTFont(path,checkChecksums=2)
    woff=TTFont(path.with_suffix('.woff2'))
    cmap=ttf.getBestCmap()
    assert set(cmap)==set(reference)==set(woff.getBestCmap())
    assert len(cmap)==179
    assert calcChecksum(path.read_bytes())==0xB1B0AFBA
    assert ttf['post'].isFixedPitch==int(mono)
    assert woff['hmtx'].metrics==ttf['hmtx'].metrics
    widths={a for a,lsb in ttf['hmtx'].metrics.values()}
    if mono:
        assert widths=={640}
        assert not any(table in ttf for table in ['kern','GPOS','GSUB'])
    else:
        assert len(widths)>20
        assert 'GPOS' in ttf and 'kern' in ttf
    fonts={s:ImageFont.truetype(str(path),s) for s in [48,128]}
    bounds=[]
    for cp,name in cmap.items():
        if cp in (32,160):continue
        g=ttf['glyf'][name];a,lsb=ttf['hmtx'][name]
        assert g.numberOfContours>0
        assert not g.isComposite(),chr(cp)
        assert 0<=g.xMin==lsb<g.xMax<=a,(stem,cp,g.xMin,g.xMax,a)
        assert -380<=g.yMin<g.yMax<=1040,(stem,cp,g.yMin,g.yMax)
        bounds.append((g.yMin,g.yMax))
        for f in fonts.values():assert f.getmask(chr(cp)).getbbox() is not None,(stem,cp)
    for table in ttf.keys():
        if table!='GlyphOrder':ttf[table].compile(ttf)
    f=ImageFont.truetype(str(path),100)
    samples={s:f.getlength(s) for s in ['iiii','WWWW','....','    ','0000','AVTo','£€$%','Àéñü']}
    if mono:assert set(samples.values())=={256.0},samples
    else:assert len(set(samples.values()))>3,samples
    reports[stem]={'characters':len(cmap),'unique_advance_widths':len(widths),'fixed_pitch':mono,
        'every_glyph_rasterized_at_px':[48,128],'four_character_widths_at_100px':samples,
        'bounds_y':[min(b[0] for b in bounds),max(b[1] for b in bounds)],'checksum_valid':True}
report={'fonts':reports,'independent_accent_bodies':54,
    'maximum_normalized_accent_parent_body_overlap':max(item['body_overlap'] for item in design['accent_body_comparisons'].values()),
    'eyes_character':'o'}
(ROOT/'work'/'wild-validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps(report,indent=2,ensure_ascii=False))
