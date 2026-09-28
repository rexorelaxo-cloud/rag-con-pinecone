# Character Limits in Localization

Many UI strings have a maximum character (or pixel) length they must fit within, because they render inside a fixed-size button, label, tab, or notification banner. Translating into a language that expands the text (as most European languages do compared to English) can easily break the layout if this isn't accounted for.

## Text expansion

As a rule of thumb, translators and localization engineers often use these approximate expansion factors from English:

- German, Finnish: can expand 20-35%
- French, Spanish, Italian, Portuguese: typically expand 15-25%
- Russian, Polish and other Slavic languages: can expand 15-25%
- Chinese, Japanese, Korean: often contract or stay similar in character count, but characters are visually wider, so pixel width still grows

Short English UI strings (button labels like "Save" or "Cancel") tend to expand the most proportionally, since a short string has little room to absorb extra characters.

## Enforcing limits

Character limits are usually enforced in one of two ways:

1. **Hard character count limits** defined in the source string metadata (e.g. `maxLength: 20`), which the CAT tool or QA checker validates automatically and flags any translation that exceeds it.
2. **Pixel-width testing**, which is more accurate for proportional fonts but requires either rendering the string in the actual UI or using a font-metrics tool to estimate rendered width.

## Practical mitigation

When a translation genuinely can't fit, localization engineers and linguists have a few options: request a shorter source string from the product team, allow the UI element to resize or wrap, use abbreviations (carefully, since these can hurt readability), or, as a last resort, request a locale-specific exception in the design.
