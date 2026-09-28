# XPath for Localization Engineers

XPath (XML Path Language) is a query language for selecting nodes in an XML document. Localization engineers use it constantly when writing file-format filters, validation scripts, or automated content extraction from XML-based sources.

## Why localization engineering needs XPath

Many localization file filters (for XLIFF, custom XML, DITA, DOCX internals, etc.) let you define which nodes are translatable using XPath expressions rather than hard-coded element names. This makes the filter reusable across many similar documents, even when there is some structural variation.

## Basic syntax examples

- `/root/item` — selects `item` elements that are direct children of `root`.
- `//title` — selects every `title` element anywhere in the document.
- `//string[@translatable="true"]` — selects `string` elements whose `translatable` attribute equals `true`.
- `//text()` — selects all text nodes.
- `//comment[not(@internal)]` — selects `comment` elements that do not have an `internal` attribute.

## Practical use in a pipeline

A typical use case: a localization engineer receives a client's proprietary XML export and needs to build a quick script (often in Python with `lxml` or `ElementTree`) that walks the tree with XPath to pull out only the translatable strings, tag each with a stable identifier (so the translation can be merged back later), and hand that list to the CAT tool or translation vendor.

## Common pitfalls

- Forgetting XML namespaces: if a document declares a namespace, XPath expressions must reference it (or use a wildcard/local-name() trick), otherwise the query silently returns nothing.
- Overly broad expressions (like `//text()`) can pick up whitespace-only text nodes or non-translatable code fragments if the source XML isn't clean.
