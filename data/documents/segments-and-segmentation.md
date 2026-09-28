# Segments and Segmentation

In localization, a "segment" is the basic translatable unit that a CAT tool works with — typically a sentence, but sometimes a heading, list item, or table cell.

## Segmentation rules

Segmentation is the process of splitting a source document into segments. Most CAT tools use SRX (Segmentation Rules eXchange), an XML-based standard that defines where a segment should break — usually after a period followed by a space and a capital letter, but with exceptions for abbreviations like "Mr." or "e.g." so the tool doesn't wrongly split mid-sentence.

Getting segmentation rules right matters a lot for TM leverage: if two projects segment the same source text differently, segments that should match 100% might not match at all, since the TM compares segment-by-segment.

## Segment status

Inside a bilingual file (such as an SDLXLIFF), each segment carries a status such as:

- Not Translated
- Draft
- Translated
- Reviewed
- Signed Off / Approved

Project managers and reviewers use these statuses to track progress and to filter which segments still need attention.

## Segment context

Some CAT tools also track the segments immediately before and after a given segment ("context"), which is what enables context matches (ICE) described in the match-percentages document. Without stored context, a TM can only offer a plain fuzzy or exact match based on the text alone, without knowing whether the surrounding sentences are the same.
