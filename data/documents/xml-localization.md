# XML Localization

A large share of localizable content — software strings, help content, DITA documentation, DOCX/PPTX internals, XLIFF and SDLXLIFF bilingual files themselves — is stored as XML. Understanding XML structure is a core skill for localization engineers.

## Translatable vs non-translatable content

Not every piece of text inside an XML file should be translated. A localization engineer typically writes a filter or configuration file that tells the CAT tool:

- which elements contain translatable text
- which attributes are translatable (e.g. an `alt` attribute on an image, but not an `id` attribute)
- which elements should be skipped entirely (scripts, internal comments, configuration values)

Getting this filter wrong is a common source of two opposite problems: translators being shown text that should never have been translated (like internal keys), or translatable text being silently skipped and shipped untranslated.

## Common XML-based localization formats

- **XLIFF**: the general-purpose XML standard for exchanging translatable content between tools.
- **TMX**: XML format for exchanging translation memories.
- **SRX**: XML format for exchanging segmentation rules.
- **TBX**: XML format for exchanging termbases/glossaries.
- **RESX**: .NET's XML resource file format, commonly localized directly.

## Encoding and special characters

XML files must correctly declare their encoding (usually UTF-8) in the XML prolog. A wrong or missing encoding declaration is a frequent cause of "mojibake" — garbled characters — especially in languages using non-Latin scripts (Japanese, Korean, Russian, Arabic). Localization engineers often need to validate encoding before ingesting files into any pipeline.
