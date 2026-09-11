"""Check the proportional and fixed-width MixedCompany fonts after building them."""
from pathlib import Path
import sys, json, unicodedata, subprocess, shutil
sys.path.insert(0,str(Path(__file__).parent/'deps'))
from fontTools.ttLib import TTFont
from fontTools.ttLib.sfnt import calcChecksum
from PIL import ImageFont

ROOT=Path(__file__).resolve().parent.parent
reports={}
reference=set(['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '¡', '¢', '£', '¥', '©', '®', '°', '±', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '×', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'à', 'á', 'â', 'ã', 'ä', 'å', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷', 'ù', 'ú', 'û', 'ü', 'ý', 'ÿ', 'Ÿ', '–', '—', '‘', '’', '“', '”', '•', '…', '€', '™', '←', '↑', '→', '↓', '−', '≠', '≤', '≥'])
reference={ord(c) for c in reference}|{32,160}|{ord(c) for c in '↔⇐⇒⇔≡≢≈'}
design=json.loads((ROOT/'work'/'font-report.json').read_text())
assert len(design['accent_body_comparisons'])==54
assert max(item['body_overlap'] for item in design['accent_body_comparisons'].values())<.80
for stem,mono in [('MixedCompany',False),('MixedCompanyMono',True)]:
    path=ROOT/'outputs'/stem/(stem+'-Regular.ttf')
    ttf=TTFont(path,checkChecksums=2)
    woff=TTFont(path.with_suffix('.woff2'))
    cmap=ttf.getBestCmap()
    assert set(cmap)==set(reference)==set(woff.getBestCmap())
    assert len(cmap)==186
    assert calcChecksum(path.read_bytes())==0xB1B0AFBA
    assert ttf['post'].isFixedPitch==int(mono)
    family='MixedCompany Mono' if mono else 'MixedCompany'
    assert ttf['name'].getDebugName(1)==family
    assert woff['name'].getDebugName(1)==family
    assert woff['hmtx'].metrics==ttf['hmtx'].metrics
    widths={a for a,lsb in ttf['hmtx'].metrics.values()}
    if mono:
        assert {ttf['hmtx'][name][0] for name in set(cmap.values())|{'.notdef'}}=={640}
        assert not any(table in ttf for table in ['kern','GPOS'])
    else:
        assert len(widths)>20
        assert 'GPOS' in ttf and 'kern' in ttf
    assert 'GSUB' in ttf and 'GSUB' in woff
    assert ttf['GSUB'].compile(ttf)==woff['GSUB'].compile(woff)
    hb=shutil.which('hb-shape')
    assert hb, 'Install HarfBuzz CLI tools to check real ligature shaping.'
    def shape(text,enabled=True):
        return json.loads(subprocess.check_output([hb,str(path),'--text='+text,'--output-format=json',
            '--features=liga='+('1' if enabled else '0')],text=True))
    shaped={}
    for sequence in design['ligatures']:
        expected='lig_'+'_'.join(f'{ord(c):04X}' for c in sequence)
        result=shape(sequence);plain=shape(sequence,False)
        assert len(result)==1 and result[0]['g']==expected,(sequence,result)
        assert len(plain)==len(sequence),(sequence,plain)
        advance=sum(ttf['hmtx'][cmap[ord(c)]][0] for c in sequence)
        assert result[0]['ax']==sum(g['ax'] for g in plain)==advance
        assert shape('a'+sequence+'b')[1]['g']==expected
        g=ttf['glyf'][expected]
        assert g.numberOfContours>0 and 0<=g.xMin<g.xMax<=advance
        assert -380<=g.yMin<g.yMax<=1040
        if mono:assert advance==640*len(sequence)
        shaped[sequence]={'glyph':expected,'advance':advance}
    assert all(not g['g'].startswith('lig_') for g in shape('< = - > ! ='))
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
    reports[stem]={'characters':len(cmap),'unique_advance_widths':len(widths),'fixed_pitch':mono,'ligature_shaping':shaped,
        'every_glyph_rasterized_at_px':[48,128],'four_character_widths_at_100px':samples,
        'bounds_y':[min(b[0] for b in bounds),max(b[1] for b in bounds)],'checksum_valid':True}
report={'fonts':reports,'independent_accent_bodies':54,
    'maximum_normalized_accent_parent_body_overlap':max(item['body_overlap'] for item in design['accent_body_comparisons'].values()),
    'eyes_character':'o'}
(ROOT/'work'/'font-validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps(report,indent=2,ensure_ascii=False))
