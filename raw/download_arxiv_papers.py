#!/usr/bin/env python3
"""Download the arXiv PDFs and LaTeX sources currently used by this vault.

This script keeps local raw assets in sync with the papers referenced by wiki
source pages. It intentionally uses a single sequential connection and spaces
requests at least three seconds apart to conservatively match arXiv's API terms
of use as of 2026-04-06:
https://info.arxiv.org/help/api/tou.html

Outputs:
  ./pdf/arxiv-<arxiv_id>.pdf
  ./latex/arxiv-<arxiv_id>/... extracted source files ...
  ./latex/arxiv-<arxiv_id>.tar.gz

When adding a paper to the vault, update PAPER_SPECS so this downloader remains
the reproducible source of truth for arXiv-managed raw assets.
"""

from __future__ import annotations

import argparse
import io
import shutil
import tarfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class PaperSpec:
    arxiv_id: str
    latex_mode: Literal["archive", "extract"]


PAPER_SPECS = [
    PaperSpec("2209.15430", "extract"),
    PaperSpec("2305.14325", "extract"),
    PaperSpec("2305.15408", "extract"),
    PaperSpec("2308.09124", "extract"),
    PaperSpec("2310.02226", "extract"),
    PaperSpec("2310.06272", "archive"),
    PaperSpec("2405.07987", "extract"),
    PaperSpec("2405.14838", "extract"),
    PaperSpec("2412.06769", "archive"),
    PaperSpec("2501.14082", "archive"),
    PaperSpec("2502.12134", "archive"),
    PaperSpec("2505.12514", "extract"),
    PaperSpec("2506.19209", "archive"),
    PaperSpec("2510.03215", "archive"),
    PaperSpec("2510.03346", "archive"),
    PaperSpec("2510.12872", "archive"),
    PaperSpec("2510.20733", "archive"),
    PaperSpec("2511.09149", "archive"),
    PaperSpec("2511.20639", "archive"),
    PaperSpec("2512.08296", "archive"),
    PaperSpec("2601.06123", "archive"),
    PaperSpec("2602.03695", "archive"),
    PaperSpec("2602.08332", "archive"),
    PaperSpec("2602.15382", "archive"),
]

PDF_DIR = Path("./pdf")
LATEX_DIR = Path("./latex")
TIMEOUT_SECONDS = 60
OVERWRITE = False
MIN_SECONDS_BETWEEN_REQUESTS = 3.0
MAX_ATTEMPTS = 3
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
BASE_RETRY_DELAY_SECONDS = 15.0
USER_AGENT = "OpenClawExperimentRawDownloader/1.0 (+local vault maintenance)"

_last_request_started_at: float | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download or verify the arXiv assets used by this vault."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned actions without downloading or modifying files.",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Check that all expected local assets exist and exit without downloading.",
    )
    args = parser.parse_args()
    if args.dry_run and args.verify_only:
        parser.error("--dry-run and --verify-only cannot be used together")
    return args


def arxiv_id_from_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    if not path:
        raise ValueError(f"Could not parse arXiv ID from URL: {url}")

    paper_id = path.split("/")[-1]
    if paper_id.startswith("arXiv:"):
        paper_id = paper_id[len("arXiv:") :]
    if paper_id.endswith(".pdf"):
        paper_id = paper_id[:-4]

    if not paper_id:
        raise ValueError(f"Could not parse arXiv ID from URL: {url}")

    return paper_id


def canonical_paper_ids(specs: Iterable[PaperSpec]) -> list[str]:
    seen: set[str] = set()
    ids: list[str] = []
    for spec in specs:
        paper_id = arxiv_id_from_url(f"https://arxiv.org/abs/{spec.arxiv_id}")
        if paper_id not in seen:
            seen.add(paper_id)
            ids.append(paper_id)
    return ids


def expected_pdf_path(paper: PaperSpec) -> Path:
    return PDF_DIR / f"arxiv-{paper.arxiv_id}.pdf"


def expected_latex_path(paper: PaperSpec) -> Path:
    suffix = ".tar.gz" if paper.latex_mode == "archive" else ""
    return LATEX_DIR / f"arxiv-{paper.arxiv_id}{suffix}"


def has_expected_latex_asset(paper: PaperSpec) -> bool:
    latex_path = expected_latex_path(paper)
    if paper.latex_mode == "archive":
        return latex_path.exists()
    return latex_path.exists() and latex_path.is_dir() and any(latex_path.iterdir())


def report_plan(paper: PaperSpec) -> None:
    pdf_path = expected_pdf_path(paper)
    latex_path = expected_latex_path(paper)

    if pdf_path.exists() and not OVERWRITE:
        print(f"  - would skip PDF (already exists): {pdf_path}")
    else:
        print(f"  - would download PDF: {pdf_path}")

    if has_expected_latex_asset(paper) and not OVERWRITE:
        kind = "source archive" if paper.latex_mode == "archive" else "source extract"
        print(f"  - would skip {kind} (already exists): {latex_path}")
    else:
        action = "download source archive" if paper.latex_mode == "archive" else "extract source"
        print(f"  - would {action}: {latex_path}")


def verify_local_assets(papers: Iterable[PaperSpec]) -> list[str]:
    failures: list[str] = []

    for paper in papers:
        pdf_path = expected_pdf_path(paper)
        latex_path = expected_latex_path(paper)

        if not pdf_path.exists():
            failures.append(f"{paper.arxiv_id}: missing PDF {pdf_path}")

        if not has_expected_latex_asset(paper):
            kind = "archive" if paper.latex_mode == "archive" else "extracted source directory"
            failures.append(f"{paper.arxiv_id}: missing LaTeX {kind} {latex_path}")

    return failures


def wait_for_rate_limit() -> None:
    global _last_request_started_at

    now = time.monotonic()
    if _last_request_started_at is not None:
        elapsed = now - _last_request_started_at
        if elapsed < MIN_SECONDS_BETWEEN_REQUESTS:
            time.sleep(MIN_SECONDS_BETWEEN_REQUESTS - elapsed)

    _last_request_started_at = time.monotonic()


def fetch_bytes(url: str) -> bytes:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Connection": "close",
        },
    )

    for attempt in range(1, MAX_ATTEMPTS + 1):
        wait_for_rate_limit()
        try:
            with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                return response.read()
        except HTTPError as exc:
            should_retry = exc.code in RETRYABLE_STATUS_CODES and attempt < MAX_ATTEMPTS
            if not should_retry:
                raise
            delay = BASE_RETRY_DELAY_SECONDS * attempt
            print(
                f"  ! HTTP {exc.code} from {url}; retrying in {delay:.0f}s "
                f"({attempt}/{MAX_ATTEMPTS})"
            )
            time.sleep(delay)
        except URLError as exc:
            if attempt >= MAX_ATTEMPTS:
                raise
            delay = BASE_RETRY_DELAY_SECONDS * attempt
            print(
                f"  ! Network error from {url}: {exc.reason}; retrying in "
                f"{delay:.0f}s ({attempt}/{MAX_ATTEMPTS})"
            )
            time.sleep(delay)

    raise RuntimeError(f"Failed to fetch {url} after {MAX_ATTEMPTS} attempts")


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def is_within_directory(directory: Path, target: Path) -> bool:
    directory = directory.resolve()
    target = target.resolve()
    return directory == target or directory in target.parents


def safe_extract_tar_bytes(data: bytes, destination: Path) -> None:
    if destination.exists():
        if OVERWRITE:
            shutil.rmtree(destination)
        else:
            existing = list(destination.iterdir())
            if existing:
                print(f"  - skip source extract (already exists): {destination}")
                return
            destination.rmdir()

    destination.mkdir(parents=True, exist_ok=True)

    with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as archive:
        members = archive.getmembers()
        for member in members:
            member_path = destination / member.name
            if not is_within_directory(destination, member_path):
                raise RuntimeError(
                    f"Unsafe path in tar archive for {destination.name}: {member.name}"
                )
        archive.extractall(destination)


def download_pdf(paper: PaperSpec) -> None:
    pdf_path = expected_pdf_path(paper)
    if pdf_path.exists() and not OVERWRITE:
        print(f"  - skip PDF (already exists): {pdf_path}")
        return

    pdf_url = f"https://arxiv.org/pdf/{paper.arxiv_id}"
    pdf_bytes = fetch_bytes(pdf_url)
    write_bytes(pdf_path, pdf_bytes)
    print(f"  - saved PDF: {pdf_path}")


def download_latex_source(paper: PaperSpec) -> None:
    if paper.latex_mode == "archive":
        archive_path = expected_latex_path(paper)
        if archive_path.exists() and not OVERWRITE:
            print(f"  - skip source archive (already exists): {archive_path}")
            return
        source_bytes = fetch_bytes(f"https://arxiv.org/src/{paper.arxiv_id}")
        write_bytes(archive_path, source_bytes)
        print(f"  - saved source archive: {archive_path}")
        return

    source_dir = expected_latex_path(paper)
    if source_dir.exists() and not OVERWRITE and any(source_dir.iterdir()):
        print(f"  - skip source extract (already exists): {source_dir}")
        return

    source_bytes = fetch_bytes(f"https://arxiv.org/src/{paper.arxiv_id}")
    safe_extract_tar_bytes(source_bytes, source_dir)
    print(f"  - extracted source: {source_dir}")


def main() -> None:
    args = parse_args()
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    LATEX_DIR.mkdir(parents=True, exist_ok=True)

    paper_ids = canonical_paper_ids(PAPER_SPECS)
    if len(paper_ids) != len(PAPER_SPECS):
        raise ValueError("PAPER_SPECS contains duplicate arXiv IDs")

    if args.verify_only:
        failures = verify_local_assets(PAPER_SPECS)
        if failures:
            print("Local asset verification failed:")
            for failure in failures:
                print(f"- {failure}")
            raise SystemExit(1)
        print(f"Verified {len(PAPER_SPECS)} arXiv papers: all expected local assets are present.")
        return

    if args.dry_run:
        print(f"Dry run for {len(PAPER_SPECS)} arXiv papers:")
        for index, paper in enumerate(PAPER_SPECS, start=1):
            print(f"[{index}/{len(PAPER_SPECS)}] {paper.arxiv_id} ({paper.latex_mode})")
            report_plan(paper)
        print("\nDry run complete.")
        return

    print(f"Downloading {len(PAPER_SPECS)} arXiv papers with 1 request every 3 seconds...")

    failures: list[tuple[str, str]] = []

    for index, paper in enumerate(PAPER_SPECS, start=1):
        print(f"[{index}/{len(PAPER_SPECS)}] {paper.arxiv_id} ({paper.latex_mode})")

        try:
            download_pdf(paper)
        except (HTTPError, URLError, OSError, ValueError, RuntimeError) as exc:
            failures.append((paper.arxiv_id, f"PDF failed: {exc}"))
            print(f"  ! PDF failed: {exc}")

        try:
            download_latex_source(paper)
        except tarfile.ReadError as exc:
            failures.append((paper.arxiv_id, f"source extract failed: {exc}"))
            print(f"  ! source extract failed: {exc}")
        except (HTTPError, URLError, OSError, ValueError, RuntimeError) as exc:
            failures.append((paper.arxiv_id, f"source download failed: {exc}"))
            print(f"  ! source download failed: {exc}")

    if failures:
        print("\nCompleted with some issues:")
        for paper_id, message in failures:
            print(f"- {paper_id}: {message}")
    else:
        print("\nDone. All PDFs and LaTeX sources were downloaded successfully.")


if __name__ == "__main__":
    main()
