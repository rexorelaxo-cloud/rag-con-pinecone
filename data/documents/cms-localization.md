# CMS Localization

Content Management Systems (CMS) present a specific localization challenge because content lives in a database or structured repository rather than in flat files, and it often needs to stay in sync with the source content as it keeps changing.

## Common CMS localization workflows

1. **Export/import**: the CMS exports content that needs translation (often as XML, JSON, or via a dedicated connector) to a translation management system (TMS), and imports the finished translations back once complete.
2. **In-context editing**: some CMS platforms offer a translation UI directly inside the CMS, letting a translator work while seeing a live preview of the page.
3. **Continuous localization**: content updates trigger automatic jobs that detect new or changed strings and route only the delta to translation, instead of re-sending entire pages every time.

## Key technical challenges

- **Content relationships**: a CMS page often references shared components, templates, or media that must not be duplicated per locale unless actually needed.
- **Versioning and staleness**: keeping track of which locale versions are up to date with the latest source content, and flagging out-of-date translations after a source update.
- **Rich text and embedded markup**: CMS fields often contain HTML-like rich text, which needs the same non-translatable-tag handling described in the placeholders-and-tags and XML-localization documents.
- **URL slugs and SEO metadata**: these often need locale-specific translation too, not just the visible page content.

## Sitecore as an example

Sitecore is one of several enterprise CMS platforms with a mature localization workflow, discussed in more detail in the dedicated Sitecore document. Other platforms (Adobe Experience Manager, Contentful, WordPress with a localization plugin) follow broadly similar patterns, differing mainly in how granular their content model is and how good their built-in translation connectors are.
