# Contrast review — 3.004

Reviewed 31 related-character groups and all 26 uppercase/lowercase pairs. Compared shapes in standard and mono at 76 and 40 px, and ligatures at 110 and 40 px.

The earlier ligatures reused stretched Unicode symbols. All 16 now have independently assigned drawings and styles, including distinct short/long arrows. An automated normalized-outline comparison includes mirrored and rotated shapes and rejects near-copied ligatures.

Visual review prompted a second pass on dashes, backslash and underscore. Fine texture remains most legible at larger display sizes; the smaller proofs check silhouette and weight contrast.

## Changed characters

| Character | Previous treatment | New treatment |
| --- | --- | --- |
| U+0050 P | pinstripe stem | Crowned capital P |
| U+0054 T | western forks | Carved stone T |
| U+0058 X | woven strokes | Half-solid capital X |
| U+005A Z | racing rules | Zipped capital Z |
| U+0063 c | diamond terminals | Buttoned lowercase c |
| U+0076 v | notched wedge | Lace-collar v |
| U+0077 w | connected double cup | Inflated lowercase w |
| U+0022 " | parallel square quotes | Mismatched flag quotes |
| U+0028 ( | fine parenthesis | Broad ink parenthesis |
| U+0029 ) | contrast parenthesis | Pearl-bead parenthesis |
| U+003C < | square left angle | Arcade stair-step angle |
| U+003E > | round right angle | Sweeping brush angle |
| U+005C \ | solid backslash | Striped ribbon backslash |
| U+005D ] | serif right bracket | Pixel gate bracket |
| U+005F _ | inlaid underscore | Saw-edge underscore |
| U+007B { | Feather brace | Scrolled iron brace |
| U+007D } | Coral brace | Thorny hedge brace |
| U+00D7 × | woven multiplication | Chain-link multiplication |
| U+2212 − | hairline minus | Terminal-ring minus |
| U+2026 … | square ellipsis | Three open-ring stops |
| U+2013 – | square en dash | Knuckled en dash |
| U+2014 — | round em dash | Chain-link em dash |
| U+2018 ‘ | angular opening quote | Curlicue opening quote |
| U+2019 ’ | soft closing quote | Pixel-chip closing quote |
| U+201C “ | fine opening double quote | Striped pennant quotes |
| U+201D ” | heavy closing double quote | Hollow loop quotes |
| U+2264 ≤ | soft less-or-equal | Electronic less-or-equal |
| U+2265 ≥ | light greater-or-equal | Candy-stripe greater-or-equal |
| U+2260 ≠ | contrasted unequal | Half-filled unequal |
| U+00A1 ¡ | square inverted exclamation | Chain inverted exclamation |
| U+00BF ¿ | rounded inverted question | Plumbed inverted question |
| U+2194 ↔ | Double-headed spear | Sawtooth bridge arrow |
| U+21D0 ⇐ | Twin-rail left arrow | Slotted double left arrow |
| U+21D2 ⇒ | Twin-rail right arrow | Half-solid double right arrow |
| U+21D4 ⇔ | Twin-rail bidirectional arrow | Button-thread double bridge |
| U+2261 ≡ | Triple-bar identity | Three hollow rails |
| U+2262 ≢ | Slashed identity | Chrome identity slash |
| U+2248 ≈ | Ribbon approximation | Striped wave ribbons |

## Ligatures

| Sequence | Treatment |
| --- | --- |
| &lt;= | Fractured stone comparison |
| >= | Pearl comparison |
| != | Stencil slash |
| == | Stitched leather straps |
| === | Three rippling ribbons |
| !== | Barbed identity |
| &lt;- | Quill arrow |
| -> | Arcade rocket |
| &lt;-> | Chain-link bridge |
| => | Blackletter double arrow |
| &lt;=> | Hollow neon bridge |
| &lt;-- | Melting arrow |
| --> | Ink comet |
| &lt;== | Brickwork double arrow |
| ==> | Skeleton double arrow |
| ~= | Pencil-wave approximation |

## Validation

Both fonts passed character coverage, checksums, glyph bounds, table compilation and rasterization checks. HarfBuzz verified each ligature, adjacent text, longest matches, disabled substitutions and preserved advances. Mono remains 640 units per input character; two/three-character ligatures retain 1280/1920 units. TTF and WOFF2 substitutions match. All 54 accented bodies retain independently styled geometry.

The body-overlap data in contrast-audit.json is a geometric aid, not a perceptual score.
