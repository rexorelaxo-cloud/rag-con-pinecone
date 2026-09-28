# Trados Studio

Trados Studio (formerly SDL Trados Studio, now published by RWS) is one of the most widely used CAT (Computer-Assisted Translation) tools in the localization industry.

## Core features

- **Translation Memory integration**: leverages past translations automatically as segments are opened.
- **Termbase integration**: shows recognized terms from a MultiTerm termbase while translating.
- **QA Checker**: runs automated checks for things like missing tags, inconsistent numbers, terminology mismatches, and empty target segments.
- **Machine translation plugins**: can pull suggestions from providers like DeepL or a customer's own MT engine, alongside TM matches.
- **Project packages**: `.sdlppx` files bundle everything a translator needs (source files, TM, termbase, settings) into a single package to send out; the translator returns a `.sdlrpx` return package with the finished work.

## File handling

Trados Studio converts most source formats (Word, InDesign, HTML, XML, JSON, .resx, and many others) into its bilingual SDLXLIFF format for translation, then converts the finished SDLXLIFF back into the original format. This conversion step is handled by file type "filters," which can be customized for formats that need special handling, such as skipping certain XML attributes or treating specific tags as non-translatable.

## Studio vs other CAT tools

Competing tools like memoQ and Wordfast offer similar workflows, but Trados Studio remains dominant in enterprise localization because of its long history, plugin ecosystem, and compatibility with TMX and SDLXLIFF, which many LSPs (Language Service Providers) already have tooling around.
