"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


# Paragraphs shorter than this carry no answerable content on their own (a
# title line, mostly), so they get merged into a neighbour instead of shipping
# as a standalone chunk.
MIN_PARAGRAPH_CHARS = 30


def _merge_short_paragraphs(paragraphs: list[str]) -> list[str]:
    """Fold any paragraph under MIN_PARAGRAPH_CHARS into the one before it."""
    merged: list[str] = []
    for para in paragraphs:
        if merged and len(para) < MIN_PARAGRAPH_CHARS:
            merged[-1] = f"{merged[-1]}\n\n{para}"  # glue it onto the previous paragraph
        else:
            merged.append(para)
    return merged


def _split_one_document(doc: Document) -> list[Chunk]:
    """Group a single document's paragraphs into title-anchored chunks."""
    paragraphs = [p.strip() for p in doc.text.split("\n\n") if p.strip()]
    if not paragraphs:
        return []

    paragraphs = _merge_short_paragraphs(paragraphs)
    title, *body = paragraphs  # every campus_life doc opens with a one-line title

    if not body:
        # Nothing but a title (or a single paragraph) — one thought, one chunk.
        return [
            Chunk(text=title, source=doc.source, index=0, produced_by="chunker.py::split_documents")
        ]

    ceiling = config.CHUNK_SIZE  # soft cap on how much a chunk should hold

    groups: list[list[str]] = []
    current: list[str] = []
    current_len = len(title)     # the title gets repeated in every chunk, so count it upfront

    for para in body:
        added_len = len(para) + 2  # +2 accounts for the blank line that will join it
        if current and current_len + added_len > ceiling:
            groups.append(current)     # this group is full, start a fresh one
            current, current_len = [], len(title)
        current.append(para)
        current_len += added_len
    if current:
        groups.append(current)  # don't drop the last, possibly under-full, group

    # No character-overlap here on purpose: every split falls on a real
    # paragraph break already, so there's no arbitrary cut to bridge, and
    # slicing a fixed number of characters off a paragraph risks cutting a
    # word in half. The repeated title is what keeps chunks 1..N legible on
    # their own.
    chunks: list[Chunk] = []
    for i, group in enumerate(groups):
        chunks.append(
            Chunk(
                text="\n\n".join([title, *group]),
                source=doc.source,
                index=i,
                produced_by="chunker.py::split_documents",
            )
        )

    return chunks

def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks, respecting paragraph boundaries.

    Built for campus_life: every document opens with a one-line title
    paragraph followed by one or more body paragraphs. A title alone is never
    useful, so it's folded into whichever body paragraph follows it instead of
    becoming its own chunk. The remaining body paragraphs are then grouped
    into chunks up to CHUNK_SIZE characters, so a document with one short
    thought stays a single chunk while one bundling several distinct facts
    (e.g. a dorm review's "good" / "bad" / "logistics" paragraphs) splits into
    separately retrievable pieces. Every chunk repeats the title so it still
    reads as "about X" on its own.
    """
    chunks: list[Chunk] = []
    for doc in documents:
        chunks.extend(_split_one_document(doc))  # each document is chunked independently
    return chunks



def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
