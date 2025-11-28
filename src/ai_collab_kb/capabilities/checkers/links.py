"""
Link Checker - Validate internal and external links in knowledge base.

This module provides:
- LinkType: Types of links (internal, external, anchor)
- LinkStatus: Link validation status
- LinkResult: Individual link check result
- LinkChecker: Comprehensive link validation

Author: AI Collaboration KB Team
Version: 2.0.0
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

logger = logging.getLogger(__name__)


class LinkType(Enum):
    """Types of links."""

    INTERNAL = "internal"  # Links to other files in KB
    EXTERNAL = "external"  # Links to external URLs
    ANCHOR = "anchor"  # Links to anchors within same file
    IMAGE = "image"  # Image references
    UNKNOWN = "unknown"


class LinkStatus(Enum):
    """Link validation status."""

    VALID = "valid"
    BROKEN = "broken"
    WARNING = "warning"  # e.g., redirect, slow
    SKIPPED = "skipped"  # e.g., external links not checked
    ERROR = "error"  # Check failed


@dataclass
class LinkResult:
    """Result of a link check."""

    source_file: str
    line_number: int
    link_text: str
    link_target: str
    link_type: LinkType
    status: LinkStatus
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "source_file": self.source_file,
            "line_number": self.line_number,
            "link_text": self.link_text,
            "link_target": self.link_target,
            "link_type": self.link_type.value,
            "status": self.status.value,
            "message": self.message,
            "details": self.details,
        }


@dataclass
class LinkReport:
    """Comprehensive link check report."""

    total_links: int
    valid_count: int
    broken_count: int
    warning_count: int
    skipped_count: int
    results: list[LinkResult]
    files_checked: int
    duration_ms: float
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def broken_rate(self) -> float:
        """Percentage of broken links."""
        checked = self.total_links - self.skipped_count
        return (self.broken_count / checked * 100) if checked > 0 else 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_links": self.total_links,
            "valid_count": self.valid_count,
            "broken_count": self.broken_count,
            "warning_count": self.warning_count,
            "skipped_count": self.skipped_count,
            "broken_rate": round(self.broken_rate, 2),
            "files_checked": self.files_checked,
            "duration_ms": round(self.duration_ms, 2),
            "timestamp": self.timestamp.isoformat(),
            "broken_links": [
                r.to_dict() for r in self.results if r.status == LinkStatus.BROKEN
            ],
        }


class LinkChecker:
    """
    Comprehensive link validation for the knowledge base.

    Features:
    - Internal link validation (file existence)
    - Anchor validation (heading existence)
    - External link validation (optional, with caching)
    - Batch checking with progress
    - Detailed reporting
    """

    # Regex patterns for link extraction
    MD_LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
    MD_IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    MD_REFERENCE_PATTERN = re.compile(r"\[([^\]]*)\]:\s*(\S+)")
    MD_HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)

    def __init__(
        self,
        kb_path: Path | None = None,
        check_external: bool = False,
        timeout_s: float = 10.0,
    ):
        """
        Initialize link checker.

        Args:
            kb_path: Path to knowledge base root
            check_external: Whether to check external URLs
            timeout_s: Timeout for external URL checks
        """
        self.kb_path = kb_path or Path(__file__).parent.parent.parent
        self.check_external = check_external
        self.timeout_s = timeout_s

        self._heading_cache: dict[str, set[str]] = {}
        self._file_cache: set[str] = set()

    def _normalize_anchor(self, heading: str) -> str:
        """Convert heading text to anchor format."""
        # GitHub-style anchor normalization
        anchor = heading.lower()
        anchor = re.sub(r"[^\w\s-]", "", anchor)
        anchor = re.sub(r"\s+", "-", anchor)
        return anchor

    def _get_file_headings(self, file_path: Path) -> set[str]:
        """Extract all headings from a markdown file."""
        if str(file_path) in self._heading_cache:
            return self._heading_cache[str(file_path)]

        headings = set()
        try:
            content = file_path.read_text(encoding="utf-8")
            for match in self.MD_HEADING_PATTERN.finditer(content):
                heading_text = match.group(1).strip()
                anchor = self._normalize_anchor(heading_text)
                headings.add(anchor)
        except Exception as e:
            logger.warning(f"Error reading headings from {file_path}: {e}")

        self._heading_cache[str(file_path)] = headings
        return headings

    def _build_file_cache(self) -> None:
        """Build cache of all files in KB."""
        self._file_cache.clear()
        for file_path in self.kb_path.rglob("*"):
            if file_path.is_file():
                rel_path = file_path.relative_to(self.kb_path)
                self._file_cache.add(str(rel_path).replace("\\", "/"))

    def _classify_link(self, link: str) -> LinkType:
        """Classify a link by type."""
        if link.startswith("#"):
            return LinkType.ANCHOR

        parsed = urlparse(link)
        if parsed.scheme in ("http", "https"):
            return LinkType.EXTERNAL

        # Check if it's an image
        lower_link = link.lower()
        if any(
            lower_link.endswith(ext)
            for ext in [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"]
        ):
            return LinkType.IMAGE

        return LinkType.INTERNAL

    def _resolve_relative_path(self, source_file: Path, target: str) -> str:
        """Resolve a relative path from source file."""
        # Remove anchor if present
        target_path = target.split("#")[0]
        if not target_path:
            return str(source_file.relative_to(self.kb_path)).replace("\\", "/")

        # Decode URL encoding
        target_path = unquote(target_path)

        # Resolve relative to source file's directory
        source_dir = source_file.parent
        resolved = (source_dir / target_path).resolve()

        try:
            return str(resolved.relative_to(self.kb_path.resolve())).replace("\\", "/")
        except ValueError:
            return target_path

    def _check_internal_link(
        self,
        source_file: Path,
        link_target: str,
        line_number: int,
        link_text: str,
    ) -> LinkResult:
        """Check an internal link."""
        # Split target and anchor
        if "#" in link_target:
            file_part, anchor = link_target.split("#", 1)
        else:
            file_part, anchor = link_target, None

        # Resolve the file path
        if file_part:
            resolved_path = self._resolve_relative_path(source_file, file_part)
            target_file = self.kb_path / resolved_path
        else:
            target_file = source_file
            resolved_path = str(source_file.relative_to(self.kb_path)).replace(
                "\\", "/"
            )

        # Check if file exists
        if file_part and not target_file.exists():
            return LinkResult(
                source_file=str(source_file.relative_to(self.kb_path)),
                line_number=line_number,
                link_text=link_text,
                link_target=link_target,
                link_type=LinkType.INTERNAL,
                status=LinkStatus.BROKEN,
                message=f"File not found: {resolved_path}",
            )

        # Check anchor if present
        if anchor:
            headings = self._get_file_headings(target_file)
            if anchor.lower() not in headings and anchor not in headings:
                return LinkResult(
                    source_file=str(source_file.relative_to(self.kb_path)),
                    line_number=line_number,
                    link_text=link_text,
                    link_target=link_target,
                    link_type=LinkType.INTERNAL,
                    status=LinkStatus.WARNING,
                    message=f"Anchor not found: #{anchor}",
                    details={"available_anchors": list(headings)[:10]},
                )

        return LinkResult(
            source_file=str(source_file.relative_to(self.kb_path)),
            line_number=line_number,
            link_text=link_text,
            link_target=link_target,
            link_type=LinkType.INTERNAL,
            status=LinkStatus.VALID,
            message="OK",
        )

    def _check_anchor_link(
        self,
        source_file: Path,
        link_target: str,
        line_number: int,
        link_text: str,
    ) -> LinkResult:
        """Check an anchor-only link."""
        anchor = link_target[1:]  # Remove leading #
        headings = self._get_file_headings(source_file)

        if anchor.lower() not in headings and anchor not in headings:
            return LinkResult(
                source_file=str(source_file.relative_to(self.kb_path)),
                line_number=line_number,
                link_text=link_text,
                link_target=link_target,
                link_type=LinkType.ANCHOR,
                status=LinkStatus.BROKEN,
                message=f"Anchor not found: {anchor}",
                details={"available_anchors": list(headings)[:10]},
            )

        return LinkResult(
            source_file=str(source_file.relative_to(self.kb_path)),
            line_number=line_number,
            link_text=link_text,
            link_target=link_target,
            link_type=LinkType.ANCHOR,
            status=LinkStatus.VALID,
            message="OK",
        )

    def _check_external_link(
        self,
        source_file: Path,
        link_target: str,
        line_number: int,
        link_text: str,
    ) -> LinkResult:
        """Check an external link (if enabled)."""
        if not self.check_external:
            return LinkResult(
                source_file=str(source_file.relative_to(self.kb_path)),
                line_number=line_number,
                link_text=link_text,
                link_target=link_target,
                link_type=LinkType.EXTERNAL,
                status=LinkStatus.SKIPPED,
                message="External link checking disabled",
            )

        # External checking would require httpx or similar
        # For now, just validate URL format
        try:
            parsed = urlparse(link_target)
            if not parsed.netloc:
                return LinkResult(
                    source_file=str(source_file.relative_to(self.kb_path)),
                    line_number=line_number,
                    link_text=link_text,
                    link_target=link_target,
                    link_type=LinkType.EXTERNAL,
                    status=LinkStatus.WARNING,
                    message="Invalid URL format",
                )

            return LinkResult(
                source_file=str(source_file.relative_to(self.kb_path)),
                line_number=line_number,
                link_text=link_text,
                link_target=link_target,
                link_type=LinkType.EXTERNAL,
                status=LinkStatus.SKIPPED,
                message="External URL validation skipped",
            )
        except Exception as e:
            return LinkResult(
                source_file=str(source_file.relative_to(self.kb_path)),
                line_number=line_number,
                link_text=link_text,
                link_target=link_target,
                link_type=LinkType.EXTERNAL,
                status=LinkStatus.ERROR,
                message=f"URL parse error: {e}",
            )

    def check_file(self, file_path: Path) -> list[LinkResult]:
        """
        Check all links in a single file.

        Args:
            file_path: Path to the markdown file

        Returns:
            List of LinkResult for each link found
        """
        results = []

        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")

            for line_num, line in enumerate(lines, start=1):
                # Check markdown links
                for match in self.MD_LINK_PATTERN.finditer(line):
                    link_text = match.group(1)
                    link_target = match.group(2).strip()

                    link_type = self._classify_link(link_target)

                    if link_type == LinkType.ANCHOR:
                        result = self._check_anchor_link(
                            file_path, link_target, line_num, link_text
                        )
                    elif link_type == LinkType.EXTERNAL:
                        result = self._check_external_link(
                            file_path, link_target, line_num, link_text
                        )
                    else:
                        result = self._check_internal_link(
                            file_path, link_target, line_num, link_text
                        )

                    results.append(result)

                # Check image links
                for match in self.MD_IMAGE_PATTERN.finditer(line):
                    link_text = match.group(1)
                    link_target = match.group(2).strip()

                    link_type = self._classify_link(link_target)
                    if link_type == LinkType.EXTERNAL:
                        result = self._check_external_link(
                            file_path, link_target, line_num, link_text
                        )
                    else:
                        result = self._check_internal_link(
                            file_path, link_target, line_num, link_text
                        )
                        result.link_type = LinkType.IMAGE

                    results.append(result)

        except Exception as e:
            logger.error(f"Error checking file {file_path}: {e}")
            results.append(
                LinkResult(
                    source_file=str(file_path.relative_to(self.kb_path)),
                    line_number=0,
                    link_text="",
                    link_target="",
                    link_type=LinkType.UNKNOWN,
                    status=LinkStatus.ERROR,
                    message=f"File read error: {e}",
                )
            )

        return results

    def check_all(self, pattern: str = "**/*.md") -> LinkReport:
        """
        Check all links in the knowledge base.

        Args:
            pattern: Glob pattern for files to check

        Returns:
            LinkReport with all results
        """
        import time

        start_time = time.monotonic()

        # Build file cache for faster lookups
        self._build_file_cache()

        all_results = []
        files_checked = 0

        for file_path in self.kb_path.glob(pattern):
            if file_path.is_file():
                results = self.check_file(file_path)
                all_results.extend(results)
                files_checked += 1

        duration = (time.monotonic() - start_time) * 1000

        # Count by status
        valid = sum(1 for r in all_results if r.status == LinkStatus.VALID)
        broken = sum(1 for r in all_results if r.status == LinkStatus.BROKEN)
        warning = sum(1 for r in all_results if r.status == LinkStatus.WARNING)
        skipped = sum(1 for r in all_results if r.status == LinkStatus.SKIPPED)

        return LinkReport(
            total_links=len(all_results),
            valid_count=valid,
            broken_count=broken,
            warning_count=warning,
            skipped_count=skipped,
            results=all_results,
            files_checked=files_checked,
            duration_ms=duration,
        )

    def get_broken_links(self) -> list[LinkResult]:
        """Get all broken links from the last check."""
        report = self.check_all()
        return [r for r in report.results if r.status == LinkStatus.BROKEN]

    def clear_cache(self) -> None:
        """Clear internal caches."""
        self._heading_cache.clear()
        self._file_cache.clear()


# Convenience function
def check_links(kb_path: Path | None = None) -> LinkReport:
    """Quick function to check all links in KB."""
    checker = LinkChecker(kb_path=kb_path)
    return checker.check_all()
