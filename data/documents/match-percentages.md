# Translation Match Percentages

When a Translation Memory searches for a matching segment, it doesn't just return exact matches — it scores every candidate on how similar it is to the new source segment, and reports that score as a match percentage.

## Common match categories

- **100% match**: the new segment is character-for-character identical to a segment already in the TM.
- **Context match (ICE — In-Context Exact)**: a 100% match where the surrounding segments also match, so the context is guaranteed identical. Usually requires no review at all.
- **Fuzzy match**: anything below 100%, meaning the source is similar but not identical. Fuzzy matches are commonly bucketed into ranges such as 50-74%, 75-84%, 85-94%, and 95-99%.
- **No match / New**: no TM match above the configured minimum threshold (often 30% or 50%), so the segment must be translated from scratch.
- **Repetition**: a segment that repeats elsewhere in the same project, so it only needs to be translated once.

## Why the percentage matters

Match percentage drives both effort estimation and pricing. A 95-99% fuzzy match usually only needs a small edit (maybe a changed number or product name), while a 50-74% match might need substantial rewriting. Many translation vendors use a pricing grid — for example paying full rate for new words, a reduced rate for fuzzy matches, and a minimal rate for 100% matches and repetitions — because the effort required is genuinely lower.

## Caveats localization engineers should know

A high match percentage does not always mean the segment is safe to reuse as-is. Numbers, placeholders, or tags may differ even when the running text matches almost exactly, so QA tools still need to flag those differences even inside high fuzzy-match segments. This is one reason automated tag and number validation exists independently of TM leverage reporting.
