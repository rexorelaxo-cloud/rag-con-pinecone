# Linguistic QA

Linguistic Quality Assurance (LQA) is the process of checking translated content for accuracy, consistency, and adherence to style and terminology guidelines, separate from purely mechanical checks.

## Automated vs human QA

Most localization workflows combine two layers:

1. **Automated QA checks**, run by the CAT tool or a dedicated QA tool (like Xbench or Verifika). These catch objective, rule-based issues: missing or extra tags, placeholder mismatches, inconsistent translation of the same source segment, number mismatches, double spaces, terminology violations against the approved termbase, untranslated segments, and trailing punctuation differences.
2. **Human linguistic review**, done by a second linguist (often called a reviewer or editor) who reads the translation for fluency, tone, register, cultural appropriateness, and meaning accuracy against the source.

## LQA scoring models

Many LSPs use a scoring model such as the Multidimensional Quality Metrics (MQM) framework, where a reviewer samples a portion of the translated content and logs errors by category (accuracy, fluency, terminology, style, locale convention) and severity (minor, major, critical). The sampled error rate is then used to calculate a pass/fail quality score for the delivery.

## Common LQA error categories

- Mistranslation (wrong meaning)
- Omission (source content missing from target)
- Addition (target has content not in source)
- Terminology inconsistency
- Grammar/spelling errors
- Style/register mismatch
- Locale convention errors (date formats, currency, measurement units)

## Why it matters for localization engineering

Localization engineers don't usually perform LQA themselves, but they build and maintain the pipelines and tooling that make it possible: exporting bilingual review files, integrating QA-checker rule sets, and feeding LQA scorecards back into vendor performance tracking.
