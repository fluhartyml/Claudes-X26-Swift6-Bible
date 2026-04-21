#!/usr/bin/env python3
"""One-off: flatten Books, Appendices, and Lexicon Chapters so sidebar
reveals are single-level. Eliminates same-name folder/file redundancy.

Before:
  Part-I-Introduction/Book-01-Slug/Book-01-Slug.html
  Appendices/Appendix-A-Slug/Appendix-A-Slug.html
  Part-II.../Chapter-A/Chapter-A.html
  Part-II.../Chapter-A/Pages/Page-*.html

After:
  Part-I-Introduction/Book-01-Slug.html
  Appendices/Appendix-A-Slug.html
  Part-II.../Chapter-A/Page-*.html     (landing file deleted; Pages/ merged up)
"""

from pathlib import Path
import shutil

BUNDLE = Path(
    "/Users/michaelfluharty/Developer.complex/inkwell/"
    "Claudes X26 Swift6 Bible/Claudes X26 Swift6 Bible/BibleContent.bundle"
)

def flatten_book_like(folder, pattern_prefix):
    """For each <pattern_prefix>-* subdir in folder, move the same-named
    .html up one level, then remove the now-empty subdir."""
    moved = 0
    for child in sorted(folder.iterdir()):
        if not child.is_dir():
            continue
        if not child.name.startswith(pattern_prefix):
            continue
        html = child / f"{child.name}.html"
        if html.exists():
            dest = folder / f"{child.name}.html"
            if dest.exists():
                dest.unlink()
            html.rename(dest)
            moved += 1
        # remove child if empty
        try:
            remaining = list(child.iterdir())
            if not remaining:
                child.rmdir()
        except OSError:
            pass
    return moved


def flatten_chapters():
    part = BUNDLE / "Part-II-The-Swift-Language"
    if not part.exists():
        return 0
    moved = 0
    for chapter in sorted(part.iterdir()):
        if not chapter.is_dir() or not chapter.name.startswith("Chapter-"):
            continue
        # delete the redundant landing file
        landing = chapter / f"{chapter.name}.html"
        if landing.exists():
            landing.unlink()
        # move Pages/*.html up into chapter dir, remove Pages/
        pages_dir = chapter / "Pages"
        if pages_dir.exists() and pages_dir.is_dir():
            for page in sorted(pages_dir.iterdir()):
                if page.suffix == ".html":
                    dest = chapter / page.name
                    if dest.exists():
                        dest.unlink()
                    page.rename(dest)
                    moved += 1
            try:
                pages_dir.rmdir()
            except OSError:
                pass
    return moved


def main():
    # Books: Part-I through Part-VI
    book_moved = 0
    for part in sorted(BUNDLE.iterdir()):
        if part.is_dir() and part.name.startswith("Part-"):
            book_moved += flatten_book_like(part, "Book-")
    print(f"Flattened {book_moved} Book files")

    # Appendices
    appendices = BUNDLE / "Appendices"
    if appendices.exists():
        ap_moved = flatten_book_like(appendices, "Appendix-")
        print(f"Flattened {ap_moved} Appendix files")

    # Lexicon Chapters
    ch_moved = flatten_chapters()
    print(f"Flattened {ch_moved} Lexicon Pages (landings deleted, Pages/ merged)")


if __name__ == "__main__":
    main()
