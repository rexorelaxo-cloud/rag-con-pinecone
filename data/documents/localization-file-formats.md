# Localization File Formats

Localization engineers work with a wide range of file formats, each requiring different handling. This document gives a quick overview of the most common ones, complementing the more detailed documents on SDLXLIFF, XML, and terminology formats.

## Bilingual/interchange formats

- **XLIFF** (`.xliff`, `.xlf`): the general XML-based standard for exchanging translatable content between tools, defined by OASIS.
- **SDLXLIFF** (`.sdlxliff`): Trados Studio's proprietary extension of XLIFF, covered in detail in its own document.
- **TMX** (`.tmx`): XML format for exchanging Translation Memories.
- **TBX** (`.tbx`): XML format for exchanging termbases.
- **SRX** (`.srx`): XML format for exchanging segmentation rules.

## Software/resource formats

- **RESX** (`.resx`): .NET resource files, XML-based, common in Windows applications.
- **PO/POT** (`.po`, `.pot`): Gettext translation files, widely used in open-source and Linux/Python software.
- **JSON**: increasingly common for web and mobile app strings (e.g. React, iOS/Android build tooling that consumes JSON string tables).
- **strings/stringsdict** (`.strings`): Apple's iOS/macOS string resource format.
- **ARB** (`.arb`): Application Resource Bundle, used by Flutter apps.

## Document/DTP formats

- **DOCX, PPTX, XLSX**: Microsoft Office Open XML formats — technically ZIP archives containing XML internally, which is why CAT tools can filter and extract translatable text from them directly.
- **IDML**: Adobe InDesign's XML-based interchange format, used so InDesign files can be translated without needing InDesign itself installed.
- **PDF**: generally not editable for translation directly; PDFs are usually translated from their original source format (InDesign, Word) when available, or reconstructed if the source is lost.

## Choosing the right filter

Every CAT tool ships with built-in filters for the most common formats, but localization engineers frequently need to write or customize a filter (often XML- or XPath-based, see the XPath document) for a client's proprietary or unusual file format, deciding exactly which elements or attributes are translatable.
