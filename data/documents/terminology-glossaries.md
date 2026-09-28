# Terminology and Glossaries

A termbase (also called a glossary or term base) is a structured collection of approved terms and their translations, used to keep word choice consistent across a project, product, or company.

## Termbase vs Translation Memory

A termbase stores individual concepts (single words or short phrases, like "invoice", "checkout", or a specific product name) along with definitions, part of speech, usage notes, and forbidden alternatives. A Translation Memory, in contrast, stores whole translated segments. Both are used together in a CAT tool: the TM suggests full-segment matches, while the termbase highlights recognized terms inline and warns if the translator uses a different word than the approved one.

## TBX format

Termbases are commonly exchanged using TBX (TermBase eXchange), an XML-based standard, so glossaries built in one tool (like SDL MultiTerm) can be imported into another CAT tool or QA checker.

## Building a good glossary

A useful termbase usually includes:

- the approved term in the source language
- the approved translation per target locale
- a short definition or usage context
- forbidden or deprecated alternative translations
- part of speech and domain/category tags

## Why glossaries matter for QA

Most linguistic QA tools cross-check every translated segment against the termbase and flag any segment where an approved term appears in the source but a different (non-approved) translation was used in the target — one of the most common categories of LQA findings, alongside tag and placeholder mismatches.
