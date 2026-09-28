# SDLXLIFF

SDLXLIFF is the native bilingual file format used by SDL Trados Studio (now RWS Trados Studio). The extension stands for "SDL XLIFF" — it is Trados's own extension of the standard XLIFF (XML Localization Interchange File Format).

## Structure

An SDLXLIFF file is plain XML. Internally it keeps, for every segment:

- the source text
- the target text (empty until translated)
- confirmation status (Draft, Translated, Reviewed, Signed Off, etc.)
- the origin of any suggestion (TM match, machine translation, context match)
- tracked changes, if track changes is enabled
- comments left by translators or reviewers

Because it's XML, an SDLXLIFF file can be opened, inspected, or even edited programmatically, although in practice almost nobody hand-edits it — the risk of corrupting the internal tag structure is too high.

## Tags inside SDLXLIFF

Formatting (bold, italics, hyperlinks) and inline elements from the original source file are represented as protected tags. A translator should never delete or reorder these tags carelessly, because doing so can break the formatting or even break the software string when the file is reconverted back to its original format (e.g. .docx, .resx, .html).

## Why it matters for localization engineering

Localization engineers often need to:

- Pre-process source files before they reach translators (splitting, merging, filtering non-translatable segments)
- Post-process SDLXLIFF back into the original file format
- Write scripts that validate tag integrity across hundreds of SDLXLIFF files before delivery

Round-tripping is the general term for taking a file from its original format into a bilingual format like SDLXLIFF and back again without losing structure or formatting.
