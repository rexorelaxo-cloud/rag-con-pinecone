# Translation Memories (TMs)

A Translation Memory (TM) is a database that stores previously translated segments (usually sentences or phrases) paired with their source text. Every time a translator confirms a segment, the pair gets saved so it can be reused later.

## Why TMs matter

The main value of a TM is leverage: reusing translations that already exist instead of retranslating from scratch. This saves time, reduces cost, and keeps terminology and phrasing consistent across a project, especially when the same client sends similar content over years (release notes, UI strings, legal boilerplate).

## How matching works

When a new segment comes in, the TM engine compares it against every stored segment and returns the closest matches, ranked by a match percentage. A 100% match means the source segment is identical to one already translated. Anything below that is a "fuzzy match" — close but not exact, usually because of small wording changes, added punctuation, or a different number.

TMs are usually stored in the TMX format (Translation Memory eXchange), an XML-based standard that lets different CAT tools (Trados Studio, memoQ, Wordfast) share memories with each other.

## TM vs Termbase

People sometimes confuse a TM with a termbase (glossary). A TM stores full sentences/segments with their translations. A termbase stores individual terms and their approved equivalents. Both are used together during translation, but they solve different problems: TMs handle repetition and phrasing, termbases handle consistent word choice.

## Leverage reports

Before a project starts, project managers usually run a "TM analysis" against the source files. This produces a leverage report broken down by match category (New, Fuzzy 75-84%, Fuzzy 85-94%, Fuzzy 95-99%, Repetitions, 100% match, Context match/ICE). Rates paid to translators are often scaled down for higher match percentages, since less new translation work is required.
