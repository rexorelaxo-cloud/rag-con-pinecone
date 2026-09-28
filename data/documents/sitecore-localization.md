# Sitecore Localization

Sitecore is an enterprise .NET-based CMS commonly used by large organizations, and it has built-in multi-language content support.

## How Sitecore stores languages

In Sitecore, every content item can have a version per language (e.g. `en`, `es-AR`, `de-DE`). A single item stores the same structural fields (layout, template, workflow state) but each language version stores its own field values. This differs from some CMS platforms that treat each locale as a fully separate copy of the page tree.

## Typical localization workflow in Sitecore

1. Content authors create or update content in the source language (often `en`).
2. A translation connector (built-in or third-party, such as connectors for Trados or a TMS) packages the changed fields and sends them for translation.
3. Translated content is imported back into the corresponding language version of each item.
4. Workflow states (Draft, Awaiting Approval, Approved, Published) track review status per language independently, so one locale can be published while another is still in review.

## Common technical issues

- **Field types matter**: rich text fields need HTML tag handling similar to any XML/HTML content, while single-line text fields are simpler but may still have character limits enforced by the template.
- **Item references**: Sitecore items often reference other items (for example a navigation menu referencing page items). A localization engineer needs to make sure translation packages don't break these references across languages.
- **Fallback languages**: Sitecore supports language fallback, showing the source-language value for a field until the localized value is filled in, which is useful for partial rollouts but can also mask untranslated content if fallback isn't monitored carefully.

## Why this matters for localization engineering

Localization engineers working with Sitecore usually build or configure the translation connector, define which templates/fields are translatable, and set up automated jobs that detect content changes and trigger new translation requests — a domain-specific version of the general CMS localization patterns described in the CMS-localization document.
