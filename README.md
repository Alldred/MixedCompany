# MixedCompany

For Will ❤️

A display typeface. Every letter is its own drawing, including the accented ones.

Two fonts: **MixedCompany** (proportional) and **MixedCompany Mono** (fixed width).

[Try it](https://alldred.github.io/MixedCompany/)

![MixedCompany](outputs/MixedCompany/MixedCompany-Preview.png)

## Download

| | TTF | WOFF2 |
| --- | --- | --- |
| MixedCompany | [Regular](outputs/MixedCompany/MixedCompany-Regular.ttf) | [Regular](outputs/MixedCompany/MixedCompany-Regular.woff2) |
| MixedCompany Mono | [Regular](outputs/MixedCompanyMono/MixedCompanyMono-Regular.ttf) | [Regular](outputs/MixedCompanyMono/MixedCompanyMono-Regular.woff2) |

[All files](outputs/MixedCompany-Package.zip)

[Character set](outputs/MixedCompany-Character-Atlas.png) · [Accents](outputs/MixedCompany-Accent-Families.png) · [Proportional vs mono](outputs/MixedCompany-Spacing-Comparison.png)

## Ligatures

With standard ligatures on:

```
<=  >=  !=  ==  ===  !==
<-  ->  <->  =>  <=>
<--  -->  <==  ==>  ~=
```

Also in the font: ≤ ≥ ≠ ← → ↔ ⇐ ⇒ ⇔ ≡ ≢ ≈

[Proportional](outputs/MixedCompany/MixedCompany-Ligatures.png) · [Mono](outputs/MixedCompanyMono/MixedCompanyMono-Ligatures.png)

186 characters. Display sizes. No combining marks.

## Source

```sh
uv sync
uv run python src/build_fonts.py
```

Python 3.12+. Drawings are in `src/build_fonts.py`.
