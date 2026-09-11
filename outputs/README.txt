MIXED COMPANY
Original display font · Version 1.0

A deliberately eclectic alphabet: rounded, serif, narrow, outlined,
stencil, engraved and handwritten treatments share a common scale.
Each base letter, number and symbol has its own prescribed treatment.
Repeated occurrences of a character keep the same design.
Accented letters inherit the treatment of their base letter.

QUICK START
On a Mac, double-click MixedCompany-Regular.ttf, then install it in
Font Book. Select "Mixed Company" from the font menu in your app.
If it does not appear immediately, reopen the app.
On Windows, right-click the TTF and choose Install.

Open MixedCompany-Try-It.html in a browser to try your own text.
It contains the font and works offline, without installation.
The size, letter spacing and ink colour are adjustable.

CONTENTS
MixedCompany-Regular.ttf      Installable desktop font
MixedCompany-Regular.woff2    Compressed font for web use
MixedCompany-Try-It.html      Offline, editable specimen
MixedCompany-Preview.png      Alphabet and sentence specimen
MixedCompany-All-Glyphs.png   Complete labelled character chart
Source/build_font.py          Editable construction source (in ZIP)

COVERAGE
179 encoded characters: all 95 printable ASCII characters, including
space; nonbreaking space; 54 common accented Latin letters; and 29
additional punctuation, currency, arithmetic and arrow symbols.
This is a selected Latin character set, not complete Unicode coverage.
The full chart shows every visible supported character. Use precomposed
accented letters (for example, é); combining accent sequences are not
implemented. The tester flags unsupported characters.

USE
Designed for titles, posters, invitations and short statements.
Start around 32 pt or larger so the fine outlines and cuts stay clear.
There is one Regular style; avoid synthetic bold or italic if you want
to preserve the individual character treatments.

CONSTRUCTION AND CHECKS
The letterforms are newly drawn vector paths, not assembled from
existing font files. The font includes 27 kerning pairs in OpenType
and legacy kerning tables. Desktop and web font character maps were
compared, table checksums and glyph bounds checked, and every visible
glyph rasterized. The preview images use the actual finished TTF.
The offline tester script passed a syntax check; in-browser testing
was unavailable because this environment blocks local-file navigation.

SOURCE
The ZIP includes the editable Python construction script. It requires
fonttools, shapely, brotli and Pillow. Run it from a Python environment
containing those packages. The font itself uses no source fonts; the
PNG specimen annotations use the macOS system Arial files referenced
near the bottom of the script. Adjust those paths on another platform.
