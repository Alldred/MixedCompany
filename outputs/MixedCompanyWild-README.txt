MIXED COMPANY WILD
Third edition · Version 3.000 · Proportional and monospaced

Two installable fonts share the same deliberately eccentric character
designs. The proportional font uses variable spacing and kerning; the
mono font gives every character a fixed 640-unit advance.

Gothic A, dripping-goo u, chalk 2, googly-eyed o, pixel M, brick b,
knitted 5, fingerprint 9, thorned R, and many other constructions make
this edition more varied than the earlier Mixed Company fonts.

All 54 accented letters have independently styled bodies. They are not
copies of their parent letters with an accent added. For example, the A
family includes mosaic, brush, ice, ripple, pipework and chain-link
designs. The family sheet shows parents in grey and accents in black.

INSTALL
Double-click either TTF on macOS and install it in Font Book. On Windows,
right-click the TTF and choose Install. The font menu names are:

  Mixed Company Wild
  Mixed Company Wild Mono

Both are Regular styles. Use larger sizes, preferably 36 pt or above,
to retain the finer textures and the details in the googly eyes.

TRY BOTH
Open MixedCompanyWild-Try-It.html in a browser. Both fonts are embedded
and the tester works offline. Switch between Proportional and Monospaced,
type your own text, and adjust size and ink colour.

CONTENTS
MixedCompanyWild/          Proportional TTF, WOFF2 and specimen
MixedCompanyWildMono/      Monospaced TTF, WOFF2 and specimen
MixedCompanyWild-Accent-Families.png
                          Every accented letter beside its parent
MixedCompanyWild-Character-Atlas.png
                          Complete labelled character and style chart
MixedCompanyWild-Spacing-Comparison.png
                          The same words in both spacing systems
MixedCompanyWild-Try-It.html
                          Offline tester for both fonts
Source/build_wild.py       Editable, self-contained vector font builder
Source/validate_wild.py    Font validation script
Validation/               Saved design and font validation reports

COVERAGE
Each font has 179 encoded characters: printable ASCII, nonbreaking
space, 54 precomposed accented letters, and 29 additional symbols.
This is selected Latin coverage, not all Unicode. Use precomposed
accented characters, for example é. Repeated characters retain their
assigned design. Every visible character in the chart is drawn in the
font; unsupported characters may use a fallback font in your application.

VALIDATION
Both fonts passed checksum, table-compilation, coverage, glyph-bound
and rendering checks. Every visible character was rasterized at 48 and
128 pixels. All mono advances equal 640; the proportional font has 136
distinct advances. At a 100-pixel font size, four supported characters
always measure 256 pixels in the mono version, including spaces and
punctuation. The accent-body comparison excludes the diacritic itself;
each accented body differs from its parent. The sheets were also viewed
to check appearance. The original two editions retain their earlier
character designs and accent behavior.

The tester JavaScript passed a syntax check. Its browser interaction
was not verified because the available browser blocks local-file URLs.

BUILD
The scripts use Python 3.12 with fonttools 4.65.0, shapely 2.1.2,
brotli 1.2.0 and Pillow 12.3.0. The font outlines are original vector
drawings. The preview annotations use macOS Arial files; adjust their
paths when rebuilding on another platform. The finished fonts do not
depend on those annotation fonts.

Run the builder from the repository's src folder (or Source in this
package); it creates outputs and work folders alongside that folder.
The validator compares coverage with the original MixedCompany-Regular.ttf,
which is available in the repository. Release ZIPs and saved validation
snapshots are packaged separately after building and checking the fonts.
