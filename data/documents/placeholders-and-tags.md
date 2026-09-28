# Placeholders and Tags

Localization content is rarely plain text. It usually contains two kinds of non-translatable elements that translators must preserve: placeholders and tags.

## Placeholders

Placeholders are variables that get replaced with dynamic content at runtime, such as `{userName}`, `%s`, `{0}`, or `<ph id="1"/>`. They're extremely common in software UI strings, emails, and notifications. Examples:

- "Welcome back, {userName}!"
- "You have %d new messages"
- "Your order #{orderId} has shipped"

A translator must keep the placeholder syntax exactly as-is — only the surrounding natural language text can be reordered or reworded, since some languages need the variable to appear in a different position in the sentence.

## Tags

Tags usually come from formatting embedded in the source document: bold, italics, hyperlinks, superscripts, or structural markup from XML/HTML. CAT tools display these as protected inline tags (sometimes shown as small numbered icons) rather than raw markup, so translators can't accidentally break the underlying code while still seeing where formatting applies.

## Why this matters for QA

Two of the most common bugs in localized software come directly from mishandled placeholders and tags:

1. A placeholder gets mistranslated, deleted, or has its casing changed, breaking the string substitution at runtime.
2. Tags get reordered or dropped, breaking formatting or, in worse cases, breaking the markup entirely so the app fails to render the string.

This is why most linguistic QA tools include an automated tag-and-placeholder check that compares source and target segments and flags any mismatch, independent of whether a human reviewer also checks the segment manually.
