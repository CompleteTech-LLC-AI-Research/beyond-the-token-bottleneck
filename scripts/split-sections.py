"""
Split large Obsidian wiki files into directory-based structures.

For each qualifying file (>= MIN_SECTIONS H2s and >= MIN_LINES lines):
  1. Create a directory with the same name as the file (minus .md)
  2. Extract each ## section into its own file in that directory
  3. Replace the original file with a version containing transclusions (![[...]])
  4. The main file keeps its original filename inside the directory,
     so all existing [[wikilinks]] resolve unchanged.

Usage:
  python scripts/split-sections.py [--dry-run] [--min-sections N] [--min-lines N] [path ...]
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

MIN_SECTIONS = 4
MIN_LINES = 100


def slugify(title: str) -> str:
    """Convert a section title to a filename slug."""
    s = title.strip().lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def parse_file(text: str):
    """
    Parse a markdown file into:
      - frontmatter (str or None, includes --- delimiters)
      - h1_line (str or None)
      - intro (str) — content between H1 and first H2
      - sections: list of (title, body) for each ## heading
    """
    lines = text.split("\n")
    idx = 0

    # --- frontmatter ---
    frontmatter = None
    if lines and lines[0].strip() == "---":
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        if end is not None:
            frontmatter = "\n".join(lines[: end + 1])
            idx = end + 1

    # skip blank lines after frontmatter
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1

    # --- H1 ---
    h1_line = None
    if idx < len(lines) and lines[idx].startswith("# ") and not lines[idx].startswith("## "):
        h1_line = lines[idx]
        idx += 1

    # --- intro (between H1 and first ##) ---
    intro_lines = []
    while idx < len(lines) and not lines[idx].startswith("## "):
        intro_lines.append(lines[idx])
        idx += 1
    intro = "\n".join(intro_lines).strip()

    # --- sections ---
    sections = []
    while idx < len(lines):
        if lines[idx].startswith("## "):
            title = lines[idx][3:].strip()
            idx += 1
            body_lines = []
            while idx < len(lines) and not lines[idx].startswith("## "):
                body_lines.append(lines[idx])
                idx += 1
            body = "\n".join(body_lines).strip()
            sections.append((title, body))
        else:
            idx += 1

    return frontmatter, h1_line, intro, sections


def build_index(frontmatter, h1_line, intro, section_files, dir_name):
    """Build the new index file with transclusions."""
    parts = []
    if frontmatter:
        parts.append(frontmatter)
        parts.append("")
    if h1_line:
        parts.append(h1_line)
        parts.append("")
    if intro:
        parts.append(intro)
        parts.append("")

    for slug, title in section_files:
        parts.append(f"## {title}")
        parts.append("")
        parts.append(f"![[{dir_name}/{slug}]]")
        parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def build_section_file(title, body):
    """Build a section file: body only, no heading (heading lives in the index)."""
    return f"{body}\n"


def process_file(filepath: Path, dry_run: bool = False,
                  min_sections: int = MIN_SECTIONS, min_lines: int = MIN_LINES):
    """Process a single file. Returns (dir_created, num_sections) or None if skipped."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")

    h2_count = sum(1 for l in lines if l.startswith("## "))
    if h2_count < min_sections or len(lines) < min_lines:
        return None

    frontmatter, h1_line, intro, sections = parse_file(text)
    if len(sections) < min_sections:
        return None

    dir_name = filepath.stem  # e.g. "overview-state-of-field"
    dir_path = filepath.parent / dir_name

    # Build section file list: (slug, title)
    section_files = []
    used_slugs = set()
    for title, body in sections:
        slug = slugify(title)
        # deduplicate slugs
        orig_slug = slug
        counter = 2
        while slug in used_slugs:
            slug = f"{orig_slug}-{counter}"
            counter += 1
        used_slugs.add(slug)
        section_files.append((slug, title, body))

    index_content = build_index(
        frontmatter, h1_line, intro,
        [(s[0], s[1]) for s in section_files],
        dir_name,
    )

    if dry_run:
        print(f"  WOULD create: {dir_path}/")
        print(f"  WOULD rewrite: {filepath}  (index with {len(sections)} transclusions)")
        for slug, title, _ in section_files:
            print(f"  WOULD create: {dir_path}/{slug}.md  ({title})")
        return dir_name, len(sections)

    # Create directory for section files
    dir_path.mkdir(exist_ok=True)

    # Write section files into the subdirectory
    for slug, title, body in section_files:
        section_path = dir_path / f"{slug}.md"
        section_path.write_text(build_section_file(title, body), encoding="utf-8")

    # Rewrite the original file in place with transclusions
    filepath.write_text(index_content, encoding="utf-8")

    return dir_name, len(sections)


def find_candidates(wiki_root: Path, min_sections: int = MIN_SECTIONS,
                    min_lines: int = MIN_LINES):
    """Find all .md files that qualify for splitting."""
    candidates = []
    for md_file in sorted(wiki_root.rglob("*.md")):
        if md_file.name in ("log.md",):
            continue
        text = md_file.read_text(encoding="utf-8")
        lines = text.split("\n")
        h2_count = sum(1 for l in lines if l.startswith("## "))
        if h2_count >= min_sections and len(lines) >= min_lines:
            candidates.append(md_file)
    return candidates


def main():
    parser = argparse.ArgumentParser(description="Split large wiki files into section directories")
    parser.add_argument("paths", nargs="*", help="Specific files to process (default: scan wiki/)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--min-sections", type=int, default=MIN_SECTIONS)
    parser.add_argument("--min-lines", type=int, default=MIN_LINES)
    args = parser.parse_args()

    min_sections = args.min_sections
    min_lines = args.min_lines

    if args.paths:
        files = [Path(p) for p in args.paths]
    else:
        wiki_root = Path(__file__).parent.parent / "wiki"
        files = find_candidates(wiki_root, min_sections, min_lines)

    print(f"Found {len(files)} candidate(s) (>={min_sections} H2 sections, >={min_lines} lines)\n")

    results = []
    for f in files:
        print(f"{'[DRY RUN] ' if args.dry_run else ''}Processing: {f.relative_to(Path(__file__).parent.parent)}")
        result = process_file(f, dry_run=args.dry_run,
                              min_sections=min_sections, min_lines=min_lines)
        if result:
            results.append((f, result))
            print(f"  -> {result[1]} sections extracted\n")
        else:
            print(f"  -> Skipped (below threshold)\n")

    print(f"\n{'Would process' if args.dry_run else 'Processed'}: {len(results)} file(s)")
    total_sections = sum(r[1][1] for r in results)
    print(f"Total sections: {total_sections}")


if __name__ == "__main__":
    main()
