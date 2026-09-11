MIXED COMPANY MONO
Second edition · Version 2.000

A more varied, genuinely monospaced version of Mixed Company.

WHAT CHANGED
The character designs now differ in construction as well as weight and
decoration: a stepped M, engraved E, dotted S, dimensional L, Tuscan I,
perforated b, double-storey g, looped l, faceted o, studded x, and diamond 8.
The before-and-after sheet compares the original with this new edition.

Every glyph uses exactly 640 units of advance width in a 1000-unit em.
Letters, digits, punctuation, symbols, ordinary spaces and nonbreaking
spaces all occupy one cell. Wide letters were fitted to that cell;
narrow characters were centred without stretching. Kerning and
ligatures are absent, so they cannot alter the column alignment.

INSTALL
Mac: double-click MixedCompanyMono-Regular.ttf and install in Font Book.
Windows: right-click the TTF and select Install.
Choose "Mixed Company Mono" from your application's font menu.
Reopen the application if the new font is not immediately listed.

TRY IT
Open MixedCompanyMono-Try-It.html in your browser. The font is embedded,
so no installation or internet connection is needed. Type your own text,
change its size or ink colour, and toggle the character-column guides.
Unsupported characters are flagged and may use a different-width fallback.

FILES
MixedCompanyMono-Regular.ttf       Installable font
MixedCompanyMono-Regular.woff2     Web font
MixedCompanyMono-Preview.png       Full-size specimen and alignment proof
MixedCompanyMono-Before-After.png  Comparison with the original
MixedCompanyMono-All-Glyphs.png    Complete labelled character chart
MixedCompanyMono-Try-It.html       Offline text tester
Source/build_mono.py              Editable vector construction source

COVERAGE AND USE
179 encoded characters: printable ASCII, common Latin accents, selected
currency signs, punctuation, mathematical symbols and arrows. The chart
shows the full visible set. Accented letters inherit their base character's
treatment; use precomposed accents such as é. This is not full Unicode
coverage. Repeated occurrences of a letter retain the same design.

This remains a display font: use it for headings, posters, invitations and
short statements, preferably at 32 pt or larger. At very small sizes the
fine rules, perforations and dots lose definition. Apply the Regular
style without synthetic bold or italic to preserve the intended shapes.

VALIDATION
All desktop and web glyph advances equal 640. Fixed-pitch metadata is set,
the original character coverage is preserved, and no kerning or substitution
tables are present. Every visible glyph was rendered at 32 and 96 pixels.
Checksums, font table compilation and glyph bounds passed. At 100 pixels,
iiii, WWWW, ...., four spaces, 0000, 1111, AVTo, £€$% and Àéñü each measured
256 pixels. The actual TTF was used for all specimen images.
The tester script passed a syntax check. Browser interaction was not
verified because the available browser blocks local-file navigation.

SOURCE
The font uses original vector drawings, with no borrowed font outlines.
The build script requires Python, fonttools, shapely, brotli and Pillow.
It uses macOS Arial files for specimen annotations; edit those annotation
font paths when building on another platform. The installable font works
independently of those annotation fonts.
